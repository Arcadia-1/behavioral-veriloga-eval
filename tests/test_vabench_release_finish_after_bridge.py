from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

import finish_vabench_release_after_bridge as finish_after_bridge
from finish_vabench_release_after_bridge import parse_args, profile_order, rerun_command


BRIDGE_REPO = ROOT.parents[1] / "iccad" / "virtuoso-bridge-lite"


def test_finish_after_bridge_discovers_release_profiles() -> None:
    profiles = [profile or "default" for profile in profile_order(BRIDGE_REPO, None)]

    assert {"default", "ci", "jin"} <= set(profiles)


def test_finish_after_bridge_builds_primary_rerun_command_without_buggy_by_default() -> None:
    args = parse_args(["--dry-run", "--profile", "ci", "--limit", "2"])
    cmd = rerun_command(args)

    assert cmd[:2] == ["python3", "runners/run_vabench_release_dual_rerun.py"]
    assert "--output-root" in cmd
    assert "--timeout-s" in cmd
    assert "--limit" in cmd
    assert "--include-buggy" not in cmd


def test_finish_after_bridge_refreshes_all_downstream_claim_gates(monkeypatch) -> None:
    calls: list[str] = []

    def record(name: str):
        return lambda *args, **kwargs: calls.append(name)

    monkeypatch.setattr(finish_after_bridge.import_vabench_release_dual_rerun_results, "main", record("import_dual"))
    monkeypatch.setattr(finish_after_bridge.sync_vabench_release_task_manifests, "main", record("sync_manifests"))
    monkeypatch.setattr(finish_after_bridge.audit_vabench_release_package, "main", record("audit_package"))
    monkeypatch.setattr(finish_after_bridge.report_vabench_release_remaining_work, "main", record("remaining"))
    monkeypatch.setattr(finish_after_bridge.report_vabench_release_speed_debug, "main", record("speed"))
    monkeypatch.setattr(finish_after_bridge.report_vabench_release_score_denominator, "main", record("score_denominator"))
    monkeypatch.setattr(finish_after_bridge.report_vabench_release_baseline_artifact, "main", record("baseline"))
    monkeypatch.setattr(finish_after_bridge.report_vabench_release_paper_artifacts, "main", record("paper"))
    monkeypatch.setattr(finish_after_bridge.report_vabench_release_schema_validation, "main", record("schema"))
    monkeypatch.setattr(finish_after_bridge.report_vabench_release_completion_audit, "main", record("completion"))
    monkeypatch.setattr(finish_after_bridge.report_vabench_release_checksum_manifest, "main", record("checksum"))
    monkeypatch.setattr(finish_after_bridge.report_vabench_release_artifact_index, "main", record("artifact_index"))

    finish_after_bridge.refresh_reports()

    assert calls == [
        "import_dual",
        "sync_manifests",
        "audit_package",
        "remaining",
        "speed",
        "score_denominator",
        "baseline",
        "paper",
        "schema",
        "completion",
        "checksum",
        "artifact_index",
        "checksum",
    ]


def test_finish_after_bridge_writes_fresh_bridge_diagnostics(monkeypatch, tmp_path) -> None:
    bridge_json = tmp_path / "bridge_profile_diagnostics.json"
    bridge_md_calls: list[dict[str, object]] = []

    monkeypatch.setattr(finish_after_bridge, "BRIDGE_DIAGNOSTICS_JSON", bridge_json)
    monkeypatch.setattr(
        finish_after_bridge,
        "build_bridge_report",
        lambda *args, **kwargs: {
            "status": "ready",
            "reason": "test ready",
            "ready_profiles": ["ci"],
            "ssh_ok_profiles": ["ci"],
        },
    )
    monkeypatch.setattr(
        finish_after_bridge,
        "write_bridge_diagnostics_markdown",
        lambda report: bridge_md_calls.append(report),
    )

    args = parse_args(["--dry-run", "--profile", "ci", "--no-refresh-reports"])
    report = finish_after_bridge.build_report(args)

    assert report["bridge_diagnostics_status"] == "ready"
    assert bridge_json.exists()
    assert bridge_md_calls and bridge_md_calls[0]["ready_profiles"] == ["ci"]
    assert report["rerun_scope"]["queue_status"] == "ready"
    assert report["rerun_scope"]["primary_queue_count"] == 2
    assert report["rerun_scope"]["primary_ready_count"] == 2
    assert report["rerun_scope"]["staging_bundle_count"] == 2
    assert report["rerun_scope"]["staging_ready_bundle_count"] == 2
    assert report["rerun_scope"]["latest_import_stale_summary"] is False


def test_finish_after_bridge_skips_profile_attempts_when_diagnostics_blocked(monkeypatch, tmp_path) -> None:
    attempted: list[str] = []
    bridge_json = tmp_path / "bridge_profile_diagnostics.json"
    monkeypatch.setattr(finish_after_bridge, "BRIDGE_DIAGNOSTICS_JSON", bridge_json)

    monkeypatch.setattr(
        finish_after_bridge,
        "build_bridge_report",
        lambda *args, **kwargs: {
            "status": "blocked",
            "reason": "test blocked",
            "ready_profiles": [],
            "ssh_ok_profiles": [],
        },
    )
    monkeypatch.setattr(finish_after_bridge, "write_bridge_diagnostics_markdown", lambda report: None)
    monkeypatch.setattr(
        finish_after_bridge,
        "run_profile",
        lambda profile, args: attempted.append(profile or "default") or {"summary_status": "complete"},
    )

    args = parse_args(["--profile", "ci", "--no-refresh-reports"])
    report = finish_after_bridge.build_report(args)

    assert report["status"] == "blocked"
    assert "simulator attempts were skipped" in report["reason"]
    assert attempted == []
    assert report["attempts"][0]["summary_status"] == "skipped_bridge_not_ready"


def test_finish_after_bridge_can_force_attempt_when_diagnostics_blocked(monkeypatch, tmp_path) -> None:
    attempted: list[str] = []
    bridge_json = tmp_path / "bridge_profile_diagnostics.json"
    monkeypatch.setattr(finish_after_bridge, "BRIDGE_DIAGNOSTICS_JSON", bridge_json)

    monkeypatch.setattr(
        finish_after_bridge,
        "build_bridge_report",
        lambda *args, **kwargs: {
            "status": "blocked",
            "reason": "test blocked",
            "ready_profiles": [],
            "ssh_ok_profiles": [],
        },
    )
    monkeypatch.setattr(finish_after_bridge, "write_bridge_diagnostics_markdown", lambda report: None)
    monkeypatch.setattr(
        finish_after_bridge,
        "run_profile",
        lambda profile, args: attempted.append(profile or "default")
        or {
            "profile": profile or "default",
            "summary_status": "complete",
            "summary_expected_miss_count": 0,
        },
    )

    args = parse_args(["--profile", "ci", "--force-attempt-when-bridge-blocked", "--no-refresh-reports"])
    report = finish_after_bridge.build_report(args)

    assert report["status"] == "complete"
    assert attempted == ["ci"]


def test_finish_after_bridge_writes_attempt_snapshot_before_refresh(monkeypatch, tmp_path) -> None:
    attempt_json = tmp_path / "finish_after_bridge_attempt.json"
    bridge_json = tmp_path / "bridge_profile_diagnostics.json"
    seen_during_refresh: list[str] = []

    monkeypatch.setattr(finish_after_bridge, "REPORT_JSON", attempt_json)
    monkeypatch.setattr(finish_after_bridge, "BRIDGE_DIAGNOSTICS_JSON", bridge_json)
    monkeypatch.setattr(
        finish_after_bridge,
        "build_bridge_report",
        lambda *args, **kwargs: {
            "status": "blocked",
            "reason": "test blocked",
            "ready_profiles": [],
            "ssh_ok_profiles": [],
        },
    )
    monkeypatch.setattr(finish_after_bridge, "write_bridge_diagnostics_markdown", lambda report: None)

    def refresh() -> None:
        assert attempt_json.exists()
        seen_during_refresh.append(attempt_json.read_text(encoding="utf-8"))

    monkeypatch.setattr(finish_after_bridge, "refresh_reports", refresh)

    args = parse_args(["--profile", "ci"])
    report = finish_after_bridge.build_report(args)

    assert report["status"] == "blocked"
    assert seen_during_refresh
    assert "simulator attempts were skipped" in seen_during_refresh[0]
