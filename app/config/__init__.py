"""
Configuration package.

Overview
--------
Centralized configuration management for the application with modular
configuration system and environment variable override support.

Design
------
- YAML-based configuration files with comprehensive settings
- Environment variable override support using ${VAR_NAME:-default} syntax
- Type-safe configuration via Pydantic Settings
- Cached configuration loading to avoid repeated file I/O

Integration
-----------
Used by all application components that need configuration values.
Replaces hardcoded values throughout the codebase.

Usage
-----
>>> from app.config.settings import get_settings
>>> settings = get_settings()
>>> settings.analytics.planner.default_limit
200
"""

from __future__ import annotations

from .settings import get_settings as _get_settings


def get_settings() -> dict:
    """Return application settings as a plain dict for broad compatibility."""

    try:
        return _get_settings().model_dump()
    except Exception:
        # Fallback to object; test fixture will handle conversion if needed
        return _get_settings()  # type: ignore[return-value]


# Backwards-compatibility shim: prefer get_settings everywhere
def get_config():  # pragma: no cover - transitional alias
    return get_settings()


__all__ = ["get_settings", "get_config"]