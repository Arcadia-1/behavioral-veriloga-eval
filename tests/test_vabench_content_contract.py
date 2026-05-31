from __future__ import annotations

import json
from pathlib import Path

from audit_vabench_content_contract import extract_sim_checks


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "benchmark-vabench-release-v1" / "reports" / "content_contract_audit.json"
MANIFEST = ROOT / "benchmark-vabench-release-v1" / "MANIFEST.json"


def test_content_contract_locks_clean_function_denominator() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    assert report["status"] == "pass"
    assert report["entry_count"] == 79
    assert report["form_count"] == 271
    assert report["track_entry_counts"] == {"core": 66, "support": 13}
    assert report["content_denominator_entry_count"] == 66
    assert report["content_denominator_form_count"] == 236
    assert report["content_excluded_entry_count"] == 13
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
    assert set(report["content_excluded_entries"]) == {
        "vbr1_l1_burst_clock_source",
        "vbr1_l1_crossing_metric_writer",
        "vbr1_l1_dither_or_noise_like_deterministic_source",
        "vbr1_l1_edge_interval_timer",
        "vbr1_l1_gain_estimator",
        "vbr1_l1_lfsr_prbs_generator",
        "vbr1_l1_peak_detector",
        "vbr1_l1_ramp_or_step_source",
        "vbr1_l1_settling_time_detector",
        "vbr1_l1_sine_periodic_voltage_source",
        "vbr1_l2_gain_extraction_convergence_measurement_flow",
        "vbr1_l2_measurement_flow",
        "vbr1_l2_programmable_stimulus_sequencer",
    }


def test_content_contract_tracks_shallow_checker_review_queue() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    shallow = [item for item in report["findings"] if item["kind"] == "shallow_generic_checker"]
    auxiliary = [item for item in report["findings"] if item["kind"] == "auxiliary_companion_checker"]

    assert len(shallow) == 0
    assert auxiliary == []
    shallow_ids = {item["entry_id"] for item in shallow}
    assert shallow_ids == set()


def test_extract_sim_checks_handles_metadata_before_checks() -> None:
    checks_text = """
sim_correct:
  dut_companion_role: "function_checked_dut"
  strong_benchmark_claim: true
  checks:
    - "ramp_code_coverage"
    - "monotonic_reconstruction"
parity:
  reference: "spectre"
"""

    assert extract_sim_checks(checks_text) == [
        "ramp_code_coverage",
        "monotonic_reconstruction",
    ]
