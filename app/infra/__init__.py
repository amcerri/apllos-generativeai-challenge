"""
Infrastructure package initializer

Overview
    Minimal, side‑effect‑free initializer for cross‑cutting infrastructure.
    This package will host modules like logging, tracing, database access and
    the LangGraph checkpointer. We keep this file import‑safe and provide only
    tiny discovery helpers during Phase B.

Design
    - No eager imports of submodules (avoid side effects and circular deps).
    - Rely on stdlib only; callers choose when to initialize infra pieces.
    - Keep helpers focused on path/namespace discovery.

Integration
    - Later phases will add `infra/logging.py`, `infra/tracing.py`, `infra/db.py`
      and `infra/checkpointer.py`. This initializer must not assume they exist
      yet; it merely documents the expected components.

Usage
    >>> from app.infra import components, has_component, component_path
    >>> components()
    ('logging', 'tracing', 'db', 'checkpointer')
    >>> has_component('db')
    True
"""

from __future__ import annotations

from pathlib import Path
from typing import Final

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
_BASE_DIR: Final[Path] = Path(__file__).resolve().parent
_COMPONENTS: Final[tuple[str, ...]] = ("logging", "tracing", "db", "checkpointer")

__all__ = [
    "base_dir",
    "components",
    "has_component",
    "component_path",
]


# ---------------------------------------------------------------------------
# Discovery helpers (no I/O)
# ---------------------------------------------------------------------------


def base_dir() -> Path:
    """Return the base directory of the infra package."""

    return _BASE_DIR


def components() -> tuple[str, ...]:
    """Return the canonical infra components for this project."""

    return _COMPONENTS


def has_component(name: str) -> bool:
    """Whether a given component is part of the canonical set."""

    return name in _COMPONENTS


def component_path(name: str) -> Path:
    """Return the expected file path for a given component module.

    Notes
        This function does not assert existence; it is safe to call in Phase B
        before the actual modules are created. Example:
        `component_path('logging')` → `app/infra/logging.py`
    """

    return _BASE_DIR / f"{name}.py"
