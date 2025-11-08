"""
Centralized caching system for routing, embeddings, and responses.

Overview
  Provides semantic caching for routing decisions, embeddings, and agent responses
  to improve performance and reduce LLM API calls. Uses query normalization and
  semantic hashing to identify similar queries and cache their results.

Design
  - In-memory cache with TTL-based expiration
  - Semantic key generation using normalized text
  - Thread-safe operations for concurrent access
  - Graceful degradation when cache is unavailable
  - Separate cache classes for different use cases (routing, embeddings, responses)

Integration
  - RoutingCache: Used by LLMClassifier to cache routing decisions
  - EmbeddingCache: Used by knowledge retriever to cache embeddings
  - ResponseCache: Used by agents to cache responses for similar queries

Usage
  >>> from app.infra.cache import RoutingCache, EmbeddingCache, ResponseCache
  >>> routing_cache = RoutingCache(ttl_seconds=3600)
  >>> embedding_cache = EmbeddingCache(ttl_seconds=86400)
  >>> response_cache = ResponseCache(ttl_seconds=3600)
"""

from __future__ import annotations

import hashlib
import json
import time
from collections.abc import Iterable, Mapping, Sequence
from threading import Lock
from typing import Any

try:
    from app.infra.logging import get_logger
except Exception:
    import logging as _logging

    def get_logger(component: str, **initial_values: Any) -> Any:
        return _logging.getLogger(component)


__all__ = ["RoutingCache", "EmbeddingCache", "ResponseCache"]


class RoutingCache:
    """Semantic cache for routing decisions.

    Caches routing decisions based on normalized query text and allowlist
    configuration. Uses TTL-based expiration to ensure cached decisions
    remain relevant.

    Parameters
    ----------
    ttl_seconds:
        Time-to-live for cached entries in seconds. Defaults to 3600 (1 hour).
    max_size:
        Maximum number of entries in cache. When exceeded, oldest entries
        are evicted. Defaults to 1000.
    """

    def __init__(self, ttl_seconds: int = 3600, max_size: int = 1000) -> None:
        self.log = get_logger(__name__)
        self.ttl = float(ttl_seconds)
        self.max_size = max(max_size, 1)
        self._cache: dict[str, tuple[Any, float]] = {}
        self._lock = Lock()

    def _query_key(self, query: str, allowlist_hash: str) -> str:
        """Generate semantic cache key from normalized query and allowlist.

        Normalizes query by lowercasing, removing extra whitespace, and
        removing punctuation. Combines with allowlist hash to create
        unique key for similar queries with same allowlist.

        Parameters
        ----------
        query:
            User query text to normalize.
        allowlist_hash:
            Hash of allowlist configuration.

        Returns
        -------
        str
            Cache key for the query-allowlist combination.
        """
        normalized = " ".join(query.lower().split())
        combined = f"{normalized}:{allowlist_hash}"
        return hashlib.sha256(combined.encode("utf-8")).hexdigest()[:16]

    def _allowlist_hash(self, allowlist: Mapping[str, Iterable[str]]) -> str:
        """Generate hash for allowlist configuration.

        Creates deterministic hash from allowlist structure to identify
        when allowlist changes and invalidate related cache entries.

        Parameters
        ----------
        allowlist:
            Allowlist mapping of tables to columns.

        Returns
        -------
        str
            MD5 hash of normalized allowlist JSON.
        """
        normalized: dict[str, list[str]] = {}
        for table, cols in allowlist.items():
            table_key = str(table).strip()
            if table_key:
                normalized[table_key] = sorted({str(c).strip() for c in cols if str(c).strip()})

        json_str = json.dumps(normalized, sort_keys=True, ensure_ascii=False)
        return hashlib.md5(json_str.encode("utf-8")).hexdigest()

    def get(
        self, query: str, allowlist: Mapping[str, Iterable[str]] | None = None
    ) -> dict[str, Any] | None:
        """Retrieve cached routing decision if available and not expired.

        Parameters
        ----------
        query:
            User query text.
        allowlist:
            Optional allowlist configuration. If None, uses empty dict.

        Returns
        -------
        dict[str, Any] | None
            Cached routing decision or None if not found or expired.
        """
        if not query or not query.strip():
            return None

        allowlist = allowlist or {}
        allowlist_hash = self._allowlist_hash(allowlist)
        key = self._query_key(query, allowlist_hash)

        with self._lock:
            if key in self._cache:
                decision, timestamp = self._cache[key]
                age = time.time() - timestamp
                if age < self.ttl:
                    self.log.debug("Cache hit", extra={"key": key, "age_seconds": age})
                    return decision
                del self._cache[key]

        return None

    def set(
        self,
        query: str,
        allowlist: Mapping[str, Iterable[str]] | None,
        decision: dict[str, Any],
    ) -> None:
        """Store routing decision in cache.

        Parameters
        ----------
        query:
            User query text.
        allowlist:
            Optional allowlist configuration. If None, uses empty dict.
        decision:
            Routing decision dictionary to cache.
        """
        if not query or not query.strip():
            return

        allowlist = allowlist or {}
        allowlist_hash = self._allowlist_hash(allowlist)
        key = self._query_key(query, allowlist_hash)

        with self._lock:
            if len(self._cache) >= self.max_size:
                self._evict_oldest()

            self._cache[key] = (decision, time.time())
            self.log.debug("Cache set", extra={"key": key, "cache_size": len(self._cache)})

    def _evict_oldest(self) -> None:
        """Evict oldest cache entry when cache is full.

        Removes entry with oldest timestamp to make room for new entries.
        """
        if not self._cache:
            return

        oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k][1])
        del self._cache[oldest_key]
        self.log.debug("Cache evicted", extra={"key": oldest_key})

    def clear(self) -> None:
        """Clear all cached entries."""
        with self._lock:
            size = len(self._cache)
            self._cache.clear()
            self.log.info("Cache cleared", extra={"entries_cleared": size})

    def stats(self) -> dict[str, Any]:
        """Get cache statistics.

        Returns
        -------
        dict[str, Any]
            Dictionary with cache size, TTL, and max size.
        """
        with self._lock:
            return {
                "size": len(self._cache),
                "max_size": self.max_size,
                "ttl_seconds": self.ttl,
            }


class EmbeddingCache:
    """Semantic cache for text embeddings.

    Caches embedding vectors for text queries to avoid redundant API calls
    when the same or similar queries are processed. Uses normalized text
    hashing to identify similar queries.

    Parameters
    ----------
    ttl_seconds:
        Time-to-live for cached entries in seconds. Defaults to 86400 (24 hours).
    max_size:
        Maximum number of entries in cache. When exceeded, oldest entries
        are evicted. Defaults to 5000.
    """

    def __init__(self, ttl_seconds: int = 86400, max_size: int = 5000) -> None:
        self.log = get_logger(__name__)
        self.ttl = float(ttl_seconds)
        self.max_size = max(max_size, 1)
        self._cache: dict[str, tuple[list[float], float]] = {}
        self._lock = Lock()

    def _text_key(self, text: str, model: str) -> str:
        """Generate semantic cache key from normalized text and model.

        Normalizes text by lowercasing and removing extra whitespace.
        Combines with model name to create unique key.

        Parameters
        ----------
        text:
            Text to normalize.
        model:
            Embedding model identifier.

        Returns
        -------
        str
            Cache key for the text-model combination.
        """
        normalized = " ".join(text.lower().split())
        combined = f"{normalized}:{model}"
        return hashlib.sha256(combined.encode("utf-8")).hexdigest()[:16]

    def get(self, text: str, model: str) -> list[float] | None:
        """Retrieve cached embedding if available and not expired.

        Parameters
        ----------
        text:
            Text query.
        model:
            Embedding model identifier.

        Returns
        -------
        list[float] | None
            Cached embedding vector or None if not found or expired.
        """
        if not text or not text.strip():
            return None

        key = self._text_key(text, model)

        with self._lock:
            if key in self._cache:
                embedding, timestamp = self._cache[key]
                age = time.time() - timestamp
                if age < self.ttl:
                    self.log.debug("Embedding cache hit", extra={"key": key, "age_seconds": age})
                    return embedding.copy()
                del self._cache[key]

        return None

    def set(self, text: str, model: str, embedding: Sequence[float]) -> None:
        """Store embedding in cache.

        Parameters
        ----------
        text:
            Text query.
        model:
            Embedding model identifier.
        embedding:
            Embedding vector to cache.
        """
        if not text or not text.strip():
            return

        key = self._text_key(text, model)
        embedding_list = list(embedding)

        with self._lock:
            if len(self._cache) >= self.max_size:
                self._evict_oldest()

            self._cache[key] = (embedding_list, time.time())
            self.log.debug("Embedding cache set", extra={"key": key, "cache_size": len(self._cache)})

    def _evict_oldest(self) -> None:
        """Evict oldest cache entry when cache is full."""
        if not self._cache:
            return

        oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k][1])
        del self._cache[oldest_key]
        self.log.debug("Embedding cache evicted", extra={"key": oldest_key})

    def clear(self) -> None:
        """Clear all cached entries."""
        with self._lock:
            size = len(self._cache)
            self._cache.clear()
            self.log.info("Embedding cache cleared", extra={"entries_cleared": size})

    def stats(self) -> dict[str, Any]:
        """Get cache statistics.

        Returns
        -------
        dict[str, Any]
            Dictionary with cache size, TTL, and max size.
        """
        with self._lock:
            return {
                "size": len(self._cache),
                "max_size": self.max_size,
                "ttl_seconds": self.ttl,
            }


class ResponseCache:
    """Semantic cache for agent responses.

    Caches agent responses for similar queries to avoid redundant processing
    and LLM calls. Uses normalized query text to identify similar queries.

    Parameters
    ----------
    ttl_seconds:
        Time-to-live for cached entries in seconds. Defaults to 3600 (1 hour).
    max_size:
        Maximum number of entries in cache. When exceeded, oldest entries
        are evicted. Defaults to 1000.
    """

    def __init__(self, ttl_seconds: int = 3600, max_size: int = 1000) -> None:
        self.log = get_logger(__name__)
        self.ttl = float(ttl_seconds)
        self.max_size = max(max_size, 1)
        self._cache: dict[str, tuple[dict[str, Any], float]] = {}
        self._lock = Lock()

    def _query_key(self, query: str, agent: str, context_hash: str | None = None) -> str:
        """Generate semantic cache key from normalized query, agent, and context.

        Normalizes query by lowercasing and removing extra whitespace.
        Combines with agent name and optional context hash.

        Parameters
        ----------
        query:
            User query text.
        agent:
            Agent identifier (e.g., "analytics", "knowledge").
        context_hash:
            Optional hash of context (e.g., allowlist, filters).

        Returns
        -------
        str
            Cache key for the query-agent-context combination.
        """
        normalized = " ".join(query.lower().split())
        combined = f"{normalized}:{agent}"
        if context_hash:
            combined = f"{combined}:{context_hash}"
        return hashlib.sha256(combined.encode("utf-8")).hexdigest()[:16]

    def get(
        self,
        query: str,
        agent: str,
        context: Mapping[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Retrieve cached response if available and not expired.

        Parameters
        ----------
        query:
            User query text.
        agent:
            Agent identifier.
        context:
            Optional context dictionary (e.g., allowlist, filters).

        Returns
        -------
        dict[str, Any] | None
            Cached response or None if not found or expired.
        """
        if not query or not query.strip():
            return None

        context_hash = None
        if context:
            normalized_ctx: dict[str, Any] = {}
            for k, v in context.items():
                if isinstance(v, (list, tuple)):
                    normalized_ctx[k] = sorted(str(x) for x in v)
                else:
                    normalized_ctx[k] = str(v)
            json_str = json.dumps(normalized_ctx, sort_keys=True, ensure_ascii=False)
            context_hash = hashlib.md5(json_str.encode("utf-8")).hexdigest()

        key = self._query_key(query, agent, context_hash)

        with self._lock:
            if key in self._cache:
                response, timestamp = self._cache[key]
                age = time.time() - timestamp
                if age < self.ttl:
                    self.log.debug("Response cache hit", extra={"key": key, "age_seconds": age, "agent": agent})
                    return response.copy()
                del self._cache[key]

        return None

    def set(
        self,
        query: str,
        agent: str,
        response: dict[str, Any],
        context: Mapping[str, Any] | None = None,
    ) -> None:
        """Store response in cache.

        Parameters
        ----------
        query:
            User query text.
        agent:
            Agent identifier.
        response:
            Response dictionary to cache.
        context:
            Optional context dictionary (e.g., allowlist, filters).
        """
        if not query or not query.strip():
            return

        context_hash = None
        if context:
            normalized_ctx: dict[str, Any] = {}
            for k, v in context.items():
                if isinstance(v, (list, tuple)):
                    normalized_ctx[k] = sorted(str(x) for x in v)
                else:
                    normalized_ctx[k] = str(v)
            json_str = json.dumps(normalized_ctx, sort_keys=True, ensure_ascii=False)
            context_hash = hashlib.md5(json_str.encode("utf-8")).hexdigest()

        key = self._query_key(query, agent, context_hash)

        with self._lock:
            if len(self._cache) >= self.max_size:
                self._evict_oldest()

            self._cache[key] = (response.copy(), time.time())
            self.log.debug("Response cache set", extra={"key": key, "cache_size": len(self._cache), "agent": agent})

    def _evict_oldest(self) -> None:
        """Evict oldest cache entry when cache is full."""
        if not self._cache:
            return

        oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k][1])
        del self._cache[oldest_key]
        self.log.debug("Response cache evicted", extra={"key": oldest_key})

    def clear(self) -> None:
        """Clear all cached entries."""
        with self._lock:
            size = len(self._cache)
            self._cache.clear()
            self.log.info("Response cache cleared", extra={"entries_cleared": size})

    def stats(self) -> dict[str, Any]:
        """Get cache statistics.

        Returns
        -------
        dict[str, Any]
            Dictionary with cache size, TTL, and max size.
        """
        with self._lock:
            return {
                "size": len(self._cache),
                "max_size": self.max_size,
                "ttl_seconds": self.ttl,
            }

