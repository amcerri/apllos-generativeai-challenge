# Architecture and Graph Orchestration

This document explains the overall system architecture and how LangGraph orchestrates the multi-agent pipelines.

## High-Level Architecture

- Interface: CLI, REST API (FastAPI), LangGraph Studio.
- Orchestration: LangGraph graph with routing classifier and deterministic supervisor.
- Agents: Analytics, Knowledge (RAG), Commerce, Triage.
- Data: PostgreSQL (analytics), pgvector `doc_chunks` (RAG), local docs store.
- External: OpenAI (chat + embeddings), optional Prometheus/OpenTelemetry.

See project [README.md](../README.md) for a mermaid diagram.

## Graph Overview ([app/graph/build.py](../app/graph/build.py))

- Typed `GraphState` with per-key channels for safe fan-out in Studio.
- Nodes:
  - `route`: LLM classifier (or heuristic fallback) + allowlist injection.
  - `supervisor`: deterministic guardrails; single-pass fallback between analytics/knowledge/triage; commerce guard.
  - Analytics: `analytics.plan` → `analytics.exec` → `analytics.normalize`.
  - Knowledge: `knowledge.retrieve` → `knowledge.rank` → `knowledge.answer`.
  - Commerce: `commerce.process_doc` → `commerce.extract_llm` → `commerce.summarize`.
  - Triage: `triage.handle`.
- Human-in-the-loop: optional SQL approval gate emitted before execution (`make_sql_gate`).
- Checkpointer: compiled graph optionally uses PostgresSaver; falls back to no-op.

### Routing

- Classifier ([app/routing/llm_classifier.py](../app/routing/llm_classifier.py)):
  - Primary: OpenAI JSON Schema structured output via centralized LLM client.
  - Fallback: heuristic context-first rules (allowlist hits, SQL-ish structure, commerce cues).
  - Output normalized to `RouterDecision` contract.
- Supervisor ([app/routing/supervisor.py](../app/routing/supervisor.py)):
  - Context-first deterministic rules; single fallback to avoid loops.
  - Confidence recalibration; commerce domination when `commerce_doc` signal exists.

### Analytics Pipeline

- Planner: NL → safe SQL with allowlist validation; schema prefix fixing; join rules.
- Executor: read-only transaction; statement_timeout; client row-cap; optional EXPLAIN; circuit breaker per SQL hash.
- Normalizer: PT-BR narrative; LLM path with robust fallback; insights for large datasets.

### Knowledge Pipeline

- Retriever: OpenAI embeddings or deterministic hash fallback; pgvector cosine search; filters; per-doc dedupe.
- Ranker: heuristic reranker with optional LLM reranker.
- Answerer: PT-BR composition; attempts LLM; extractive fallback; always returns citations.

### Commerce Pipeline

- Processor: PDF/DOCX/TXT/Image extraction; OCR fallback; metadata and warnings.
- LLM Extractor: JSON Schema structured output; heuristic fallback on error/unavailable.
- Summarizer: PT-BR summary with totals, top items, risks, and follow-ups.

## API Layer ([app/api/server.py](../app/api/server.py))

- FastAPI app with `/`, `/health`, `/ready`, `/ok` endpoints; mounts LangGraph server at `/graph`.
- Metrics mount at `/metrics` when Prometheus client is available.
- Graceful fallbacks when optional dependencies are absent.

## Configuration ([app/config/settings.py](../app/config/settings.py) + YAMLs)

- Pydantic Settings + YAML merge with env substitution.
- Centralized model configs and feature flags (reranker, normalizer).
- Analytics limits and timeouts; RAG thresholds; OCR settings.

## Observability

- Logging: stdlib logging with contextvars and JSON mode option.
- Metrics: optional Prometheus counters/histograms.
- Tracing: optional OpenTelemetry with no-op fallbacks and log correlation.

## Safety Principles

- Defense-in-depth:
  - Planner allowlist validation; join rules; schema prefix fixes.
  - Executor read-only, timeouts, row caps, and EXPLAIN-only dry-run on rejected approvals.
  - Knowledge ranker deterministic fallback; answerer extractive fallback.
  - Commerce extractor reconciles totals and flags inconsistencies.
- Single-pass routing fallback; no loops.

## Failure Modes and Fallbacks

- Missing dependencies (LLM/DB/langgraph/prometheus/otel): graceful stubs or no-ops.
- LLM errors: planner/normalizer/answerer/extractor revert to deterministic strategies.
- DB errors/timeouts: executor circuit breaker opens for repeated failures.

## Extensibility

- Add new agent: create pipeline nodes and wire conditional edge from `supervisor`.
- Replace LLMs: adjust centralized `llm_client` or settings.
- Add metrics: register counters/histograms in `infra.metrics`.
