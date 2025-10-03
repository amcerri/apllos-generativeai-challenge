"""
Commerce context manager (session-based document storage).

Overview
--------
Manage commerce document context within user sessions to enable follow-up
questions and conversations about uploaded documents. Provides both in-memory
storage (via LangGraph state) and optional persistent storage for longer
sessions.

Design
------
- Input: thread_id and structured commerce document
- Output: context retrieval and storage operations
- Storage: LangGraph state (primary) + optional PostgreSQL (persistent)
- TTL: automatic cleanup of old sessions
- Thread-safe: designed for concurrent access

Integration
-----------
- Used by commerce agent after document extraction
- Integrates with LangGraph checkpointing system
- Optional database persistence for cross-session continuity

Usage
-----
>>> from app.agents.commerce.context import CommerceContextManager
>>> manager = CommerceContextManager()
>>> manager.store_document("thread-123", {"doc": {...}, "items": [...]})
>>> context = manager.get_context("thread-123")
>>> manager.has_context("thread-123")
True
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from typing import Any

try:  # Optional logger
    from app.infra.logging import get_logger
except Exception:  # pragma: no cover - optional
    import logging as _logging

    def get_logger(component: str, **initial_values: Any) -> Any:
        return _logging.getLogger(component)

# Import memory manager
try:
    from app.agents.commerce.memory import get_memory_manager
    _memory_available = True
except Exception:  # pragma: no cover - optional
    _memory_available = False
    get_memory_manager = None


# Tracing (optional; single alias)
start_span: Any
try:
    from app.infra.tracing import start_span as _start_span
    start_span = _start_span
except Exception:  # pragma: no cover - optional
    from contextlib import nullcontext as _nullcontext

    def _fallback_start_span(_name: str, _attrs: dict[str, Any] | None = None):
        return _nullcontext()

    start_span = _fallback_start_span


# Optional database engine
try:
    from app.infra.db import get_engine
    from sqlalchemy import text
    _db_available = True
except Exception:  # pragma: no cover - optional
    _db_available = False
    get_engine = None


__all__ = ["CommerceContextManager"]


# ---------------------------------------------------------------------------
# Commerce Context Manager
# ---------------------------------------------------------------------------
class CommerceContextManager:
    """Manage commerce document context for user sessions."""

    def __init__(self, *, use_db: bool = True, ttl_hours: int = 24) -> None:
        """Initialize context manager.
        
        Parameters
        ----------
        use_db: Whether to use database persistence (requires PostgreSQL)
        ttl_hours: Time-to-live for stored contexts in hours
        """
        self.log = get_logger("agent.commerce.context")
        self.use_db = use_db and _db_available
        self.ttl_hours = ttl_hours
        
        # In-memory cache for active sessions
        self._memory_cache: dict[str, dict[str, Any]] = {}
        
        if self.use_db:
            self._ensure_db_schema()

    def store_document(self, thread_id: str, document: dict[str, Any]) -> None:
        """Store commerce document in session context and memory.
        
        Parameters
        ----------
        thread_id: Unique session/thread identifier
        document: Structured commerce document from extractor
        """
        with start_span("commerce.context.store"):
            if not thread_id or not document:
                self.log.warning("Invalid store request", thread_id=thread_id, has_document=bool(document))
                return
            
            # Prepare context data
            context = {
                "thread_id": thread_id,
                "document": document,
                "stored_at": datetime.now(timezone.utc).isoformat(),
                "expires_at": (datetime.now(timezone.utc) + timedelta(hours=self.ttl_hours)).isoformat(),
                "conversation_count": 0,
                "last_accessed": datetime.now(timezone.utc).isoformat()
            }
            
            # Store in memory cache
            self._memory_cache[thread_id] = context
            
            # Store in database if available
            if self.use_db:
                try:
                    self._store_in_db(context)
                except Exception as e:
                    self.log.warning("Failed to store in database", thread_id=thread_id, error=str(e))
            
            # Store in memory manager for semantic search
            if _memory_available and get_memory_manager:
                try:
                    memory_manager = get_memory_manager()
                    # Generate order ID from thread_id and timestamp
                    order_id = f"order_{thread_id}_{int(datetime.now().timestamp())}"
                    memory_manager.store_order(order_id, document)
                    self.log.info("Document stored in memory manager", order_id=order_id)
                except Exception as e:
                    self.log.warning("Failed to store in memory manager", thread_id=thread_id, error=str(e))
            
            self.log.info(
                "Document stored in context",
                thread_id=thread_id,
                doc_type=document.get("doc", {}).get("doc_type"),
                items_count=len(document.get("items", [])),
                storage_method="memory" + ("+db" if self.use_db else "") + ("+search" if _memory_available else "")
            )

    def get_context(self, thread_id: str) -> dict[str, Any] | None:
        """Retrieve commerce document context for session.
        
        Parameters
        ----------
        thread_id: Unique session/thread identifier
        
        Returns
        -------
        Context dict with document and metadata, or None if not found
        """
        with start_span("commerce.context.get"):
            if not thread_id:
                return None
            
            # Check memory cache first
            context = self._memory_cache.get(thread_id)
            
            # If not in memory, try database
            if not context and self.use_db:
                try:
                    context = self._load_from_db(thread_id)
                    if context:
                        # Cache in memory for faster access
                        self._memory_cache[thread_id] = context
                except Exception as e:
                    self.log.warning("Failed to load from database", thread_id=thread_id, error=str(e))
            
            if not context:
                return None
            
            # Check if expired
            try:
                expires_at = datetime.fromisoformat(context["expires_at"].replace("Z", "+00:00"))
                if datetime.now(timezone.utc) > expires_at:
                    self.log.info("Context expired", thread_id=thread_id)
                    self.clear_context(thread_id)
                    return None
            except Exception as e:
                self.log.warning("Failed to check expiration", thread_id=thread_id, error=str(e))
            
            # Update last accessed
            context["last_accessed"] = datetime.now(timezone.utc).isoformat()
            
            return context

    def has_context(self, thread_id: str) -> bool:
        """Check if context exists for thread.
        
        Parameters
        ----------
        thread_id: Unique session/thread identifier
        
        Returns
        -------
        True if context exists and is not expired
        """
        return self.get_context(thread_id) is not None

    def increment_conversation(self, thread_id: str) -> None:
        """Increment conversation count for analytics.
        
        Parameters
        ----------
        thread_id: Unique session/thread identifier
        """
        context = self.get_context(thread_id)
        if context:
            context["conversation_count"] += 1
            context["last_accessed"] = datetime.now(timezone.utc).isoformat()
            
            # Update in database if available
            if self.use_db:
                try:
                    self._update_conversation_count(thread_id, context["conversation_count"])
                except Exception as e:
                    self.log.warning("Failed to update conversation count", thread_id=thread_id, error=str(e))

    def clear_context(self, thread_id: str) -> None:
        """Clear context for thread.
        
        Parameters
        ----------
        thread_id: Unique session/thread identifier
        """
        with start_span("commerce.context.clear"):
            # Remove from memory
            self._memory_cache.pop(thread_id, None)
            
            # Remove from database
            if self.use_db:
                try:
                    self._delete_from_db(thread_id)
                except Exception as e:
                    self.log.warning("Failed to delete from database", thread_id=thread_id, error=str(e))
            
            self.log.info("Context cleared", thread_id=thread_id)

    def cleanup_expired(self) -> int:
        """Clean up expired contexts.
        
        Returns
        -------
        Number of contexts cleaned up
        """
        with start_span("commerce.context.cleanup"):
            cleaned = 0
            now = datetime.now(timezone.utc)
            
            # Clean memory cache
            expired_threads = []
            for thread_id, context in self._memory_cache.items():
                try:
                    expires_at = datetime.fromisoformat(context["expires_at"].replace("Z", "+00:00"))
                    if now > expires_at:
                        expired_threads.append(thread_id)
                except Exception:
                    expired_threads.append(thread_id)  # Invalid format, remove it
            
            for thread_id in expired_threads:
                self._memory_cache.pop(thread_id, None)
                cleaned += 1
            
            # Clean database
            if self.use_db:
                try:
                    db_cleaned = self._cleanup_db_expired()
                    cleaned += db_cleaned
                except Exception as e:
                    self.log.warning("Failed to cleanup database", error=str(e))
            
            if cleaned > 0:
                self.log.info("Cleaned up expired contexts", count=cleaned)
            
            return cleaned

    def get_stats(self) -> dict[str, Any]:
        """Get context manager statistics.
        
        Returns
        -------
        Dict with statistics about stored contexts
        """
        stats = {
            "memory_contexts": len(self._memory_cache),
            "db_available": self.use_db,
            "ttl_hours": self.ttl_hours
        }
        
        if self.use_db:
            try:
                stats["db_contexts"] = self._count_db_contexts()
            except Exception as e:
                stats["db_error"] = str(e)
        
        return stats

    # Database operations (private methods)
    
    def _ensure_db_schema(self) -> None:
        """Ensure database schema exists."""
        if not self.use_db:
            return
        
        try:
            engine = get_engine()
            with engine.begin() as conn:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS commerce_sessions (
                        thread_id VARCHAR(255) PRIMARY KEY,
                        document_data JSONB NOT NULL,
                        stored_at TIMESTAMP WITH TIME ZONE NOT NULL,
                        expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
                        conversation_count INTEGER DEFAULT 0,
                        last_accessed TIMESTAMP WITH TIME ZONE NOT NULL
                    )
                """))
                
                # Create index for cleanup
                conn.execute(text("""
                    CREATE INDEX IF NOT EXISTS idx_commerce_sessions_expires_at 
                    ON commerce_sessions(expires_at)
                """))
                
        except Exception as e:
            self.log.warning("Failed to ensure database schema", error=str(e))
            self.use_db = False  # Disable DB if schema creation fails

    def _store_in_db(self, context: dict[str, Any]) -> None:
        """Store context in database."""
        engine = get_engine()
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO commerce_sessions 
                (thread_id, document_data, stored_at, expires_at, conversation_count, last_accessed)
                VALUES (:thread_id, :document_data, :stored_at, :expires_at, :conversation_count, :last_accessed)
                ON CONFLICT (thread_id) DO UPDATE SET
                    document_data = EXCLUDED.document_data,
                    stored_at = EXCLUDED.stored_at,
                    expires_at = EXCLUDED.expires_at,
                    conversation_count = EXCLUDED.conversation_count,
                    last_accessed = EXCLUDED.last_accessed
            """), {
                "thread_id": context["thread_id"],
                "document_data": json.dumps(context),
                "stored_at": context["stored_at"],
                "expires_at": context["expires_at"],
                "conversation_count": context["conversation_count"],
                "last_accessed": context["last_accessed"]
            })

    def _load_from_db(self, thread_id: str) -> dict[str, Any] | None:
        """Load context from database."""
        engine = get_engine()
        with engine.begin() as conn:
            result = conn.execute(text("""
                SELECT document_data FROM commerce_sessions 
                WHERE thread_id = :thread_id AND expires_at > NOW()
            """), {"thread_id": thread_id})
            
            row = result.fetchone()
            if row:
                return json.loads(row[0])
            return None

    def _update_conversation_count(self, thread_id: str, count: int) -> None:
        """Update conversation count in database."""
        engine = get_engine()
        with engine.begin() as conn:
            conn.execute(text("""
                UPDATE commerce_sessions 
                SET conversation_count = :count, last_accessed = NOW()
                WHERE thread_id = :thread_id
            """), {"thread_id": thread_id, "count": count})

    def _delete_from_db(self, thread_id: str) -> None:
        """Delete context from database."""
        engine = get_engine()
        with engine.begin() as conn:
            conn.execute(text("""
                DELETE FROM commerce_sessions WHERE thread_id = :thread_id
            """), {"thread_id": thread_id})

    def _cleanup_db_expired(self) -> int:
        """Clean up expired contexts from database."""
        engine = get_engine()
        with engine.begin() as conn:
            result = conn.execute(text("""
                DELETE FROM commerce_sessions WHERE expires_at <= NOW()
            """))
            return result.rowcount or 0

    def _count_db_contexts(self) -> int:
        """Count active contexts in database."""
        engine = get_engine()
        with engine.begin() as conn:
            result = conn.execute(text("""
                SELECT COUNT(*) FROM commerce_sessions WHERE expires_at > NOW()
            """))
            return result.scalar() or 0
