from __future__ import annotations

import re

TOKEN = re.compile(r"[a-zA-ZáéíóúñÁÉÍÓÚÑ0-9]+")


def tokens(text: str) -> set[str]:
    return {t.lower() for t in TOKEN.findall(text)}


def keyword_coverage(expected_keywords: list[str], answer: str) -> float:
    if not expected_keywords:
        return 1.0
    ans = answer.lower()
    hits = sum(1 for kw in expected_keywords if kw.lower() in ans)
    return hits / len(expected_keywords)


def token_f1(expected: str, predicted: str) -> float:
    exp = tokens(expected)
    pred = tokens(predicted)
    if not exp and not pred:
        return 1.0
    if not exp or not pred:
        return 0.0
    overlap = len(exp & pred)
    precision = overlap / len(pred)
    recall = overlap / len(exp)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def faithfulness_ratio(answer: str, contexts: list[str]) -> float:
    ans_tokens = tokens(answer)
    if not ans_tokens:
        return 1.0
    context_tokens = set()
    for ctx in contexts:
        context_tokens |= tokens(ctx)
    supported = sum(1 for t in ans_tokens if t in context_tokens)
    return supported / len(ans_tokens)


def citation_support(citations: list[str], contexts: list[str], answer: str) -> float:
    if not citations:
        return 0.0 if answer.strip() else 1.0
    joined = " ".join(contexts).lower()
    hits = sum(1 for c in citations if c.lower() in joined or any(c.lower() in ctx.lower() for ctx in contexts))
    return hits / len(citations)
