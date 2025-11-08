# Triage Agent

Covers the triage handler used when context is missing or classification is weak, and handles meta questions about system capabilities and usage.

## Handler ([app/agents/triage/handler.py](../../app/agents/triage/handler.py))

- Heuristic suggestion of agent based on keywords and router signals.
- Returns concise PT-BR guidance with follow-up questions to unlock routing.
- Uses `Answer` contract when available; otherwise returns dict with `text`, `meta`, `followups`.
- Meta question detection: automatically detects and responds to questions about system capabilities or usage.

## Meta Question Detection

The Triage agent automatically detects meta questions about system capabilities or usage and provides detailed responses:

- **Capabilities Questions**: Questions like "Quais suas funções?", "O que você pode fazer?", "Como você funciona?"
  - Returns detailed information about all system capabilities and agent specializations.
  
- **Usage Questions**: Questions like "Como faço para consultar pedidos?", "Como usar para buscar dados?"
  - Returns guidance on how to use the system for specific tasks.

Meta questions are detected using pattern matching and routed directly to Triage, bypassing normal routing logic.

## Design

- Prioritizes clarity and next steps over attempting to answer without context.
- Works as a safe default when classifier confidence is low or signals conflict.
- Provides detailed system information when users ask about capabilities or usage.

---

**← [Back to Documentation Index](../README.md)**
