# API Server and Endpoints

This document provides details about the ASGI (_Asynchronous Server Gateway Interface_) API server, endpoints, and integration with LangGraph Server and Studio.

## API Overview

The Apllos Assistant provides a REST API built on FastAPI with health monitoring and LangGraph integration:

- **Implementation**: [app/api/server.py](../app/api/server.py)
- **Framework**: FastAPI (optional at import time; graceful fallback to stubs)
- **Integration**: LangGraph Server handlers mounted under `/graph`
- **Health Monitoring**: Multiple health check endpoints
- **Metrics**: Prometheus-compatible metrics endpoint
- **CORS**: Configurable cross-origin resource sharing

## API Architecture

```
FastAPI Application
├── Health Endpoints (/health, /ready, /ok)
├── LangGraph Server (/graph/*)
├── Metrics Endpoint (/metrics)
└── CORS Configuration
```

## Endpoints

- `GET /` (landing): returns basic links to `/docs`, `/openapi.json`, `/graph`, `/health`, `/ready`.
- `GET /health`: liveness.
- `GET /ready`: readiness.
- `GET /ok`: extended health: DB connectivity and checkpointer availability.
- `GET /graph/...`: LangGraph Server (threads, runs, state) for Studio.
- `GET /metrics`: Prometheus scrape endpoint (optional).

## Extended Health (`/ok`)

- DB: uses `app.infra.db.open_connection()` and `SELECT 1`.
- Checkpointer: uses `app.infra.checkpointer.get_checkpointer()` and `is_noop()`.
- Response example: `{ "status": "ok", "db": "ok|down", "checkpointer": "ok|noop" }`.

## CORS

- Controlled by env `API_ENABLE_CORS` (default enabled). Allows all origins/headers/methods for dev.

## Logging and Tracing

- `start_span("api.server.build")` wraps initialization (no-op if tracing disabled).
- Uses centralized logging via `app.infra.logging.get_logger`.

## Running Locally

- Make targets:
  - `make studio-up`: runs LangGraph Studio (exposes `/graph` and Studio UI).
  - `make api-up`: runs FastAPI on port 8000 for standalone API.

## Error Handling & Fallbacks

- If FastAPI/langgraph unavailable at import, `get_app()` returns a stub assistant payload to keep imports safe.
- Metrics mount is best-effort; logs a notice when not available.

---

**← [Back to Documentation Index](../README.md)**
