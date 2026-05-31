#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRACKER_CSV = ROOT / "docs" / "VABENCH_RELEASE_TRACKER.csv"
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
TASKS_ROOT = PACKAGE_ROOT / "tasks"
REPORTS_ROOT = PACKAGE_ROOT / "reports"
STATUS_REPORT_JSON = REPORTS_ROOT / "release_status.json"
DUAL_REPORT_JSON = REPORTS_ROOT / "dual_certification.json"
STATIC_REPORT_JSON = REPORTS_ROOT / "static_certification.json"
ASSET_REPORT_JSON = REPORTS_ROOT / "asset_integrity.json"
CONFORMANCE_REPORT_JSON = REPORTS_ROOT / "conformance_manifest.json"
REMAINING_REPORT_JSON = REPORTS_ROOT / "remaining_work.json"
CERTIFICATION_MATRIX_JSON = REPORTS_ROOT / "certification_matrix.json"
RERUN_STAGING_REPORT_JSON = REPORTS_ROOT / "dual_rerun_staging_manifest.json"
DUAL_RERUN_IMPORT_JSON = REPORTS_ROOT / "dual_rerun_import.json"
DUAL_RERUN_SUMMARY_JSON = ROOT / "results" / "vabench-release-v1-dual-rerun" / "summary.json"
BRIDGE_DIAGNOSTICS_JSON = REPORTS_ROOT / "bridge_profile_diagnostics.json"
EXTERNAL_BLOCKERS_JSON = REPORTS_ROOT / "external_blockers.json"
SPEED_ARTIFACT_JSON = REPORTS_ROOT / "speed_debug_artifact.json"
BASLINE_ARTIFACT_JSON = REPORTS_ROOT / "baseline_artifact.json"
SCORE_DENOMINATOR_JSON = REPORTS_ROOT / "score_denominator_manifest.json"
MAIN120_EVAS_SUMMARY = ROOT / "results" / "vabench-main-v1-main120-gold-evas-2026-05-08" / "summary.json"
MAIN120_SPECTRE_SUMMARY = ROOT / "results" / "vabench-main-v1-main120-gold-spectre-jin-2026-05-08" / "summary.json"
REPORT_JSON = REPORTS_ROOT / "paper_artifacts.json"
REPORT_MD = REPORTS_ROOT / "paper_artifacts.md"
PLANNED_ENTRY_TARGET = 79


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def read_release_entries() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path in sorted(TASKS_ROOT.glob("*/vbr1_*/release_entry.json")):
        payload = read_json(path)
        if payload:
            rows.append(payload)
    return rows


def entry_form_count(entry: dict[str, object]) -> int:
    tasks = entry.get("release_tasks", [])
    return len([task for task in tasks if isinstance(task, dict)]) if isinstance(tasks, list) else 0


def imported_summary_path(import_report: dict[str, object]) -> Path:
    summary = str(import_report.get("summary", "") or "")
    if not summary:
        return DUAL_RERUN_SUMMARY_JSON
    path = Path(summary)
    return path if path.is_absolute() else ROOT / path


def count(rows: list[dict[str, str]], field: str) -> dict[str, int]:
    return dict(sorted(Counter(row[field] for row in rows).items()))


def backend_gold_summary(path: Path, key: str) -> dict[str, object]:
    payload = read_json(path)
    backend = payload.get(key, {})
    if not isinstance(backend, dict):
        backend = {}
    total = int(backend.get("total_tasks", payload.get("total_tasks", 0)) or 0)
    passed = int(backend.get("pass_count", 0) or 0)
    return {
        "source": path.relative_to(ROOT).as_posix() if path.exists() else "",
        "available": path.exists(),
        "total_tasks": total,
        "pass_count": passed,
        "pass_rate": passed / total if total else None,
        "axis_rates": backend.get("axis_rates", {}),
    }


def build_report() -> dict[str, object]:
    tracker = read_csv(TRACKER_CSV)
    status = read_json(STATUS_REPORT_JSON)
    dual = read_json(DUAL_REPORT_JSON)
    static = read_json(STATIC_REPORT_JSON)
    asset = read_json(ASSET_REPORT_JSON)
    conformance = read_json(CONFORMANCE_REPORT_JSON)
    remaining = read_json(REMAINING_REPORT_JSON)
    certification_matrix = read_json(CERTIFICATION_MATRIX_JSON)
    certification_matrix_summary = certification_matrix.get("summary", {})
    if not isinstance(certification_matrix_summary, dict):
        certification_matrix_summary = {}
    staging = read_json(RERUN_STAGING_REPORT_JSON)
    import_report = read_json(DUAL_RERUN_IMPORT_JSON)
    summary_path = imported_summary_path(import_report)
    rerun_summary = read_json(summary_path)
    bridge_diagnostics = read_json(BRIDGE_DIAGNOSTICS_JSON)
    external_blockers = read_json(EXTERNAL_BLOCKERS_JSON)
    speed_artifact = read_json(SPEED_ARTIFACT_JSON)
    baseline_artifact = read_json(BASLINE_ARTIFACT_JSON)
    score_denominator = read_json(SCORE_DENOMINATOR_JSON)
    denominator_summary = score_denominator.get("summary", {})
    if not isinstance(denominator_summary, dict):
        denominator_summary = {}
    release_entries = read_release_entries()
    track_counts = dict(sorted(Counter(str(entry.get("track", "core")) for entry in release_entries).items()))
    track_form_counts = dict(
        sorted(
            Counter(
                str(entry.get("track", "core"))
                for entry in release_entries
                for _ in range(entry_form_count(entry))
            ).items()
        )
    )
    difficulty_counts = dict(sorted(Counter(str(entry.get("difficulty", "D2")) for entry in release_entries).items()))
    scored = int(denominator_summary.get("scored_entry_count", 0) or 0)
    scored_forms = int(denominator_summary.get("scored_form_count", 0) or 0)
    dual_failed = int(status.get("dual_failed_release_task_count", 0) or 0)
    mismatch = int(status.get("evas_pass_spectre_fail_count", 0) or 0)
    dual_certified_forms = int(
        certification_matrix_summary.get(
            "certified_form_count",
            dual.get("dual_certified_release_task_count", 0),
        )
        or 0
    )
    dual_pending_forms = int(
        certification_matrix_summary.get(
            "pending_form_count",
            dual.get("dual_pending_release_task_count", 0),
        )
        or 0
    )
    source_equivalence_blocked_forms = int(
        certification_matrix_summary.get(
            "source_equivalence_blocked_form_count",
            dual.get("source_equivalence_blocked_release_task_count", 0),
        )
        or 0
    )
    asset_issues = int(status.get("asset_integrity_issue_count", 0) or 0)
    asset_warnings = int(status.get("asset_integrity_warning_count", 0) or 0)
    static_failed = int(status.get("static_failed_release_task_count", 0) or 0)
    source_pending = int(remaining.get("source_design_pending_entry_count", 0) or 0)
    rerun_pending = int(remaining.get("selected_rerun_pending_form_count", 0) or 0)
    missing_required = int(remaining.get("missing_required_form_entry_count", 0) or 0)
    current_seed_missing = int(remaining.get("current_seed_missing_form_entry_count", 0) or 0)
    planned_entries = int(status.get("planned_entries", 0) or 0)
    source_linked_entries = int(status.get("source_linked_entry_count", 0) or 0)
    materialized_entries = int(status.get("asset_materialized_entry_count", 0) or 0)
    materialization_complete = (
        source_pending == 0
        and missing_required == 0
        and current_seed_missing == 0
        and source_linked_entries >= planned_entries
        and materialized_entries >= planned_entries
        and asset_issues == 0
        and asset_warnings == 0
        and static_failed == 0
    )
    fresh_queue_ready = (
        staging.get("status") == "complete"
        or (
            staging.get("status") == "ready"
            and int(staging.get("queue_rows_with_ready_primary_bundle", 0) or 0)
            == int(staging.get("queue_row_count", 0) or 0)
            and int(staging.get("blocked_bundle_count", 0) or 0) == 0
        )
    )
    bridge_ready = bridge_diagnostics.get("status") == "ready" and bool(bridge_diagnostics.get("ready_profiles", []))
    full_dual_certified = (
        certification_matrix.get("status") in {"complete", "pass"}
        and dual_pending_forms == 0
        and dual_failed == 0
        and mismatch == 0
    )
    bridge_required_for_certification = not full_dual_certified

    coverage_summary = {
        "planned_entries": status.get("planned_entries", len(tracker)),
        "level_counts": status.get("level_counts", count(tracker, "level")),
        "category_counts": count(tracker, "category"),
        "track_counts": track_counts,
        "track_form_counts": track_form_counts,
        "difficulty_counts": difficulty_counts,
        "core_entry_count": track_counts.get("core", 0),
        "support_entry_count": track_counts.get("support", 0),
        "core_form_count": track_form_counts.get("core", 0),
        "support_form_count": track_form_counts.get("support", 0),
        "package_status_counts": status.get("package_status_counts", count(tracker, "package_status")),
        "source_linked_entry_count": status.get("source_linked_entry_count", 0),
        "asset_materialized_entry_count": status.get("asset_materialized_entry_count", 0),
        "static_certified_release_task_count": static.get("static_certified_release_task_count", 0),
        "dual_certified_release_task_count": dual_certified_forms,
        "fully_certified_entry_count": dual.get("fully_certified_entry_count", 0),
        "certification_matrix_status": certification_matrix.get("status", "missing"),
        "scored_release_entries": scored,
        "scored_release_forms": scored_forms,
        "core_scored_release_entries": int(denominator_summary.get("core_scored_entry_count", scored) or 0),
        "core_scored_release_forms": int(denominator_summary.get("core_scored_form_count", scored_forms) or 0),
        "support_scored_release_entries": int(denominator_summary.get("support_scored_entry_count", 0) or 0),
        "support_scored_release_forms": int(denominator_summary.get("support_scored_form_count", 0) or 0),
        "score_denominator_status": score_denominator.get("status", "missing"),
        "claim_status": "planning_and_full_certified_unscored" if scored == 0 else "core_score_enabled",
    }
    parity_summary = {
        "release_dual_status": certification_matrix.get("status", dual.get("status", "missing")),
        "dual_certified_release_task_count": dual_certified_forms,
        "dual_pending_release_task_count": dual_pending_forms,
        "dual_failed_release_task_count": dual_failed,
        "evas_pass_spectre_fail_count": mismatch,
        "source_equivalence_blocked_release_task_count": source_equivalence_blocked_forms,
        "imported_dual_pending_release_task_count": dual.get("dual_pending_release_task_count", 0),
        "main120_gold_evas": backend_gold_summary(MAIN120_EVAS_SUMMARY, "evas"),
        "main120_gold_spectre": backend_gold_summary(MAIN120_SPECTRE_SUMMARY, "spectre"),
        "l0_conformance_case_count": conformance.get("conformance_case_count", 0),
        "l0_counts_in_benchmark_denominator": conformance.get("benchmark_coverage_count", "missing"),
        "dual_rerun_staging_status": staging.get("status", "missing"),
        "dual_rerun_queue_rows_with_ready_primary_bundle": staging.get(
            "queue_rows_with_ready_primary_bundle", 0
        ),
        "dual_rerun_ready_bundle_count": staging.get("ready_bundle_count", 0),
        "latest_dual_rerun_attempt_status": rerun_summary.get("status", "missing"),
        "latest_dual_rerun_attempt_reason": rerun_summary.get("reason", ""),
        "bridge_diagnostics_status": bridge_diagnostics.get("status", "missing"),
        "bridge_diagnostics_reason": bridge_diagnostics.get("reason", ""),
        "bridge_ready_profiles": bridge_diagnostics.get("ready_profiles", []),
        "bridge_ssh_ok_profiles": bridge_diagnostics.get("ssh_ok_profiles", []),
    }
    speed_debug_summary = {
        "status": speed_artifact.get("status", "pending_measurement"),
        "claim_allowed": speed_artifact.get("claim_allowed", False),
        "reason": speed_artifact.get(
            "reason",
            "No same-slice release timing artifact compares EVAS and Spectre wall-clock/runtime yet.",
        ),
        "required_artifact": SPEED_ARTIFACT_JSON.relative_to(ROOT).as_posix(),
        "measurement_scope": speed_artifact.get("measurement_scope", {}),
        "timing_totals": speed_artifact.get("timing_totals", {}),
        "current_debug_evidence": [
            "benchmark-vabench-release-v1/reports/remaining_work.json",
            "benchmark-vabench-release-v1/reports/dual_certification.json",
            "benchmark-vabench-release-v1/reports/dual_rerun_staging_manifest.json",
            SPEED_ARTIFACT_JSON.relative_to(ROOT).as_posix(),
        ],
    }
    baseline_summary = {
        "status": baseline_artifact.get("status", "pending_release_baselines"),
        "claim_allowed": baseline_artifact.get("claim_allowed", False),
        "reason": (
            "No model baseline is scored against the clean release package because scored_release_entries is still zero."
            if scored == 0
            else "Score denominator is enabled, but no claimable model baseline summary has been produced yet."
        ),
        "required_artifact": BASLINE_ARTIFACT_JSON.relative_to(ROOT).as_posix(),
        "current_scored_release_entries": scored,
        "current_scored_release_forms": scored_forms,
        "score_denominator_status": score_denominator.get("status", "missing"),
        "score_denominator": SCORE_DENOMINATOR_JSON.relative_to(ROOT).as_posix(),
        "baseline_summary_count": baseline_artifact.get("baseline_summary_count", 0),
        "baseline_protocol": baseline_artifact.get("baseline_protocol", {}),
    }
    certification_gap_summary = {
        "assets_materialized": materialization_complete,
        "static_certification_complete": static.get("status") == "pass" and static_failed == 0,
        "fresh_dual_rerun_queue_ready": fresh_queue_ready,
        "fresh_dual_rerun_queue_count": staging.get("queue_row_count", 0),
        "fresh_dual_rerun_ready_bundle_count": staging.get("ready_bundle_count", 0),
        "dual_pending_release_task_count": dual_pending_forms,
        "bridge_ready": bridge_ready,
        "bridge_required_for_certification": bridge_required_for_certification,
        "bridge_ready_profiles": bridge_diagnostics.get("ready_profiles", []),
        "external_blockers_status": external_blockers.get("status", "missing"),
        "external_blocked_count": external_blockers.get("blocked_count", 0),
        "external_pending_count": external_blockers.get("pending_count", 0),
        "stale_rerun_summary_rejected": import_report.get("stale_summary") is True,
        "import_status": import_report.get("status", "missing"),
        "import_reason": import_report.get("reason", ""),
    }
    claim_gates = {
        "can_claim_release_assets_materialized": materialization_complete,
        "can_claim_top_level_coverage_plan": len(tracker) == PLANNED_ENTRY_TARGET,
        "can_claim_release_package_complete": (
            materialization_complete
            and dual_pending_forms == 0
            and dual_failed == 0
            and mismatch == 0
        ),
        "can_claim_scored_benchmark": scored > 0,
        "can_claim_zero_evas_pass_spectre_fail_on_imported_release_evidence": mismatch == 0 and dual_failed == 0,
        "can_claim_speedup": bool(speed_debug_summary["claim_allowed"]),
        "can_claim_model_baseline": bool(baseline_summary["claim_allowed"]),
        "blocking_conditions": [
            *(["asset integrity issues or warnings remain"] if asset_issues or asset_warnings else []),
            *(["static failures remain"] if static_failed else []),
            *(["dual failures or EVAS/Spectre mismatches remain"] if dual_failed or mismatch else []),
            *(["release entries are not scored yet"] if scored == 0 else []),
            *(["selected source design pending"] if source_pending else []),
            *(
                ["release entries with missing required forms remain unscored"]
                if missing_required
                else []
            ),
            *(["selected EVAS/Spectre rerun pending"] if rerun_pending else []),
            *(
                [f"EVAS/Spectre rerun blocked: {rerun_summary.get('reason')}"]
                if rerun_summary.get("status") == "blocked"
                else []
            ),
            *(
                [f"bridge diagnostics blocked: {bridge_diagnostics.get('reason')}"]
                if bridge_required_for_certification and bridge_diagnostics.get("status") == "blocked"
                else []
            ),
            *(
                [
                    "external blocker report active: "
                    f"{external_blockers.get('blocked_count')} blocked, "
                    f"{external_blockers.get('pending_count')} pending"
                ]
                if external_blockers.get("status") in {"blocked", "pending"}
                else []
            ),
            *(["speed/debug timing artifact not claimable"] if not speed_debug_summary["claim_allowed"] else []),
            *(["release model baseline artifact pending"] if not baseline_summary["claim_allowed"] else []),
        ],
    }
    return {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "status": "in_progress",
        "coverage_summary": coverage_summary,
        "parity_summary": parity_summary,
        "speed_debug_summary": speed_debug_summary,
        "baseline_summary": baseline_summary,
        "certification_gap_summary": certification_gap_summary,
        "claim_gates": claim_gates,
        "evidence_sources": {
            "tracker": TRACKER_CSV.relative_to(ROOT).as_posix(),
            "release_status": STATUS_REPORT_JSON.relative_to(ROOT).as_posix(),
            "asset_integrity": ASSET_REPORT_JSON.relative_to(ROOT).as_posix(),
            "static_certification": STATIC_REPORT_JSON.relative_to(ROOT).as_posix(),
            "dual_certification": DUAL_REPORT_JSON.relative_to(ROOT).as_posix(),
            "dual_rerun_staging": RERUN_STAGING_REPORT_JSON.relative_to(ROOT).as_posix(),
            "dual_rerun_import": DUAL_RERUN_IMPORT_JSON.relative_to(ROOT).as_posix(),
            "bridge_profile_diagnostics": (
                BRIDGE_DIAGNOSTICS_JSON.relative_to(ROOT).as_posix()
                if BRIDGE_DIAGNOSTICS_JSON.exists()
                else ""
            ),
            "external_blockers": (
                EXTERNAL_BLOCKERS_JSON.relative_to(ROOT).as_posix()
                if EXTERNAL_BLOCKERS_JSON.exists()
                else ""
            ),
            "speed_debug_artifact": SPEED_ARTIFACT_JSON.relative_to(ROOT).as_posix(),
            "baseline_artifact": BASLINE_ARTIFACT_JSON.relative_to(ROOT).as_posix(),
            "score_denominator_manifest": SCORE_DENOMINATOR_JSON.relative_to(ROOT).as_posix(),
            "latest_dual_rerun_attempt": (
                summary_path.relative_to(ROOT).as_posix()
                if summary_path.exists() and summary_path.is_relative_to(ROOT)
                else ""
            ),
            "conformance_manifest": CONFORMANCE_REPORT_JSON.relative_to(ROOT).as_posix(),
            "remaining_work": REMAINING_REPORT_JSON.relative_to(ROOT).as_posix(),
            "certification_matrix": (
                CERTIFICATION_MATRIX_JSON.relative_to(ROOT).as_posix()
                if CERTIFICATION_MATRIX_JSON.exists()
                else ""
            ),
        },
        "remaining_counts": {
            "source_design_pending_entry_count": remaining.get("source_design_pending_entry_count", 0),
            "selected_rerun_pending_form_count": remaining.get("selected_rerun_pending_form_count", 0),
            "source_equivalence_blocked_form_count": remaining.get("source_equivalence_blocked_form_count", 0),
            "missing_required_form_entry_count": remaining.get("missing_required_form_entry_count", 0),
            "current_seed_missing_form_entry_count": remaining.get("current_seed_missing_form_entry_count", 0),
        },
    }


def write_markdown(report: dict[str, object]) -> None:
    coverage = report["coverage_summary"]
    parity = report["parity_summary"]
    speed = report["speed_debug_summary"]
    baseline = report["baseline_summary"]
    gap = report["certification_gap_summary"]
    gates = report["claim_gates"]
    remaining = report["remaining_counts"]
    lines = [
        "# vaBench Paper-Facing Artifact Summary",
        "",
        f"Date: {report['date']}",
        "",
        "This is a claim-gated summary for paper writing. It records what can be",
        "cited from the current release package and what must remain pending.",
        "",
        "## Coverage",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| planned L1/L2 entries | {coverage['planned_entries']} |",
        f"| core circuit entries | {coverage['core_entry_count']} |",
        f"| support entries | {coverage['support_entry_count']} |",
        f"| D1/D2/D3 difficulty counts | `{coverage['difficulty_counts']}` |",
        f"| source-linked entries | {coverage['source_linked_entry_count']} |",
        f"| entries with copied assets | {coverage['asset_materialized_entry_count']} |",
        f"| static-certified release forms | {coverage['static_certified_release_task_count']} |",
        f"| dual-certified release forms | {coverage['dual_certified_release_task_count']} |",
        f"| fully certified entries | {coverage['fully_certified_entry_count']} |",
        f"| certification matrix | `{coverage['certification_matrix_status']}` |",
        f"| scored release entries | {coverage['scored_release_entries']} |",
        f"| scored release forms | {coverage['scored_release_forms']} |",
        f"| core scored release entries | {coverage['core_scored_release_entries']} |",
        f"| core scored release forms | {coverage['core_scored_release_forms']} |",
        f"| support scored release entries | {coverage['support_scored_release_entries']} |",
        f"| support scored release forms | {coverage['support_scored_release_forms']} |",
        f"| score denominator status | `{coverage['score_denominator_status']}` |",
        "",
        "## Parity",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| release dual status | `{parity['release_dual_status']}` |",
        f"| dual-certified release forms | {parity['dual_certified_release_task_count']} |",
        f"| dual-pending release forms | {parity['dual_pending_release_task_count']} |",
        f"| dual-failed release forms | {parity['dual_failed_release_task_count']} |",
        f"| EVAS PASS / Spectre FAIL count | {parity['evas_pass_spectre_fail_count']} |",
        f"| source-equivalence blocked forms | {parity['source_equivalence_blocked_release_task_count']} |",
        f"| dual rerun staging status | `{parity['dual_rerun_staging_status']}` |",
        f"| rerun rows with ready primary bundle | {parity['dual_rerun_queue_rows_with_ready_primary_bundle']} |",
        f"| ready rerun bundles | {parity['dual_rerun_ready_bundle_count']} |",
        f"| latest dual rerun attempt | `{parity['latest_dual_rerun_attempt_status']}` |",
        f"| bridge diagnostics | `{parity['bridge_diagnostics_status']}` |",
        f"| bridge ready profiles | `{', '.join(parity['bridge_ready_profiles']) or 'none'}` |",
        f"| main120 EVAS gold pass | {parity['main120_gold_evas']['pass_count']}/{parity['main120_gold_evas']['total_tasks']} |",
        f"| main120 Spectre gold pass | {parity['main120_gold_spectre']['pass_count']}/{parity['main120_gold_spectre']['total_tasks']} |",
        f"| L0 conformance cases | {parity['l0_conformance_case_count']} |",
        f"| L0 counted in benchmark denominator | {parity['l0_counts_in_benchmark_denominator']} |",
        "",
        "## Certification Gap",
        "",
        "| Gate | Value |",
        "| --- | --- |",
        f"| assets materialized | `{gap['assets_materialized']}` |",
        f"| static certification complete | `{gap['static_certification_complete']}` |",
        f"| fresh dual rerun queue ready | `{gap['fresh_dual_rerun_queue_ready']}` |",
        f"| fresh dual rerun queue rows | {gap['fresh_dual_rerun_queue_count']} |",
        f"| ready rerun bundles | {gap['fresh_dual_rerun_ready_bundle_count']} |",
        f"| dual-pending release forms | {gap['dual_pending_release_task_count']} |",
        f"| bridge ready | `{gap['bridge_ready']}` |",
        f"| external blockers | `{gap['external_blockers_status']}` |",
        f"| external blocked count | {gap['external_blocked_count']} |",
        f"| external pending count | {gap['external_pending_count']} |",
        f"| stale rerun summary rejected | `{gap['stale_rerun_summary_rejected']}` |",
        f"| import status | `{gap['import_status']}` |",
        "",
        "## Speed / Debug",
        "",
        f"- Status: `{speed['status']}`",
        f"- Claim allowed: `{speed['claim_allowed']}`",
        f"- Reason: {speed['reason']}",
        "",
        "## Baselines",
        "",
        f"- Status: `{baseline['status']}`",
        f"- Claim allowed: `{baseline['claim_allowed']}`",
        f"- Reason: {baseline['reason']}",
        "",
        "## Claim Gates",
        "",
        "| Claim | Allowed |",
        "| --- | --- |",
    ]
    for key, value in gates.items():
        if key == "blocking_conditions":
            continue
        lines.append(f"| `{key}` | `{value}` |")
    lines.extend(["", "## Remaining Counts", "", "| Queue | Count |", "| --- | ---: |"])
    for key, value in remaining.items():
        lines.append(f"| `{key}` | {value} |")
    lines.extend(["", "## Blocking Conditions", ""])
    for item in gates["blocking_conditions"]:
        lines.append(f"- {item}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    report = build_report()
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report)
    print(
        "wrote paper artifacts summary: coverage {entries} planned entries; parity mismatches {mismatch}; speed/baseline pending".format(
            entries=report["coverage_summary"]["planned_entries"],
            mismatch=report["parity_summary"]["evas_pass_spectre_fail_count"],
        )
    )


if __name__ == "__main__":
    main()
