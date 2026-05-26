from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

from run_vabench_release_dual_rerun import dry_run_raw_result, expected_result_met

PACKAGE = ROOT / "benchmark-vabench-release-v1"
MANIFEST = PACKAGE / "reports" / "dual_rerun_staging_manifest.json"
MANIFEST_CSV = PACKAGE / "reports" / "dual_rerun_staging_manifest.csv"
PENDING_CT07_GAIN = {
    ("vbr1_l1_gain_estimator", "e2e"),
    ("vbr1_l1_gain_estimator", "tb"),
}


def test_dual_rerun_staging_prepares_primary_bundle_for_each_queue_row() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert manifest["status"] == "ready"
    assert manifest["queue_row_count"] == 2
    assert manifest["queue_rows_with_ready_primary_bundle"] == 2
    assert manifest["bundle_count"] == 2
    assert manifest["ready_bundle_count"] == 2
    assert manifest["blocked_bundle_count"] == 0
    assert manifest["variant_counts"] == {"gold": 2}


def test_dual_rerun_staging_bundles_are_runner_shaped() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows = list(csv.DictReader(MANIFEST_CSV.open(encoding="utf-8")))

    assert len(rows) == manifest["bundle_count"]
    assert len(rows) == 2
    for record in manifest["bundles"]:
        assert record["status"] == "ready"
        task_dir = ROOT / record["staged_task_dir"]
        gold_dir = task_dir / "gold"
        assert (task_dir / "meta.json").exists()
        assert gold_dir.exists()
        assert (ROOT / record["staged_testbench"]).exists()
        for include_path in record["staged_includes"]:
            assert (ROOT / include_path).exists()


def test_dual_rerun_staging_bugfix_variants_preserve_buggy_fixed_origins() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    bugfix_records = [record for record in manifest["bundles"] if record["form"] == "bugfix"]

    assert len(bugfix_records) == 0
    for record in bugfix_records:
        origins = record["source_include_origins"]
        assert origins
        origin_paths = set(origins.values())
        if record["variant"] == "buggy":
            assert any(path.endswith("/dut_buggy.va") for path in origin_paths), record
            assert record["expected_result"] == "fail"
        elif record["variant"] == "fixed":
            assert any(path.endswith("/dut_fixed.va") for path in origin_paths), record
            assert record["expected_result"] == "pass"


def test_dual_rerun_staging_preserves_release_ids_but_maps_behavior_checkers() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert {(row["entry_id"], row["form"]) for row in manifest["bundles"]} == PENDING_CT07_GAIN
    assert {
        (row["form"], row["checker_task_id"], row["expected_result"])
        for row in manifest["bundles"]
    } == {
        ("e2e", "vbr1_l1_gain_estimator_e2e", "pass"),
        ("tb", "vbr1_l1_gain_estimator_tb", "pass"),
    }


def test_dual_rerun_dry_run_reports_staged_task_and_checker_ids() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert manifest["status"] == "ready"
    assert {(row["entry_id"], row["form"]) for row in manifest["bundles"]} == PENDING_CT07_GAIN


def test_buggy_expected_fail_requires_behavior_failure_on_both_backends() -> None:
    raw = {
        "status": "FAIL_EVAS",
        "evas": {
            "status": "FAIL_SIM_CORRECTNESS",
            "notes": ["returncode=0", "behavior mismatch"],
        },
        "spectre": {
            "ok": True,
            "status": "success",
            "behavior_score": 0.0,
            "behavior_notes": ["behavior mismatch"],
        },
    }

    assert expected_result_met(raw, "fail") is True


def test_buggy_expected_fail_rejects_compile_infra_and_one_sided_failures() -> None:
    compile_fail = {
        "status": "FAIL_EVAS",
        "evas": {"status": "FAIL_DUT_COMPILE", "notes": ["dut_not_compiled"]},
        "spectre": {"ok": True, "status": "success", "behavior_score": 0.0},
    }
    infra_fail = {
        "status": "FAIL_INFRA",
        "evas": {"status": "FAIL_SIM_CORRECTNESS"},
        "spectre": {"ok": False, "status": "blocked", "behavior_score": 0.0},
    }
    spectre_pass = {
        "status": "FAIL_EVAS",
        "evas": {"status": "FAIL_SIM_CORRECTNESS"},
        "spectre": {"ok": True, "status": "success", "behavior_score": 1.0},
    }

    assert expected_result_met(compile_fail, "fail") is False
    assert expected_result_met(infra_fail, "fail") is False
    assert expected_result_met(spectre_pass, "fail") is False
