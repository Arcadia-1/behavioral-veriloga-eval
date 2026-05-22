#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
REPORTS_ROOT = PACKAGE_ROOT / "reports"
DUAL_RERUN_SUMMARY_JSON = ROOT / "results" / "vabench-release-v1-dual-rerun" / "summary.json"
REPORT_JSON = REPORTS_ROOT / "external_blockers.json"
REPORT_MD = REPORTS_ROOT / "external_blockers.md"
FINISH_ATTEMPT_JSON = REPORTS_ROOT / "finish_after_bridge_attempt.json"


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def imported_summary_path(import_report: dict[str, object]) -> Path:
    summary = str(import_report.get("summary", "") or "")
    if not summary:
        return DUAL_RERUN_SUMMARY_JSON
    path = Path(summary)
    return path if path.is_absolute() else ROOT / path


def blocker(
    *,
    blocker_id: str,
    status: str,
    scope: str,
    diagnosis: str,
    claim_impact: list[str],
    evidence: list[str],
    recovery_commands: list[str],
    stop_condition: str,
    details: dict[str, object] | None = None,
) -> dict[str, object]:
    return {
        "id": blocker_id,
        "status": status,
        "scope": scope,
        "diagnosis": diagnosis,
        "claim_impact": claim_impact,
        "evidence": evidence,
        "recovery_commands": recovery_commands,
        "stop_condition": stop_condition,
        "details": details or {},
    }


def build_report() -> dict[str, object]:
    bridge = read_json(REPORTS_ROOT / "bridge_profile_diagnostics.json")
    finish = read_json(REPORTS_ROOT / "finish_after_bridge_attempt.json")
    queue = read_json(REPORTS_ROOT / "dual_rerun_queue.json")
    staging = read_json(REPORTS_ROOT / "dual_rerun_staging_manifest.json")
    import_report = read_json(REPORTS_ROOT / "dual_rerun_import.json")
    dual = read_json(REPORTS_ROOT / "dual_certification.json")
    paper = read_json(REPORTS_ROOT / "paper_artifacts.json")
    completion = read_json(REPORTS_ROOT / "completion_audit.json")
    speed = read_json(REPORTS_ROOT / "speed_debug_artifact.json")
    baseline = read_json(REPORTS_ROOT / "baseline_artifact.json")
    score = read_json(REPORTS_ROOT / "score_denominator_manifest.json")
    summary_path = imported_summary_path(import_report)
    rerun_summary = read_json(summary_path)

    queue_count = int(queue.get("queue_count", 0) or 0)
    staging_ready = int(staging.get("ready_bundle_count", 0) or 0)
    bridge_status = str(bridge.get("status", "missing"))
    bridge_ready = bridge_status == "ready" and bool(bridge.get("ready_profiles", []))
    dual_complete = (
        dual.get("status") == "pass"
        and int(dual.get("dual_pending_release_task_count", 0) or 0) == 0
        and int(dual.get("dual_failed_release_task_count", 0) or 0) == 0
        and int(dual.get("evas_pass_spectre_fail_count", 0) or 0) == 0
    )
    import_complete = import_report.get("status") in {"imported", "imported_with_failures"} and import_report.get("stale_summary") is False
    rerun_complete = (
        rerun_summary.get("status") == "complete"
        and int(rerun_summary.get("expected_miss_count", 0) or 0) == 0
    ) or (queue_count == 0 and dual_complete and import_complete)
    score_enabled = score.get("status") not in {
        "disabled_until_full_certification",
        "disabled_until_score_enablement",
    }

    blockers: list[dict[str, object]] = []
    if not bridge_ready and not (dual_complete and rerun_complete and import_complete):
        blockers.append(
            blocker(
                blocker_id="B1_bridge_ssh_or_tunnel_reachability",
                status="blocked",
                scope="external Virtuoso bridge profile readiness",
                diagnosis=str(bridge.get("reason", "bridge diagnostics are missing or not ready")),
                claim_impact=[
                    "fresh EVAS/Spectre release rerun cannot start",
                    "dual-pending release forms cannot be promoted",
                    "speed/debug and baseline claims remain disabled",
                ],
                evidence=[rel(REPORTS_ROOT / "bridge_profile_diagnostics.json")],
                recovery_commands=[
                    "python3 runners/report_vabench_release_bridge_diagnostics.py --ssh-timeout-s 10",
                    "VB_USE_SSH_CONFIG_JUMP=1 python3 runners/report_vabench_release_bridge_diagnostics.py --ssh-timeout-s 10",
                    "python3 runners/finish_vabench_release_after_bridge.py --dry-run --no-refresh-reports",
                ],
                stop_condition="At least one bridge profile appears in bridge_profile_diagnostics.ready_profiles.",
                details={
                    "ready_profiles": bridge.get("ready_profiles", []),
                    "ssh_ok_profiles": bridge.get("ssh_ok_profiles", []),
                    "ssh_config_jump_ok_profiles": bridge.get("ssh_config_jump_ok_profiles", []),
                    "ssh_failure_code_counts": bridge.get("ssh_failure_code_counts", {}),
                    "alternate_ssh_failure_code_counts": bridge.get("alternate_ssh_failure_code_counts", {}),
                    "hop_ssh_failure_code_counts": bridge.get("hop_ssh_failure_code_counts", {}),
                    "hop_ssh_ok_routes": bridge.get("hop_ssh_ok_routes", []),
                    "profile_count": bridge.get("profile_count", 0),
                    "latest_finish_attempt_status": finish.get("status", "missing"),
                    "latest_finish_attempt_reason": finish.get("reason", ""),
                },
            )
        )

    if not rerun_complete and not dual_complete:
        rerun_diagnosis = str(
            finish.get("reason")
            or rerun_summary.get(
                "reason",
                "fresh dual rerun summary is missing or has not completed",
            )
        )
        blockers.append(
            blocker(
                blocker_id="B2_fresh_dual_rerun_not_complete",
                status="blocked" if not bridge_ready else "ready_to_run",
                scope=f"{queue_count} primary EVAS/Spectre release rows",
                diagnosis=rerun_diagnosis,
                claim_impact=[
                    "release package cannot be claimed fully EVAS/Spectre certified",
                    "score denominator remains disabled",
                ],
                evidence=[
                    rel(REPORTS_ROOT / "dual_rerun_queue.json"),
                    rel(REPORTS_ROOT / "dual_rerun_staging_manifest.json"),
                    rel(FINISH_ATTEMPT_JSON) if FINISH_ATTEMPT_JSON.exists() else "",
                    rel(summary_path) if summary_path.exists() else "",
                ],
                recovery_commands=[
                    "python3 runners/finish_vabench_release_after_bridge.py",
                    "VB_USE_SSH_CONFIG_JUMP=1 python3 runners/finish_vabench_release_after_bridge.py",
                    "./scripts/run_with_bridge.sh python3 runners/run_vabench_release_dual_rerun.py --output-root results/vabench-release-v1-dual-rerun --timeout-s 180",
                ],
                stop_condition="The active rerun summary has status=complete, zero expected misses, and is imported into dual_certification.json.",
                details={
                    "queue_status": queue.get("status", "missing"),
                    "queue_count": queue_count,
                    "queue_ready_count": queue.get("ready_count", 0),
                    "staging_status": staging.get("status", "missing"),
                    "ready_staging_bundle_count": staging_ready,
                    "latest_summary_status": rerun_summary.get("status", "missing"),
                    "latest_summary_tasks_total": rerun_summary.get("tasks_total"),
                    "latest_finish_attempt_status": finish.get("status", "missing"),
                    "latest_finish_attempt_reason": finish.get("reason", ""),
                },
            )
        )

    if not import_complete and not dual_complete:
        blockers.append(
            blocker(
                blocker_id="B3_fresh_result_import_not_complete",
                status="blocked" if not rerun_complete else "ready_to_import",
                scope="fresh rerun result import gate",
                diagnosis=str(import_report.get("reason", "fresh rerun results have not been imported")),
                claim_impact=[
                    "fresh simulator results are not certification evidence",
                    "paper parity summary must rely only on imported historical/certified subset",
                ],
                evidence=[rel(REPORTS_ROOT / "dual_rerun_import.json")],
                recovery_commands=[
                    "python3 runners/import_vabench_release_dual_rerun_results.py",
                    "python3 runners/run_vabench_release_longrun.py",
                ],
                stop_condition="dual_rerun_import.json has status=imported or imported_with_failures and is not stale.",
                details={
                    "import_status": import_report.get("status", "missing"),
                    "stale_summary": import_report.get("stale_summary"),
                    "imported_count": import_report.get("imported_count", 0),
                },
            )
        )

    if not score_enabled or not speed.get("claim_allowed") or not baseline.get("claim_allowed"):
        disabled_claims = [
            *(["score"] if not score_enabled else []),
            *(["speed/debug"] if not speed.get("claim_allowed") else []),
            *(["model baseline"] if not baseline.get("claim_allowed") else []),
        ]
        blockers.append(
            blocker(
                blocker_id="B4_downstream_paper_claims_disabled",
                status="pending",
                scope=", ".join(disabled_claims) + " artifacts",
                diagnosis="downstream paper claims remain disabled until their dedicated artifacts are explicitly enabled",
                claim_impact=[
                    *(["do not claim benchmark scores"] if not score_enabled else []),
                    *(["do not claim EVAS speedup/debug advantage"] if not speed.get("claim_allowed") else []),
                    *(["do not claim model baseline results on the release package"] if not baseline.get("claim_allowed") else []),
                ],
                evidence=[
                    rel(REPORTS_ROOT / "score_denominator_manifest.json"),
                    rel(REPORTS_ROOT / "speed_debug_artifact.json"),
                    rel(REPORTS_ROOT / "baseline_artifact.json"),
                    rel(REPORTS_ROOT / "paper_artifacts.json"),
                ],
                recovery_commands=[
                    *(["python3 runners/report_vabench_release_score_denominator.py"] if not score_enabled else []),
                    *(["python3 runners/report_vabench_release_speed_debug.py"] if not speed.get("claim_allowed") else []),
                    *(["python3 runners/report_vabench_release_baseline_artifact.py"] if not baseline.get("claim_allowed") else []),
                ],
                stop_condition="paper_artifacts claim gates allow scored benchmark, speedup, and baseline claims only after their dedicated artifacts support them.",
                details={
                    "score_denominator_status": score.get("status", "missing"),
                    "speed_status": speed.get("status", "missing"),
                    "speed_claim_allowed": speed.get("claim_allowed", False),
                    "baseline_status": baseline.get("status", "missing"),
                    "baseline_claim_allowed": baseline.get("claim_allowed", False),
                },
            )
        )

    active_statuses = {item["status"] for item in blockers}
    if any(status == "blocked" for status in active_statuses):
        status = "blocked"
    elif blockers:
        status = "pending"
    else:
        status = "clear"

    if dual_complete and rerun_complete and import_complete:
        recovery_sequence = [
            "Keep the imported full EVAS/Spectre rerun as the release certification evidence.",
            "Use the enabled score denominator gate for scored benchmark rows/forms.",
            "Enable speed/debug and model baseline claims only after their dedicated artifacts support them.",
        ]
    else:
        recovery_sequence = [
            "Fix external SSH/VPN/jump-host reachability until bridge diagnostics reports a ready profile.",
            "Run finish_after_bridge without --dry-run to execute the fresh release dual rerun.",
            "Import only a complete current rerun summary, then regenerate paper artifacts and completion audit.",
            "Enable scored benchmark and baseline artifacts only after dual certification has no pending release forms.",
        ]

    return {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "status": status,
        "blocker_count": len(blockers),
        "blocked_count": sum(1 for item in blockers if item["status"] == "blocked"),
        "pending_count": sum(1 for item in blockers if item["status"] == "pending"),
        "ready_to_continue_count": sum(1 for item in blockers if item["status"].startswith("ready_")),
        "bridge_status": bridge_status,
        "bridge_reason": bridge.get("reason", ""),
        "latest_finish_attempt_status": finish.get("status", "missing"),
        "latest_finish_attempt_reason": finish.get("reason", ""),
        "queue_count": queue_count,
        "ready_staging_bundle_count": staging_ready,
        "latest_rerun_summary_status": rerun_summary.get("status", "missing"),
        "latest_import_status": import_report.get("status", "missing"),
        "paper_status": paper.get("status", "missing"),
        "completion_status": completion.get("status", "missing"),
        "blockers": blockers,
        "claim_boundary": [
            "This report is blocker/recovery evidence only; it is not EVAS/Spectre certification evidence.",
            "A blocked or dry-run simulator summary must not be imported into release evidence.",
            "Score, speed, and baseline claims remain governed by their dedicated claim gates.",
        ],
        "recovery_sequence": recovery_sequence,
    }


def write_markdown(report: dict[str, object]) -> None:
    lines = [
        "# vaBench Release External Blockers",
        "",
        f"Date: {report['date']}",
        "",
        "This report isolates the non-certification blockers that prevent the",
        "release package from becoming fully paper-claimable. It is a recovery",
        "and claim-boundary artifact, not simulator certification evidence.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| status | `{report['status']}` |",
        f"| blockers | {report['blocker_count']} |",
        f"| blocked | {report['blocked_count']} |",
        f"| pending | {report['pending_count']} |",
        f"| ready-to-continue | {report['ready_to_continue_count']} |",
        f"| bridge status | `{report['bridge_status']}` |",
        f"| primary rerun queue rows | {report['queue_count']} |",
        f"| ready staging bundles | {report['ready_staging_bundle_count']} |",
        f"| latest rerun summary | `{report['latest_rerun_summary_status']}` |",
        f"| latest import | `{report['latest_import_status']}` |",
        "",
        "## Blockers",
        "",
        "| ID | Status | Scope | Diagnosis |",
        "| --- | --- | --- | --- |",
    ]
    for item in report["blockers"]:
        lines.append(
            f"| `{item['id']}` | `{item['status']}` | {item['scope']} | {item['diagnosis']} |"
        )
    lines.extend(["", "## Recovery Sequence", ""])
    for action in report["recovery_sequence"]:
        lines.append(f"- {action}")
    lines.extend(["", "## Claim Boundary", ""])
    for item in report["claim_boundary"]:
        lines.append(f"- {item}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    report = build_report()
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report)
    print(
        "wrote external blockers: status={status}; blocked={blocked}; pending={pending}".format(
            status=report["status"],
            blocked=report["blocked_count"],
            pending=report["pending_count"],
        )
    )


if __name__ == "__main__":
    main()
