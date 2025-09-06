"""
Graph package initializer

Overview
    Minimal, side‑effect‑free initializer for the graph runtime. This package
    will host the LangGraph application and the entrypoint consumed by
    LangGraph Server / Studio.

Design
    - Keep this module lightweight (no imports of submodules yet).
    - Provide discovery helpers only; avoid I/O and side effects.
    - Align names with the server import path: `app.graph.assistant:get_assistant`.

Integration
    - External processes may safely import `app.graph` to inspect paths.
    - The concrete `assistant.py` with `get_assistant()` will be added in a
      later phase; this module only documents and resolves its path.

Usage
    >>> from app.graph import entrypoint_module, entrypoint_symbol, module_path
    >>> entrypoint_module()
    'assistant'
    >>> entrypoint_symbol()
    'get_assistant'
    >>> module_path('assistant').name
    'assistant.py'
"""

from __future__ import annotations

from pathlib import Path
from typing import Final

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
_BASE_DIR: Final[Path] = Path(__file__).resolve().parent
_ENTRYPOINT_MODULE: Final[str] = "assistant"
_ENTRYPOINT_SYMBOL: Final[str] = "get_assistant"

__all__ = [
    "base_dir",
    "entrypoint_module",
    "entrypoint_symbol",
    "module_path",
]


# ---------------------------------------------------------------------------
# Discovery helpers (no I/O)
# ---------------------------------------------------------------------------


def base_dir() -> Path:
    """Return the base directory of the graph package."""

    return _BASE_DIR


def entrypoint_module() -> str:
    """Return the canonical module name for the graph entrypoint."""

    return _ENTRYPOINT_MODULE


def entrypoint_symbol() -> str:
    """Return the canonical function name exported by the entrypoint module."""

    return _ENTRYPOINT_SYMBOL


def module_path(name: str) -> Path:
    """Return the expected file path for a given module under `app/graph`.

    Example
        `module_path('assistant')` → `app/graph/assistant.py`
    """

    return _BASE_DIR / f"{name}.py"
