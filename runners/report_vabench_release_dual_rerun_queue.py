#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
DUAL_REPORT_JSON = PACKAGE_ROOT / "reports" / "dual_certification.json"
TASKS_ROOT = PACKAGE_ROOT / "tasks"
REPORT_JSON = PACKAGE_ROOT / "reports" / "dual_rerun_queue.json"
REPORT_CSV = PACKAGE_ROOT / "reports" / "dual_rerun_queue.csv"
REPORT_MD = PACKAGE_ROOT / "reports" / "dual_rerun_queue.md"
CERTIFICATION_MATRIX_JSON = PACKAGE_ROOT / "reports" / "certification_matrix.json"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def read_entries() -> dict[str, dict[str, Any]]:
    entries: dict[str, dict[str, Any]] = {}
    for path in sorted(TASKS_ROOT.glob("*/vbr1_*/release_entry.json")):
        payload = read_json(path)
        entries[str(payload["release_entry_id"])] = payload
    return entries


def task_by_form(entry: dict[str, Any], form: str) -> dict[str, Any]:
    for task in entry.get("release_tasks", []):
        if isinstance(task, dict) and task.get("form") == form:
            return task
    return {}


def classify_queue_row(report: dict[str, Any], task: dict[str, Any]) -> str:
    if int(report.get("source_equivalence_failure_count", 0) or 0) > 0:
        return "source_equivalence_blocked_rerun"
    source_path = str(task.get("source_path", ""))
    if source_path.startswith("designed_release_spec:"):
        return "designed_release_source_rerun"
    return "selected_existing_source_rerun"


def row_from_release_task(
    *,
    entry_id: str,
    form: str,
    entry: dict[str, Any],
    release_task: dict[str, Any],
    report_row: dict[str, Any],
) -> dict[str, Any]:
    provenance = release_task.get("provenance", {})
    if not isinstance(provenance, dict):
        provenance = {}
    release_source_task_id = str(
        provenance.get("source_task_id")
        or report_row.get("release_source_task_id")
        or report_row.get("source_task_id")
        or release_task.get("release_source_task_id")
        or ""
    )
    historical_source_task_id = str(
        provenance.get("historical_source_task_id")
        or report_row.get("historical_source_task_id")
        or report_row.get("source_task_id")
        or release_task.get("historical_source_task_id")
        or ""
    )
    gold = [str(path) for path in release_task.get("gold", [])]
    gold_va = [path for path in gold if path.endswith(".va")]
    gold_scs = [path for path in gold if path.endswith(".scs")]
    queue_reason = str(report_row.get("queue_reason") or classify_queue_row(report_row, release_task))
    return {
        "entry_id": entry_id,
        "form": form,
        "level": entry["level"],
        "category": entry["category"],
        "base_function": entry["base_function"],
        "source_task_id": release_source_task_id,
        "historical_source_task_id": historical_source_task_id,
        "queue_reason": queue_reason,
        "static_status": report_row.get("static", release_task.get("static_status", "missing")),
        "evas_status": report_row.get("evas", release_task.get("evas_status", "pending")),
        "spectre_status": report_row.get("spectre", release_task.get("spectre_status", "pending")),
        "gold_va_count": len(gold_va),
        "gold_scs_count": len(gold_scs),
        "gold": gold,
        "evidence": report_row.get("evidence", release_task.get("dual_evidence", "")),
        "pending_blockers": report_row.get("pending_blockers", []),
        "ready_for_dual_rerun": release_task.get("static_status") == "pass" and bool(gold),
    }


def selected_category(category: str, selected: set[str]) -> bool:
    return not selected or category in selected


def build_queue_from_dual(*, categories: set[str]) -> list[dict[str, Any]]:
    dual = read_json(DUAL_REPORT_JSON)
    entries = read_entries()
    rows: list[dict[str, Any]] = []
    for report in dual.get("task_reports", []):
        if not isinstance(report, dict) or report.get("status") != "pending":
            continue
        entry_id = str(report["entry_id"])
        form = str(report["form"])
        entry = entries[entry_id]
        if not selected_category(str(entry.get("category", "")), categories):
            continue
        release_task = task_by_form(entry, form)
        rows.append(
            row_from_release_task(
                entry_id=entry_id,
                form=form,
                entry=entry,
                release_task=release_task,
                report_row=report,
            )
        )
    return rows


def build_queue_from_certification_matrix(*, categories: set[str]) -> list[dict[str, Any]]:
    matrix = read_json(CERTIFICATION_MATRIX_JSON)
    entries = read_entries()
    rows: list[dict[str, Any]] = []
    for report in matrix.get("form_rows", []):
        if not isinstance(report, dict) or report.get("pending_cause") == "certified":
            continue
        category = str(report.get("category", ""))
        if not selected_category(category, categories):
            continue
        entry_id = str(report["release_entry_id"])
        form = str(report["form"])
        entry = entries[entry_id]
        release_task = task_by_form(entry, form)
        rows.append(
            row_from_release_task(
                entry_id=entry_id,
                form=form,
                entry=entry,
                release_task=release_task,
                report_row=report,
            )
        )
    return rows


def build_queue(*, source: str = "dual", categories: set[str] | None = None) -> dict[str, object]:
    selected_categories = categories or set()
    if source == "certification-matrix":
        rows = build_queue_from_certification_matrix(categories=selected_categories)
    else:
        rows = build_queue_from_dual(categories=selected_categories)
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
            f"This queue is derived from {source} pending forms.",
            "Rows here are not failures and are not scored benchmark results.",
            "Run EVAS and Spectre on these release gold assets, then replace pending evidence with fresh dual evidence.",
        ],
    }


def write_csv(report: dict[str, object], path: Path) -> None:
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
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row[field] for field in fields})


def write_markdown(report: dict[str, object], path: Path) -> None:
    lines = [
        "# vaBench Release Dual Rerun Queue",
        "",
        f"Date: {report['date']}",
        "",
        "This is the machine-readable queue for converting pending release forms",
        "into fresh EVAS/Spectre evidence.",
        f"Source report: `{report.get('source', 'dual')}`.",
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
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def path_arg(text: str) -> Path:
    path = Path(text)
    return path if path.is_absolute() else ROOT / path


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Build a vaBench release dual rerun queue.")
    ap.add_argument(
        "--source",
        choices=("dual", "certification-matrix"),
        default="dual",
        help="Source report for pending forms. Default preserves the historical behavior.",
    )
    ap.add_argument(
        "--category",
        action="append",
        default=[],
        help="Limit pending forms to this exact category. Can be repeated.",
    )
    ap.add_argument("--output-json", default=str(REPORT_JSON), help="Output queue JSON.")
    ap.add_argument("--output-csv", default=str(REPORT_CSV), help="Output queue CSV.")
    ap.add_argument("--output-md", default=str(REPORT_MD), help="Output queue Markdown.")
    return ap.parse_args()


def main() -> None:
    args = parse_args()
    report = build_queue(source=args.source, categories=set(args.category))
    output_json = path_arg(args.output_json)
    output_csv = path_arg(args.output_csv)
    output_md = path_arg(args.output_md)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    report["source"] = args.source
    report["category_filter"] = list(args.category)
    output_json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_csv(report, output_csv)
    write_markdown(report, output_md)
    print(
        "reported dual rerun queue: {count} rows; {ready} ready; {blocked} blocked".format(
            count=report["queue_count"],
            ready=report["ready_count"],
            blocked=report["blocked_count"],
        )
    )


if __name__ == "__main__":
    main()
