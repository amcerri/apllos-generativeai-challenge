# Operations and Troubleshooting

This document provides comprehensive runbooks for local development, bootstrap procedures, monitoring, and troubleshooting common issues.

## System Overview

The Apllos Assistant is designed for high availability and reliability with multiple deployment options:

- **Docker Compose**: Recommended for development and testing
- **Local Installation**: For development and debugging
- **Production**: Containerized deployment with external services

## Bootstrap Procedures

### Docker Compose (Recommended)

The Docker Compose setup provides a complete environment with all dependencies:

```bash
# 1. Environment setup
cp .env.example .env
# Edit .env with your OPENAI_API_KEY

# 2. Complete bootstrap (automated)
make bootstrap-complete
```

**What `bootstrap-complete` does**:
1. **Reset**: Cleans up any existing containers and volumes
2. **Build**: Builds Docker images with all dependencies
3. **Database**: Starts PostgreSQL with pgvector extension
4. **Ingest Analytics**: Loads Olist dataset into PostgreSQL
5. **Ingest Vectors**: Creates embeddings and populates doc_chunks table
6. **Generate Allowlist**: Creates routing allowlist from database schema
7. **Studio**: Starts LangGraph Studio for development
8. **Validate**: Runs health checks to ensure everything works

### Local Environment Setup

For development without Docker:

```bash
# 1. Install dependencies
pip install -e .

# 2. Start database
make db-start db-wait db-init

# 3. Ingest data
make ingest-analytics ingest-vectors gen-allowlist

# 4. Start services
make studio-up
```

### Production Deployment

For production environments:

```bash
# 1. Set production environment variables
export OPENAI_API_KEY="your-key"
export DATABASE_URL="postgresql://user:pass@host:port/db"
export LOG_LEVEL="INFO"
export TRACING_ENABLED="true"

# 2. Deploy with Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# 3. Run health checks
curl http://localhost:8000/ok
```

## Health Checks

- API health: `curl http://localhost:2024/ok` → `{"status":"ok","db":"ok|down","checkpointer":"ok|noop"}`
- Metrics: `curl http://localhost:2024/metrics` (if prometheus_client is installed)

## Logs and Tracing

- Logs: `make logs` (Studio container) or view terminal output.
- Tracing: enable OTEL as needed; see [infra.md](../core/infra.md) for exporters.

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

---

**← [Back to Documentation Index](../README.md)**
