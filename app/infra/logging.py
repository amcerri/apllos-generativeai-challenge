"""
Logging utilities (stdlib-only implementation).

Overview
--------
Opinionated setup for structured logging with optional JSON output using the
Python standard library only. Provides a `configure()` function and a
`get_logger()` helper that returns a logger with a `bind()` method compatible
with prior usages.

Design
------
- Stdlib `logging` with a lightweight adapter that supports `bind(**context)`.
- Optional JSON rendering selectable via parameters or environment variables.
- Context propagation via `contextvars` (`bind_context` / `clear_context`).

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
from typing import Any, Final
import contextvars
import json

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

# Context store for implicit fields (e.g., trace_id, thread_id)
_CTX: Final[contextvars.ContextVar[dict[str, Any]]] = contextvars.ContextVar(
    "app_logging_context", default={}
)


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


class _JsonFormatter(logging.Formatter):
    """Minimal JSON formatter.

    Emits a JSON object with standard fields and any extra attributes attached
    to the `LogRecord` (excluding dunder/private and standard ones).
    """

    def format(self, record: logging.LogRecord) -> str:  # noqa: D401 - simple
        base = {
            "timestamp": self.formatTime(record, datefmt="%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # Merge implicit context stored in contextvars
        ctx = _CTX.get().copy()
        # Collect extras directly set via LoggerAdapter/extra
        extras = {
            k: v
            for k, v in record.__dict__.items()
            if not k.startswith("_")
            and k
            not in {
                "name",
                "msg",
                "args",
                "levelname",
                "levelno",
                "pathname",
                "filename",
                "module",
                "exc_info",
                "exc_text",
                "stack_info",
                "lineno",
                "funcName",
                "created",
                "msecs",
                "relativeCreated",
                "thread",
                "threadName",
                "processName",
                "process",
            }
        }
        payload = {**base, **ctx, **extras}
        try:
            return json.dumps(payload, ensure_ascii=False, sort_keys=True)
        except Exception:
            # Fallback to best-effort string conversion for non-serializable extras
            for k, v in list(payload.items()):
                try:
                    json.dumps(v)
                except Exception:
                    payload[k] = str(v)
            return json.dumps(payload, ensure_ascii=False, sort_keys=True)


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


class _BoundLogger(logging.LoggerAdapter):
    """Logger adapter that supports `.bind(**kwargs)` to accumulate context.

    The adapter stores bound context in `self.extra` and merges it with
    `contextvars` content and per-call kwargs.
    """

    def bind(self, **kwargs: Any) -> "_BoundLogger":  # noqa: D401 - fluent API
        merged = {**self.extra, **kwargs}
        return _BoundLogger(self.logger, merged)

    # Ensure kwargs passed in logging calls are merged into extra
    def process(self, msg: str, kwargs: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        call_extra = kwargs.pop("extra", {}) or {}
        # Hoist all non-standard kwargs into `extra` to avoid TypeError in stdlib
        # Keep only recognized logging kwargs in `kwargs` (exc_info, stack_info, stacklevel)
        recognized = {"exc_info", "stack_info", "stacklevel"}
        arbitrary: dict[str, Any] = {}
        for k in list(kwargs.keys()):
            if k not in recognized:
                arbitrary[k] = kwargs.pop(k)
        # Merge: bound -> contextvars -> call_extra -> arbitrary
        merged_extra = {**self.extra, **_CTX.get(), **call_extra, **arbitrary}
        # Attach component prefix to logger name if provided
        if "component" in merged_extra and not self.logger.name:
            self.logger.name = str(merged_extra["component"])  # type: ignore[attr-defined]
        kwargs["extra"] = merged_extra
        return msg, kwargs


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def configure(*, level: str | int | None = None, json: bool | None = None) -> None:
    """Configure standard library logging.

    Parameters
    ----------
    level : str | int | None
        Logging level as string/int. If `None`, uses env `LOG_LEVEL` or INFO.
    json : bool | None
        If `True`, emit JSON; if `False`, human-friendly console. If `None`,
        uses env `STRUCTLOG_JSON` (truthy values: 1,true,yes,on).
    """

    env_level = os.getenv("LOG_LEVEL")
    env_json = os.getenv("STRUCTLOG_JSON")

    resolved_level = _parse_level(level if level is not None else env_level)
    resolved_json = json if isinstance(json, bool) else _is_truthy(env_json)

    _clear_root_handlers()

    handler = logging.StreamHandler(sys.stdout)
    if resolved_json:
        handler.setFormatter(_JsonFormatter())
    else:
        # Console-friendly format with time, level, logger and message
        fmt = "%(asctime)s %(levelname)s %(name)s: %(message)s"
        datefmt = "%Y-%m-%dT%H:%M:%S%z"
        handler.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))

    logging.basicConfig(level=resolved_level, handlers=[handler])


def get_logger(component: str, **initial_values: Any) -> _BoundLogger:
    """Return a logger adapter bound to a `component` field.

    Parameters
    ----------
    component : str
        Component name to bind on the logger.
    **initial_values : Any
        Extra context to bind to this logger instance.

    Returns
    -------
    _BoundLogger
        Logger adapter supporting `.bind(**kwargs)`.
    """

    if not component:
        component = "app"
    base = logging.getLogger(component)
    return _BoundLogger(base, {"component": component, **initial_values})


def bind_context(**kwargs: Any) -> None:
    """Bind fields to the contextvars store for implicit inclusion.

    Useful for request/thread correlation:
    >>> bind_context(thread_id="abc123", request_id="req-42")
    """

    ctx = _CTX.get().copy()
    ctx.update(kwargs)
    _CTX.set(ctx)


def clear_context(keys: Iterable[str] | None = None) -> None:
    """Clear bound context variables.

    If `keys` is provided, clears only those keys; otherwise clears all.
    """

    if keys:
        ctx = _CTX.get().copy()
        for k in keys:
            ctx.pop(str(k), None)
        _CTX.set(ctx)
    else:
        _CTX.set({})


__all__ = [
    "configure",
    "get_logger",
    "bind_context",
    "clear_context",
]
