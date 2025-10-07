# Infrastructure

This document details the shared infrastructure modules: LLM client, database engine factory, logging, metrics, tracing, and checkpointer.

## LLM Client (`app/infra/llm_client.py`)

- Singleton factory `get_llm_client()` provides a configured `LLMClient`.
- Backed by `openai` (optional); supports timeouts, retries (exponential backoff), and JSON extraction helpers.
- `LLMClient.chat_completion`: wraps OpenAI Chat Completions; returns `LLMResponse`.
- `LLMClient.get_embeddings`: fetches embeddings; callers may fallback to deterministic hashing when unavailable.
- `LLMClient.extract_json`: tolerant parsing (direct JSON, regex fallback), with optional schema guidance.

## Database (`app/infra/db.py`)

- Cached SQLAlchemy engine via `get_engine()` with read-only connection options for Postgres.
- `open_connection(readonly=True)`: context manager that sets `default_transaction_read_only` when supported.
- Handles Docker hostname translation (`@db:` → `@host.docker.internal:`) and `postgresql+psycopg://` normalization.

## Logging (`app/infra/logging.py`)

- Stdlib logging with a `bind()`-capable adapter and contextvars (`bind_context`, `clear_context`).
- Optional JSON formatter; configured via env `STRUCTLOG_JSON`.
- Usage:
  ```python
  from app.infra.logging import get_logger
  log = get_logger("agent.analytics").bind(thread_id="thr-1")
  log.info("planned", sql="...", limit=200)
  ```

## Metrics (`app/infra/metrics.py`)

- Optional Prometheus client; exposes counters/histograms/gauges registry and an ASGI app for `/metrics`.
- Default series:
  - `requests_total{agent,node}`
  - `routing_fallbacks_total{from_agent,to_agent}`
  - `llm_failures_total{component}`
  - `node_latency_ms{node}` (with buckets)

## Tracing (`app/infra/tracing.py`)

- Optional OpenTelemetry setup with exporters (`otlp-http`, `otlp-grpc`, `console`).
- `start_span(name, attrs)`: context manager that correlates logs with `trace_id`/`span_id` even when OTEL is absent (no-op with generated IDs).

## Checkpointer (`app/infra/checkpointer.py`)

- Native LangGraph PostgresSaver with cached factory `get_checkpointer()`; returns no-op saver when disabled/missing.
- Cleanup helper `_cleanup_old_checkpoints()` deletes aged rows when saver engine is accessible.

## Operational Notes

- All infra modules avoid hard dependencies at import time and degrade gracefully to keep the system operable in constrained environments.
