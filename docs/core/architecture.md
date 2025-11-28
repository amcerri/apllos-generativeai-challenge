# Architecture and Graph Orchestration

This document explains the overall system architecture and how LangGraph orchestrates the multi-agent pipelines.

## High-Level Architecture

The project is built on a multi-agent architecture that combines LLM-first decision making with deterministic fallbacks. The system is designed for high availability, safety, intelligent routing, and an end-to-end async I/O model (FastAPI → LangGraph → agents → LLM/DB), using `async/await` and `asyncio.to_thread` to avoid blocking the event loop.

### Core Components

- **Interface Layer**: CLI, REST API (FastAPI), LangGraph Studio
- **Orchestration Layer**: LangGraph graph with intelligent routing and deterministic supervision
- **Agent Layer**: Four specialized agents (Analytics, Knowledge, Commerce, Triage)
- **Data Layer**: PostgreSQL (analytics), pgvector `doc_chunks` (RAG), local document store
- **Infrastructure Layer**: LLM client, database connections, observability stack
- **External Services**: OpenAI (chat + embeddings), optional Prometheus/OpenTelemetry

### System Flow

```
User Input   →   Router   →   Supervisor   →   Agent Pipeline   →   LLM Processing   →   Database   →   Response
     ↓             ↓              ↓                  ↓                    ↓                 ↓              ↓
  CLI/API      LLM-based     Guardrails         Specialized          OpenAI API         PostgreSQL       PT-BR
               Classifier   & Fallbacks         Processing          (GPT-4o-mini)       + pgvector       Output
```

See project [README.md](../README.md) for a detailed mermaid diagram.

## Graph Overview ([app/graph/build.py](../app/graph/build.py))

- Typed `GraphState` with per-key channels for safe fan-out in Studio.
- **Conversation Memory**: `GraphState` includes `conversation_history`, `last_agent`, and `last_answer` for context-aware routing and natural follow-up conversations.
- Nodes (all I/O-bound nodes are exposed as `async def` in the LangGraph definition):
  - `route`: LLM classifier (or heuristic fallback) + allowlist injection + conversation context integration.
  - `supervisor`: deterministic guardrails; single-pass fallback between analytics/knowledge/triage; commerce guard.
  - Analytics: `analytics.plan` → `analytics.exec` → `analytics.normalize`.
  - Knowledge: `knowledge.retrieve` → `knowledge.rank` → `knowledge.answer`.
  - Commerce: `commerce.process_doc` → `commerce.extract_llm` → `commerce.summarize`.
  - Triage: `triage.handle`.
  - `update_history`: Updates conversation history after each agent response.
- Human-in-the-loop: optional SQL approval gate emitted before execution (`make_sql_gate`).
- Checkpointer: compiled graph optionally uses PostgresSaver; falls back to no-op. Automatically persists conversation history.

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

- FastAPI app with `/`, `/health`, `/ready`, `/ok` endpoints (async handlers), and mounts the LangGraph server at `/graph`.
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
- DB errors/timeouts: executor circuit breaker opens for repeated failures

---

**← [Back to Documentation Index](../README.md)**
