"""
Configuration settings for the frontend application.

This module provides configuration management for the Chainlit frontend,
including server URLs, timeouts, and UI settings.
"""

from __future__ import annotations

import os
from pathlib import Path


# Project root directory (two levels up from this file)
PROJECT_ROOT = Path(__file__).parent.parent

# Public assets directory
PUBLIC_DIR = PROJECT_ROOT / "public"

# LangGraph Server configuration
LANGGRAPH_SERVER_URL = os.getenv(
    "LANGGRAPH_SERVER_URL", "http://localhost:2024"
)

# Polling configuration
POLLING_INTERVAL_SECONDS = float(os.getenv("POLLING_INTERVAL_SECONDS", "1.0"))
POLLING_TIMEOUT_SECONDS = int(os.getenv("POLLING_TIMEOUT_SECONDS", "300"))

# UI Configuration
UI_NAME = os.getenv("UI_NAME", "Assistente Apllos")
UI_DESCRIPTION = os.getenv(
    "UI_DESCRIPTION",
    "Sistema multi-agente inteligente para análises, conhecimento e processamento de documentos",
)

# Asset paths
LOGO_PATH = PUBLIC_DIR / "logo.png"
FAVICON_PATH = PUBLIC_DIR / "favicon.png"
AVATAR_PATH = PUBLIC_DIR / "avatars" / "assistant.png"

