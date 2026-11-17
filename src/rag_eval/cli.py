from __future__ import annotations

import argparse
from pathlib import Path

from rich.console import Console
from rich.table import Table

from rag_eval.runner import run_evaluation
from rag_eval.suites import ALL_SUITES

console = Console()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="rag-eval", description="Evaluación local de pipelines RAG")
    parser.add_argument("--docs", default="samples/docs_a", help="carpeta de documentos")
    parser.add_argument("--gt", default="samples/ground_truth/questions.jsonl", help="ground truth jsonl")
    parser.add_argument("--scenario", default="baseline", help="nombre del escenario A/B")
    parser.add_argument("--results", default="results", help="carpeta de reportes")
    parser.add_argument("--save-baseline", action="store_true", help="guardar run como baseline")
    parser.add_argument("--baseline", default="results/baseline.json", help="ruta del baseline")
    parser.add_argument(
        "--suite",
        action="append",
        dest="suites",
        help=f"suite a ejecutar ({', '.join(ALL_SUITES)}). repetible",
    )
    args = parser.parse_args(argv)

    report, regression = run_evaluation(
        docs_dir=Path(args.docs),
        gt_path=Path(args.gt),
        scenario=args.scenario,
        suites=args.suites,
        results_dir=Path(args.results),
        save_as_baseline=args.save_baseline,
        baseline_path=Path(args.baseline),
    )

    table = Table(title=f"RAG Eval · {report.scenario}")
    table.add_column("suite")
    table.add_column("passed", justify="right")
    table.add_column("failed", justify="right")
    table.add_column("score", justify="right")
    for s in report.suites:
        table.add_row(s.name, str(s.passed), str(s.failed), f"{s.score:.0%}")
    console.print(table)
    console.print(f"overall: [bold]{report.overall:.0%}[/bold]")
    console.print(f"gt items: {report.meta.get('ground_truth')}")
    console.print(f"reportes → {args.results}/ (json, md, html)")

    if args.save_baseline:
        console.print(f"baseline guardado → {args.baseline}")
    if regression:
        color = "green" if regression["ok"] else "red"
        console.print(
            f"[{color}]vs baseline: {regression['overall_delta']:+.0%} "
            f"(regressions={len(regression['regressions'])})[/{color}]"
        )

    if regression and not regression["ok"]:
        return 2
    return 0 if report.overall >= 0.5 else 1


if __name__ == "__main__":
    raise SystemExit(main())
