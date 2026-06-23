from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

import report_vabench_release_rust_coverage_manifest as rust_cov


def test_release_rust_coverage_manifest_smoke() -> None:
    report = rust_cov.build_report(max_models=8)

    assert report["schema_version"] == "evas-release-rust-coverage-manifest.v1"
    assert report["artifact_kind"] == "engineering_rust_coverage_manifest"
    assert report["claim_policy"]["paper_speed_claim_allowed"] is False
    assert report["summary"]["model_rows"] == 8
    assert report["summary"]["compile_status_counts"]["pass"] >= 1
    assert report["summary"]["whole_segment_invalid_candidate_count"] == 0
    assert report["rustification_completion_estimate"]["percent"] > 0

    behavior_ids = {row["id"] for row in report["behavior_table"]}
    assert {"B01", "B10", "B12", "B18"}.issubset(behavior_ids)
    assert len(report["models"]) == 8
    assert all("path" in row and "rust_signals" in row for row in report["models"])


def test_gold_va_discovery_can_filter_entry_and_form() -> None:
    paths = rust_cov.iter_gold_va_files(
        entries={"vbr1_l1_binary_weighted_voltage_dac"},
        forms={"dut"},
    )

    assert paths
    assert all("vbr1_l1_binary_weighted_voltage_dac" in path.as_posix() for path in paths)
    assert all("/forms/dut/" in path.as_posix() for path in paths)
