from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from rag_eval.models import EvalReport


def to_dict(report: EvalReport) -> dict:
    return {
        "scenario": report.scenario,
        "overall": round(report.overall, 4),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "meta": report.meta,
        "suites": [
            {
                "name": s.name,
                "passed": s.passed,
                "failed": s.failed,
                "score": round(s.score, 4),
                "details": s.details,
            }
            for s in report.suites
        ],
    }


def write_json(report: EvalReport, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(to_dict(report), ensure_ascii=False, indent=2), encoding="utf-8")


def write_markdown(report: EvalReport, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# RAG Eval — {report.scenario}",
        "",
        f"- overall: **{report.overall:.2%}**",
        f"- generated_at: `{datetime.now(timezone.utc).isoformat()}`",
        "",
        "| suite | passed | failed | score |",
        "|---|---:|---:|---:|",
    ]
    for s in report.suites:
        lines.append(f"| {s.name} | {s.passed} | {s.failed} | {s.score:.2%} |")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_html(report: EvalReport, path: Path, regression: dict | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = "".join(
        f"<tr><td>{s.name}</td><td>{s.passed}</td><td>{s.failed}</td>"
        f"<td>{s.score:.0%}</td></tr>"
        for s in report.suites
    )
    reg_block = ""
    if regression:
        status = "OK" if regression.get("ok") else "REGRESIÓN"
        items = "".join(
            f"<li>{x['suite']}: {x['baseline']:.0%} → {x['current']:.0%} ({x['delta']:+.0%})</li>"
            for x in regression.get("suites", [])
        )
        reg_block = f"<h2>Baseline · {status}</h2><ul>{items}</ul>"
    html = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8"/>
  <title>RAG Eval · {report.scenario}</title>
  <style>
    body {{ font-family: JetBrains Mono, Consolas, monospace; background:#0D1117; color:#E6EDF3; margin:2rem; }}
    h1 {{ color:#A371F7; }}
    table {{ border-collapse: collapse; width: min(720px, 100%); }}
    th, td {{ border:1px solid #30363D; padding:.55rem .7rem; text-align:left; }}
    th {{ background:#161B22; color:#1F6FEB; }}
    .meta {{ color:#8B949E; margin-bottom:1.2rem; }}
    .score {{ color:#3FB950; font-size:1.2rem; }}
  </style>
</head>
<body>
  <h1>rag-eval · {report.scenario}</h1>
  <p class="meta">generated_at: {datetime.now(timezone.utc).isoformat()}</p>
  <p class="score">overall: {report.overall:.0%}</p>
  <table>
    <thead><tr><th>suite</th><th>passed</th><th>failed</th><th>score</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
  {reg_block}
</body>
</html>
"""
    path.write_text(html, encoding="utf-8")
