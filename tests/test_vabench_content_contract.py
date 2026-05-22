from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "benchmark-vabench-release-v1" / "reports" / "content_contract_audit.json"
MANIFEST = ROOT / "benchmark-vabench-release-v1" / "MANIFEST.json"


def test_content_contract_locks_clean_function_denominator() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    assert report["status"] == "pass"
    assert report["entry_count"] == 75
    assert report["form_count"] == 259
    assert report["content_denominator_entry_count"] == 74
    assert report["content_denominator_form_count"] == 255
    assert report["content_excluded_entry_count"] == 1
    assert report["severity_counts"].get("BLOCKER", 0) == 0
    assert report["duplicate_groups"] == []


def test_content_contract_deletes_known_duplicate_l2_entries() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    deleted_duplicates = {
        "vbr1_l2_gain_calibration_convergence_loop",
        "vbr1_l2_sample_hold_plus_calibration_system_flow",
        "vbr1_l2_sar_adc_mini_loop",
        "vbr1_l2_signal_conditioning_chain",
        "vbr1_l2_source_driven_verification_flow",
    }
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entry_ids = {entry["release_entry_id"] for entry in manifest["entries"]}

    assert deleted_duplicates.isdisjoint(entry_ids)
    assert report["content_excluded_entries"] == {
        "vbr1_l1_clocked_comparator": ["duplicate_strongarm_clocked_comparator"]
    }


def test_content_contract_tracks_shallow_checker_review_queue() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    shallow = [item for item in report["findings"] if item["kind"] == "shallow_generic_checker"]
    auxiliary = [item for item in report["findings"] if item["kind"] == "auxiliary_companion_checker"]

    assert len(shallow) == 0
    assert auxiliary == []
    shallow_ids = {item["entry_id"] for item in shallow}
    assert shallow_ids == set()
