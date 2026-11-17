from __future__ import annotations

from rag_eval.metrics import faithfulness_ratio
from rag_eval.models import SuiteResult


def run_faithfulness(ctx: dict) -> SuiteResult:
    gt = ctx["ground_truth"]
    answerer = ctx["answerer"]
    details = []
    passed = failed = 0
    threshold = ctx.get("faithfulness_threshold", 0.45)

    for item in gt:
        if item.should_abstain:
            continue
        result = answerer.ask(item.question)
        contexts = [r.chunk.text for r in result.retrieved]
        ratio = faithfulness_ratio(result.answer, contexts)
        ok = ratio >= threshold
        details.append(
            {
                "id": item.id,
                "faithfulness": round(ratio, 3),
                "ok": ok,
            }
        )
        passed += int(ok)
        failed += int(not ok)

    return SuiteResult(name="faithfulness", passed=passed, failed=failed, details=details)
