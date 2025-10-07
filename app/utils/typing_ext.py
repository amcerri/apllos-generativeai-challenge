"""
Typing extensions and common aliases

Overview
--------
Essential typing utilities using modern Python 3.11+ features.
Focuses on JSON serialization contracts and essential protocols.

Design
------
- Provide JSON‑related aliases (recursive) for serialization contracts.
- Essential protocols (e.g., `SupportsToDict`).
- Lightweight helpers for JSON compatibility checking.

Integration
-----------
- Safe to import early; no side effects. Modules can rely on these aliases
  without depending on external packages.

Usage
-----
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
    Final,
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

__all__: Final[list[str]] = [
    "T",
    "R",
    "StrPath",
    "JSONScalar",
    "JSONValue",
    "JSONArray",
    "JSONObject",
    "SupportsToDict",
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




# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def is_json_compatible(value: Any) -> bool:
    """Return True if *value* fits the JSONValue alias (by structural check).

    Accepts primitives, lists/tuples, and mappings with string keys.
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

    return False
