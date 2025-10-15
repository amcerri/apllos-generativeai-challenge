import json
import os

import pytest


class _StubBackend:
    """Stub JSON backend that inspects messages to decide agent.

    - For ensemble variants, we infer intent from examples in messages.
    - For scorer, we return fixed scores favoring analytics.
    """

    def generate_json(self, *, system, messages, json_schema, model=None, temperature=0.0, max_output_tokens=None):  # noqa: D401 - test stub
        content = "\n".join(str(m.get("content", "")) for m in messages if isinstance(m, dict))
        # Scorer path: detect scorer system hint
        if "routing scorer" in system.lower():
            return {"scores": {"analytics": 0.9, "commerce": 0.1, "knowledge": 0.2, "triage": 0.1}}

        low = content.lower()
        # Simulate decisions based on example cues
        if any(k in low for k in ("fatura", "nota fiscal", "invoice", "contrato")):
            return {
                "agent": "commerce",
                "confidence": 0.8,
                "reason": "document processing",
                "tables": [],
                "columns": [],
                "signals": ["commerce_doc"],
                "thread_id": None,
            }
        if any(k in low for k in ("select", " from ", "orders", "média", "soma", "quantos")):
            return {
                "agent": "analytics",
                "confidence": 0.8,
                "reason": "data query",
                "tables": ["orders"] if "orders" in low else [],
                "columns": [],
                "signals": ["sql_intent"],
                "thread_id": None,
            }
        return {
            "agent": "knowledge",
            "confidence": 0.7,
            "reason": "conceptual",
            "tables": [],
            "columns": [],
            "signals": ["doc_intent"],
            "thread_id": None,
        }


def _make_classifier(monkeypatch):
    from app.routing.llm_classifier import LLMClassifier

    clf = LLMClassifier(backend=_StubBackend(), model="test-router", temperature=0.0)

    # Craft examples set with analytics-heavy cues and a few commerce cues
    examples = [
        {"role": "user", "content": "Quantos pedidos?"},
        {"role": "assistant", "content": json.dumps({"agent": "analytics"})},
        {"role": "user", "content": "SELECT * FROM orders LIMIT 10"},
        {"role": "assistant", "content": json.dumps({"agent": "analytics"})},
        {"role": "user", "content": "Processe esta fatura"},
        {"role": "assistant", "content": json.dumps({"agent": "commerce"})},
    ]

    def _fake_load_examples(self):
        return examples

    monkeypatch.setattr(LLMClassifier, "_load_examples", _fake_load_examples, raising=False)
    return clf


def test_ensemble_majority_analytics(monkeypatch):
    # Ensure ensemble is on
    os.environ["ROUTER_ENSEMBLE_ENABLED"] = "true"
    os.environ["ROUTER_SCORER_ENABLED"] = "true"
    clf = _make_classifier(monkeypatch)

    dec = clf.classify("Preciso de um relatório simples")
    assert getattr(dec, "agent", dec.get("agent")) == "analytics"
    # ensemble should tag a signal
    sigs = getattr(dec, "signals", dec.get("signals"))
    assert "ensemble_majority" in sigs or "ensemble_scorer" in sigs


def test_ensemble_tie_uses_scorer(monkeypatch):
    # Make examples balanced to force a tie; scorer favors analytics
    os.environ["ROUTER_ENSEMBLE_ENABLED"] = "true"
    os.environ["ROUTER_SCORER_ENABLED"] = "true"
    from app.routing.llm_classifier import LLMClassifier

    clf = LLMClassifier(backend=_StubBackend(), model="test-router", temperature=0.0)

    # balanced examples with both commerce and analytics cues
    examples = [
        {"role": "user", "content": "Processe esta fatura"},
        {"role": "assistant", "content": json.dumps({"agent": "commerce"})},
        {"role": "user", "content": "SELECT * FROM orders"},
        {"role": "assistant", "content": json.dumps({"agent": "analytics"})},
    ]

    def _fake_load_examples(self):
        return examples

    monkeypatch.setattr(LLMClassifier, "_load_examples", _fake_load_examples, raising=False)

    dec = clf.classify("Preciso de ajuda")
    assert getattr(dec, "agent", dec.get("agent")) == "analytics"
    sigs = getattr(dec, "signals", dec.get("signals"))
    assert "ensemble_scorer" in sigs


