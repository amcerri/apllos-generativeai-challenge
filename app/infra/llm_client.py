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
                self.log.info("LLM client initialized", extra={"model": model, "timeout": timeout})
            except Exception as exc:
                self.log.error("Failed to initialize OpenAI client", extra={"error": str(exc)})
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
                    extra={"attempt": attempt + 1, "model": model, "messages_count": len(messages)},
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
                # Normalize usage to a plain dict
                if response.usage is None:
                    usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
                else:
                    try:
                        usage = {
                            "prompt_tokens": int(getattr(response.usage, "prompt_tokens", 0) or 0),
                            "completion_tokens": int(getattr(response.usage, "completion_tokens", 0) or 0),
                            "total_tokens": int(getattr(response.usage, "total_tokens", 0) or 0),
                        }
                    except Exception:
                        try:
                            # If it's already a mapping
                            u = dict(response.usage)
                            usage = {
                                "prompt_tokens": int(u.get("prompt_tokens", 0) or 0),
                                "completion_tokens": int(u.get("completion_tokens", 0) or 0),
                                "total_tokens": int(u.get("total_tokens", 0) or 0),
                            }
                        except Exception:
                            usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

                self.log.debug(
                    "LLM response received",
                    extra={"model": model, "text_length": len(text), "usage": usage},
                )

                # Track cost
                self._track_cost(model, usage)

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
                    extra={"attempt": attempt + 1, "error": str(exc), "error_type": type(exc).__name__},
                )

                if attempt < retries:
                    delay = self.retry_delay * (2 ** attempt)  # Exponential backoff
                    self.log.info("Retrying LLM request", extra={"delay": delay})
                    time.sleep(delay)
                else:
                    self.log.error("All LLM retry attempts failed", extra={"error": str(exc)})

        return None

    def chat_completion_with_tools(
        self,
        messages: list[dict[str, str]],
        tools: list[dict[str, Any]],
        *,
        model: str | None = None,
        temperature: float = 0.1,
        max_tokens: int | None = None,
        tool_choice: str | dict[str, Any] = "auto",
        max_retries: int | None = None,
    ) -> LLMResponse | None:
        """Generate chat completion with tool calling for structured outputs.

        Uses OpenAI tool calling API which is more token-efficient than JSON Schema
        for structured outputs. The tool call arguments are returned as the response text.

        Parameters
        ----------
        messages:
            List of message dictionaries with 'role' and 'content' keys.
        tools:
            List of tool definitions following OpenAI tool calling format.
        model:
            Model to use. Defaults to client's default model.
        temperature:
            Sampling temperature (0.0 to 2.0).
        max_tokens:
            Maximum tokens to generate.
        tool_choice:
            Tool choice mode: "auto", "none", or {"type": "function", "function": {"name": "..."}}.
            Use "required" to force tool call (equivalent to {"type": "function", "function": {"name": tools[0]["function"]["name"]}}).
        max_retries:
            Override default max retries for this call.

        Returns
        -------
        LLMResponse | None
            Structured response with tool call arguments as text, or None if failed.
        """
        if self._client is None:
            self.log.warning("LLM client not available; returning None")
            return None

        model = model or self.model
        last_exception = None
        retries = self.max_retries if max_retries is None else max(0, int(max_retries))

        # Normalize tool_choice
        if tool_choice == "required" and tools:
            tool_choice = {"type": "function", "function": {"name": tools[0]["function"]["name"]}}

        for attempt in range(retries + 1):
            try:
                self.log.debug(
                    "LLM tool calling request attempt",
                    extra={"attempt": attempt + 1, "model": model, "tools_count": len(tools)},
                )

                response = self._client.chat.completions.create(
                    model=model,
                    messages=messages,
                    tools=tools,
                    tool_choice=tool_choice,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )

                # Extract response data
                choice = response.choices[0]
                message = choice.message

                # Extract tool call arguments as text
                text = ""
                if message.tool_calls and len(message.tool_calls) > 0:
                    # Use first tool call arguments as response text
                    tool_call = message.tool_calls[0]
                    text = tool_call.function.arguments
                elif message.content:
                    text = message.content

                # Normalize usage
                if response.usage is None:
                    usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
                else:
                    try:
                        usage = {
                            "prompt_tokens": int(getattr(response.usage, "prompt_tokens", 0) or 0),
                            "completion_tokens": int(getattr(response.usage, "completion_tokens", 0) or 0),
                            "total_tokens": int(getattr(response.usage, "total_tokens", 0) or 0),
                        }
                    except Exception:
                        try:
                            u = dict(response.usage)
                            usage = {
                                "prompt_tokens": int(u.get("prompt_tokens", 0) or 0),
                                "completion_tokens": int(u.get("completion_tokens", 0) or 0),
                                "total_tokens": int(u.get("total_tokens", 0) or 0),
                            }
                        except Exception:
                            usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

                self.log.debug(
                    "LLM tool calling response received",
                    extra={"model": model, "text_length": len(text), "usage": usage},
                )

                # Track cost
                self._track_cost(model, usage)

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
                    "LLM tool calling request failed",
                    extra={"attempt": attempt + 1, "error": str(exc), "error_type": type(exc).__name__},
                )

                if attempt < retries:
                    delay = self.retry_delay * (2 ** attempt)
                    self.log.info("Retrying LLM tool calling request", extra={"delay": delay})
                    time.sleep(delay)
                else:
                    self.log.error("All LLM tool calling retry attempts failed", extra={"error": str(exc)})

        return None

    def get_embeddings(self, *, text: str, model: str | None = None) -> list[float] | None:
        """Return embedding vector for a single text when provider is available.

        Falls back to None; callers may implement deterministic hashing.
        """
        if self._client is None:
            return None
        try:
            m = model or "text-embedding-3-small"
            resp = self._client.embeddings.create(model=m, input=text)
            vec = resp.data[0].embedding
            
            # Track embedding cost
            usage = {
                "prompt_tokens": resp.usage.prompt_tokens if resp.usage else 0,
                "completion_tokens": 0,
                "total_tokens": resp.usage.total_tokens if resp.usage else 0,
            }
            self._track_cost(m, usage)
            
            return [float(x) for x in vec]
        except Exception as exc:
            self.log.warning("Embedding request failed", extra={"error": str(exc)})
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

        # Normalize common wrappers (strip code fences)
        t0 = text.strip()
        if t0.startswith("```"):
            try:
                # remove first fence line and last fence if present
                lines = t0.splitlines()
                if len(lines) >= 2 and lines[0].startswith("```"):
                    if lines[-1].startswith("```"):
                        t0 = "\n".join(lines[1:-1]).strip()
                    else:
                        t0 = "\n".join(lines[1:]).strip()
            except Exception:
                pass

        # Try direct JSON parsing first
        try:
            result = json.loads(t0)
            self.log.debug("JSON extracted successfully", keys=list(result.keys()) if isinstance(result, dict) else None)
            return result
        except json.JSONDecodeError as e:
            self.log.debug("Direct JSON parsing failed", error=str(e))

        if not fallback_parsing:
            return None

        # Fallback 1: extract first JSON object/array and balance delimiters
        try:
            s = text
            # normalize smart quotes
            s = s.replace("“", '"').replace("”", '"').replace("’", "'")
            # find first JSON start
            start_idx_obj = s.find('{')
            start_idx_arr = s.find('[')
            starts = [idx for idx in [start_idx_obj, start_idx_arr] if idx != -1]
            if starts:
                start = min(starts)
                candidate = s[start:]
                # balance braces/brackets to cut a plausible JSON snippet
                def _balanced_cut(payload: str) -> str:
                    depth_obj = 0
                    depth_arr = 0
                    for i, ch in enumerate(payload):
                        if ch == '{':
                            depth_obj += 1
                        elif ch == '}':
                            depth_obj = max(0, depth_obj - 1)
                        elif ch == '[':
                            depth_arr += 1
                        elif ch == ']':
                            depth_arr = max(0, depth_arr - 1)
                        if depth_obj == 0 and depth_arr == 0 and i > 0:
                            return payload[: i + 1]
                    return payload
                snippet = _balanced_cut(candidate).strip()
                # remove trailing commas before } or ]
                snippet = re.sub(r",\s*([}\]])", r"\1", snippet)
                # try load
                try:
                    result = json.loads(snippet)
                    self.log.debug("JSON extracted via balanced snippet")
                    return result
                except json.JSONDecodeError:
                    pass

        except Exception as exc:
            self.log.warning("Fallback JSON parsing failed", extra={"error": str(exc)})

        # Fallback 2: regex search for objects/arrays, as last resort
        try:
            json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
            for match in re.findall(json_pattern, text, re.DOTALL):
                try:
                    m2 = re.sub(r",\s*([}\]])", r"\1", match)
                    result = json.loads(m2)
                    self.log.debug("JSON extracted via regex object")
                    return result
                except json.JSONDecodeError:
                    continue
            array_pattern = r'\[[^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*\]'
            for match in re.findall(array_pattern, text, re.DOTALL):
                try:
                    m2 = re.sub(r",\s*([}\]])", r"\1", match)
                    result = json.loads(m2)
                    self.log.debug("JSON extracted via regex array")
                    return {"data": result}
                except json.JSONDecodeError:
                    continue
        except Exception as exc:
            self.log.warning("Regex JSON parsing failed", extra={"error": str(exc)})

        self.log.warning("All JSON extraction methods failed", extra={"text_preview": text[:100]})
        return None

    def _track_cost(self, model: str, usage: dict[str, int]) -> None:
        """Track LLM API costs based on model and token usage.

        Calculates cost using OpenAI pricing (as of 2024) and records metrics.
        Falls back gracefully if metrics are unavailable.

        Parameters
        ----------
        model:
            Model identifier (e.g., "gpt-4o-mini", "gpt-4o").
        usage:
            Token usage dictionary with prompt_tokens, completion_tokens, total_tokens.
        """
        try:
            # OpenAI pricing per 1M tokens (as of 2024)
            pricing: dict[str, dict[str, float]] = {
                "gpt-4o": {"input": 2.50, "output": 10.00},
                "gpt-4o-mini": {"input": 0.15, "output": 0.60},
                "gpt-4-turbo": {"input": 10.00, "output": 30.00},
                "gpt-4": {"input": 30.00, "output": 60.00},
                "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
                "text-embedding-3-small": {"input": 0.02, "output": 0.0},
                "text-embedding-3-large": {"input": 0.13, "output": 0.0},
                "text-embedding-ada-002": {"input": 0.10, "output": 0.0},
            }

            # Find matching model pricing (handle model variants)
            model_key = model.lower()
            for key, prices in pricing.items():
                if key in model_key:
                    input_price = prices["input"]
                    output_price = prices["output"]
                    break
            else:
                # Default to gpt-4o-mini pricing if unknown
                input_price = 0.15
                output_price = 0.60
                self.log.debug("Unknown model pricing, using default", extra={"model": model})

            prompt_tokens = usage.get("prompt_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)

            # Calculate cost in USD
            input_cost = (prompt_tokens / 1_000_000.0) * input_price
            output_cost = (completion_tokens / 1_000_000.0) * output_price
            total_cost = input_cost + output_cost

            # Record metrics if available
            try:
                from app.infra.metrics import inc_counter, observe_histogram

                inc_counter(
                    "llm_cost_usd_total",
                    labels={"model": model},
                    amount=total_cost,
                )
                observe_histogram(
                    "llm_tokens_total",
                    value=float(usage.get("total_tokens", 0)),
                    labels={"model": model, "type": "total"},
                )
                observe_histogram(
                    "llm_tokens_total",
                    value=float(prompt_tokens),
                    labels={"model": model, "type": "prompt"},
                )
                observe_histogram(
                    "llm_tokens_total",
                    value=float(completion_tokens),
                    labels={"model": model, "type": "completion"},
                )
            except Exception:
                pass  # Metrics unavailable, continue silently

            self.log.debug(
                "Cost tracked",
                extra={
                    "model": model,
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "cost_usd": total_cost,
                },
            )

        except Exception as exc:
            self.log.debug("Cost tracking failed", extra={"error": str(exc)})

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
        # Pull defaults from settings when available
        try:
            from app.config.settings import get_settings as _get_settings  # local import
            _cfg = _get_settings()
            timeout = float(getattr(getattr(_cfg, "openai"), "request_timeout_ms", 90000) / 1000.0)
            max_retries = int(getattr(getattr(_cfg, "openai"), "max_retries", 3))
        except Exception:
            timeout = 90.0
            max_retries = 3

        _LLM_CLIENT = LLMClient(api_key=api_key, model=model, timeout=timeout, max_retries=max_retries)
    
    return _LLM_CLIENT
