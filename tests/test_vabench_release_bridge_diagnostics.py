from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "benchmark-vabench-release-v1" / "reports" / "bridge_profile_diagnostics.json"


def test_bridge_profile_diagnostics_records_known_profiles() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    assert report["status"] in {"ready", "blocked"}
    assert report["profile_count"] >= 3
    profiles = {row["profile"] for row in report["profiles"]}
    assert {"default", "ci", "jin"} <= profiles


def test_bridge_profile_diagnostics_is_not_certification_evidence() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    assert any("not EVAS/Spectre certification evidence" in note for note in report["notes"])
    for row in report["profiles"]:
        assert "preflight" in row
        assert "ssh_smoke" in row
        assert "failure_code" in row["ssh_smoke"]
        assert "failure_summary" in row["ssh_smoke"]
        assert "remediation" in row["ssh_smoke"]
        assert row["local_port"]
        assert row["ready_for_release_rerun"] in {True, False}
        assert row["use_ssh_config_jump"] in {True, False}
        assert "diagnostic_notes" in row
        assert "hop_ssh_smokes" in row
        assert "alternate_ssh_smokes" in row


def test_bridge_profile_diagnostics_records_ssh_config_alternate_smoke() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    assert "ssh_config_jump_ok_profiles" in report
    assert "ssh_failure_code_counts" in report
    assert "alternate_ssh_failure_code_counts" in report
    assert "hop_ssh_failure_code_counts" in report
    assert "hop_ssh_ok_routes" in report
    alternates = [
        alt
        for row in report["profiles"]
        for alt in row.get("alternate_ssh_smokes", [])
    ]
    assert all(alt["env"] == "VB_USE_SSH_CONFIG_JUMP=1" for alt in alternates)
    assert all(alt["route"] == "ssh_config_proxyjump" for alt in alternates)
    assert all("failure_code" in alt["ssh_smoke"] for alt in alternates)


def test_bridge_profile_diagnostics_records_hop_level_smokes() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    hop_smokes = [
        hop
        for row in report["profiles"]
        for hop in row.get("hop_ssh_smokes", [])
    ]

    assert hop_smokes
    assert {hop["route"] for hop in hop_smokes} >= {"ssh_config_proxyjump"}
    assert any(hop["route"] == "explicit_jump" for hop in hop_smokes)
    for hop in hop_smokes:
        assert hop["target_host"]
        assert hop["target_user"]
        assert "failure_code" in hop["ssh_smoke"]
        assert "failure_summary" in hop["ssh_smoke"]


def test_bridge_profile_diagnostics_surfaces_jump_route_mismatch() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    notes = [
        note
        for row in report["profiles"]
        for note in row.get("diagnostic_notes", [])
    ]

    assert any("VB_USE_SSH_CONFIG_JUMP=1" in note for note in notes)
