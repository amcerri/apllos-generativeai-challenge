# Routing: Classifier, Supervisor, Allowlist

This document explains how messages are routed to agents using an LLM-based classifier with deterministic supervision and allowlist context.

## Classifier ([app/routing/llm_classifier.py](../app/routing/llm_classifier.py))

- Primary path: OpenAI JSON Schema via centralized `llm_client`.
  - System prompt injects allowlist JSON (tables → columns) to improve table/column extraction.
  - Examples are intentionally skipped at runtime to reduce latency; can be enabled with prompts.
- Fallback: deterministic heuristic routing when LLM is unavailable or errors.
  - Signals considered (ordered by weight):
    - Allowlist overlap (strong signal) → analytics
    - SQL-like structure (block or SELECT FROM) → analytics
    - Commerce cues (currency + totals terms) → commerce
    - Document-style phrasing without tabular cues → knowledge
- Output: normalized to `RouterDecision` (dataclass if available), including `agent`, `confidence`, `reason`, `tables`, `columns`, `signals`, `thread_id`.

## Supervisor ([app/routing/supervisor.py](../app/routing/supervisor.py))

- Purpose: apply guardrails on top of classifier output; single-pass fallback, no loops.
- Inputs: `RouterDecision` and optional `RoutingContext` (RAG hits, allowlist hints).
- Rules:
  - Commerce guard: if `commerce_doc` in signals → force `commerce` with high confidence.
  - Fallbacks:
    - analytics → knowledge when doc cues present and no allowlist cues
    - knowledge → analytics when allowlist cues present
    - triage → knowledge/analytics based on cues
  - Confidence recalibration: bumps to conservative targets (`~0.8`) on fallback.

## Allowlist

- Generated from schema via [scripts/gen_allowlist.py](../scripts/gen_allowlist.py) into `app/routing/allowlist.json`.
- Embedded defaults are used if file is absent to avoid IO during request path ([app/graph/assistant.py](../app/graph/assistant.py)).
- Planner validates identifiers strictly against allowlist; executor enforces read-only and further safety.

## Design Considerations

- Context-first: prefer structural evidence (allowlist, SQL shape) over keywords.
- Determinism under failure: when LLM unavailable, heuristic ensures predictable routing.
- Safety: limit to single fallback per message to avoid oscillation.
