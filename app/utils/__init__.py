"""
Utilities package initializer

Overview
    Small, dependency‑free helpers used across the project. This module is kept
    side‑effect‑free and safe to import early. Utilities here are intentionally
    generic (time, ids, coercion, string ops, JSON helpers) and avoid importing
    any internal packages during Phase B.

Design
    - **Stdlib‑first**: prefer Python stdlib; optional `orjson` when available.
    - **No I/O, no globals**: functions only; no runtime initialization.
    - **Type‑hinted** and narrow scope to keep linting strict and usage clear.

Integration
    - These helpers are used by infra/agents later but do not depend on them.
    - JSON helpers fall back to the stdlib `json` seamlessly when `orjson` is absent.

Usage
    >>> from app.utils import utc_now, short_uuid, truncate, safe_json_dumps
    >>> isinstance(utc_now().tzinfo, object)
    True
    >>> len(short_uuid())
    8
    >>> truncate("hello world", 8)
    'hello…'
    >>> safe_json_dumps({"b": 1, "a": 2})
    '{"a":2,"b":1}'
"""

from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime
from typing import Any

# Optional fast JSON — import if available without type-ignores
_orjson: Any | None = None
try:  # pragma: no cover - exercised when orjson is installed
    import orjson as _imported_orjson
except Exception:
    _imported_orjson = None
_orjson = _imported_orjson

__all__ = [
    "utc_now",
    "short_uuid",
    "coerce_int",
    "coerce_float",
    "is_truthy",
    "truncate",
    "safe_json_dumps",
    "safe_json_loads",
]

# ---------------------------------------------------------------------------
# Time & IDs
# ---------------------------------------------------------------------------


def utc_now() -> datetime:
    """Return an aware UTC datetime suitable for timestamps and logs."""

    return datetime.now(UTC)


def short_uuid(length: int = 8) -> str:
    """Return a lowercase hex short id derived from UUID4 (default 8 chars).

    Notes
        The resulting string is not a cryptographic identifier; it is for UI/logs.
    """

    if length <= 0:
        return ""
    return uuid.uuid4().hex[:length]


# ---------------------------------------------------------------------------
# Coercion helpers
# ---------------------------------------------------------------------------


def coerce_int(value: Any, default: int | None = None) -> int | None:
    """Best‑effort conversion to int; returns `default` on failure."""

    try:
        if value is None:
            return default
        if isinstance(value, bool):  # avoid True -> 1 surprises unless desired
            return int(value)
        return int(str(value).strip())
    except (ValueError, TypeError):
        return default


def coerce_float(value: Any, default: float | None = None) -> float | None:
    """Best‑effort conversion to float; returns `default` on failure."""

    try:
        if value is None:
            return default
        if isinstance(value, bool):
            return float(value)
        return float(str(value).strip())
    except (ValueError, TypeError):
        return default


def is_truthy(value: Any) -> bool | None:
    """Coerce common truthy/falsey representations to `bool`.

    Returns `None` for unknown/empty values to let callers decide defaults.
    """

    if value is None:
        return None
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if not text:
        return None
    if text in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if text in {"0", "false", "f", "no", "n", "off"}:
        return False
    return None


# ---------------------------------------------------------------------------
# Strings
# ---------------------------------------------------------------------------


def truncate(text: str, max_len: int, suffix: str = "…") -> str:
    """Return `text` truncated to `max_len`, appending `suffix` if truncated.

    If `max_len` is shorter than the suffix, the suffix is returned alone.
    """

    if max_len <= 0:
        return ""
    if len(text) <= max_len:
        return text
    if len(suffix) >= max_len:
        return suffix[:max_len]
    return text[: max_len - len(suffix)] + suffix


# ---------------------------------------------------------------------------
# JSON helpers (fast path with orjson, fallback to stdlib)
# ---------------------------------------------------------------------------


def safe_json_dumps(obj: Any) -> str:
    """Serialize `obj` to a compact JSON string with stable key ordering.

    - Uses `orjson` if available (fast) with sorted keys.
    - Falls back to `json.dumps(..., ensure_ascii=False, sort_keys=True)`.
    - Non‑serializable objects are coerced via `str()` in the fallback path.
    """

    if _orjson is not None:  # pragma: no cover - behavior exercised in prod
        # orjson sorts keys via OPT_SORT_KEYS and returns bytes
        return _orjson.dumps(obj, option=_orjson.OPT_SORT_KEYS).decode("utf-8")
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, default=str)


def safe_json_loads(s: str) -> Any:
    """Deserialize JSON string `s` into Python objects.

    Uses `orjson` if present; otherwise falls back to `json.loads`.
    """

    if _orjson is not None:  # pragma: no cover
        return _orjson.loads(s)
    return json.loads(s)
