from __future__ import annotations

from rag_eval.chunk import chunk_corpus
from rag_eval.models import SuiteResult


def run_chunking(ctx: dict) -> SuiteResult:
    docs = ctx["docs"]
    chunks = chunk_corpus(docs, size=280, overlap=40)
    details = []
    passed = failed = 0

    ok_any = len(chunks) > 0
    details.append({"check": "chunks_created", "count": len(chunks), "ok": ok_any})
    passed += int(ok_any)
    failed += int(not ok_any)

    covered_docs = {c.doc_id for c in chunks}
    for doc in docs:
        ok = doc.doc_id in covered_docs
        details.append({"check": "doc_covered", "doc_id": doc.doc_id, "ok": ok})
        passed += int(ok)
        failed += int(not ok)

    empty = [c for c in chunks if not c.text.strip()]
    ok_empty = len(empty) == 0
    details.append({"check": "no_empty_chunks", "empty": len(empty), "ok": ok_empty})
    passed += int(ok_empty)
    failed += int(not ok_empty)

    for doc in docs:
        joined = " ".join(c.text for c in chunks if c.doc_id == doc.doc_id)
        sample = doc.text[:80].split()
        hits = sum(1 for w in sample if w in joined)
        ok = hits >= max(1, len(sample) // 2)
        details.append({"check": "content_preserved", "doc_id": doc.doc_id, "ok": ok})
        passed += int(ok)
        failed += int(not ok)

    return SuiteResult(name="chunking", passed=passed, failed=failed, details=details)
