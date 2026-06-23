from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

import report_vabench_release_rust_speed_claim_gate as gate


def test_rust_speed_claim_gate_allows_only_stage_claim_without_ax_artifact() -> None:
    report = gate.build_report(
        coverage_json=ROOT / "speed-optimization/reports/current_release_rust_coverage_manifest_20260604.json",
        stage_json=ROOT / "speed-optimization/reports/rust_stage55_topwall10_072_20260604.json",
        same_server_json=None,
    )

    stage_gate = report["gates"]["stage55_topwall_engineering_speedup"]
    assert stage_gate["allowed"] is False
    assert stage_gate["blockers"] == [
        "no_stage_rows",
        "stage_completion_below_threshold",
        "stage_wall_speedup_not_positive",
    ]
    assert report["gates"]["full_release_rustification"]["allowed"] is False
    assert report["gates"]["evas_faster_than_spectre_ax"]["allowed"] is False
    assert "missing_same_server_ax_artifact" in report["gates"]["evas_faster_than_spectre_ax"]["blockers"]
    assert report["claim_policy"]["engineering_stage_claim_allowed"] is False
    assert report["claim_policy"]["full_rustification_claim_allowed"] is False
    assert report["claim_policy"]["paper_speed_claim_allowed"] is False


def test_spectre_ax_gate_blocks_when_artifact_lacks_rust55_and_claim_allowed() -> None:
    report = gate.build_report(
        coverage_json=ROOT / "speed-optimization/reports/current_release_rust_coverage_manifest_20260604.json",
        stage_json=ROOT / "speed-optimization/reports/rust_stage55_topwall10_072_20260604.json",
        same_server_json=ROOT / "speed-optimization/reports/current_fourway_topwall10_clean_20260604.json",
    )

    ax_gate = report["gates"]["evas_faster_than_spectre_ax"]
    assert ax_gate["allowed"] is False
    assert ax_gate["blockers"] == ["missing_same_server_ax_artifact"]


def test_spectre_ax_gate_can_pass_for_complete_synthetic_same_server_artifact() -> None:
    same_server = {
        "claim_allowed": True,
        "parity_safety": {"violations": []},
        "summary": {
            "mode_summary": [
                {
                    "backend": "evas",
                    "mode": "profile_fast_rust_55",
                    "total_wall_time_s": 5.0,
                },
                {
                    "backend": "spectre",
                    "mode": "ax_speed",
                    "total_wall_time_s": 8.0,
                },
            ]
        },
    }

    ax_gate = gate.build_spectre_ax_gate(
        same_server,
        evas_mode="profile_fast_rust_55",
        spectre_ax_mode="ax_speed",
        require_artifact_claim_allowed=True,
    )

    assert ax_gate["allowed"] is True
    assert ax_gate["spectre_ax_over_evas_speedup"] == 1.6
