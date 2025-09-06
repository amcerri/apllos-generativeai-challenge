# apllos-generativeai-challenge

LangGraph-based engineering assistant that routes user requests to specialized agents — **analytics**, **knowledge**, **commerce**, and **triage** — and responds to end users in **pt-BR**. The runtime supports persistence (checkpointer), optional human-in-the-loop interruptions, and structured logging + (optional) tracing.

> This repo is built **file-by-file** following an explicit order. We only commit at the **end of each phase**.

---

## Overview
This POC implements a **context-first router** plus four specialized agents:
- **analytics**: safe SQL over Olist analytics data (allowlist only, no `SELECT *`, enforced LIMITs). Final answer is business-oriented in pt-BR.
- **knowledge**: RAG over documents using pgvector; answers **must include citations** when retrieval is used.
- **commerce**: heterogeneous commercial docs (PO/Order Form/BEO/invoice, etc.) → canonical schema (buyer/vendor/items/totals/terms/signatures/risks).
- **triage**: short guidance + redirection when context is insufficient.

**Routing rules (single-pass fallbacks, no loops):**
1) If answerable via docs → **knowledge**.
2) If tables/columns/aggregations → **analytics**.
3) If commercial-doc signals → **commerce**.
4) Otherwise → **triage**.

**Models (OpenAI only):** router `gpt-4.1-mini`; analytics planner `o3` (or `o4-mini`); RAG `gpt-4.1` (or `gpt-4.1-mini`); commerce extractor `gpt-4.1`.

**Contracts:**
- `RouterDecision`: `{ agent ∈ {analytics,knowledge,commerce,triage}, confidence, reason, tables[], columns[], signals[], thread_id? }`.
- `Answer`: `{ text, data?, columns?, citations?, meta?, no_context?, artifacts?, followups? }`.

---

## Architecture
- **LangGraph** orchestrates the graph (nodes = agents/pipeline steps).
- **LangGraph Server + Studio** expose HTTP/stream endpoints and a visual UI.
- **Postgres** stores analytics data and application state; **pgvector** indexes embeddings for RAG.
- **Checkpointer** persists graph state/thread for resumability.
- **Observability**: `structlog` (structured logs with `component/event/thread_id`); optional OpenTelemetry spans.
- **Config**: `config.yaml` (thresholds like `confidence_min`, `retrieval_min_score`, timeouts, row caps).

Folders of interest (final layout):
```
app/                # agents, routing, contracts, prompts
infra/              # logging, tracing, db, checkpointer
scripts/            # ingest_analytics.py, ingest_vectors.py, explain_sql.py, gen_allowlist.py
data/raw/analytics # Olist CSVs (not tracked by git)

data/docs          # RAG source docs (not tracked)
```

---

## Local development
### Prerequisites
- Python **3.11+**
- Docker + Docker Compose
- GNU Make

### Quickstart (Docker-first)
```bash
# 1) Create data folders
make dirs

# 2) Start Postgres (pgvector)
make db-start db-wait db-init

# 3) (Later) Build and run the app image once Dockerfile exists
make app-build
make app-run CMD="python -m app.graph.assistant"
```

### Python venv (optional, for local runs)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pre-commit install
```

### Environment variables
Create a `.env` file (used by Docker targets) with values appropriate to your environment.
```dotenv
# OpenAI
OPENAI_API_KEY=sk-...

# Postgres (Makefile defaults also set a user/pass/db)
POSTGRES_USER=app
POSTGRES_PASSWORD=app
POSTGRES_DB=app
POSTGRES_PORT=5432

# App URLs
DATABASE_URL=postgresql+psycopg://app:app@localhost:5432/app
```

### Data folders
- Place Olist CSVs under `data/raw/analytics/` (kept outside the chat; not committed).
- Place RAG docs (PDF/TXT) under `data/docs/`.

---

## Docker & Make targets
Run `make help` to see all targets. Common ones:
- `db-start` / `db-wait` / `db-init` / `db-psql` / `db-backup` / `db-restore FILE=...`
- `app-build` / `app-run` / `app-sh`
- `ingest-analytics` / `ingest-vectors` / `explain-sql` (available when scripts land)
- `compose-up` / `compose-down`
- `prune` / `clean`

---

## Testing
```bash
pytest -q
```

---

## Code & prompts conventions
- **Language**: source code in **English**; runtime answers to users in **pt-BR**.
- **Style**: PEP-8, PEP-257 docstrings, full type hints.
- **Prompts**: versioned under `app/prompts/{routing,analytics,knowledge,commerce}`; few-shot, contrastive, and minimal.
- **Git workflow**: branches as `<type>/<area>-<scope>/<short-task-slug>`; **Conventional Commits**; **commit only at the end of each phase** in this POC.

---

## Safety & guardrails
- Analytics: allowlist-only SQL, read-only, no DDL/DML, no `SELECT *`, enforced LIMITs.
- Knowledge (RAG): citations required; use `no_context=true` with follow-ups when retrieval signal is weak.
- Commerce: normalize amounts/currencies/dates; validate line sum ≈ subtotal; flag risks/warnings.

---

## License
MIT
