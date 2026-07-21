from __future__ import annotations

import copy
from pathlib import Path

from runners.checkers.v4.registry import load_checker


TARGET_CHECKERS = tuple(
    f"v4_{family}_{name}"
    for family, name in (
        (371, "bandgap_startup_trim_system"),
        (372, "buck_converter_controller_macro"),
        (373, "charge_pump_voltage_multiplier_controller"),
        (374, "crystal_oscillator_startup_monitor"),
        (375, "nonoverlap_clock_generator"),
        (376, "pwm_ramp_modulator_front_end"),
        (377, "bidirectional_hybrid_macro"),
        (378, "current_limited_regulator_macro"),
        (379, "periodic_sampler_aperture_metric"),
        (380, "am_modulator_source_macro"),
    )
)


def _shift_and_scale(rows: list[dict[str, float]], scale: float = 1.37) -> list[dict[str, float]]:
    shifted = copy.deepcopy(rows)
    for row in shifted:
        row["time"] = scale * row["time"] + 2e-9
    return shifted


def _sampler_rows() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    hold = 0.0
    metric = 0.0
    valid = 0.0
    values = (0.60, 0.60, 0.20, 0.20, 0.75, 0.75, 0.30, 0.30)
    sample_enabled = (True, True, False, True, True, False, True, True)
    for index, (vin, enabled) in enumerate(zip(values, sample_enabled)):
        edge = (2.0 + 6.0 * index) * 1e-9
        base = {
            "time": edge - 0.1e-9,
            "vin": vin,
            "clk": 0.0,
            "rst": 0.9 if index == 0 else 0.0,
            "sample_en": 0.9 if enabled else 0.0,
            "vhold": hold,
            "aperture_metric": 0.0,
            "valid": valid,
        }
        rows.append(base)
        if index == 0:
            hold = 0.0
            valid = 0.0
            metric = 0.0
        elif enabled:
            metric = min(0.9, 0.5 * abs(vin - hold))
            hold = vin
            valid = 0.9
        rows.append({
            **base,
            "time": edge,
            "clk": 0.9,
        })
        rows.append({
            **base,
            "time": edge + 1.0e-9,
            "clk": 0.9,
            "vhold": hold,
            "aperture_metric": metric,
            "valid": valid,
        })
    return rows


def test_all_batch38_checkers_fail_closed_with_actionable_empty_trace_details() -> None:
    for checker_id in TARGET_CHECKERS:
        checker = load_checker(checker_id)
        assert checker is not None
        passed, detail = checker([])
        assert not passed
        assert detail


def test_periodic_sampler_gold_is_invariant_to_shift_and_scale() -> None:
    checker = load_checker("v4_379_periodic_sampler_aperture_metric")
    assert checker is not None
    rows = _sampler_rows()
    assert checker(rows)[0]
    assert checker(_shift_and_scale(rows))[0]


def test_batch38_removed_absolute_time_windows_from_checkers() -> None:
    root = Path(__file__).resolve().parents[1] / "runners" / "checkers" / "v4"
    forbidden = ("5e-9", "15e-9", "82e-9", "84e-9", "edge_t > 1e-9")
    for family in (374, 375, 380):
        text = (root / f"task_{family}.py").read_text(encoding="utf-8")
        assert all(token not in text for token in forbidden)
