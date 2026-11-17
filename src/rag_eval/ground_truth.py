from __future__ import annotations

import json
from pathlib import Path

from rag_eval.models import GroundTruthItem


def load_ground_truth(path: str | Path) -> list[GroundTruthItem]:
    items: list[GroundTruthItem] = []
    with Path(path).open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            raw = json.loads(line)
            items.append(
                GroundTruthItem(
                    id=raw["id"],
                    question=raw["question"],
                    expected_answer=raw["expected_answer"],
                    source_doc=raw["source_doc"],
                    expected_keywords=raw.get("expected_keywords", []),
                    should_abstain=raw.get("should_abstain", False),
                    tags=raw.get("tags", []),
                )
            )
    return items
