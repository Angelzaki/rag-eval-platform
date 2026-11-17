from pathlib import Path

from rag_eval.answerer import HeuristicAnswerer
from rag_eval.chunk import chunk_corpus
from rag_eval.extract import load_corpus
from rag_eval.ground_truth import load_ground_truth
from rag_eval.retrieve import LocalRetriever
from rag_eval.runner import run_evaluation

ROOT = Path(__file__).resolve().parents[1]
DOCS_A = ROOT / "samples" / "docs_a"
GT = ROOT / "samples" / "ground_truth" / "questions.jsonl"


def test_load_ground_truth():
    items = load_ground_truth(GT)
    assert len(items) >= 5
    assert any(i.should_abstain for i in items)


def test_retrieval_hits_source():
    docs = load_corpus(DOCS_A)
    chunks = chunk_corpus(docs)
    retriever = LocalRetriever(chunks)
    hits = retriever.search("descuento máximo A1", k=3)
    assert hits
    assert any(h.chunk.doc_id == "politica_a1" for h in hits)


def test_abstention_on_unknown():
    docs = load_corpus(DOCS_A)
    answerer = HeuristicAnswerer(LocalRetriever(chunk_corpus(docs)))
    result = answerer.ask("política de viajes interplanetarios 2099")
    assert result.abstained


def test_full_eval_baseline(tmp_path):
    report, regression = run_evaluation(
        docs_dir=DOCS_A,
        gt_path=GT,
        scenario="scenario_a",
        results_dir=tmp_path,
        save_as_baseline=True,
        baseline_path=tmp_path / "baseline.json",
    )
    assert report.meta["docs"] >= 3
    assert report.meta["ground_truth"] >= 18
    assert report.overall >= 0.5
    assert (tmp_path / "scenario_a.json").exists()
    assert (tmp_path / "scenario_a.md").exists()
    assert (tmp_path / "scenario_a.html").exists()
    assert (tmp_path / "baseline.json").exists()
    assert regression is None

    report2, regression2 = run_evaluation(
        docs_dir=DOCS_A,
        gt_path=GT,
        scenario="scenario_a_rerun",
        results_dir=tmp_path,
        baseline_path=tmp_path / "baseline.json",
    )
    assert report2.overall >= 0.5
    assert regression2 is not None
    assert regression2["ok"] is True
