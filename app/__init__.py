"""
Apllos Assistant — package initializer

Overview
    Minimal, side‑effect‑free initializer for the LangGraph-based engineering assistant.
    It exposes package metadata and tiny helpers. It intentionally avoids importing
    subpackages to prevent early side effects and circular imports during Phase B.

Design
    - Keep this module lightweight: no heavy imports or I/O.
    - Do not import internal submodules here (they will be created in later phases).
    - Provide a single source of truth for package identity and version helpers.

Integration
    - External tools (e.g., LangGraph Server/Studio) may import `app` safely.
    - Future entrypoints (e.g., `app.graph.assistant:get_assistant`) are not imported here
      to avoid premature initialization.

Usage
    >>> import app
    >>> app.__package_name__
    'apllos-generativeai-challenge'
    >>> app.__version__
    '0.1.0'  # or the installed distribution version
    >>> app.get_version()
    '0.1.0'
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version
from typing import Final

# Package identity (kept in sync with pyproject.toml `project.name`)
__package_name__: Final[str] = "apllos-generativeai-challenge"

# Resolve the installed distribution version if available; fall back to the dev default.
try:
    __version__: str = version(__package_name__)
except PackageNotFoundError:
    # Dev fallback (matches pyproject.toml `project.version` during Phase B)
    __version__ = "0.1.0"

__all__ = [
    "__package_name__",
    "__version__",
    "get_version",
    "get_package_info",
]


def get_version() -> str:
    """Return the package version string.

    This is a tiny convenience to avoid importing importlib.metadata across the codebase.
    """

    return __version__


def get_package_info() -> dict[str, str]:
    """Return basic package info (name and version).

    Notes
        Keep this minimal; expand only if needed by telemetry or diagnostics later on.
    """

    return {"name": __package_name__, "version": __version__}
