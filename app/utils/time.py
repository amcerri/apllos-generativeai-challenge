"""
Time utilities

Overview
--------
Essential time helpers using stdlib datetime and time modules.
Focuses on UTC datetime handling and monotonic clock operations.

Design
------
- Stdlib only (`datetime`, `time`).
- Always return **aware UTC** datetimes when constructing/parsing.
- Essential API: UTC datetime handling, monotonic clocks, and basic conversions.

Integration
-----------
- Safe to import early; no I/O. Complements `app.utils.utc_now`.

Usage
-----
>>> from app.utils.time import (
...     as_utc, parse_iso8601, format_iso8601,
...     monotonic_now, has_expired, remaining_ms,
... )
>>> dt = parse_iso8601("2024-01-02T03:04:05Z")
>>> format_iso8601(dt)
'2024-01-02T03:04:05Z'
>>> monotonic_now() > 0
True
"""

from __future__ import annotations

import time as _time
from datetime import UTC, datetime
from typing import Final

__all__: Final[list[str]] = [
    "as_utc",
    "parse_iso8601",
    "format_iso8601",
    "monotonic_now",
    "has_expired",
    "remaining_ms",
]


# ---------------------------------------------------------------------------
# Datetime conversions
# ---------------------------------------------------------------------------


def as_utc(dt: datetime, *, assume_naive_utc: bool = True) -> datetime:
    """Return `dt` as an **aware** UTC datetime.

    If `dt` is naive and `assume_naive_utc=True` (default), interpret as UTC.
    If `dt` is naive and `assume_naive_utc=False`, raise `ValueError`.
    """

    if dt.tzinfo is None:
        if not assume_naive_utc:
            raise ValueError("naive datetime provided and assume_naive_utc=False")
        return dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


# ---------------------------------------------------------------------------
# ISO‑8601 parsing/formatting
# ---------------------------------------------------------------------------


def parse_iso8601(value: str) -> datetime | None:
    """Parse a subset of ISO‑8601/RFC3339 into an aware UTC datetime.

    Accepts 'Z' or numeric offsets. Returns `None` when parsing fails.
    Examples: "2024-01-02T03:04:05Z", "2024-01-02T03:04:05+00:00".
    """

    if not value:
        return None
    s = str(value).strip()
    if not s:
        return None
    try:
        # Support trailing Z by normalizing to +00:00 for fromisoformat
        s_norm = s[:-1] + "+00:00" if s.endswith("Z") else s
        dt = datetime.fromisoformat(s_norm)
        # fromisoformat returns naive when no offset is present; interpret as UTC
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC)
        return dt.astimezone(UTC)
    except Exception:
        return None


def format_iso8601(dt: datetime, *, ms: bool = False) -> str:
    """Return UTC datetime as RFC3339 string with trailing 'Z'.

    If `ms=True`, include milliseconds.
    """

    dtu = as_utc(dt)
    if ms:
        # Ensure three fractional digits
        frac = f"{int(dtu.microsecond / 1000):03d}"
        return dtu.strftime("%Y-%m-%dT%H:%M:%S.") + frac + "Z"
    return dtu.strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# Monotonic clocks & deadlines
# ---------------------------------------------------------------------------


def monotonic_now() -> float:
    """Return the current value of a monotonic clock (seconds as float)."""

    return _time.monotonic()


def has_expired(start_monotonic: float, timeout_ms: int) -> bool:
    """Return True if the time elapsed since `start_monotonic` exceeds timeout."""

    if timeout_ms <= 0:
        return True
    elapsed_ms = (monotonic_now() - float(start_monotonic)) * 1000.0
    return elapsed_ms >= float(timeout_ms)


def remaining_ms(start_monotonic: float, timeout_ms: int) -> int:
    """Return remaining time in milliseconds (never negative)."""

    if timeout_ms <= 0:
        return 0
    elapsed_ms = (monotonic_now() - float(start_monotonic)) * 1000.0
    rem = int(timeout_ms - elapsed_ms)
    return rem if rem > 0 else 0
