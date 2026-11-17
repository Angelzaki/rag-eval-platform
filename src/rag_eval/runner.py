from __future__ import annotations

import json
from pathlib import Path

from rag_eval.answerer import HeuristicAnswerer
from rag_eval.baseline import compare_to_baseline, load_baseline, save_baseline
from rag_eval.chunk import chunk_corpus
from rag_eval.extract import load_corpus
from rag_eval.ground_truth import load_ground_truth
from rag_eval.models import EvalReport
from rag_eval.report import to_dict, write_html, write_json, write_markdown
from rag_eval.retrieve import LocalRetriever
from rag_eval.suites import ALL_SUITES


def build_context(docs_dir: Path, gt_path: Path, scenario: str) -> dict:
    docs = load_corpus(docs_dir)
    chunks = chunk_corpus(docs)
    retriever = LocalRetriever(chunks)
    answerer = HeuristicAnswerer(retriever)
    ground_truth = load_ground_truth(gt_path)
    return {
        "scenario": scenario,
        "docs_dir": docs_dir,
        "docs": docs,
        "chunks": chunks,
        "retriever": retriever,
        "answerer": answerer,
        "ground_truth": ground_truth,
    }


def run_evaluation(
    docs_dir: str | Path,
    gt_path: str | Path,
    scenario: str = "baseline",
    suites: list[str] | None = None,
    results_dir: str | Path | None = None,
    save_as_baseline: bool = False,
    baseline_path: str | Path | None = None,
) -> tuple[EvalReport, dict | None]:
    ctx = build_context(Path(docs_dir), Path(gt_path), scenario)
    selected = suites or list(ALL_SUITES.keys())
    results = []
    for name in selected:
        if name not in ALL_SUITES:
            raise ValueError(f"suite desconocida: {name}")
        results.append(ALL_SUITES[name](ctx))

    report = EvalReport(
        scenario=scenario,
        suites=results,
        meta={
            "docs": len(ctx["docs"]),
            "chunks": len(ctx["chunks"]),
            "ground_truth": len(ctx["ground_truth"]),
            "suites": selected,
        },
    )

    regression = None
    payload = to_dict(report)

    if results_dir:
        out = Path(results_dir)
        stamp = scenario.replace(" ", "_")
        base_file = Path(baseline_path) if baseline_path else out / "baseline.json"
        if save_as_baseline:
            save_baseline(payload, base_file)
        previous = load_baseline(base_file)
        if previous and not save_as_baseline:
            regression = compare_to_baseline(payload, previous)
            (out / f"{stamp}_regression.json").write_text(
                json.dumps(regression, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        write_json(report, out / f"{stamp}.json")
        write_markdown(report, out / f"{stamp}.md")
        write_html(report, out / f"{stamp}.html", regression=regression)

    return report, regression
