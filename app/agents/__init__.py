"""
Agents package initializer

Overview
    Minimal, side‑effect‑free initializer for agent packages. This project
    defines four specialized agents: analytics, knowledge, commerce and triage.
    We provide tiny discovery helpers without importing subpackages to avoid
    early side effects during Phase B.

Design
    - Stdlib‑only; no I/O or dynamic imports here.
    - Keep naming aligned with the architecture and routing rules.
    - Return **paths** to agent packages rather than importing them.

Integration
    - Other modules can resolve `agent_path(name)` and later import from there
      when implementations are added in subsequent phases.

Usage
    >>> from app.agents import agents, has_agent, agent_path
    >>> agents()
    ('analytics', 'knowledge', 'commerce', 'triage')
    >>> has_agent('analytics')
    True
    >>> agent_path('knowledge').name
    'knowledge'
"""

from __future__ import annotations

from pathlib import Path
from typing import Final

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
_BASE_DIR: Final[Path] = Path(__file__).resolve().parent
_AGENTS: Final[tuple[str, ...]] = ("analytics", "knowledge", "commerce", "triage")

__all__ = [
    "base_dir",
    "agents",
    "has_agent",
    "agent_path",
]


# ---------------------------------------------------------------------------
# Discovery helpers (no I/O)
# ---------------------------------------------------------------------------


def base_dir() -> Path:
    """Return the base directory of the agents package."""

    return _BASE_DIR


def agents() -> tuple[str, ...]:
    """Return the canonical agent package names."""

    return _AGENTS


def has_agent(name: str) -> bool:
    """Whether a given name is one of the canonical agents."""

    return name in _AGENTS


def agent_path(name: str) -> Path:
    """Return the directory path for a given agent package.

    Notes
        This does not assert existence; callers decide when to create/verify.
    """

    return _BASE_DIR / name
