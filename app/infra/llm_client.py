"""
Centralized LLM client with timeout, retries, and consistent JSON extraction.

Overview
--------
Shared LLM client for all agents with standardized configuration, timeout handling,
retry logic, and JSON response parsing. Uses native Python stdlib for retries
and timeout management, with OpenAI as the primary backend.

Design
------
- Single client factory with `functools.lru_cache` for deterministic initialization.
- Configurable timeout, retries, and model parameters via Settings.
- Consistent JSON extraction with fallback parsing strategies.
- Structured logging for debugging and monitoring.

Integration
-----------
- Used by all agents requiring LLM functionality (analytics, knowledge, commerce, routing).
- Configuration via `app.config.settings.LLMConfig`.
- Fallback to no-op when OpenAI is unavailable.

Usage
-----
>>> from app.infra.llm_client import get_llm_client
>>> client = get_llm_client()
>>> response = client.chat_completion(
...     messages=[{"role": "user", "content": "Hello"}],
...     model="gpt-4o-mini",
...     temperature=0.1
... )
>>> response.text
"Hello! How can I help you today?"
"""

from __future__ import annotations

import functools
import json
import logging
import os
import re
import time
from typing import Any, Mapping

# Load .env early to ensure OPENAI_API_KEY is visible even if singleton initializes first
try:  # pragma: no cover - optional dependency
    from dotenv import load_dotenv as _load_dotenv
    _load_dotenv()
except Exception:
    pass

# Prefer centralized logger adapter (accepts structured extras)
try:  # pragma: no cover - optional
    from app.infra.logging import get_logger as _get_logger
    _log = _get_logger(__name__)
except Exception:  # fallback to stdlib logger
    _log = logging.getLogger(__name__)

# Optional OpenAI client
_OpenAI: Any | None = None
try:  # pragma: no cover - exercised only when openai is installed
    from openai import OpenAI as _imported_OpenAI
except Exception:  # pragma: no cover - keep optional
    _imported_OpenAI = None
_OpenAI = _imported_OpenAI

__all__ = [
    "get_llm_client",
    "LLMResponse",
    "LLMClient",
]


class LLMResponse:
    """Structured response from LLM client."""

    def __init__(
        self,
        text: str,
        model: str,
        usage: dict[str, int] | None = None,
        finish_reason: str | None = None,
        raw_response: Any = None,
    ) -> None:
        """Initialize LLM response.

        Parameters
        ----------
        text:
            The generated text content.
        model:
            The model used for generation.
        usage:
            Token usage information (prompt_tokens, completion_tokens, total_tokens).
        finish_reason:
            Reason for completion (stop, length, content_filter, etc.).
        raw_response:
            The raw response object from the LLM provider.
        """
        self.text = text
        self.model = model
        self.usage = usage or {}
        self.finish_reason = finish_reason
        self.raw_response = raw_response

    def __repr__(self) -> str:
        return f"LLMResponse(text={self.text[:50]}..., model={self.model})"


class LLMClient:
    """Centralized LLM client with timeout, retries, and JSON extraction."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "gpt-4o-mini",
        timeout: float = 60.0,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ) -> None:
        """Initialize LLM client.

        Parameters
        ----------
        api_key:
            OpenAI API key. Defaults to OPENAI_API_KEY environment variable.
        model:
            Default model to use for completions.
        timeout:
            Request timeout in seconds.
        max_retries:
            Maximum number of retry attempts.
        retry_delay:
            Delay between retries in seconds.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.log = _log

        if not self.api_key:
            self.log.warning("No OpenAI API key provided; client will use no-op mode")
            self._client = None
        elif _OpenAI is None:
            self.log.warning("OpenAI package not available; client will use no-op mode")
            self._client = None
        else:
            try:
                self._client = _OpenAI(api_key=self.api_key, timeout=self.timeout)
                self.log.info("LLM client initialized", model=model, timeout=timeout)
            except Exception as exc:
                self.log.error("Failed to initialize OpenAI client", error=str(exc))
                self._client = None

    def chat_completion(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        temperature: float = 0.1,
        max_tokens: int | None = None,
        response_format: dict[str, Any] | None = None,
        *,
        max_retries: int | None = None,
    ) -> LLMResponse | None:
        """Generate chat completion with retry logic.

        Parameters
        ----------
        messages:
            List of message dictionaries with 'role' and 'content' keys.
        model:
            Model to use. Defaults to client's default model.
        temperature:
            Sampling temperature (0.0 to 2.0).
        max_tokens:
            Maximum tokens to generate.
        response_format:
            Response format configuration (e.g., JSON schema).

        Returns
        -------
        LLMResponse | None
            Structured response or None if all retries failed.
        """
        if self._client is None:
            self.log.warning("LLM client not available; returning None")
            return None

        model = model or self.model
        last_exception = None
        retries = self.max_retries if max_retries is None else max(0, int(max_retries))

        for attempt in range(retries + 1):
            try:
                self.log.debug(
                    "LLM request attempt",
                    attempt=attempt + 1,
                    model=model,
                    messages_count=len(messages),
                )

                response = self._client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    response_format=response_format,
                )

                # Extract response data
                choice = response.choices[0]
                text = choice.message.content or ""
                usage = {
                    "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                    "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                    "total_tokens": response.usage.total_tokens if response.usage else 0,
                }

                self.log.debug(
                    "LLM response received",
                    model=model,
                    text_length=len(text),
                    usage=usage,
                )

                return LLMResponse(
                    text=text,
                    model=model,
                    usage=usage,
                    finish_reason=choice.finish_reason,
                    raw_response=response,
                )

            except Exception as exc:
                last_exception = exc
                self.log.warning(
                    "LLM request failed",
                    attempt=attempt + 1,
                    error=str(exc),
                    error_type=type(exc).__name__,
                )

                if attempt < retries:
                    delay = self.retry_delay * (2 ** attempt)  # Exponential backoff
                    self.log.info("Retrying LLM request", delay=delay)
                    time.sleep(delay)
                else:
                    self.log.error("All LLM retry attempts failed", error=str(exc))

        return None

    def extract_json(
        self,
        text: str,
        schema: dict[str, Any] | None = None,
        fallback_parsing: bool = True,
    ) -> dict[str, Any] | None:
        """Extract JSON from LLM response with fallback parsing strategies.

        Parameters
        ----------
        text:
            Text response from LLM that should contain JSON.
        schema:
            Optional JSON schema for validation.
        fallback_parsing:
            Whether to use regex-based fallback parsing if JSON parsing fails.

        Returns
        -------
        dict[str, Any] | None
            Parsed JSON object or None if parsing failed.
        """
        if not text:
            self.log.warning("Empty text provided for JSON extraction")
            return None

        # Try direct JSON parsing first
        try:
            result = json.loads(text)
            self.log.debug("JSON extracted successfully", keys=list(result.keys()) if isinstance(result, dict) else None)
            return result
        except json.JSONDecodeError as e:
            self.log.debug("Direct JSON parsing failed", error=str(e))

        if not fallback_parsing:
            return None

        # Fallback: extract JSON using regex
        try:
            # Look for JSON object in the text
            json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
            matches = re.findall(json_pattern, text, re.DOTALL)
            
            for match in matches:
                try:
                    result = json.loads(match)
                    self.log.debug("JSON extracted via regex fallback", keys=list(result.keys()) if isinstance(result, dict) else None)
                    return result
                except json.JSONDecodeError:
                    continue

            # Try to find JSON array
            array_pattern = r'\[[^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*\]'
            array_matches = re.findall(array_pattern, text, re.DOTALL)
            
            for match in array_matches:
                try:
                    result = json.loads(match)
                    self.log.debug("JSON array extracted via regex fallback")
                    return {"data": result}  # Wrap array in object
                except json.JSONDecodeError:
                    continue

        except Exception as exc:
            self.log.warning("Fallback JSON parsing failed", error=str(exc))

        self.log.warning("All JSON extraction methods failed", text_preview=text[:100])
        return None

    def is_available(self) -> bool:
        """Check if LLM client is available and configured.

        Returns
        -------
        bool
            True if client is available, False otherwise.
        """
        return self._client is not None and self.api_key is not None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


# Global singleton instance
_LLM_CLIENT: LLMClient | None = None


def get_llm_client() -> LLMClient:
    """Get a configured LLM client (singleton).

    This function creates and caches a single LLM client instance
    for the lifetime of the application.

    Returns
    -------
    LLMClient
        Configured LLM client instance.
    """
    global _LLM_CLIENT
    
    # Rebuild client when missing or unavailable (e.g., .env loaded after first call)
    if _LLM_CLIENT is None or not _LLM_CLIENT.is_available():
        # Reload .env just in case runtime loaded it later
        try:
            from dotenv import load_dotenv as _reload_dotenv  # type: ignore
            _reload_dotenv()
        except Exception:
            pass

        api_key = os.getenv("OPENAI_API_KEY")
        model = "gpt-4o-mini"
        timeout = 60.0
        max_retries = 3

        _LLM_CLIENT = LLMClient(
            api_key=api_key,
            model=model,
            timeout=timeout,
            max_retries=max_retries,
        )
    
    return _LLM_CLIENT
