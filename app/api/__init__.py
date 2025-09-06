"""
API package initializer

Overview
    Minimal, side‑effect‑free initializer for the optional HTTP API surface.
    The project primarily runs via LangGraph Server/Studio, but we keep a thin
    FastAPI‑based façade available for integrations when needed.

Design
    - Keep this module lightweight (no I/O, no dynamic imports, stdlib‑only).
    - Do **not** import FastAPI or submodules here to avoid side effects.
    - Provide discovery helpers that resolve **paths** to API modules.

Integration
    - A future `server.py` module may expose a FastAPI app that proxies to the
      LangGraph runtime. This initializer merely documents that expectation and
      offers helpers to locate module paths without importing them.

Usage
    >>> from app.api import modules, has_module, module_path
    >>> modules()
    ('server',)
    >>> has_module('server')
    True
    >>> module_path('server').name
    'server.py'
"""

from __future__ import annotations

from pathlib import Path
from typing import Final

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
_BASE_DIR: Final[Path] = Path(__file__).resolve().parent
_MODULES: Final[tuple[str, ...]] = ("server",)

__all__ = [
    "base_dir",
    "modules",
    "has_module",
    "module_path",
]


# ---------------------------------------------------------------------------
# Discovery helpers (no I/O)
# ---------------------------------------------------------------------------


def base_dir() -> Path:
    """Return the base directory of the API package."""

    return _BASE_DIR


def modules() -> tuple[str, ...]:
    """Return the canonical API module names (thin FastAPI façade expected)."""

    return _MODULES


def has_module(name: str) -> bool:
    """Whether a given API module name is part of the canonical set."""

    return name in _MODULES


def module_path(name: str) -> Path:
    """Return the expected file path for a given API module.

    Example
        `module_path('server')` → `app/api/server.py`
    """

    return _BASE_DIR / f"{name}.py"
