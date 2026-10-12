import os
import sys
import json
import hashlib
import datetime
from pathlib import Path

# UTF-8 Encoding fuer Windows Konsole sicherstellen
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

class SecurityAgent:
    """
    SkyOS WORM Security Agent (Proof of Prior Art)
    Verankert System-Assets revisionssicher in einer fortlaufenden SHA-256 Hashchain.
    """
    def __init__(self, workspace_dir=None):
        if workspace_dir is None:
            self.workspace_dir = Path(__file__).resolve().parent
        else:
            self.workspace_dir = Path(workspace_dir)
            
        self.ledger_file = self.workspace_dir / "data" / "L4_organized" / "worm_ledger.jsonl"
        self.ledger_file.parent.mkdir(parents=True, exist_ok=True)

    def get_last_hash(self) -> str:
        """Liest den Hash des vorherigen Blocks aus der Kette."""
        if not self.ledger_file.exists():
            return "0" * 64  # Genesis Vorgaenger-Hash
        
        last_line = ""
        with open(self.ledger_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    last_line = line.strip()
        
        if not last_line:
            return "0" * 64
        
        try:
            data = json.loads(last_line)
            return data.get("current_hash", "0" * 64)
        except Exception:
            return "0" * 64

    def register_asset(self, event_type: str, target_file: str, description: str = ""):
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        target_path = Path(target_file)
        if not target_path.is_absolute():
            file_path = self.workspace_dir / target_path
        else:
            file_path = target_path

        file_sha256 = "FILE_NOT_FOUND"
        if file_path.exists() and file_path.is_file():
            hasher = hashlib.sha256()
            with open(file_path, "rb") as f:
                while chunk := f.read(8192):
                    hasher.update(chunk)
            file_sha256 = hasher.hexdigest()

        previous_hash = self.get_last_hash()

        payload = {
            "timestamp_utc": timestamp,
            "event_type": event_type,
            "target_file": str(target_file),
            "file_sha256": file_sha256,
            "previous_hash": previous_hash,
            "description": description
        }

        current_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
        payload["current_hash"] = current_hash

        with open(self.ledger_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")

        print(f"[WORM GUARD] Signiert: {target_file}")
        print(f"             |-- Asset-Hash: {file_sha256[:16]}...")
        print(f"             |-- Prev-Hash:  {previous_hash[:16]}...")
        print(f"             +-- WORM Block: {current_hash}")
        return payload

if __name__ == "__main__":
    agent = SecurityAgent()
    event_type = sys.argv[1] if len(sys.argv) > 1 else "PRIOR_ART_PROOF"
    target = sys.argv[2] if len(sys.argv) > 2 else "LICENSE"
    desc = sys.argv[3] if len(sys.argv) > 3 else "Initialer WORM Prioritaetsnachweis fuer SkyOS Sustainable Use License v1.0"
    
    agent.register_asset(event_type, target, desc)
