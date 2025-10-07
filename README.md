# Apllos Generative AI Challenge

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org) [![LangGraph](https://img.shields.io/badge/LangGraph-0.6+-green.svg)](https://langchain-ai.github.io/langgraph/) [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://postgresql.org) [![Docker](https://img.shields.io/badge/Docker-20+-blue.svg)](https://docker.com) [![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-purple.svg)](https://openai.com)

> Multi‑Agent assistant for e‑commerce analytics, knowledge retrieval (RAG) and commerce document processing, powered by LangGraph.

---

## Contents

- Overview
- Architecture
- Quick Start
- Configuration
- Usage (Studio, CLI)
- Agents (Analytics, Knowledge, Commerce, Triage)
- API (health, graph)
- Development (Makefile targets, scripts)
- Testing
- Observability
- Troubleshooting
- License

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
graph TB
    subgraph "Interface"
        CLI[CLI]
        API[REST (FastAPI)]
        STUDIO[LangGraph Studio]
    end
    subgraph "Orchestration"
        LG[LangGraph]
        RT[LLM Router]
        SP[Supervisor]
    end
    subgraph "Agents"
        KA[Knowledge (RAG)]
        AA[Analytics]
        CA[Commerce]
        TR[Triage]
    end
    subgraph "Data"
        PG[(PostgreSQL analytics)]
        VEC[(pgvector doc_chunks)]
        DOCS[(Docs store)]
    end
    subgraph "External"
        OAI[OpenAI]
    end
    CLI-->API
    STUDIO-->LG
    API-->RT-->SP
    SP-->KA
    SP-->AA
    SP-->CA
    SP-->TR
    KA-->VEC
    AA-->PG
    CA-->DOCS
    KA-->OAI
    AA-->OAI
    CA-->OAI
```

Key decisions
- Fallbacks everywhere (no hard deps at import time)
- Settings via Pydantic + YAML; models centralizados em `settings.models.*`
- Human approval gates para SQL (interrupts) quando habilitado

---

## Quick Start

### Docker (recomendado)
```bash
# 1) Clone
git clone https://github.com/amcerri/apllos-generativeai-challenge.git
cd apllos-generativeai-challenge

# 2) Variáveis de ambiente
cp .env.example .env
# edite .env (OPENAI_API_KEY, etc.)

# 3) Bootstrap completo (DB + ingestões + Studio)
make bootstrap-complete

# 4) Acesse
make studio-up
# Health check estendido
curl http://localhost:2024/ok
# => {"status":"ok","db":"ok|down","checkpointer":"ok|noop"}
```

### Ambiente local
```bash
# Dependências
pip install -e .

# Banco
make db-start
make db-wait
make db-init
make db-seed

# Ingestões
make ingest-analytics
make ingest-vectors   # inclui ANALYZE doc_chunks

# Studio
make studio-up
```

Quick test (CLI)
```bash
# Analytics
make query QUERY="Quantos pedidos existem no total?"
# Knowledge
make query QUERY="Quais são as melhores práticas de precificação no e-commerce?"
# Commerce com documento
make query QUERY="Analise este pedido" ATTACHMENT="data/samples/orders/Simple Order.docx"
```

---

## Configuration

- `.env` (carregado pelo runtime) + YAMLs em `app/config/*.yaml`
- Settings Pydantic (`app/config/settings.py`) com nested keys e substituição de env

Principais variáveis
```bash
OPENAI_API_KEY=...
DATABASE_URL=postgresql+psycopg://app:app@localhost:5432/app
LOG_LEVEL=INFO
REQUIRE_SQL_APPROVAL=false
```

Modelos centralizados
- `settings.models.router`
- `settings.models.analytics_planner`
- `settings.models.analytics_normalizer`
- `settings.models.knowledge_answerer` (e mini)
- `settings.models.commerce_extractor`, `commerce_summarizer`
- `settings.models.embeddings`

Row caps e timeouts (analytics executor)
- `analytics.executor.default_timeout_seconds`
- `analytics.executor.default_row_cap`
- Heurística: se SQL contém `GROUP BY`, eleva cap ao máximo configurado (evita truncar listas pequenas como 27 estados)

---

## Usage

### LangGraph Studio
- UI: `https://smith.langchain.com/studio/?baseUrl=http://localhost:2024`
- Threads: preservam contexto; visualize estado, nós e interrupções humanas

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
- Retriever: pgvector sobre `doc_chunks` (1536 dims), filtros leves, dedupe por doc
- Ranker: heurístico (overlap, frase, penalidades de tamanho)
- Answerer: resposta PT‑BR com citações; fallback extractivo se LLM indisponível

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
- Processor: PDF/DOCX/TXT/Imagens com OCR (Tesseract) e fallbacks
- Extractor (LLM): JSON Schema estruturado (modelos via `settings.models`)
- Summarizer: visão executiva PT‑BR, riscos e próximos passos

### Triage
- Resposta curta PT‑BR quando faltar contexto + follow‑ups objetivos

---

## API

Endpoints (ASGI — `app/api/server.py`)
- `GET /`     → landing
- `GET /health` → liveness
- `GET /ready`  → readiness
- `GET /ok`     → health estendido (DB e checkpointer)
- `GET /graph`  → handlers do LangGraph Server (Studio)

---

## Development

Estrutura
```bash
app/        # código principal
scripts/    # ingestões, batch, CLI
data/       # datasets e amostras
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
- `scripts/ingest_analytics.py`: carrega CSVs Olist
- `scripts/ingest_vectors.py`: indexa documentos em `doc_chunks`
- `scripts/gen_allowlist.py`: gera allowlist (tabelas/colunas) em `app/routing/allowlist.json`
- `scripts/query_assistant.py`: CLI para consultar o assistente (Studio server)

---

## Testing

- Unit: `tests/unit/*`
- E2E: `tests/e2e/*`
- Batch YAMLs: `tests/batch/*.yaml`

Executar
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

Tracing (opcional)
```python
from app.infra.tracing import start_span
with start_span("node.analytics.exec"):
    ...
```

Health
```bash
curl http://localhost:2024/ok
# {"status":"ok","db":"ok|down","checkpointer":"ok|noop"}
```

---

## Troubleshooting

- Banco não responde
```bash
make db-status
make db-stop && make db-start
```
- OpenAI indisponível
```bash
echo $OPENAI_API_KEY
```
- Vetores lentos após ingestão: confirme `ANALYZE doc_chunks;` (Make já inclui)

---

## License

MIT
