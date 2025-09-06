"""
Routing package initializer

Overview
    Minimal, side‑effect‑free initializer for the routing layer. This package
    will contain the context‑first router (LLM classifier → RouterDecision) and
    the Supervisor that applies deterministic rules and single‑pass fallbacks.

Design
    - No eager imports of submodules (avoid side effects and circular deps).
    - Stdlib‑only; helpers are for discovery/path composition during Phase B.
    - Keep names aligned with later files: allowlist_snapshot, llm_classifier, supervisor.

Integration
    - Other modules can use `node_path()` to resolve the expected file path for
      a routing component without importing it yet.
    - This keeps imports safe until the concrete implementations land in later phases.

Usage
    >>> from app.routing import nodes, has_node, node_path
    >>> nodes()
    ('allowlist_snapshot', 'llm_classifier', 'supervisor')
    >>> has_node('llm_classifier')
    True
"""

from __future__ import annotations

from pathlib import Path
from typing import Final

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
_BASE_DIR: Final[Path] = Path(__file__).resolve().parent
_NODES: Final[tuple[str, ...]] = (
    "allowlist_snapshot",
    "llm_classifier",
    "supervisor",
)

__all__ = [
    "base_dir",
    "nodes",
    "has_node",
    "node_path",
]


# ---------------------------------------------------------------------------
# Discovery helpers (no I/O)
# ---------------------------------------------------------------------------


def base_dir() -> Path:
    """Return the base directory of the routing package."""

    return _BASE_DIR


def nodes() -> tuple[str, ...]:
    """Return the canonical routing components (files expected later)."""

    return _NODES


def has_node(name: str) -> bool:
    """Whether a given routing component name is part of the canonical set."""

    return name in _NODES


def node_path(name: str) -> Path:
    """Return the expected file path for a given routing component module.

    Example
        `node_path('llm_classifier')` → `app/routing/llm_classifier.py`
    """

    return _BASE_DIR / f"{name}.py"
