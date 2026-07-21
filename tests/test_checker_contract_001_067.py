from __future__ import annotations

import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

from checkers.v4.registry import load_checker


def _set_bits(row: dict[str, float], prefix: str, width: int, value: int) -> None:
    for bit in range(width):
        row[f"{prefix}{bit}"] = 0.9 if value & (1 << bit) else 0.0


def _tdc_trace(*, code_error: int) -> list[dict[str, float]]:
    pairs = ((2, 5), (10, 15), (20, 27))
    code = 0
    rows: list[dict[str, float]] = []
    for time_ns in range(35):
        start = 0.9 if any(time_ns == begin for begin, _ in pairs) else 0.0
        stop = 0.9 if any(time_ns == end for _, end in pairs) else 0.0
        for begin, end in pairs:
            if time_ns == end:
                code = end - begin + code_error
        row = {
            "time": time_ns * 1e-9,
            "start": start,
            "stop": stop,
            "valid": 0.9 if code else 0.0,
        }
        _set_bits(row, "code", 8, code)
        rows.append(row)
    return rows


def _duty_trace(*, code_error: int) -> list[dict[str, float]]:
    rises = (1, 11, 21, 31)
    falls = (4, 16, 28)
    expected = {11: 77, 21: 127, 31: 179}
    code = 0
    rows: list[dict[str, float]] = []
    for time_ns in range(40):
        clk = 0.9 if any(
            rise <= time_ns < fall
            for rise, fall in zip(rises, (*falls, 40))
        ) else 0.0
        if time_ns in expected:
            code = expected[time_ns] + code_error
        row = {
            "time": time_ns * 1e-9,
            "clk_in": clk,
            "valid": 0.9 if code else 0.0,
        }
        _set_bits(row, "duty", 8, code)
        rows.append(row)
    return rows


def _gated_clock_trace(*, high_level: float) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for step in range(301):
        time_ns = step / 10.0
        clk = 0.9 if int(time_ns // 2) % 2 else 0.0
        enable = 0.9 if time_ns < 20 else 0.0
        pulse = high_level if clk > 0.45 and enable > 0.45 else 0.0
        rows.append({"time": time_ns * 1e-9, "clk": clk, "en": enable, "pulse": pulse})
    return rows


def _edge_detector_trace(*, high_level: float) -> list[dict[str, float]]:
    selected_edges = (5, 15, 25, 35)
    rows: list[dict[str, float]] = []
    for step in range(401):
        time_ns = step / 10.0
        signal = 0.9 if (
            5 <= time_ns < 10
            or 15 <= time_ns < 20
            or 25 <= time_ns < 30
            or time_ns >= 35
        ) else 0.0
        pulse = high_level if any(edge <= time_ns < edge + 2 for edge in selected_edges) else 0.0
        rows.append(
            {"time": time_ns * 1e-9, "sig": signal, "rise_en": 0.9, "pulse": pulse}
        )
    return rows


def _mixer_trace(*, reset_out: float, reset_metric: float) -> list[dict[str, float]]:
    states = (
        {"rst": 0.9, "clk": 0.0, "vin": 0.45, "out": reset_out, "metric": reset_metric},
        {"rst": 0.0, "clk": 0.9, "vin": 0.70, "out": 0.72, "metric": 0.9},
        {"rst": 0.0, "clk": 0.0, "vin": 0.70, "out": 0.22, "metric": 0.9},
        {"rst": 0.0, "clk": 0.9, "vin": 0.20, "out": 0.22, "metric": 0.9},
        {"rst": 0.0, "clk": 0.0, "vin": 0.20, "out": 0.68, "metric": 0.9},
    )
    rows: list[dict[str, float]] = []
    time_s = 0.0
    for state in states:
        for _ in range(10):
            rows.append({"time": time_s, **state})
            time_s += 1e-9
    return rows


def _comparator_trace(*, delayed_crossing: bool) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for time_ns in range(601):
        phase = (time_ns // 100) % 2
        vinp, vinn = ((0.7, 0.2) if phase == 0 else (0.2, 0.7))
        output = 0.9 if vinp > vinn else 0.0
        if delayed_crossing and time_ns < 3:
            output = 0.0
        if delayed_crossing and 300 <= time_ns < 304:
            output = 0.9
        rows.append({"time": time_ns * 1e-9, "vinp": vinp, "vinn": vinn, "out_p": output})
    return rows


def _step_value(
    time_s: float,
    initial: float,
    transitions: tuple[tuple[float, float], ...],
) -> float:
    value = initial
    for edge_s, next_value in transitions:
        if time_s >= edge_s:
            value = next_value
    return value


def _deglitch_trace(*, omit_late_outputs: bool) -> list[dict[str, float]]:
    vin_edges = (
        (5.0e-9, 0.9),
        (15.0e-9, 0.0),
        (25.0e-9, 0.9),
        (25.4e-9, 0.0),
        (35.0e-9, 0.9),
        (45.0e-9, 0.0),
    )
    all_vout_edges = (
        (7.2e-9, 0.9),
        (17.2e-9, 0.0),
        (37.2e-9, 0.9),
        (47.2e-9, 0.0),
    )
    vout_edges = all_vout_edges[:2] if omit_late_outputs else all_vout_edges
    valid_edges = tuple((edge, 0.9) for edge, _ in vout_edges) + tuple(
        (edge + 0.5e-9, 0.0) for edge, _ in vout_edges
    )
    rejected_edges = ((25.45e-9, 0.9), (26.0e-9, 0.0))
    rows: list[dict[str, float]] = []
    for step in range(0, 561):
        time_s = step * 0.1e-9
        rows.append(
            {
                "time": time_s,
                "vin": _step_value(time_s, 0.0, vin_edges),
                "rst": 0.9 if time_s < 1e-9 else 0.0,
                "enable": 0.9 if 2e-9 <= time_s < 50e-9 else 0.0,
                "vout": _step_value(time_s, 0.0, vout_edges),
                "edge_valid": _step_value(time_s, 0.0, tuple(sorted(valid_edges))),
                "rejected": _step_value(time_s, 0.0, rejected_edges),
            }
        )
    return rows


def _phase_accumulator_trace(*, period_ns: float, phase_step: float) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for sample_index in range(501):
        time_ns = sample_index / 10.0
        updates = int(time_ns // period_ns)
        phase = (phase_step * updates) % 1.0
        rows.append(
            {
                "time": time_ns * 1e-9,
                "VDD": 0.9,
                "VSS": 0.0,
                "phase_out": 0.9 * phase,
                "clk_out": 0.9 if phase < 0.5 else 0.0,
            }
        )
    return rows


def _latency_counter_trace(*, include_zero_latency: bool) -> list[dict[str, float]]:
    # Transactions complete with latencies 2 and 1; the legal trace adds a
    # simultaneous valid+ready request to exercise the public zero-latency case.
    inputs = (
        (True, False),
        (False, False),
        (False, False),
        (False, True),
        (True, False),
        (False, False),
        (False, True),
        (include_zero_latency, include_zero_latency),
        (False, False),
    )
    latched = 0
    active = False
    count = 0
    rows: list[dict[str, float]] = []
    for cycle, (valid, ready) in enumerate(inputs):
        edge_s = (1.0 + 10.0 * cycle) * 1e-9
        done = False
        if valid and not active:
            active = True
            count = 0
        elif active and not ready:
            count += 1
        if active and ready:
            latched = count
            done = True
            active = False
        base = {
            "valid_i": 0.9 if valid else 0.0,
            "ready_i": 0.9 if ready else 0.0,
            "done": 0.9 if done else 0.0,
        }
        _set_bits(base, "lat", 12, latched)
        rows.append({"time": edge_s - 0.1e-9, "clk": 0.0, **base})
        rows.append({"time": edge_s, "clk": 0.9, **base})
        rows.append({"time": edge_s + 2.0e-9, "clk": 0.9, **base})
        rows.append({"time": edge_s + 5.0e-9, "clk": 0.0, **base})
    return rows


def _integrator_trace(*, continuous: bool) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    state = 0.0
    for step in range(401):
        time_ns = step / 10.0
        reset = time_ns < 5 or 20 <= time_ns < 25
        if reset:
            state = 0.0
        elif continuous:
            state = min(0.85, state + 0.006)
        elif abs(time_ns - round(time_ns)) < 1e-9:
            state = min(0.85, state + 0.06)
        rows.append(
            {"time": time_ns * 1e-9, "vin": 0.06, "rst": 0.9 if reset else 0.0, "vout": state}
        )
    return rows


def _slew_trace(*, continuous: bool) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    state = 0.0
    for step in range(1501):
        time_ns = step / 10.0
        target = 0.0 if time_ns < 5 or time_ns >= 75 else 0.9
        if continuous:
            delta = max(-0.0015, min(0.0015, target - state))
            state += delta
        elif abs(time_ns - round(time_ns)) < 1e-9:
            delta = max(-0.015, min(0.015, target - state))
            state += delta
        rows.append({"time": time_ns * 1e-9, "vin": target, "vout": state})
    return rows


def _droop_trace(*, periodic: bool) -> list[dict[str, float]]:
    captures = {5.0: 0.20, 15.0: 0.60, 65.0: 0.80}
    held = 0.0
    rows: list[dict[str, float]] = []
    for step in range(651):
        time_ns = step / 5.0
        reset = time_ns >= 110.0
        sample_active = any(edge <= time_ns < edge + 0.4 for edge in captures)
        capture = next((value for edge, value in captures.items() if abs(time_ns - edge) < 1e-9), None)
        if reset:
            held = 0.0
        elif capture is not None:
            held = capture
        elif periodic and abs(time_ns - round(time_ns)) < 1e-9:
            held *= 0.985
        elif not periodic and held > 0.0:
            held -= 0.0012 / 5.0
        vin = 0.20 if time_ns < 14.0 else 0.60 if time_ns < 64.0 else 0.80
        rows.append(
            {
                "time": time_ns * 1e-9,
                "sample": 0.9 if sample_active else 0.0,
                "rst": 0.9 if reset else 0.0,
                "vin": vin,
                "vout": max(0.0, held),
            }
        )
    return rows


@pytest.mark.parametrize(
    ("checker_id", "legal", "adversarial"),
    [
        (
            "v4_059_edge_interval_tdc_8b",
            _tdc_trace(code_error=0),
            _tdc_trace(code_error=1),
        ),
        (
            "v4_060_duty_cycle_meter_8b",
            _duty_trace(code_error=0),
            _duty_trace(code_error=1),
        ),
        (
            "v4_065_enable_gated_clock_pulse",
            _gated_clock_trace(high_level=0.9),
            _gated_clock_trace(high_level=1.5),
        ),
        (
            "v4_066_configurable_polarity_edge_detector",
            _edge_detector_trace(high_level=0.9),
            _edge_detector_trace(high_level=0.46),
        ),
    ],
)
def test_exact_codes_and_public_output_rails(
    checker_id: str,
    legal: list[dict[str, float]],
    adversarial: list[dict[str, float]],
) -> None:
    checker = load_checker(checker_id)
    assert checker is not None

    legal_passed, legal_detail = checker(legal)
    assert legal_passed, legal_detail

    adversarial_passed, adversarial_detail = checker(adversarial)
    assert not adversarial_passed, adversarial_detail


@pytest.mark.parametrize(
    ("checker_id", "legal", "adversarial"),
    [
        (
            "v4_041_rf_mixer_downconverter_macro",
            _mixer_trace(reset_out=0.45, reset_metric=0.0),
            _mixer_trace(reset_out=0.9, reset_metric=0.9),
        ),
        (
            "v4_045_threshold_comparator",
            _comparator_trace(delayed_crossing=False),
            _comparator_trace(delayed_crossing=True),
        ),
        (
            "v4_064_edge_delay_line_with_deglitch",
            _deglitch_trace(omit_late_outputs=False),
            _deglitch_trace(omit_late_outputs=True),
        ),
    ],
)
def test_reset_and_every_required_event_are_checked(
    checker_id: str,
    legal: list[dict[str, float]],
    adversarial: list[dict[str, float]],
) -> None:
    checker = load_checker(checker_id)
    assert checker is not None

    legal_passed, legal_detail = checker(legal)
    assert legal_passed, legal_detail

    adversarial_passed, adversarial_detail = checker(adversarial)
    assert not adversarial_passed, adversarial_detail


@pytest.mark.parametrize(
    ("checker_id", "legal", "adversarial"),
    [
        (
            "v4_026_digital_phase_accumulator_with_modulo_wrap",
            _phase_accumulator_trace(period_ns=4.0, phase_step=0.2),
            _phase_accumulator_trace(period_ns=3.0, phase_step=0.3),
        ),
        (
            "v4_062_latency_counter_ready_valid_12b",
            _latency_counter_trace(include_zero_latency=True),
            _latency_counter_trace(include_zero_latency=False),
        ),
    ],
)
def test_score_overrides_and_zero_latency_are_observed(
    checker_id: str,
    legal: list[dict[str, float]],
    adversarial: list[dict[str, float]],
) -> None:
    checker = load_checker(checker_id)
    assert checker is not None
    legal_passed, legal_detail = checker(legal)
    assert legal_passed, legal_detail
    adversarial_passed, adversarial_detail = checker(adversarial)
    assert not adversarial_passed, adversarial_detail


@pytest.mark.parametrize(
    ("checker_id", "legal", "adversarial"),
    [
        (
            "v4_013_resettable_integrator",
            _integrator_trace(continuous=False),
            _integrator_trace(continuous=True),
        ),
        (
            "v4_016_slew_rate_limiter",
            _slew_trace(continuous=False),
            _slew_trace(continuous=True),
        ),
        (
            "v4_042_sample_and_hold_with_droop_leakage",
            _droop_trace(periodic=True),
            _droop_trace(periodic=False),
        ),
    ],
)
def test_periodic_state_updates_include_observable_hold_intervals(
    checker_id: str,
    legal: list[dict[str, float]],
    adversarial: list[dict[str, float]],
) -> None:
    checker = load_checker(checker_id)
    assert checker is not None
    legal_passed, legal_detail = checker(legal)
    assert legal_passed, legal_detail
    adversarial_passed, adversarial_detail = checker(adversarial)
    assert not adversarial_passed, adversarial_detail
