# Triage Agent

Covers the triage handler used when context is missing or classification is weak.

## Handler ([app/agents/triage/handler.py](../../app/agents/triage/handler.py))

- Heuristic suggestion of agent based on keywords and router signals.
- Returns concise PT-BR guidance with follow-up questions to unlock routing.
- Uses `Answer` contract when available; otherwise returns dict with `text`, `meta`, `followups`.

## Design

- Prioritizes clarity and next steps over attempting to answer without context.
- Works as a safe default when classifier confidence is low or signals conflict.
