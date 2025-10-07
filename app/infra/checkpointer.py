"""
LangGraph native checkpointer backends with safe fallbacks.

Overview
--------
Factory for LangGraph's native checkpoint backends (PostgresSaver). Uses cached
factory pattern for deterministic initialization without global mutable state.
Gracefully degrades to a no-op checkpointer when dependencies or configuration
are missing.

Design
------
- Native LangGraph PostgresSaver with `functools.lru_cache` for deterministic initialization.
- No global mutable state; Settings-based configuration.
- Fallback to no-op saver when backend is unavailable or disabled.

Integration
-----------
- Configured via Pydantic Settings (`app.config.settings.CheckpointerConfig`).
- Returns a saver compatible with LangGraph runtime.
- When not configured or disabled, returns a `_NoopSaver`.

Usage
-----
>>> from app.infra.checkpointer import get_checkpointer
>>> saver = get_checkpointer()
>>> # or with explicit settings
>>> from app.config import _get_settings
>>> settings = _get_settings()
>>> saver = get_checkpointer(
...     enabled=settings.checkpointer.enabled,
...     backend=settings.checkpointer.backend,
...     url=settings.database.url,
...     table=settings.checkpointer.table
... )
"""

from __future__ import annotations

import functools
import logging
import os
from typing import Any

_log = logging.getLogger(__name__)

# Optional LangGraph Postgres saver
_PostgresSaver: Any | None = None
try:  # pragma: no cover - exercised only when langgraph-checkpoint is installed
    from langgraph.checkpoint.postgres import PostgresSaver as _imported_PostgresSaver
except Exception:  # pragma: no cover - keep optional
    _imported_PostgresSaver = None
_PostgresSaver = _imported_PostgresSaver

__all__ = [
    "get_checkpointer",
    "is_noop",
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


@functools.lru_cache(maxsize=1)
def get_checkpointer(
    enabled: bool | None = None,
    backend: str | None = None,
    url: str | None = None,
    table: str | None = None,
) -> Any:
    """Return a configured checkpointer using native LangGraph backends (cached).

    This function uses `functools.lru_cache` to ensure deterministic, side-effect-free
    initialization. The checkpointer is created once and reused across calls with the
    same parameters.

    Parameters
    ----------
    enabled:
        Whether the checkpointer is enabled. If False or None, returns a no-op saver.
        Defaults to environment variable CHECKPOINTER_ENABLED or True.
    backend:
        Backend type ('postgres' or 'noop'). Defaults to environment variable
        CHECKPOINTER_BACKEND or 'postgres'.
    url:
        Database connection string (e.g., 'postgresql://user:pass@host:5432/db').
        Defaults to environment variable DATABASE_URL.
    table:
        Table name for storing checkpoints. Defaults to environment variable
        CHECKPOINTER_TABLE or 'checkpoints'.

    Returns
    -------
    Any
        A LangGraph-compatible checkpointer (PostgresSaver) or a no-op saver.
    """
    # Load configuration from environment if not provided
    if enabled is None:
        env_enabled = os.getenv("CHECKPOINTER_ENABLED")
        if env_enabled is not None:
            enabled = env_enabled.strip().lower() not in {"0", "false", "no", "off"}
        else:
            enabled = True

    if not enabled:
        _log.info("checkpointer disabled; using Noop")
        return _NoopSaver("disabled")

    backend = backend or os.getenv("CHECKPOINTER_BACKEND", "postgres").strip().lower()
    table = table or os.getenv("CHECKPOINTER_TABLE", "checkpoints").strip() or "checkpoints"
    url = url or os.getenv("DATABASE_URL", "").strip()

    if backend != "postgres":
        _log.warning("unknown checkpointer backend '%s'; using Noop", backend)
        return _NoopSaver(f"unknown-backend:{backend}")

    if not url:
        _log.warning("checkpointer.postgres: missing database URL; using Noop")
        return _NoopSaver("missing-db-url")

    if _PostgresSaver is None:
        _log.info("langgraph PostgresSaver not available; using Noop")
        return _NoopSaver("missing-dependency")

    # Create saver using native LangGraph API
    try:
        # Prefer from_conn_string if available (standard API)
        if hasattr(_PostgresSaver, "from_conn_string"):
            saver = _PostgresSaver.from_conn_string(url, table_name=table)
        else:
            # Fallback: direct construction
            saver = _PostgresSaver(url, table_name=table)
        _log.info("PostgresSaver initialized", extra={"table": table, "backend": "postgres"})
        return saver
    except Exception as exc:  # pragma: no cover - defensive around API drift
        _log.exception("failed to initialize Postgres checkpointer; falling back to Noop")
        return _NoopSaver(f"init-error: {exc.__class__.__name__}")


def is_noop(saver: Any) -> bool:
    """Check whether the given saver is a no-op implementation.

    Parameters
    ----------
    saver:
        The saver instance to check.

    Returns
    -------
    bool
        True if the saver is a no-op implementation, False otherwise.
    """
    return isinstance(saver, _NoopSaver)
