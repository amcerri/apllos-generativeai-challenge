"""
HTTP API server (FastAPI façade over LangGraph server and infra endpoints).

Overview
  Exposes a minimal FastAPI app with health/readiness, optional Prometheus
  metrics, and mounts the LangGraph Server handlers at `/graph`. Designed to be
  import-safe when dependencies are unavailable (falls back to a stub).

Design
  - Dependency-light at import time; guards all optional deps.
  - CORS configurable via env: `API_ENABLE_CORS`, `API_ALLOWED_ORIGINS`.
  - Metrics (optional): mounts `/metrics` when metrics infra is available.
  - Health endpoints: `/health`, `/ready`, and `/ok` (DB/checkpointer check).
  - Local runner: `run()` uses Uvicorn when invoked as a script.

Integration
  - `get_app(settings)` returns an ASGI app for embedding or serving.
  - Mounts LangGraph handlers created from `app.graph.assistant.get_assistant`.

Usage
  >>> from app.api.server import get_app
  >>> app = get_app()
  >>> isinstance(app, dict) or hasattr(app, "router")
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
    from app.infra.metrics import configure_metrics, asgi_metrics_app, metrics_available
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
    def configure_metrics(*_a: object, **_k: object) -> None:  # type: ignore
        return
    def asgi_metrics_app():  # type: ignore
        return None
    def metrics_available() -> bool:  # type: ignore
        return False

__all__ = ["get_app", "run"]

# ---------------------------------------------------------------------------
# Config helpers
# ---------------------------------------------------------------------------
_TRUE_SET: Final[set[str]] = {"1", "true", "yes", "on"}


def _as_bool(v: Any, default: bool) -> bool:
    """Coerce arbitrary input to a boolean with a default fallback.

    Accepts common string representations ("1", "true", "yes", "on") as true and
    ("0", "false", "no", "off") as false; returns the provided default otherwise.
    """
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
    """Return an ASGI application exposing health, metrics and `/graph`.

    When optional dependencies are missing, returns a lightweight assistant
    stub so callers can still interact with the graph representation.
    """
    log = get_logger("api.server")

    # Single guard: if dependencies are not available, return assistant stub
    if not _DEPS_AVAILABLE:
        return get_assistant(settings)

    allow_cors = _as_bool(os.environ.get("API_ENABLE_CORS"), True)
    allowed_origins = os.environ.get("API_ALLOWED_ORIGINS", "*").strip()
    origin_list = [o.strip() for o in allowed_origins.split(",") if o.strip()] or ["*"]

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
                allow_origins=origin_list,
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

        @app.get("/ok", tags=["infra"], include_in_schema=False)
        def ok() -> dict[str, str]:
            """Extended health: checks DB and checkpointer availability."""
            db_ok = False
            cp_ok = False
            try:
                from app.infra.db import open_connection
                with open_connection() as conn:
                    conn.exec_driver_sql("SELECT 1")
                    db_ok = True
            except Exception:
                db_ok = False
            try:
                from app.infra.checkpointer import get_checkpointer, is_noop
                cp = get_checkpointer()
                cp_ok = not is_noop(cp)
            except Exception:
                cp_ok = False
            return {"status": "ok", "db": "ok" if db_ok else "down", "checkpointer": "ok" if cp_ok else "noop"}

        # Metrics endpoint (optional)
        try:
            configure_metrics(namespace="apllos", subsystem="api")
            mapp = asgi_metrics_app()
            if mapp is not None:
                app.mount("/metrics", mapp)
                log.info("Prometheus metrics mounted", extra={"path": "/metrics"})
        except Exception:
            pass

        # Mount LangGraph Server handlers
        try:
            assistant = get_assistant(settings)
            lg_app = create_server(assistant)
            app.mount("/graph", lg_app)
            log.info("LangGraph handlers mounted", extra={"path": "/graph"})
        except Exception as exc:  # defensive: server still usable
            log.exception("failed to mount langgraph handlers", extra={"error": type(exc).__name__})

        return app


# ---------------------------------------------------------------------------
# Local runner (optional)
# ---------------------------------------------------------------------------


def run() -> None:  # pragma: no cover - manual use only
    """Run the API server locally using Uvicorn with environment defaults."""
    if not _DEPS_AVAILABLE or uvicorn is None:
        return
    app = get_app()
    host = os.environ.get("API_HOST", "0.0.0.0")
    port = int(os.environ.get("API_PORT", "8000"))
    uvicorn.run(app, host=host, port=port, log_level=os.environ.get("UVICORN_LOG_LEVEL", "info"))


if __name__ == "__main__":  # pragma: no cover - convenience
    run()
