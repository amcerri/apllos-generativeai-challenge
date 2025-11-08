# Infrastructure

This document provides details about the shared infrastructure modules that power the system, including LLM client, database connections, logging, metrics, tracing, and checkpointer.

## Infrastructure Overview

The infrastructure layer provides essential services for the multi-agent system:

- **LLM Client**: Centralized OpenAI integration with retry logic, JSON extraction, tool calling, and cost tracking
- **Database**: PostgreSQL with pgvector for analytics and RAG
- **Caching**: Semantic caching for routing decisions, embeddings, and agent responses
- **Logging**: Structured logging with context variables and correlation IDs
- **Metrics**: Prometheus-compatible metrics for monitoring and alerting
- **Tracing**: OpenTelemetry integration for distributed tracing
- **Checkpointer**: LangGraph state persistence for conversation continuity

## LLM Client ([app/infra/llm_client.py](../app/infra/llm_client.py))

The LLM Client is the central component for all OpenAI interactions, providing a unified interface with error handling and retry logic.

### Key Features

- **Singleton Pattern**: `get_llm_client()` provides a configured `LLMClient` instance
- **OpenAI Integration**: Backed by `openai` library (optional dependency)
- **Tool Calling**: Efficient structured outputs using OpenAI's tool calling API with JSON Schema fallback
- **Cost Tracking**: Automatic cost calculation and metrics for all LLM interactions
- **Retry Logic**: Exponential backoff for transient failures
- **Timeout Handling**: Configurable timeouts for all operations
- **JSON Extraction**: Tolerant parsing with regex fallback
- **Error Recovery**: Graceful degradation when OpenAI is unavailable

### Core Methods

- **`LLMClient.chat_completion`**: Wraps OpenAI Chat Completions API
  - Returns structured `LLMResponse` with metadata
  - Supports streaming and non-streaming modes
  - Handles rate limiting and quota errors
  - Implements exponential backoff retry logic
  - Automatically tracks costs for all interactions

- **`LLMClient.chat_completion_with_tools`**: Tool calling for structured outputs
  - Uses OpenAI's tool calling API for token-efficient structured outputs
  - Converts JSON schemas to tool definitions automatically
  - Falls back to JSON Schema mode if tool calling fails
  - Extracts tool call arguments as response text
  - Reduces token usage compared to JSON Schema mode

- **`LLMClient.get_embeddings`**: Fetches vector embeddings
  - Uses `text-embedding-3-small` by default
  - Supports batch processing for efficiency
  - Fallback to deterministic hashing when unavailable
  - Returns normalized vectors for pgvector storage
  - Automatically tracks costs for embedding requests

- **`LLMClient.extract_json`**: JSON extraction
  - Direct JSON parsing with error handling
  - Regex fallback for malformed responses
  - Optional schema validation and guidance
  - Tolerant parsing for LLM-generated content

- **`LLMClient._track_cost`**: Cost tracking (internal)
  - Calculates costs based on model pricing and token usage
  - Records metrics for Prometheus monitoring
  - Supports all OpenAI models with current pricing
  - Logs cost information for debugging

### Configuration

```python
# Example LLM Client configuration
from app.infra.llm_client import get_llm_client

client = get_llm_client()
response = client.chat_completion(
    messages=[{"role": "user", "content": "Hello"}],
    model="gpt-4o-mini",
    temperature=0.7,
    max_tokens=1000
)
```

## Database ([app/infra/db.py](../app/infra/db.py))

- Cached SQLAlchemy engine via `get_engine()` with read-only connection options for Postgres.
- `open_connection(readonly=True)`: context manager that sets `default_transaction_read_only` when supported.
- Handles Docker hostname translation (`@db:` → `@host.docker.internal:`) and `postgresql+psycopg://` normalization.

## Logging ([app/infra/logging.py](../app/infra/logging.py))

- Stdlib logging with a `bind()`-capable adapter and contextvars (`bind_context`, `clear_context`).
- Optional JSON formatter; configured via env `STRUCTLOG_JSON`.
- Usage:
  ```python
  from app.infra.logging import get_logger
  log = get_logger("agent.analytics").bind(thread_id="thr-1")
  log.info("planned", sql="...", limit=200)
  ```

## Caching ([app/infra/cache.py](../app/infra/cache.py))

The caching system provides semantic caching for routing decisions, embeddings, and agent responses to improve performance and reduce LLM API calls.

### Cache Classes

- **`RoutingCache`**: Caches routing decisions based on normalized query text
  - TTL: 1 hour (configurable)
  - Max size: 500 entries (configurable)
  - Semantic key generation using normalized text and SHA-256 hashing
  - Thread-safe operations for concurrent access

- **`EmbeddingCache`**: Caches embedding vectors for text queries
  - TTL: 24 hours (configurable)
  - Max size: 5000 entries (configurable)
  - Key includes normalized text and model name
  - Reduces redundant embedding API calls

- **`ResponseCache`**: Caches agent responses for similar queries
  - TTL: 1 hour (configurable)
  - Max size: 1000 entries (configurable)
  - Context-aware caching (includes query, agent, and context hash)
  - Supports different responses for different contexts

### Cache Features

- **Semantic Normalization**: Queries are normalized (lowercase, whitespace cleanup) before hashing
- **TTL-based Expiration**: Automatic expiration of stale entries
- **LRU Eviction**: Oldest entries evicted when max size reached
- **Thread Safety**: Lock-based synchronization for concurrent access
- **Graceful Degradation**: System continues to work if cache is unavailable

### Usage

```python
from app.infra.cache import RoutingCache, EmbeddingCache, ResponseCache

# Routing cache
routing_cache = RoutingCache(ttl_seconds=3600, max_size=500)
cached = routing_cache.get("query text")
if cached is None:
    result = process_query("query text")
    routing_cache.set("query text", result)

# Embedding cache
embedding_cache = EmbeddingCache(ttl_seconds=86400, max_size=5000)
embedding = embedding_cache.get("text", "text-embedding-3-small")
if embedding is None:
    embedding = generate_embedding("text", "text-embedding-3-small")
    embedding_cache.set("text", "text-embedding-3-small", embedding)

# Response cache
response_cache = ResponseCache(ttl_seconds=3600, max_size=1000)
response = response_cache.get("query", "analytics", context={"sql": "..."})
if response is None:
    response = generate_response("query", "analytics", context={"sql": "..."})
    response_cache.set("query", "analytics", response, context={"sql": "..."})
```

## Metrics ([app/infra/metrics.py](../app/infra/metrics.py))

- Optional Prometheus client; exposes counters/histograms/gauges registry and an ASGI app for `/metrics`.
- Default series:
  - `requests_total{agent,node}`
  - `routing_fallbacks_total{from_agent,to_agent}`
  - `llm_failures_total{component}`
  - `node_latency_ms{node}` (with buckets)
  - `llm_cost_usd_total{model}`: Total LLM API cost in USD, labeled by model
  - `llm_tokens_total{model,type}`: Total LLM tokens used, labeled by model and type (prompt/completion/total)

## Tracing ([app/infra/tracing.py](../app/infra/tracing.py))

- Optional OpenTelemetry setup with exporters (`otlp-http`, `otlp-grpc`, `console`).
- `start_span(name, attrs)`: context manager that correlates logs with `trace_id`/`span_id` even when OTEL is absent (no-op with generated IDs).

## Checkpointer ([app/infra/checkpointer.py](../app/infra/checkpointer.py))

- Native LangGraph PostgresSaver with cached factory `get_checkpointer()`; returns no-op saver when disabled/missing.
- Cleanup helper `_cleanup_old_checkpoints()` deletes aged rows when saver engine is accessible.

## Operational Notes

- All infra modules avoid hard dependencies at import time and degrade gracefully to keep the system operable in constrained environments.

---

**← [Back to Documentation Index](../README.md)**
