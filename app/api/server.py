"""
HTTP Server (ASGI) for the multi‑agent assistant.

Overview
--------
Expose an ASGI app compatible with LangGraph Server / Studio. The server mounts
LangGraph's HTTP handlers under `/graph` when available and provides minimal
health endpoints. All dependencies are optional at import time to keep the POC
lightweight and friendly to static checks.

Design
------
- Optional imports for FastAPI, LangGraph and Uvicorn with graceful fallbacks.
- Single factory `get_app(settings)` returning the ASGI app.
- Logs and tracing via infra helpers when present.

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
# Optional infra: logging & tracing (safe fallbacks)
# ---------------------------------------------------------------------------
try:
    from app.infra.logging import get_logger
except Exception:  # pragma: no cover - optional
    import logging as _logging

    def get_logger(component: str, **initial_values: Any) -> Any:  # noqa: D401 - simple fallback
        return _logging.getLogger(component)


start_span: Any
try:
    from app.infra.tracing import start_span as _start_span

    start_span = _start_span
except Exception:  # pragma: no cover - optional
    from contextlib import nullcontext as _nullcontext

    def _fallback_start_span(_name: str, _attrs: dict[str, Any] | None = None):
        return _nullcontext()

    start_span = _fallback_start_span

# ---------------------------------------------------------------------------
# Optional framework & LangGraph imports
# ---------------------------------------------------------------------------
FastAPI: Any
CORSMiddleware: Any
try:
    from fastapi import FastAPI as _FastAPI
    from fastapi.middleware.cors import CORSMiddleware as _CORSMiddleware

    FastAPI = _FastAPI
    CORSMiddleware = _CORSMiddleware
except Exception:  # pragma: no cover - optional
    FastAPI = None
    CORSMiddleware = None

create_server: Any
try:
    from langgraph.server import create_server as _create_server

    create_server = _create_server
except Exception:  # pragma: no cover - optional
    create_server = None

# Assistant factory (optional)
try:
    from app.graph.assistant import get_assistant as _get_assistant

    get_assistant = _get_assistant
except Exception:  # pragma: no cover - optional

    def get_assistant(settings: Mapping[str, Any] | None = None) -> Any:  # fallback stub
        return {"engine": "stub", "nodes": [], "require_sql_approval": True}


# Uvicorn (optional) for local runs via `python -m app.api.server`
try:
    import uvicorn as _uvicorn
except Exception:  # pragma: no cover - optional
    _uvicorn = None

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

    # If FastAPI is not available, return the assistant graph (stub or real) so
    # that callers can still interact programmatically.
    if FastAPI is None:
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

        # CORS (optional, default enabled)
        if allow_cors and "CORSMiddleware" in globals() and CORSMiddleware is not None:
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

        # Mount LangGraph Server handlers, if present
        if create_server is not None:
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
    if _uvicorn is None:
        return
    app = get_app()
    host = os.environ.get("API_HOST", "0.0.0.0")
    port = int(os.environ.get("API_PORT", "8000"))
    _uvicorn.run(app, host=host, port=port, log_level=os.environ.get("UVICORN_LOG_LEVEL", "info"))


if __name__ == "__main__":  # pragma: no cover - convenience
    run()
