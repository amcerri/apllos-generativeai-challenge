# Apllos Generative AI Challenge

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org) [![LangGraph](https://img.shields.io/badge/LangGraph-0.6+-green.svg)](https://langchain-ai.github.io/langgraph/) [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://postgresql.org) [![Docker](https://img.shields.io/badge/Docker-20+-blue.svg)](https://docker.com) [![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-purple.svg)](https://openai.com)

> Multi‑Agent assistant for e‑commerce analytics, knowledge retrieval (RAG) and commerce document processing, powered by LangGraph.

---

## Contents

- [Apllos Generative AI Challenge](#apllos-generative-ai-challenge)
  - [Contents](#contents)
  - [Overview](#overview)
  - [Architecture](#architecture)
  - [Quick Start](#quick-start)
    - [Docker (recomendado)](#docker-recomendado)
    - [Ambiente local](#ambiente-local)
  - [Configuration](#configuration)
  - [Usage](#usage)
    - [LangGraph Studio](#langgraph-studio)
    - [CLI (`scripts/query_assistant.py` via Make)](#cli-scriptsquery_assistantpy-via-make)
  - [Agents](#agents)
    - [Analytics](#analytics)
    - [Knowledge (RAG)](#knowledge-rag)
    - [Commerce](#commerce)
    - [Triage](#triage)
  - [API](#api)
  - [Development](#development)
  - [Testing](#testing)
  - [Observability](#observability)
  - [Troubleshooting](#troubleshooting)

---

## Overview

- Multi‑agent orchestration with router + supervisor and optional human approval gates
- Safe analytics SQL (allowlist, read‑only, timeouts, row caps)
- Knowledge RAG over pgvector (`doc_chunks`) with citations
- Commerce processor (PDF/DOCX/TXT/OCR) → LLM extraction → summarization
- Portable: Docker Compose or local development
- Strong DX: Makefile, scripts, tests, logging, optional tracing

---

## Architecture

```mermaid
flowchart TB
    subgraph "Interface"
        CLI["CLI"]
        API["REST (FastAPI)"]
        STUDIO["LangGraph Studio"]
    end
    subgraph "Orchestration"
        LG["LangGraph"]
        RT["LLM Router"]
        SP["Supervisor"]
    end
    subgraph "Agents"
        KA["Knowledge (RAG)"]
        AA["Analytics"]
        CA["Commerce"]
        TR["Triage"]
    end
    subgraph "Data"
        PG[("PostgreSQL analytics")]
        VEC[("pgvector doc_chunks")]
        DOCS[("Docs store")]
    end
    subgraph "External"
        OAI["OpenAI"]
    end
    CLI --> API
    STUDIO --> LG
    API --> RT --> SP
    SP --> KA
    SP --> AA
    SP --> CA
    SP --> TR
    KA --> VEC
    AA --> PG
    CA --> DOCS
    KA --> OAI
    AA --> OAI
    CA --> OAI
```

Key decisions
- Fallbacks everywhere (no hard deps at import time)
- Settings via Pydantic + YAML; models centralized under `settings.models.*`
- Human approval gates for SQL (interrupts) when enabled

---

## Quick Start

### Docker (recommended)

```bash
# 1) Clone
git clone https://github.com/amcerri/apllos-generativeai-challenge.git
cd apllos-generativeai-challenge

# 2) Environment variables
cp .env.example .env
# edit .env (OPENAI_API_KEY, etc.)

# 3) Full bootstrap (DB + ingestions + Studio)
make bootstrap-complete

# 4) Access
make studio-up
# Extended health check
curl http://localhost:2024/ok
# => {"status":"ok","db":"ok|down","checkpointer":"ok|noop"}
```

### Local environment

```bash
# Dependencies
pip install -e .

# Database
make db-start
make db-wait
make db-init
make db-seed

# Ingestions
make ingest-analytics
make ingest-vectors   # inclui ANALYZE doc_chunks

# Studio
make studio-up
```

Quick test (CLI)

```bash
# Analytics
make query QUERY="How many orders are there in total?"
# Knowledge
make query QUERY="What are the best pricing practices in e‑commerce?"
# Commerce with attachment
make query QUERY="Analyze this order" ATTACHMENT="data/samples/orders/Simple Order.docx"
```

---

## Configuration

- `.env` (loaded at runtime) + YAMLs in `app/config/*.yaml`
- Pydantic Settings (`app/config/settings.py`) with nested keys and env overrides

Key variables
```bash
OPENAI_API_KEY=...
DATABASE_URL=postgresql+psycopg://app:app@localhost:5432/app
LOG_LEVEL=INFO
REQUIRE_SQL_APPROVAL=false
```

Centralized model configs
- `settings.models.router`
- `settings.models.analytics_planner`
- `settings.models.analytics_normalizer`
- `settings.models.knowledge_answerer` (and mini)
- `settings.models.commerce_extractor`, `commerce_summarizer`
- `settings.models.embeddings`

Row caps and timeouts (analytics executor)
- `analytics.executor.default_timeout_seconds`
- `analytics.executor.default_row_cap`
- Heuristic: if SQL contains `GROUP BY`, raise cap to configured max (avoids truncating small lists like 27 states)

---

## Usage

### LangGraph Studio

- UI: `https://smith.langchain.com/studio/?baseUrl=http://localhost:2024`
- Threads preserve context; visualize state, nodes and human interrupts

### CLI (`scripts/query_assistant.py` via Make)

```bash
# Query simples
make query QUERY="Qual a receita total?"
# Com anexo (auto base64 p/ binários)
make query QUERY="Analise este pedido" ATTACHMENT="data/samples/orders/Simple Order.docx"
# Reusar thread
make query QUERY="Detalhe por estado" THREAD_ID=thr-...
```

---

## Agents

### Analytics
- Planner: NL → SQL seguro (allowlist, sem DDL/DML, prefix fix)
- Executor: read‑only, timeout, row cap (com heurística para GROUP BY)
- Normalizer: PT‑BR, formatação de negócios, fallback inteligente

### Knowledge (RAG)
- Retriever: pgvector over `doc_chunks` (1536 dims), light filters, per‑doc dedupe
- Ranker: heuristic (overlap, phrase, length penalties)
- Answerer: pt‑BR answer with citations; extractive fallback if LLM unavailable

RAG schema (DDL incluída em `data/samples/schema.sql`)
```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE IF NOT EXISTS doc_chunks (
  doc_id TEXT, chunk_id TEXT,
  title TEXT, content TEXT, source TEXT,
  metadata JSONB,
  embedding vector(1536),
  PRIMARY KEY (doc_id, chunk_id)
);
-- IVFFLAT (cosine)
CREATE INDEX IF NOT EXISTS idx_doc_chunks_embedding_ivfflat
  ON doc_chunks USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
```

### Commerce
- Processor: PDF/DOCX/TXT/Images with OCR (Tesseract) and fallbacks
- Extractor (LLM): structured JSON Schema (models via `settings.models`)
- Summarizer: executive pt‑BR view, risks and next steps

### Triage
- Short pt‑BR reply when context is missing + objective follow‑ups

---

## API

Endpoints (ASGI — `app/api/server.py`)
- `GET /`     → landing
- `GET /health` → liveness
- `GET /ready`  → readiness
- `GET /ok`     → extended health (DB and checkpointer)
- `GET /graph`  → LangGraph Server handlers (Studio)

---

## Development

Structure
```bash
app/        # main code
scripts/    # ingestions, batch, CLI
data/       # datasets and samples
```

Makefile (principais)
```bash
# Bootstrap
make bootstrap            # reset + setup + ingest + studio + validate
make bootstrap-complete   # sequência com logs explicativos

# Docker / App
make docker-build
make studio-up | studio-down
make api-up    | api-down
make app-status

# Banco
make db-start db-wait db-init db-seed db-reset db-status db-psql

# Ingestões
make ingest-analytics
make ingest-vectors    # inclui ANALYZE doc_chunks
make gen-allowlist
make ingest-all

# Testes / Validação
make test test-unit test-e2e validate

# Utilitários
make query           # QUERY="..." [ATTACHMENT=path] [THREAD_ID=thr]
make batch-query     # INPUT=queries.yaml [OUTPUT=results.md]
make logs logs-db shell shell-db clean install-deps
```

Scripts
- `scripts/ingest_analytics.py`: load Olist CSVs
- `scripts/ingest_vectors.py`: index documents into `doc_chunks`
- `scripts/gen_allowlist.py`: generate allowlist (tables/columns) into `app/routing/allowlist.json`
- `scripts/query_assistant.py`: CLI to query the assistant (Studio server)

---

## Testing

- Unit: `tests/unit/*`
- E2E: `tests/e2e/*`
- Batch YAMLs: `tests/batch/*.yaml`

Run
```bash
make test
make test-unit
make test-e2e
```

---

## Observability

Logging
```python
from app.infra.logging import get_logger
log = get_logger("agent.analytics").bind(thread_id="thr-1")
log.info("planned", sql="...", limit=200)
```

Tracing (optional)
```python
from app.infra.tracing import start_span
with start_span("node.analytics.exec"):
    ...
```

Health
Metrics (optional)
```bash
# If prometheus_client is installed, the API exposes /metrics
curl http://localhost:2024/metrics
# Prometheus scrape endpoint with counters and histograms
```

Directed tracing and node metrics
- The server configures a local metrics registry (when available) and exposes counters:
  - apllos_api_requests_total{agent,node}
  - apllos_api_routing_fallbacks_total{from_agent,to_agent}
  - apllos_api_llm_failures_total{component}
- Histograms:
  - apllos_api_node_latency_ms{node}

Normalizer prompts
- Analytics normalizer now loads system prompt and examples from `app/prompts/analytics/normalizer_system.txt` and `normalizer_examples.jsonl` when present, with an embedded fallback.

```bash
curl http://localhost:2024/ok
# {"status":"ok","db":"ok|down","checkpointer":"ok|noop"}
```

---

## Troubleshooting

- Database is not responding
```bash
make db-status
make db-stop && make db-start
```
- OpenAI unavailable
```bash
echo $OPENAI_API_KEY
```
- Vectors slow after ingestion: confirm `ANALYZE doc_chunks;` (Make already includes)
