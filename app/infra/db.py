"""
Database helpers (SQLAlchemy with safe, optional dependency).

Overview
--------
Minimal utilities to configure and access a SQLAlchemy engine for Postgres
(or any SQLAlchemy-supported backend). Uses cached factory pattern to avoid
global mutable state and improve testability.

Design
------
- Optional import of SQLAlchemy; errors are raised only when used.
- No imports from other internal modules; stdlib logging only.
- Cached engine factory using functools.lru_cache for deterministic behavior.
- Provide small, composable functions: get_engine, open_connection, and ensure_db.

Integration
-----------
- Call `ensure_db()` at bootstrap to initialize database connection.
- Obtain the engine via `get_engine(dsn, ...)` with cached factory.
- Use `open_connection(readonly=True)` for database operations.
- If no URL is provided, falls back to env var DATABASE_URL.

Usage
-----
>>> from app.infra.db import ensure_db, get_engine, open_connection
>>> ensure_db()  # Initialize database connection
>>> engine = get_engine()  # Get cached engine
>>> with open_connection() as conn:
...     result = conn.exec_driver_sql("SELECT 1").scalar()
...     assert result == 1
"""

from __future__ import annotations

import functools
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

__all__ = [
    "get_engine",
    "open_connection",
    "ensure_db",
]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


@functools.lru_cache(maxsize=1)
def get_engine(
    *,
    url: str | None = None,
    pool_size: int | None = None,
    pool_timeout_sec: int | None = None,
    echo: bool | None = None,
    readonly_default: bool = False,
) -> Any:
    """Get a cached SQLAlchemy engine with the specified parameters.
    
    Parameters
    ----------
    url: SQLAlchemy connection string. If None, uses DATABASE_URL env var.
    pool_size: Optional pool size (default 5 if not provided by SQLAlchemy)
    pool_timeout_sec: Optional pool checkout timeout in seconds
    echo: Enable SQL echoing (debug). If None, read from env `SQL_ECHO`.
    readonly_default: For Postgres, attach `default_transaction_read_only=on` via
                     connection options to encourage read-only sessions.
    
    Returns
    -------
    SQLAlchemy Engine instance
    
    Raises
    ------
    ImportError: If SQLAlchemy is not available
    ValueError: If no database URL is provided and DATABASE_URL is not set
    """
    
    if _sa is None:
        raise ImportError("SQLAlchemy is required to create database engine")
    
    if not url:
        url = os.getenv("DATABASE_URL", "").strip()
        if not url:
            raise ValueError("database url must be provided or DATABASE_URL env var must be set")
        
        # Convert postgresql+psycopg:// to postgresql:// for SQLAlchemy
        if url.startswith("postgresql+psycopg://"):
            url = url.replace("postgresql+psycopg://", "postgresql://")
        
        # Convert Docker internal hostname for external access
        if "@db:" in url:
            url = url.replace("@db:", "@host.docker.internal:")
    
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
    _log.info(
        "database engine created",
        extra={
            "url_dialect": url.split(":", 1)[0],
            "pool_size": pool_size,
            "pool_timeout_sec": pool_timeout_sec,
            "readonly_default": readonly_default,
            "echo": resolved_echo,
        },
    )
    return eng


def ensure_db() -> None:
    """Ensure database connection is available.
    
    This function initializes the database connection by creating a cached engine.
    It's safe to call multiple times and will not recreate the engine if already cached.
    
    Raises
    ------
    ImportError: If SQLAlchemy is not available
    ValueError: If no database URL is provided and DATABASE_URL is not set
    """
    
    # Try to get engine to ensure it's cached
    try:
        get_engine()
    except Exception:
        # No database configured, which is acceptable for some use cases
        pass


@contextmanager
def open_connection(*, readonly: bool = True) -> Iterator["_SAConnection"]:
    """Yield a DB-API connection from the cached engine.

    For Postgres, `readonly=True` attempts to enforce read-only at session level
    using `SET LOCAL default_transaction_read_only = on`.
    
    Parameters
    ----------
    readonly: bool, default True
        Whether to enforce read-only mode for the connection
        
    Yields
    ------
    SQLAlchemy connection object
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
