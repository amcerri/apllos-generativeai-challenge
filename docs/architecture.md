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
  - Primary: OpenAI JSON Schema structured output via centralized LLM client with state-of-the-art prompt engineering.
  - Enhanced validation with critical override rules for conceptual questions, document processing, data queries, and greetings.
  - Fallback: heuristic context-first rules (allowlist hits, SQL-ish structure, commerce cues) with improved pattern matching.
  - Output normalized to `RouterDecision` contract.
- Supervisor ([app/routing/supervisor.py](../app/routing/supervisor.py)):
  - Simplified guardrails with LLM-first approach; single fallback to avoid loops.
  - Confidence recalibration; commerce domination when `commerce_doc` signal exists.

### Analytics Pipeline

- Planner: NL → safe SQL with allowlist validation; schema prefix fixing; join rules; Chain-of-Thought reasoning.
- Executor: read-only transaction; statement_timeout; client row-cap; optional EXPLAIN; circuit breaker per SQL hash; window functions support.
- Normalizer: LLM-first intelligent data balancing; PT-BR narrative with analytical insights; configurable thresholds for complete data vs. intelligent analysis.

### Knowledge Pipeline

- Retriever: OpenAI embeddings or deterministic hash fallback; pgvector cosine search; filters; per-doc dedupe.
- Ranker: heuristic reranker with optional LLM reranker.
- Answerer: PT-BR composition with cross-validation; Chain-of-Thought reasoning; confidence calibration; extractive fallback; always returns citations.

### Commerce Pipeline

- Processor: PDF/DOCX/TXT/Image extraction; OCR fallback; metadata and warnings.
- LLM Extractor: JSON Schema structured output with Chain-of-Thought reasoning and self-consistency checks; heuristic fallback on error/unavailable.
- Summarizer: PT-BR summary with totals, top items, risks, and follow-ups; confidence calibration.

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
  - Planner allowlist validation; join rules; schema prefix fixes; Chain-of-Thought reasoning.
  - Executor read-only, timeouts, row caps, window functions support, and EXPLAIN-only dry-run on rejected approvals.
  - Knowledge ranker deterministic fallback; answerer cross-validation and extractive fallback.
  - Commerce extractor reconciles totals and flags inconsistencies; self-consistency checks.
- LLM-first routing with intelligent fallbacks; single-pass routing fallback; no loops.

## Failure Modes and Fallbacks

- Missing dependencies (LLM/DB/langgraph/prometheus/otel): graceful stubs or no-ops.
- LLM errors: planner/normalizer/answerer/extractor revert to deterministic strategies.
- DB errors/timeouts: executor circuit breaker opens for repeated failures.

## Extensibility

- Add new agent: create pipeline nodes and wire conditional edge from `supervisor`.
- Replace LLMs: adjust centralized `llm_client` or settings.
- Add metrics: register counters/histograms in `infra.metrics`.
