#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
TASKS_ROOT = PACKAGE_ROOT / "tasks"
REPORTS_ROOT = PACKAGE_ROOT / "reports"
DUAL_JSON = REPORTS_ROOT / "dual_certification.json"
SCORE_JSON = REPORTS_ROOT / "score_denominator_manifest.json"
QUEUE_JSON = REPORTS_ROOT / "dual_rerun_queue.json"
REPORT_JSON = REPORTS_ROOT / "certification_matrix.json"
REPORT_MD = REPORTS_ROOT / "certification_matrix.md"
ENTRY_CSV = REPORTS_ROOT / "certification_matrix_entries.csv"
FORM_CSV = REPORTS_ROOT / "certification_matrix_forms.csv"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def read_entries() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for path in sorted(TASKS_ROOT.glob("*/release_entry.json")):
        payload = read_json(path)
        if payload:
            payload["_manifest"] = rel(path)
            entries.append(payload)
    return entries


def dual_task_index(dual: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    return {
        (str(row.get("entry_id")), str(row.get("form"))): row
        for row in dual.get("task_reports", [])
        if isinstance(row, dict)
    }


def score_form_index(score: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    return {
        (str(row.get("release_entry_id")), str(row.get("form"))): row
        for row in score.get("form_rows", [])
        if isinstance(row, dict)
    }


def score_entry_index(score: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(row.get("release_entry_id")): row
        for row in score.get("entry_rows", [])
        if isinstance(row, dict)
    }


def queue_index(queue: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    return {
        (str(row.get("entry_id")), str(row.get("form"))): row
        for row in queue.get("rows", [])
        if isinstance(row, dict)
    }


def form_pending_cause(task_report: dict[str, Any], task: dict[str, Any]) -> str:
    status = str(task_report.get("status", "pending"))
    if status == "pass":
        return "certified"
    if status == "fail":
        return "dual_failure"
    backend = task_report.get("backend_status", {})
    if not isinstance(backend, dict):
        backend = {}
    source_equivalence_failures = int(task_report.get("source_equivalence_failure_count", 0) or 0)
    if backend.get("evas") == "pass" and backend.get("spectre") == "pass" and source_equivalence_failures:
        return "source_equivalence_blocked"
    if task.get("evas_status") == "pending" or task.get("spectre_status") == "pending":
        return "fresh_dual_rerun_pending"
    return "pending_unknown"


def disposition_for(pending_cause: str, queue_row: dict[str, Any]) -> str:
    if pending_cause == "certified":
        return "none"
    if pending_cause in {"fresh_dual_rerun_pending", "source_equivalence_blocked"}:
        return "fresh_dual_rerun_required" if queue_row.get("ready_for_dual_rerun") is True else "rerun_staging_required"
    if pending_cause == "dual_failure":
        return "investigate_dual_failure"
    return "manual_audit_required"


def entry_pending_cause(form_rows: list[dict[str, Any]], entry: dict[str, Any]) -> str:
    if entry.get("missing_forms"):
        return "missing_required_forms"
    if any(row["pending_cause"] == "dual_failure" for row in form_rows):
        return "dual_failure"
    if any(row["pending_cause"] == "source_equivalence_blocked" for row in form_rows):
        return "source_equivalence_blocked"
    if any(row["pending_cause"] == "fresh_dual_rerun_pending" for row in form_rows):
        return "fresh_dual_rerun_pending"
    if all(row["pending_cause"] == "certified" for row in form_rows) and form_rows:
        return "fully_certified"
    return "pending_unknown"


def build_form_rows(
    entries: list[dict[str, Any]],
    task_index: dict[tuple[str, str], dict[str, Any]],
    score_forms: dict[tuple[str, str], dict[str, Any]],
    queue_rows: dict[tuple[str, str], dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for entry in entries:
        entry_id = str(entry["release_entry_id"])
        for task in entry.get("release_tasks", []):
            if not isinstance(task, dict):
                continue
            form = str(task.get("form", ""))
            task_report = task_index.get((entry_id, form), {})
            score_row = score_forms.get((entry_id, form), {})
            queue_row = queue_rows.get((entry_id, form), {})
            backend = task_report.get("backend_status", {})
            if not isinstance(backend, dict):
                backend = {}
            pending_cause = form_pending_cause(task_report, task)
            rows.append(
                {
                    "release_entry_id": entry_id,
                    "form": form,
                    "level": entry.get("level", ""),
                    "category": entry.get("category", ""),
                    "base_function": entry.get("base_function", ""),
                    "package_status": entry.get("package_status", ""),
                    "source_task_id": task.get("release_source_task_id")
                    or task.get("historical_source_task_id")
                    or task_report.get("release_source_task_id")
                    or task_report.get("source_task_id", ""),
                    "static": task.get("static_status", "pending"),
                    "evas": backend.get("evas", task.get("evas_status", "pending")),
                    "spectre": backend.get("spectre", task.get("spectre_status", "pending")),
                    "dual_status": task_report.get("status", "pending"),
                    "pending_cause": pending_cause,
                    "disposition": disposition_for(pending_cause, queue_row),
                    "queue_reason": queue_row.get("queue_reason", ""),
                    "ready_for_dual_rerun": bool(queue_row.get("ready_for_dual_rerun", False)),
                    "source_equivalence_failure_count": int(
                        task_report.get("source_equivalence_failure_count", 0) or 0
                    ),
                    "blocker_count": int(task_report.get("blocker_count", 0) or 0),
                    "benchmark_score_enabled": bool(score_row.get("benchmark_score_enabled", False)),
                    "counted_in_score": bool(score_row.get("counted_in_score", False)),
                    "evidence": task_report.get("evidence", task.get("dual_evidence", "")),
                    "release_path": task.get("release_path", ""),
                }
            )
    return rows


def build_entry_rows(
    entries: list[dict[str, Any]],
    form_rows: list[dict[str, Any]],
    score_entries: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    forms_by_entry: dict[str, list[dict[str, Any]]] = {}
    for row in form_rows:
        forms_by_entry.setdefault(str(row["release_entry_id"]), []).append(row)
    rows: list[dict[str, Any]] = []
    for entry in entries:
        entry_id = str(entry["release_entry_id"])
        entry_forms = forms_by_entry.get(entry_id, [])
        score_row = score_entries.get(entry_id, {})
        certified_forms = sum(1 for row in entry_forms if row["pending_cause"] == "certified")
        pending_forms = len(entry_forms) - certified_forms
        pending_cause = entry_pending_cause(entry_forms, entry)
        rows.append(
            {
                "release_entry_id": entry_id,
                "level": entry.get("level", ""),
                "category": entry.get("category", ""),
                "base_function": entry.get("base_function", ""),
                "package_status": entry.get("package_status", ""),
                "score_surface": entry.get("score_surface", ""),
                "form_count": len(entry_forms),
                "certified_form_count": certified_forms,
                "pending_form_count": pending_forms,
                "entry_status": "fully_certified" if pending_cause == "fully_certified" else "pending",
                "pending_cause": pending_cause,
                "missing_forms": entry.get("missing_forms", []),
                "release_blockers": entry.get("release_blockers", []),
                "benchmark_score_enabled": bool(score_row.get("benchmark_score_enabled", False)),
                "counted_in_score": bool(score_row.get("counted_in_score", False)),
                "manifest": entry.get("_manifest", ""),
            }
        )
    return rows


def counts(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    return dict(sorted(Counter(str(row.get(key, "")) for row in rows).items()))


def nested_counts(rows: list[dict[str, Any]], outer: str, inner: str) -> dict[str, dict[str, int]]:
    result: dict[str, Counter[str]] = {}
    for row in rows:
        result.setdefault(str(row.get(outer, "")), Counter()).update([str(row.get(inner, ""))])
    return {key: dict(sorted(value.items())) for key, value in sorted(result.items())}


def build_report() -> dict[str, Any]:
    entries = read_entries()
    dual = read_json(DUAL_JSON)
    score = read_json(SCORE_JSON)
    queue = read_json(QUEUE_JSON)
    form_rows = build_form_rows(entries, dual_task_index(dual), score_form_index(score), queue_index(queue))
    entry_rows = build_entry_rows(entries, form_rows, score_entry_index(score))
    source_equivalence_blocked_forms = [
        row for row in form_rows if row["pending_cause"] == "source_equivalence_blocked"
    ]
    fresh_pending_forms = [row for row in form_rows if row["pending_cause"] == "fresh_dual_rerun_pending"]
    summary = {
        "entry_count": len(entry_rows),
        "form_count": len(form_rows),
        "fully_certified_entry_count": sum(1 for row in entry_rows if row["entry_status"] == "fully_certified"),
        "pending_entry_count": sum(1 for row in entry_rows if row["entry_status"] != "fully_certified"),
        "certified_form_count": sum(1 for row in form_rows if row["pending_cause"] == "certified"),
        "pending_form_count": sum(1 for row in form_rows if row["pending_cause"] != "certified"),
        "fresh_dual_rerun_pending_form_count": len(fresh_pending_forms),
        "source_equivalence_blocked_form_count": len(source_equivalence_blocked_forms),
        "dual_failure_form_count": sum(1 for row in form_rows if row["pending_cause"] == "dual_failure"),
        "evas_pass_spectre_fail_count": int(dual.get("evas_pass_spectre_fail_count", 0) or 0),
        "scored_entry_count": sum(1 for row in entry_rows if row["counted_in_score"]),
        "scored_form_count": sum(1 for row in form_rows if row["counted_in_score"]),
        "entry_status_counts": counts(entry_rows, "entry_status"),
        "entry_pending_cause_counts": counts(entry_rows, "pending_cause"),
        "form_pending_cause_counts": counts(form_rows, "pending_cause"),
        "form_disposition_counts": counts(form_rows, "disposition"),
        "form_counts_by_form": counts(form_rows, "form"),
        "form_pending_cause_by_category": nested_counts(form_rows, "category", "pending_cause"),
        "entry_pending_cause_by_level": nested_counts(entry_rows, "level", "pending_cause"),
    }
    status = "complete" if summary["pending_form_count"] == 0 and summary["dual_failure_form_count"] == 0 else "partial"
    return {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "status": status,
        "summary": summary,
        "source_equivalence_blocked_forms": source_equivalence_blocked_forms,
        "fresh_dual_rerun_pending_sample": fresh_pending_forms[:20],
        "entry_rows": entry_rows,
        "form_rows": form_rows,
        "claim_boundary": [
            "This matrix reorganizes existing release certification evidence; it does not create new simulator evidence.",
            "Only forms with static/evas/spectre pass and counted_in_score=true may enter benchmark scores.",
            "Pending fresh dual rerun and source-equivalence blocked forms remain excluded from score and full-release claims.",
        ],
        "evidence_sources": {
            "dual_certification": rel(DUAL_JSON),
            "score_denominator": rel(SCORE_JSON),
            "dual_rerun_queue": rel(QUEUE_JSON),
            "release_tasks_root": rel(TASKS_ROOT),
        },
    }


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_markdown(report: dict[str, Any]) -> None:
    summary = report["summary"]
    lines = [
        "# vaBench Release Certification Matrix",
        "",
        f"Date: {report['date']}",
        "",
        "This matrix is a paper-facing audit view over the release certification",
        "state. It reorganizes existing evidence and does not create new",
        "simulator certification evidence.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| status | `{report['status']}` |",
        f"| entries | {summary['entry_count']} |",
        f"| forms | {summary['form_count']} |",
        f"| fully certified entries | {summary['fully_certified_entry_count']} |",
        f"| pending entries | {summary['pending_entry_count']} |",
        f"| certified forms | {summary['certified_form_count']} |",
        f"| pending forms | {summary['pending_form_count']} |",
        f"| fresh dual-rerun pending forms | {summary['fresh_dual_rerun_pending_form_count']} |",
        f"| source-equivalence blocked forms | {summary['source_equivalence_blocked_form_count']} |",
        f"| dual-failure forms | {summary['dual_failure_form_count']} |",
        f"| EVAS PASS / Spectre FAIL | {summary['evas_pass_spectre_fail_count']} |",
        f"| scored entries | {summary['scored_entry_count']} |",
        f"| scored forms | {summary['scored_form_count']} |",
        "",
        "## Entry Pending Cause Counts",
        "",
    ]
    for key, value in summary["entry_pending_cause_counts"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Form Pending Cause Counts", ""])
    for key, value in summary["form_pending_cause_counts"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Form Disposition Counts", ""])
    for key, value in summary["form_disposition_counts"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Source-Equivalence Blocked Forms", ""])
    if report["source_equivalence_blocked_forms"]:
        lines.extend(["| Entry | Form | Source task | Blockers |", "| --- | --- | --- | ---: |"])
        for row in report["source_equivalence_blocked_forms"]:
            lines.append(
                f"| `{row['release_entry_id']}` | `{row['form']}` | `{row['source_task_id']}` | {row['blocker_count']} |"
            )
    else:
        lines.append("- none")
    lines.extend(["", "## Claim Boundary", ""])
    for item in report["claim_boundary"]:
        lines.append(f"- {item}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    report = build_report()
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_csv(
        ENTRY_CSV,
        report["entry_rows"],
        [
            "release_entry_id",
            "level",
            "category",
            "base_function",
            "package_status",
            "score_surface",
            "form_count",
            "certified_form_count",
            "pending_form_count",
            "entry_status",
            "pending_cause",
            "benchmark_score_enabled",
            "counted_in_score",
            "manifest",
        ],
    )
    write_csv(
        FORM_CSV,
        report["form_rows"],
        [
            "release_entry_id",
            "form",
            "level",
            "category",
            "base_function",
            "package_status",
            "source_task_id",
            "static",
            "evas",
            "spectre",
            "dual_status",
            "pending_cause",
            "disposition",
            "queue_reason",
            "ready_for_dual_rerun",
            "source_equivalence_failure_count",
            "blocker_count",
            "benchmark_score_enabled",
            "counted_in_score",
            "evidence",
            "release_path",
        ],
    )
    write_markdown(report)
    summary = report["summary"]
    print(
        "wrote certification matrix: status={status}; entries={entries}; forms={forms}; pending_forms={pending}".format(
            status=report["status"],
            entries=summary["entry_count"],
            forms=summary["form_count"],
            pending=summary["pending_form_count"],
        )
    )


if __name__ == "__main__":
    main()
