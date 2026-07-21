from __future__ import annotations

import sys
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

from checkers.v4.task_358 import CHECKER as CHECKER_358
from checkers.v4.task_362 import CHECKER as CHECKER_362
from checkers.v4.task_363 import CHECKER as CHECKER_363


def _square(time_s: float, *, first_rise: float, period: float, width: float) -> float:
    if time_s < first_rise:
        return 0.0
    elapsed = time_s - first_rise
    cycle = math.floor(elapsed / period + 1e-12)
    phase = elapsed - cycle * period
    return 0.9 if phase < width - 1e-15 else 0.0


def _bits(code: int, prefix: str, width: int) -> dict[str, float]:
    return {f"{prefix}_{bit}": 0.9 if code & (1 << bit) else 0.0 for bit in range(width)}


def _trace_358(
    *,
    wrong_source: bool = False,
    reversed_delay: bool = False,
    missing_delay: bool = False,
) -> list[dict[str, float]]:
    codes = [2, 7, 8, 12, 17, 24, 30, 5, 2]
    rows: list[dict[str, float]] = []
    for index in range(10_001):
        time_s = index * 10e-12
        rst = 0.9 if time_s < 3e-9 else 0.0
        code = codes[min(len(codes) - 1, max(0, int((time_s - 5e-9) // 10e-9)))]
        clk_i = _square(time_s, first_rise=10e-9, period=10e-9, width=2e-9)
        clk_q = _square(time_s, first_rise=12.5e-9, period=10e-9, width=2e-9)
        quadrant = code // 8
        intra_code = code % 8
        delay_code = 0 if missing_delay else (7 - intra_code) if reversed_delay else intra_code
        delay = delay_code * 5e-12
        selected = _square(
            time_s - delay,
            first_rise=10e-9 if quadrant in (0, 2) else 12.5e-9,
            period=10e-9,
            width=2e-9,
        )
        rows.append(
            {
                "time": time_s,
                "clk_i": clk_i,
                "clk_q": clk_q,
                "rst": rst,
                **_bits(code, "code", 5),
                "clk_out": 0.0 if rst else (clk_i if wrong_source else selected),
                "quadrant_1": 0.0 if rst else (0.9 if quadrant & 2 else 0.0),
                "quadrant_0": 0.0 if rst else (0.9 if quadrant & 1 else 0.0),
                "phase_metric": 0.0 if rst else 0.9 * code / 31.0,
            }
        )
    return rows


def _trace_362(*, corrupt_metric: bool = False) -> list[dict[str, float]]:
    step = 50e-12
    stop = 190e-9
    rows: list[dict[str, float]] = []
    dco_state = div_state = rise_count = 0
    next_toggle: float | None = None
    previous_enable = False
    for index in range(round(stop / step) + 1):
        time_s = index * step
        rst = time_s < 1.3e-9 or 164.1e-9 <= time_s < 170.1e-9
        enable = (3.1e-9 <= time_s < 118.1e-9) or (131.1e-9 <= time_s < 162.1e-9) or time_s >= 171.1e-9
        code = 0 if time_s < 44.1e-9 else 21 if time_s < 82.1e-9 else 46
        target = min(250e6, 80e6 + 2e6 * code)
        active = enable and not rst
        if not active:
            dco_state = div_state = rise_count = 0
            next_toggle = None
        elif not previous_enable:
            next_toggle = time_s + 0.5 / target
        while active and next_toggle is not None and time_s + 0.25 * step >= next_toggle:
            dco_state = 1 - dco_state
            if dco_state:
                rise_count += 1
                if rise_count == 4:
                    rise_count = 0
                    div_state = 1 - div_state
            next_toggle += 0.5 / target
        metric = 0.9 * (target - 80e6) / 170e6 if active else 0.0
        if corrupt_metric and 30e-9 <= time_s <= 31e-9:
            metric = 0.9
        rows.append(
            {
                "time": time_s,
                "enable": 0.9 if enable else 0.0,
                "rst": 0.9 if rst else 0.0,
                **_bits(code, "fcw", 6),
                "dco_clk": 0.9 * dco_state,
                "div_clk": 0.9 * div_state,
                "freq_metric": metric,
            }
        )
        previous_enable = active
    return rows


def _trace_363(*, corrupt_selection: bool = False) -> list[dict[str, float]]:
    step = 50e-12
    stop = 360e-9
    decision_edges: list[tuple[float, int, int]] = []
    for start, end in ((5.1e-9, 320.1e-9), (332.1e-9, stop + step)):
        accumulator = carry = count = div_state = decisions = 0
        for rise_index in range(1, 2000):
            edge = 1.3e-9 + (rise_index - 1) * 600e-12
            if edge <= start:
                continue
            if edge >= end:
                break
            count += 1
            if count < 8 + carry:
                continue
            count = 0
            div_state = 1 - div_state
            decision_edges.append((edge, div_state, carry))
            accumulator += 15
            carry = int(accumulator >= 16)
            accumulator %= 16
            decisions += 1

    rows: list[dict[str, float]] = []
    for index in range(round(stop / step) + 1):
        time_s = index * step
        rst = time_s < 3.1e-9
        enable = (5.1e-9 <= time_s < 320.1e-9) or time_s >= 332.1e-9
        active_edges = [item for item in decision_edges if item[0] <= time_s]
        if not enable or rst:
            div_state = selection = 0
        elif active_edges:
            _, div_state, selection = active_edges[-1]
        else:
            div_state = selection = 0
        if corrupt_selection and 247.4e-9 < time_s < 252.0e-9:
            selection = 1 - selection
        decision_count = sum(1 for edge, _, _ in active_edges if edge >= 5.1e-9)
        valid = bool(active_edges) and time_s - active_edges[-1][0] < 0.2e-9 and decision_count % 16 == 0
        rows.append(
            {
                "time": time_s,
                "ref_clk": _square(time_s, first_rise=3e-9, period=18e-9, width=9e-9),
                "dco_clk": _square(time_s, first_rise=1.3e-9, period=600e-12, width=300e-12),
                "rst": 0.9 if rst else 0.0,
                "enable": 0.9 if enable else 0.0,
                **_bits(15, "frac", 4),
                "div_clk": 0.9 * div_state,
                "div_sel": 0.9 * selection,
                "avg_ratio_metric": 8.9375 if active_edges and enable else 0.0,
                "valid": 0.9 if valid else 0.0,
            }
        )
    return rows


def _time_transform(rows: list[dict[str, float]], scale: float, shift: float) -> list[dict[str, float]]:
    return [{**row, "time": row["time"] * scale + shift} for row in rows]


def test_358_rejects_activity_unrelated_to_selected_quadrature_reference() -> None:
    rows = _trace_358()
    assert CHECKER_358(rows)[0]
    assert CHECKER_358(_time_transform(rows, 1.37, 2e-9))[0]
    passed, detail = CHECKER_358(_trace_358(wrong_source=True))
    assert not passed
    assert "P_SELECTED_EDGE_DELAY" in detail
    passed, detail = CHECKER_358(_trace_358(reversed_delay=True))
    assert not passed
    assert "P_SELECTED_EDGE_DELAY" in detail


def test_358_rejects_missing_intra_code_delay() -> None:
    passed, detail = CHECKER_358(_trace_358(missing_delay=True))
    assert not passed
    assert "delay_step" in detail


def test_362_allows_only_explicit_metric_update_transients() -> None:
    rows = _trace_362()
    assert CHECKER_362(rows)[0]
    passed, detail = CHECKER_362(_trace_362(corrupt_metric=True))
    assert not passed
    assert "P_FREQUENCY_WORD_MAPPING status=FAIL" in detail


def test_363_uses_an_independent_accumulator_reference() -> None:
    rows = _trace_363()
    assert CHECKER_363(rows)[0]
    assert CHECKER_363(_time_transform(rows, 1.19, 3e-9))[0]
    passed, detail = CHECKER_363(_trace_363(corrupt_selection=True))
    assert not passed
    assert "P_FRACTIONAL_SELECTION status=FAIL" in detail
