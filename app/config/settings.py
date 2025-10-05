"""
Configuration settings with Pydantic Settings

Overview
--------
Modern configuration management using Pydantic Settings with automatic
environment variable loading, validation, and type safety. Replaces the
custom YAML loader with a more robust and maintainable solution.

Design
------
- Pydantic BaseSettings for automatic environment variable loading
- Type-safe configuration with validation
- Automatic YAML file loading with environment variable substitution
- Hierarchical configuration with proper defaults
- JSON Schema generation for documentation

Integration
-----------
- Replaces app.config.loader.ConfigLoader
- Used by all agents and services that need configuration values
- Provides type-safe access to configuration values

Usage
-----
>>> from app.config.settings import get_settings
>>> settings = get_settings()
>>> model_name = settings.models.router.name
>>> timeout = settings.models.analytics_planner.timeout_seconds
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml
from pydantic import BaseModel, Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseModel):
    """Application environment configuration.
    
    Attributes
    ----------
    env : str
        Application environment (development, staging, production)
    """
    
    env: str = Field(default="development", description="Application environment")


class ServerConfig(BaseModel):
    """Server configuration.
    
    Attributes
    ----------
    host : str
        Server host address
    port : int
        LangGraph Server port
    studio_port : int
        LangGraph Studio port
    """
    
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=2024, description="LangGraph Server port")
    studio_port: int = Field(default=2025, description="LangGraph Studio port")


class OpenAIConfig(BaseModel):
    """OpenAI global configuration.
    
    Attributes
    ----------
    request_timeout_ms : int
        Request timeout in milliseconds
    max_retries : int
        Maximum retries
    api_base : Optional[str]
        OpenAI API base URL
    router_model : str
        Router model name
    analytics_planner_model : str
        Analytics planner model name
    analytics_planner_fallback : str
        Analytics planner fallback model name
    analytics_normalizer_model : str
        Analytics normalizer model name
    knowledge_model : str
        Knowledge model name
    knowledge_model_mini : str
        Knowledge model mini name
    commerce_model : str
        Commerce model name
    commerce_conversation_model : str
        Commerce conversation model name
    embeddings_model : str
        Embeddings model name
    """
    
    request_timeout_ms: int = Field(default=30000, description="Request timeout in milliseconds")
    max_retries: int = Field(default=3, description="Maximum retries")
    api_base: Optional[str] = Field(default=None, description="OpenAI API base URL")
    
    # Model names for backward compatibility
    router_model: str = Field(default="gpt-4o-mini", description="Router model name")
    analytics_planner_model: str = Field(default="gpt-4o-mini", description="Analytics planner model")
    analytics_planner_fallback: str = Field(default="gpt-4o-mini", description="Analytics planner fallback model")
    analytics_normalizer_model: str = Field(default="gpt-4o-mini", description="Analytics normalizer model")
    knowledge_model: str = Field(default="gpt-4o-mini", description="Knowledge model")
    knowledge_model_mini: str = Field(default="gpt-4o-mini", description="Knowledge model mini")
    commerce_model: str = Field(default="gpt-4o-mini", description="Commerce model")
    commerce_conversation_model: str = Field(default="gpt-4o-mini", description="Commerce conversation model")
    embeddings_model: str = Field(default="text-embedding-3-small", description="Embeddings model")


class ModelConfig(BaseModel):
    """Individual model configuration.
    
    Attributes
    ----------
    provider : str
        Model provider name
    name : str
        Model name
    temperature : float
        Model temperature (0.0 to 2.0)
    max_tokens : int
        Maximum tokens to generate
    timeout_seconds : int
        Timeout in seconds
    output : Optional[Dict[str, Any]]
        Output configuration
    """
    
    provider: str = Field(default="openai", description="Model provider")
    name: str = Field(default="gpt-4o-mini", description="Model name")
    temperature: float = Field(default=0.0, ge=0.0, le=2.0, description="Model temperature")
    max_tokens: int = Field(default=800, ge=1, description="Maximum tokens")
    timeout_seconds: int = Field(default=60, ge=1, description="Timeout in seconds")
    
    # Optional output configuration
    output: Optional[Dict[str, Any]] = Field(default=None, description="Output configuration")


class EmbeddingsConfig(BaseModel):
    """Embeddings model configuration.
    
    Attributes
    ----------
    provider : str
        Model provider name
    name : str
        Model name
    temperature : float
        Model temperature (not used for embeddings)
    max_tokens : int
        Maximum tokens (not used for embeddings)
    timeout_seconds : int
        Timeout in seconds
    parameters : Dict[str, Any]
        Embeddings parameters including dimensions and batch size
    """
    
    provider: str = Field(default="openai", description="Model provider")
    name: str = Field(default="text-embedding-3-small", description="Model name")
    temperature: float = Field(default=0.0, ge=0.0, le=2.0, description="Model temperature")
    max_tokens: int = Field(default=0, ge=0, description="Maximum tokens (not used for embeddings)")
    timeout_seconds: int = Field(default=60, ge=1, description="Timeout in seconds")
    parameters: Dict[str, Any] = Field(
        default_factory=lambda: {"dimensions": 1536, "batch_size": 256},
        description="Embeddings parameters"
    )


class ModelsConfig(BaseModel):
    """All models configuration.
    
    Attributes
    ----------
    router : ModelConfig
        Router model configuration
    analytics_planner : ModelConfig
        Analytics planner model configuration
    analytics_normalizer : ModelConfig
        Analytics normalizer model configuration
    knowledge_answerer : ModelConfig
        Knowledge answerer model configuration
    knowledge_answerer_mini : ModelConfig
        Knowledge answerer mini model configuration
    commerce_extractor : ModelConfig
        Commerce extractor model configuration
    commerce_conversation : ModelConfig
        Commerce conversation model configuration
    commerce_summarizer : ModelConfig
        Commerce summarizer model configuration
    embeddings : EmbeddingsConfig
        Embeddings model configuration
    """
    
    router: ModelConfig = Field(default_factory=ModelConfig)
    analytics_planner: ModelConfig = Field(default_factory=ModelConfig)
    analytics_normalizer: ModelConfig = Field(default_factory=ModelConfig)
    knowledge_answerer: ModelConfig = Field(default_factory=ModelConfig)
    knowledge_answerer_mini: ModelConfig = Field(default_factory=ModelConfig)
    commerce_extractor: ModelConfig = Field(default_factory=ModelConfig)
    commerce_conversation: ModelConfig = Field(default_factory=ModelConfig)
    commerce_summarizer: ModelConfig = Field(default_factory=ModelConfig)
    embeddings: EmbeddingsConfig = Field(default_factory=EmbeddingsConfig)


class AnalyticsPlannerConfig(BaseModel):
    """Analytics planner configuration.
    
    Attributes
    ----------
    default_limit : int
        Default query limit
    max_limit : int
        Maximum query limit
    disallow_select_star : bool
        Whether to disallow SELECT * queries
    require_limit_on_non_aggregate : bool
        Whether to require LIMIT on non-aggregate queries
    examples_count : int
        Number of examples to use
    max_examples : int
        Maximum number of examples
    """
    
    default_limit: int = Field(default=200, ge=1, description="Default query limit")
    max_limit: int = Field(default=1000, ge=1, description="Maximum query limit")
    disallow_select_star: bool = Field(default=True, description="Disallow SELECT *")
    require_limit_on_non_aggregate: bool = Field(default=True, description="Require LIMIT on non-aggregate queries")
    examples_count: int = Field(default=3, ge=0, description="Number of examples to use")
    max_examples: int = Field(default=5, ge=1, description="Maximum examples")


class AnalyticsSQLConfig(BaseModel):
    """Analytics SQL configuration.
    
    Attributes
    ----------
    readonly : bool
        Whether to use read-only mode
    max_rows : int
        Maximum number of rows
    timeout_ms : int
        Timeout in milliseconds
    allowlist_path : str
        Path to allowlist file
    """
    
    readonly: bool = Field(default=True, description="Read-only mode")
    max_rows: int = Field(default=5000, ge=1, description="Maximum rows")
    timeout_ms: int = Field(default=15000, ge=1000, description="Timeout in milliseconds")
    allowlist_path: str = Field(default="app/routing/allowlist.json", description="Allowlist file path")


class AnalyticsExecutorConfig(BaseModel):
    """Analytics executor configuration.
    
    Attributes
    ----------
    explain_analyze : bool
        Whether to enable EXPLAIN ANALYZE
    default_timeout_seconds : int
        Default timeout in seconds
    default_row_cap : int
        Default row cap
    max_row_cap : int
        Maximum row cap
    """
    
    explain_analyze: bool = Field(default=False, description="Enable EXPLAIN ANALYZE")
    default_timeout_seconds: int = Field(default=60, ge=1, description="Default timeout")
    default_row_cap: int = Field(default=2000, ge=1, description="Default row cap")
    max_row_cap: int = Field(default=10000, ge=1, description="Maximum row cap")


class AnalyticsNormalizerConfig(BaseModel):
    """Analytics normalizer configuration.
    
    Attributes
    ----------
    fallback_enabled : bool
        Whether to enable fallback
    max_examples_in_prompt : int
        Maximum examples in prompt
    json_extraction_regex : bool
        Whether to enable JSON extraction regex
    """
    
    fallback_enabled: bool = Field(default=True, description="Enable fallback")
    max_examples_in_prompt: int = Field(default=1, ge=0, description="Max examples in prompt")
    json_extraction_regex: bool = Field(default=True, description="Enable JSON extraction regex")


class AnalyticsConfig(BaseModel):
    """Analytics agent configuration.
    
    Attributes
    ----------
    planner : AnalyticsPlannerConfig
        Analytics planner configuration
    sql : AnalyticsSQLConfig
        Analytics SQL configuration
    executor : AnalyticsExecutorConfig
        Analytics executor configuration
    normalizer : AnalyticsNormalizerConfig
        Analytics normalizer configuration
    """
    
    planner: AnalyticsPlannerConfig = Field(default_factory=AnalyticsPlannerConfig)
    sql: AnalyticsSQLConfig = Field(default_factory=AnalyticsSQLConfig)
    executor: AnalyticsExecutorConfig = Field(default_factory=AnalyticsExecutorConfig)
    normalizer: AnalyticsNormalizerConfig = Field(default_factory=AnalyticsNormalizerConfig)


class KnowledgeRetrievalConfig(BaseModel):
    """Knowledge retrieval configuration.
    
    Attributes
    ----------
    top_k : int
        Top K results to retrieve
    min_score : float
        Minimum similarity score
    deduplicate : bool
        Whether to deduplicate results
    index : str
        Vector index name
    default_min_score : float
        Default minimum score
    """
    
    top_k: int = Field(default=8, ge=1, description="Top K results")
    min_score: float = Field(default=0.18, ge=0.0, le=1.0, description="Minimum similarity score")
    deduplicate: bool = Field(default=True, description="Deduplicate results")
    index: str = Field(default="doc_chunks", description="Vector index name")
    default_min_score: float = Field(default=0.01, ge=0.0, le=1.0, description="Default minimum score")


class KnowledgeRankerConfig(BaseModel):
    """Knowledge ranker configuration.
    
    Attributes
    ----------
    rerank_top_k : int
        Re-rank top K results
    """
    
    rerank_top_k: int = Field(default=6, ge=1, description="Re-rank top K results")


class KnowledgeAnswererConfig(BaseModel):
    """Knowledge answerer configuration.
    
    Attributes
    ----------
    max_tokens : int
        Maximum tokens to generate
    require_citations : bool
        Whether to require citations
    max_chars_summary : int
        Maximum characters in summary
    max_citations : int
        Maximum number of citations
    """
    
    max_tokens: int = Field(default=800, ge=1, description="Maximum tokens")
    require_citations: bool = Field(default=True, description="Require citations")
    max_chars_summary: int = Field(default=2000, ge=1, description="Maximum characters in summary")
    max_citations: int = Field(default=5, ge=1, description="Maximum citations")


class KnowledgeConfig(BaseModel):
    """Knowledge agent configuration.
    
    Attributes
    ----------
    retrieval : KnowledgeRetrievalConfig
        Knowledge retrieval configuration
    ranker : KnowledgeRankerConfig
        Knowledge ranker configuration
    answerer : KnowledgeAnswererConfig
        Knowledge answerer configuration
    """
    
    retrieval: KnowledgeRetrievalConfig = Field(default_factory=KnowledgeRetrievalConfig)
    ranker: KnowledgeRankerConfig = Field(default_factory=KnowledgeRankerConfig)
    answerer: KnowledgeAnswererConfig = Field(default_factory=KnowledgeAnswererConfig)


class CommerceExtractionConfig(BaseModel):
    """Commerce extraction configuration.
    
    Attributes
    ----------
    min_confidence : float
        Minimum confidence threshold
    json_schema_strict : bool
        Whether to use strict JSON schema
    """
    
    min_confidence: float = Field(default=0.50, ge=0.0, le=1.0, description="Minimum confidence")
    json_schema_strict: bool = Field(default=False, description="Strict JSON schema")


class CommerceValidationConfig(BaseModel):
    """Commerce validation configuration.
    
    Attributes
    ----------
    line_total_tolerance : float
        Line total tolerance
    currency_default : str
        Default currency
    """
    
    line_total_tolerance: float = Field(default=0.02, ge=0.0, le=1.0, description="Line total tolerance")
    currency_default: str = Field(default="BRL", description="Default currency")


class CommerceSummarizerConfig(BaseModel):
    """Commerce summarizer configuration.
    
    Attributes
    ----------
    max_tokens : int
        Maximum tokens to generate
    top_items_display : int
        Top items to display
    max_items_display : int
        Maximum items to display
    top_items : int
        Top items for analysis
    """
    
    max_tokens: int = Field(default=600, ge=1, description="Maximum tokens")
    top_items_display: int = Field(default=10, ge=1, description="Top items to display")
    max_items_display: int = Field(default=5, ge=1, description="Maximum items to display")
    top_items: int = Field(default=3, ge=1, description="Top items for analysis")


class CommerceConversationConfig(BaseModel):
    """Commerce conversation configuration.
    
    Attributes
    ----------
    max_tokens : int
        Maximum tokens to generate
    temperature : float
        Model temperature
    timeout_seconds : int
        Timeout in seconds
    """
    
    max_tokens: int = Field(default=1000, ge=1, description="Maximum tokens")
    temperature: float = Field(default=0.3, ge=0.0, le=2.0, description="Temperature")
    timeout_seconds: int = Field(default=60, ge=1, description="Timeout in seconds")


class CommerceConfig(BaseModel):
    """Commerce agent configuration.
    
    Attributes
    ----------
    extraction : CommerceExtractionConfig
        Commerce extraction configuration
    validation : CommerceValidationConfig
        Commerce validation configuration
    summarizer : CommerceSummarizerConfig
        Commerce summarizer configuration
    conversation : CommerceConversationConfig
        Commerce conversation configuration
    """
    
    extraction: CommerceExtractionConfig = Field(default_factory=CommerceExtractionConfig)
    validation: CommerceValidationConfig = Field(default_factory=CommerceValidationConfig)
    summarizer: CommerceSummarizerConfig = Field(default_factory=CommerceSummarizerConfig)
    conversation: CommerceConversationConfig = Field(default_factory=CommerceConversationConfig)


class DocumentProcessingOCRConfig(BaseModel):
    """Document processing OCR configuration.
    
    Attributes
    ----------
    enabled : bool
        Whether OCR is enabled
    language : str
        OCR language
    dpi : int
        OCR DPI
    """
    
    enabled: bool = Field(default=True, description="Enable OCR")
    language: str = Field(default="por", description="OCR language")
    dpi: int = Field(default=300, ge=100, description="OCR DPI")


class DocumentProcessingConfig(BaseModel):
    """Document processing configuration.
    
    Attributes
    ----------
    ocr : DocumentProcessingOCRConfig
        OCR configuration
    max_file_size_mb : int
        Maximum file size in MB
    max_pages_for_ocr : int
        Maximum pages for OCR
    supported_formats : List[str]
        Supported file formats
    """
    
    ocr: DocumentProcessingOCRConfig = Field(default_factory=DocumentProcessingOCRConfig)
    max_file_size_mb: int = Field(default=50, ge=1, description="Maximum file size in MB")
    max_pages_for_ocr: int = Field(default=20, ge=1, description="Maximum pages for OCR")
    supported_formats: List[str] = Field(
        default_factory=lambda: ["pdf", "docx", "txt", "doc"],
        description="Supported file formats"
    )


class BatchProcessingMarkdownConfig(BaseModel):
    """Batch processing markdown configuration.
    
    Attributes
    ----------
    include_toc : bool
        Whether to include table of contents
    include_back_to_top : bool
        Whether to include back to top
    separator_style : str
        Separator style
    max_chunk_length : int
        Maximum chunk length
    """
    
    include_toc: bool = Field(default=True, description="Include table of contents")
    include_back_to_top: bool = Field(default=True, description="Include back to top")
    separator_style: str = Field(default="---", description="Separator style")
    max_chunk_length: int = Field(default=1000, ge=1, description="Maximum chunk length")


class BatchProcessingConfig(BaseModel):
    """Batch processing configuration.
    
    Attributes
    ----------
    sequential_processing : bool
        Whether to process queries sequentially
    query_timeout_seconds : int
        Query timeout in seconds
    markdown : BatchProcessingMarkdownConfig
        Markdown configuration
    """
    
    sequential_processing: bool = Field(default=True, description="Process queries sequentially")
    query_timeout_seconds: int = Field(default=60, ge=1, description="Query timeout in seconds")
    markdown: BatchProcessingMarkdownConfig = Field(default_factory=BatchProcessingMarkdownConfig)


class RoutingConfig(BaseModel):
    """Routing configuration.
    
    Attributes
    ----------
    confidence_min : float
        Minimum confidence threshold
    fallback_enabled : bool
        Whether fallback is enabled
    rag_hits_threshold : int
        RAG hits threshold
    rag_min_score_threshold : float
        RAG minimum score threshold
    """
    
    confidence_min: float = Field(default=0.55, ge=0.0, le=1.0, description="Minimum confidence")
    fallback_enabled: bool = Field(default=True, description="Enable fallback")
    rag_hits_threshold: int = Field(default=2, ge=1, description="RAG hits threshold")
    rag_min_score_threshold: float = Field(default=0.78, ge=0.0, le=1.0, description="RAG minimum score threshold")


class InterruptsConfig(BaseModel):
    """Interrupts configuration.
    
    Attributes
    ----------
    require_approval_for : List[str]
        Actions requiring approval
    approval_timeout_seconds : int
        Approval timeout in seconds
    """
    
    require_approval_for: List[str] = Field(
        default_factory=lambda: ["analytics.execute_sql", "commerce.external_call"],
        description="Actions requiring approval"
    )
    approval_timeout_seconds: int = Field(default=300, ge=1, description="Approval timeout in seconds")


class DatabaseConfig(BaseModel):
    """Database configuration.
    
    Attributes
    ----------
    url : str
        Database URL
    pool_size : int
        Connection pool size
    pool_timeout_sec : int
        Pool timeout in seconds
    echo : bool
        Whether to echo SQL queries
    readonly_default : bool
        Default to read-only mode
    """
    
    url: str = Field(default="postgresql+psycopg://app:app@localhost:5432/app", description="Database URL")
    pool_size: int = Field(default=10, ge=1, description="Connection pool size")
    pool_timeout_sec: int = Field(default=10, ge=1, description="Pool timeout in seconds")
    echo: bool = Field(default=False, description="Echo SQL queries")
    readonly_default: bool = Field(default=True, description="Default to read-only")


class CheckpointerConfig(BaseModel):
    """Checkpointer configuration.
    
    Attributes
    ----------
    enabled : bool
        Whether checkpointer is enabled
    backend : str
        Checkpointer backend
    table : str
        Checkpoints table name
    cleanup_interval_hours : int
        Cleanup interval in hours
    """
    
    enabled: bool = Field(default=True, description="Enable checkpointer")
    backend: str = Field(default="postgres", description="Checkpointer backend")
    table: str = Field(default="checkpoints", description="Checkpoints table name")
    cleanup_interval_hours: int = Field(default=24, ge=1, description="Cleanup interval in hours")


class LoggingConfig(BaseModel):
    """Logging configuration.
    
    Attributes
    ----------
    level : str
        Logging level
    structlog_json : bool
        Whether to use JSON logging
    component_prefix : bool
        Whether to add component prefix
    """
    
    level: str = Field(default="INFO", description="Logging level")
    structlog_json: bool = Field(default=False, description="Use JSON logging")
    component_prefix: bool = Field(default=True, description="Add component prefix")


class TracingConfig(BaseModel):
    """Tracing configuration.
    
    Attributes
    ----------
    enabled : bool
        Whether tracing is enabled
    sample_ratio : float
        Sampling ratio
    span_timeout_seconds : int
        Span timeout in seconds
    """
    
    enabled: bool = Field(default=False, description="Enable tracing")
    sample_ratio: float = Field(default=0.0, ge=0.0, le=1.0, description="Sampling ratio")
    span_timeout_seconds: int = Field(default=30, ge=1, description="Span timeout in seconds")


class DebugConfig(BaseModel):
    """Debug configuration.
    
    Attributes
    ----------
    enable_verbose_logging : bool
        Whether to enable verbose logging
    log_sql_queries : bool
        Whether to log SQL queries
    log_llm_requests : bool
        Whether to log LLM requests
    log_llm_responses : bool
        Whether to log LLM responses
    save_debug_files : bool
        Whether to save debug files
    debug_output_dir : str
        Debug output directory
    """
    
    enable_verbose_logging: bool = Field(default=False, description="Enable verbose logging")
    log_sql_queries: bool = Field(default=False, description="Log SQL queries")
    log_llm_requests: bool = Field(default=False, description="Log LLM requests")
    log_llm_responses: bool = Field(default=False, description="Log LLM responses")
    save_debug_files: bool = Field(default=False, description="Save debug files")
    debug_output_dir: str = Field(default="debug_output", description="Debug output directory")


class ObservabilityConfig(BaseModel):
    """Observability configuration.
    
    Attributes
    ----------
    logging : LoggingConfig
        Logging configuration
    tracing : TracingConfig
        Tracing configuration
    debug : DebugConfig
        Debug configuration
    """
    
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    tracing: TracingConfig = Field(default_factory=TracingConfig)
    debug: DebugConfig = Field(default_factory=DebugConfig)


class Settings(BaseSettings):
    """Main application settings using Pydantic Settings.
    
    Attributes
    ----------
    app : AppConfig
        Application configuration
    server : ServerConfig
        Server configuration
    openai : OpenAIConfig
        OpenAI configuration
    models : ModelsConfig
        Models configuration
    analytics : AnalyticsConfig
        Analytics agent configuration
    knowledge : KnowledgeConfig
        Knowledge agent configuration
    commerce : CommerceConfig
        Commerce agent configuration
    document_processing : DocumentProcessingConfig
        Document processing configuration
    batch_processing : BatchProcessingConfig
        Batch processing configuration
    routing : RoutingConfig
        Routing configuration
    interruptions : InterruptsConfig
        Interrupts configuration
    database : DatabaseConfig
        Database configuration
    checkpointer : CheckpointerConfig
        Checkpointer configuration
    observability : ObservabilityConfig
        Observability configuration
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Core application settings
    app: AppConfig = Field(default_factory=AppConfig)
    server: ServerConfig = Field(default_factory=ServerConfig)
    
    # LLM and model settings
    openai: OpenAIConfig = Field(default_factory=OpenAIConfig)
    models: ModelsConfig = Field(default_factory=ModelsConfig)
    
    # Agent configurations
    analytics: AnalyticsConfig = Field(default_factory=AnalyticsConfig)
    knowledge: KnowledgeConfig = Field(default_factory=KnowledgeConfig)
    commerce: CommerceConfig = Field(default_factory=CommerceConfig)
    
    # Processing configurations
    document_processing: DocumentProcessingConfig = Field(default_factory=DocumentProcessingConfig)
    batch_processing: BatchProcessingConfig = Field(default_factory=BatchProcessingConfig)
    
    # System configurations
    routing: RoutingConfig = Field(default_factory=RoutingConfig)
    interruptions: InterruptsConfig = Field(default_factory=InterruptsConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    checkpointer: CheckpointerConfig = Field(default_factory=CheckpointerConfig)
    observability: ObservabilityConfig = Field(default_factory=ObservabilityConfig)
    
    @classmethod
    def load_from_yaml_files(cls, config_dir: Optional[Path] = None) -> "Settings":
        """Load settings from YAML files with environment variable substitution.
        
        Parameters
        ----------
        config_dir : Optional[Path]
            Optional path to config directory. Defaults to config dir.
            
        Returns
        -------
        Settings
            Settings instance loaded from YAML files
        """
        if config_dir is None:
            config_dir = Path(__file__).parent
        
        # Load and merge YAML files
        merged_config = {}
        config_files = [
            "config.yaml",
            "models.yaml", 
            "agents.yaml",
            "database.yaml",
            "observability.yaml"
        ]
        
        for config_file in config_files:
            config_path = config_dir / config_file
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Substitute environment variables
                content = cls._substitute_env_vars(content)
                
                # Parse YAML
                file_config = yaml.safe_load(content) or {}
                
                # Merge into main config
                cls._merge_config(merged_config, file_config)
        
        # Create settings instance with merged config
        return cls(**merged_config)
    
    @staticmethod
    def _substitute_env_vars(content: str) -> str:
        """Substitute environment variables in YAML content.
        
        Parameters
        ----------
        content : str
            YAML content string
            
        Returns
        -------
        str
            Content with environment variables substituted
        """
        import re
        
        def replace_var(match):
            var_name = match.group(1)
            default_value = match.group(2) if match.group(2) else ""
            return os.getenv(var_name, default_value)
        
        # Pattern: ${VAR_NAME:-default_value}
        pattern = r'\$\{([^:}]+)(?::-([^}]*))?\}'
        return re.sub(pattern, replace_var, content)
    
    @staticmethod
    def _merge_config(base: Dict[str, Any], new: Dict[str, Any]) -> None:
        """Merge new configuration into base configuration.
        
        Parameters
        ----------
        base : Dict[str, Any]
            Base configuration dict to merge into
        new : Dict[str, Any]
            New configuration dict to merge from
        """
        for key, value in new.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                # Recursively merge nested dictionaries
                Settings._merge_config(base[key], value)
            else:
                # Overwrite or add the value
                base[key] = value


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get the global settings instance.
    
    Returns
    -------
    Settings
        Settings instance
    """
    global _settings
    if _settings is None:
        _settings = Settings.load_from_yaml_files()
    return _settings


def reload_settings() -> Settings:
    """Reload settings from YAML files.
    
    Returns
    -------
    Settings
        Fresh Settings instance
    """
    global _settings
    _settings = Settings.load_from_yaml_files()
    return _settings