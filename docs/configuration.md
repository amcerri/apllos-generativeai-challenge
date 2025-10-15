# Configuration and Models Settings

Explains the configuration model ([app/config/settings.py](../app/config/settings.py)) and YAML files under `app/config/*.yaml`.

## Settings Loader

- `Settings` (Pydantic Settings) merges:
  - [config.yaml](../app/config/config.yaml): app/server basics
  - [models.yaml](../app/config/models.yaml): LLM and embeddings models
  - [agents.yaml](../app/config/agents.yaml): per-agent settings
  - [database.yaml](../app/config/database.yaml): DB and checkpointer
  - [observability.yaml](../app/config/observability.yaml): logging, tracing, debug
- Environment variables support with `${VAR:-default}` substitution.
- Global accessor: `from app.config.settings import get_settings`.

## Key Sections

- `models`:
  - `router`, `analytics_planner`, `analytics_normalizer`, `knowledge_answerer`, `knowledge_answerer_mini`, `commerce_extractor`, `commerce_conversation`, `commerce_summarizer`, `embeddings`.
  - Flags: `tier`, `enable_reranker`, `enable_normalizer_llm`.
- `analytics`:
  - `planner`: default/max limits, disallow `SELECT *`, enforce LIMIT.
  - `sql`: read-only, max_rows, timeout, `allowlist_path`.
  - `executor`: default timeout (increased to 120s), row caps, max cap; EXPLAIN ANALYZE toggle; window functions support.
  - `normalizer`: examples in prompt, JSON extraction, `complete_data_threshold` (configurable, default 100 records).
- `knowledge`:
  - `retrieval`: top_k, min_score, dedupe, index, default_min_score.
  - `ranker`: rerank_top_k.
  - `answerer`: max_tokens, require_citations, summary char caps, cross-validation.
- `commerce`:
  - `extraction`: min_confidence, JSON schema strictness, Chain-of-Thought reasoning.
  - `validation`: line_total tolerance, default currency.
  - `summarizer` and `conversation` parameters with confidence calibration.
- `document_processing`: OCR settings, supported formats, size/page limits.
- `routing`: thresholds for LLM-first classifier/supervisor interplay with RAG; enhanced validation rules.
- `interruptions`: human approval required actions and timeouts.
- `database`: URL, pooling, echo, read-only default.
- `checkpointer`: enabled/backend/table/cleanup.
- `observability`: log level/JSON, tracing flag/ratio (increased to 60s), debug toggles.

## Environment Variables

Common vars:

- `OPENAI_API_KEY`, `OPENAI_API_BASE`
- `DATABASE_URL`
- `LOG_LEVEL`, `STRUCTLOG_JSON`
- `REQUIRE_SQL_APPROVAL`
- `TRACING_ENABLED`

## Overriding Models

- Override model names via env (e.g., `ANALYTICS_PLANNER_MODEL`) or YAML edits.
- Embeddings dimensions must match pgvector index (`1536` by default).
