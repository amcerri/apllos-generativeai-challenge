"""
Triage agent package initializer

Overview
    Side‑effect‑free initializer for the **triage** agent. The triage agent is a
    lightweight path when there isn’t enough context for other agents; it offers
    brief guidance and objective next steps to unlock routing.

Design
    - Keep this module minimal (no I/O, no dynamic imports, stdlib‑only).
    - Unlike other agents, triage intentionally has **no fixed stages** in this POC.
    - Provide discovery helpers consistent with other agent packages.

Integration
    - Other parts of the app can rely on this package being import‑safe at all
      times. If we later add a small module (e.g., `responder.py`), callers can
      resolve its path via `module_path(name)`.

Usage
    >>> from app.agents.triage import modules, has_module
    >>> modules()
    ()
    >>> has_module('responder')
    False
"""

from __future__ import annotations

from pathlib import Path
from typing import Final

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
_BASE_DIR: Final[Path] = Path(__file__).resolve().parent
_MODULES: Final[tuple[str, ...]] = ()  # no fixed modules in this POC phase

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
    """Return the base directory of the triage agent package."""

    return _BASE_DIR


def modules() -> tuple[str, ...]:
    """Return the known modules for the triage agent (empty in this POC phase)."""

    return _MODULES


def has_module(name: str) -> bool:
    """Whether a given module name belongs to the triage agent set (currently none)."""

    return name in _MODULES


def module_path(name: str) -> Path:
    """Return the expected file path for a future triage module.

    Example
        `module_path('responder')` → `app/agents/triage/responder.py`
    """

    return _BASE_DIR / f"{name}.py"
