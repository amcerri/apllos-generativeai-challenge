"""
Knowledge agent package initializer

Overview
    Side‑effect‑free initializer for the **knowledge** agent (RAG). This package
    will contain three stages executed in order: **retriever** → **ranker** → **answerer**.
    The agent answers with document context and **must include citations** when
    retrieval is used.

Design
    - Keep this module lightweight (no I/O, no dynamic imports).
    - Do **not** import submodules here to avoid early side effects/cycles.
    - Provide discovery helpers that return **paths** to stage modules.

Integration
    - Other parts of the app can inspect available stages via `stages()` and
      resolve `stage_path(name)` without importing the stage implementations yet.
    - Implementations will later use pgvector for embeddings/retrieval.

Usage
    >>> from app.agents.knowledge import stages, has_stage, stage_path
    >>> stages()
    ('retriever', 'ranker', 'answerer')
    >>> has_stage('retriever')
    True
    >>> stage_path('answerer').name
    'answerer.py'
"""

from __future__ import annotations

from pathlib import Path
from typing import Final

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
_BASE_DIR: Final[Path] = Path(__file__).resolve().parent
_STAGES: Final[tuple[str, ...]] = ("retriever", "ranker", "answerer")

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
    """Return the base directory of the knowledge agent package."""

    return _BASE_DIR


def stages() -> tuple[str, ...]:
    """Return the canonical stage module names for the knowledge agent."""

    return _STAGES


def has_stage(name: str) -> bool:
    """Whether a given stage name is part of the canonical set."""

    return name in _STAGES


def stage_path(name: str) -> Path:
    """Return the expected file path for a given stage module.

    Example
        `stage_path('retriever')` → `app/agents/knowledge/retriever.py`
    """

    return _BASE_DIR / f"{name}.py"
