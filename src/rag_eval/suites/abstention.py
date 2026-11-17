from __future__ import annotations

from rag_eval.models import SuiteResult


def run_abstention(ctx: dict) -> SuiteResult:
    gt = ctx["ground_truth"]
    answerer = ctx["answerer"]
    details = []
    passed = failed = 0

    for item in gt:
        result = answerer.ask(item.question)
        if item.should_abstain:
            ok = result.abstained
        else:
            ok = not result.abstained
        details.append(
            {
                "id": item.id,
                "should_abstain": item.should_abstain,
                "abstained": result.abstained,
                "ok": ok,
            }
        )
        passed += int(ok)
        failed += int(not ok)

    return SuiteResult(name="abstention", passed=passed, failed=failed, details=details)
