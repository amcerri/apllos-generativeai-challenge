"""
Configuration loader with environment variable override support.

Overview
--------
Centralized configuration management that loads from YAML files and allows
environment variable overrides. Provides type-safe access to configuration
values with sensible defaults.

Design
------
- Loads base configuration from `config.yaml`
- Supports environment variable overrides using `${VAR_NAME:-default}` syntax
- Provides typed accessors for different configuration sections
- Caches loaded configuration to avoid repeated file I/O
- Handles missing configuration gracefully with defaults

Integration
-----------
Used by all agents and services that need configuration values.
Replaces hardcoded values throughout the codebase.

Usage
-----
>>> from app.config.loader import get_config
>>> config = get_config()
>>> timeout = config.get_llm_timeout("analytics_planner")
>>> max_tokens = config.get_llm_max_tokens("commerce_extractor")
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml

try:
    from app.infra.logging import get_logger
except Exception:  # pragma: no cover - optional
    import logging as _logging

    def get_logger(component: str, **initial_values: Any) -> Any:
        return _logging.getLogger(component)


class ConfigLoader:
    """Centralized configuration loader with environment variable support."""
    
    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize configuration loader.
        
        Parameters
        ----------
        config_dir: Optional path to config directory. Defaults to config dir.
        """
        self.log = get_logger("config.loader")
        self._config_dir = config_dir or Path(__file__).parent
        self._config: Optional[Dict[str, Any]] = None
        
        # Define configuration files to load
        self._config_files = [
            "config.yaml",      # Main application config
            "models.yaml",      # LLM models and parameters
            "agents.yaml",      # Agent-specific settings
            "database.yaml",    # Database settings
            "observability.yaml" # Logging, tracing, debug
        ]
    
    def load(self) -> Dict[str, Any]:
        """Load configuration from multiple YAML files with environment variable substitution.
        
        Returns
        -------
        Dict containing the merged configuration from all files
        """
        if self._config is not None:
            return self._config
        
        self._config = {}
        
        for config_file in self._config_files:
            config_path = self._config_dir / config_file
            try:
                if config_path.exists():
                    with open(config_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Substitute environment variables
                    content = self._substitute_env_vars(content)
                    
                    # Parse YAML
                    file_config = yaml.safe_load(content) or {}
                    
                    # Merge into main config
                    self._merge_config(self._config, file_config)
                    self.log.info(f"Loaded configuration from {config_file}")
                else:
                    self.log.warning(f"Configuration file not found: {config_file}")
                    
            except Exception as e:
                self.log.error(f"Failed to load configuration from {config_file}: {e}")
                # Continue loading other files even if one fails
        
        self.log.info(f"Configuration loaded from {len(self._config_files)} files")
        return self._config
    
    def _substitute_env_vars(self, content: str) -> str:
        """Substitute environment variables in YAML content.
        
        Supports syntax: ${VAR_NAME:-default_value}
        """
        def replace_var(match):
            var_name = match.group(1)
            default_value = match.group(2) if match.group(2) else ""
            return os.getenv(var_name, default_value)
        
        # Pattern: ${VAR_NAME:-default_value}
        pattern = r'\$\{([^:}]+)(?::-([^}]*))?\}'
        return re.sub(pattern, replace_var, content)
    
    def _merge_config(self, base: Dict[str, Any], new: Dict[str, Any]) -> None:
        """Merge new configuration into base configuration.
        
        Parameters
        ----------
        base: Base configuration dict to merge into
        new: New configuration dict to merge from
        """
        for key, value in new.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                # Recursively merge nested dictionaries
                self._merge_config(base[key], value)
            else:
                # Overwrite or add the value
                base[key] = value
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """Get configuration value using dot notation.
        
        Parameters
        ----------
        key_path: Dot-separated path to configuration value (e.g., "openai.models.router.temperature")
        default: Default value if key not found
        
        Returns
        -------
        Configuration value or default
        """
        config = self.load()
        keys = key_path.split('.')
        
        current = config
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        
        return current
    
    # LLM Configuration Accessors
    def get_llm_model(self, model_type: str) -> str:
        """Get LLM model name for specific type."""
        return self.get(f"models.{model_type}.name", "gpt-4o-mini")
    
    def get_llm_temperature(self, model_type: str) -> float:
        """Get LLM temperature for specific type."""
        return self.get(f"models.{model_type}.temperature", 0.0)
    
    def get_llm_max_tokens(self, model_type: str) -> int:
        """Get LLM max_tokens for specific type."""
        return self.get(f"models.{model_type}.max_tokens", 800)
    
    def get_llm_timeout(self, model_type: str) -> int:
        """Get LLM timeout in seconds for specific type."""
        return self.get(f"models.{model_type}.timeout_seconds", 10)
    
    def get_global_timeout_ms(self) -> int:
        """Get global LLM request timeout in milliseconds."""
        return self.get("openai.request_timeout_ms", 30000)
    
    def get_max_retries(self) -> int:
        """Get maximum number of retries for LLM requests."""
        return self.get("openai.max_retries", 3)
    
    # Analytics Configuration Accessors
    def get_analytics_planner_config(self) -> Dict[str, Any]:
        """Get analytics planner configuration."""
        return self.get("analytics.planner", {})
    
    def get_analytics_sql_config(self) -> Dict[str, Any]:
        """Get analytics SQL configuration."""
        return self.get("analytics.sql", {})
    
    def get_analytics_executor_config(self) -> Dict[str, Any]:
        """Get analytics executor configuration."""
        return self.get("analytics.executor", {})
    
    def get_analytics_normalizer_config(self) -> Dict[str, Any]:
        """Get analytics normalizer configuration."""
        return self.get("analytics.normalizer", {})
    
    # Knowledge Configuration Accessors
    def get_knowledge_retrieval_config(self) -> Dict[str, Any]:
        """Get knowledge retrieval configuration."""
        return self.get("knowledge.retrieval", {})
    
    def get_knowledge_ranker_config(self) -> Dict[str, Any]:
        """Get knowledge ranker configuration."""
        return self.get("knowledge.ranker", {})
    
    def get_knowledge_answerer_config(self) -> Dict[str, Any]:
        """Get knowledge answerer configuration."""
        return self.get("knowledge.answerer", {})
    
    # Commerce Configuration Accessors
    def get_commerce_extraction_config(self) -> Dict[str, Any]:
        """Get commerce extraction configuration."""
        return self.get("commerce.extraction", {})
    
    def get_commerce_validation_config(self) -> Dict[str, Any]:
        """Get commerce validation configuration."""
        return self.get("commerce.validation", {})
    
    def get_commerce_summarizer_config(self) -> Dict[str, Any]:
        """Get commerce summarizer configuration."""
        return self.get("commerce.summarizer", {})
    
    def get_commerce_conversation_config(self) -> Dict[str, Any]:
        """Get commerce conversation configuration."""
        return self.get("commerce.conversation", {})
    
    # Routing Configuration Accessors
    def get_routing_config(self) -> Dict[str, Any]:
        """Get routing configuration."""
        return self.get("routing", {})
    
    # Document Processing Configuration Accessors
    def get_document_processing_config(self) -> Dict[str, Any]:
        """Get document processing configuration."""
        return self.get("document_processing", {})
    
    # Batch Processing Configuration Accessors
    def get_batch_processing_config(self) -> Dict[str, Any]:
        """Get batch processing configuration."""
        return self.get("batch_processing", {})
    
    # Database Configuration Accessors
    def get_database_config(self) -> Dict[str, Any]:
        """Get database configuration."""
        return self.get("database", {})
    
    # Observability Configuration Accessors
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration."""
        return self.get("logging", {})
    
    def get_tracing_config(self) -> Dict[str, Any]:
        """Get tracing configuration."""
        return self.get("tracing", {})
    
    def get_debug_config(self) -> Dict[str, Any]:
        """Get debug configuration."""
        return self.get("debug", {})


# Global configuration instance
_config_loader: Optional[ConfigLoader] = None


def get_config() -> ConfigLoader:
    """Get the global configuration loader instance.
    
    Returns
    -------
    ConfigLoader instance
    """
    global _config_loader
    if _config_loader is None:
        _config_loader = ConfigLoader()
    return _config_loader


def reload_config() -> ConfigLoader:
    """Reload configuration from file.
    
    Returns
    -------
    Fresh ConfigLoader instance
    """
    global _config_loader
    _config_loader = ConfigLoader()
    return _config_loader
