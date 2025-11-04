# Frontend (Chainlit)

This document explains the frontend chat interface used to interact with the multi‑agent graph. It focuses on implementation, integration points, and design decisions.

## Overview

The frontend is a Chainlit‑based chat UI that sends user input to the LangGraph runtime and renders responses, interruptions (e.g., SQL approval), and basic diagnostics when available. It is not a knowledge upload surface and does not modify the RAG index.

## Implementation

- Entrypoint and UI wiring: [frontend/chainlit_app.py](../frontend/chainlit_app.py)
- Backend client (LangGraph Server/API): [frontend/client.py](../frontend/client.py)
- Runtime configuration: [frontend/config.py](../frontend/config.py)
- Utilities (formatting/attachments): [frontend/utils.py](../frontend/utils.py)

### Integration

- Primary backend: LangGraph Server (Studio) mounted at `/graph` (see [app/api/server.py](../app/api/server.py)).
- Configuration via environment variables resolved in the frontend config; aligns with backend settings.
- Attachments are routed exclusively to the Commerce pipeline; they do not feed Knowledge (RAG).

## Design Decisions

- Chainlit chosen for rapid chat UI iteration and attachment handling.
- No RAG uploads from UI: Knowledge answers are constrained to existing `doc_chunks` index.
- Attachment guardrails limited to Commerce flows (PDF/DOCX/TXT/Images) to avoid scope drift.
- Minimal coupling: the client abstracts Graph Server vs. API differences.

---

**← [Back to Documentation Index](../README.md)**


