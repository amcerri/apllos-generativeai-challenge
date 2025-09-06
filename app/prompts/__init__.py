"""
Prompts package initializer

Overview
    Minimal, side‑effect‑free initializer for prompt assets. This package will
    host versioned prompt templates for routing and specialized agents.
    We expose small helpers for namespace discovery and path composition without
    reading any files during import.

Design
    - Keep this module lightweight (no I/O, no template parsing).
    - Do not import other internal packages; rely only on stdlib.
    - Namespaces are fixed to match the agents and router: routing, analytics,
      knowledge, commerce.

Integration
    - Callers can use `namespace_path()` and `prompt_path()` to build paths and
      load templates later in the pipeline (e.g., during agent initialization).
    - Works both on host and inside containers; paths are relative to this file.

Usage
    >>> from app.prompts import namespaces, has_namespace, namespace_path
    >>> namespaces()
    ('routing', 'analytics', 'knowledge', 'commerce')
    >>> has_namespace('routing')
    True
    >>> namespace_path('routing').name
    'routing'
"""

from __future__ import annotations

from pathlib import Path
from typing import Final

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
_BASE_DIR: Final[Path] = Path(__file__).resolve().parent
_NAMESPACES: Final[tuple[str, ...]] = ("routing", "analytics", "knowledge", "commerce")

__all__ = [
    "namespaces",
    "has_namespace",
    "base_dir",
    "namespace_path",
    "prompt_path",
]


# ---------------------------------------------------------------------------
# Discovery helpers (no I/O)
# ---------------------------------------------------------------------------


def base_dir() -> Path:
    """Return the base directory of the prompts package."""

    return _BASE_DIR


def namespaces() -> tuple[str, ...]:
    """Return the canonical prompt namespaces for this project."""

    return _NAMESPACES


def has_namespace(name: str) -> bool:
    """Whether a given namespace is part of the canonical set."""

    return name in _NAMESPACES


def namespace_path(name: str) -> Path:
    """Return the directory path for a given prompt namespace.

    Notes
        Does not check for existence; callers decide when to assert or create.
    """

    return _BASE_DIR / name


def prompt_path(namespace: str, *parts: str) -> Path:
    """Compose a path under a given namespace using additional segments.

    Examples
        >>> prompt_path('routing', 'system.txt')  # app/prompts/routing/system.txt
        >>> prompt_path('analytics', 'planner', 'system.txt')
    """

    return namespace_path(namespace) / Path(*parts)
