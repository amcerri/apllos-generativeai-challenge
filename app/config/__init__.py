"""
Configuration package initializer

Overview
    Minimal, side‑effect‑free utilities for locating and reading configuration
    during early phases. Provides helpers for resolving the project root,
    composing the default config path, loading YAML safely, and reading
    environment variables with type coercion.

Design
    - Keep this module lightweight (no eager file I/O on import).
    - Do not import other internal packages yet to avoid circular deps.
    - All helpers are optional utilities; callers control when to read files.

Integration
    - Later phases may build higher-level config objects on top of these helpers
      (e.g., loading thresholds from config.yaml or env overrides).
    - Works both inside containers and on the host.

Usage
    >>> from app.config import default_config_path, load_yaml, env_bool
    >>> default_config_path().name
    'config.yaml'
    >>> env_bool('TRACING_ENABLED', False)
    False
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Final

# Defer import errors until a function that needs yaml is called.
yaml: Any | None = None
try:
    import yaml as _yaml  # runtime import; stubs provided via types-PyYAML

    yaml = _yaml
except Exception:  # pragma: no cover - surfaced only when PyYAML isn't installed
    pass

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DEFAULT_CONFIG_FILENAME: Final[str] = "config.yaml"
ROOT_MARKERS: Final[tuple[str, ...]] = ("pyproject.toml", ".git")

__all__ = [
    "DEFAULT_CONFIG_FILENAME",
    "find_project_root",
    "default_config_path",
    "load_yaml",
    "env_str",
    "env_int",
    "env_bool",
]


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------


def find_project_root(start: Path | None = None) -> Path:
    """Return the repository/project root by walking upwards.

    The first directory containing any of the ROOT_MARKERS is considered the root.
    If none is found, returns the current working directory (or `start` if given).
    """

    here = Path(start or Path.cwd()).resolve()
    for parent in (here, *here.parents):
        for marker in ROOT_MARKERS:
            if (parent / marker).exists():
                return parent
    return here


def default_config_path() -> Path:
    """Return the default path to `config.yaml` at the project root."""

    return find_project_root() / DEFAULT_CONFIG_FILENAME


# ---------------------------------------------------------------------------
# File I/O (opt-in)
# ---------------------------------------------------------------------------


def load_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML file safely and return a dictionary.

    Notes
        - Returns an empty dict if the file does not exist.
        - Raises the underlying exception for malformed YAML.
        - ImportError for PyYAML is raised only when this function is invoked.
    """

    if not path.exists():
        return {}
    if yaml is None:  # pragma: no cover
        raise ImportError("PyYAML is required to load YAML configuration.")
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data or {}


# ---------------------------------------------------------------------------
# Environment helpers
# ---------------------------------------------------------------------------


def env_str(key: str, default: str | None = None) -> str | None:
    """Read an environment variable as string with an optional default."""

    return os.getenv(key, default)


def env_int(key: str, default: int | None = None) -> int | None:
    """Read an environment variable as int with an optional default.

    Non-integer values fall back to the default.
    """

    val = os.getenv(key)
    if val is None:
        return default
    try:
        return int(val)
    except ValueError:
        return default


def env_bool(key: str, default: bool | None = None) -> bool | None:
    """Read an environment variable and coerce to bool.

    Truthy: '1', 'true', 't', 'yes', 'y', 'on'
    Falsy:  '0', 'false', 'f', 'no', 'n', 'off'
    Case-insensitive; other values return the default.
    """

    val = os.getenv(key)
    if val is None:
        return default
    norm = val.strip().lower()
    if norm in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if norm in {"0", "false", "f", "no", "n", "off"}:
        return False
    return default
