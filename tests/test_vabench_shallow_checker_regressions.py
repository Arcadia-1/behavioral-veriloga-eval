from __future__ import annotations

import json
from pathlib import Path

from runners.vabench_release_paths import release_form_dir


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
REPORT = PACKAGE_ROOT / "reports" / "content_contract_audit.json"

SHALLOW_DUT_COMPANIONS: set[str] = set()

PROMOTED_FUNCTION_CHECKED_DUTS = {
    "vbr1_l1_burst_clock_source",
    "vbr1_l1_clocked_adc_quantizer",
    "vbr1_l1_clocked_sample_and_hold",
    "vbr1_l1_sample_and_hold_with_droop_leakage",
    "vbr1_l1_digital_phase_accumulator_with_modulo_wrap",
    "vbr1_l1_dither_or_noise_like_deterministic_source",
    "vbr1_l1_dwa_dem_encoder",
    "vbr1_l1_higher_order_filter",
    "vbr1_l1_hysteresis_comparator",
    "vbr1_l1_pfd_small_phase_error_response",
    "vbr1_l1_propagation_delay_comparator",
    "vbr1_l1_ramp_or_step_source",
    "vbr1_l1_serializer_frame_aligner",
    "vbr1_l1_soft_hysteretic_limiter",
    "vbr1_l1_threshold_comparator",
    "vbr1_l1_unit_element_thermometer_dac",
    "vbr1_l1_voltage_gain_amplifier",
    "vbr1_l1_window_comparator_detector",
    "vbr1_l1_xor_phase_detector",
}

NEWLY_TEMPLATE_FUNCTION_CHECKED_DUTS = PROMOTED_FUNCTION_CHECKED_DUTS - {
    "vbr1_l1_pfd_small_phase_error_response",
    "vbr1_l1_sample_and_hold_with_droop_leakage",
    "vbr1_l1_unit_element_thermometer_dac",
}


def test_unresolved_shallow_dut_companions_stay_in_manual_review() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    shallow = [item for item in report["findings"] if item["kind"] == "shallow_generic_checker"]
    auxiliary = [item for item in report["findings"] if item["kind"] == "auxiliary_companion_checker"]
    shallow_ids = {item["entry_id"] for item in shallow}

    assert shallow_ids == SHALLOW_DUT_COMPANIONS
    assert not (shallow_ids & PROMOTED_FUNCTION_CHECKED_DUTS)
    assert auxiliary == []


def test_review_required_dut_companion_checks_do_not_claim_function_strength() -> None:
    assert SHALLOW_DUT_COMPANIONS == set()
    for entry_id in SHALLOW_DUT_COMPANIONS:
        checks_path = release_form_dir(PACKAGE_ROOT / "tasks", entry_id, "dut") / "checks.yaml"
        text = checks_path.read_text(encoding="utf-8")

        assert 'dut_companion_role: "function_checked_dut"' not in text
        assert "strong_benchmark_claim: true" not in text
        assert "auxiliary_companion_not_counted_as_strong_claim" not in text
        assert "behavioral_module_present" in text
        assert "companion_testbench_available" in text
        assert "voltage_domain_outputs" in text


def test_review_required_dut_prompts_remain_visible_as_companion_risks() -> None:
    assert SHALLOW_DUT_COMPANIONS == set()
    for entry_id in SHALLOW_DUT_COMPANIONS:
        prompt_path = release_form_dir(PACKAGE_ROOT / "tasks", entry_id, "dut") / "prompt.md"
        text = prompt_path.read_text(encoding="utf-8")
        lowered = text.lower()

        assert "DUT Companion" in text
        assert "materialized from the already source-controlled `e2e`" in text
        assert "preserve the public module name and ports" in lowered


def test_promoted_function_checked_duts_have_specific_public_contracts() -> None:
    for entry_id in PROMOTED_FUNCTION_CHECKED_DUTS:
        dut_dir = release_form_dir(PACKAGE_ROOT / "tasks", entry_id, "dut")
        prompt_path = dut_dir / "prompt.md"
        checks_path = dut_dir / "checks.yaml"
        prompt = prompt_path.read_text(encoding="utf-8")
        checks = checks_path.read_text(encoding="utf-8")

        assert "DUT Companion" not in prompt
        assert "behavioral_module_present" not in checks
        if entry_id in NEWLY_TEMPLATE_FUNCTION_CHECKED_DUTS:
            assert 'dut_companion_role: "function_checked_dut"' in checks
            assert "strong_benchmark_claim: true" in checks
        assert "sim_correct:" in checks


def test_duplicate_clocked_comparator_is_removed_from_release_package() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    excluded = report["content_excluded_entries"]
    shallow_ids = {item["entry_id"] for item in report["findings"] if item["kind"] == "shallow_generic_checker"}
    task_dir = PACKAGE_ROOT / "tasks" / "CT02_comparators_and_decision_circuits" / "vbr1_l1_clocked_comparator"

    assert not task_dir.exists()
    assert "vbr1_l1_clocked_comparator" not in excluded
    assert "vbr1_l1_clocked_comparator" not in shallow_ids
