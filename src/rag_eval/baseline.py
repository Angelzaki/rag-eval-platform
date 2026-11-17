from __future__ import annotations

import json
from pathlib import Path


def save_baseline(report_dict: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report_dict, ensure_ascii=False, indent=2), encoding="utf-8")


def load_baseline(path: Path) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def compare_to_baseline(current: dict, baseline: dict) -> dict:
    cur_suites = {s["name"]: s["score"] for s in current.get("suites", [])}
    base_suites = {s["name"]: s["score"] for s in baseline.get("suites", [])}
    deltas = []
    regressions = []
    for name, score in cur_suites.items():
        prev = base_suites.get(name)
        if prev is None:
            continue
        delta = round(score - prev, 4)
        item = {"suite": name, "baseline": prev, "current": score, "delta": delta}
        deltas.append(item)
        if delta < -0.05:
            regressions.append(item)
    return {
        "overall_baseline": baseline.get("overall"),
        "overall_current": current.get("overall"),
        "overall_delta": round(current.get("overall", 0) - baseline.get("overall", 0), 4),
        "suites": deltas,
        "regressions": regressions,
        "ok": len(regressions) == 0,
    }
