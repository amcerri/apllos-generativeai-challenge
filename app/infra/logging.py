"""
Structured logging utilities using structlog.

Overview
--------
Opinionated setup for structured logging with optional JSON output. Provides
a `configure()` function and a `get_logger()` helper that pre-binds a
`component` name and accepts additional context fields (e.g., `thread_id`).

Design
------
- Uses `structlog` with stdlib integration via `ProcessorFormatter`.
- Supports console (human-friendly) or JSON rendering, selectable via
  parameters or environment variables.
- Binds common fields such as `component`, `event`, `thread_id`.

Integration
-----------
- Call `configure()` once at app startup. Then use `get_logger("component")`.
- This module avoids importing other internal packages to remain import-safe.

Usage
-----
>>> from app.infra.logging import configure, get_logger
>>> configure(level="INFO", json=False)
>>> log = get_logger("routing").bind(thread_id="abc123")
>>> log.info("router-started", agent_count=4)
"""

from __future__ import annotations

import logging
import os
import sys
from collections.abc import Iterable, Mapping
from typing import Any

import structlog

# ---------------------------------------------------------------------------
# Constants & defaults
# ---------------------------------------------------------------------------
_DEFAULT_LEVEL = "INFO"
_LEVELS: Mapping[str, int] = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "NOTSET": logging.NOTSET,
}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _parse_level(level: str | int | None) -> int:
    """Return a stdlib logging level (int) from str/int/None.

    Falls back to `_DEFAULT_LEVEL` when value is invalid/None.
    """

    if isinstance(level, int):
        return level
    if isinstance(level, str):
        upper = level.strip().upper()
        if upper in _LEVELS:
            return _LEVELS[upper]
        try:
            # Accept numeric strings like "20"
            return int(upper)
        except ValueError:
            pass
    return _LEVELS[_DEFAULT_LEVEL]


def _shared_processors(json_output: bool) -> list[structlog.types.Processor]:
    return [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True, key="timestamp"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        # Rename `event` to `message` for JSON to align with common conventions
        (structlog.processors.EventRenamer("message") if json_output else (lambda _logger, _name, event_dict: event_dict)),
    ]


def _renderer(json_output: bool) -> structlog.types.Processor:
    if json_output:
        return structlog.processors.JSONRenderer(sort_keys=True, ensure_ascii=False)
    return structlog.dev.ConsoleRenderer()


def _clear_root_handlers() -> None:
    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)
        try:
            h.close()
        except Exception:
            pass


def _is_truthy(v: Any) -> bool:
    """Best-effort boolean parser for env/CLI style values."""
    if isinstance(v, bool):
        return v
    if v is None:
        return False
    return str(v).strip().lower() in {"1", "true", "yes", "on"}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def configure(*, level: str | int | None = None, json: bool | None = None) -> None:
    """Configure stdlib logging and structlog.

    Parameters
    ----------
    level:
        Logging level as string/int. If `None`, uses env `LOG_LEVEL` or INFO.
    json:
        If `True`, emit JSON; if `False`, human-friendly console. If `None`,
        uses env `STRUCTLOG_JSON` (truthy values: 1,true,yes,on).
    """

    env_level = os.getenv("LOG_LEVEL")
    env_json = os.getenv("STRUCTLOG_JSON")

    resolved_level = _parse_level(level if level is not None else env_level)
    resolved_json = json if isinstance(json, bool) else _is_truthy(env_json)

    _clear_root_handlers()

    # ProcessorFormatter integrates stdlib logging with structlog
    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True, key="timestamp"),
        ],
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            *_shared_processors(resolved_json),
            _renderer(resolved_json),
        ],
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logging.basicConfig(level=resolved_level, handlers=[handler])

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True, key="timestamp"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(component: str, **initial_values: Any) -> structlog.stdlib.BoundLogger:
    """Return a structured logger bound to a `component` field.

    Examples
    --------
    >>> log = get_logger("analytics", thread_id="abc123")
    >>> log.info("planner-start", sql="SELECT 1")
    """

    if not component:
        component = "app"
    return structlog.get_logger().bind(component=component, **initial_values)


def bind_context(**kwargs: Any) -> None:
    """Bind fields to the contextvars store for implicit inclusion.

    Useful for request/thread correlation:
    >>> bind_context(thread_id="abc123", request_id="req-42")
    """

    structlog.contextvars.bind_contextvars(**kwargs)


def clear_context(keys: Iterable[str] | None = None) -> None:
    """Clear bound context variables.

    If `keys` is provided, clears only those keys; otherwise clears all.
    """

    if keys:
        structlog.contextvars.unbind_contextvars(*keys)
    else:
        structlog.contextvars.clear_contextvars()


__all__ = [
    "configure",
    "get_logger",
    "bind_context",
    "clear_context",
]
