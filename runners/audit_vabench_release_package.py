#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRACKER_CSV = ROOT / "docs" / "VABENCH_RELEASE_TRACKER.csv"
SEED_MANIFEST_CSV = ROOT / "docs" / "VABENCH_RELEASE_SEED_MANIFEST.csv"
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
TASKS_ROOT = PACKAGE_ROOT / "tasks"
REPORT_JSON = PACKAGE_ROOT / "reports" / "release_status.json"
REPORT_MD = PACKAGE_ROOT / "reports" / "release_status.md"
ASSET_REPORT_JSON = PACKAGE_ROOT / "reports" / "asset_integrity.json"
STATIC_REPORT_JSON = PACKAGE_ROOT / "reports" / "static_certification.json"
DUAL_REPORT_JSON = PACKAGE_ROOT / "reports" / "dual_certification.json"
CONFORMANCE_REPORT_JSON = PACKAGE_ROOT / "reports" / "conformance_manifest.json"
SCORE_DENOMINATOR_REPORT_JSON = PACKAGE_ROOT / "reports" / "score_denominator_manifest.json"
SPEED_DEBUG_REPORT_JSON = PACKAGE_ROOT / "reports" / "speed_debug_artifact.json"
BASELINE_REPORT_JSON = PACKAGE_ROOT / "reports" / "baseline_artifact.json"
CLAIM_GATE_REPORT_JSON = PACKAGE_ROOT / "reports" / "claim_gate.json"
DUAL_RERUN_IMPORT_REPORT_JSON = PACKAGE_ROOT / "reports" / "dual_rerun_import.json"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_release_entries() -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    if not TASKS_ROOT.exists():
        return entries
    for path in sorted(TASKS_ROOT.glob("CT*/vbr1_*/release_entry.json")):
        entries.append(json.loads(path.read_text(encoding="utf-8")))
    return entries


def read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def count(rows: list[dict[str, str]], field: str) -> dict[str, int]:
    return dict(sorted(Counter(row[field] for row in rows).items()))


def release_entry_certified(entry: dict[str, object]) -> bool:
    certification = entry.get("certification", {})
    if not isinstance(certification, dict):
        return False
    missing_forms = entry.get("missing_forms", [])
    blockers = entry.get("release_blockers", [])
    return (
        certification.get("static") == "pass"
        and certification.get("evas") == "pass"
        and certification.get("spectre") == "pass"
        and missing_forms == []
        and blockers == []
    )


def release_entry_scored(entry: dict[str, object]) -> bool:
    counts = entry.get("counts", {})
    return isinstance(counts, dict) and bool(counts.get("benchmark_score"))


def release_tasks(entry: dict[str, object]) -> list[dict[str, object]]:
    tasks = entry.get("release_tasks", [])
    if not isinstance(tasks, list):
        return []
    return [task for task in tasks if isinstance(task, dict)]


def release_entry_has_materialized_assets(entry: dict[str, object]) -> bool:
    return any(task.get("asset_materialized") is True for task in release_tasks(entry))


def build_report() -> dict[str, object]:
    tracker = read_csv(TRACKER_CSV)
    seeds = read_csv(SEED_MANIFEST_CSV) if SEED_MANIFEST_CSV.exists() else []
    entries = read_release_entries()
    asset_report = read_json(ASSET_REPORT_JSON)
    static_report = read_json(STATIC_REPORT_JSON)
    dual_report = read_json(DUAL_REPORT_JSON)
    conformance_report = read_json(CONFORMANCE_REPORT_JSON)
    score_denominator_report = read_json(SCORE_DENOMINATOR_REPORT_JSON)
    speed_debug_report = read_json(SPEED_DEBUG_REPORT_JSON)
    baseline_report = read_json(BASELINE_REPORT_JSON)
    claim_gate_report = read_json(CLAIM_GATE_REPORT_JSON)
    dual_rerun_import_report = read_json(DUAL_RERUN_IMPORT_REPORT_JSON)
    score_summary = score_denominator_report.get("summary", {})
    if not isinstance(score_summary, dict):
        score_summary = {}
    score_claim_rule = score_denominator_report.get("claim_rule", {})
    if not isinstance(score_claim_rule, dict):
        score_claim_rule = {}
    speed_measurement_scope = speed_debug_report.get("measurement_scope", {})
    if not isinstance(speed_measurement_scope, dict):
        speed_measurement_scope = {}
    blocked_claim_ids = claim_gate_report.get("blocked_claim_ids", [])
    if not isinstance(blocked_claim_ids, list):
        blocked_claim_ids = []
    linked_ids = {str(entry["release_entry_id"]) for entry in entries}
    tracker_ids = {row["entry_id"] for row in tracker}
    selected_missing = [
        row["entry_id"]
        for row in tracker
        if row["entry_id"] not in linked_ids and row["package_status"].startswith("selected_")
    ]
    current_missing = [
        row["entry_id"]
        for row in tracker
        if row["entry_id"] not in linked_ids and row["package_status"].startswith("current_")
    ]
    unexpected_entries = sorted(linked_ids - tracker_ids)
    missing_forms = [
        {
            "entry_id": row["entry_id"],
            "base_id": row["base_id"],
            "missing_forms": row["missing_forms"],
        }
        for row in seeds
        if row["missing_forms"]
    ]
    materialized_entries = [entry for entry in entries if release_entry_has_materialized_assets(entry)]
    fully_materialized_seed_ids = {
        row["entry_id"]
        for row in seeds
        if row["missing_forms"] == "" and row["asset_materialized_forms"]
    }

    score_ready = bool(score_claim_rule.get("score_claim_allowed", False)) and bool(
        score_summary.get("scored_entry_count", 0)
    )
    report = {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "planned_entries": len(tracker),
        "level_counts": count(tracker, "level"),
        "package_status_counts": count(tracker, "package_status"),
        "tracker_certification_counts": count(tracker, "certification_status"),
        "source_linked_entry_count": len(entries),
        "source_linked_seed_count": len(seeds),
        "asset_materialized_entry_count": len(materialized_entries),
        "fully_materialized_seed_count": len(fully_materialized_seed_ids),
        "asset_integrity_status": asset_report.get("status", "missing"),
        "asset_integrity_issue_count": asset_report.get("issue_count", "missing"),
        "asset_integrity_warning_count": asset_report.get("warning_count", "missing"),
        "static_certification_status": static_report.get("status", "missing"),
        "static_certified_release_task_count": static_report.get("static_certified_release_task_count", "missing"),
        "static_failed_release_task_count": static_report.get("static_failed_release_task_count", "missing"),
        "static_certified_entry_count": static_report.get("static_certified_entry_count", "missing"),
        "dual_certification_status": dual_report.get("status", "missing"),
        "dual_certified_release_task_count": dual_report.get("dual_certified_release_task_count", "missing"),
        "dual_failed_release_task_count": dual_report.get("dual_failed_release_task_count", "missing"),
        "dual_pending_release_task_count": dual_report.get("dual_pending_release_task_count", "missing"),
        "dual_pass_materialized_entry_count": dual_report.get("dual_pass_materialized_entry_count", "missing"),
        "dual_pending_materialized_entry_count": dual_report.get("dual_pending_materialized_entry_count", "missing"),
        "dual_failed_materialized_entry_count": dual_report.get("dual_failed_materialized_entry_count", "missing"),
        "fully_certified_entry_count": dual_report.get("fully_certified_entry_count", "missing"),
        "source_equivalence_failure_count": dual_report.get("source_equivalence_failure_count", "missing"),
        "source_equivalence_blocked_release_task_count": dual_report.get(
            "source_equivalence_blocked_release_task_count", "missing"
        ),
        "evas_pass_spectre_fail_count": dual_report.get("evas_pass_spectre_fail_count", "missing"),
        "dual_simulator_rerun": dual_report.get("simulator_rerun", "missing"),
        "l0_conformance_case_count": conformance_report.get("conformance_case_count", "missing"),
        "l0_conformance_benchmark_coverage_count": conformance_report.get("benchmark_coverage_count", "missing"),
        "l0_conformance_model_capability_count": conformance_report.get("model_capability_count", "missing"),
        "l0_conformance_broad_parity_denominator_count": conformance_report.get(
            "broad_parity_denominator_count", "missing"
        ),
        "score_denominator_status": score_denominator_report.get("status", "missing"),
        "score_denominator_enabled": bool(score_claim_rule.get("score_claim_allowed", False)),
        "score_claim_allowed": bool(score_claim_rule.get("score_claim_allowed", False)),
        "score_content_denominator_entry_count": score_summary.get("content_denominator_entry_count", "missing"),
        "score_content_denominator_form_count": score_summary.get("content_denominator_form_count", "missing"),
        "score_certified_entry_count": score_summary.get("certified_entry_count", "missing"),
        "score_certified_form_count": score_summary.get("certified_form_count", "missing"),
        "scored_release_forms": score_summary.get("scored_form_count", "missing"),
        "speed_debug_status": speed_debug_report.get("status", "missing"),
        "speed_claim_allowed": bool(speed_debug_report.get("claim_allowed", False)),
        "speed_timed_rows": speed_measurement_scope.get("timed_rows", "missing"),
        "baseline_status": baseline_report.get("status", "missing"),
        "baseline_claim_allowed": bool(baseline_report.get("claim_allowed", False)),
        "baseline_summary_count": baseline_report.get("baseline_summary_count", "missing"),
        "claim_gate_status": claim_gate_report.get("status", "missing"),
        "allowed_claim_count": claim_gate_report.get("allowed_claim_count", "missing"),
        "blocked_claim_count": claim_gate_report.get("blocked_claim_count", "missing"),
        "blocked_claim_ids": blocked_claim_ids,
        "dual_rerun_import_status": dual_rerun_import_report.get("status", "missing"),
        "dual_rerun_import_stale_summary": dual_rerun_import_report.get("stale_summary", "missing"),
        "entry_ids_missing_from_tracker": unexpected_entries,
        "current_seed_entries_without_package_dir": current_missing,
        "selected_entries_without_package_dir": selected_missing,
        "seed_entries_with_missing_forms": missing_forms,
        "seed_entries_all_forms_present": len(seeds) - len(missing_forms),
        "scored_release_entries": score_summary.get("scored_entry_count", "missing"),
        "certified_release_entries": sum(1 for entry in entries if release_entry_certified(entry)),
        "stop_condition": {
            "ready_to_score": score_ready,
            "reason": (
                "Certified content-denominator release entries have benchmark_score enabled."
                if score_ready
                else "Certified release entries remain unscored until benchmark_score is explicitly enabled."
            ),
        },
        "next_actions": [
            "Use score_denominator_manifest.json as the frozen denominator for score and baseline work.",
            "Run the same-slice EVAS/Spectre speed timing artifact before making speedup claims.",
            "Run minimal release baselines only against counted score-denominator rows.",
            "Keep L0 EVAS/Spectre conformance cases outside the L1/L2 denominator.",
        ],
    }
    return report


def write_markdown(report: dict[str, object]) -> None:
    missing_forms = report["seed_entries_with_missing_forms"]
    selected_missing = report["selected_entries_without_package_dir"]
    current_missing = report["current_seed_entries_without_package_dir"]

    lines = [
        "# vaBench Release Package Status",
        "",
        f"Date: {report['date']}",
        "",
        "This report is generated by `runners/audit_vabench_release_package.py`.",
        "It is intentionally conservative: source-linked rows are not counted as",
        "scored benchmark tasks until release assets and EVAS/Spectre certification",
        "are complete.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| planned L1/L2 entries | {report['planned_entries']} |",
        f"| source-linked package entries | {report['source_linked_entry_count']} |",
        f"| source-linked current seeds | {report['source_linked_seed_count']} |",
        f"| entries with copied release assets | {report['asset_materialized_entry_count']} |",
        f"| current seeds with all requested release assets | {report['fully_materialized_seed_count']} |",
        f"| asset integrity status | `{report['asset_integrity_status']}` |",
        f"| asset integrity issues | {report['asset_integrity_issue_count']} |",
        f"| asset integrity warnings | {report['asset_integrity_warning_count']} |",
        f"| static certification status | `{report['static_certification_status']}` |",
        f"| static-certified release forms | {report['static_certified_release_task_count']} |",
        f"| static-failed release forms | {report['static_failed_release_task_count']} |",
        f"| static-certified entries | {report['static_certified_entry_count']} |",
        f"| dual certification status | `{report['dual_certification_status']}` |",
        f"| dual-certified release forms | {report['dual_certified_release_task_count']} |",
        f"| dual-failed release forms | {report['dual_failed_release_task_count']} |",
        f"| dual-pending release forms | {report['dual_pending_release_task_count']} |",
        f"| dual-pass materialized entries | {report['dual_pass_materialized_entry_count']} |",
        f"| dual-pending materialized entries | {report['dual_pending_materialized_entry_count']} |",
        f"| dual-failed materialized entries | {report['dual_failed_materialized_entry_count']} |",
        f"| fully certified entries | {report['fully_certified_entry_count']} |",
        f"| source-equivalence blocked forms | {report['source_equivalence_blocked_release_task_count']} |",
        f"| source-equivalence blocker details | {report['source_equivalence_failure_count']} |",
        f"| EVAS PASS / Spectre FAIL count | {report['evas_pass_spectre_fail_count']} |",
        f"| dual simulator rerun | `{report['dual_simulator_rerun']}` |",
        f"| L0 conformance cases | {report['l0_conformance_case_count']} |",
        f"| L0 benchmark coverage count | {report['l0_conformance_benchmark_coverage_count']} |",
        f"| L0 model capability count | {report['l0_conformance_model_capability_count']} |",
        f"| L0 broad parity denominator count | {report['l0_conformance_broad_parity_denominator_count']} |",
        f"| score denominator status | `{report['score_denominator_status']}` |",
        f"| score claim allowed | `{report['score_claim_allowed']}` |",
        f"| score content denominator entries | {report['score_content_denominator_entry_count']} |",
        f"| score content denominator forms | {report['score_content_denominator_form_count']} |",
        f"| score-certified entries | {report['score_certified_entry_count']} |",
        f"| score-certified forms | {report['score_certified_form_count']} |",
        f"| scored release forms | {report['scored_release_forms']} |",
        f"| speed/debug status | `{report['speed_debug_status']}` |",
        f"| speed claim allowed | `{report['speed_claim_allowed']}` |",
        f"| speed timed rows | {report['speed_timed_rows']} |",
        f"| baseline status | `{report['baseline_status']}` |",
        f"| baseline claim allowed | `{report['baseline_claim_allowed']}` |",
        f"| baseline summary count | {report['baseline_summary_count']} |",
        f"| claim gate status | `{report['claim_gate_status']}` |",
        f"| allowed paper claims | {report['allowed_claim_count']} |",
        f"| blocked paper claims | {report['blocked_claim_count']} |",
        f"| dual rerun import status | `{report['dual_rerun_import_status']}` |",
        f"| dual rerun import stale summary | `{report['dual_rerun_import_stale_summary']}` |",
        f"| seed entries with all requested forms | {report['seed_entries_all_forms_present']} |",
        f"| seed entries with missing forms | {len(missing_forms)} |",
        f"| selected expansion entries without package dir | {len(selected_missing)} |",
        f"| current seed entries without package dir | {len(current_missing)} |",
        f"| certified release entries | {report['certified_release_entries']} |",
        f"| scored release entries | {report['scored_release_entries']} |",
        "",
        "## Counts",
        "",
        "### Level",
        "",
        "| Level | Count |",
        "| --- | ---: |",
    ]
    for key, value in dict(report["level_counts"]).items():
        lines.append(f"| {key} | {value} |")

    lines.extend(["", "### Package Status", "", "| Status | Count |", "| --- | ---: |"])
    for key, value in dict(report["package_status_counts"]).items():
        lines.append(f"| {key} | {value} |")

    lines.extend(
        [
            "",
            "## Missing Seed Forms",
            "",
            "| Entry | Base | Missing forms |",
            "| --- | --- | --- |",
        ]
    )
    if missing_forms:
        for row in missing_forms:
            lines.append(f"| `{row['entry_id']}` | `{row['base_id']}` | `{row['missing_forms']}` |")
    else:
        lines.append("| none | none | none |")

    lines.extend(
        [
            "",
            "## Stop Condition",
            "",
            f"- Ready to score: `{report['stop_condition']['ready_to_score']}`",
            f"- Reason: {report['stop_condition']['reason']}",
            "",
            "## Next Actions",
            "",
        ]
    )
    for action in report["next_actions"]:
        lines.append(f"- {action}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    report = build_report()
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report)
    print(
        "audited {planned} planned entries; {linked} source-linked; {certified} certified".format(
            planned=report["planned_entries"],
            linked=report["source_linked_entry_count"],
            certified=report["certified_release_entries"],
        )
    )


if __name__ == "__main__":
    main()
