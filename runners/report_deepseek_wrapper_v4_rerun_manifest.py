#!/usr/bin/env python3
"""Build the minimal DeepSeek wrapper-v4 rerun queue.

The full wrapper-v1 run has rows that are inconclusive because the public prompt
plus old runner wrapper did not state shared simulator contracts clearly enough.
This report selects only those rows for regeneration under wrapper-v4. Other
inconclusive rows are kept in a skipped section because they need runner or
evaluator fixes rather than a prompt-wrapper rerun.
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "benchmark-vabench-release-v1" / "reports"
INPUT_CSV = REPORT_DIR / "deepseek_failure_attribution_inconclusive_20260528.csv"
OUT_JSON = REPORT_DIR / "deepseek_wrapper_v4_changed_rerun_manifest_20260528.json"
OUT_CSV = REPORT_DIR / "deepseek_wrapper_v4_changed_rerun_manifest_20260528.csv"
OUT_MD = REPORT_DIR / "deepseek_wrapper_v4_changed_rerun_manifest_20260528.md"
OUT_TASK_IDS = REPORT_DIR / "deepseek_wrapper_v4_changed_rerun_task_ids_20260528.txt"

SELECT_ATTRIBUTION = "prompt_contract_gap_old_wrapper"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def compact_row(row: dict[str, str]) -> dict[str, str]:
    keys = [
        "release_task_id",
        "release_entry_id",
        "form",
        "level",
        "difficulty",
        "track",
        "category",
        "base_function",
        "primary_attribution",
        "root_cause_family",
        "root_cause_detail",
        "evidence",
        "recommended_action",
    ]
    return {key: row.get(key, "") for key in keys}


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = [
        "release_task_id",
        "release_entry_id",
        "form",
        "level",
        "difficulty",
        "track",
        "category",
        "base_function",
        "primary_attribution",
        "root_cause_family",
        "root_cause_detail",
        "evidence",
        "recommended_action",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, payload: dict[str, Any]) -> None:
    selected = payload["selected_rows"]
    skipped = payload["skipped_rows"]
    lines = [
        "# DeepSeek Wrapper-v4 Changed Rerun Manifest",
        "",
        f"Generated: `{payload['generated_at']}`",
        "",
        "This is a minimal rerun queue. It includes only rows whose old wrapper-v1",
        "candidate failure was attributed to missing shared prompt-wrapper contract",
        "rules. It does not request a full 236-row baseline rerun.",
        "",
        "## Summary",
        "",
        f"- selected for wrapper-v4 regeneration: {payload['selected_count']}",
        f"- skipped inconclusive rows: {payload['skipped_count']}",
        f"- task-id file: `{payload['task_id_file']}`",
        "",
        "## Selected Root Causes",
        "",
        "| Root cause | Count |",
        "| --- | ---: |",
    ]
    for key, value in payload["selected_root_cause_counts"].items():
        lines.append(f"| `{key}` | {value} |")
    lines.extend(
        [
            "",
            "## Skipped Inconclusive Rows",
            "",
            "| Attribution | Count | Reason |",
            "| --- | ---: | --- |",
        ]
    )
    skipped_counts = Counter(row["primary_attribution"] for row in skipped)
    skipped_reasons = {
        "runner_infra_extraction": "needs extraction/max-token runner handling, not a wrapper-contract rerun",
        "evaluator_runner_review": "needs evaluator or checker triage before being counted as model evidence",
    }
    for key, value in sorted(skipped_counts.items()):
        reason = skipped_reasons.get(key, "not selected by wrapper-v4 contract criterion")
        lines.append(f"| `{key}` | {value} | {reason} |")
    lines.extend(
        [
            "",
            "## Selected Rows",
            "",
            "| Release task id | Form | Level | Category | Root cause | Evidence |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in selected:
        lines.append(
            "| `{release_task_id}` | `{form}` | `{level}` | {category} | `{root_cause_detail}` | {evidence} |".format(
                **row
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    rows = read_rows(INPUT_CSV)
    selected = [compact_row(row) for row in rows if row.get("primary_attribution") == SELECT_ATTRIBUTION]
    skipped = [compact_row(row) for row in rows if row.get("primary_attribution") != SELECT_ATTRIBUTION]
    task_ids = sorted({row["release_task_id"] for row in selected if row["release_task_id"]})
    if len(task_ids) != len(selected):
        raise SystemExit("Selected rows must map one-to-one to release_task_id values.")

    payload: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_csv": INPUT_CSV.relative_to(ROOT).as_posix(),
        "selection_rule": {
            "primary_attribution": SELECT_ATTRIBUTION,
            "description": "Rows whose wrapper-v1 candidates failed because shared prompt-wrapper contract rules were missing.",
        },
        "wrapper_from": "release-runner-wrapper-v1",
        "wrapper_to": "release-runner-wrapper-v4",
        "full_denominator_rows": 236,
        "inconclusive_source_rows": len(rows),
        "selected_count": len(selected),
        "skipped_count": len(skipped),
        "task_id_file": OUT_TASK_IDS.relative_to(ROOT).as_posix(),
        "selected_root_cause_counts": dict(Counter(row["root_cause_detail"] for row in selected)),
        "skipped_attribution_counts": dict(Counter(row["primary_attribution"] for row in skipped)),
        "selected_rows": selected,
        "skipped_rows": skipped,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(OUT_CSV, selected)
    OUT_TASK_IDS.write_text("\n".join(task_ids) + "\n", encoding="utf-8")
    write_markdown(OUT_MD, payload)
    print(
        f"selected={len(selected)} skipped={len(skipped)} "
        f"task_ids={OUT_TASK_IDS.relative_to(ROOT).as_posix()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
