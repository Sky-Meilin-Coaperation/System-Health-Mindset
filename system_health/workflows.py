import hashlib
import json
from datetime import UTC, datetime
from typing import Any, Callable
from uuid import uuid4

from system_health.telemetry import collect_system_metrics
from system_health.worm import append_event

WorkflowAction = Callable[[dict[str, Any]], dict[str, Any]]


def _run_system_diagnostic(_: dict[str, Any]) -> dict[str, Any]:
    return {"metrics": collect_system_metrics()}


_WORKFLOWS: dict[str, tuple[str, str, WorkflowAction]] = {
    "system-diagnostic": (
        "System diagnostic",
        "Capture a fresh snapshot of the host and application runtime.",
        _run_system_diagnostic,
    ),
}


def list_workflows() -> list[dict[str, str]]:
    return [
        {"id": workflow_id, "name": name, "description": description}
        for workflow_id, (name, description, _) in _WORKFLOWS.items()
    ]


def run_workflow(workflow_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    try:
        _, _, action = _WORKFLOWS[workflow_id]
    except KeyError:
        raise KeyError(workflow_id) from None

    run_id = str(uuid4())
    started_at = datetime.now(UTC).isoformat()
    append_event(
        {
            "event_type": "workflow.started",
            "workflow_id": workflow_id,
            "run_id": run_id,
        }
    )
    try:
        result = action(payload)
    except Exception as exc:
        append_event(
            {
                "event_type": "workflow.failed",
                "workflow_id": workflow_id,
                "run_id": run_id,
                "error_type": type(exc).__name__,
            }
        )
        raise

    completed_at = datetime.now(UTC).isoformat()
    audit_entry = append_event(
        {
            "event_type": "workflow.completed",
            "workflow_id": workflow_id,
            "run_id": run_id,
            "result_sha256": hashlib.sha256(
                json.dumps(
                    result,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                    allow_nan=False,
                ).encode("utf-8")
            ).hexdigest(),
        }
    )
    return {
        "run_id": run_id,
        "workflow_id": workflow_id,
        "status": "completed",
        "started_at": started_at,
        "completed_at": completed_at,
        "result": result,
        "audit": {"sequence": audit_entry["sequence"], "hash": audit_entry["hash"]},
    }
