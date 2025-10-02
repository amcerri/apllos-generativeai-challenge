"""
LangGraph checkpointer helpers (Postgres with safe fallbacks).

Overview
--------
Thin factory around LangGraph's checkpoint backends. Prefers Postgres when
available and gracefully degrades to a no-op checkpointer if the optional
dependency or configuration is missing.

Design
------
- Optional import of LangGraph Postgres saver (`PostgresSaver`).
- No hard dependency on other internal modules; stdlib logging only.
- Global getter `get_checkpointer()` returns a configured instance or a
  no-op implementation that satisfies the minimal Saver-like surface.

Integration
-----------
- Initialized during application bootstrap using a configuration mapping.
- Returns a saver compatible with LangGraph runtime.
- When not configured or disabled, the returned saver is a `_NoopSaver`.

Usage
-----
>>> from app.infra.checkpointer import configure_from_config, get_checkpointer
>>> cfg = {"database": {"url": "postgresql+psycopg://..."},
...        "checkpointer": {"enabled": True, "backend": "postgres", "table": "checkpoints"}}
>>> configure_from_config(cfg)
>>> saver = get_checkpointer()
"""

from __future__ import annotations

import logging
import os
from collections.abc import Mapping
from typing import Any

_log = logging.getLogger(__name__)

# Optional LangGraph Postgres saver
_PostgresSaver: Any | None = None
try:  # pragma: no cover - exercised only when langgraph-checkpoint is installed
    from langgraph.checkpoint.postgres import PostgresSaver as _imported_PostgresSaver
except Exception:  # pragma: no cover - keep optional
    _imported_PostgresSaver = None
_PostgresSaver = _imported_PostgresSaver

# Global holder (configured at runtime)
_CHECKPOINTER: Any | None = None

__all__ = [
    "is_configured",
    "get_checkpointer",
    "configure_postgres",
    "configure_from_config",
]


class _NoopSaver:
    """Minimal Saver-like object used when checkpointer is disabled or unavailable."""

    def __init__(self, reason: str = "disabled") -> None:
        self.reason = reason

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return f"<NoopCheckpointer reason={self.reason!r}>"

    # The real Postgres saver exposes methods used by LangGraph runtime. We
    # intentionally keep this stub permissive: attribute access will succeed
    # (returning callables that do nothing) to avoid crashes in early bootstrap.
    def __getattr__(self, name: str) -> Any:  # pragma: no cover - defensive
        def _noop(*_args: Any, **_kwargs: Any) -> None:
            return None

        return _noop


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def is_configured() -> bool:
    """Return whether a non-noop checkpointer has been configured."""

    return _CHECKPOINTER is not None and not isinstance(_CHECKPOINTER, _NoopSaver)


def get_checkpointer() -> Any:
    """Return the configured checkpointer or a no-op saver if none was set."""

    return _CHECKPOINTER or _NoopSaver("not-configured")


def configure_postgres(*, url: str, table: str = "checkpoints") -> Any:
    """Configure a Postgres-based checkpointer using LangGraph's PostgresSaver.

    Parameters
    ----------
    url:
        SQLAlchemy/psycopg-style connection string, e.g.,
        ``postgresql+psycopg://user:pass@host:5432/db``.
    table:
        Table name to store checkpoints.
    """

    global _CHECKPOINTER

    if not url:
        _log.warning("checkpointer.postgres: missing database URL; using Noop")
        _CHECKPOINTER = _NoopSaver("missing-db-url")
        return _CHECKPOINTER

    if _PostgresSaver is None:
        _log.info("langgraph PostgresSaver not available; using Noop")
        _CHECKPOINTER = _NoopSaver("missing-dependency")
        return _CHECKPOINTER

    # Create saver using the most common constructor; fall back if signature differs
    try:
        if hasattr(_PostgresSaver, "from_conn_string"):
            saver = _PostgresSaver.from_conn_string(url, table_name=table)
        elif hasattr(_PostgresSaver, "from_connection_string"):
            saver = _PostgresSaver.from_connection_string(url, table_name=table)
        else:
            # Last resort: try direct construction with common keyword
            saver = _PostgresSaver(url, table_name=table)
    except Exception as exc:  # pragma: no cover - defensive around API drift
        _log.exception("failed to initialize Postgres checkpointer; falling back to Noop")
        saver = _NoopSaver(f"init-error: {exc.__class__.__name__}")

    _CHECKPOINTER = saver
    return _CHECKPOINTER


def configure_from_config(cfg: Mapping[str, Any]) -> Any:
    """Configure the checkpointer from a nested config mapping.

    Expected keys (all optional):
        cfg["checkpointer"]["enabled"]: bool
        cfg["checkpointer"]["backend"]: "postgres" | "noop"
        cfg["checkpointer"]["table"]: str
        cfg["database"]["url"]: str

    Returns the configured saver (or a `_NoopSaver`).
    """

    cp = cfg.get("checkpointer", {}) if isinstance(cfg.get("checkpointer"), Mapping) else {}
    db = cfg.get("database", {}) if isinstance(cfg.get("database"), Mapping) else {}

    # Environment overrides (take precedence if present)
    env_enabled = os.getenv("CHECKPOINTER_ENABLED")
    if env_enabled is not None:
        enabled = env_enabled.strip().lower() not in {"0", "false", "no", "off"}
    else:
        enabled = bool(cp.get("enabled", True))

    backend = str(os.getenv("CHECKPOINTER_BACKEND", cp.get("backend", "postgres"))).strip().lower()
    table = str(os.getenv("CHECKPOINTER_TABLE", cp.get("table", "checkpoints"))).strip() or "checkpoints"
    url = (str(db.get("url", "")).strip() or os.getenv("DATABASE_URL", "").strip())

    if not enabled:
        _log.info("checkpointer disabled in config; using Noop")
        _set_noop("disabled")
        return get_checkpointer()

    if backend == "postgres":
        return configure_postgres(url=url, table=table)

    _log.warning("unknown checkpointer backend '%s'; using Noop", backend)
    _set_noop(f"unknown-backend:{backend}")
    return get_checkpointer()


# ---------------------------------------------------------------------------
# Internals
# ---------------------------------------------------------------------------


def _set_noop(reason: str) -> None:
    global _CHECKPOINTER
    _CHECKPOINTER = _NoopSaver(reason)
