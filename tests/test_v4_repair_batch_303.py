from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

from checkers.common.issue109_factory import (  # noqa: E402
    VHI,
    VTH,
    _clip01,
    _cont_expected,
    _normalized_inputs,
    _sample_times,
)
from checkers.v4.registry import load_checker  # noqa: E402


NORMALIZATION_PROPERTY = "P_MEASURE_ANALOG_INPUTS_RELATIVE_TO_THE"

CONTINUOUS_CASES = [
    (
        "v4_251_weighted_balance_summer",
        "sum",
        "P_COMPUTE_THE_WEIGHTED_BALANCE_SUM_AS",
    ),
    (
        "v4_252_supply_qualified_window_flag",
        "window",
        "P_WHEN_VALID_DRIVE_OUT_VHI_CLIP01",
    ),
    (
        "v4_253_power_mode_clamped_mux",
        "mux",
        "P_USE_THE_TWO_CONTROL_LEVELS_AS",
    ),
    (
        "v4_254_bias_trim_affine_mapper",
        "gain",
        "P_COMPUTE_THE_BIAS_TRIM_AFFINE_VALUE",
    ),
    (
        "v4_255_reset_polarity_qualifier",
        "window",
        "P_DRIVE_OUT_VHI_CLIP01_X0_ASSERT",
    ),
    (
        "v4_256_multi_condition_enable_combiner",
        "reduction",
        "P_COUNT_THE_NUMBER_OF_NORMALIZED_INPUTS",
    ),
    (
        "v4_257_phase_mismatch_qualifier",
        "phase",
        "P_COMPUTE_CORE_CLIP01_0_5_X0",
    ),
    (
        "v4_258_priority_fault_code_driver",
        "priority",
        "P_ENCODE_THE_HIGHEST_PRIORITY_FAULT_CODE",
    ),
    (
        "v4_259_lane_validity_reduction_monitor",
        "reduction",
        "P_COUNT_HOW_MANY_OF_X0_X1",
    ),
]

CONTINUOUS_STATES = [
    {"x0": 0.10, "x1": 0.90, "x2": 0.20, "x3": 0.30, "c0": 0.00, "c1": 0.00, "en": 0.90},
    {"x0": 0.90, "x1": 0.10, "x2": 0.80, "x3": 0.70, "c0": 0.80, "c1": 0.20, "en": 0.90},
    {"x0": 0.50, "x1": 0.45, "x2": 0.40, "x3": 0.30, "c0": 0.80, "c1": 0.70, "en": 0.90},
    {"x0": 0.35, "x1": 0.36, "x2": 0.37, "x3": 0.38, "c0": 0.20, "c1": 0.20, "en": 0.00},
    {"x0": 0.65, "x1": 0.20, "x2": 0.60, "x3": 0.10, "c0": 0.30, "c1": 0.90, "en": 0.90},
]


def _property_count(note: str, property_id: str) -> int:
    match = re.search(rf"{re.escape(property_id)} mismatch_count=(\d+)", note)
    assert match is not None, note
    return int(match.group(1))


def _continuous_row(time_s: float, mode: str, state: dict[str, float]) -> dict[str, float]:
    vss = 0.04
    vdd = 1.03
    span = vdd - vss
    values = {
        "time": time_s,
        "in0": vss + span * state["x0"],
        "in1": vss + span * state["x1"],
        "in2": vss + span * state["x2"],
        "in3": vss + span * state["x3"],
        "ctrl0": VHI * state["c0"],
        "ctrl1": VHI * state["c1"],
        "vdd": vdd,
        "vss": vss,
        "en": state["en"],
    }
    values.update(_cont_expected(mode, values))
    return values


def _continuous_rows(
    mode: str,
    *,
    states: list[dict[str, float]] | None = None,
    start_s: float = 37.0e-9,
    stop_s: float = 143.0e-9,
) -> list[dict[str, float]]:
    chosen_states = states or CONTINUOUS_STATES
    rows = [_continuous_row(start_s, mode, chosen_states[0])]
    for index, time_s in enumerate(_sample_times([{"time": start_s}, {"time": stop_s}])):
        state = chosen_states[index % len(chosen_states)]
        for offset_s in (-0.20e-9, 0.0, 0.20e-9):
            rows.append(_continuous_row(time_s + offset_s, mode, state))
    rows.append(_continuous_row(stop_s, mode, chosen_states[-1]))
    return sorted(rows, key=lambda row: row["time"])


@pytest.mark.parametrize(("checker_id", "mode", "function_property_id"), CONTINUOUS_CASES)
def test_batch303_continuous_checkers_are_shifted_and_property_diagnostic(
    checker_id: str,
    mode: str,
    function_property_id: str,
) -> None:
    checker = load_checker(checker_id)
    assert checker is not None

    passed, note = checker(_continuous_rows(mode))

    assert passed, note
    assert _property_count(note, NORMALIZATION_PROPERTY) == 0
    assert _property_count(note, function_property_id) == 0


def test_batch303_continuous_diagnostics_count_observable_mismatches() -> None:
    checker = load_checker("v4_251_weighted_balance_summer")
    assert checker is not None
    rows = _continuous_rows("sum")
    for row in rows:
        if row["en"] > VTH:
            row["out"] = 0.0

    passed, note = checker(rows)

    assert not passed
    assert _property_count(note, NORMALIZATION_PROPERTY) > 0
    assert _property_count(note, "P_COMPUTE_THE_WEIGHTED_BALANCE_SUM_AS") > 0


def test_batch303_continuous_checkers_reject_insufficient_excitation() -> None:
    checker = load_checker("v4_251_weighted_balance_summer")
    assert checker is not None
    low_flag_state = CONTINUOUS_STATES[0]
    disabled_state = {**CONTINUOUS_STATES[0], "en": 0.0}

    passed, note = checker(_continuous_rows("sum", states=[low_flag_state, disabled_state]))

    assert not passed
    assert "insufficient_flag_dynamic_range" in note


def _clocked_values(state: dict[str, float]) -> dict[str, float]:
    vss = 0.02
    vdd = vss + state.get("span", 1.02)
    span = vdd - vss
    return {
        "rst": state["rst"],
        "in0": vss + span * state["x0"],
        "in1": vss + span * state["x1"],
        "in2": vss + span * state.get("x2", 0.25),
        "in3": vss + span * state.get("x3", 0.75),
        "ctrl0": VHI * state.get("c0", 0.0),
        "ctrl1": VHI * state.get("c1", 0.0),
        "vdd": vdd,
        "vss": vss,
        "en": state["en"],
    }


def _clocked_expected(values: dict[str, float]) -> dict[str, float]:
    state = _normalized_inputs(values)
    if values["rst"] > VTH or state["valid"] <= 0.5:
        return {"out": 0.0, "flag": 0.0, "metric": 0.0}
    decision = state["x0"] > state["x1"]
    return {
        "out": VHI if decision else 0.0,
        "flag": VHI if decision else 0.0,
        "metric": VHI * _clip01(abs(state["x0"] - state["x1"])),
    }


def _clocked_row(
    time_s: float,
    clk: float,
    values: dict[str, float],
    outputs: dict[str, float],
) -> dict[str, float]:
    return {"time": time_s, "clk": clk, **values, **outputs}


def _clocked_rows(*, corrupt_clear: bool = False) -> list[dict[str, float]]:
    states = [
        {"rst": 0.90, "en": 0.90, "x0": 0.20, "x1": 0.80},
        {"rst": 0.90, "en": 0.90, "x0": 0.80, "x1": 0.20},
        {"rst": 0.00, "en": 0.00, "x0": 0.90, "x1": 0.10},
        {"rst": 0.00, "en": 0.90, "x0": 0.90, "x1": 0.10},
        {"rst": 0.00, "en": 0.90, "x0": 0.20, "x1": 0.80},
        {"rst": 0.00, "en": 0.90, "x0": 0.60, "x1": 0.20, "span": 0.42},
        {"rst": 0.00, "en": 0.90, "x0": 0.55, "x1": 0.45},
        {"rst": 0.00, "en": 0.90, "x0": 0.80, "x1": 0.10, "span": 1.48},
        {"rst": 0.00, "en": 0.90, "x0": 0.30, "x1": 0.70},
        {"rst": 0.00, "en": 0.90, "x0": 0.85, "x1": 0.15},
        {"rst": 0.00, "en": 0.90, "x0": 0.40, "x1": 0.60},
        {"rst": 0.00, "en": 0.90, "x0": 0.75, "x1": 0.25},
    ]
    rows: list[dict[str, float]] = []
    previous = {"out": 0.0, "flag": 0.0, "metric": 0.0}
    start_s = 51.0e-9
    period_s = 3.7e-9
    for index, state in enumerate(states):
        edge_s = start_s + index * period_s
        values = _clocked_values(state)
        expected = _clocked_expected(values)
        output_values = expected
        if corrupt_clear and (values["rst"] > VTH or values["en"] <= VTH):
            output_values = {"out": VHI, "flag": VHI, "metric": VHI}

        rows.extend(
            [
                _clocked_row(edge_s - 1.0e-12, 0.0, values, previous),
                _clocked_row(edge_s, VHI, values, previous),
                _clocked_row(edge_s + 1.0e-12, VHI, values, previous),
                _clocked_row(edge_s + 0.12e-9, VHI, values, output_values),
                _clocked_row(edge_s + 0.45 * period_s, VHI, values, output_values),
                _clocked_row(edge_s + 0.55 * period_s, 0.0, values, output_values),
            ]
        )
        previous = output_values
    return sorted(rows, key=lambda row: row["time"])


def test_batch303_clocked_checker_is_event_relative_and_property_diagnostic() -> None:
    checker = load_checker("v4_260_comparator_decision_capture")
    assert checker is not None

    passed, note = checker(_clocked_rows())

    assert passed, note
    assert _property_count(note, NORMALIZATION_PROPERTY) == 0
    assert _property_count(note, "P_INITIALIZE_ALL_OBSERVABLE_STATE_TO_0") == 0


def test_batch303_clocked_diagnostics_count_clear_mismatches() -> None:
    checker = load_checker("v4_260_comparator_decision_capture")
    assert checker is not None

    passed, note = checker(_clocked_rows(corrupt_clear=True))

    assert not passed
    assert _property_count(note, NORMALIZATION_PROPERTY) > 0
    assert _property_count(note, "P_INITIALIZE_ALL_OBSERVABLE_STATE_TO_0") > 0


def _task303_pwl_value(points: list[tuple[float, float]], time_s: float) -> float:
    if time_s <= points[0][0]:
        return points[0][1]
    for index in range(1, len(points)):
        t0, v0 = points[index - 1]
        t1, v1 = points[index]
        if time_s <= t1:
            if t1 == t0:
                return v1
            alpha = (time_s - t0) / (t1 - t0)
            return v0 + alpha * (v1 - v0)
    return points[-1][1]


def _task303_affine_points(
    points: list[tuple[float, float]], *, scale: float, shift_s: float
) -> list[tuple[float, float]]:
    return [(shift_s + time_s * scale, value) for time_s, value in points]


def _task303_expected(vinp: float, vinn: float, enable: float) -> dict[str, float]:
    if enable <= 0.45:
        return {
            "voutp": 0.45,
            "voutn": 0.45,
            "gm_metric": 0.0,
            "limit_flag": 0.0,
        }
    diff_limit = 120e-3
    diff = vinp - vinn
    limited = diff / (1.0 + abs(diff) / diff_limit)
    sep = 4.0 * limited
    voutp = max(0.0, min(0.9, 0.45 + 0.5 * sep))
    voutn = max(0.0, min(0.9, 0.45 - 0.5 * sep))
    return {
        "voutp": voutp,
        "voutn": voutn,
        "gm_metric": 0.9 * diff_limit / (diff_limit + abs(diff)),
        "limit_flag": 0.9 if abs(diff) > diff_limit else 0.0,
    }


def _task303_affine_rows(*, corrupt_common_mode: bool = False) -> list[dict[str, float]]:
    scale = 1.37
    shift_s = 2.0e-9
    stop_s = shift_s + 76e-9 * scale
    vinp_points = _task303_affine_points(
        [
            (0.0, 0.30),
            (8e-9, 0.30),
            (16e-9, 0.70),
            (28e-9, 0.70),
            (38e-9, 0.20),
            (48e-9, 0.20),
            (62e-9, 0.62),
            (76e-9, 0.62),
        ],
        scale=scale,
        shift_s=shift_s,
    )
    vinn_points = _task303_affine_points(
        [
            (0.0, 0.52),
            (8e-9, 0.52),
            (16e-9, 0.40),
            (28e-9, 0.40),
            (38e-9, 0.58),
            (48e-9, 0.58),
            (62e-9, 0.50),
            (76e-9, 0.50),
        ],
        scale=scale,
        shift_s=shift_s,
    )
    enable_points = _task303_affine_points(
        [
            (0.0, 0.0),
            (4e-9, 0.0),
            (4.1e-9, 0.9),
            (50e-9, 0.9),
            (50.1e-9, 0.0),
            (57e-9, 0.0),
            (57.1e-9, 0.9),
            (76e-9, 0.9),
        ],
        scale=scale,
        shift_s=shift_s,
    )
    rows: list[dict[str, float]] = [
        {
            "time": 0.0,
            "vinp": 0.30,
            "vinn": 0.52,
            "bias": 0.45,
            "enable": 0.0,
            **_task303_expected(0.30, 0.52, 0.0),
        }
    ]
    tick_s = 500e-12
    probe_offsets = (300e-12, 450e-12)
    tick = 0
    while tick * tick_s + probe_offsets[-1] <= stop_s:
        event_time = tick * tick_s
        vinp = _task303_pwl_value(vinp_points, event_time)
        vinn = _task303_pwl_value(vinn_points, event_time)
        enable = _task303_pwl_value(enable_points, event_time)
        outputs = _task303_expected(vinp, vinn, enable)
        if corrupt_common_mode and enable > 0.45:
            outputs = {**outputs, "voutp": 0.45, "voutn": 0.45}
        for time_s in (event_time, *(event_time + offset for offset in probe_offsets)):
            rows.append(
                {
                    "time": time_s,
                    "vinp": _task303_pwl_value(vinp_points, time_s),
                    "vinn": _task303_pwl_value(vinn_points, time_s),
                    "bias": 0.45,
                    "enable": _task303_pwl_value(enable_points, time_s),
                    **outputs,
                }
            )
        tick += 1
    return sorted(rows, key=lambda row: row["time"])


def test_v4_303_affine_stimulus_uses_unscaled_dut_timer_grid() -> None:
    checker = load_checker("v4_303_differential_pair_gm_limiter")
    assert checker is not None

    correct_passed, correct_note = checker(_task303_affine_rows())

    assert correct_passed, correct_note


def test_v4_303_affine_stimulus_still_rejects_common_mode_output_fault() -> None:
    checker = load_checker("v4_303_differential_pair_gm_limiter")
    assert checker is not None

    passed, note = checker(_task303_affine_rows(corrupt_common_mode=True))

    assert not passed
    assert _property_count(note, "P_SCALE_SMALL_SIGNAL_OUTPUT_SEPARATION_BY") > 0
