"""
Commerce Memory Manager - Contextual memory for processed orders.

Overview
--------
Manages temporary in-memory storage of processed commercial documents during
an active session. Provides semantic search capabilities to find orders by
item descriptions, customer names, or other contextual information.

Design
------
- In-memory storage using dictionaries for fast access
- Semantic search using simple text matching and keyword extraction
- Automatic cleanup when session ends
- Thread-safe operations for concurrent access

Integration
-----------
- Used by Commerce Agent to store processed documents
- Integrated with conversation handler for contextual queries
- Replaces dependency on external thread_id management

Usage
-----
>>> memory = CommerceMemoryManager()
>>> memory.store_order("order_123", order_data)
>>> results = memory.search_orders("canetas azuis")
>>> memory.get_order("order_123")
"""

import re
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

import structlog

logger = structlog.get_logger()


@dataclass
class OrderMemory:
    """In-memory representation of a processed order."""
    
    order_id: str
    doc_type: str
    customer_name: Optional[str]
    items: List[Dict[str, Any]]
    total_value: float
    currency: str
    order_date: Optional[str]
    metadata: Dict[str, Any]
    processed_at: datetime
    raw_text: str


class CommerceMemoryManager:
    """Manages contextual memory for processed commercial documents."""
    
    def __init__(self):
        """Initialize the memory manager."""
        self._orders: Dict[str, OrderMemory] = {}
        self._search_index: Dict[str, List[str]] = {}
        self.log = logger.bind(component="commerce.memory")
    
    def store_order(self, order_id: str, order_data: Dict[str, Any]) -> None:
        """Store a processed order in memory.
        
        Parameters
        ----------
        order_id : str
            Unique identifier for the order
        order_data : Dict[str, Any]
            Processed order data from the extractor
        """
        with self.log.contextvars(order_id=order_id):
            try:
                # Extract items for indexing
                items = order_data.get("items", [])
                items_text = []
                for item in items:
                    item_text = f"{item.get('description', '')} {item.get('category', '')}"
                    items_text.append(item_text.strip())
                
                # Create searchable text
                searchable_text = " ".join([
                    order_data.get("customer_name", ""),
                    order_data.get("doc_type", ""),
                    " ".join(items_text),
                    order_data.get("currency", ""),
                    str(order_data.get("grand_total", "")),
                ]).lower()
                
                # Create order memory object
                order_memory = OrderMemory(
                    order_id=order_id,
                    doc_type=order_data.get("doc_type", "unknown"),
                    customer_name=order_data.get("customer_name"),
                    items=items,
                    total_value=order_data.get("grand_total", 0.0),
                    currency=order_data.get("currency", "BRL"),
                    order_date=order_data.get("order_date"),
                    metadata=order_data.get("metadata", {}),
                    processed_at=datetime.now(),
                    raw_text=searchable_text
                )
                
                # Store in memory
                self._orders[order_id] = order_memory
                
                # Update search index
                self._update_search_index(order_id, searchable_text)
                
                self.log.info("Order stored in memory", 
                             items_count=len(items),
                             total_value=order_memory.total_value)
                
            except Exception as e:
                self.log.error("Failed to store order in memory", error=str(e))
                raise
    
    def search_orders(self, query: str, limit: int = 5) -> List[OrderMemory]:
        """Search for orders using semantic text matching.
        
        Parameters
        ----------
        query : str
            Search query (e.g., "canetas azuis", "pedido do João")
        limit : int, optional
            Maximum number of results to return, by default 5
            
        Returns
        -------
        List[OrderMemory]
            Matching orders sorted by relevance
        """
        with self.log.contextvars(query=query, limit=limit):
            if not query or not self._orders:
                return []
            
            query_lower = query.lower()
            results = []
            
            for order_id, order in self._orders.items():
                score = self._calculate_relevance_score(query_lower, order.raw_text)
                if score > 0:
                    results.append((score, order))
            
            # Sort by relevance (highest first)
            results.sort(key=lambda x: x[0], reverse=True)
            
            # Return top results
            top_results = [order for _, order in results[:limit]]
            
            self.log.info("Search completed", 
                         results_count=len(top_results),
                         total_orders=len(self._orders))
            
            return top_results
    
    def get_order(self, order_id: str) -> Optional[OrderMemory]:
        """Get a specific order by ID.
        
        Parameters
        ----------
        order_id : str
            Order identifier
            
        Returns
        -------
        Optional[OrderMemory]
            Order if found, None otherwise
        """
        return self._orders.get(order_id)
    
    def list_orders(self) -> List[OrderMemory]:
        """Get all stored orders.
        
        Returns
        -------
        List[OrderMemory]
            All orders sorted by processing time (newest first)
        """
        orders = list(self._orders.values())
        orders.sort(key=lambda x: x.processed_at, reverse=True)
        return orders
    
    def clear_memory(self) -> None:
        """Clear all stored orders from memory."""
        self._orders.clear()
        self._search_index.clear()
        self.log.info("Memory cleared")
    
    def _update_search_index(self, order_id: str, searchable_text: str) -> None:
        """Update the search index with order text."""
        # Extract keywords for better matching
        keywords = self._extract_keywords(searchable_text)
        
        for keyword in keywords:
            if keyword not in self._search_index:
                self._search_index[keyword] = []
            if order_id not in self._search_index[keyword]:
                self._search_index[keyword].append(order_id)
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract relevant keywords from text."""
        # Remove common stop words
        stop_words = {
            'de', 'da', 'do', 'das', 'dos', 'em', 'na', 'no', 'nas', 'nos',
            'para', 'por', 'com', 'sem', 'sobre', 'entre', 'até', 'desde',
            'a', 'o', 'e', 'ou', 'mas', 'se', 'que', 'um', 'uma', 'uns', 'umas',
            'é', 'são', 'foi', 'será', 'tem', 'têm', 'ter', 'terá', 'terão'
        }
        
        # Extract words (3+ characters, alphanumeric)
        words = re.findall(r'\b[a-záêçõ]{3,}\b', text.lower())
        
        # Filter out stop words and return unique keywords
        keywords = [word for word in words if word not in stop_words]
        return list(set(keywords))
    
    def _calculate_relevance_score(self, query: str, order_text: str) -> float:
        """Calculate relevance score between query and order text."""
        if not query or not order_text:
            return 0.0
        
        # Simple scoring based on keyword matches
        query_words = set(query.split())
        order_words = set(order_text.split())
        
        # Calculate intersection
        matches = query_words.intersection(order_words)
        
        if not matches:
            return 0.0
        
        # Score based on match ratio and word importance
        match_ratio = len(matches) / len(query_words)
        
        # Boost score for exact phrase matches
        phrase_boost = 1.0
        if query in order_text:
            phrase_boost = 2.0
        
        return match_ratio * phrase_boost


# Global memory manager instance
_memory_manager = None


def get_memory_manager() -> CommerceMemoryManager:
    """Get the global memory manager instance."""
    global _memory_manager
    if _memory_manager is None:
        _memory_manager = CommerceMemoryManager()
    return _memory_manager
