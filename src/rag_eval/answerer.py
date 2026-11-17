from __future__ import annotations

from rag_eval.models import RagAnswer
from rag_eval.retrieve import LocalRetriever, tokenize


ABSTAIN_PHRASE = "No cuento con evidencia suficiente en el corpus para responder."
STOP = {
    "politica",
    "política",
    "cuales",
    "cuáles",
    "cual",
    "cuál",
    "como",
    "cómo",
    "que",
    "qué",
    "tiene",
    "tienen",
    "para",
    "sobre",
    "desde",
    "hasta",
    "este",
    "esta",
    "estos",
    "estas",
}


class HeuristicAnswerer:
    def __init__(self, retriever: LocalRetriever, min_score: float = 0.12):
        self.retriever = retriever
        self.min_score = min_score

    def ask(self, question: str, k: int = 3) -> RagAnswer:
        retrieved = self.retriever.search(question, k=k)
        if not retrieved or not self._has_evidence(question, retrieved[0].chunk.text, retrieved[0].score):
            return RagAnswer(
                question=question,
                answer=ABSTAIN_PHRASE,
                citations=[],
                retrieved=retrieved,
                abstained=True,
            )

        contexts = [r.chunk.text for r in retrieved]
        answer = self._compose(question, contexts)
        citations = [r.chunk.doc_id for r in retrieved]
        return RagAnswer(
            question=question,
            answer=answer,
            citations=list(dict.fromkeys(citations)),
            retrieved=retrieved,
            abstained=False,
        )

    def _has_evidence(self, question: str, chunk_text: str, score: float) -> bool:
        if score < self.min_score:
            return False
        content = [t for t in tokenize(question) if t not in STOP and len(t) > 3]
        if not content:
            return score >= max(self.min_score, 0.25)
        ctx = set(tokenize(chunk_text))
        overlap = sum(1 for t in content if t in ctx)
        return (overlap / len(content)) >= 0.34

    def _compose(self, question: str, contexts: list[str]) -> str:
        best = contexts[0]
        sentences = [s.strip() for s in best.replace("\n", " ").split(".") if s.strip()]
        q_words = {w.lower() for w in question.split() if len(w) > 3}
        ranked = sorted(
            sentences,
            key=lambda s: sum(1 for w in q_words if w in s.lower()),
            reverse=True,
        )
        picked = ranked[:2] if ranked else [best[:220]]
        return ". ".join(picked).strip() + "."
