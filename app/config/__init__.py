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
- Type-safe configuration access with dedicated accessor methods
- Cached configuration loading to avoid repeated file I/O

Integration
-----------
Used by all application components that need configuration values.
Replaces hardcoded values throughout the codebase.

Usage
-----
>>> from app.config import get_config
>>> config = get_config()
>>> timeout = config.get_llm_timeout("analytics_planner")
>>> max_tokens = config.get_llm_max_tokens("commerce_extractor")
"""

from __future__ import annotations

from .loader import ConfigLoader, get_config, reload_config

__all__ = ["ConfigLoader", "get_config", "reload_config"]