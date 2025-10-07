"""
HTTP Server (ASGI) for the multi‑agent assistant.

Overview
--------
Expose an ASGI app compatible with LangGraph Server / Studio. The server mounts
LangGraph's HTTP handlers under `/graph` when available and provides minimal
health endpoints. Uses single guard for optional dependencies with graceful fallbacks.

Design
------
- Single guard for FastAPI/LangGraph unavailability with graceful fallbacks.
- Logs via stdlib logging with start_span no-op fallback.
- Simplified error handling and conditional logic.

Integration
-----------
LangGraph Server may import the graph directly (`app.graph.assistant:get_assistant`).
This module targets local runs and container deployment.

Usage
-----
>>> from app.api.server import get_app
>>> app = get_app({"require_sql_approval": False})
>>> bool(app)
True
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from typing import Any, Final

# ---------------------------------------------------------------------------
# Optional dependencies guard
# ---------------------------------------------------------------------------
_DEPS_AVAILABLE = True
try:
    from app.infra.logging import get_logger
    from app.infra.tracing import start_span
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from langgraph.server import create_server
    from app.graph.assistant import get_assistant
    import uvicorn
except Exception:  # pragma: no cover - optional
    _DEPS_AVAILABLE = False
    import logging as _logging
    from contextlib import nullcontext as _nullcontext
    
    def get_logger(component: str, **initial_values: Any) -> Any:
        return _logging.getLogger(component)
    
    def start_span(_name: str, _attrs: dict[str, Any] | None = None):
        return _nullcontext()
    
    def get_assistant(settings: Mapping[str, Any] | None = None) -> Any:
        return {"engine": "stub", "nodes": [], "require_sql_approval": True}
    
    FastAPI = None
    CORSMiddleware = None
    create_server = None
    uvicorn = None

__all__ = ["get_app", "run"]

# ---------------------------------------------------------------------------
# Config helpers
# ---------------------------------------------------------------------------
_TRUE_SET: Final[set[str]] = {"1", "true", "yes", "on"}


def _as_bool(v: Any, default: bool) -> bool:
    if isinstance(v, bool):
        return v
    if v is None:
        return default
    s = str(v).strip().lower()
    if s in _TRUE_SET:
        return True
    if s in {"0", "false", "no", "off"}:
        return False
    return default


# ---------------------------------------------------------------------------
# Public factory
# ---------------------------------------------------------------------------


def get_app(settings: Mapping[str, Any] | None = None) -> Any:
    """Return an ASGI application exposing the assistant endpoints."""
    log = get_logger("api.server")

    # Single guard: if dependencies are not available, return assistant stub
    if not _DEPS_AVAILABLE:
        return get_assistant(settings)

    allow_cors = _as_bool(os.environ.get("API_ENABLE_CORS"), True)

    with start_span("api.server.build"):
        app = FastAPI(title="POC Multi-Agent Assistant", version="0.1.0")

        @app.get("/", tags=["infra"], include_in_schema=False)
        def index() -> dict[str, str]:
            """Basic landing page to avoid 404 on `/` in local/dev runs."""
            return {
                "service": "POC Multi-Agent Assistant",
                "docs": "/docs",
                "openapi": "/openapi.json",
                "graph": "/graph",
                "health": "/health",
                "ready": "/ready",
            }

        # CORS middleware (simplified conditional)
        if allow_cors:
            app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

        @app.get("/health", tags=["infra"])  # lightweight liveness
        def health() -> dict[str, str]:
            return {"status": "ok"}

        @app.get("/ready", tags=["infra"])  # readiness check
        def ready() -> dict[str, str]:
            return {"status": "ready"}

        # Mount LangGraph Server handlers
        try:
            assistant = get_assistant(settings)
            lg_app = create_server(assistant)
            app.mount("/graph", lg_app)
            log.info("LangGraph handlers mounted", path="/graph")
        except Exception as exc:  # defensive: server still usable
            log.exception("failed to mount langgraph handlers", error=type(exc).__name__)

        return app


# ---------------------------------------------------------------------------
# Local runner (optional)
# ---------------------------------------------------------------------------


def run() -> None:  # pragma: no cover - manual use only
    if not _DEPS_AVAILABLE or uvicorn is None:
        return
    app = get_app()
    host = os.environ.get("API_HOST", "0.0.0.0")
    port = int(os.environ.get("API_PORT", "8000"))
    uvicorn.run(app, host=host, port=port, log_level=os.environ.get("UVICORN_LOG_LEVEL", "info"))


if __name__ == "__main__":  # pragma: no cover - convenience
    run()
