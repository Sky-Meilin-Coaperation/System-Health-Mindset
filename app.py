from pathlib import Path
from threading import Lock
from time import monotonic
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from system_health.telemetry import collect_system_metrics
from system_health.workflows import list_workflows, run_workflow

_STARTED_AT = monotonic()
_DASHBOARD_PATH = Path(__file__).parent / "static" / "index.html"
_request_counts = {"total": 0, "errors": 0}
_request_counts_lock = Lock()

app = FastAPI(
    title="System Health Evolution",
    version="1.0.0",
    description="A modular core for system monitoring and workflow automation.",
)


@app.middleware("http")
async def record_request_metrics(
    request: Request, call_next: RequestResponseEndpoint
) -> Response:
    response = await call_next(request)
    with _request_counts_lock:
        _request_counts["total"] += 1
        if response.status_code >= 400:
            _request_counts["errors"] += 1
    return response


@app.get("/", include_in_schema=False)
def dashboard() -> FileResponse:
    return FileResponse(_DASHBOARD_PATH)


@app.get("/health")
def health_check() -> dict[str, Any]:
    return {
        "health": "optimal",
        "status": "healthy",
        "uptime_seconds": round(monotonic() - _STARTED_AT, 2),
    }


@app.get("/api/v1/telemetry")
def get_telemetry() -> dict[str, Any]:
    with _request_counts_lock:
        total_requests = _request_counts["total"]
        error_rate = (
            _request_counts["errors"] / total_requests * 100
            if total_requests
            else 0.0
        )

    metrics = collect_system_metrics()
    return {
        "timestamp": metrics["timestamp"],
        "status": "online",
        "error_rate": round(error_rate, 2),
        "metrics": (
            f"Load (1m): {metrics['load_average_1m']}; "
            f"Memory used: {metrics['memory']['used_percent'] if metrics['memory'] else 'unavailable'}%; "
            f"Disk used: {metrics['disk']['used_percent']}%"
        ),
        "system": metrics,
    }


@app.get("/api/v1/workflows")
def get_workflows() -> dict[str, list[dict[str, str]]]:
    return {"workflows": list_workflows()}


@app.post("/api/v1/workflows/{workflow_id}/trigger")
def trigger_workflow(
    workflow_id: str, payload: dict[str, Any] | None = None
) -> dict[str, Any]:
    try:
        return run_workflow(workflow_id, payload or {})
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Workflow not found") from exc
