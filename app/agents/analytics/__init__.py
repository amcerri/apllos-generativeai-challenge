"""
Analytics agent package initializer

Overview
    Side‑effect‑free initializer for the **analytics** agent. This package will
    contain three stages executed in order: **planner** → **executor** → **normalize**.
    The agent answers tabular questions over Olist data through **safe SQL** using
    an allowlist; the final user response is business‑friendly in pt‑BR.

Design
    - Keep this module lightweight (no I/O, no dynamic imports).
    - Do **not** import submodules here to avoid early side effects/cycles.
    - Provide discovery helpers that return **paths** to stage modules.

Integration
    - Other parts of the app can inspect available stages via `stages()` and
      resolve `stage_path(name)` without importing the stage implementations yet.

Usage
    >>> from app.agents.analytics import stages, has_stage, stage_path
    >>> stages()
    ('planner', 'executor', 'normalize')
    >>> has_stage('planner')
    True
    >>> stage_path('normalize').name
    'normalize.py'
"""

from __future__ import annotations

from pathlib import Path
from typing import Final

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
_BASE_DIR: Final[Path] = Path(__file__).resolve().parent
_STAGES: Final[tuple[str, ...]] = ("planner", "executor", "normalize")

__all__ = [
    "base_dir",
    "stages",
    "has_stage",
    "stage_path",
]


# ---------------------------------------------------------------------------
# Discovery helpers (no I/O)
# ---------------------------------------------------------------------------


def base_dir() -> Path:
    """Return the base directory of the analytics agent package."""

    return _BASE_DIR


def stages() -> tuple[str, ...]:
    """Return the canonical stage module names for the analytics agent."""

    return _STAGES


def has_stage(name: str) -> bool:
    """Whether a given stage name is part of the canonical set."""

    return name in _STAGES


def stage_path(name: str) -> Path:
    """Return the expected file path for a given stage module.

    Example
        `stage_path('planner')` → `app/agents/analytics/planner.py`
    """

    return _BASE_DIR / f"{name}.py"
