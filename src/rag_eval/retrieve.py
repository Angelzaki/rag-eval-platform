from __future__ import annotations

import math
import re
from collections import Counter

from rag_eval.models import Chunk, RetrievedChunk

TOKEN = re.compile(r"[a-zA-ZáéíóúñÁÉÍÓÚÑ0-9]+")


def tokenize(text: str) -> list[str]:
    return [t.lower() for t in TOKEN.findall(text)]


def _tfidf_vectors(corpus: list[list[str]]) -> tuple[list[dict[str, float]], dict[str, float]]:
    df: Counter[str] = Counter()
    for tokens in corpus:
        df.update(set(tokens))
    n = len(corpus)
    idf = {term: math.log((n + 1) / (freq + 1)) + 1.0 for term, freq in df.items()}
    vectors: list[dict[str, float]] = []
    for tokens in corpus:
        tf = Counter(tokens)
        length = len(tokens) or 1
        vectors.append({t: (c / length) * idf[t] for t, c in tf.items()})
    return vectors, idf


def _cosine(a: dict[str, float], b: dict[str, float]) -> float:
    keys = set(a) | set(b)
    if not keys:
        return 0.0
    dot = sum(a.get(k, 0.0) * b.get(k, 0.0) for k in keys)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


class LocalRetriever:
    def __init__(self, chunks: list[Chunk]):
        self.chunks = chunks
        tokenized = [tokenize(c.text) for c in chunks]
        self.vectors, self.idf = _tfidf_vectors(tokenized)

    def search(self, query: str, k: int = 3) -> list[RetrievedChunk]:
        q_tokens = tokenize(query)
        tf = Counter(q_tokens)
        length = len(q_tokens) or 1
        q_vec = {t: (c / length) * self.idf.get(t, 0.0) for t, c in tf.items()}
        scored = [
            RetrievedChunk(chunk=chunk, score=_cosine(q_vec, vec))
            for chunk, vec in zip(self.chunks, self.vectors)
        ]
        scored.sort(key=lambda x: x.score, reverse=True)
        return scored[:k]
