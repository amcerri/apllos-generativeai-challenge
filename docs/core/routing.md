# Routing: LLM-First with Ensemble and Probes

This document provides a comprehensive overview of the routing system, explaining the differences between the Router (LLM Classifier) and Supervisor, and detailing the ensemble routing capabilities.

## Overview

The routing system consists of two main components working in tandem:

- **Router (LLM Classifier)**: `app/routing/llm_classifier.py::LLMClassifier` - Primary decision maker using LLM
- **Supervisor**: `app/routing/supervisor.py::supervise` - Deterministic guardrails and fallback logic
- **Probes**: Evidence-gathering mechanisms executed in `app/graph/build.py::node_route` and passed as `routing_ctx` to supervisor

## Router vs Supervisor: Key Differences

### Router (LLM Classifier)
**Purpose**: Primary intelligent decision maker using LLM with structured output

**Responsibilities**:
- Analyzes natural language queries for intent and context
- Uses state-of-the-art prompt engineering with Chain-of-Thought reasoning
- Produces structured `RouterDecision` with confidence scores
- Implements ensemble routing with multiple LLM variants
- Falls back to deterministic heuristics when LLM unavailable

**Key Features**:
- JSON Schema structured output for consistent decision format
- Enhanced validation with critical override rules
- Context-first routing prioritizing structural evidence
- Self-consistency checks and confidence calibration
- Few-shot examples for improved classification accuracy

**Output**: `RouterDecision` containing:
- `agent`: Target agent (analytics, knowledge, commerce, triage)
- `confidence`: Confidence score (0.0-1.0)
- `reason`: Human-readable explanation
- `tables`: Detected database tables
- `columns`: Detected database columns
- `signals`: Routing signals and hints
- `thread_id`: Conversation thread identifier

### Supervisor
**Purpose**: Deterministic guardrails and business rule enforcement

**Responsibilities**:
- Applies safety constraints and business rules
- Handles single-pass fallbacks to prevent routing loops
- Recalibrates confidence scores conservatively
- Enforces domain-specific routing rules
- Provides final routing decision with safety guarantees

**Key Features**:
- Commerce document dominance detection
- Analytics vs Knowledge fallback logic
- Confidence recalibration for fallback decisions
- Single-pass fallback to avoid oscillations
- Context-aware routing using probe signals

**Input**: `RouterDecision` + `RoutingContext` (probe results)
**Output**: Final `RouterDecision` with applied guardrails

### Decision Flow

```
Query → Router (LLM) → RouterDecision → Supervisor → Final Decision → Agent
  ↓         ↓              ↓              ↓             ↓               ↓
Input   Analysis       Structured      Guardrails   Validated      Specialized
        & Context       Decision      & Fallbacks    Decision      Processing
```

## Router Implementation Details

## Improvements

- Evidence-augmented probes in `route` node:
  - Attachment probe → signals: `attachment_present`, `attachment_mime:<mime>`
  - SQL probe → signal: `sql_probe_true`
  - Shallow RAG probe (top_k=2, min_score=0.82) → signals: `rag_probe_hit`, plus `routing_ctx.rag_hits`, `routing_ctx.rag_min_score`
- Supervisor consumes `RoutingContext` to apply safer, context-first fallbacks.
- Ensemble router (feature-flagged) with scorer tie-breaker:
  - Variants: neutral, analytics-focused, commerce-focused examples
  - Majority vote; on tie, scorer picks the best candidate

## Environment Flags

- `ROUTER_ENSEMBLE_ENABLED` (default: true) — enables ensemble routing
- `ROUTER_SCORER_ENABLED` (default: true) — enables scorer tie-breaker
- `ROUTER_CALIBRATION` (JSON) — piecewise confidence calibration mapping
- `ROUTER_SECONDARY_HINTS` (default: true) — emits secondary intent hints in `signals`

## Signals

Classifier output signals are augmented by route probes; supervisor logs and keeps `signals` for observability:

- `ensemble_majority`, `ensemble_scorer`
- `attachment_present`, `attachment_mime:<mime>`
- `sql_probe_true`
- `rag_probe_hit`
- `supervisor_fallback`

## Tests

- `tests/unit/test_routing_ensemble.py` — ensemble majority and scorer tie-break
- `tests/unit/test_supervisor_routing_ctx.py` — supervisor fallback using `RoutingContext`
- `scripts/eval_routing.py` + `make test-routing` — evaluation harness over a labeled set

## Routing: Classifier, Supervisor, Allowlist

This section explains how messages are routed to agents using an LLM-based classifier with deterministic supervision and allowlist context.

### Classifier ([app/routing/llm_classifier.py](../app/routing/llm_classifier.py))

- Primary path: OpenAI JSON Schema via centralized `llm_client` with state-of-the-art prompt engineering.
  - System prompt injects allowlist JSON (tables → columns) to improve table/column extraction.
  - Chain-of-Thought reasoning, self-consistency checks, and confidence calibration.
  - Enhanced validation with critical override rules for conceptual questions, document processing, data queries, and greetings.
- Fallback: deterministic heuristic routing when LLM is unavailable or errors.
  - Signals considered (ordered by weight):
    - Allowlist overlap (strong signal) → analytics
    - SQL-like structure (block or SELECT FROM) → analytics
    - Commerce cues (currency + totals terms) → commerce
    - Document-style phrasing without tabular cues → knowledge
    - Greeting patterns → triage
    - Farewell patterns → triage
- Output: normalized to `RouterDecision` (dataclass if available), including `agent`, `confidence`, `reason`, `tables`, `columns`, `signals`, `thread_id`.

### Supervisor ([app/routing/supervisor.py](../app/routing/supervisor.py))

- Purpose: apply simplified guardrails on top of classifier output with LLM-first approach; single-pass fallback, no loops.
- Inputs: `RouterDecision` and optional `RoutingContext` (RAG hits, allowlist hints).
- Rules:
  - Commerce guard: if `commerce_doc` in signals → force `commerce` with high confidence.
  - Simplified fallbacks (removed problematic redirections):
    - analytics → knowledge when doc cues present and no allowlist cues
    - knowledge → analytics when allowlist cues present
    - triage → knowledge/analytics based on cues
  - Confidence recalibration: bumps to conservative targets (`~0.8`) on fallback.

### Allowlist

- Generated from schema via [scripts/gen_allowlist.py](../scripts/gen_allowlist.py) into `app/routing/allowlist.json`.
- Embedded defaults are used if file is absent to avoid IO during request path ([app/graph/assistant.py](../app/graph/assistant.py)).
- Planner validates identifiers strictly against allowlist; executor enforces read-only and further safety.

### Design Considerations

- LLM-first approach: prioritize LLM decisions with intelligent fallbacks.
- Context-first: prefer structural evidence (allowlist, SQL shape) over keywords.
- State-of-the-art prompt engineering: Chain-of-Thought, self-consistency checks, confidence calibration.
- Determinism under failure: when LLM unavailable, heuristic ensures predictable routing.
- Safety: limit to single fallback per message to avoid oscillation.

---

**← [Back to Documentation Index](../README.md)**
