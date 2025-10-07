# Testing Strategy and Guardrails

Describes the unit, e2e, and batch tests and the safety guarantees they enforce.

## Overview

- Unit tests under `tests/unit/*` validate planner heuristics/joins/props, executor guards/breaker, knowledge retrieval, commerce extraction heuristics, router contract shape, triage handler.
- E2E tests under `tests/e2e/*` validate human gates and routing paths.
- Batch YAMLs in `tests/batch/*.yaml` provide scenario inputs for manual/batch runs.

## Key Safety Assertions

- Planner:
  - Enforces allowlist identifiers, blocks cross-schema joins, requires LIMIT on non-aggregate queries, fixes schema prefixes and alias issues.
- Executor:
  - Only SELECT/WITH, forbids DDL/DML and unknown functions; statement timeout, client row caps; EXPLAIN-only dry run on rejected approvals; circuit breaker opens on repeated failures.
- Knowledge:
  - Retrieval with min_score threshold; dedupe per `doc_id`; ranker deterministic; answerer returns citations.
- Commerce:
  - Heuristic extraction parses items/totals; reconciles components to detect inconsistencies; flags risks.
- Routing:
  - RouterDecision contract is strict; supervisor applies single-pass fallbacks; confidence bounds enforced.

## Human-in-the-Loop

- `app/graph/interrupts.py` provides `make_sql_gate` used by analytics executor when `require_sql_approval=True`.
- E2E test checks shape/serializability of gates and the graph builder toggle.

## CI Considerations

- Tests avoid hard dependencies where possible; modules degrade to stubs; network calls are avoided in unit tests.
