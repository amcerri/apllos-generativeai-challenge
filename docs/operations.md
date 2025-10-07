# Operations and Troubleshooting

This document provides runbooks for local development, bootstrap, monitoring, and common issues.

## Bootstrap

- Docker (recommended):
  - `cp .env.example .env` and set `OPENAI_API_KEY`.
  - `make bootstrap-complete` (reset → build → db → ingest analytics → vectors → allowlist → studio → validate)
- Local env:
  - `pip install -e .`
  - `make db-start db-wait db-init`
  - `make ingest-analytics ingest-vectors gen-allowlist`
  - `make studio-up`

## Health Checks

- API health: `curl http://localhost:2024/ok` → `{"status":"ok","db":"ok|down","checkpointer":"ok|noop"}`
- Metrics: `curl http://localhost:2024/metrics` (if prometheus_client is installed)

## Logs and Tracing

- Logs: `make logs` (Studio container) or view terminal output.
- Tracing: enable OTEL as needed; see [infra.md](infra.md) for exporters.

## Database

- Start: `make db-start`; status: `make db-status`; psql: `make db-psql`.
- Reset: `make db-reset`.

## Regenerating Artifacts

- Allowlist: `make gen-allowlist` (rerun after schema changes)
- Vectors: `make ingest-vectors` (requires embeddings model configured)

## Troubleshooting

- DB not responding:
  - `make db-status`; `make db-stop && make db-start`
- OpenAI unavailable:
  - `echo $OPENAI_API_KEY` and confirm network access
  - System will fallback to deterministic heuristics; LLM-dependent features will be reduced.
- Vector search slow after ingestion:
  - Confirm `ANALYZE doc_chunks;` (Make target runs it automatically)

## Safety Toggles

- `REQUIRE_SQL_APPROVAL=true` to enforce human gate for SQL execution.
- `APP_EXPLAIN_ANALYZE=true` to run EXPLAIN ANALYZE (staging only recommended).
- `API_ALLOWED_ORIGINS="http://localhost:3000,https://example.com"` to restrict CORS.
- `EXECUTOR_SANITIZE_SQL=true` to include a safe SQL preview instead of full SQL in meta.
