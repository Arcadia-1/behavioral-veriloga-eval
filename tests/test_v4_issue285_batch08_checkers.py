from __future__ import annotations

import math
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))


def _bias_target(vin: float) -> float:
    return min(0.82, max(0.28, 0.28 + 0.55 * ((vin - 0.25) / 0.65)))


def test_v4_073_bias_checker_uses_observed_clock_events_not_absolute_windows() -> None:
    from checkers.v4.registry import load_checker

    checker = load_checker("v4_073_bias_voltage_generator_with_enable_trim")
    assert checker is not None

    rows: list[dict[str, float]] = []
    start_s = 250.0e-9
    period = 2.0e-9
    state = 0.0
    vin_by_cycle = (0.10, 0.10, 0.35, 0.35, 0.75, 0.75, 0.10, 0.55, 0.55)
    for index, vin in enumerate(vin_by_cycle):
        edge_t = start_s + index * period
        rst = 0.9 if index < 2 else 0.0
        rows.append({"time": edge_t - 0.10 * period, "clk": 0.0, "rst": rst, "vin": vin, "out": state, "metric": 0.0})
        rows.append({"time": edge_t, "clk": 0.9, "rst": rst, "vin": vin, "out": state, "metric": 0.0})
        if rst > 0.45 or vin < 0.25:
            state = 0.0
            metric = 0.0
        else:
            state += 0.45 * (_bias_target(vin) - state)
            metric = 0.9
        rows.append({"time": edge_t + 0.35 * period, "clk": 0.9, "rst": rst, "vin": vin, "out": state, "metric": metric})
        rows.append({"time": edge_t + 0.75 * period, "clk": 0.0, "rst": rst, "vin": vin, "out": state, "metric": metric})

    passed, detail = checker(rows)
    assert passed, detail
    assert "P_CLOCKED_UPDATE mismatch_count=0" in detail


def _prbs_next(code: int) -> int:
    feedback = ((code >> 6) & 1) ^ ((code >> 5) & 1)
    return ((code & 0x3F) << 1) | feedback


def _state_row(time_s: float, clk: float, rst_n: float, en: float, code: int) -> dict[str, float]:
    row = {
        "time": time_s,
        "clk": clk,
        "rst_n": rst_n,
        "en": en,
        "serial_out": 0.9 if (code >> 6) & 1 else 0.0,
    }
    for bit in range(7):
        row[f"state_{bit}"] = 0.9 if (code >> bit) & 1 else 0.0
    return row


def test_v4_078_prbs_checker_anchors_post_reset_to_observed_release() -> None:
    from checkers.v4.registry import load_checker

    checker = load_checker("v4_078_lfsr_prbs_generator")
    assert checker is not None

    rows: list[dict[str, float]] = []
    start_s = 400.0e-9
    period = 1.0e-9
    code = 0x5A
    for index in range(32):
        edge_t = start_s + index * period
        rst_n = 0.0 if index < 3 else 0.9
        rows.append(_state_row(edge_t - 0.10 * period, 0.0, rst_n, 0.9, code))
        rows.append(_state_row(edge_t, 0.9, rst_n, 0.9, code))
        if rst_n <= 0.45:
            code = 0x5A
        else:
            code = _prbs_next(code)
        rows.append(_state_row(edge_t + 0.25 * period, 0.9, rst_n, 0.9, code))
        rows.append(_state_row(edge_t + 0.75 * period, 0.0, rst_n, 0.9, code))

    passed, detail = checker(rows)
    assert passed, detail
    assert "P_RESET_SEED mismatch_count=0" in detail


def test_v4_080_multitone_checker_uses_recorded_times_not_secret_sample_points() -> None:
    from checkers.v4.registry import load_checker

    checker = load_checker("v4_080_sine_periodic_voltage_source")
    assert checker is not None

    start_s = 10.0e-6
    rows = []
    for index in range(80):
        time_s = start_s + index * 6.25e-9
        out = (
            0.2 * math.sin(2 * math.pi * 1e6 * time_s)
            + 0.1 * math.sin(2 * math.pi * 2e6 * time_s)
            + 0.05 * math.sin(2 * math.pi * 3e6 * time_s)
        )
        rows.append({"time": time_s, "OUT": out})

    passed, detail = checker(rows)
    assert passed, detail
    assert "P_LINEAR_SUPERPOSITION mismatch_count=0" in detail
