#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import audit_vabench_release_package
import import_vabench_release_dual_rerun_results
import report_vabench_release_artifact_index
import report_vabench_release_baseline_artifact
import report_vabench_release_certification_matrix
import report_vabench_release_claim_gate
import report_vabench_release_checksum_manifest
import report_vabench_release_completion_audit
import report_vabench_release_evaluator_contract
import report_vabench_release_external_blockers
import report_vabench_release_finish_readiness
import report_vabench_release_paper_artifacts
import report_vabench_release_paper_tables
import report_vabench_release_package_manifest
import report_vabench_release_remaining_work
import report_vabench_release_schema_validation
import report_vabench_release_score_denominator
import report_vabench_release_speed_debug
import sync_vabench_release_task_manifests
from report_vabench_release_bridge_diagnostics import (
    DEFAULT_BRIDGE_REPO,
    REPORT_JSON as BRIDGE_DIAGNOSTICS_JSON,
    build_report as build_bridge_report,
    discover_profiles,
    load_env_pairs,
    write_markdown as write_bridge_diagnostics_markdown,
)


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
REPORTS_ROOT = PACKAGE_ROOT / "reports"
DEFAULT_OUTPUT_ROOT = ROOT / "results" / "vabench-release-v1-dual-rerun"
SUMMARY_JSON = DEFAULT_OUTPUT_ROOT / "summary.json"
REPORT_JSON = REPORTS_ROOT / "finish_after_bridge_attempt.json"
REPORT_MD = REPORTS_ROOT / "finish_after_bridge_attempt.md"


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def profile_label(profile: str | None) -> str:
    return profile or "default"


def normalize_profile(profile: str) -> str | None:
    return None if profile == "default" else profile


def profile_order(bridge_repo: Path, requested: list[str] | None) -> list[str | None]:
    if requested:
        return [normalize_profile(item) for item in requested]
    env_pairs = load_env_pairs(bridge_repo / ".env")
    return discover_profiles(env_pairs)


def rerun_command(args: argparse.Namespace) -> list[str]:
    cmd = [
        "python3",
        "runners/run_vabench_release_dual_rerun.py",
        "--output-root",
        args.output_root,
        "--timeout-s",
        str(args.timeout_s),
    ]
    if args.limit is not None:
        cmd.extend(["--limit", str(args.limit)])
    if args.include_buggy:
        cmd.append("--include-buggy")
    return cmd


def rerun_scope(args: argparse.Namespace) -> dict[str, object]:
    queue = read_json(REPORTS_ROOT / "dual_rerun_queue.json")
    staging = read_json(REPORTS_ROOT / "dual_rerun_staging_manifest.json")
    import_report = read_json(REPORTS_ROOT / "dual_rerun_import.json")
    summary = read_json(Path(args.output_root) / "summary.json")
    selected_limit = args.limit if args.limit is not None else queue.get("queue_count")
    return {
        "queue_status": queue.get("status", "missing"),
        "primary_queue_count": queue.get("queue_count"),
        "primary_ready_count": queue.get("ready_count"),
        "primary_blocked_count": queue.get("blocked_count"),
        "queue_reason_counts": queue.get("reason_counts", {}),
        "staging_status": staging.get("status", "missing"),
        "staging_bundle_count": staging.get("bundle_count"),
        "staging_ready_bundle_count": staging.get("ready_bundle_count"),
        "staging_blocked_bundle_count": staging.get("blocked_bundle_count"),
        "include_buggy": args.include_buggy,
        "planned_bundle_limit": selected_limit,
        "latest_summary_status": summary.get("status", "missing"),
        "latest_summary_tasks_total": summary.get("tasks_total"),
        "latest_import_status": import_report.get("status", "missing"),
        "latest_import_stale_summary": import_report.get("stale_summary"),
        "latest_import_reason": import_report.get("reason", ""),
    }


def run_profile(profile: str | None, args: argparse.Namespace) -> dict[str, object]:
    started = datetime.now().isoformat(timespec="seconds")
    env = os.environ.copy()
    if profile is not None:
        env["BRIDGE_PROFILE"] = profile
    else:
        env.pop("BRIDGE_PROFILE", None)
    env["VB_SSH_CONNECT_TIMEOUT"] = str(args.ssh_connect_timeout)
    env["VB_SSH_SERVER_ALIVE_INTERVAL"] = str(args.ssh_server_alive_interval)
    env["VB_SSH_SERVER_ALIVE_COUNT_MAX"] = str(args.ssh_server_alive_count_max)
    cmd = ["./scripts/run_with_bridge.sh", *rerun_command(args)]
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
        timeout=args.profile_timeout_s,
    )
    summary = read_json(Path(args.output_root) / "summary.json")
    return {
        "profile": profile_label(profile),
        "started_at": started,
        "finished_at": datetime.now().isoformat(timespec="seconds"),
        "returncode": proc.returncode,
        "command": cmd,
        "stdout_tail": proc.stdout[-4000:],
        "stderr_tail": proc.stderr[-4000:],
        "summary_status": summary.get("status", "missing"),
        "summary_reason": summary.get("reason", ""),
        "summary_expected_miss_count": summary.get("expected_miss_count"),
        "summary_tasks_total": summary.get("tasks_total"),
    }


def refresh_reports() -> None:
    import_vabench_release_dual_rerun_results.main([])
    sync_vabench_release_task_manifests.main()
    audit_vabench_release_package.main()
    report_vabench_release_certification_matrix.main()
    report_vabench_release_remaining_work.main()
    report_vabench_release_speed_debug.main()
    report_vabench_release_score_denominator.main()
    report_vabench_release_baseline_artifact.main()
    report_vabench_release_external_blockers.main()
    report_vabench_release_finish_readiness.main()
    report_vabench_release_paper_artifacts.main()
    report_vabench_release_external_blockers.main()
    report_vabench_release_claim_gate.main()
    report_vabench_release_paper_tables.main()
    report_vabench_release_package_manifest.main()
    report_vabench_release_evaluator_contract.main()
    report_vabench_release_schema_validation.main()
    report_vabench_release_completion_audit.main()
    report_vabench_release_external_blockers.main()
    report_vabench_release_finish_readiness.main()
    report_vabench_release_claim_gate.main()
    audit_vabench_release_package.main()
    report_vabench_release_paper_tables.main()
    report_vabench_release_package_manifest.main()
    report_vabench_release_evaluator_contract.main()
    report_vabench_release_schema_validation.main()
    report_vabench_release_completion_audit.main()
    report_vabench_release_checksum_manifest.main()
    report_vabench_release_artifact_index.main()
    report_vabench_release_checksum_manifest.main()


def build_report(args: argparse.Namespace) -> dict[str, object]:
    bridge_repo = Path(args.bridge_repo).resolve()
    profiles = profile_order(bridge_repo, args.profile)
    diagnostics = build_bridge_report(
        bridge_repo,
        ssh_timeout_s=args.ssh_timeout_s,
        skip_ssh=args.skip_diagnostics_ssh,
    )
    BRIDGE_DIAGNOSTICS_JSON.parent.mkdir(parents=True, exist_ok=True)
    write_json(BRIDGE_DIAGNOSTICS_JSON, diagnostics)
    write_bridge_diagnostics_markdown(diagnostics)
    attempts: list[dict[str, object]] = []
    ready_profiles = set(str(profile) for profile in diagnostics.get("ready_profiles", []))

    if args.dry_run:
        status = "dry_run"
        reason = "dry run: no bridge tunnel or simulator command was executed"
        attempts = [
            {
                "profile": profile_label(profile),
                "command": ["./scripts/run_with_bridge.sh", *rerun_command(args)],
                "status": "planned",
            }
            for profile in profiles
        ]
    elif not ready_profiles and not args.force_attempt_when_bridge_blocked:
        status = "blocked"
        reason = "bridge diagnostics reported no ready profile; simulator attempts were skipped"
        attempts = [
            {
                "profile": profile_label(profile),
                "command": ["./scripts/run_with_bridge.sh", *rerun_command(args)],
                "status": "skipped_bridge_not_ready",
                "summary_status": "skipped_bridge_not_ready",
                "summary_reason": "bridge_profile_diagnostics.ready_profiles is empty",
                "summary_expected_miss_count": None,
                "summary_tasks_total": None,
            }
            for profile in profiles
        ]
    else:
        status = "blocked"
        reason = "no profile produced a complete EVAS/Spectre release rerun"
        for profile in profiles:
            try:
                attempt = run_profile(profile, args)
            except subprocess.TimeoutExpired as exc:
                attempt = {
                    "profile": profile_label(profile),
                    "started_at": datetime.now().isoformat(timespec="seconds"),
                    "finished_at": datetime.now().isoformat(timespec="seconds"),
                    "returncode": None,
                    "command": ["./scripts/run_with_bridge.sh", *rerun_command(args)],
                    "stdout_tail": (exc.stdout or "")[-4000:] if isinstance(exc.stdout, str) else "",
                    "stderr_tail": (exc.stderr or "")[-4000:] if isinstance(exc.stderr, str) else "",
                    "summary_status": "timeout",
                    "summary_reason": f"profile attempt exceeded {args.profile_timeout_s}s",
                    "summary_expected_miss_count": None,
                    "summary_tasks_total": None,
                }
            attempts.append(attempt)
            if attempt["summary_status"] == "complete":
                if attempt.get("summary_expected_miss_count") == 0:
                    status = "complete"
                    reason = f"profile {attempt['profile']} completed release rerun without expected misses"
                else:
                    status = "complete_with_failures"
                    reason = f"profile {attempt['profile']} completed release rerun with expected misses"
                break

    completion = read_json(REPORTS_ROOT / "completion_audit.json")
    scope = rerun_scope(args)
    report = {
        "date": datetime.now().date().isoformat(),
        "release": "vabench-release-v1",
        "status": status,
        "reason": reason,
        "dry_run": args.dry_run,
        "bridge_repo": str(bridge_repo),
        "profiles": [profile_label(profile) for profile in profiles],
        "bridge_diagnostics_status": diagnostics.get("status"),
        "bridge_diagnostics_reason": diagnostics.get("reason"),
        "bridge_ready_profiles": diagnostics.get("ready_profiles", []),
        "bridge_ssh_ok_profiles": diagnostics.get("ssh_ok_profiles", []),
        "rerun_scope": scope,
        "output_root": rel(Path(args.output_root)),
        "summary": rel(Path(args.output_root) / "summary.json"),
        "attempts": attempts,
        "post_attempt_completion_status": completion.get("status", "missing"),
        "post_attempt_completion_blockers": completion.get("blocking_conditions", []),
        "next_actions": [
            "Fix SSH/tunnel reachability for at least one bridge profile if all attempts are blocked.",
            "Re-run this script without --dry-run after bridge diagnostics reports a ready profile.",
            "Import only complete rerun summaries; blocked summaries remain non-certification evidence.",
        ],
    }
    if args.refresh_reports:
        write_json(REPORT_JSON, report)
        refresh_reports()
        completion = read_json(REPORTS_ROOT / "completion_audit.json")
        report["rerun_scope"] = rerun_scope(args)
        report["post_attempt_completion_status"] = completion.get("status", "missing")
        report["post_attempt_completion_blockers"] = completion.get("blocking_conditions", [])
    return report


def write_markdown(report: dict[str, object]) -> None:
    lines = [
        "# vaBench Release Finish-After-Bridge Attempt",
        "",
        f"Date: {report['date']}",
        "",
        "This report records attempts to finish the release after the external",
        "Virtuoso bridge becomes available. It does not turn blocked runs into",
        "certification evidence.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | --- |",
        f"| status | `{report['status']}` |",
        f"| reason | {report['reason']} |",
        f"| profiles | `{', '.join(report['profiles']) or 'none'}` |",
        f"| bridge diagnostics | `{report['bridge_diagnostics_status']}` |",
        f"| ready profiles | `{', '.join(report['bridge_ready_profiles']) or 'none'}` |",
        f"| completion audit | `{report['post_attempt_completion_status']}` |",
        "",
        "## Rerun Scope",
        "",
        "| Metric | Value |",
        "| --- | --- |",
        f"| queue status | `{report['rerun_scope']['queue_status']}` |",
        f"| primary queue rows | {report['rerun_scope']['primary_queue_count']} |",
        f"| ready primary rows | {report['rerun_scope']['primary_ready_count']} |",
        f"| staging bundles | {report['rerun_scope']['staging_bundle_count']} |",
        f"| ready staging bundles | {report['rerun_scope']['staging_ready_bundle_count']} |",
        f"| include buggy variants | `{report['rerun_scope']['include_buggy']}` |",
        f"| latest summary status | `{report['rerun_scope']['latest_summary_status']}` |",
        f"| latest import status | `{report['rerun_scope']['latest_import_status']}` |",
        f"| latest import stale summary | `{report['rerun_scope']['latest_import_stale_summary']}` |",
        "",
        "## Attempts",
        "",
        "| Profile | Status | Return code | Reason |",
        "| --- | --- | ---: | --- |",
    ]
    for attempt in report["attempts"]:
        lines.append(
            "| `{profile}` | `{status}` | {returncode} | {reason} |".format(
                profile=attempt["profile"],
                status=attempt.get("summary_status", attempt.get("status", "missing")),
                returncode=attempt.get("returncode", ""),
                reason=attempt.get("summary_reason", ""),
            )
        )
    lines.extend(["", "## Next Actions", ""])
    for action in report["next_actions"]:
        lines.append(f"- {action}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Finish vaBench release once the Virtuoso bridge is reachable.")
    parser.add_argument("--bridge-repo", default=str(DEFAULT_BRIDGE_REPO), help="Path to virtuoso-bridge-lite.")
    parser.add_argument("--profile", action="append", help="Bridge profile to try; may be repeated. Defaults to all .env profiles.")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT), help="Release dual rerun output root.")
    parser.add_argument("--timeout-s", type=int, default=180, help="Per-bundle simulator timeout.")
    parser.add_argument("--profile-timeout-s", type=int, default=21600, help="Maximum wall time for one profile attempt.")
    parser.add_argument("--limit", type=int, default=None, help="Optional maximum number of bundles for smoke attempts.")
    parser.add_argument("--include-buggy", action="store_true", help="Also run buggy companion bundles.")
    parser.add_argument("--dry-run", action="store_true", help="Write the attempt plan without starting bridge or simulators.")
    parser.add_argument("--refresh-reports", action=argparse.BooleanOptionalAction, default=True, help="Refresh import/paper/completion reports after attempts.")
    parser.add_argument("--ssh-timeout-s", type=int, default=5, help="Per-profile diagnostics SSH timeout.")
    parser.add_argument("--skip-diagnostics-ssh", action="store_true", help="Skip active SSH smoke in diagnostics.")
    parser.add_argument("--ssh-connect-timeout", type=int, default=8, help="Tunnel startup SSH ConnectTimeout.")
    parser.add_argument("--ssh-server-alive-interval", type=int, default=2, help="Tunnel startup ServerAliveInterval.")
    parser.add_argument("--ssh-server-alive-count-max", type=int, default=1, help="Tunnel startup ServerAliveCountMax.")
    parser.add_argument(
        "--force-attempt-when-bridge-blocked",
        action="store_true",
        help="Try bridge/simulator profiles even when diagnostics reports no ready profile.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report = build_report(args)
    write_json(REPORT_JSON, report)
    write_markdown(report)
    print(
        "finish-after-bridge: status={status}; profiles={profiles}; completion={completion}".format(
            status=report["status"],
            profiles=",".join(report["profiles"]) or "none",
            completion=report["post_attempt_completion_status"],
        )
    )
    if report["status"] in {"complete", "dry_run"}:
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
