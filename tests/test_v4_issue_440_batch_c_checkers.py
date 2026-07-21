from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

from checkers.v4.task_201 import check_v3_cdac_6b_stage1_up
from checkers.v4.task_206 import check_v3_sar_comparator_reset_high
from checkers.v4.task_214 import check_v3_comparator_reset_low_1p8


def _cdac_trace(*, repeated_sample: bool) -> list[dict[str, float]]:
    signals = {
        "vin": 0.2,
        "clks": 1.0,
        "vres": 0.2,
        **{f"dctrl{bit}": 0.0 for bit in range(6)},
    }
    rows: list[dict[str, float]] = [{"time": 0.0, **signals}]

    def event(time_ns: float, updates: dict[str, float]) -> None:
        rows.append({"time": (time_ns - 0.1) * 1e-9, **signals})
        signals.update(updates)
        rows.append({"time": (time_ns + 0.1) * 1e-9, **signals})
        rows.append({"time": (time_ns + 0.35) * 1e-9, **signals})

    event(1.0, {"clks": 0.0})
    event(2.0, {"dctrl5": 1.0, "vres": 0.7})
    event(3.0, {"dctrl4": 1.0, "vres": 0.95})
    event(4.0, {"dctrl3": 1.0, "vres": 1.075})
    event(5.0, {"dctrl2": 1.0, "vres": 1.1375})
    event(5.4, {"dctrl1": 1.0, "vres": 1.16875})
    event(5.7, {"dctrl0": 1.0, "vres": 1.184375})
    if repeated_sample:
        event(6.0, {"clks": 1.0, "vin": -0.1})
        event(7.0, {"clks": 0.0, "vres": -0.1})
    rows.append({"time": 8.0e-9, **signals})
    return rows


def _comparator_trace(*, reset_high: bool, include_equal: bool) -> list[dict[str, float]]:
    vdd = 0.9 if reset_high else 1.8
    reset = vdd if reset_high else 0.0
    rows: list[dict[str, float]] = []
    time_ns = 0.0
    scenarios = [(0.7 * vdd, 0.5 * vdd), (0.3 * vdd, 0.5 * vdd)]
    if include_equal:
        scenarios.append((0.5 * vdd, 0.5 * vdd))
    else:
        scenarios.append((0.7 * vdd, 0.5 * vdd))
    for vinp, vinn in scenarios:
        rows.append({"time": time_ns * 1e-9, "cmpck": 0.0, "vinp": vinp, "vinn": vinn,
                     "dcmpp": reset, "dcmpn": reset})
        rows.append({"time": (time_ns + 0.1) * 1e-9, "cmpck": vdd, "vinp": vinp, "vinn": vinn,
                     "dcmpp": reset, "dcmpn": reset})
        if vinp > vinn:
            decision = (vdd, 0.0)
        elif vinp < vinn:
            decision = (0.0, vdd)
        else:
            decision = (0.0, 0.0)
        rows.append({"time": (time_ns + 0.12) * 1e-9, "cmpck": vdd, "vinp": vinp, "vinn": vinn,
                     "dcmpp": decision[0], "dcmpn": decision[1]})
        rows.append({"time": (time_ns + 0.35) * 1e-9, "cmpck": vdd, "vinp": vinp, "vinn": vinn,
                     "dcmpp": decision[0], "dcmpn": decision[1]})
        rows.append({"time": (time_ns + 0.6) * 1e-9, "cmpck": 0.0, "vinp": vinp, "vinn": vinn,
                     "dcmpp": decision[0], "dcmpn": decision[1]})
        rows.append({"time": (time_ns + 0.62) * 1e-9, "cmpck": 0.0, "vinp": vinp, "vinn": vinn,
                     "dcmpp": reset, "dcmpn": reset})
        rows.append({"time": (time_ns + 0.85) * 1e-9, "cmpck": 0.0, "vinp": vinp, "vinn": vinn,
                     "dcmpp": reset, "dcmpn": reset})
        time_ns += 1.2
    return rows


def test_201_requires_a_changed_repeated_sample_event() -> None:
    assert check_v3_cdac_6b_stage1_up(_cdac_trace(repeated_sample=True))[0]
    assert not check_v3_cdac_6b_stage1_up(_cdac_trace(repeated_sample=False))[0]


def test_206_requires_equal_input_decision_coverage() -> None:
    assert check_v3_sar_comparator_reset_high(
        _comparator_trace(reset_high=True, include_equal=True)
    )[0]
    assert not check_v3_sar_comparator_reset_high(
        _comparator_trace(reset_high=True, include_equal=False)
    )[0]


def test_214_requires_equal_input_decision_coverage() -> None:
    assert check_v3_comparator_reset_low_1p8(
        _comparator_trace(reset_high=False, include_equal=True)
    )[0]
    assert not check_v3_comparator_reset_low_1p8(
        _comparator_trace(reset_high=False, include_equal=False)
    )[0]
