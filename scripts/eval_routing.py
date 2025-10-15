#!/usr/bin/env python3
"""
Evaluate routing accuracy against a small labeled YAML/JSONL set.

Usage:
  python scripts/eval_routing.py --input tests/batch/test_routing.yaml
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def _load_examples(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() in {".jsonl"}:
        out: list[dict[str, Any]] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            out.append(json.loads(line))
        return out
    if path.suffix.lower() in {".json"}:
        return json.loads(path.read_text(encoding="utf-8"))
    if path.suffix.lower() in {".yaml", ".yml"}:
        import yaml  # type: ignore
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and "cases" in data:
            return list(data["cases"])
    raise SystemExit(f"Unsupported input file: {path}")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Labeled set (yaml/json/jsonl)")
    args = ap.parse_args(argv)

    path = Path(args.input).resolve()
    rows = _load_examples(path)

    # Lazy import to avoid hard deps in runtime env
    from app.routing.llm_classifier import LLMClassifier

    clf = LLMClassifier()

    total = 0
    correct = 0
    mistakes: list[dict[str, Any]] = []

    for row in rows:
        msg = str(row.get("input") or row.get("message") or "").strip()
        expected = str(row.get("expected") or row.get("agent") or "").strip()
        if not msg or not expected:
            continue
        total += 1
        dec = clf.classify(msg)
        agent = getattr(dec, "agent", None) or (dec.get("agent") if isinstance(dec, dict) else None)
        if agent == expected:
            correct += 1
        else:
            mistakes.append({"msg": msg, "expected": expected, "got": agent})

    acc = (correct / total) if total else 0.0
    print(json.dumps({"total": total, "correct": correct, "accuracy": acc, "mistakes": mistakes}, ensure_ascii=False, indent=2))
    return 0 if total and acc >= 0.0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


