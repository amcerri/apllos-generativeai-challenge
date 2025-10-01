"""
Database helpers (SQLAlchemy with safe, optional dependency).

Overview
    Minimal utilities to configure and access a SQLAlchemy engine for Postgres
    (or any SQLAlchemy-supported backend). Prefers read-only connections for
    analytics workloads by setting Postgres session flags when possible.

Design
    - Optional import of SQLAlchemy; errors are raised only when used.
    - No imports from other internal modules; stdlib logging only.
    - Provide small, composable functions: configure, get/close engine, and a
      context manager for connections.

Integration
    - Call `configure_from_config(cfg)` at bootstrap.
    - Obtain the engine via `get_engine()` or a connection with
      `open_connection(readonly=True)`.
    - If no URL is provided in config, falls back to env var 
      
      DATABASE_URL.

Usage
    >>> from app.infra.db import configure_from_config, get_engine, open_connection
    >>> cfg = {"database": {"url": "postgresql+psycopg://user:pass@localhost:5432/app",
    ...                     "pool_size": 10, "pool_timeout_sec": 10}}
    >>> configure_from_config(cfg)
    >>> engine = get_engine()
    >>> with open_connection() as conn:
    ...     result = conn.exec_driver_sql("SELECT 1").scalar()
    ...     assert result == 1
"""

from __future__ import annotations

import logging
import os
from collections.abc import Mapping
from contextlib import contextmanager
from typing import Any, TYPE_CHECKING, Iterator

if TYPE_CHECKING:  # pragma: no cover - typing-only import
    try:
        from sqlalchemy.engine import Connection as _SAConnection  # type: ignore
    except Exception:  # SQLAlchemy may be absent at type-check time
        _SAConnection = Any  # type: ignore

# Optional SQLAlchemy import
_sa: Any | None = None
try:  # pragma: no cover - exercised only when SQLAlchemy is installed
    import sqlalchemy as _imported_sa
except Exception:  # pragma: no cover - keep optional
    _imported_sa = None
_sa = _imported_sa

_log = logging.getLogger(__name__)
_ENGINE: Any | None = None

__all__ = [
    "engine_is_configured",
    "get_engine",
    "close_engine",
    "configure_engine",
    "configure_from_config",
    "open_connection",
]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def engine_is_configured() -> bool:
    """Return whether a SQLAlchemy engine has been configured."""

    return _ENGINE is not None


def get_engine() -> Any:
    """Return the configured SQLAlchemy engine or raise if missing."""

    if _ENGINE is None:
        raise RuntimeError("database engine not configured; call configure_from_config() first")
    return _ENGINE


def close_engine() -> None:
    """Dispose the global engine if configured."""

    global _ENGINE
    eng = _ENGINE
    _ENGINE = None
    if eng is not None:
        try:
            eng.dispose()
        except Exception:  # pragma: no cover - defensive
            pass


def configure_engine(
    *,
    url: str,
    pool_size: int | None = None,
    pool_timeout_sec: int | None = None,
    echo: bool | None = None,
    readonly_default: bool = True,
) -> Any:
    """Create and register a global SQLAlchemy engine.

    Parameters
    ----------
    url: SQLAlchemy connection string (e.g., postgresql+psycopg://...)
    pool_size: Optional pool size (default 5 if not provided by SQLAlchemy)
    pool_timeout_sec: Optional pool checkout timeout in seconds
    echo: Enable SQL echoing (debug). If None, read from env `SQL_ECHO`.
    readonly_default: For Postgres, attach `default_transaction_read_only=on` via
                     connection options to encourage read-only sessions.
    """

    global _ENGINE

    if not url:
        raise ValueError("database url must be provided")

    if _sa is None:
        raise ImportError("SQLAlchemy is required to configure the database engine")

    assert _sa is not None

    resolved_echo = (
        (str(echo).lower() in {"1", "true", "yes", "on"})
        if echo is not None
        else _env_bool("SQL_ECHO")
    )

    connect_args: dict[str, Any] = {}
    if readonly_default and url.startswith("postgresql"):
        # Encourage read-only behavior at the session level for Postgres
        opts = "-c default_transaction_read_only=on"
        connect_args["options"] = opts

    create_kwargs: dict[str, Any] = {
        "echo": resolved_echo,
        "connect_args": connect_args,
        "pool_pre_ping": True,  # avoid stale connections
    }
    if pool_size is not None:
        create_kwargs["pool_size"] = int(pool_size)
    if pool_timeout_sec is not None:
        create_kwargs["pool_timeout"] = int(pool_timeout_sec)

    eng = _sa.create_engine(url, **create_kwargs)
    _ENGINE = eng
    _log.info(
        "database engine configured",
        extra={
            "url_dialect": url.split(":", 1)[0],
            "pool_size": pool_size,
            "pool_timeout_sec": pool_timeout_sec,
            "readonly_default": readonly_default,
            "echo": resolved_echo,
        },
    )
    return eng


def configure_from_config(cfg: Mapping[str, Any]) -> Any:
    """Configure the engine from a nested config mapping.

    Expected keys (all optional):
        cfg["database"]["url"]: str
        cfg["database"]["pool_size"]: int
        cfg["database"]["pool_timeout_sec"]: int
    """

    db = cfg.get("database", {}) if isinstance(cfg.get("database"), Mapping) else {}
    url = str(db.get("url", "")).strip()
    if not url:
        url = os.getenv("DATABASE_URL", "").strip()
    pool_size = db.get("pool_size")
    pool_timeout_sec = db.get("pool_timeout_sec")
    echo_opt = db.get("echo")  # bool or str; let configure_engine resolve if None
    readonly_default = bool(db.get("readonly_default", True))

    return configure_engine(
        url=url,
        pool_size=int(pool_size) if isinstance(pool_size, int) else None,
        pool_timeout_sec=int(pool_timeout_sec) if isinstance(pool_timeout_sec, int) else None,
        echo=echo_opt if isinstance(echo_opt, bool) else None,
        readonly_default=readonly_default,
    )


@contextmanager
def open_connection(*, readonly: bool = True) -> Iterator["_SAConnection"]:
    """Yield a DB-API connection from the configured engine.

    For Postgres, `readonly=True` attempts to enforce read-only at session level
    using `SET LOCAL default_transaction_read_only = on`.
    """

    eng = get_engine()
    conn = eng.connect()
    try:
        if readonly:
            try:
                # Works across SQLAlchemy 1.4/2.x using driver-level execution
                conn.exec_driver_sql("SET LOCAL default_transaction_read_only = on")
            except Exception:  # pragma: no cover - non-Postgres or unsupported
                pass
        yield conn
    finally:
        try:
            conn.close()
        except Exception:  # pragma: no cover - defensive
            pass


# ---------------------------------------------------------------------------
# Internals
# ---------------------------------------------------------------------------


def _env_bool(name: str, default: bool = False) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return str(val).strip().lower() in {"1", "true", "t", "yes", "y", "on"}
