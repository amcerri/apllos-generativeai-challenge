"""
Validation helpers

Overview
    Small, dependency‑free helpers for validating and coercing data. Utilities
    are intentionally generic so they can be reused across agents and infra
    without importing external libraries.

Design
    - Stdlib only. No I/O. Pure functions with explicit types.
    - Provide safe coercions (`coerce_int/float/bool`) and common checks
      (`is_non_empty_str`, `within_range`, etc.).
    - Keep error messages short and actionable.

Integration
    - Import and use in planners, supervisors and normalizers to guard inputs.
    - Functions raise `ValueError` for invalid inputs when prefixed with
      `ensure_`.

Usage
    >>> from app.utils.validation import (
    ...   is_non_empty_str, ensure_non_empty_str, coerce_int,
    ...   within_range, ensure_subset, normalize_list_str, safe_limit,
    ... )
    >>> is_non_empty_str(" hello ")
    True
    >>> ensure_non_empty_str("  ok  ", name="agent")
    'ok'
    >>> coerce_int("42", min_value=1, max_value=100)
    42
    >>> within_range(10, 0, 20)
    True
    >>> ensure_subset(["a", "b"], ["a", "b", "c"])  # returns normalized list
    ['a', 'b']
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any, TypeVar

__all__ = [
    "is_non_empty_str",
    "ensure_non_empty_str",
    "is_positive_int",
    "within_range",
    "clamp",
    "coerce_int",
    "coerce_float",
    "coerce_bool",
    "ensure_subset",
    "require_keys",
    "normalize_list_str",
    "safe_limit",
]

TNum = TypeVar("TNum", int, float)


# ---------------------------------------------------------------------------
# String helpers
# ---------------------------------------------------------------------------


def is_non_empty_str(value: Any) -> bool:
    """Return True if value is a non-empty string after stripping."""

    return isinstance(value, str) and bool(value.strip())


def ensure_non_empty_str(value: Any, *, name: str = "value") -> str:
    """Return stripped string or raise `ValueError` if empty/invalid."""

    if not isinstance(value, str):
        raise ValueError(f"{name} must be a string")
    s = value.strip()
    if not s:
        raise ValueError(f"{name} must be a non-empty string")
    return s


# ---------------------------------------------------------------------------
# Numeric helpers
# ---------------------------------------------------------------------------


def is_positive_int(value: Any) -> bool:
    """Return True if value is an int > 0 (bools are excluded)."""

    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def within_range(value: TNum, minimum: TNum | None, maximum: TNum | None) -> bool:
    """Return True if `value` lies within [minimum, maximum] where provided."""

    if (minimum is not None) and (value < minimum):
        return False
    if (maximum is not None) and (value > maximum):
        return False
    return True


def clamp(value: TNum, minimum: TNum | None = None, maximum: TNum | None = None) -> TNum:
    """Clamp `value` into [minimum, maximum] where provided."""

    v = value
    if minimum is not None and v < minimum:
        v = minimum
    if maximum is not None and v > maximum:
        v = maximum
    return v


def coerce_int(
    value: Any,
    default: int | None = None,
    *,
    min_value: int | None = None,
    max_value: int | None = None,
) -> int | None:
    """Best‑effort convert `value` to `int` and validate range.

    Returns `default` when conversion fails and `default` is not None,
    otherwise raises `ValueError`.
    """

    try:
        iv = int(str(value).strip())
    except Exception as err:
        if default is not None:
            return default
        raise ValueError("value is not an integer") from err
    if not within_range(iv, min_value, max_value):
        raise ValueError("integer out of allowed range")
    return iv


def coerce_float(
    value: Any,
    default: float | None = None,
    *,
    min_value: float | None = None,
    max_value: float | None = None,
) -> float | None:
    """Best‑effort convert `value` to `float` and validate range."""

    try:
        fv = float(str(value).strip())
    except Exception as err:
        if default is not None:
            return default
        raise ValueError("value is not a float") from err
    if not within_range(fv, min_value, max_value):
        raise ValueError("float out of allowed range")
    return fv


def coerce_bool(value: Any, default: bool | None = None) -> bool | None:
    """Best‑effort convert common string/int representations to bool.

    Recognizes: 1/0, true/false, yes/no, on/off (case‑insensitive).
    Returns `default` when conversion fails and `default` is not None,
    otherwise raises `ValueError`.
    """

    if isinstance(value, bool):
        return value
    if isinstance(value, int | float):
        return bool(int(value))
    if isinstance(value, str):
        s = value.strip().lower()
        if s in {"1", "true", "t", "yes", "y", "on"}:
            return True
        if s in {"0", "false", "f", "no", "n", "off"}:
            return False
    if default is not None:
        return default
    raise ValueError("value is not a recognized boolean literal")


# ---------------------------------------------------------------------------
# Collections and mapping helpers
# ---------------------------------------------------------------------------


def normalize_list_str(
    values: Iterable[Any] | None,
    *,
    lower: bool = False,
    unique: bool = True,
    non_empty: bool = True,
) -> list[str]:
    """Normalize an iterable to a list[str] with optional lower/unique filters."""

    if not values:
        return []
    out: list[str] = []
    seen: set[str] = set()
    for v in values:
        s = str(v).strip()
        if lower:
            s = s.lower()
        if non_empty and not s:
            continue
        if unique:
            if s in seen:
                continue
            seen.add(s)
        out.append(s)
    return out


def ensure_subset(
    values: Iterable[str],
    allowed: Iterable[str],
    *,
    casefold: bool = False,
    name: str = "values",
) -> list[str]:
    """Return list(values) if all items are in `allowed`; else raise ValueError.

    Preserves input order and de‑duplicates items.
    """

    norm = (lambda s: s.casefold()) if casefold else (lambda s: s)
    allowed_set = {norm(str(a)) for a in allowed}
    out: list[str] = []
    seen: set[str] = set()
    for v in values:
        sv = str(v)
        nv = norm(sv)
        if nv not in allowed_set:
            raise ValueError(f"{name} contains a disallowed item: {sv!r}")
        if nv in seen:
            continue
        seen.add(nv)
        out.append(sv)
    return out


def require_keys(mapping: Mapping[str, Any], required: Iterable[str]) -> None:
    """Raise ValueError if any required key is missing from `mapping`."""

    missing = [k for k in required if k not in mapping]
    if missing:
        raise ValueError(f"missing required keys: {', '.join(missing)}")


# ---------------------------------------------------------------------------
# Domain-specific shorthands
# ---------------------------------------------------------------------------


def safe_limit(
    limit: Any,
    *,
    default: int = 200,
    min_value: int = 1,
    max_value: int = 1000,
) -> int:
    """Coerce a LIMIT‑like integer while enforcing sane boundaries."""

    try:
        iv = coerce_int(limit, min_value=min_value, max_value=max_value)
    except ValueError:
        iv = default
    if iv is None:
        iv = default
    return clamp(iv, min_value, max_value)
