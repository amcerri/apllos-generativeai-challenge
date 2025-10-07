# Glossary

- Agent: A specialized component (analytics, knowledge, commerce, triage) responsible for a pipeline.
- Allowlist: Mapping of tables → columns that constrains the planner and informs routing.
- Checkpointer: Persistence backend for LangGraph threads/state.
- Circuit breaker: Mechanism in executor to short-circuit repeated failures/timeouts.
- EXPLAIN: Postgres plan introspection; optionally ANALYZE for runtime stats.
- Heuristic: Deterministic rule-based logic used when LLM is unavailable or to add guardrails.
- RAG: Retrieval-Augmented Generation (retriever + ranker + answerer with citations).
- RouterDecision: Structured decision produced by the classifier.
- SQL Approval Gate: Human-in-the-loop interrupt requesting approval before executing SQL.
