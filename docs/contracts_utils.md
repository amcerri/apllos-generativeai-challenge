# Contracts and Utilities

## Contracts

### Answer (`app/contracts/answer.py`)

- Dataclass with fields: `text`, optional `data/columns`, `citations`, `chunks`, `meta`, `no_context`, `artifacts`, `followups`.
- JSON Schema provided for LLM Structured Outputs; strict validation in `from_dict`.
- `citations` enforce presence of `url` or `doc_id`.

### RouterDecision (`app/contracts/router_decision.py`)

- Dataclass with fields: `agent`, `confidence`, `reason`, `tables`, `columns`, `signals`, `thread_id`.
- JSON Schema for the LLM classifier; strict parsing disallows unknown keys.

## Utilities

### Validation (`app/utils/validation.py`)

- `clamp(value, minimum, maximum)`
- `safe_limit(limit, default=200, min_value=1, max_value=1000)`

### IDs (`app/utils/ids.py`)

- `short_uuid(length=8)`, `random_token(length=32)`, `stable_hash(value, length=16)`
- `make_thread_id(prefix="thr", suffix_len=8)`
- UUID helpers: `is_valid_uuid`, `parse_uuid`, `normalize_id`
- ULID utilities: `ulid()`, `is_valid_ulid()`

### Time (`app/utils/time.py`)

- UTC helpers: `as_utc`, `parse_iso8601`, `format_iso8601`
- Monotonic helpers: `monotonic_now`, `has_expired`, `remaining_ms`
