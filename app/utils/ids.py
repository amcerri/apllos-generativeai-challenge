"""
ID utilities

Overview
    Helpers to generate and validate identifiers for logs, thread correlation,
    and lightweight persistence. Prefers stdlib primitives (uuid, secrets,
    hashlib) and avoids external dependencies.

Design
    - Deterministic hashing via `stable_hash` (JSON-serialized input).
    - Random, URL-safe tokens via `random_token` (length-capped).
    - Short, human-friendly IDs via `short_uuid` (wrapper) and `ulid` generator.
    - Thread IDs combine UTC timestamp with a short suffix for easy eyeballing.

Integration
    - Safe to import early; no I/O and no global state beyond constants.
    - Complements `app.utils.__init__` helpers; does not require other packages.

Usage
    >>> from app.utils.ids import short_uuid, random_token, stable_hash, make_thread_id, ulid
    >>> short_uuid()
    'a1b2c3d4'
    >>> token = random_token(24)
    >>> h = stable_hash({"a": 1, "b": 2}, length=12)
    >>> tid = make_thread_id()
    >>> u = ulid()
"""

from __future__ import annotations

import hashlib
import secrets
import uuid
from typing import Any

from . import safe_json_dumps, utc_now
from . import short_uuid as _short_uuid

__all__ = [
    "short_uuid",
    "random_token",
    "stable_hash",
    "make_thread_id",
    "is_valid_uuid",
    "parse_uuid",
    "normalize_id",
    "ulid",
]


# ---------------------------------------------------------------------------
# Short IDs & tokens
# ---------------------------------------------------------------------------


def short_uuid(length: int = 8) -> str:
    """Return a lowercase hex short id derived from UUID4 (default 8 chars).

    Wrapper around `app.utils.short_uuid` for discoverability in this module.
    """

    return _short_uuid(length)


def random_token(length: int = 32, *, url_safe: bool = True) -> str:
    """Return a cryptographically-strong random token with approximate length.

    - When `url_safe=True` (default), uses base64url characters; output is
      trimmed to `length`.
    - When `False`, returns a hex string of exact length.
    """

    if length <= 0:
        return ""

    if url_safe:
        # token_urlsafe takes bytes and yields ~ceil(n*4/3) chars; generate and trim
        nbytes = max(1, (length * 3) // 4)
        token = secrets.token_urlsafe(nbytes)
        if len(token) >= length:
            return token[:length]
        # If shorter (rare), extend until we reach the desired length
        parts = [token]
        while sum(len(p) for p in parts) < length:
            parts.append(secrets.token_urlsafe(1))
        return ("".join(parts))[:length]

    # Hex path: each byte → two hex chars; request enough bytes then slice
    nbytes = (length + 1) // 2
    return secrets.token_hex(nbytes)[:length]


# ---------------------------------------------------------------------------
# Deterministic hashing
# ---------------------------------------------------------------------------


def stable_hash(value: Any, *, algo: str = "sha256", length: int = 16) -> str:
    """Return a stable hex digest for arbitrary JSON-serializable input.

    - Uses `safe_json_dumps` (sorted keys) for canonicalization.
    - Supports any `hashlib` algorithm name (default: sha256).
    - Output is truncated to `length` (min 1).
    """

    payload = safe_json_dumps(value)
    h = hashlib.new(algo)
    h.update(payload.encode("utf-8"))
    cut = max(1, int(length))
    return h.hexdigest()[:cut]


# ---------------------------------------------------------------------------
# Thread-friendly IDs
# ---------------------------------------------------------------------------


def make_thread_id(prefix: str = "thr", *, suffix_len: int = 8) -> str:
    """Return an easy-to-read thread id: `prefix-YYYYMMDDThhmmssZ-xxxxxxxx`.

    The suffix uses `short_uuid` (hex); the timestamp is UTC.
    """

    ts = utc_now().strftime("%Y%m%dT%H%M%SZ")
    return f"{prefix}-{ts}-{short_uuid(suffix_len)}"


# ---------------------------------------------------------------------------
# UUID helpers
# ---------------------------------------------------------------------------


def is_valid_uuid(value: str) -> bool:
    """Return True if `value` is a valid UUID string (any variant)."""

    try:
        uuid.UUID(str(value))
        return True
    except Exception:
        return False


def parse_uuid(value: str) -> uuid.UUID | None:
    """Return `UUID` if parseable, else `None`. Accepts hyphenated or hex-only."""

    try:
        return uuid.UUID(str(value))
    except Exception:
        return None


def normalize_id(value: str | None, *, lower: bool = True) -> str | None:
    """Trim and optionally lowercase an id-like string; empty → None."""

    if value is None:
        return None
    s = str(value).strip()
    if lower:
        s = s.lower()
    return s or None


# ---------------------------------------------------------------------------
# ULID (Universally Unique Lexicographically Sortable Identifier)
# ---------------------------------------------------------------------------
_ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"  # Crockford's Base32 (no I, L, O, U)


def _encode_crockford(value: int, length: int) -> str:
    chars: list[str] = []
    for _ in range(length):
        chars.append(_ALPHABET[value & 31])
        value >>= 5
    return "".join(reversed(chars))


def ulid() -> str:
    """Generate a ULID string (26 chars, Crockford base32).

    ULID = 48-bit timestamp (ms) + 80-bit randomness; lexicographically sortable.
    """

    # 48-bit timestamp in milliseconds
    ts_ms = int(utc_now().timestamp() * 1000) & ((1 << 48) - 1)
    rand80 = secrets.randbits(80)
    value = (ts_ms << 80) | rand80
    return _encode_crockford(value, 26)
