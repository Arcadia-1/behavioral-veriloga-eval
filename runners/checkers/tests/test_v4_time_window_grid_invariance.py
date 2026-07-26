from __future__ import annotations

import math

import pytest

from runners.checkers.v4.task_226 import CHECKER as CHECK_LEVEL_SHIFT
from runners.checkers.v4.task_370 import CHECKER as CHECK_SETTLING
from runners.checkers.v4.task_389 import CHECKER as CHECK_HEADROOM


def _ns(value: float) -> float:
    return value * 1e-9


def _level_shift_row(time_ns: float, *, offset_error: float = 0.0) -> dict[str, float]:
    phase = (time_ns - 0.1) / 9.9
    sigin = 0.45 + 0.38 * math.sin(2.0 * math.pi * phase)
    return {"time": _ns(time_ns), "sigin": sigin, "sigout": sigin + 0.35 + offset_error}


def _level_shift_rows(kind: str, *, offset_error: float = 0.0) -> list[dict[str, float]]:
    if kind == "dense":
        times = [0.05 * index for index in range(221)]
    elif kind == "sparse":
        times = [0.0, 0.1, 0.35, 1.25, 2.75, 4.3, 5.8, 7.2, 8.9, 10.4, 11.0]
    else:
        times = [0.0, 0.07, 0.13, 0.41, 0.93, 1.77, 2.46, 3.81, 5.06, 6.52, 7.64, 9.38, 10.1, 11.0]
    return [_level_shift_row(time_ns, offset_error=offset_error) for time_ns in times]


@pytest.mark.parametrize("kind", ["dense", "sparse", "nonuniform"])
def test_task226_level_shift_verdict_is_grid_invariant(kind: str) -> None:
    passed, note = CHECK_LEVEL_SHIFT(_level_shift_rows(kind))
    assert passed, note


def test_task226_level_shift_still_rejects_wrong_offset() -> None:
    passed, note = CHECK_LEVEL_SHIFT(_level_shift_rows("nonuniform", offset_error=0.08))
    assert not passed, note
    assert "level_shift_error" in note


_SETTLING_EDGES_NS = [2.0, 3.0, 4.0, 5.0, 6.0, 9.4, 10.4, 11.4, 12.4, 13.4, 14.4]


def _logic_window(time_ns: float, starts: list[float], width_ns: float) -> float:
    return 0.9 if any(start <= time_ns < start + width_ns for start in starts) else 0.0


def _settling_state_at(time_ns: float) -> tuple[float, float, bool]:
    vout = 0.45
    settle_count = 0
    err = 0.0
    edges = [
        edge_ns
        for edge_ns in _SETTLING_EDGES_NS
        if not (time_ns >= 8.8 and edge_ns < 8.8)
    ]
    for edge_ns in edges:
        if time_ns < edge_ns + 0.7:
            break
        code = 3
        vin = 0.62 if edge_ns < 8.0 else 0.47
        target = max(0.0, min(0.9, 0.45 + (1.0 + 0.5 * code) * (vin - 0.45)))
        vout = max(0.0, min(0.9, vout + 0.3 * (target - vout)))
        err = target - vout
        settle_count = settle_count + 1 if abs(err) < 0.040 else 0
    return vout, err + 0.45, settle_count >= 3


def _settling_row(time_ns: float, *, vout_error_after_ns: float | None = None) -> dict[str, float]:
    rst = 0.9 if time_ns < 1.0 else 0.0
    enable = 0.0 if time_ns < 1.6 or 7.2 <= time_ns < 8.8 else 0.9
    vout, metric, settled = _settling_state_at(time_ns)
    if rst > 0.45 or enable <= 0.45:
        vout = metric = 0.45
        settled = False
    if vout_error_after_ns is not None and time_ns >= vout_error_after_ns:
        vout += 0.18
    return {
        "time": _ns(time_ns),
        "clk": _logic_window(time_ns, _SETTLING_EDGES_NS, 0.35),
        "rst": rst,
        "enable": enable,
        "vin": 0.62 if time_ns < 8.0 else 0.47,
        "gain_0": 0.9,
        "gain_1": 0.9,
        "gain_2": 0.0,
        "vout": vout,
        "error_metric": metric,
        "settled": 0.9 if settled else 0.0,
    }


def _settling_rows(kind: str, *, vout_error_after_ns: float | None = None) -> list[dict[str, float]]:
    if kind == "dense":
        times = [0.1 * index for index in range(161)]
    elif kind == "sparse":
        times = [0.0, 1.0, 1.7]
        for edge in _SETTLING_EDGES_NS:
            times.extend([edge - 0.05, edge + 0.05, edge + 0.72])
        times.extend([7.3, 8.1, 8.85, 16.0])
    else:
        times = [0.0, 0.37, 1.02, 1.71]
        for index, edge in enumerate(_SETTLING_EDGES_NS):
            times.extend([edge - 0.09, edge + 0.03, edge + 0.71 + 0.02 * (index % 2)])
        times.extend([7.31, 8.09, 8.87, 15.8])
    times.append(0.8)
    unique = sorted(set(round(time, 6) for time in times if 0.0 <= time <= 16.0))
    return [_settling_row(time_ns, vout_error_after_ns=vout_error_after_ns) for time_ns in unique]


@pytest.mark.parametrize("kind", ["dense", "sparse", "nonuniform"])
def test_task370_settling_verdict_is_grid_invariant(kind: str) -> None:
    passed, note = CHECK_SETTLING(_settling_rows(kind))
    assert passed, note


def test_task370_settling_still_rejects_wrong_update_value() -> None:
    passed, note = CHECK_SETTLING(_settling_rows("nonuniform", vout_error_after_ns=10.0))
    assert not passed, note
    assert "vout_errors=" in note


def _headroom_values(time_ns: float) -> tuple[float, float, float, float, float, float, float, float]:
    rst = 0.9 if time_ns < 1.0 else 0.0
    enable = 0.0 if time_ns < 1.5 or 8.0 <= time_ns < 9.0 else 0.9
    segment = int(max(0.0, time_ns - 1.5) // 0.8)
    vin = [0.25, 0.36, 0.45, 0.54, 0.66][segment % 5]
    vbias = 0.78 if segment % 3 else 0.58
    vdd_sense = 0.86 if segment % 4 else 0.61
    rail_limit = min(vdd_sense, vbias) - 0.16
    if rst > 0.45 or enable <= 0.45:
        return vin, vbias, vdd_sense, enable, rst, 0.45, 0.0, 0.0
    raw = 0.45 - 1.8 * (vin - 0.45)
    vout = max(0.0, min(rail_limit, raw))
    return vin, vbias, vdd_sense, enable, rst, vout, abs(vout - 0.45), 0.9 if rail_limit > 0.50 else 0.0


def _headroom_row(time_ns: float, *, metric_error_after_ns: float | None = None) -> dict[str, float]:
    vin, vbias, vdd_sense, enable, rst, vout, metric, ok = _headroom_values(time_ns)
    if metric_error_after_ns is not None and time_ns >= metric_error_after_ns and enable > 0.45 and rst <= 0.45:
        metric += 0.18
    return {
        "time": _ns(time_ns),
        "vin": vin,
        "vbias": vbias,
        "vdd_sense": vdd_sense,
        "enable": enable,
        "rst": rst,
        "vout": vout,
        "gain_metric": metric,
        "headroom_ok": ok,
    }


def _headroom_rows(kind: str, *, metric_error_after_ns: float | None = None) -> list[dict[str, float]]:
    if kind == "dense":
        times = [0.1 * index for index in range(141)]
    elif kind == "sparse":
        times = [0.0, 1.0, 1.5, 2.05, 2.85, 3.65, 4.45, 5.25, 6.05, 6.85, 7.65, 8.2, 9.1, 9.8, 10.6, 11.4, 12.2, 13.0, 13.8, 14.0]
    else:
        times = [0.0, 0.93, 1.47, 2.04, 2.89, 3.61, 4.51, 5.18, 6.09, 6.82, 7.7, 8.26, 9.13, 9.86, 10.67, 11.36, 12.28, 13.07, 13.79, 14.0]
    # Include two samples inside every physical regime.  A settling checker
    # cannot infer a stable window from a single isolated value at a change.
    stable_times = [0.2, 0.8, 1.1]
    for start in [1.5 + 0.8 * index for index in range(16)]:
        stable_times.extend([start + 0.05, start + 0.65])
    stable_times.extend([8.1, 8.7, 9.1, 9.7, 13.9])
    return [
        _headroom_row(time_ns, metric_error_after_ns=metric_error_after_ns)
        for time_ns in sorted(set(times + stable_times))
    ]


@pytest.mark.parametrize("kind", ["dense", "sparse", "nonuniform"])
def test_task389_headroom_verdict_is_grid_invariant(kind: str) -> None:
    passed, note = CHECK_HEADROOM(_headroom_rows(kind))
    assert passed, note


def test_task389_headroom_still_rejects_wrong_metric() -> None:
    passed, note = CHECK_HEADROOM(_headroom_rows("nonuniform", metric_error_after_ns=10.0))
    assert not passed, note
    assert "P_GAIN_METRIC" in note
