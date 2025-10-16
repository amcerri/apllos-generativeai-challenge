# Infrastructure

This document provides details about the shared infrastructure modules that power the system, including LLM client, database connections, logging, metrics, tracing, and checkpointer.

## Infrastructure Overview

The infrastructure layer provides essential services for the multi-agent system:

- **LLM Client**: Centralized OpenAI integration with retry logic and JSON extraction
- **Database**: PostgreSQL with pgvector for analytics and RAG
- **Logging**: Structured logging with context variables and correlation IDs
- **Metrics**: Prometheus-compatible metrics for monitoring and alerting
- **Tracing**: OpenTelemetry integration for distributed tracing
- **Checkpointer**: LangGraph state persistence for conversation continuity

## LLM Client ([app/infra/llm_client.py](../app/infra/llm_client.py))

The LLM Client is the central component for all OpenAI interactions, providing a unified interface with error handling and retry logic.

### Key Features

- **Singleton Pattern**: `get_llm_client()` provides a configured `LLMClient` instance
- **OpenAI Integration**: Backed by `openai` library (optional dependency)
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

- **`LLMClient.get_embeddings`**: Fetches vector embeddings
  - Uses `text-embedding-3-small` by default
  - Supports batch processing for efficiency
  - Fallback to deterministic hashing when unavailable
  - Returns normalized vectors for pgvector storage

- **`LLMClient.extract_json`**: JSON extraction
  - Direct JSON parsing with error handling
  - Regex fallback for malformed responses
  - Optional schema validation and guidance
  - Tolerant parsing for LLM-generated content

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

## Metrics ([app/infra/metrics.py](../app/infra/metrics.py))

- Optional Prometheus client; exposes counters/histograms/gauges registry and an ASGI app for `/metrics`.
- Default series:
  - `requests_total{agent,node}`
  - `routing_fallbacks_total{from_agent,to_agent}`
  - `llm_failures_total{component}`
  - `node_latency_ms{node}` (with buckets)

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
