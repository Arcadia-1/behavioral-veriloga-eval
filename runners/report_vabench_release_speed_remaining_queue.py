#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
TASKS_ROOT = PACKAGE_ROOT / "tasks"
REPORTS_ROOT = PACKAGE_ROOT / "reports"
SCORE_DENOMINATOR_JSON = REPORTS_ROOT / "score_denominator_manifest.json"
REPORT_JSON = REPORTS_ROOT / "speed_remaining_queue.json"
REPORT_CSV = REPORTS_ROOT / "speed_remaining_queue.csv"
REPORT_MD = REPORTS_ROOT / "speed_remaining_queue.md"


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def is_release_speed_summary(path: Path) -> bool:
    name = path.parent.name
    return "full-after-fixes" in name or "speed-remaining" in name


def release_entry(entry_id: str) -> dict[str, object]:
    return read_json(TASKS_ROOT / entry_id / "release_entry.json")


def task_by_form(entry: dict[str, object], form: str) -> dict[str, object]:
    for task in entry.get("release_tasks", []):
        if isinstance(task, dict) and task.get("form") == form:
            return task
    return {}


def timed_scored_keys() -> set[tuple[str, str]]:
    keys: set[tuple[str, str]] = set()
    for path in sorted((ROOT / "results").glob("vabench-release-v1-dual-rerun*/summary.json")):
        if not is_release_speed_summary(path):
            continue
        summary = read_json(path)
        if summary.get("status") != "complete" or summary.get("dry_run") is True:
            continue
        for item in summary.get("results", []):
            if not isinstance(item, dict):
                continue
            raw = item.get("raw_result", {})
            if not isinstance(raw, dict) or raw.get("status") != "PASS":
                continue
            timing = raw.get("timing", {})
            if not isinstance(timing, dict):
                continue
            if "evas_wall_time_s" in timing and "spectre_wall_time_s" in timing:
                keys.add((str(item.get("entry_id", "")), str(item.get("form", ""))))
    return keys


def scored_form_rows() -> list[dict[str, object]]:
    score = read_json(SCORE_DENOMINATOR_JSON)
    rows = score.get("form_rows", [])
    if not isinstance(rows, list):
        return []
    return [
        row
        for row in rows
        if isinstance(row, dict)
        and row.get("counted_in_score") is True
        and row.get("benchmark_score_enabled") is True
    ]


def queue_row(form_row: dict[str, object]) -> dict[str, object]:
    entry_id = str(form_row["release_entry_id"])
    form = str(form_row["form"])
    entry = release_entry(entry_id)
    task = task_by_form(entry, form)
    provenance = task.get("provenance", {})
    if not isinstance(provenance, dict):
        provenance = {}
    release_source_task_id = str(
        provenance.get("source_task_id")
        or task.get("source_task_id")
        or form_row.get("task_id")
        or ""
    )
    historical_source_task_id = str(
        provenance.get("historical_source_task_id")
        or task.get("historical_source_task_id")
        or release_source_task_id
    )
    gold = [str(path) for path in task.get("gold", [])]
    gold_va = [path for path in gold if path.endswith(".va")]
    gold_scs = [path for path in gold if path.endswith(".scs")]
    return {
        "entry_id": entry_id,
        "form": form,
        "level": form_row.get("level", entry.get("level", "")),
        "category": form_row.get("category", entry.get("category", "")),
        "base_function": form_row.get("base_function", entry.get("base_function", "")),
        "source_task_id": release_source_task_id,
        "historical_source_task_id": historical_source_task_id,
        "queue_reason": "missing_scored_speed_timing",
        "static_status": task.get("static_status", form_row.get("static", "missing")),
        "evas_status": task.get("evas_status", form_row.get("evas", "missing")),
        "spectre_status": task.get("spectre_status", form_row.get("spectre", "missing")),
        "gold_va_count": len(gold_va),
        "gold_scs_count": len(gold_scs),
        "gold": gold,
        "evidence": form_row.get("manifest", ""),
        "pending_blockers": [],
        "ready_for_dual_rerun": task.get("static_status") == "pass" and bool(gold),
    }


def build_queue() -> dict[str, object]:
    timed = timed_scored_keys()
    scored_rows = scored_form_rows()
    scored_keys = {
        (str(row.get("release_entry_id", "")), str(row.get("form", "")))
        for row in scored_rows
    }
    timed_scored = timed & scored_keys
    rows = [
        queue_row(row)
        for row in scored_rows
        if (str(row["release_entry_id"]), str(row["form"])) not in timed
    ]
    rows.sort(key=lambda row: (str(row["entry_id"]), str(row["form"])))
    return {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "status": "complete" if not rows else ("ready" if all(row["ready_for_dual_rerun"] for row in rows) else "blocked"),
        "queue_count": len(rows),
        "ready_count": sum(1 for row in rows if row["ready_for_dual_rerun"]),
        "blocked_count": sum(1 for row in rows if not row["ready_for_dual_rerun"]),
        "form_counts": dict(sorted(Counter(str(row["form"]) for row in rows).items())),
        "category_counts": dict(sorted(Counter(str(row["category"]) for row in rows).items())),
        "timed_scored_form_count": len(timed_scored),
        "scored_form_count": len(scored_rows),
        "rows": rows,
        "notes": [
            "This queue is for speed/debug measurement only; it does not change release certification status.",
            "Rows are scored release forms that do not yet have PASS same-slice EVAS/Spectre timing.",
            "Stage this queue with prepare_vabench_release_dual_rerun.py using speed-specific output paths.",
        ],
    }


def write_csv(report: dict[str, object]) -> None:
    fields = [
        "entry_id",
        "form",
        "level",
        "category",
        "base_function",
        "source_task_id",
        "historical_source_task_id",
        "queue_reason",
        "static_status",
        "evas_status",
        "spectre_status",
        "gold_va_count",
        "gold_scs_count",
        "ready_for_dual_rerun",
        "evidence",
    ]
    with REPORT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in report["rows"]:
            writer.writerow({field: row[field] for field in fields})


def write_markdown(report: dict[str, object]) -> None:
    lines = [
        "# vaBench Release Speed Remaining Queue",
        "",
        f"Date: {report['date']}",
        "",
        "This queue contains scored release forms still missing same-slice",
        "EVAS/Spectre timing. It is speed/debug measurement input only.",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| queue rows | {report['queue_count']} |",
        f"| ready rows | {report['ready_count']} |",
        f"| blocked rows | {report['blocked_count']} |",
        f"| timed scored forms | {report['timed_scored_form_count']} |",
        f"| scored forms | {report['scored_form_count']} |",
        "",
        "## Form Counts",
        "",
        "| Form | Count |",
        "| --- | ---: |",
    ]
    for form, count in dict(report["form_counts"]).items():
        lines.append(f"| `{form}` | {count} |")
    lines.extend(["", "## Rows", "", "| Entry | Form | Category |", "| --- | --- | --- |"])
    for row in report["rows"]:
        lines.append(f"| `{row['entry_id']}` | `{row['form']}` | {row['category']} |")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    report = build_queue()
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_csv(report)
    write_markdown(report)
    print(
        "reported speed remaining queue: {count} rows; {ready} ready; {blocked} blocked".format(
            count=report["queue_count"],
            ready=report["ready_count"],
            blocked=report["blocked_count"],
        )
    )


if __name__ == "__main__":
    main()
