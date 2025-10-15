def test_supervisor_uses_routing_ctx_for_fallback():
    from app.routing.supervisor import supervise, RoutingContext

    # Router decided analytics with weak signals, but probes indicate doc-style and RAG hit
    dec = {
        "agent": "analytics",
        "confidence": 0.55,
        "reason": "weak sql cues",
        "tables": [],
        "columns": [],
        "signals": [],
        "thread_id": None,
    }
    ctx = RoutingContext(
        rag_hits=1,
        rag_min_score=0.85,
        allowlist_tables=(),
        allowlist_columns=(),
        extra_signals=("doc_style",),
    )

    final = supervise(dec, ctx)
    assert final["agent"] in {"knowledge", "analytics"}
    # With doc_style and rag_hits the fallback to knowledge is expected
    assert final["agent"] == "knowledge"
    assert "supervisor_fallback" in final.get("signals", [])


