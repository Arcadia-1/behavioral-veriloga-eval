from __future__ import annotations

from runners.checkers.v4.task_199 import CHECKER as CHECK_199
from runners.checkers.v4.task_302 import CHECKER as CHECK_302
from runners.checkers.v4.task_322 import CHECKER as CHECK_322
from runners.checkers.v4.task_375 import CHECKER as CHECK_375
from runners.checkers.v4.task_387 import CHECKER as CHECK_387


def _logic(time_ns: float, windows: list[tuple[float, float]], *, midpoint_edges: bool = True) -> float:
    if any(start < time_ns < stop for start, stop in windows):
        return 0.9
    if midpoint_edges and any(time_ns == start or time_ns == stop for start, stop in windows):
        return 0.45
    return 0.0


def _times(stop_ns: float, step_ns: float, *, include_midpoints: bool) -> list[float]:
    count = int(round(stop_ns / step_ns))
    values = {round(index * step_ns, 12) for index in range(count + 1)}
    if include_midpoints:
        values.update(round(index + 0.5, 12) for index in range(int(stop_ns)))
    return sorted(values)


def _assert_same_pass(checker, base: list[dict[str, float]], variant: list[dict[str, float]]) -> None:
    base_ok, base_note = checker(base)
    variant_ok, variant_note = checker(variant)
    assert base_ok, base_note
    assert variant_ok == base_ok, variant_note


def _task199_rows(*, include_midpoints: bool, bad_output: bool = False) -> list[dict[str, float]]:
    rdy_windows = [(1.1, 1.7), (3.1, 3.7), (5.1, 5.7), (7.1, 7.7)]
    edges = [1.1, 3.1, 5.1, 7.1]
    codes = [
        (0, 0, 0, 0, 0, 0, 0),
        (1, 0, 0, 0, 0, 0, 0),
        (0, 1, 0, 0, 0, 0, 0),
        (1, 1, 0, 0, 0, 0, 0),
    ]
    weights = [0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0]
    total_weight = sum(weights) + 1.0
    expected = 0.0
    prev_rdy = 0.0
    rows: list[dict[str, float]] = []
    for time_ns in _times(10.0, 0.1 if include_midpoints else 0.2, include_midpoints=include_midpoints):
        rdy = _logic(time_ns, rdy_windows, midpoint_edges=include_midpoints)
        if prev_rdy < 0.45 <= rdy:
            edge_index = max(i for i, edge in enumerate(edges) if edge <= time_ns)
            if edge_index > 0:
                expected = (sum(bit * weight for bit, weight in zip(codes[edge_index], weights)) / total_weight) * 1.8 - 0.9
        prev_rdy = rdy
        row = {
            "time": time_ns * 1e-9,
            "rdy": rdy,
            "aout": expected + (0.09 if bad_output and time_ns > 8.0 else 0.0),
        }
        for bit_index, bit in enumerate(codes[max(i for i, edge in enumerate(edges) if edge <= time_ns)] if time_ns >= edges[0] else codes[0], start=1):
            row[f"din{bit_index}"] = 0.9 if bit else 0.0
        rows.append(row)
    return rows


def test_task199_ready_dac_midpoint_and_density_invariant() -> None:
    _assert_same_pass(
        CHECK_199,
        _task199_rows(include_midpoints=False),
        _task199_rows(include_midpoints=True),
    )
    passed, note = CHECK_199(_task199_rows(include_midpoints=True, bad_output=True))
    assert not passed, note


def _period_windows(start_ns: float, period_ns: float, count: int, width_ns: float) -> list[tuple[float, float]]:
    return [(start_ns + period_ns * index, start_ns + period_ns * index + width_ns) for index in range(count)]


def _task302_rows(*, include_midpoints: bool, bad_lock: bool = False) -> list[dict[str, float]]:
    ref_windows = _period_windows(1.1, 10.0, 4, 1.0) + _period_windows(45.1, 8.0, 7, 0.8)
    fb_windows = _period_windows(1.3, 10.0, 4, 1.0) + _period_windows(45.3, 8.0, 7, 0.8)
    dco_edges: list[float] = []
    for index, (start, _) in enumerate(fb_windows):
        dco_edges.extend(start + 0.48 * count for count in range(1, 16))
        if index % 2 == 1:
            dco_edges.append(start + 7.68)
    dco_windows = [(edge, edge + 0.2) for edge in dco_edges]
    rows: list[dict[str, float]] = []
    for time_ns in _times(100.0, 0.1 if include_midpoints else 0.2, include_midpoints=include_midpoints):
        lock = 0.0 if bad_lock or 45.0 <= time_ns < 69.0 else 0.9
        rows.append(
            {
                "time": time_ns * 1e-9,
                "ref_clk": _logic(time_ns, ref_windows, midpoint_edges=include_midpoints),
                "fb_clk": _logic(time_ns, fb_windows, midpoint_edges=include_midpoints),
                "dco_clk": _logic(time_ns, dco_windows, midpoint_edges=include_midpoints),
                "lock": lock,
                "vctrl_mon": 0.42 + 0.04 * min(1.0, time_ns / 100.0),
            }
        )
    return rows


def test_task302_fractional_divider_midpoint_and_density_invariant() -> None:
    _assert_same_pass(
        CHECK_302,
        _task302_rows(include_midpoints=False),
        _task302_rows(include_midpoints=True),
    )
    passed, note = CHECK_302(_task302_rows(include_midpoints=True, bad_lock=True))
    assert not passed, note


def _task322_rows(*, include_midpoints: bool, stuck_metric: bool = False) -> list[dict[str, float]]:
    clk_a_windows = _period_windows(2.1, 4.0, 9, 1.0)
    clk_b_windows = _period_windows(4.1, 4.0, 8, 1.0)
    rows: list[dict[str, float]] = []
    active = "clk_a"
    for time_ns in _times(38.0, 0.2 if include_midpoints else 0.4, include_midpoints=include_midpoints):
        rst = 0.9 if time_ns < 2.0 else 0.0
        enable = 0.9 if 2.5 < time_ns < 34.0 else 0.0
        sel = 0.9 if 14.0 < time_ns < 30.0 else 0.0
        clk_a = _logic(time_ns, clk_a_windows, midpoint_edges=include_midpoints)
        clk_b = _logic(time_ns, clk_b_windows, midpoint_edges=include_midpoints)
        if enable > 0.45 and rst <= 0.45 and clk_a <= 0.45 and clk_b <= 0.45:
            active = "clk_b" if sel > 0.45 else "clk_a"
        switching = 15.4 <= time_ns <= 18.0 or 31.8 <= time_ns <= 34.0
        valid = enable > 0.45 and rst <= 0.45 and time_ns > 5.0 and not (
            14.0 <= time_ns < 16.2 or 30.0 <= time_ns < 32.4
        )
        rows.append(
            {
                "time": time_ns * 1e-9,
                "clk_a": clk_a,
                "clk_b": clk_b,
                "sel": sel,
                "rst": rst,
                "enable": enable,
                "clk_out": (clk_b if active == "clk_b" else clk_a) if enable > 0.45 and rst <= 0.45 else 0.0,
                "switch_metric": 0.9 if (stuck_metric or switching) and enable > 0.45 else 0.0,
                "valid": 0.9 if valid else 0.0,
            }
        )
    return rows


def test_task322_mux_midpoint_and_density_invariant() -> None:
    _assert_same_pass(
        CHECK_322,
        _task322_rows(include_midpoints=False),
        _task322_rows(include_midpoints=True),
    )
    passed, note = CHECK_322(_task322_rows(include_midpoints=True, stuck_metric=True))
    assert not passed, note


def _task375_rows(*, include_midpoints: bool, overlap: bool = False) -> list[dict[str, float]]:
    clk_windows = _period_windows(2.1, 4.0, 10, 2.0)
    rows: list[dict[str, float]] = []
    for time_ns in _times(44.0, 0.2 if include_midpoints else 0.4, include_midpoints=include_midpoints):
        rst = 0.9 if time_ns < 1.0 else 0.0
        enable = 0.9 if 1.4 < time_ns < 39.0 else 0.0
        clk = _logic(time_ns, clk_windows, midpoint_edges=include_midpoints)
        if rst > 0.45 or enable <= 0.45:
            phi1 = phi2 = dead = valid = 0.0
        else:
            phase_high = any(start + 0.6 <= time_ns < stop for start, stop in clk_windows)
            phase_low = any(stop + 0.6 <= time_ns < stop + 2.0 for _, stop in clk_windows)
            phi1 = 0.9 if phase_high else 0.0
            phi2 = 0.9 if phase_low or overlap and 15.0 < time_ns < 15.4 else 0.0
            dead = 0.9 if clk <= 0.45 and phi1 <= 0.45 and phi2 <= 0.45 else 0.0
            valid = 0.9 if time_ns > 5.0 else 0.0
        rows.append(
            {
                "time": time_ns * 1e-9,
                "clk_in": clk,
                "rst": rst,
                "enable": enable,
                "phi1": phi1,
                "phi2": phi2,
                "deadtime_metric": dead,
                "valid": valid,
            }
        )
    return rows


def test_task375_nonoverlap_midpoint_and_density_invariant() -> None:
    _assert_same_pass(
        CHECK_375,
        _task375_rows(include_midpoints=False),
        _task375_rows(include_midpoints=True),
    )
    passed, note = CHECK_375(_task375_rows(include_midpoints=True, overlap=True))
    assert not passed, note


def _task387_rows(
    *,
    include_midpoints: bool,
    bad_flag: bool = False,
    include_transition_lag: bool = False,
) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    step_ns = 0.1 if include_midpoints else 0.15
    for time_ns in _times(40.0, step_ns, include_midpoints=include_midpoints):
        rst = 0.9 if time_ns < 1.0 else 0.0
        enable = 0.9 if 2.0 < time_ns < 38.0 else 0.0
        phase = time_ns % 0.6
        vin = 0.72 if 0.25 <= phase <= 0.35 else 0.50
        if rst > 0.45 or enable <= 0.45:
            vout = 0.45
            gain_metric = 0.0
            flag = 0.0
        else:
            excess = max(0.0, abs(vin - 0.45) - 0.18)
            gain = 4.0 / (1.0 + excess / 0.20)
            vout = max(0.0, min(0.9, 0.45 + gain * (vin - 0.45)))
            gain_metric = max(0.0, min(0.9, 0.9 * gain / 4.0))
            flag = 0.9 if gain < 3.4 else 0.0
            if bad_flag:
                flag = 0.0
            if include_transition_lag and any(
                abs(time_ns - edge) < 0.2
                for edge in (18.0, 42.0, 64.0)
            ):
                vout = 0.5 * (vout + 0.45)
                gain_metric *= 0.5
                flag *= 0.5
        rows.append(
            {
                "time": time_ns * 1e-9,
                "rst": rst,
                "enable": enable,
                "vin": vin,
                "vout": vout,
                "gain_metric": gain_metric,
                "compression_flag": flag,
            }
        )
    return rows


def test_task387_lna_midpoint_and_density_invariant() -> None:
    _assert_same_pass(
        CHECK_387,
        _task387_rows(include_midpoints=False),
        _task387_rows(include_midpoints=True),
    )
    passed, note = CHECK_387(_task387_rows(include_midpoints=True, bad_flag=True))
    assert not passed, note


def test_task387_ignores_short_analog_transition_lag() -> None:
    passed, note = CHECK_387(
        _task387_rows(include_midpoints=True, include_transition_lag=True)
    )
    assert passed, note
