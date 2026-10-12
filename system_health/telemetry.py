from datetime import UTC, datetime
from pathlib import Path
import os
import platform
import shutil
from time import monotonic
from typing import Any

_STARTED_AT = monotonic()
_PROC_MEMINFO = Path("/proc/meminfo")
_CGROUP_MEMORY_FILES = (
    (
        Path("/sys/fs/cgroup/memory.max"),
        Path("/sys/fs/cgroup/memory.current"),
    ),
    (
        Path("/sys/fs/cgroup/memory/memory.limit_in_bytes"),
        Path("/sys/fs/cgroup/memory/memory.usage_in_bytes"),
    ),
)


def _memory_metrics() -> dict[str, int | float | str] | None:
    for limit_path, current_path in _CGROUP_MEMORY_FILES:
        if not limit_path.is_file() or not current_path.is_file():
            continue

        raw_limit = limit_path.read_text(encoding="ascii").strip()
        if raw_limit == "max":
            continue
        total_bytes = int(raw_limit)
        if total_bytes <= 0 or total_bytes >= 1 << 60:
            continue

        used_bytes = int(current_path.read_text(encoding="ascii").strip())
        return {
            "total_bytes": total_bytes,
            "available_bytes": max(total_bytes - used_bytes, 0),
            "used_percent": round(used_bytes / total_bytes * 100, 1),
            "source": "container",
        }

    if not _PROC_MEMINFO.is_file():
        return None

    values: dict[str, int] = {}
    with _PROC_MEMINFO.open(encoding="ascii") as meminfo:
        for line in meminfo:
            key, _, value = line.partition(":")
            if key in {"MemTotal", "MemAvailable"}:
                values[key] = int(value.strip().split()[0]) * 1024

    total_bytes = values.get("MemTotal")
    available_bytes = values.get("MemAvailable")
    if not total_bytes or available_bytes is None:
        return None

    used_bytes = total_bytes - available_bytes
    return {
        "total_bytes": total_bytes,
        "available_bytes": available_bytes,
        "used_percent": round(used_bytes / total_bytes * 100, 1),
        "source": "host",
    }


def _load_average() -> float | None:
    if not hasattr(os, "getloadavg"):
        return None
    return round(os.getloadavg()[0], 2)


def collect_system_metrics() -> dict[str, Any]:
    disk = shutil.disk_usage(Path.cwd())
    return {
        "timestamp": datetime.now(UTC).isoformat(),
        "platform": platform.system().lower(),
        "cpu_count": os.cpu_count(),
        "load_average_1m": _load_average(),
        "memory": _memory_metrics(),
        "disk": {
            "total_bytes": disk.total,
            "free_bytes": disk.free,
            "used_percent": round((disk.total - disk.free) / disk.total * 100, 1),
        },
        "process_uptime_seconds": round(monotonic() - _STARTED_AT, 2),
    }
