#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
REPORTS_ROOT = PACKAGE_ROOT / "reports"
SUMMARY_JSON = ROOT / "results" / "vabench-release-v1-dual-rerun" / "summary.json"
REPORT_JSON = REPORTS_ROOT / "finish_readiness.json"
REPORT_MD = REPORTS_ROOT / "finish_readiness.md"


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def as_int(value: object) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def imported_summary_path(import_report: dict[str, Any]) -> Path:
    summary = str(import_report.get("summary", "") or "")
    if not summary:
        return SUMMARY_JSON
    path = Path(summary)
    return path if path.is_absolute() else ROOT / path


def check(
    *,
    check_id: str,
    status: str,
    requirement: str,
    evidence: list[str],
    finding: str,
    recovery: list[str] | None = None,
) -> dict[str, object]:
    return {
        "id": check_id,
        "status": status,
        "requirement": requirement,
        "evidence": evidence,
        "finding": finding,
        "recovery": recovery or [],
    }


def build_report() -> dict[str, object]:
    release_status = read_json(REPORTS_ROOT / "release_status.json")
    asset = read_json(REPORTS_ROOT / "asset_integrity.json")
    static = read_json(REPORTS_ROOT / "static_certification.json")
    dual = read_json(REPORTS_ROOT / "dual_certification.json")
    queue = read_json(REPORTS_ROOT / "dual_rerun_queue.json")
    staging = read_json(REPORTS_ROOT / "dual_rerun_staging_manifest.json")
    bridge = read_json(REPORTS_ROOT / "bridge_profile_diagnostics.json")
    external = read_json(REPORTS_ROOT / "external_blockers.json")
    import_report = read_json(REPORTS_ROOT / "dual_rerun_import.json")
    summary_path = imported_summary_path(import_report)
    summary = read_json(summary_path)

    planned_entries = as_int(release_status.get("planned_entries"))
    source_linked = as_int(release_status.get("source_linked_entry_count"))
    materialized = as_int(release_status.get("asset_materialized_entry_count"))
    static_failed = as_int(release_status.get("static_failed_release_task_count"))
    queue_count = as_int(queue.get("queue_count"))
    queue_ready = as_int(queue.get("ready_count"))
    queue_blocked = as_int(queue.get("blocked_count"))
    staging_queue_rows = as_int(staging.get("queue_row_count"))
    staging_ready_rows = as_int(staging.get("queue_rows_with_ready_primary_bundle"))
    staging_bundles = as_int(staging.get("bundle_count"))
    staging_ready_bundles = as_int(staging.get("ready_bundle_count"))
    staging_blocked_bundles = as_int(staging.get("blocked_bundle_count"))
    dual_pending = as_int(dual.get("dual_pending_release_task_count"))
    dual_failed = as_int(dual.get("dual_failed_release_task_count"))
    mismatch = as_int(dual.get("evas_pass_spectre_fail_count"))
    summary_tasks = as_int(summary.get("tasks_total"))
    expected_miss = as_int(summary.get("expected_miss_count"))

    local_ready = (
        planned_entries == 75
        and source_linked >= planned_entries
        and materialized >= planned_entries
        and asset.get("status") == "pass"
        and static.get("status") == "pass"
        and static_failed == 0
    )
    full_dual_ready = dual_pending == 0 and dual_failed == 0 and mismatch == 0
    queue_complete_ok = full_dual_ready and queue.get("status") == "complete" and queue_count == 0 and queue_blocked == 0
    queue_ready_ok = queue_complete_ok or (
        queue.get("status") == "ready" and queue_count > 0 and queue_ready == queue_count and queue_blocked == 0
    )
    staging_ready_ok = (
        (
            full_dual_ready
            and staging.get("status") == "complete"
            and staging_queue_rows == 0
            and staging_bundles == 0
            and staging_blocked_bundles == 0
        )
        or (
            staging.get("status") == "ready"
            and staging_queue_rows == queue_count
            and staging_ready_rows == queue_count
            and staging_blocked_bundles == 0
            and staging_ready_bundles == staging_bundles
        )
    )
    bridge_ready = bridge.get("status") == "ready" and bool(bridge.get("ready_profiles", []))
    imported_full_dual_complete = (
        full_dual_ready
        and queue_count == 0
        and import_report.get("status") in {"imported", "imported_with_failures"}
        and import_report.get("stale_summary") is False
    )
    current_summary_complete = imported_full_dual_complete or (
        summary.get("status") == "complete"
        and (summary_tasks == queue_count or (full_dual_ready and summary_tasks == as_int(import_report.get("summary_tasks_total"))))
        and summary.get("dry_run") is False
        and expected_miss == 0
    )
    import_ready = imported_full_dual_complete or (
        current_summary_complete
        and import_report.get("status") in {"imported", "imported_with_failures"}
        and import_report.get("stale_summary") is False
    )

    checks = [
        check(
            check_id="P1_local_release_package_ready",
            status="pass" if local_ready else "blocked",
            requirement="The 75-entry release plan is covered by materialized entries with zero asset/static issues.",
            evidence=[
                rel(REPORTS_ROOT / "release_status.json"),
                rel(REPORTS_ROOT / "asset_integrity.json"),
                rel(REPORTS_ROOT / "static_certification.json"),
            ],
            finding=f"planned={planned_entries}, source_linked={source_linked}, materialized={materialized}, asset={asset.get('status')}, static={static.get('status')}",
            recovery=["python3 runners/run_vabench_release_longrun.py"] if not local_ready else [],
        ),
        check(
            check_id="P2_primary_rerun_queue_ready",
            status="pass" if queue_ready_ok else "blocked",
            requirement="Every pending primary release row is ready for EVAS/Spectre rerun.",
            evidence=[rel(REPORTS_ROOT / "dual_rerun_queue.json")],
            finding=f"queue_status={queue.get('status')}, queue_count={queue_count}, ready={queue_ready}, blocked={queue_blocked}",
            recovery=["python3 runners/report_vabench_release_dual_rerun_queue.py"] if not queue_ready_ok else [],
        ),
        check(
            check_id="P3_staging_ready",
            status="pass" if staging_ready_ok else "blocked",
            requirement="Every queue row has a ready primary rerun bundle and no staged bundle blockers.",
            evidence=[rel(REPORTS_ROOT / "dual_rerun_staging_manifest.json")],
            finding=f"queue_rows={staging_queue_rows}, ready_primary_rows={staging_ready_rows}, bundles={staging_bundles}, ready_bundles={staging_ready_bundles}, blocked_bundles={staging_blocked_bundles}",
            recovery=["python3 runners/prepare_vabench_release_dual_rerun.py"] if not staging_ready_ok else [],
        ),
        check(
            check_id="P4_bridge_ready",
            status="pass" if bridge_ready or full_dual_ready else "blocked",
            requirement="At least one bridge profile is reachable before starting the fresh rerun.",
            evidence=[rel(REPORTS_ROOT / "bridge_profile_diagnostics.json"), rel(REPORTS_ROOT / "external_blockers.json")],
            finding=(
                "full release dual certification is already imported; bridge readiness is not required to finish"
                if full_dual_ready and not bridge_ready
                else f"bridge_status={bridge.get('status')}, ready_profiles={bridge.get('ready_profiles', [])}, reason={bridge.get('reason', '')}"
            ),
            recovery=[
                "python3 runners/report_vabench_release_bridge_diagnostics.py --ssh-timeout-s 10",
                "VB_USE_SSH_CONFIG_JUMP=1 python3 runners/report_vabench_release_bridge_diagnostics.py --ssh-timeout-s 10",
            ]
            if not bridge_ready and not full_dual_ready
            else [],
        ),
        check(
            check_id="P5_current_summary_acceptable",
            status="pass" if current_summary_complete else "blocked",
            requirement="Fresh rerun summary must be complete, non-dry-run, current to the queue, and have zero expected misses.",
            evidence=[rel(summary_path) if summary_path.exists() else ""],
            finding=f"summary_status={summary.get('status', 'missing')}, tasks_total={summary.get('tasks_total')}, queue_count={queue_count}, dry_run={summary.get('dry_run')}, expected_miss_count={summary.get('expected_miss_count')}",
            recovery=["python3 runners/finish_vabench_release_after_bridge.py"] if not current_summary_complete else [],
        ),
        check(
            check_id="P6_import_gate_clear",
            status="pass" if import_ready else "blocked",
            requirement="Only a complete current rerun summary may be imported as release certification evidence.",
            evidence=[rel(REPORTS_ROOT / "dual_rerun_import.json")],
            finding=f"import_status={import_report.get('status')}, stale_summary={import_report.get('stale_summary')}, imported={import_report.get('imported_primary_result_count')}",
            recovery=["python3 runners/import_vabench_release_dual_rerun_results.py"] if current_summary_complete and not import_ready else [],
        ),
        check(
            check_id="P7_full_dual_certification_clear",
            status="pass" if full_dual_ready else "blocked",
            requirement="Full release dual certification has no pending forms, failures, or EVAS PASS / Spectre FAIL mismatches.",
            evidence=[rel(REPORTS_ROOT / "dual_certification.json"), rel(REPORTS_ROOT / "certification_matrix.json")],
            finding=f"dual_pending={dual_pending}, dual_failed={dual_failed}, evas_pass_spectre_fail={mismatch}",
            recovery=["python3 runners/run_vabench_release_longrun.py"] if import_ready and not full_dual_ready else [],
        ),
    ]
    blocked_checks = [item for item in checks if item["status"] != "pass"]
    ready_to_run = local_ready and queue_count > 0 and queue_ready_ok and staging_ready_ok and bridge_ready
    ready_to_import = current_summary_complete
    ready_to_finish = not blocked_checks
    status = "ready_to_finish" if ready_to_finish else ("ready_to_run" if ready_to_run else "blocked")
    return {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "status": status,
        "ready_to_run_fresh_dual": ready_to_run,
        "ready_to_import_fresh_dual": ready_to_import,
        "ready_to_finish_release": ready_to_finish,
        "pass_count": sum(1 for item in checks if item["status"] == "pass"),
        "blocked_count": len(blocked_checks),
        "blocked_check_ids": [str(item["id"]) for item in blocked_checks],
        "run_scope": {
            "primary_queue_rows": queue_count,
            "ready_primary_queue_rows": queue_ready,
            "staged_bundle_count": staging_bundles,
            "ready_staged_bundle_count": staging_ready_bundles,
            "default_include_buggy": False,
            "expected_primary_summary_tasks_total": queue_count,
            "source_equivalence_blocked_forms": as_int(read_json(REPORTS_ROOT / "remaining_work.json").get("source_equivalence_blocked_form_count")),
        },
        "checks": checks,
        "fresh_summary_acceptance_criteria": [
            "summary.status == complete",
            "summary.tasks_total matches the active queue before import, or matches the imported full-rerun summary after certification import",
            "summary.dry_run is false or absent",
            "summary.expected_miss_count == 0",
            "dual_rerun_import.json is not stale after import",
        ],
        "next_commands": {
            "refresh_local_package": "python3 runners/run_vabench_release_longrun.py",
            "refresh_bridge_diagnostics": "python3 runners/report_vabench_release_bridge_diagnostics.py --ssh-timeout-s 10",
            "dry_run_finish_plan": "python3 runners/finish_vabench_release_after_bridge.py --dry-run --no-refresh-reports",
            "finish_after_bridge": "python3 runners/finish_vabench_release_after_bridge.py",
            "direct_primary_rerun": "./scripts/run_with_bridge.sh python3 runners/run_vabench_release_dual_rerun.py --output-root results/vabench-release-v1-dual-rerun --timeout-s 180",
        },
        "claim_boundary": [
            "This readiness report is not simulator certification evidence.",
            "A ready queue or ready staging bundle does not imply EVAS/Spectre pass.",
            "A stale, blocked, dry-run, or partial summary must not be imported.",
        ],
        "evidence_sources": {
            "dual_rerun_queue": rel(REPORTS_ROOT / "dual_rerun_queue.json"),
            "dual_rerun_staging": rel(REPORTS_ROOT / "dual_rerun_staging_manifest.json"),
            "bridge_profile_diagnostics": rel(REPORTS_ROOT / "bridge_profile_diagnostics.json"),
            "external_blockers": rel(REPORTS_ROOT / "external_blockers.json"),
            "dual_rerun_import": rel(REPORTS_ROOT / "dual_rerun_import.json"),
            "dual_certification": rel(REPORTS_ROOT / "dual_certification.json"),
        },
    }


def write_markdown(report: dict[str, object]) -> None:
    lines = [
        "# vaBench Release Finish Readiness",
        "",
        f"Date: {report['date']}",
        "",
        "This report states whether it is safe to start or import the fresh",
        "EVAS/Spectre release rerun. It is a readiness gate, not simulator",
        "certification evidence.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | --- |",
        f"| status | `{report['status']}` |",
        f"| ready to run fresh dual | `{report['ready_to_run_fresh_dual']}` |",
        f"| ready to import fresh dual | `{report['ready_to_import_fresh_dual']}` |",
        f"| ready to finish release | `{report['ready_to_finish_release']}` |",
        f"| passed checks | {report['pass_count']} |",
        f"| blocked checks | {report['blocked_count']} |",
        "",
        "## Checks",
        "",
        "| ID | Status | Finding |",
        "| --- | --- | --- |",
    ]
    for item in report["checks"]:
        lines.append(f"| `{item['id']}` | `{item['status']}` | {item['finding']} |")
    lines.extend(["", "## Fresh Summary Acceptance Criteria", ""])
    for item in report["fresh_summary_acceptance_criteria"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Commands", "", "| Command | Value |", "| --- | --- |"])
    for key, value in report["next_commands"].items():
        lines.append(f"| `{key}` | `{value}` |")
    lines.extend(["", "## Claim Boundary", ""])
    for item in report["claim_boundary"]:
        lines.append(f"- {item}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    report = build_report()
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report)
    print(
        "wrote finish readiness: status={status}; pass={passed}; blocked={blocked}".format(
            status=report["status"],
            passed=report["pass_count"],
            blocked=report["blocked_count"],
        )
    )


if __name__ == "__main__":
    main()
