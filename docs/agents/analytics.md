# Analytics Agent

Covers the planner, executor, and normalizer modules.

## Planner (`app/agents/analytics/planner.py`)

- Purpose: Translate NL requests into safe SQL bounded by an allowlist.
- Features:
  - Heuristics for preview/aggregate/time series queries.
  - Allowlist validation of identifiers; join validation; schema prefix fixing; alias dot fixes.
  - Optional OpenAI JSON Schema backend using `llm_client` and prompts.
  - Config-driven limits: `default_limit`, `max_limit`, examples count.
- Output: `PlannerPlan` with `sql`, `params`, `reason`, `limit_applied`, `warnings`.

## Executor (`app/agents/analytics/executor.py`)

- Purpose: Execute planner SQL safely.
- Safety:
  - Read-only transaction; `statement_timeout` per query.
  - Client row caps; GROUP BY heuristic raises cap to avoid truncating categorical sets.
  - EXPLAIN (FORMAT JSON) attached when requested; optional ANALYZE via env.
  - Circuit breaker keyed by SQL hash with backoff after repeated failures.
- Output: `ExecutorResult` with `rows`, counts, latency, warnings, and `meta` (sql, row_cap, timeout, explain, breaker stats).

## Normalizer (`app/agents/analytics/normalize.py`)

- Purpose: Convert raw rows into PT-BR business narrative.
- Paths:
  - LLM-based: system prompt + examples; produces JSON (`text`, optional structured payload).
  - Fallback: deterministic formatting with insights for small/medium/large datasets.
- Extras:
  - Pattern detection (temporal trends, dominance, geographic concentration, category concentration, 1:1 ratios).
  - For large outputs, sampling for LLM then full data appended in response.
