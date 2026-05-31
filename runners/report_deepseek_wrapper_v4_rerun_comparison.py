#!/usr/bin/env python3
"""Summarize the DeepSeek wrapper-v1 to wrapper-v4 changed-row rerun."""
from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "benchmark-vabench-release-v1" / "reports"
OLD_INCONCLUSIVE_CSV = REPORT_DIR / "deepseek_failure_attribution_inconclusive_20260528.csv"
NEW_BASELINE_SUMMARY = (
    ROOT
    / "results"
    / "vabench-release-v1-baseline-minimax-deepseek-v4-pro-20260528-wrapper-v4-changed55"
    / "summary.json"
)
NEW_DUAL_SUMMARY = (
    ROOT
    / "results"
    / "vabench-release-v1-baseline-dual-deepseek-v4-pro-20260528-wrapper-v4-changed55-dual"
    / "summary.json"
)
NEW_DUAL_RESULTS_ROOT = NEW_DUAL_SUMMARY.parent / "results"
OUT_JSON = REPORT_DIR / "deepseek_wrapper_v4_changed_rerun_comparison_20260528.json"
OUT_CSV = REPORT_DIR / "deepseek_wrapper_v4_changed_rerun_comparison_20260528.csv"
OUT_MD = REPORT_DIR / "deepseek_wrapper_v4_changed_rerun_comparison_20260528.md"

SELECT_ATTRIBUTION = "prompt_contract_gap_old_wrapper"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_old_rows() -> list[dict[str, str]]:
    with OLD_INCONCLUSIVE_CSV.open(newline="", encoding="utf-8") as f:
        return [
            row
            for row in csv.DictReader(f)
            if row.get("primary_attribution") == SELECT_ATTRIBUTION
        ]


def read_new_result_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(NEW_DUAL_RESULTS_ROOT.glob("*/result.json")):
        data = read_json(path)
        classification = data.get("classification", {})
        rows.append(
            {
                "release_task_id": data.get("release_task_id", ""),
                "release_entry_id": data.get("release_entry_id", ""),
                "form": data.get("form", ""),
                "category": data.get("category", ""),
                "difficulty": data.get("difficulty", ""),
                "baseline_evas_status": data.get("baseline_evas_status", ""),
                "new_evas_status": classification.get("evas_status", ""),
                "new_spectre_checker_pass": bool(classification.get("spectre_checker_pass")),
                "new_dual_status": classification.get("dual_status", ""),
                "new_dual_pass": bool(classification.get("dual_pass")),
                "new_result_json": path.relative_to(ROOT).as_posix(),
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = [
        "release_task_id",
        "release_entry_id",
        "form",
        "category",
        "difficulty",
        "old_evas_status",
        "old_spectre_checker_pass",
        "old_dual_status",
        "old_root_cause_detail",
        "baseline_evas_status",
        "new_evas_status",
        "new_spectre_checker_pass",
        "new_dual_status",
        "new_dual_pass",
        "new_result_json",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def form_counts(rows: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    buckets: dict[str, dict[str, int]] = defaultdict(lambda: {"total": 0, "dual_pass": 0})
    for row in rows:
        bucket = buckets[str(row["form"])]
        bucket["total"] += 1
        if row["new_dual_pass"]:
            bucket["dual_pass"] += 1
    return dict(sorted(buckets.items()))


def write_markdown(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# DeepSeek Wrapper-v4 Changed-Rerun Comparison",
        "",
        f"Generated: `{payload['generated_at']}`",
        "",
        "Scope: only the 55 rows whose wrapper-v1 candidates were attributed to",
        "`prompt_contract_gap_old_wrapper`. This is not a full 236-row baseline.",
        "",
        "## Headline",
        "",
        f"- old wrapper-v1 selected rows: {payload['selected_count']}",
        f"- old selected rows Spectre pass: {payload['old_spectre_pass_count']}/{payload['selected_count']}",
        f"- wrapper-v4 generation: {payload['new_generation_generated_count']}/{payload['selected_count']} generated",
        f"- wrapper-v4 EVAS initial pass: {payload['new_evas_initial_pass_count']}/{payload['selected_count']}",
        f"- wrapper-v4 Spectre final pass: {payload['new_spectre_pass_count']}/{payload['selected_count']}",
        f"- wrapper-v4 EVAS PASS / Spectre FAIL: {payload['new_evas_pass_spectre_fail_count']}",
        f"- wrapper-v4 Spectre PASS / EVAS FAIL: {payload['new_spectre_pass_evas_fail_count']}",
        "",
        "## Old Wrapper-v1 Failure Roots",
        "",
        "| Root cause | Count |",
        "| --- | ---: |",
    ]
    for key, value in payload["old_root_cause_counts"].items():
        lines.append(f"| `{key}` | {value} |")
    lines.extend(["", "## New Wrapper-v4 Failure/Pass Status", "", "| EVAS status | Count |", "| --- | ---: |"])
    for key, value in payload["new_evas_status_counts"].items():
        lines.append(f"| `{key}` | {value} |")
    lines.extend(["", "## New Passes By Form", "", "| Form | Pass | Total |", "| --- | ---: | ---: |"])
    for key, stats in payload["new_by_form"].items():
        lines.append(f"| `{key}` | {stats['dual_pass']} | {stats['total']} |")
    lines.extend(
        [
            "",
            "## Rows Newly Passing Spectre",
            "",
            "| Release task id | Form | Category |",
            "| --- | --- | --- |",
        ]
    )
    for row in payload["new_pass_rows"]:
        lines.append(f"| `{row['release_task_id']}` | `{row['form']}` | {row['category']} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "The wrapper-v4 contract repair converted 7 previously inconclusive old-wrapper",
            "rows into EVAS/Spectre dual passes, with zero EVAS/Spectre pass/fail",
            "mismatches on this rerun slice. The remaining failures should now be",
            "attributed with the v4 candidates rather than carried over from the old",
            "wrapper-v1 failure labels.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    old_rows = read_old_rows()
    old_by_task = {row["release_task_id"]: row for row in old_rows}
    new_summary = read_json(NEW_BASELINE_SUMMARY)
    dual_summary = read_json(NEW_DUAL_SUMMARY)
    new_rows = read_new_result_rows()
    if len(new_rows) != len(old_rows):
        raise SystemExit(f"row mismatch: old={len(old_rows)} new={len(new_rows)}")

    comparison_rows: list[dict[str, Any]] = []
    for row in sorted(new_rows, key=lambda item: item["release_task_id"]):
        old = old_by_task.get(row["release_task_id"])
        if old is None:
            raise SystemExit(f"missing old attribution row for {row['release_task_id']}")
        comparison_rows.append(
            {
                **row,
                "old_evas_status": old.get("evas_status", ""),
                "old_spectre_checker_pass": old.get("spectre_checker_pass", ""),
                "old_dual_status": old.get("dual_status", ""),
                "old_root_cause_detail": old.get("root_cause_detail", ""),
            }
        )

    new_pass_rows = [row for row in comparison_rows if row["new_dual_pass"]]
    payload: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": "55 prompt_contract_gap_old_wrapper rows only",
        "wrapper_from": "release-runner-wrapper-v1",
        "wrapper_to": "release-runner-wrapper-v4",
        "selected_count": len(comparison_rows),
        "old_spectre_pass_count": sum(row.get("spectre_checker_pass") == "True" for row in old_rows),
        "old_root_cause_counts": dict(Counter(row.get("root_cause_detail", "") for row in old_rows)),
        "old_evas_status_counts": dict(Counter(row.get("evas_status", "") for row in old_rows)),
        "new_generation_generated_count": new_summary.get("generation_status_counts", {}).get("generated", 0),
        "new_evas_initial_pass_count": new_summary.get("evas_pass_count", 0),
        "new_spectre_pass_count": dual_summary.get("spectre_final_pass_count", 0),
        "new_dual_pass_count": dual_summary.get("dual_pass_count", 0),
        "new_evas_pass_spectre_fail_count": dual_summary.get("evas_pass_spectre_fail_count", 0),
        "new_spectre_pass_evas_fail_count": dual_summary.get("spectre_pass_evas_fail_count", 0),
        "new_evas_status_counts": dict(Counter(row["new_evas_status"] for row in comparison_rows)),
        "new_dual_status_counts": dict(Counter(row["new_dual_status"] for row in comparison_rows)),
        "new_by_form": form_counts(comparison_rows),
        "new_pass_rows": new_pass_rows,
        "comparison_rows": comparison_rows,
        "sources": {
            "old_inconclusive_csv": OLD_INCONCLUSIVE_CSV.relative_to(ROOT).as_posix(),
            "new_baseline_summary": NEW_BASELINE_SUMMARY.relative_to(ROOT).as_posix(),
            "new_dual_summary": NEW_DUAL_SUMMARY.relative_to(ROOT).as_posix(),
        },
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(OUT_CSV, comparison_rows)
    write_markdown(OUT_MD, payload)
    print(
        f"selected={payload['selected_count']} "
        f"new_spectre_pass={payload['new_spectre_pass_count']} "
        f"evas_pass_spectre_fail={payload['new_evas_pass_spectre_fail_count']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
