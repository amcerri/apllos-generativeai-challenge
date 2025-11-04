"""
LangGraph Server HTTP client.

This module provides an async client for interacting with the LangGraph Server
API endpoints.

Design
------
- Async HTTP client using httpx
- Thread management for conversation context
- Run creation and polling for async operations
- Error handling and retry logic

Usage
-----
>>> client = LangGraphClient(base_url="http://localhost:2024")
>>> thread_id = await client.create_thread()
>>> run_id = await client.create_run(thread_id, {"query": "Hello"})
>>> result = await client.poll_for_answer(thread_id, run_id)
"""

from __future__ import annotations

import asyncio
import json
from typing import Any, Callable

import httpx


class LangGraphClient:
    """Async HTTP client for LangGraph Server API."""

    def __init__(
        self,
        base_url: str = "http://localhost:2024",
        timeout: float = 300.0,
    ) -> None:
        """Initialize LangGraph client.

        Parameters
        ----------
        base_url: str
            Base URL of the LangGraph Server
        timeout: float
            HTTP request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client = httpx.AsyncClient(timeout=timeout)

    async def create_thread(self) -> str:
        """Create a new conversation thread.

        Returns
        -------
        str
            Thread ID
        """
        response = await self._client.post(f"{self.base_url}/threads", json={})
        response.raise_for_status()
        data = response.json()
        return data["thread_id"]

    async def create_run(
        self, thread_id: str, input_data: dict[str, Any]
    ) -> str:
        """Create a new run for a thread.

        Parameters
        ----------
        thread_id: str
            Thread ID
        input_data: dict
            Input data for the run

        Returns
        -------
        str
            Run ID
        """
        run_data = {
            "assistant_id": "assistant",
            "input": input_data,
        }
        
        response = await self._client.post(
            f"{self.base_url}/threads/{thread_id}/runs",
            json=run_data,
        )
        response.raise_for_status()
        run_response = response.json()
        return run_response.get("run_id", "")

    async def get_thread_state(self, thread_id: str) -> dict[str, Any]:
        """Get current state of a thread.

        Parameters
        ----------
        thread_id: str
            Thread ID

        Returns
        -------
        dict
            Thread state
        """
        response = await self._client.get(
            f"{self.base_url}/threads/{thread_id}/state"
        )
        response.raise_for_status()
        return response.json()

    async def get_run_status(
        self, thread_id: str, run_id: str
    ) -> dict[str, Any] | None:
        """Get status of a run.

        Parameters
        ----------
        thread_id: str
            Thread ID
        run_id: str
            Run ID

        Returns
        -------
        dict | None
            Run status or None if endpoint not available
        """
        try:
            response = await self._client.get(
                f"{self.base_url}/threads/{thread_id}/runs/{run_id}"
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError:
            # Endpoint might not be available
            return None

    async def poll_for_answer(
        self,
        thread_id: str,
        run_id: str,
        polling_interval: float = 1.0,
        polling_timeout: int = 300,
        progress_callback: Callable[[str], Any] | None = None,
    ) -> dict[str, Any]:
        """Poll for answer completion.

        Parameters
        ----------
        thread_id: str
            Thread ID
        run_id: str
            Run ID
        polling_interval: float
            Interval between polling attempts in seconds
        polling_timeout: int
            Maximum time to poll in seconds
        progress_callback: Callable | None
            Optional callback for progress updates

        Returns
        -------
        dict
            Answer data with keys: text, citations, meta, followups
        """
        # Get previous answer to detect changes
        previous_state = await self.get_thread_state(thread_id)
        previous_answer = previous_state.get("values", {}).get("answer")
        previous_answer_json = json.dumps(previous_answer, sort_keys=True) if previous_answer else None
        
        max_attempts = polling_timeout // int(polling_interval)
        answer_updated = False
        
        for attempt in range(max_attempts):
            # Check run status first (faster check)
            run_status = await self.get_run_status(thread_id, run_id)
            
            # Check run status for completion or errors first
            if run_status:
                status = run_status.get("status", "").lower()
                if status in ("failed", "error", "cancelled"):
                    return {
                        "error": f"Run {status}",
                        "text": "Erro ao processar requisição.",
                    }
                elif status in ("success", "completed", "end"):
                    # Run completed - get final state
                    state = await self.get_thread_state(thread_id)
                    values = state.get("values", {})
                    current_answer = values.get("answer")
                    if current_answer:
                        answer_updated = True
                        break
            
            # Get current state
            state = await self.get_thread_state(thread_id)
            values = state.get("values", {})
            current_answer = values.get("answer")
            
            # Check if answer updated (compare JSON serialized versions)
            if current_answer:
                current_answer_json = json.dumps(current_answer, sort_keys=True)
                if previous_answer_json is None:
                    # First answer received
                    answer_updated = True
                    break
                elif current_answer_json != previous_answer_json:
                    # Answer changed
                    answer_updated = True
                    break
            
            # Progress callback
            if progress_callback:
                agent = values.get("agent", "N/A")
                elapsed = (attempt + 1) * polling_interval
                # Call async callback if it's a coroutine function
                message = f"Agente: {agent} | Tempo: {elapsed:.1f}s"
                if asyncio.iscoroutinefunction(progress_callback):
                    await progress_callback(message)
                else:
                    progress_callback(message)
            
            await asyncio.sleep(polling_interval)
        else:
            return {
                "error": "Timeout",
                "text": "A requisição demorou muito para processar.",
            }
        
        if not answer_updated:
            return {
                "error": "No answer",
                "text": "Nenhuma resposta recebida.",
            }
        
        # Get final state
        state = await self.get_thread_state(thread_id)
        values = state.get("values", {})
        answer = values.get("answer")
        
        # Extract answer components
        if isinstance(answer, dict):
            text = answer.get("text", "")
            citations = answer.get("citations", [])
            meta = answer.get("meta", {})
            followups = answer.get("followups", [])
        elif answer is not None:
            # If answer is a string or other type, convert to dict format
            text = str(answer)
            citations = []
            meta = {}
            followups = []
        else:
            # No answer found
            text = "Nenhuma resposta disponível."
            citations = []
            meta = {}
            followups = []
        
        # Merge meta with additional info from state if available
        if not isinstance(meta, dict):
            meta = {}
        agent = values.get("agent")
        if agent:
            meta["agent"] = agent
        router_decision = values.get("router_decision", {})
        if router_decision:
            if "confidence" in router_decision:
                meta["confidence"] = router_decision["confidence"]
            if "reason" in router_decision:
                meta["reason"] = router_decision["reason"]
        
        return {
            "text": text,
            "citations": citations,
            "meta": meta,
            "followups": followups,
        }

    async def close(self) -> None:
        """Close HTTP client."""
        await self._client.aclose()

    async def __aenter__(self) -> "LangGraphClient":
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.close()

