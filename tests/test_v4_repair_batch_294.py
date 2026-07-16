from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))


BATCH_294_CHECKERS = (
    "v4_161_dac_restore_10bit_offset",
    "v4_162_flash_data_align_pipeline",
    "v4_163_cyclic_decoder_10b",
    "v4_164_ideal_adc_out_7bits",
    "v4_165_va_lx_dac_ideal_4b",
    "v4_166_l2_cdac_4b_residue",
    "v4_167_ideal_clkmux_8channel",
    "v4_168_dac_ideal_4b_offset",
    "v4_169_linear_pfd_gain",
    "v4_170_comparator_delay_overdrive_meter",
)


def test_batch_294_checkers_report_structured_missing_trace_diagnostics() -> None:
    from checkers.v4.registry import load_checker

    for checker_id in BATCH_294_CHECKERS:
        checker = load_checker(checker_id)
        assert checker is not None, checker_id
        passed, detail = checker([])
        assert not passed, checker_id
        assert "property_id=" in detail, detail
        assert "category=invalid_trace" in detail, detail
        assert "event=full_trace" in detail, detail


def test_linear_pfd_gain_checker_uses_shifted_stable_windows() -> None:
    from checkers.v4.registry import load_checker

    checker = load_checker("v4_169_linear_pfd_gain")
    assert checker is not None
    rows = [
        {"time": 100e-9, "in1": 0.2, "in2": 0.1, "out": 2.03 * (0.2 - 0.1)},
        {"time": 110e-9, "in1": 0.2, "in2": 0.1, "out": 2.03 * (0.2 - 0.1)},
        {"time": 110.1e-9, "in1": 0.4, "in2": 0.3, "out": 2.03 * (0.4 - 0.3)},
        {"time": 120e-9, "in1": 0.4, "in2": 0.3, "out": 2.03 * (0.4 - 0.3)},
        {"time": 120.1e-9, "in1": 0.1, "in2": 0.5, "out": 2.03 * (0.1 - 0.5)},
        {"time": 130e-9, "in1": 0.1, "in2": 0.5, "out": 2.03 * (0.1 - 0.5)},
    ]
    passed, detail = checker(rows)
    assert passed, detail
