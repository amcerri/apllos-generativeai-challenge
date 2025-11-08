# Knowledge Agent (RAG)

Covers retriever, ranker, and answerer.

## Retriever ([app/agents/knowledge/retriever.py](../../app/agents/knowledge/retriever.py))

- Embeddings: OpenAI or deterministic hash fallback; `text-embedding-3-small` by default.
- Caching: Embedding cache stores generated embeddings for text queries to reduce redundant API calls.
  - Cache key includes normalized text and model name.
  - TTL: 24 hours (configurable).
  - Significantly reduces latency and costs for repeated or similar queries.
- Storage: pgvector table `doc_chunks` with IVFFLAT cosine index; similarity computed as `1 - (embedding <=> :qvec)`.
- Filters: `doc_id`, `source`, `title` (ILIKE), `mime`, `tag`, JSONB containment, `min_length`, `doc_type`.
- Deduplication: keep best `doc_id` hit; return top_k above min_score.

## Ranker ([app/agents/knowledge/ranker.py](../../app/agents/knowledge/ranker.py))

- Heuristic reranker with signals: title overlap, body coverage, exact phrase boost; penalties for very short/long chunks.
- Optional LLM reranker controlled by settings flag.

## Answerer ([app/agents/knowledge/answerer.py](../../app/agents/knowledge/answerer.py))

- Produces PT-BR answer with mandatory citations and cross-validation.
- Prompt engineering with Chain-of-Thought reasoning and confidence calibration.
- Attempts LLM composition with compact context; compresses if above char cap; fallback to extractive bullets.
- Caching: Response cache stores generated answers for similar queries with same document hits.
  - Cache key includes query, agent name, and context hash (top hits and character cap).
  - TTL: 1 hour (configurable).
  - Reduces redundant LLM calls for repeated or similar knowledge queries.
- Cross-validation: forces `no_context=true` when relevance is low or no relevant hits for conceptual questions.
- Always returns `citations` referencing either public `url` or `doc_id`.

---

**← [Back to Documentation Index](../README.md)**