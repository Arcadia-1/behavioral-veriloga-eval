#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v3"
REPORTS_ROOT = PACKAGE_ROOT / "reports"
TASKS_JSON = PACKAGE_ROOT / "TASKS.json"
REPORT_JSON = REPORTS_ROOT / "score_support_manifest.json"
REPORT_MD = REPORTS_ROOT / "score_support_manifest.md"
REPORT_CSV = REPORTS_ROOT / "score_support_manifest_tasks.csv"


SUPPORT_CATEGORIES = {
    "measurement",
    "measurement_instrumentation_flows",
    "stimulus",
    "stimulus_source_generators",
    "testbench_utility_modules",
}

CANDIDATE_PROVENANCE_TIERS = {
    "behavior-extension-candidate",
    "bias-reference-power-replacement-candidate",
}


def read_tasks() -> dict[str, dict[str, Any]]:
    return json.loads(TASKS_JSON.read_text(encoding="utf-8"))["tasks"]


def task_number(task_key: str) -> int | None:
    match = re.match(r"^(\d{3})-", task_key)
    return int(match.group(1)) if match else None


def sort_key(task_key: str) -> tuple[int, str]:
    number = task_number(task_key)
    return (number if number is not None else 10_000, task_key)


def score_role_for(task_key: str, task: dict[str, Any]) -> tuple[str, bool, str]:
    number = task_number(task_key)
    tier = str(task.get("tier") or "<none>")
    category = str(task.get("category") or "")
    if number is not None and number <= 300:
        if category in SUPPORT_CATEGORIES:
            return (
                "support",
                False,
                "v3_support_category_excluded_from_core_score",
            )
        return ("scored_benchmark", True, "")
    if tier in CANDIDATE_PROVENANCE_TIERS or number is None:
        return (
            "candidate_provenance",
            False,
            "outside_current_v3_score_slots_until_explicit_promotion",
        )
    return (
        "language_extension",
        False,
        "language_or_semantics_extension_excluded_from_core_score",
    )


def build_rows(tasks: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for task_key in sorted(tasks, key=sort_key):
        task = tasks[task_key]
        role, counted, exclusion_reason = score_role_for(task_key, task)
        number = task_number(task_key)
        rows.append({
            "task_key": task_key,
            "task_number": number if number is not None else "",
            "task_id": task.get("id", ""),
            "title": task.get("title", ""),
            "level": task.get("level", ""),
            "form": task.get("form", ""),
            "difficulty": task.get("difficulty", ""),
            "category": task.get("category", ""),
            "tier": task.get("tier") or "<none>",
            "score_role": role,
            "counted_in_core_score": counted,
            "support_suite": role == "support",
            "exclusion_reason": exclusion_reason,
            "target": ";".join(task.get("target", [])),
        })
    return rows


def count_by(rows: list[dict[str, Any]], field: str) -> dict[str, int]:
    return dict(sorted(Counter(str(row[field]) for row in rows).items()))


def nested_count_by(rows: list[dict[str, Any]], outer: str, inner: str) -> dict[str, dict[str, int]]:
    buckets: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        buckets[str(row[outer])][str(row[inner])] += 1
    return {
        key: dict(sorted(counter.items()))
        for key, counter in sorted(buckets.items())
    }


def build_report() -> dict[str, Any]:
    tasks = read_tasks()
    rows = build_rows(tasks)
    role_counts = count_by(rows, "score_role")
    numbered = [row for row in rows if row["task_number"] != ""]
    original_rows = [
        row for row in rows
        if row["task_number"] != "" and int(row["task_number"]) <= 300
    ]
    extension_rows = [
        row for row in rows
        if row["task_number"] != "" and int(row["task_number"]) > 300
    ]
    unnumbered_rows = [row for row in rows if row["task_number"] == ""]
    summary = {
        "total_tasks": len(rows),
        "numbered_tasks": len(numbered),
        "unnumbered_candidates": len(unnumbered_rows),
        "original_001_300_tasks": len(original_rows),
        "extension_301_plus_tasks": len(extension_rows),
        "scored_benchmark_tasks": role_counts.get("scored_benchmark", 0),
        "support_tasks": role_counts.get("support", 0),
        "language_extension_tasks": role_counts.get("language_extension", 0),
        "candidate_provenance_tasks": role_counts.get("candidate_provenance", 0),
        "score_role_counts": role_counts,
        "score_role_by_category": nested_count_by(rows, "score_role", "category"),
        "score_role_by_level": nested_count_by(rows, "score_role", "level"),
    }
    return {
        "date": date.today().isoformat(),
        "release": "benchmark-vabench-release-v3",
        "status": "v3_score_support_manifest_current_after_issue109_backfills",
        "summary": summary,
        "policy": {
            "source_of_truth": "benchmark-vabench-release-v3/reports/score_support_manifest.json",
            "historical_denominators": "v1/v1.1 entry-form score denominators are provenance only and are not used to score the current v3 task tree.",
            "scored_benchmark_rule": "Count current v3 tasks 001-300 except measurement/stimulus/testbench utility support categories.",
            "support_rule": "Current v3 tasks 001-300 in measurement, stimulus, or testbench utility categories are certified support assets and excluded from the core score.",
            "language_extension_rule": "Current numbered tasks above 300 are language/semantics extension rows unless explicitly promoted into a future score policy.",
            "candidate_provenance_rule": "Unnumbered candidates and numbered behavior-extension candidates outside 001-300 are preserved as provenance/candidate material and excluded from the current core score.",
        },
        "task_rows": rows,
    }


def write_csv(rows: list[dict[str, Any]]) -> None:
    fields = [
        "task_key",
        "task_number",
        "task_id",
        "title",
        "level",
        "form",
        "difficulty",
        "category",
        "tier",
        "score_role",
        "counted_in_core_score",
        "support_suite",
        "exclusion_reason",
        "target",
    ]
    with REPORT_CSV.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_md(report: dict[str, Any]) -> None:
    summary = report["summary"]
    support_rows = [
        row for row in report["task_rows"]
        if row["score_role"] == "support"
    ]
    lines = [
        "# vaBench v3 Score/Support Manifest",
        "",
        f"Date: {report['date']}",
        "",
        "## Summary",
        "",
        f"- Total active v3 tasks: **{summary['total_tasks']}**",
        f"- Numbered active tasks: **{summary['numbered_tasks']}**",
        f"- Unnumbered candidates: **{summary['unnumbered_candidates']}**",
        f"- Current scored benchmark tasks: **{summary['scored_benchmark_tasks']}**",
        f"- Current support tasks: **{summary['support_tasks']}**",
        f"- Non-scored language-extension tasks: **{summary['language_extension_tasks']}**",
        f"- Non-scored candidate/provenance tasks: **{summary['candidate_provenance_tasks']}**",
        "",
        "## Policy",
        "",
    ]
    for key, value in report["policy"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend([
        "",
        "## Score Roles",
        "",
        "| Score role | Tasks | Score status |",
        "| --- | ---: | --- |",
        f"| `scored_benchmark` | {summary['scored_benchmark_tasks']} | Counted in the current v3 core score. |",
        f"| `support` | {summary['support_tasks']} | Certified/reviewed separately; excluded from the core score. |",
        f"| `language_extension` | {summary['language_extension_tasks']} | Non-scored Verilog-A language/semantics extension coverage. |",
        f"| `candidate_provenance` | {summary['candidate_provenance_tasks']} | Non-scored candidate/provenance material pending explicit promotion. |",
        "",
        "## Support Tasks",
        "",
        "| Task | Category | Level | Title |",
        "| --- | --- | --- | --- |",
    ])
    for row in support_rows:
        lines.append(
            f"| `{row['task_key']}` | `{row['category']}` | `{row['level']}` | {row['title']} |"
        )
    lines.extend([
        "",
        "## Category Counts By Score Role",
        "",
    ])
    for role, counts in summary["score_role_by_category"].items():
        lines.extend([
            f"### `{role}`",
            "",
            "| Category | Tasks |",
            "| --- | ---: |",
        ])
        for category, count in counts.items():
            lines.append(f"| `{category}` | {count} |")
        lines.append("")
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    report = build_report()
    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_csv(report["task_rows"])
    write_md(report)
    print(f"wrote {REPORT_JSON.relative_to(ROOT)}")
    print(f"wrote {REPORT_CSV.relative_to(ROOT)}")
    print(f"wrote {REPORT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
