import hashlib
import hmac
import json
import os
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
import threading
from typing import Any, Iterator

_REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
_DEFAULT_LEDGER_PATH = _REPOSITORY_ROOT / "data" / "L4_organized" / "worm_ledger.jsonl"
_PROCESS_LOCK = threading.Lock()
_GENESIS_HASH = "0" * 64


class LedgerIntegrityError(ValueError):
    """Raised when the WORM ledger cannot be trusted or extended."""


def _ledger_path() -> Path:
    configured_path = os.environ.get("WORM_LEDGER_PATH")
    return Path(configured_path) if configured_path else _DEFAULT_LEDGER_PATH


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _entry_hash(unsigned_entry: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(unsigned_entry)).hexdigest()


@contextmanager
def _locked(ledger_path: Path) -> Iterator[None]:
    lock_path = ledger_path.with_name(ledger_path.name + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with _PROCESS_LOCK, lock_path.open("a+b") as lock_file:
        if os.name == "nt":
            import msvcrt

            lock_file.seek(0, os.SEEK_END)
            if lock_file.tell() == 0:
                lock_file.write(b"\0")
                lock_file.flush()
            lock_file.seek(0)
            msvcrt.locking(lock_file.fileno(), msvcrt.LK_LOCK, 1)
            try:
                yield
            finally:
                lock_file.seek(0)
                msvcrt.locking(lock_file.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def _read_entries(ledger_path: Path) -> list[dict[str, Any]]:
    if not ledger_path.exists():
        return []

    entries: list[dict[str, Any]] = []
    previous_hash = _GENESIS_HASH
    try:
        with ledger_path.open("rb") as ledger_file:
            for line_number, raw_line in enumerate(ledger_file, start=1):
                if not raw_line.endswith(b"\n"):
                    raise LedgerIntegrityError(
                        f"Ledger entry at line {line_number} is incomplete."
                    )
                try:
                    entry = json.loads(raw_line)
                except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                    raise LedgerIntegrityError(
                        f"Ledger entry at line {line_number} is not valid JSON."
                    ) from exc

                if not isinstance(entry, dict) or set(entry) != {
                    "sequence",
                    "timestamp",
                    "event",
                    "previous_hash",
                    "hash",
                }:
                    raise LedgerIntegrityError(
                        f"Ledger entry at line {line_number} has an invalid shape."
                    )
                if (
                    type(entry["sequence"]) is not int
                    or entry["sequence"] != line_number
                    or not isinstance(entry["timestamp"], str)
                    or not isinstance(entry["event"], dict)
                    or entry["previous_hash"] != previous_hash
                    or not isinstance(entry["hash"], str)
                    or len(entry["hash"]) != 64
                    or any(character not in "0123456789abcdef" for character in entry["hash"])
                ):
                    raise LedgerIntegrityError(
                        f"Ledger entry at line {line_number} breaks the hash chain."
                    )

                unsigned_entry = {key: entry[key] for key in entry if key != "hash"}
                try:
                    expected_hash = _entry_hash(unsigned_entry)
                except (TypeError, ValueError) as exc:
                    raise LedgerIntegrityError(
                        f"Ledger entry at line {line_number} cannot be hashed."
                    ) from exc
                if not hmac.compare_digest(expected_hash, entry["hash"]):
                    raise LedgerIntegrityError(
                        f"Ledger entry at line {line_number} has an invalid hash."
                    )
                previous_hash = entry["hash"]
                entries.append(entry)
    except OSError as exc:
        raise LedgerIntegrityError("The WORM ledger could not be read.") from exc
    return entries


def append_event(event: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(event, dict):
        raise TypeError("WORM ledger events must be dictionaries.")
    _canonical_json(event)

    ledger_path = _ledger_path()
    with _locked(ledger_path):
        entries = _read_entries(ledger_path)
        previous_hash = entries[-1]["hash"] if entries else _GENESIS_HASH
        unsigned_entry = {
            "sequence": len(entries) + 1,
            "timestamp": datetime.now(UTC).isoformat(),
            "event": event,
            "previous_hash": previous_hash,
        }
        entry = {**unsigned_entry, "hash": _entry_hash(unsigned_entry)}
        try:
            ledger_path.parent.mkdir(parents=True, exist_ok=True)
            with ledger_path.open("ab") as ledger_file:
                ledger_file.write(_canonical_json(entry) + b"\n")
                ledger_file.flush()
                os.fsync(ledger_file.fileno())
        except OSError as exc:
            raise LedgerIntegrityError("The WORM ledger entry could not be persisted.") from exc
        return entry


def verify_ledger() -> dict[str, Any]:
    ledger_path = _ledger_path()
    if not ledger_path.exists():
        return {"valid": True, "entry_count": 0, "head_hash": None}

    try:
        with _locked(ledger_path):
            entries = _read_entries(ledger_path)
    except LedgerIntegrityError as exc:
        return {"valid": False, "entry_count": None, "head_hash": None, "error": str(exc)}

    return {
        "valid": True,
        "entry_count": len(entries),
        "head_hash": entries[-1]["hash"] if entries else None,
    }
