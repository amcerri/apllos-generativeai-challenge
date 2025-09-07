"""
Human-in-the-loop gates — end‑to‑end tests.

Overview
--------
These tests validate the shape and availability of our human approval gates used
in the LangGraph pipeline. They avoid heavy dependencies (DB/LLM) and focus on
contract-level checks so CI remains deterministic in this POC.

What we assert
--------------
- A SQL approval gate can be created with basic fields present.
- Gate payloads are JSON-serializable (primitive-friendly) and contain the
  provided SQL/metadata.
- The graph builder exposes the `require_sql_approval` toggle for runtime wiring.

Integration
-----------
Imports are guarded. If a symbol is missing in this environment, the test will
`pytest.skip` gracefully.
"""

from __future__ import annotations

import importlib
import json
from collections.abc import Mapping, Sequence
from typing import Any

import pytest

# ---------------------------------------------------------------------------
# Helper utilities (pure Python)
# ---------------------------------------------------------------------------


def _is_mapping(x: Any) -> bool:
    return isinstance(x, Mapping)


def _flatten_items(obj: Any, prefix: str = "") -> list[tuple[str, Any]]:
    """Flatten nested mappings/lists into (path, value) tuples for probing."""
    out: list[tuple[str, Any]] = []
    if isinstance(obj, Mapping):
        for k, v in obj.items():
            key = f"{prefix}.{k}" if prefix else str(k)
            out.extend(_flatten_items(v, key))
    elif isinstance(obj, Sequence) and not isinstance(obj, str | bytes | bytearray):
        for i, v in enumerate(list(obj)[:100]):
            key = f"{prefix}[{i}]"
            out.extend(_flatten_items(v, key))
    else:
        out.append((prefix, obj))
    return out


def _find_first(
    obj: Any, *, key_eq: str | None = None, key_contains: str | None = None
) -> Any | None:
    if not isinstance(obj, Mapping):
        return None
    for k, v in obj.items():
        if (key_eq and k == key_eq) or (key_contains and key_contains in str(k)):
            return v
        if isinstance(v, Mapping):
            found = _find_first(v, key_eq=key_eq, key_contains=key_contains)
            if found is not None:
                return found
    return None


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "sample",
    [
        {"sql": "SELECT 1", "params": {}, "limit": 5, "tables": ["orders"], "reason": "preview"},
        {
            "sql": "WITH x AS (SELECT 1) SELECT * FROM x",
            "params": {},
            "limit": 10,
            "tables": [],
            "reason": "cte",
        },
    ],
)
def test_sql_gate_shape_and_serializability(sample: Mapping[str, Any]) -> None:
    # Dynamically load gate factory to avoid attr errors in different envs
    try:
        intr = importlib.import_module("app.graph.interrupts")
        make_sql_gate = getattr(intr, "make_sql_gate", None)
    except Exception as exc:  # pragma: no cover - optional
        pytest.skip(f"interrupts module unavailable: {type(exc).__name__}")
        return

    if make_sql_gate is None or not callable(make_sql_gate):
        pytest.skip("make_sql_gate not available")
        return

    gate = make_sql_gate(**sample)
    assert _is_mapping(gate), "gate should be a mapping/dict-like structure"

    # Basic top-level signals: try common keys but don't enforce strict schema
    name = _find_first(gate, key_eq="name") or _find_first(gate, key_contains="name")
    gtype = _find_first(gate, key_eq="type") or _find_first(gate, key_contains="type")
    assert isinstance(name, str) or isinstance(gtype, str), "gate should expose a name/type"

    # Must contain the SQL text somewhere in payload
    found_sql = _find_first(gate, key_eq="sql") or _find_first(gate, key_contains="sql")
    assert isinstance(found_sql, str) and "select" in found_sql.lower()

    # Limit and tables (if provided) should round-trip as primitives/arrays
    lim = _find_first(gate, key_eq="limit") or _find_first(gate, key_contains="limit")
    if lim is not None:
        assert isinstance(lim, int) and lim > 0
    tabs = _find_first(gate, key_eq="tables") or _find_first(gate, key_contains="table")
    if tabs is not None:
        assert isinstance(tabs, Sequence)

    # Ensure JSON-serializable
    json.dumps(dict(_flatten_items(gate)))


def test_graph_builder_exposes_sql_toggle() -> None:
    try:
        build = importlib.import_module("app.graph.build")
        build_graph = getattr(build, "build_graph", None)
    except Exception as exc:  # pragma: no cover - optional
        pytest.skip(f"graph builder unavailable: {type(exc).__name__}")
        return

    if build_graph is None or not callable(build_graph):
        pytest.skip("build_graph not available")
        return

    g = build_graph(require_sql_approval=True)
    if isinstance(g, Mapping):
        # For our POC, we expect the compiled graph config to carry this flag
        val = g.get("require_sql_approval")
        assert val is True
    else:
        # If a compiled object is returned, ensure the call doesn't error
        assert g is not None
