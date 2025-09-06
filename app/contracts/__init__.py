"""
Contracts package initializer

Overview
    Lightweight, side‑effect‑free initializer for the contracts layer. In later
    phases this package will expose strict dataclasses for:
      • RouterDecision — router output with deterministic fields/validation
      • Answer         — agent output for user responses (pt‑BR), optional data
    During Phase B we avoid importing submodules to prevent circular imports and
    to keep the foundations build green.

Design
    - No eager imports of submodules; keep this file import‑safe at all times.
    - Provide tiny helpers for discovery without introducing runtime deps.
    - Docstring explains the expected contracts without binding to them yet.

Integration
    - Other packages may use `list_contracts()` to know what will be available
      once contracts land (Phase D), without importing missing modules.

Usage
    >>> from app.contracts import list_contracts, has_contract
    >>> list_contracts()
    ('RouterDecision', 'Answer')
    >>> has_contract('Answer')
    True
"""

from __future__ import annotations

from typing import Final

# Public API (string-based to avoid imports before contracts exist)
__all__ = ["list_contracts", "has_contract"]

# Canonical contract names expected to be exposed later in Phase D.
_EXPECTED_CONTRACTS: Final[tuple[str, ...]] = ("RouterDecision", "Answer")


def list_contracts() -> tuple[str, ...]:
    """Return the canonical contract class names expected in this package.

    Notes
        This returns **strings only** to avoid importing modules that will be
        created in a later phase. It is safe to call at import time.
    """

    return _EXPECTED_CONTRACTS


def has_contract(name: str) -> bool:
    """Whether a given contract is expected to exist in this package."""

    return name in _EXPECTED_CONTRACTS
