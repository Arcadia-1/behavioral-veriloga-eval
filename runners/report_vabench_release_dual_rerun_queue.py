#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
DUAL_REPORT_JSON = PACKAGE_ROOT / "reports" / "dual_certification.json"
TASKS_ROOT = PACKAGE_ROOT / "tasks"
REPORT_JSON = PACKAGE_ROOT / "reports" / "dual_rerun_queue.json"
REPORT_CSV = PACKAGE_ROOT / "reports" / "dual_rerun_queue.csv"
REPORT_MD = PACKAGE_ROOT / "reports" / "dual_rerun_queue.md"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def read_entries() -> dict[str, dict[str, object]]:
    entries: dict[str, dict[str, object]] = {}
    for path in sorted(TASKS_ROOT.glob("*/vbr1_*/release_entry.json")):
        payload = read_json(path)
        entries[str(payload["release_entry_id"])] = payload
    return entries


def task_by_form(entry: dict[str, object], form: str) -> dict[str, object]:
    for task in entry.get("release_tasks", []):
        if isinstance(task, dict) and task.get("form") == form:
            return task
    return {}


def classify_queue_row(report: dict[str, object], task: dict[str, object]) -> str:
    if int(report.get("source_equivalence_failure_count", 0)) > 0:
        return "source_equivalence_blocked_rerun"
    source_path = str(task.get("source_path", ""))
    if source_path.startswith("designed_release_spec:"):
        return "designed_release_source_rerun"
    return "selected_existing_source_rerun"


def build_queue() -> dict[str, object]:
    dual = read_json(DUAL_REPORT_JSON)
    entries = read_entries()
    rows: list[dict[str, object]] = []
    for report in dual.get("task_reports", []):
        if not isinstance(report, dict) or report.get("status") != "pending":
            continue
        entry_id = str(report["entry_id"])
        form = str(report["form"])
        entry = entries[entry_id]
        release_task = task_by_form(entry, form)
        provenance = release_task.get("provenance", {})
        if not isinstance(provenance, dict):
            provenance = {}
        release_source_task_id = str(
            provenance.get("source_task_id")
            or report.get("release_source_task_id")
            or report.get("source_task_id")
            or ""
        )
        historical_source_task_id = str(
            provenance.get("historical_source_task_id")
            or report.get("historical_source_task_id")
            or report.get("source_task_id")
            or ""
        )
        gold = [str(path) for path in release_task.get("gold", [])]
        gold_va = [path for path in gold if path.endswith(".va")]
        gold_scs = [path for path in gold if path.endswith(".scs")]
        queue_reason = classify_queue_row(report, release_task)
        rows.append(
            {
                "entry_id": entry_id,
                "form": form,
                "level": entry["level"],
                "category": entry["category"],
                "base_function": entry["base_function"],
                "source_task_id": release_source_task_id,
                "historical_source_task_id": historical_source_task_id,
                "queue_reason": queue_reason,
                "static_status": release_task.get("static_status", "missing"),
                "evas_status": release_task.get("evas_status", "pending"),
                "spectre_status": release_task.get("spectre_status", "pending"),
                "gold_va_count": len(gold_va),
                "gold_scs_count": len(gold_scs),
                "gold": gold,
                "evidence": report["evidence"],
                "pending_blockers": report.get("pending_blockers", []),
                "ready_for_dual_rerun": release_task.get("static_status") == "pass" and bool(gold),
            }
        )
    rows.sort(key=lambda row: (str(row["queue_reason"]), str(row["entry_id"]), str(row["form"])))
    reason_counts = dict(sorted(Counter(str(row["queue_reason"]) for row in rows).items()))
    form_counts = dict(sorted(Counter(str(row["form"]) for row in rows).items()))
    status = "complete" if not rows else ("ready" if all(row["ready_for_dual_rerun"] for row in rows) else "blocked")
    return {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "status": status,
        "queue_count": len(rows),
        "reason_counts": reason_counts,
        "form_counts": form_counts,
        "ready_count": sum(1 for row in rows if row["ready_for_dual_rerun"]),
        "blocked_count": sum(1 for row in rows if not row["ready_for_dual_rerun"]),
        "rows": rows,
        "notes": [
            "This queue is derived from dual_certification.json pending forms.",
            "Rows here are not failures and are not scored benchmark results.",
            "Run EVAS and Spectre on these release gold assets, then replace pending evidence with fresh dual evidence.",
        ],
    }


def write_csv(report: dict[str, object]) -> None:
    rows = list(report["rows"])
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
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row[field] for field in fields})


def write_markdown(report: dict[str, object]) -> None:
    lines = [
        "# vaBench Release Dual Rerun Queue",
        "",
        f"Date: {report['date']}",
        "",
        "This is the machine-readable queue for converting pending release forms",
        "into fresh EVAS/Spectre evidence. It is generated from the current",
        "`dual_certification.json` report.",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| queue rows | {report['queue_count']} |",
        f"| ready rows | {report['ready_count']} |",
        f"| blocked rows | {report['blocked_count']} |",
        "",
        "## Reason Counts",
        "",
        "| Reason | Count |",
        "| --- | ---: |",
    ]
    for reason, count in dict(report["reason_counts"]).items():
        lines.append(f"| `{reason}` | {count} |")
    lines.extend(
        [
            "",
            "## Rows",
            "",
            "| Entry | Form | Reason | Release Source | Historical Source |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in report["rows"]:
        lines.append(
            f"| `{row['entry_id']}` | `{row['form']}` | `{row['queue_reason']}` | `{row['source_task_id']}` | `{row['historical_source_task_id']}` |"
        )
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    report = build_queue()
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_csv(report)
    write_markdown(report)
    print(
        "reported dual rerun queue: {count} rows; {ready} ready; {blocked} blocked".format(
            count=report["queue_count"],
            ready=report["ready_count"],
            blocked=report["blocked_count"],
        )
    )


if __name__ == "__main__":
    main()
