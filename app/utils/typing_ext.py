"""
Typing extensions and common aliases

Overview
    Shared typing utilities and aliases used across the project. Prefer modern
    Python 3.11+ features (e.g., X | Y unions) and keep this module stdlib‑only.

Design
    - Provide JSON‑related aliases (recursive) for serialization contracts.
    - Small utility protocols (e.g., `SupportsToDict`).
    - Lightweight helpers like `is_json_compatible` and common TypeVars.

Integration
    - Safe to import early; no side effects. Modules can rely on these aliases
      without depending on external packages.

Usage
    >>> from app.utils.typing_ext import JSONValue, SupportsToDict, StrPath
    >>> def to_payload(x: JSONValue) -> JSONValue:  # doctest: +SKIP
    ...     return x
"""

from __future__ import annotations

import os
from collections.abc import Mapping, MutableMapping, MutableSequence, Sequence
from typing import (
    Any,
    Protocol,
    TypeVar,
    runtime_checkable,
)

# ---------------------------------------------------------------------------
# Type variables
# ---------------------------------------------------------------------------
T = TypeVar("T")
R = TypeVar("R")


# ---------------------------------------------------------------------------
# Common aliases
# ---------------------------------------------------------------------------
# Pathlike strings
StrPath = str | os.PathLike[str]

# JSON types (recursive). Keep names explicit for readability.
JSONScalar = str | int | float | bool | None
JSONValue = JSONScalar | dict[str, "JSONValue"] | list["JSONValue"]
JSONArray = list[JSONValue]
JSONObject = dict[str, JSONValue]

__all__ = [
    "T",
    "R",
    "StrPath",
    "JSONScalar",
    "JSONValue",
    "JSONArray",
    "JSONObject",
    "SupportsToDict",
    "SupportsStr",
    "is_json_compatible",
]


# ---------------------------------------------------------------------------
# Protocols
# ---------------------------------------------------------------------------
@runtime_checkable
class SupportsToDict(Protocol):
    """Objects that can export themselves as a plain dict."""

    def to_dict(self) -> dict[str, Any]:  # pragma: no cover - structural typing
        ...


@runtime_checkable
class SupportsStr(Protocol):
    """Objects that provide a meaningful string representation."""

    def __str__(self) -> str:  # pragma: no cover - structural typing
        ...


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def is_json_compatible(value: Any) -> bool:
    """Return True if *value* fits the JSONValue alias (by structural check).

    Accepts primitives, lists/tuples, and mappings with string keys. For objects
    exposing `to_dict()`, the function validates the returned mapping.
    """

    # Primitives
    if isinstance(value, str | int | float | bool) or value is None:
        return True

    # Mappings with string keys
    if isinstance(value, Mapping):
        for k, v in value.items():
            if not isinstance(k, str) or not is_json_compatible(v):
                return False
        return True

    # Sequences (but not str/bytes/bytearray)
    if isinstance(value, Sequence) and not isinstance(value, str | bytes | bytearray):
        for item in value:
            if not is_json_compatible(item):
                return False
        return True

    # Mutable variants (for completeness)
    if isinstance(value, MutableMapping | MutableSequence):
        return (
            is_json_compatible(dict(value))
            if isinstance(value, MutableMapping)
            else is_json_compatible(list(value))
        )

    # Objects with to_dict()
    if hasattr(value, "to_dict") and callable(value.to_dict):
        try:
            as_dict = value.to_dict()
        except Exception:
            return False
        return is_json_compatible(as_dict)

    return False
