from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class GroundTruthItem:
    id: str
    question: str
    expected_answer: str
    source_doc: str
    expected_keywords: list[str] = field(default_factory=list)
    should_abstain: bool = False
    tags: list[str] = field(default_factory=list)


@dataclass
class Document:
    doc_id: str
    path: str
    text: str


@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    text: str
    start: int
    end: int


@dataclass
class RetrievedChunk:
    chunk: Chunk
    score: float


@dataclass
class RagAnswer:
    question: str
    answer: str
    citations: list[str] = field(default_factory=list)
    retrieved: list[RetrievedChunk] = field(default_factory=list)
    abstained: bool = False


@dataclass
class SuiteResult:
    name: str
    passed: int
    failed: int
    details: list[dict[str, Any]] = field(default_factory=list)

    @property
    def total(self) -> int:
        return self.passed + self.failed

    @property
    def score(self) -> float:
        return self.passed / self.total if self.total else 0.0


@dataclass
class EvalReport:
    scenario: str
    suites: list[SuiteResult]
    meta: dict[str, Any] = field(default_factory=dict)

    @property
    def overall(self) -> float:
        totals = [(s.passed, s.total) for s in self.suites]
        p = sum(x[0] for x in totals)
        t = sum(x[1] for x in totals)
        return p / t if t else 0.0
