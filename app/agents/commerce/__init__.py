"""
Commerce agent package initializer

Overview
    Side‑effect‑free initializer for the **commerce** agent. This package will
    contain three stages executed in order: **detector** → **extractor** → **summarizer**.
    The agent normalizes heterogeneous commercial documents (PO/Order Form/BEO/
    invoice, etc.) into a canonical schema and produces a humanized summary in
    pt‑BR with risks/insights when applicable.

Design
    - Keep this module lightweight (no I/O, no dynamic imports).
    - Do **not** import submodules here to avoid early side effects/cycles.
    - Provide discovery helpers that return **paths** to stage modules.

Integration
    - Other parts of the app can inspect available stages via `stages()` and
      resolve `stage_path(name)` without importing the stage implementations yet.

Usage
    >>> from app.agents.commerce import stages, has_stage, stage_path
    >>> stages()
    ('detector', 'extractor', 'summarizer')
    >>> has_stage('extractor')
    True
    >>> stage_path('summarizer').name
    'summarizer.py'
"""

from __future__ import annotations

from pathlib import Path
from typing import Final

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
_BASE_DIR: Final[Path] = Path(__file__).resolve().parent
_STAGES: Final[tuple[str, ...]] = ("detector", "extractor", "summarizer")

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
    """Return the base directory of the commerce agent package."""

    return _BASE_DIR


def stages() -> tuple[str, ...]:
    """Return the canonical stage module names for the commerce agent."""

    return _STAGES


def has_stage(name: str) -> bool:
    """Whether a given stage name is part of the canonical set."""

    return name in _STAGES


def stage_path(name: str) -> Path:
    """Return the expected file path for a given stage module.

    Example
        `stage_path('detector')` → `app/agents/commerce/detector.py`
    """

    return _BASE_DIR / f"{name}.py"
