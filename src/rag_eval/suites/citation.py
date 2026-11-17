from __future__ import annotations

from rag_eval.models import SuiteResult


def run_citation(ctx: dict) -> SuiteResult:
    gt = ctx["ground_truth"]
    answerer = ctx["answerer"]
    details = []
    passed = failed = 0

    for item in gt:
        if item.should_abstain:
            continue
        result = answerer.ask(item.question)
        if result.abstained:
            details.append({"id": item.id, "ok": False, "reason": "abstained"})
            failed += 1
            continue
        ok_has = len(result.citations) > 0
        ok_source = item.source_doc in result.citations
        ok = ok_has and ok_source
        details.append(
            {
                "id": item.id,
                "citations": result.citations,
                "expected": item.source_doc,
                "ok": ok,
            }
        )
        passed += int(ok)
        failed += int(not ok)

    return SuiteResult(name="citation", passed=passed, failed=failed, details=details)
