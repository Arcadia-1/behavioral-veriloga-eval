from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

from main120_stable_checks import evaluate_main120_stable_check, sample_signal  # noqa: E402
from simulate_evas import check_cmp_strongarm, load_csv, normalize_rows_for_task  # noqa: E402


EVAS_MAIN120 = ROOT / "results/vabench-main-v1-main120-gold-evas-2026-05-08"
SPECTRE_MAIN120 = ROOT / "results/vabench-main-v1-main120-gold-spectre-jin-2026-05-08"


def _main120_csv(task_id: str, backend: str) -> Path:
    if backend == "evas":
        return EVAS_MAIN120 / task_id / "evas_output" / "tran.csv"
    if backend == "spectre":
        return SPECTRE_MAIN120 / task_id / "tran.csv"
    raise ValueError(backend)


def test_main120_p1_sequence_checkers_match_across_evas_and_spectre() -> None:
    expected_notes = {
        "vbm1_background_calibration_accumulator_dut": "accum_samples=0.450,0.490,0.570,0.610,0.530,0.530,0.570 expected=0.450,0.490,0.570,0.610,0.530,0.530,0.570 direction_ok=True in_range=True",
        "vbm1_barrel_pointer_window_dut": "window_sequence=12,23,03,01,12,23 expected=12,23,03,01,12,23",
        "vbm1_debounce_latch_dut": "debounce_early_low=LLLL late_high=HH",
        "vbm1_edge_detector_dut": "rising_edge_pulse_samples=HHHH low_window_samples=LLLLL",
        "vbm1_element_shuffler_dut": "active_sequence=1,2,3,0,1,2 expected=1,2,3,0,1,2",
        "vbm1_rotating_element_selector_dut": "active_sequence=1,2,3,0,1,2 expected=1,2,3,0,1,2",
        "vbm1_segmented_dac_dut": "dac_levels=0.000,0.060,0.120,0.420,0.720 expected=0.000,0.060,0.120,0.420,0.720 monotonic=True",
        "vbm1_strongarm_comparator_behavior_dut": "decision_samples=PPNN expected=PPNN",
        "vbm1_thermometer_dac_dut": "dac_levels=0.000,0.120,0.240,0.360,0.480,0.600,0.720,0.900 expected=0.000,0.120,0.240,0.360,0.480,0.600,0.720,0.900 max_err=0.000 monotonic=True full_scale_ok=True",
        "vbm1_thermometer_decoder_guarded_dut": "thermometer_sequence=-,-,0,01,012,012 expected=-,-,0,01,012,012",
    }

    for task_id, expected_note in expected_notes.items():
        evas = evaluate_main120_stable_check(task_id, _main120_csv(task_id, "evas"))
        spectre = evaluate_main120_stable_check(task_id, _main120_csv(task_id, "spectre"))

        assert evas == (True, expected_note)
        assert spectre == (True, expected_note)


def test_main120_p2_watch_checkers_match_across_evas_and_spectre() -> None:
    expected_notes = {
        "vbm1_leaky_hold_bugfix": "leaky_hold_samples=0.706,0.563,0.307,0.195,0.000,0.000 sample_captured=True decay_direction=True decay_amount=True reset_clear=True",
        "vbm1_one_shot_timer_bugfix": "pulse_high_windows=HHHHH pulse_low_windows=LLLLL reset_clear=True",
        "vbm1_track_hold_aperture_bugfix": "aperture_samples=0.100,0.350,0.600,0.250,0.700,0.400,0.800 expected=0.100,0.350,0.600,0.250,0.700,0.400,0.800 mismatches=0 span=0.700",
    }

    for task_id, expected_note in expected_notes.items():
        evas = evaluate_main120_stable_check(task_id, _main120_csv(task_id, "evas"))
        spectre = evaluate_main120_stable_check(task_id, _main120_csv(task_id, "spectre"))

        assert evas == (True, expected_note)
        assert spectre == (True, expected_note)


def test_cmp_strongarm_checker_uses_decision_samples_not_row_fractions() -> None:
    task_id = "vbm1_strongarm_comparator_behavior_dut"
    rows = normalize_rows_for_task("cmp_strongarm_smoke", load_csv(_main120_csv(task_id, "evas")))

    ok, note = check_cmp_strongarm(rows)

    assert ok
    assert note == "decision_samples=PPNN expected=PPNN"


def test_main120_sample_signal_rejects_out_of_range_samples() -> None:
    rows = [{"time": 1.0, "out": 0.2}, {"time": 2.0, "out": 0.8}]

    assert sample_signal(rows, "out", 0.5) is None
    assert sample_signal(rows, "out", 2.5) is None
    assert sample_signal(rows, "out", 1.5) == 0.5
