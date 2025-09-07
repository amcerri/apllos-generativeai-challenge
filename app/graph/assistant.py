"""
Assistant factory (entrypoint for LangGraph Server / Studio).

Overview
--------
Expose a single function `get_assistant()` that returns a compiled LangGraph
for our multi‑agent assistant (analytics, knowledge, commerce, triage). The
builder is delegated to `app.graph.build.build_graph`, and this module only
collects runtime switches (e.g., human‑in‑the‑loop gates) from optional
settings or environment variables.

Design
------
- Keep import‑time side effects minimal and optional.
- Provide resilient fallbacks for logging/tracing and for the graph builder.
- Make configuration discoverable via function argument or environment.

Integration
-----------
LangGraph Server should import: `app.graph.assistant:get_assistant`.

Usage
-----
>>> from app.graph.assistant import get_assistant
>>> graph = get_assistant({"require_sql_approval": False})
>>> bool(graph)
True
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from typing import Any, Final

# ---------------------------------------------------------------------------
# Optional infra: logging & tracing with safe fallbacks
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
# Graph builder (optional import)
# ---------------------------------------------------------------------------
try:
    from app.graph.build import build_graph as _build_graph
except Exception:  # pragma: no cover - optional

    def _build_graph(*, require_sql_approval: bool = True) -> Any:
        return {"engine": "stub", "nodes": [], "require_sql_approval": bool(require_sql_approval)}


__all__ = ["get_assistant"]

# ---------------------------------------------------------------------------
# Configuration helpers
# ---------------------------------------------------------------------------
_TRUE_SET: Final[set[str]] = {"1", "true", "yes", "on"}
_FALSE_SET: Final[set[str]] = {"0", "false", "no", "off"}


def _as_bool(v: Any, default: bool) -> bool:
    if isinstance(v, bool):
        return v
    if v is None:
        return default
    s = str(v).strip().lower()
    if s in _TRUE_SET:
        return True
    if s in _FALSE_SET:
        return False
    return default


def _get_require_sql_approval(settings: Mapping[str, Any] | None) -> bool:
    # 1) Explicit function argument
    if settings and "require_sql_approval" in settings:
        return _as_bool(settings.get("require_sql_approval"), True)

    # 2) Nested settings keys (defensive)
    if settings:
        runtime = settings.get("runtime") if isinstance(settings, Mapping) else None
        if isinstance(runtime, Mapping) and "require_sql_approval" in runtime:
            return _as_bool(runtime.get("require_sql_approval"), True)

    # 3) Environment variables (first hit wins)
    for key in ("ASSISTANT_REQUIRE_SQL_APPROVAL", "REQUIRE_SQL_APPROVAL"):
        if key in os.environ:
            return _as_bool(os.environ.get(key), True)

    # 4) Default
    return True


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def get_assistant(settings: Mapping[str, Any] | None = None) -> Any:
    """Return a compiled graph (or stub) ready for LangGraph Server.

    Parameters
    ----------
    settings: Optional mapping with runtime switches.
    """
    log = get_logger("graph.assistant")

    require_sql_approval = _get_require_sql_approval(settings)

    with start_span("assistant.get", {"require_sql_approval": require_sql_approval}):
        graph = _build_graph(require_sql_approval=require_sql_approval)
        try:
            log.info(
                "Assistant graph ready",
                require_sql_approval=require_sql_approval,
                has_nodes=bool(getattr(graph, "nodes", None)),
            )
        except Exception:
            pass
        return graph


if __name__ == "__main__":  # pragma: no cover - convenience
    log = get_logger("graph.assistant")
    g = get_assistant({"require_sql_approval": False})
    kind = "compiled" if hasattr(g, "__class__") else "stub"
    try:
        log.info("assistant ready", kind=kind, require_sql_approval=False)
    except Exception:
        pass
