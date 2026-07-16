from __future__ import annotations

from collections.abc import Callable
import math
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

from checkers.v4.registry import load_checker
from checkers.v4.stimulus_relative import transformed_rows


Row = dict[str, float]
TraceFactory = Callable[[], list[Row]]


def _assert_event_relative(checker_id: str, rows: list[Row]) -> None:
    checker = load_checker(checker_id)
    assert checker is not None
    for trace in (rows, transformed_rows(rows)):
        passed, detail = checker(trace)
        assert passed, detail
        assert "checked=" in detail
        assert "mismatch_count=0" in detail
        assert "secret" not in detail.lower()


def _clocked_rows(
    scenarios: list[dict[str, float]],
    update: Callable[[dict[str, float]], dict[str, float]],
    *,
    signal_names: tuple[str, ...],
    start_s: float = 100e-9,
    period_s: float = 10e-9,
    clock: str = "clk",
    low: float = 0.0,
    high: float = 0.9,
) -> list[Row]:
    rows: list[Row] = []
    outputs = update(scenarios[0])
    for cycle, scenario in enumerate(scenarios):
        edge_s = start_s + cycle * period_s
        base = {name: 0.0 for name in signal_names}
        base.update(outputs)
        rows.append({**base, **scenario, "time": edge_s - 0.25e-9, clock: low})
        edge = {**base, **scenario, "time": edge_s, clock: high}
        rows.append(edge)
        outputs = update(edge)
        for offset_s in (1.6e-9, 3.5e-9, 8.0e-9):
            rows.append({**base, **scenario, **outputs, "time": edge_s + offset_s, clock: high})
        rows.append({**base, **scenario, **outputs, "time": edge_s + 9.0e-9, clock: low})
    return rows


def _rails(code: int, bits: list[str], *, high: float = 0.9, low: float = 0.0) -> dict[str, float]:
    return {signal: high if code & (1 << index) else low for index, signal in enumerate(bits)}


def _trace_021() -> list[Row]:
    state = 0.45

    def update(edge: Row) -> dict[str, float]:
        nonlocal state
        if edge["rst"] > 0.45:
            state = 0.45
            metric = 0.0
        else:
            error_v = edge["vin"] - 0.45
            if error_v > 0.05:
                state += 0.06
                metric = 0.9
            elif error_v < -0.05:
                state -= 0.06
                metric = 0.9
            else:
                metric = 0.0
        state = min(0.85, max(0.05, state))
        return {"out": state, "metric": metric}

    scenarios = [
        {"rst": 0.9, "vin": 0.45},
        {"rst": 0.0, "vin": 0.62},
        {"rst": 0.0, "vin": 0.28},
        {"rst": 0.0, "vin": 0.47},
    ]
    return _clocked_rows(scenarios, update, signal_names=("clk", "rst", "vin", "out", "metric"))


def _trace_022() -> list[Row]:
    state = 0.45

    def update(edge: Row) -> dict[str, float]:
        nonlocal state
        if edge["rst"] > 0.45:
            state = 0.45
            metric = 0.45
        elif edge["up"] > 0.45 and edge["dn"] <= 0.45:
            state += 0.06
            metric = 0.75
        elif edge["dn"] > 0.45 and edge["up"] <= 0.45:
            state -= 0.06
            metric = 0.15
        else:
            metric = 0.45
        state = min(0.85, max(0.05, state))
        return {"vctrl": state, "metric": metric}

    scenarios = [
        {"rst": 0.9, "up": 0.0, "dn": 0.0},
        {"rst": 0.0, "up": 0.9, "dn": 0.0},
        {"rst": 0.0, "up": 0.0, "dn": 0.9},
        {"rst": 0.0, "up": 0.0, "dn": 0.0},
    ]
    return _clocked_rows(
        scenarios,
        update,
        signal_names=("clk", "rst", "up", "dn", "vctrl", "metric"),
    )


def _trace_023() -> list[Row]:
    bits = ["dout0", "dout1", "dout2"]

    def update(edge: Row) -> dict[str, float]:
        span = edge["vdd"] - edge["vss"]
        code = min(7, max(0, math.floor(8.0 * (edge["vin"] - edge["vss"]) / span)))
        return _rails(code, bits, high=edge["vdd"], low=edge["vss"])

    scenarios = []
    for code in range(8):
        normalized = 0.25 if code == 0 else 7.75 if code == 7 else code + 0.25
        scenarios.append({"vin": 0.9 * normalized / 8.0, "vdd": 0.9, "vss": 0.0})
    return _clocked_rows(scenarios, update, signal_names=("clk", "vin", "vdd", "vss", *bits))


def _trace_024() -> list[Row]:
    rows: list[Row] = []
    start_s = 100e-9
    held = 0.25
    for cycle, sample_in in enumerate((0.25, 0.72, 0.48, 0.65)):
        edge_s = start_s + cycle * 10e-9
        base = {"vdd": 1.0, "vss": 0.1}
        rows.append({**base, "time": edge_s - 0.25e-9, "clk": 0.1, "in": sample_in, "out": held})
        rows.append({**base, "time": edge_s, "clk": 1.0, "in": sample_in, "out": held})
        held = sample_in
        rows.append({**base, "time": edge_s + 1.6e-9, "clk": 1.0, "in": sample_in, "out": held})
        rows.append({**base, "time": edge_s + 3.5e-9, "clk": 1.0, "in": sample_in + 0.08, "out": held})
        rows.append({**base, "time": edge_s + 4.2e-9, "clk": 0.1, "in": sample_in + 0.12, "out": held})
        rows.append({**base, "time": edge_s + 8.0e-9, "clk": 0.1, "in": sample_in - 0.05, "out": held})
    return rows


def _trace_025() -> list[Row]:
    bits = ["b0", "b1", "b2", "b3"]
    values = [
        (0.0, [0.0, 0.0, 0.0, 0.0]),
        (3e-9, [0.0, 0.0, 0.0, 0.0]),
        (8e-9, [0.6, 0.0, 0.0, 0.0]),
        (11e-9, [0.6, 0.0, 0.0, 0.0]),
        (16e-9, [0.9, 0.9, 0.9, 0.0]),
        (19e-9, [0.9, 0.9, 0.9, 0.0]),
        (24e-9, [0.9, 0.9, 0.9, 0.9]),
        (34e-9, [0.9, 0.9, 0.9, 0.9]),
    ]
    weights = [1.00, 2.02, 3.96, 8.08]
    rows: list[Row] = []
    for time_s, bit_values in values:
        active = sum(weight for weight, value in zip(weights, bit_values) if value > 0.45)
        out = 0.9 * active / sum(weights)
        rows.append({"time": 100e-9 + time_s, "out": out, **dict(zip(bits, bit_values))})
    return rows


def _trace_026() -> list[Row]:
    rows: list[Row] = []
    phases = [0.0, 0.25, 0.50, 0.75, 0.0, 0.25, 0.50, 0.75, 0.0]
    for index, phase in enumerate(phases):
        for offset_s in (0.0, 0.7e-9, 1.4e-9, 2.1e-9, 2.8e-9, 3.6e-9, 4.4e-9, 5.2e-9):
            time_s = 100e-9 + index * 7e-9 + offset_s
            rows.append(
                {
                    "time": time_s,
                    "VDD": 0.9,
                    "VSS": 0.0,
                    "phase_out": 0.9 * phase,
                    "clk_out": 0.9 if phase < 0.5 else 0.0,
                }
            )
    return rows


def _trace_027() -> list[Row]:
    code_bits = ["code_0", "code_1", "code_2", "code_3"]
    ptr_bits = [f"ptr_{index}" for index in range(16)]
    cell_bits = [f"cell_en_{index}" for index in range(16)]
    pointer = 0
    previous_helper = 0
    outputs = {**_rails(0, code_bits), **_rails(1, ptr_bits), **_rails(1, cell_bits)}
    rows: list[Row] = []
    scenarios = [
        (0.0, 0),
        (0.9, 3),
        (0.9, 4),
        (0.9, 5),
        (0.9, 6),
        (0.9, 7),
        (0.9, 8),
    ]
    for cycle, (rst_ni, helper_code) in enumerate(scenarios):
        edge_s = 100e-9 + cycle * 10e-9
        base = {"clk_i": 0.0, "rst_ni": rst_ni, "vin_node": float(helper_code), **outputs}
        rows.append({"time": edge_s - 0.25e-9, **base})
        rows.append({"time": edge_s, **base, "clk_i": 0.9})
        if rst_ni < 0.45:
            pointer = 0
            effective = 0
        else:
            effective = previous_helper
            pointer = (pointer + effective) % 16
        cells = 0
        for offset in range(effective + 1):
            cells |= 1 << ((pointer - offset) % 16)
        outputs = {
            **_rails(helper_code, code_bits),
            **_rails(1 << pointer, ptr_bits),
            **_rails(cells, cell_bits),
        }
        previous_helper = helper_code
        for offset_s in (1.6e-9, 3.5e-9, 8.0e-9):
            rows.append({"time": edge_s + offset_s, "clk_i": 0.9, "rst_ni": rst_ni, "vin_node": float(helper_code), **outputs})
    return rows


def _trace_028() -> list[Row]:
    state1 = 0.45
    state2 = 0.45

    def update(edge: Row) -> dict[str, float]:
        nonlocal state1, state2
        if edge["rst"] > 0.45:
            state1 = 0.45
            state2 = 0.45
        else:
            target = min(0.9, max(0.0, 1.8 * (edge["vin"] - 0.45) + 0.45))
            state1 += 0.18 * (target - state1)
            state2 += 0.18 * (state1 - state2)
        return {"out": min(0.9, max(0.0, state2)), "metric": state1 - state2 + 0.45}

    scenarios = [
        {"rst": 0.9, "vin": 0.45},
        {"rst": 0.0, "vin": 0.80},
        {"rst": 0.0, "vin": 0.78},
        {"rst": 0.0, "vin": 0.10},
        {"rst": 0.0, "vin": 0.12},
    ]
    return _clocked_rows(scenarios, update, signal_names=("clk", "rst", "vin", "out", "metric"))


def _trace_029() -> list[Row]:
    rows: list[Row] = []
    for offset_ns, diff, high in (
        (0.0, -0.010, False),
        (5.0, -0.003, False),
        (10.0, 0.000, False),
        (15.0, 0.004, False),
        (16.0, 0.006, False),
        (19.0, 0.010, True),
        (25.0, 0.003, True),
        (30.0, 0.000, True),
        (35.0, -0.004, True),
        (36.0, -0.006, True),
        (39.0, -0.010, False),
        (45.0, -0.003, False),
        (50.0, 0.000, False),
    ):
        vdd = 0.9
        vss = 0.0
        rows.append(
            {
                "time": 100e-9 + offset_ns * 1e-9,
                "vdd": vdd,
                "vss": vss,
                "vinp": 0.45 + 0.5 * diff,
                "vinn": 0.45 - 0.5 * diff,
                "out_p": vdd if high else vss,
                "out_n": vss if high else vdd,
            }
        )
    return rows


def _trace_030() -> list[Row]:
    state = 0.60

    def update(edge: Row) -> dict[str, float]:
        nonlocal state
        if edge["rst"] > 0.45:
            state = 0.60
            metric = 0.9
        else:
            load = min(0.9, max(0.0, edge["vin"]))
            target = 0.62 - 0.055 * load
            state += 0.35 * (target - state)
            state = min(0.75, max(0.25, state))
            metric = min(0.9, max(0.0, 0.9 - 4.0 * abs(state - target)))
        return {"out": state, "metric": metric}

    scenarios = [
        {"rst": 0.9, "vin": 0.4},
        {"rst": 0.0, "vin": 0.0},
        {"rst": 0.0, "vin": 0.9},
        {"rst": 0.0, "vin": 0.2},
    ]
    return _clocked_rows(scenarios, update, signal_names=("clk", "rst", "vin", "out", "metric"))


@pytest.mark.parametrize(
    ("checker_id", "trace_factory"),
    [
        ("v4_021_calibration_deadband_controller", _trace_021),
        ("v4_022_charge_pump_abstraction", _trace_022),
        ("v4_023_clocked_adc_quantizer", _trace_023),
        ("v4_024_clocked_sample_and_hold", _trace_024),
        ("v4_025_dac_mismatch_unit_weighting_model", _trace_025),
        ("v4_026_digital_phase_accumulator_with_modulo_wrap", _trace_026),
        ("v4_027_dwa_dem_encoder", _trace_027),
        ("v4_028_higher_order_filter", _trace_028),
        ("v4_029_hysteresis_comparator", _trace_029),
        ("v4_030_ldo_regulator_macro_model", _trace_030),
    ],
)
def test_batch03_checkers_accept_public_event_relative_traces(
    checker_id: str,
    trace_factory: TraceFactory,
) -> None:
    _assert_event_relative(checker_id, trace_factory())


def test_batch03_checker_diagnostics_are_structured_and_redacted() -> None:
    checker = load_checker("v4_021_calibration_deadband_controller")
    assert checker is not None
    rows = _trace_021()
    for row in rows:
        row["out"] = 0.0
    passed, detail = checker(rows)
    assert not passed
    assert "v4_021_calibration_deadband_controller" in detail
    assert "mismatch_count=" in detail
    assert "sample_time=" in detail
    assert "metric_gap=" in detail
    assert "secret" not in detail.lower()
