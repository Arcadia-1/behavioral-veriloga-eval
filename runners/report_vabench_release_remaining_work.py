#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
TASKS_ROOT = PACKAGE_ROOT / "tasks"
SELECTED_MANIFEST_CSV = ROOT / "docs" / "VABENCH_RELEASE_SELECTED_MANIFEST.csv"
DUAL_REPORT_JSON = PACKAGE_ROOT / "reports" / "dual_certification.json"
STATUS_REPORT_JSON = PACKAGE_ROOT / "reports" / "release_status.json"
REPORT_JSON = PACKAGE_ROOT / "reports" / "remaining_work.json"
REPORT_MD = PACKAGE_ROOT / "reports" / "remaining_work.md"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def source_design_pending_rows() -> list[dict[str, str]]:
    return [
        {
            "entry_id": row["entry_id"],
            "base_function": row["base_function"],
            "package_status": row["package_status"],
            "missing_forms": row["missing_forms"],
            "reason": "no release-ready source task mapped yet",
        }
        for row in read_csv(SELECTED_MANIFEST_CSV)
        if row.get("forms_materialized", "") == ""
    ]


def selected_rerun_pending_forms(dual: dict[str, object]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for task in dual.get("task_reports", []):
        if not isinstance(task, dict):
            continue
        if task.get("status") != "pending":
            continue
        if int(task.get("source_equivalence_failure_count", 0)) > 0:
            continue
        blockers = task.get("pending_blockers", [])
        reason = "; ".join(str(blocker) for blocker in blockers) if isinstance(blockers, list) else str(blockers)
        rows.append(
            {
                "entry_id": task["entry_id"],
                "form": task["form"],
                "source_task_id": task["source_task_id"],
                "reason": reason or "fresh EVAS/Spectre rerun required",
                "evidence": task["evidence"],
            }
        )
    return rows


def source_equivalence_blocked_forms(dual: dict[str, object]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for task in dual.get("task_reports", []):
        if not isinstance(task, dict):
            continue
        if int(task.get("source_equivalence_failure_count", 0)) > 0:
            rows.append(
                {
                    "entry_id": task["entry_id"],
                    "form": task["form"],
                    "source_task_id": task["source_task_id"],
                    "pending_blockers": task.get("pending_blockers", []),
                    "evidence": task["evidence"],
                }
            )
    return rows


def current_seed_missing_forms(status: dict[str, object]) -> list[dict[str, object]]:
    return list(status.get("seed_entries_with_missing_forms", []))


def all_missing_required_forms() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path in sorted(TASKS_ROOT.glob("*/vbr1_*/release_entry.json")):
        entry = read_json(path)
        missing = entry.get("missing_forms", [])
        if not missing:
            continue
        rows.append(
            {
                "entry_id": entry["release_entry_id"],
                "base_function": entry["base_function"],
                "level": entry["level"],
                "package_status": entry["package_status"],
                "score_surface": entry["score_surface"],
                "missing_forms": missing,
                "release_blockers": entry.get("release_blockers", []),
                "manifest": path.relative_to(ROOT).as_posix(),
            }
        )
    return rows


def next_queue(
    *,
    source_pending_count: int,
    rerun_pending_count: int,
    source_equiv_count: int,
    missing_required_count: int,
    scored_entries: object,
) -> list[str]:
    queue: list[str] = []
    if source_pending_count:
        queue.append("Design release-ready source tasks for selected entries with no mapped source assets.")
    fresh_queue_count = rerun_pending_count + source_equiv_count
    if fresh_queue_count:
        queue.append(
            f"Run the current {fresh_queue_count}-form EVAS/Spectre fresh dual certification queue."
        )
    if source_equiv_count:
        queue.append(
            "Treat source-equivalence blocked historical imports as fresh-rerun rows; do not promote them from historical evidence."
        )
    if missing_required_count:
        queue.append("Resolve or explicitly defer release entries with missing required forms before enabling scoring.")
    if int(scored_entries or 0) == 0:
        queue.append("Only enable benchmark_score after every counted form is certified.")
    if not queue:
        queue.append("No remaining release work is known from current reports.")
    return queue


def build_report() -> dict[str, object]:
    dual = read_json(DUAL_REPORT_JSON)
    status = read_json(STATUS_REPORT_JSON)
    source_pending = source_design_pending_rows()
    rerun_pending = selected_rerun_pending_forms(dual)
    source_equiv = source_equivalence_blocked_forms(dual)
    fresh_queue_count = len(rerun_pending) + len(source_equiv)
    seed_missing = current_seed_missing_forms(status)
    missing_required = all_missing_required_forms()
    scored_entries = status.get("scored_release_entries", "missing")
    ready_to_score = int(scored_entries or 0) > 0
    return {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "status": "in_progress",
        "ready_to_score": ready_to_score,
        "planned_entries": status.get("planned_entries", "missing"),
        "source_linked_entry_count": status.get("source_linked_entry_count", "missing"),
        "asset_materialized_entry_count": status.get("asset_materialized_entry_count", "missing"),
        "static_certified_release_task_count": status.get("static_certified_release_task_count", "missing"),
        "dual_certified_release_task_count": dual.get("dual_certified_release_task_count", "missing"),
        "dual_pending_release_task_count": dual.get("dual_pending_release_task_count", "missing"),
        "dual_failed_release_task_count": dual.get("dual_failed_release_task_count", "missing"),
        "evas_pass_spectre_fail_count": dual.get("evas_pass_spectre_fail_count", "missing"),
        "scored_release_entries": scored_entries,
        "source_design_pending_entry_count": len(source_pending),
        "selected_rerun_pending_form_count": len(rerun_pending),
        "source_equivalence_blocked_form_count": len(source_equiv),
        "fresh_dual_rerun_queue_form_count": fresh_queue_count,
        "source_equivalence_resolution_policy": (
            "Historical source-equivalence blockers are already staged as fresh EVAS/Spectre rerun rows. "
            "They remain excluded from certification until the fresh rerun is imported."
        ),
        "missing_required_form_entry_count": len(missing_required),
        "current_seed_missing_form_entry_count": len(seed_missing),
        "source_design_pending_entries": source_pending,
        "selected_rerun_pending_forms": rerun_pending,
        "source_equivalence_blocked_forms": source_equiv,
        "missing_required_form_entries": missing_required,
        "current_seed_missing_forms": seed_missing,
        "next_queue": next_queue(
            source_pending_count=len(source_pending),
            rerun_pending_count=len(rerun_pending),
            source_equiv_count=len(source_equiv),
            missing_required_count=len(missing_required),
            scored_entries=scored_entries,
        ),
    }


def write_markdown(report: dict[str, object]) -> None:
    lines = [
        "# vaBench Release Remaining Work",
        "",
        f"Date: {report['date']}",
        "",
        "This report is the active queue for finishing the clean vaBench release.",
        "It separates missing source design from missing simulator evidence and",
        "from historical source-equivalence blockers. Scoring readiness is reported",
        "from the frozen score denominator, not inferred from source presence alone.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| planned entries | {report['planned_entries']} |",
        f"| source-linked entries | {report['source_linked_entry_count']} |",
        f"| entries with copied assets | {report['asset_materialized_entry_count']} |",
        f"| static-certified release forms | {report['static_certified_release_task_count']} |",
        f"| dual-certified release forms | {report['dual_certified_release_task_count']} |",
        f"| dual-pending release forms | {report['dual_pending_release_task_count']} |",
        f"| dual-failed release forms | {report['dual_failed_release_task_count']} |",
        f"| EVAS PASS / Spectre FAIL count | {report['evas_pass_spectre_fail_count']} |",
        f"| source-design pending entries | {report['source_design_pending_entry_count']} |",
        f"| selected rerun-pending forms | {report['selected_rerun_pending_form_count']} |",
        f"| source-equivalence blocked forms | {report['source_equivalence_blocked_form_count']} |",
        f"| fresh dual rerun queue forms | {report['fresh_dual_rerun_queue_form_count']} |",
        f"| missing required-form entries | {report['missing_required_form_entry_count']} |",
        f"| current seed missing-form entries | {report['current_seed_missing_form_entry_count']} |",
        f"| scored release entries | {report['scored_release_entries']} |",
        "",
        "## Source Design Pending",
        "",
        "| Entry | Function | Missing forms |",
        "| --- | --- | --- |",
    ]
    for row in report["source_design_pending_entries"]:
        lines.append(f"| `{row['entry_id']}` | {row['base_function']} | `{row['missing_forms']}` |")
    if not report["source_design_pending_entries"]:
        lines.append("| none | none | none |")

    lines.extend(
        [
            "",
            "## Selected Rerun Pending",
            "",
            "| Entry | Form | Source task |",
            "| --- | --- | --- |",
        ]
    )
    for row in report["selected_rerun_pending_forms"]:
        lines.append(f"| `{row['entry_id']}` | `{row['form']}` | `{row['source_task_id']}` |")
    if not report["selected_rerun_pending_forms"]:
        lines.append("| none | none | none |")

    lines.extend(
        [
            "",
            "## Source-Equivalence Blocked",
            "",
            "These rows are not a separate manual source-design queue. They are",
            "historical-evidence import blockers that must be resolved by the",
            "current fresh EVAS/Spectre rerun queue.",
            "",
            "| Entry | Form | Source task | Blockers |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in report["source_equivalence_blocked_forms"]:
        blockers = "; ".join(row["pending_blockers"])
        lines.append(f"| `{row['entry_id']}` | `{row['form']}` | `{row['source_task_id']}` | {blockers} |")
    if not report["source_equivalence_blocked_forms"]:
        lines.append("| none | none | none | none |")

    lines.extend(
        [
            "",
            "## Missing Required Forms",
            "",
            "| Entry | Level | Package status | Missing forms |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in report["missing_required_form_entries"]:
        lines.append(
            f"| `{row['entry_id']}` | `{row['level']}` | `{row['package_status']}` | `{', '.join(row['missing_forms'])}` |"
        )
    if not report["missing_required_form_entries"]:
        lines.append("| none | none | none | none |")

    lines.extend(
        [
            "",
            "## Current Seed Missing Forms",
            "",
            "| Entry | Base | Missing forms |",
            "| --- | --- | --- |",
        ]
    )
    for row in report["current_seed_missing_forms"]:
        lines.append(f"| `{row['entry_id']}` | `{row['base_id']}` | `{row['missing_forms']}` |")
    if not report["current_seed_missing_forms"]:
        lines.append("| none | none | none |")

    lines.extend(["", "## Next Queue", ""])
    for item in report["next_queue"]:
        lines.append(f"- {item}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    report = build_report()
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report)
    print(
        "reported remaining work: {source} source-design entries; {rerun} rerun-pending forms; {equiv} source-equivalence blockers".format(
            source=report["source_design_pending_entry_count"],
            rerun=report["selected_rerun_pending_form_count"],
            equiv=report["source_equivalence_blocked_form_count"],
        )
    )


if __name__ == "__main__":
    main()
