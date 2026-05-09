#!/usr/bin/env python3
"""Audit vaBench benchmark integrity beyond simulator pass/fail.

This gate checks benchmark design risks that EVAS/Spectre success cannot catch:
missing task forms, hidden task-id routing, checker/gold leakage in prompts,
heldout contamination, and source identity leaks inside current benchmark
checkers.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BENCH = ROOT / "benchmark-vabench-main-v1"
FORMS = {"bugfix", "spec-to-va", "end-to-end", "tb-generation"}
HELDOUT_PACKS = {
    "folding_adc_encoder",
    "pwm_modulator",
    "phase_frequency_lock_monitor",
    "adaptive_threshold_tracker",
    "windowed_rms_detector",
    "charge_pump_behavior",
    "sigma_delta_modulator_1st",
    "glitch_filter",
    "quadrature_phase_detector",
    "sample_rate_converter_stub",
    "temperature_sensor_lut",
    "noise_source_stat_tb",
}
CHECKER_FORBIDDEN = {
    "source_task_id": "checker should not route through historical source_task_id",
    "evaluate_behavior(": "checker should not delegate to source-task behavior registry",
    "simulate_evas import evaluate_behavior": "checker should not import source-task behavior registry",
}
PROMPT_FORBIDDEN_RE = [
    (re.compile(r"\bchecker\.py\b", re.I), "prompt_mentions_checker_file"),
    (re.compile(r"\bgold/", re.I), "prompt_mentions_gold_path"),
    (re.compile(r"\bsource_task_id\b", re.I), "prompt_mentions_source_task_id"),
]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def add(issues: list[dict[str, str]], severity: str, code: str, detail: str) -> None:
    issues.append({"severity": severity, "code": code, "detail": detail})


def audit(bench: Path) -> dict[str, Any]:
    tasks_dir = bench / "tasks"
    task_dirs = sorted(p for p in tasks_dir.iterdir() if (p / "meta.json").is_file())
    issues: list[dict[str, str]] = []
    packs: dict[str, list[dict[str, Any]]] = defaultdict(list)
    task_rows: list[dict[str, Any]] = []

    manifest = read_json(bench / "manifest.json") if (bench / "manifest.json").is_file() else {}
    manifest_task_count = manifest.get("task_count")
    if manifest_task_count is not None and manifest_task_count != len(task_dirs):
        add(issues, "FAIL", "manifest_task_count_mismatch", f"manifest={manifest_task_count} actual={len(task_dirs)}")

    for task_dir in task_dirs:
        meta = read_json(task_dir / "meta.json")
        task_id = meta.get("task_id", task_dir.name)
        pack_id = meta.get("pack_id") or meta.get("circuit_function_id") or "UNKNOWN"
        form = meta.get("task_form") or meta.get("family") or "UNKNOWN"
        packs[pack_id].append({"task_id": task_id, "form": form})
        row_issues: list[dict[str, str]] = []

        if task_id != task_dir.name:
            add(row_issues, "FAIL", "task_dir_meta_id_mismatch", f"dir={task_dir.name} meta={task_id}")
        if form not in FORMS:
            add(row_issues, "FAIL", "unknown_task_form", str(form))
        if pack_id in HELDOUT_PACKS:
            add(row_issues, "FAIL", "heldout_pack_in_main", pack_id)

        prompt = read_text(task_dir / "prompt.md") if (task_dir / "prompt.md").is_file() else ""
        checker = read_text(task_dir / "checker.py") if (task_dir / "checker.py").is_file() else ""
        for needle, detail in CHECKER_FORBIDDEN.items():
            if needle in checker:
                add(row_issues, "FAIL", "hidden_source_checker_routing", detail)
        for pattern, code in PROMPT_FORBIDDEN_RE:
            if pattern.search(prompt):
                add(row_issues, "FAIL", code, pattern.pattern)

        gold_dir = task_dir / "gold"
        if not gold_dir.is_dir():
            add(row_issues, "FAIL", "missing_gold_dir", str(gold_dir))
        else:
            va_count = len(list(gold_dir.glob("*.va")))
            tb_count = len(list(gold_dir.glob("*.scs")))
            if va_count < 1:
                add(row_issues, "FAIL", "missing_gold_va", task_id)
            if tb_count < 1:
                add(row_issues, "FAIL", "missing_gold_tb", task_id)

        scoring = meta.get("scoring", [])
        if form != "tb-generation" and "dut_compile" not in scoring:
            add(row_issues, "FAIL", "missing_dut_compile_axis", repr(scoring))
        if "tb_compile" not in scoring:
            add(row_issues, "FAIL", "missing_tb_compile_axis", repr(scoring))
        if "sim_correct" not in scoring:
            add(row_issues, "WARN", "sim_correct_not_scored", repr(scoring))

        status = "FAIL" if any(i["severity"] == "FAIL" for i in row_issues) else "WARN" if row_issues else "PASS"
        task_rows.append({"task_id": task_id, "pack_id": pack_id, "form": form, "status": status, "issues": row_issues})
        issues.extend({**i, "task_id": task_id, "pack_id": pack_id} for i in row_issues)

    for pack_id, rows in sorted(packs.items()):
        forms = {row["form"] for row in rows}
        missing = sorted(FORMS - forms)
        extra = sorted(forms - FORMS)
        if missing:
            add(issues, "FAIL", "pack_missing_forms", f"{pack_id}: {missing}")
        if extra:
            add(issues, "FAIL", "pack_unknown_forms", f"{pack_id}: {extra}")
        if len(rows) != 4:
            add(issues, "FAIL", "pack_not_four_tasks", f"{pack_id}: {len(rows)}")

    status_counts = Counter(row["status"] for row in task_rows)
    issue_counts = Counter(issue["code"] for issue in issues)
    overall = "FAIL" if any(i["severity"] == "FAIL" for i in issues) else "WARN" if issues else "PASS"
    return {
        "benchmark": str(bench),
        "task_count": len(task_dirs),
        "pack_count": len(packs),
        "overall": overall,
        "status_counts": dict(status_counts),
        "issue_counts": dict(issue_counts),
        "issues": issues,
        "tasks": task_rows,
        "packs": {pack: sorted(row["form"] for row in rows) for pack, rows in sorted(packs.items())},
    }


def write_md(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# vaBench Benchmark Integrity Audit",
        "",
        "**Date**: 2026-05-08",
        "",
        f"Overall: **{report['overall']}**",
        "",
        "## Summary",
        "",
        f"- Packs: `{report['pack_count']}`",
        f"- Tasks: `{report['task_count']}`",
        f"- Task status: `{report['status_counts']}`",
        f"- Issue counts: `{report['issue_counts']}`",
        "",
        "## Task Findings",
        "",
        "| Status | Task | Pack | Form | Issues |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in report["tasks"]:
        issues = "<br>".join(f"{i['severity']}:{i['code']}={i['detail']}" for i in row["issues"]) or "none"
        lines.append(f"| {row['status']} | `{row['task_id']}` | `{row['pack_id']}` | `{row['form']}` | {issues} |")
    lines.extend(["", "## Pack Forms", "", "| Pack | Forms |", "| --- | --- |"])
    for pack, forms in report["packs"].items():
        lines.append(f"| `{pack}` | `{', '.join(forms)}` |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--bench-dir", type=Path, default=DEFAULT_BENCH)
    ap.add_argument("--output-dir", type=Path, default=ROOT / "analysis")
    args = ap.parse_args()
    bench = args.bench_dir if args.bench_dir.is_absolute() else ROOT / args.bench_dir
    out = args.output_dir if args.output_dir.is_absolute() else ROOT / args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    report = audit(bench)
    stem = bench.name.replace("benchmark-", "") + "_integrity_audit_20260508"
    json_path = out / f"{stem}.json"
    md_path = out / f"{stem}.md"
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_md(md_path, report)
    print(json.dumps({"overall": report["overall"], "task_count": report["task_count"], "pack_count": report["pack_count"], "issue_counts": report["issue_counts"]}, indent=2))
    print(f"json={json_path.relative_to(ROOT)}")
    print(f"md={md_path.relative_to(ROOT)}")
    return 1 if report["overall"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
