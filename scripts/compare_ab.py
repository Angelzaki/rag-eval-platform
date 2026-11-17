from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rich.console import Console
from rich.table import Table

from rag_eval.runner import run_evaluation

console = Console()


def main() -> int:
    gt = ROOT / "samples" / "ground_truth" / "questions.jsonl"
    results = ROOT / "results"

    a, _ = run_evaluation(ROOT / "samples" / "docs_a", gt, "scenario_a", results_dir=results)
    b, _ = run_evaluation(ROOT / "samples" / "docs_b", gt, "scenario_b", results_dir=results)

    table = Table(title="Comparación A/B")
    table.add_column("suite")
    table.add_column("A", justify="right")
    table.add_column("B", justify="right")
    table.add_column("delta", justify="right")

    by_a = {s.name: s.score for s in a.suites}
    by_b = {s.name: s.score for s in b.suites}
    for name in by_a:
        delta = by_b[name] - by_a[name]
        table.add_row(name, f"{by_a[name]:.0%}", f"{by_b[name]:.0%}", f"{delta:+.0%}")

    console.print(table)
    console.print(f"overall A={a.overall:.0%}  B={b.overall:.0%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
