from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "benchmark-vabench-release-v1"
REPORT = PACKAGE / "reports" / "conformance_manifest.json"


def test_l0_conformance_manifest_is_separate_from_benchmark_denominator() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    assert report["suite"] == "evas-spectre"
    assert report["conformance_case_count"] == 4
    assert report["model_capability_count"] == 0
    assert report["benchmark_coverage_count"] == 0
    assert report["bugfix_claim_count"] == 0
    assert report["broad_parity_denominator_count"] == 0


def test_l0_conformance_cases_have_required_assets_and_false_counts() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    assert {case["id"] for case in report["cases"]} == {
        "file_metric_writer_io_timing",
        "cross_event_post_side_read",
        "settling_done_boundary",
        "vco_timer0_startup",
    }
    for case in report["cases"]:
        package_path = ROOT / case["package_path"]
        meta = json.loads((package_path / "meta.json").read_text(encoding="utf-8"))
        assert meta["asset_type"] == "evas_spectre_conformance"
        assert meta["suite"] == "evas-spectre"
        assert meta["counts"] == {
            "model_capability": False,
            "benchmark_coverage": False,
            "bugfix_claim": False,
            "broad_parity_denominator": False,
        }
        assert (package_path / "README.md").exists()
        assert (package_path / "checks.yaml").exists()
        assert (package_path / "gold").is_dir()
        assert any((package_path / "gold").iterdir())
