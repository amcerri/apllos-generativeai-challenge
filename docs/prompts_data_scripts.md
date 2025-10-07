# Prompts, Data, and Scripts

## Prompts (`app/prompts/*`)

- Analytics
  - [planner_system.txt](../app/prompts/analytics/planner_system.txt): system prompt for SQL planning (allowlist injected runtime).
  - [examples.jsonl](../app/prompts/analytics/examples.jsonl): few-shot examples for planner LLM path.
  - [normalizer_system.txt](../app/prompts/analytics/normalizer_system.txt), [normalizer_examples.jsonl](../app/prompts/analytics/normalizer_examples.jsonl): used by analytics normalizer LLM path.
- Knowledge
  - [system.txt](../app/prompts/knowledge/system.txt), [examples.jsonl](../app/prompts/knowledge/examples.jsonl): knowledge agent context.
- Commerce
  - [extractor_system.txt](../app/prompts/commerce/extractor_system.txt), [examples.jsonl](../app/prompts/commerce/examples.jsonl): LLM extractor guidance.
- Routing
  - [system.txt](../app/prompts/routing/system.txt), [examples.jsonl](../app/prompts/routing/examples.jsonl): optional classifier examples.

Notes: Agent code embeds fallback prompts to avoid blocking IO during requests.

## Data

- `data/raw/analytics/*`: Olist CSV datasets.
- `data/docs`: PDFs/DOCX/TXT for ingestion into `doc_chunks`.
- [data/samples/schema.sql](../data/samples/schema.sql) and [seed.sql](../data/samples/seed.sql): vector table DDL and sample seeds.

## Scripts (`scripts/*`)

- [ingest_analytics.py](../scripts/ingest_analytics.py): loads CSVs into Postgres according to schema; supports truncate/analyze.
- [ingest_vectors.py](../scripts/ingest_vectors.py): builds embeddings and ingests into `doc_chunks` (requires `OPENAI_API_KEY`); runs `ANALYZE`.
- [gen_allowlist.py](../scripts/gen_allowlist.py): generates `app/routing/allowlist.json` from schema.
- [query_assistant.py](../scripts/query_assistant.py): CLI that talks to LangGraph server (`/graph` threads/runs API). Supports attachment base64 for binaries and text for plaintext.
- [batch_query.py](../scripts/batch_query.py): batch runner for YAML queries; outputs optional Markdown.

## Operational Tips

- Always run `make ingest-analytics` and `make ingest-vectors` before RAG/analytics queries.
- Regenerate `allowlist.json` when the analytics schema changes.
