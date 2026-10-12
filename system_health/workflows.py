from datetime import UTC, datetime
from typing import Any, Callable
from uuid import uuid4

from system_health.telemetry import collect_system_metrics

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

    return {
        "run_id": str(uuid4()),
        "workflow_id": workflow_id,
        "status": "completed",
        "started_at": datetime.now(UTC).isoformat(),
        "result": action(payload),
    }
