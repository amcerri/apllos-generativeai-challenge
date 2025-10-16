# Contracts and Utilities

This document provides comprehensive details about the data contracts, validation utilities, and helper functions used throughout the Apllos Assistant system.

## Data Contracts

The system uses strict data contracts to ensure type safety and validation across all components.

## Contracts

### Answer ([app/contracts/answer.py](../app/contracts/answer.py))

The `Answer` contract is the primary response format for all agents, ensuring consistent structure and validation.

**Fields**:
- `text`: Primary response text in PT-BR
- `data`: Optional structured data payload
- `columns`: Optional column metadata for tabular data
- `citations`: Required citations with `url` or `doc_id`
- `chunks`: Optional source chunks for RAG responses
- `meta`: Optional metadata and processing information
- `no_context`: Boolean flag for insufficient context
- `artifacts`: Optional artifacts and attachments
- `followups`: Optional follow-up questions

**Validation**:
- JSON Schema provided for LLM Structured Outputs
- Strict validation in `from_dict` method
- Citations must have either `url` or `doc_id`
- Type safety enforced through Pydantic models

### RouterDecision ([app/contracts/router_decision.py](../app/contracts/router_decision.py))

- Dataclass with fields: `agent`, `confidence`, `reason`, `tables`, `columns`, `signals`, `thread_id`.
- JSON Schema for the LLM classifier; strict parsing disallows unknown keys.

## Utilities

### Validation ([app/utils/validation.py](../app/utils/validation.py))

- `clamp(value, minimum, maximum)`
- `safe_limit(limit, default=200, min_value=1, max_value=1000)`

### IDs ([app/utils/ids.py](../app/utils/ids.py))

- `short_uuid(length=8)`, `random_token(length=32)`, `stable_hash(value, length=16)`
- `make_thread_id(prefix="thr", suffix_len=8)`
- UUID helpers: `is_valid_uuid`, `parse_uuid`, `normalize_id`
- ULID utilities: `ulid()`, `is_valid_ulid()`

### Time ([app/utils/time.py](../app/utils/time.py))

- UTC helpers: `as_utc`, `parse_iso8601`, `format_iso8601`
- Monotonic helpers: `monotonic_now`, `has_expired`, `remaining_ms`

---

**← [Back to Documentation Index](../README.md)**
