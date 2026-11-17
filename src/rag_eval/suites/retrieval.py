from __future__ import annotations

from rag_eval.models import SuiteResult


def run_retrieval(ctx: dict) -> SuiteResult:
    gt = ctx["ground_truth"]
    retriever = ctx["retriever"]
    details = []
    passed = failed = 0

    for item in gt:
        if item.should_abstain:
            continue
        hits = retriever.search(item.question, k=3)
        doc_ids = [h.chunk.doc_id for h in hits]
        ok = item.source_doc in doc_ids
        details.append(
            {
                "id": item.id,
                "expected_doc": item.source_doc,
                "retrieved": doc_ids,
                "top_score": hits[0].score if hits else 0.0,
                "ok": ok,
            }
        )
        passed += int(ok)
        failed += int(not ok)

    return SuiteResult(name="retrieval", passed=passed, failed=failed, details=details)
