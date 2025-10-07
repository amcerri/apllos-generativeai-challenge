"""
Validation helpers.

Overview
--------
Domain-specific validation utilities that complement Pydantic's native
validation. This module provides specialized helpers that don't fit well
into Pydantic models, such as safe limit clamping for SQL queries.

Design
------
- Stdlib only. No I/O. Pure functions with explicit types.
- Focus on domain-specific utilities (e.g., `safe_limit` for SQL).
- Use Pydantic for structured validation (see `pydantic.BaseModel`).
- Keep error messages short and actionable.

Integration
-----------
- Import and use for specialized validation needs beyond Pydantic.
- For structured data validation, prefer Pydantic models with Field validators.
- Functions raise `ValueError` for invalid inputs.

Usage
-----
>>> from app.utils.validation import safe_limit, clamp
>>> safe_limit(5000)  # Returns 1000 (clamped to max)
1000
>>> safe_limit(10, min_value=1, max_value=100)
10
>>> clamp(150, minimum=0, maximum=100)
100
"""

from __future__ import annotations

from typing import Any, TypeVar, Final

__all__: Final[list[str]] = [
    "clamp",
    "safe_limit",
]

TNum = TypeVar("TNum", int, float)


# ---------------------------------------------------------------------------
# Numeric helpers
# ---------------------------------------------------------------------------


def clamp(value: TNum, minimum: TNum | None = None, maximum: TNum | None = None) -> TNum:
    """Clamp `value` into [minimum, maximum] where provided.
    
    Parameters
    ----------
    value : int | float
        The value to clamp
    minimum : int | float | None
        Minimum allowed value (inclusive)
    maximum : int | float | None
        Maximum allowed value (inclusive)
        
    Returns
    -------
    int | float
        Clamped value within [minimum, maximum]
        
    Examples
    --------
    >>> clamp(150, minimum=0, maximum=100)
    100
    >>> clamp(5, minimum=10, maximum=20)
    10
    >>> clamp(15, minimum=10, maximum=20)
    15
    """
    
    v = value
    if minimum is not None and v < minimum:
        v = minimum
    if maximum is not None and v > maximum:
        v = maximum
    return v


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
    """Coerce a LIMIT‑like integer while enforcing sane boundaries.
    
    This is a domain-specific helper for SQL LIMIT clauses that ensures
    the limit is always a reasonable value, preventing accidentally huge
    result sets or invalid values.
    
    Parameters
    ----------
    limit : Any
        Value to coerce into a safe limit
    default : int, default 200
        Default value if coercion fails
    min_value : int, default 1
        Minimum allowed limit
    max_value : int, default 1000
        Maximum allowed limit
        
    Returns
    -------
    int
        Safe limit value within [min_value, max_value]
        
    Examples
    --------
    >>> safe_limit(5000)  # Returns 1000 (clamped to max)
    1000
    >>> safe_limit(10, min_value=1, max_value=100)
    10
    >>> safe_limit("invalid", default=50)
    50
    >>> safe_limit(None, default=100)
    100
    """
    
    try:
        iv = int(str(limit).strip())
    except Exception:
        iv = default
    
    return clamp(iv, min_value, max_value)
