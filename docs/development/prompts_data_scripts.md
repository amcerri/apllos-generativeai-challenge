# Prompts, Data, and Scripts

This document provides comprehensive details about the prompt engineering, data management, and utility scripts that power the Apllos Assistant system.

## Prompt Engineering

The system uses state-of-the-art prompt engineering techniques with Chain-of-Thought reasoning, self-consistency checks, and confidence calibration.

## Prompts (`app/prompts/*`)

### Analytics Prompts

**Planner System Prompt** ([planner_system.txt](../app/prompts/analytics/planner_system.txt)):
- System prompt for SQL planning with allowlist injection at runtime
- Includes Chain-of-Thought reasoning instructions
- Provides context about database schema and constraints
- Emphasizes safety and allowlist compliance

**Planner Examples** ([examples.jsonl](../app/prompts/analytics/examples.jsonl)):
- Few-shot examples for planner LLM path
- Demonstrates proper SQL generation patterns
- Shows allowlist validation and safety checks
- Includes error handling and edge cases

**Normalizer System Prompt** ([normalizer_system.txt](../app/prompts/analytics/normalizer_system.txt)):
- Instructions for converting raw data to PT-BR narratives
- Emphasizes analytical insights and business context
- Includes intelligent data balancing guidelines
- Provides examples of human-like responses

**Normalizer Examples** ([normalizer_examples.jsonl](../app/prompts/analytics/normalizer_examples.jsonl)):
- Examples of data normalization and formatting
- Shows different response styles for various data sizes
- Demonstrates analytical insights and patterns
- Includes confidence calibration examples

### Knowledge Prompts

**System Prompt** ([system.txt](../app/prompts/knowledge/system.txt)):
- Instructions for knowledge agent context and behavior
- Emphasizes citation requirements and accuracy
- Includes cross-validation guidelines
- Provides context about document sources

**Examples** ([examples.jsonl](../app/prompts/knowledge/examples.jsonl)):
- Few-shot examples for knowledge agent
- Demonstrates proper citation formatting
- Shows cross-validation techniques
- Includes confidence scoring examples

### Commerce Prompts

**Extractor System Prompt** ([extractor_system.txt](../app/prompts/commerce/extractor_system.txt)):
- Instructions for structured data extraction
- Emphasizes business context and risk analysis
- Includes self-consistency check guidelines
- Provides examples of extraction patterns

**Extractor Examples** ([examples.jsonl](../app/prompts/commerce/examples.jsonl)):
- Examples of document extraction and parsing
- Shows structured data formatting
- Demonstrates risk flagging and validation
- Includes confidence scoring examples

### Routing Prompts

**System Prompt** ([system.txt](../app/prompts/routing/system.txt)):
- Instructions for routing classification
- Emphasizes context-first routing decisions
- Includes ensemble routing guidelines
- Provides confidence calibration instructions

**Examples** ([examples.jsonl](../app/prompts/routing/examples.jsonl)):
- Optional classifier examples for routing
- Demonstrates different routing scenarios
- Shows confidence scoring patterns
- Includes fallback decision examples

**Note**: Agent code embeds fallback prompts to avoid blocking IO during requests, ensuring system reliability even when prompt files are unavailable.

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

---

**← [Back to Documentation Index](../README.md)**
