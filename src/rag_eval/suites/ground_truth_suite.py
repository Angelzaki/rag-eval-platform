from __future__ import annotations

from rag_eval.metrics import keyword_coverage, token_f1
from rag_eval.models import SuiteResult


def run_ground_truth(ctx: dict) -> SuiteResult:
    gt = ctx["ground_truth"]
    answerer = ctx["answerer"]
    details = []
    passed = failed = 0
    threshold = ctx.get("gt_threshold", 0.35)

    for item in gt:
        if item.should_abstain:
            continue
        result = answerer.ask(item.question)
        f1 = token_f1(item.expected_answer, result.answer)
        cover = keyword_coverage(item.expected_keywords, result.answer)
        score = 0.6 * f1 + 0.4 * cover
        ok = score >= threshold and not result.abstained
        details.append(
            {
                "id": item.id,
                "f1": round(f1, 3),
                "keyword_coverage": round(cover, 3),
                "score": round(score, 3),
                "answer": result.answer,
                "ok": ok,
            }
        )
        passed += int(ok)
        failed += int(not ok)

    return SuiteResult(name="ground_truth", passed=passed, failed=failed, details=details)
