from __future__ import annotations

from collections.abc import Callable
import math
from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from runners.checkers.v4.task_052 import check_v3_497_thermometer_bus_encoder
from runners.checkers.v4.task_072 import check_v4_aperture_delay_track_and_hold
from runners.checkers.v4.task_187 import check_v3_adc_sample_clock_sequencer
from runners.checkers.v4.task_202 import check_v3_adc_zoom_timing_sequencer
from runners.checkers.v4.task_217 import check_v3_single_shot_timer_pulse
from runners.checkers.v4.task_252 import check_v4_252_supply_qualified_window_flag
from runners.checkers.v4.task_285 import check_v4_285_configurable_startup_policy
from runners.checkers.v4.task_300 import check_v3_503_differential_vco_clip_idtmod


NS = 1e-9


def _times(
    stop_ns: float,
    *,
    step_ns: float,
    offset_ns: float,
    breakpoints_ns: tuple[float, ...],
) -> list[float]:
    grid = {
        offset_ns + index * step_ns
        for index in range(int((stop_ns - offset_ns) / step_ns) + 1)
    }
    grid.update((0.0, stop_ns, *breakpoints_ns))
    return sorted(time_ns for time_ns in grid if 0.0 <= time_ns <= stop_ns)


def _pwl_logic(time_ns: float, start_ns: float, stop_ns: float, edge_ns: float) -> float:
    if time_ns < start_ns or time_ns > stop_ns + edge_ns:
        return 0.0
    if time_ns < start_ns + edge_ns:
        return 0.9 * (time_ns - start_ns) / edge_ns
    if time_ns <= stop_ns:
        return 0.9
    return 0.9 * (stop_ns + edge_ns - time_ns) / edge_ns


def _window_value(
    time_ns: float,
    windows: tuple[tuple[float, float], ...],
    *,
    frame_ns: float,
    high: float,
    edge_ns: float,
    phase_shift_ns: float = 0.0,
) -> float:
    phase_ns = time_ns % frame_ns
    return max(
        (
            high
            / 0.9
            * _pwl_logic(
                phase_ns,
                start_ns + phase_shift_ns,
                stop_ns + phase_shift_ns,
                edge_ns,
            )
            for start_ns, stop_ns in windows
        ),
        default=0.0,
    )


def _thermometer_rows(*, step_ns: float, offset_ns: float, broken_prefix: bool = False) -> list[dict[str, float]]:
    plateaus = ((0.0, -0.1), (2.0, 0.22), (4.0, 0.51), (6.0, 0.88), (8.0, 1.05))
    rows: list[dict[str, float]] = []
    for time_ns in _times(
        9.5,
        step_ns=step_ns,
        offset_ns=offset_ns,
        breakpoints_ns=tuple(time_ns for time_ns, _ in plateaus),
    ):
        vin = plateaus[0][1]
        for start_ns, value in plateaus:
            if time_ns >= start_ns:
                vin = value
        code = max(0, min(16, int(16.0 * min(1.0, max(0.0, vin)))))
        row = {"time": time_ns * NS, "vin": vin}
        for bit in range(16):
            row[f"t{bit}"] = 0.9 if bit < code else 0.0
        if broken_prefix and code >= 8:
            row["t2"] = 0.0
            row["t10"] = 0.9
        rows.append(row)
    return rows


def test_thermometer_verdict_is_invariant_to_shifted_time_grid() -> None:
    for rows in (
        _thermometer_rows(step_ns=0.05, offset_ns=0.0),
        _thermometer_rows(step_ns=0.37, offset_ns=0.11),
    ):
        ok, note = check_v3_497_thermometer_bus_encoder(rows)
        assert ok, note


def test_thermometer_non_prefix_negative_remains_rejected() -> None:
    ok, note = check_v3_497_thermometer_bus_encoder(
        _thermometer_rows(step_ns=0.37, offset_ns=0.11, broken_prefix=True)
    )
    assert not ok, note


def _track_hold_rows(*, step_ns: float, offset_ns: float, wrong_capture: bool = False) -> list[dict[str, float]]:
    edges = (5.0, 25.0, 45.0, 65.0, 85.0)
    captured = (0.10, 0.35, 0.60, 0.25, 0.70)
    critical = tuple(
        point
        for edge_ns in edges
        for point in (edge_ns, edge_ns + 0.02, edge_ns + 0.20, edge_ns + 0.25, edge_ns + 1.0)
    )
    rows: list[dict[str, float]] = []
    for time_ns in _times(
        100.0,
        step_ns=step_ns,
        offset_ns=offset_ns,
        breakpoints_ns=critical,
    ):
        clk = max(_pwl_logic(time_ns, edge_ns, edge_ns + 10.0, 0.02) for edge_ns in edges)
        vin = 0.05
        vout = 0.05
        for edge_ns, value in zip(edges, captured):
            if time_ns >= edge_ns + 0.12:
                vin = value
            if time_ns >= edge_ns + 0.25:
                vout = value
        if wrong_capture and time_ns >= edges[2] + 0.25:
            vout = 0.10
        rows.append(
            {
                "time": time_ns * NS,
                "VDD": 0.9,
                "VSS": 0.0,
                "clk": clk,
                "vin": vin,
                "vout": vout,
            }
        )
    return rows


def test_aperture_capture_is_invariant_to_shifted_time_grid() -> None:
    for rows in (
        _track_hold_rows(step_ns=0.02, offset_ns=0.0),
        _track_hold_rows(step_ns=0.31, offset_ns=0.13),
    ):
        ok, note = check_v4_aperture_delay_track_and_hold(rows)
        assert ok, note


def test_aperture_wrong_capture_negative_remains_rejected() -> None:
    ok, note = check_v4_aperture_delay_track_and_hold(
        _track_hold_rows(step_ns=0.31, offset_ns=0.13, wrong_capture=True)
    )
    assert not ok, note


SEQUENCER_187_WINDOWS = {
    "rst": ((0.0, 0.25),),
    "s": ((0.6, 1.0), (6.6, 7.0), (12.6, 13.0)),
    "ss": ((0.6, 1.2), (6.6, 7.2), (12.6, 13.2)),
    "nc_az": ((1.35, 1.55), (7.35, 7.55), (13.35, 13.55)),
    "nc": ((1.7, 2.05), (7.7, 8.05), (13.7, 14.05)),
    "conv": ((2.4, 5.4), (8.4, 11.4), (14.4, 17.4)),
}


SEQUENCER_202_WINDOWS = {
    "rst": ((0.5, 0.8),),
    "s": ((1.5, 2.5),),
    "sar": ((3.0, 5.4),),
    "clk_sar": ((3.0, 3.25), (3.6, 3.85), (4.2, 4.45)),
    "res": ((6.0, 6.6),),
    "intg": ((8.0, 8.7),),
    "zoom": ((9.2, 10.8),),
    "clk_zoom": ((9.2, 9.45), (9.8, 10.05)),
    "rst_zoom": ((11.0, 11.5),),
}


def _sequencer_rows(
    windows_by_signal: dict[str, tuple[tuple[float, float], ...]],
    *,
    frame_ns: float,
    stop_ns: float,
    high: float,
    step_ns: float,
    offset_ns: float,
    phase_shift_ns: float = 0.0,
) -> list[dict[str, float]]:
    critical = tuple(
        frame + edge + delta + phase_shift_ns
        for frame in (0.0, frame_ns)
        for windows in windows_by_signal.values()
        for window in windows
        for edge in window
        for delta in (0.0, 0.02)
        if 0.0 <= frame + edge + delta + phase_shift_ns <= stop_ns
    )
    return [
        {
            "time": time_ns * NS,
            **{
                signal: _window_value(
                    time_ns,
                    windows,
                    frame_ns=frame_ns,
                    high=high,
                    edge_ns=0.02,
                    phase_shift_ns=phase_shift_ns,
                )
                for signal, windows in windows_by_signal.items()
            },
        }
        for time_ns in _times(
            stop_ns,
            step_ns=step_ns,
            offset_ns=offset_ns,
            breakpoints_ns=critical,
        )
    ]


@pytest.mark.parametrize(
    "checker,windows,frame_ns,stop_ns,high",
    [
        (check_v3_adc_sample_clock_sequencer, SEQUENCER_187_WINDOWS, 18.0, 22.0, 0.9),
        (check_v3_adc_zoom_timing_sequencer, SEQUENCER_202_WINDOWS, 32.0, 45.0, 1.1),
    ],
)
def test_fixed_window_sequencers_are_invariant_to_shifted_time_grid(
    checker: Callable[[list[dict[str, float]]], tuple[bool, str]],
    windows: dict[str, tuple[tuple[float, float], ...]],
    frame_ns: float,
    stop_ns: float,
    high: float,
) -> None:
    for rows in (
        _sequencer_rows(
            windows,
            frame_ns=frame_ns,
            stop_ns=stop_ns,
            high=high,
            step_ns=0.01,
            offset_ns=0.0,
        ),
        _sequencer_rows(
            windows,
            frame_ns=frame_ns,
            stop_ns=stop_ns,
            high=high,
            step_ns=0.37,
            offset_ns=0.13,
        ),
    ):
        ok, note = checker(rows)
        assert ok, note


@pytest.mark.parametrize(
    "checker,windows,frame_ns,stop_ns,high",
    [
        (check_v3_adc_sample_clock_sequencer, SEQUENCER_187_WINDOWS, 18.0, 22.0, 0.9),
        (check_v3_adc_zoom_timing_sequencer, SEQUENCER_202_WINDOWS, 32.0, 45.0, 1.1),
    ],
)
def test_fixed_window_phase_shift_negative_remains_rejected(
    checker: Callable[[list[dict[str, float]]], tuple[bool, str]],
    windows: dict[str, tuple[tuple[float, float], ...]],
    frame_ns: float,
    stop_ns: float,
    high: float,
) -> None:
    ok, note = checker(
        _sequencer_rows(
            windows,
            frame_ns=frame_ns,
            stop_ns=stop_ns,
            high=high,
            step_ns=0.37,
            offset_ns=0.13,
            phase_shift_ns=0.15,
        )
    )
    assert not ok, note


def _single_shot_rows(*, step_ns: float, offset_ns: float, missing_last_fall: bool = False) -> list[dict[str, float]]:
    triggers = (0.61, 3.61)
    output_windows = ((0.71, 2.72), (3.71, 5.72))
    critical = tuple(
        point
        for trigger_ns, (rise_ns, fall_ns) in zip(triggers, output_windows)
        for point in (
            trigger_ns,
            trigger_ns + 0.02,
            rise_ns,
            rise_ns + 0.01,
            fall_ns,
            fall_ns + 0.01,
        )
    )
    rows: list[dict[str, float]] = []
    for time_ns in _times(
        5.8,
        step_ns=step_ns,
        offset_ns=offset_ns,
        breakpoints_ns=critical,
    ):
        vin = max(_pwl_logic(time_ns, trigger_ns, trigger_ns + 0.58, 0.02) for trigger_ns in triggers)
        vout = 0.0
        for index, (rise_ns, fall_ns) in enumerate(output_windows):
            if missing_last_fall and index == 1:
                fall_ns = 6.5
            vout = max(vout, _pwl_logic(time_ns, rise_ns, fall_ns, 0.01))
        rows.append({"time": time_ns * NS, "vin": vin, "vout": vout})
    return rows


def test_single_shot_complete_pulses_are_invariant_to_shifted_time_grid() -> None:
    for rows in (
        _single_shot_rows(step_ns=0.005, offset_ns=0.0),
        _single_shot_rows(step_ns=0.071, offset_ns=0.019),
    ):
        ok, note = check_v3_single_shot_timer_pulse(rows)
        assert ok, note


def test_single_shot_missing_final_fall_remains_rejected() -> None:
    ok, note = check_v3_single_shot_timer_pulse(
        _single_shot_rows(step_ns=0.071, offset_ns=0.019, missing_last_fall=True)
    )
    assert not ok, note
    assert "output_falls=1" in note


def _window_contract_row(time_us: float, *, wrong_out: bool = False) -> dict[str, float]:
    en = 0.0 if time_us < 0.8 else 0.9
    vdd = 0.9
    in0 = 0.1
    if 1.6 <= time_us < 2.8:
        in0 = 0.4
    elif 2.8 <= time_us < 4.0:
        in0 = 0.82
    elif 4.0 <= time_us < 5.4:
        vdd = min(1.0, max(0.0, (time_us - 4.0) / 1.4))
        in0 = 0.5
    elif 5.4 <= time_us < 6.8:
        vdd = 1.0 + 0.4 * (time_us - 5.4) / 1.4
        in0 = 0.5
    elif time_us >= 6.8:
        in0 = 0.2
    span = vdd
    valid = en > 0.45 and 0.62 <= span <= 1.28
    x0 = min(1.0, max(0.0, in0 / max(span, 0.05)))
    out = 0.9 * x0 if valid else 0.0
    flag = 0.9 if valid and 0.24 <= x0 <= 0.72 else 0.0
    metric = 0.9 * min(1.0, abs(x0 - 0.48) / 0.48) if valid else 0.0
    if wrong_out and 2.0 <= time_us <= 2.5:
        out = 0.0
    return {
        "time": time_us * 1e-6,
        "in0": in0,
        "in1": 0.2,
        "in2": 0.5,
        "in3": 0.8,
        "ctrl0": 0.9,
        "ctrl1": 0.0,
        "vdd": vdd,
        "vss": 0.0,
        "en": en,
        "out": out,
        "flag": flag,
        "metric": metric,
    }


def _window_rows(*, step_us: float, offset_us: float, wrong_out: bool = False) -> list[dict[str, float]]:
    times = {0.0, 8.0}
    times.update(offset_us + index * step_us for index in range(int(8.0 / step_us) + 1))
    return [
        _window_contract_row(time_us, wrong_out=wrong_out)
        for time_us in sorted(time_us for time_us in times if 0.0 <= time_us <= 8.0)
    ]


@pytest.mark.parametrize(
    "checker",
    [check_v4_252_supply_qualified_window_flag, check_v4_285_configurable_startup_policy],
)
def test_continuous_window_contract_is_invariant_across_validity_boundaries(
    checker: Callable[[list[dict[str, float]]], tuple[bool, str]],
) -> None:
    for rows in (
        _window_rows(step_us=0.01, offset_us=0.0),
        _window_rows(step_us=0.137, offset_us=0.043),
    ):
        ok, note = checker(rows)
        assert ok, note


@pytest.mark.parametrize(
    "checker",
    [check_v4_252_supply_qualified_window_flag, check_v4_285_configurable_startup_policy],
)
def test_continuous_window_wrong_settled_output_remains_rejected(
    checker: Callable[[list[dict[str, float]]], tuple[bool, str]],
) -> None:
    ok, note = checker(_window_rows(step_us=0.137, offset_us=0.043, wrong_out=True))
    assert not ok, note


def _adaptive_vco_rows(*, wrong_metric: bool = False) -> list[dict[str, float]]:
    diffs = (-0.30, -0.30, 0.30, 0.30, 0.50, 0.50, -0.30, -0.30, 0.15, 0.15, 0.50, 0.50) * 4
    increments_ns = (7.0, 83.0, 13.0, 97.0, 29.0, 71.0)
    rows: list[dict[str, float]] = []
    time_s = 0.0
    phase = 0.0
    for index, diff in enumerate(diffs):
        if index:
            previous_diff = diffs[index - 1]
            frequency = min(80e6, max(5e6, 20e6 + 160e6 * previous_diff))
            dt = increments_ns[(index - 1) % len(increments_ns)] * NS
            time_s += dt
            phase = (phase + frequency * dt) % 1.0
        sine = 0.4 * math.sin(2.0 * math.pi * phase)
        metric = 0.9 * phase
        if wrong_metric and index >= len(diffs) // 2:
            metric = 0.0
        rows.append(
            {
                "time": time_s,
                "vinp": 0.45 + 0.5 * diff,
                "vinm": 0.45 - 0.5 * diff,
                "outp": 0.45 + sine,
                "outm": 0.45 - sine,
                "metric": metric,
            }
        )
    return rows


def test_vco_outputs_use_the_phase_observed_at_each_physical_sample() -> None:
    ok, note = check_v3_503_differential_vco_clip_idtmod(_adaptive_vco_rows())
    assert ok, note


def test_vco_wrong_phase_metric_remains_rejected() -> None:
    ok, note = check_v3_503_differential_vco_clip_idtmod(
        _adaptive_vco_rows(wrong_metric=True)
    )
    assert not ok, note
