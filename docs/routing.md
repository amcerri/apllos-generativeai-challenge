# Routing: Classifier, Supervisor, Allowlist

This document explains how messages are routed to agents using an LLM-based classifier with deterministic supervision and allowlist context.

## Classifier ([app/routing/llm_classifier.py](../app/routing/llm_classifier.py))

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

## Supervisor ([app/routing/supervisor.py](../app/routing/supervisor.py))

- Purpose: apply simplified guardrails on top of classifier output with LLM-first approach; single-pass fallback, no loops.
- Inputs: `RouterDecision` and optional `RoutingContext` (RAG hits, allowlist hints).
- Rules:
  - Commerce guard: if `commerce_doc` in signals → force `commerce` with high confidence.
  - Simplified fallbacks (removed problematic redirections):
    - analytics → knowledge when doc cues present and no allowlist cues
    - knowledge → analytics when allowlist cues present
    - triage → knowledge/analytics based on cues
  - Confidence recalibration: bumps to conservative targets (`~0.8`) on fallback.

## Allowlist

- Generated from schema via [scripts/gen_allowlist.py](../scripts/gen_allowlist.py) into `app/routing/allowlist.json`.
- Embedded defaults are used if file is absent to avoid IO during request path ([app/graph/assistant.py](../app/graph/assistant.py)).
- Planner validates identifiers strictly against allowlist; executor enforces read-only and further safety.

## Design Considerations

- LLM-first approach: prioritize LLM decisions with intelligent fallbacks.
- Context-first: prefer structural evidence (allowlist, SQL shape) over keywords.
- State-of-the-art prompt engineering: Chain-of-Thought, self-consistency checks, confidence calibration.
- Determinism under failure: when LLM unavailable, heuristic ensures predictable routing.
- Safety: limit to single fallback per message to avoid oscillation.
