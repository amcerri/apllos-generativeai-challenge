# Prompts, Data, and Scripts

## Prompts (`app/prompts/*`)

- Analytics
  - `planner_system.txt`: system prompt for SQL planning (allowlist injected runtime).
  - `examples.jsonl`: few-shot examples for planner LLM path.
  - `normalizer_system.txt`, `normalizer_examples.jsonl`: used by analytics normalizer LLM path.
- Knowledge
  - `system.txt`, `examples.jsonl`: knowledge agent context.
- Commerce
  - `extractor_system.txt`, `examples.jsonl`: LLM extractor guidance.
- Routing
  - `system.txt`, `examples.jsonl`: optional classifier examples.

Notes: Agent code embeds fallback prompts to avoid blocking IO during requests.

## Data

- `data/raw/analytics/*`: Olist CSV datasets.
- `data/docs`: PDFs/DOCX/TXT for ingestion into `doc_chunks`.
- `data/samples/schema.sql` and `seed.sql`: vector table DDL and sample seeds.

## Scripts (`scripts/*`)

- `ingest_analytics.py`: loads CSVs into Postgres according to schema; supports truncate/analyze.
- `ingest_vectors.py`: builds embeddings and ingests into `doc_chunks` (requires `OPENAI_API_KEY`); runs `ANALYZE`.
- `gen_allowlist.py`: generates `app/routing/allowlist.json` from schema.
- `query_assistant.py`: CLI that talks to LangGraph server (`/graph` threads/runs API). Supports attachment base64 for binaries and text for plaintext.
- `batch_query.py`: batch runner for YAML queries; outputs optional Markdown.

## Operational Tips

- Always run `make ingest-analytics` and `make ingest-vectors` before RAG/analytics queries.
- Regenerate `allowlist.json` when the analytics schema changes.
