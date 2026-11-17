from __future__ import annotations

from pathlib import Path

from rag_eval.extract import extract_text, load_corpus
from rag_eval.models import SuiteResult


def run_extraction(ctx: dict) -> SuiteResult:
    docs_dir = Path(ctx["docs_dir"])
    details = []
    passed = failed = 0

    files = [p for p in docs_dir.rglob("*") if p.is_file() and p.suffix.lower() in {".txt", ".md"}]
    for path in files:
        try:
            text = extract_text(path)
            ok = len(text.strip()) > 20
            details.append({"file": str(path), "chars": len(text), "ok": ok})
            passed += int(ok)
            failed += int(not ok)
        except Exception as exc:
            details.append({"file": str(path), "ok": False, "error": str(exc)})
            failed += 1

    corpus = load_corpus(docs_dir)
    ok_corpus = len(corpus) >= 2
    details.append({"check": "corpus_min_docs", "count": len(corpus), "ok": ok_corpus})
    passed += int(ok_corpus)
    failed += int(not ok_corpus)

    return SuiteResult(name="extraction", passed=passed, failed=failed, details=details)
