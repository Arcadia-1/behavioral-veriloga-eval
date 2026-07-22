from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

from checkers.v4.task_140 import check_v3_rs_latch_voltage
from checkers.v4.task_201 import check_v3_cdac_6b_stage1_up


SOURCE = (
    ROOT
    / "benchmark-vabench-release-v4"
    / "provenance"
    / "dut-base-v3-exact-five-hash-bound-v2"
)


def _numbers_from_wave(line: str) -> list[float]:
    match = re.search(r"wave=\[([^\]]+)\]", line)
    assert match is not None
    values = match.group(1).split()
    return [float(value.removesuffix("n")) for value in values[1::2]]


def test_140_score_deck_distinguishes_public_045_threshold() -> None:
    deck = (SOURCE / "140-rs-latch-voltage" / "evaluator" / "score_tb.scs").read_text()
    input_levels: list[float] = []
    for line in deck.splitlines():
        if line.startswith(("Vs ", "Vr ")):
            input_levels.extend(_numbers_from_wave(line))
    assert any(0.45 < level < 0.7 for level in input_levels)


def test_140_checker_accepts_static_reset_level_just_above_threshold() -> None:
    rows: list[dict[str, float]] = []

    def extend(start_ns: int, stop_ns: int, *, s: float, r: float, q: int) -> None:
        for time_ns in range(start_ns, stop_ns):
            rows.append(
                {
                    "time": time_ns * 1e-9,
                    "vin_s": s,
                    "vin_r": r,
                    "vout_q": 0.9 if q else 0.0,
                    "vout_qbar": 0.0 if q else 0.9,
                }
            )

    extend(0, 10, s=0.0, r=0.0, q=0)
    extend(10, 20, s=0.9, r=0.0, q=1)
    extend(20, 30, s=0.0, r=0.0, q=1)
    extend(30, 40, s=0.0, r=0.5, q=0)
    extend(40, 50, s=0.0, r=0.0, q=0)

    ok, detail = check_v3_rs_latch_voltage(rows)
    assert ok, detail
    assert "'reset'" in detail


def _cdac_trace(*, include_lsb_controls: bool) -> list[dict[str, float]]:
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
    if include_lsb_controls:
        event(6.0, {"dctrl1": 1.0, "vres": 1.16875})
        event(7.0, {"dctrl0": 1.0, "vres": 1.184375})
    event(8.0, {"clks": 1.0, "vin": -0.1})
    event(9.0, {"clks": 0.0, "vres": -0.1})
    rows.append({"time": 10.0e-9, **signals})
    return rows


def test_201_checker_requires_lsb_control_weights() -> None:
    assert check_v3_cdac_6b_stage1_up(_cdac_trace(include_lsb_controls=True))[0]
    ok, detail = check_v3_cdac_6b_stage1_up(_cdac_trace(include_lsb_controls=False))
    assert not ok
    assert "dctrl0" in detail and "dctrl1" in detail


def test_201_score_deck_drives_all_control_bits() -> None:
    deck = (SOURCE / "201-cdac-6b-stage1-up" / "evaluator" / "score_tb.scs").read_text()
    for bit in range(6):
        assert f"Vd{bit} (dctrl{bit} 0) vsource type=pulse" in deck
