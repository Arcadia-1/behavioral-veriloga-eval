from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

from checkers.v4.task_075 import check_v4_peak_detector
from checkers.v4.task_105 import check_v3_single_shot


def _peak_rows(*, continuous_peak: bool) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    retained = 0.0
    sample_period_ns = 0.5
    for step in range(0, 91):
        time_ns = step / 10.0
        rst = 0.9 if time_ns < 1.5 or 4.0 <= time_ns < 5.5 else 0.0
        vin = 0.12
        if 2.2 <= time_ns <= 2.3:
            vin = 0.82
        elif 6.2 <= time_ns <= 6.3:
            vin = 0.86
        elif rst <= 0.45:
            vin = 0.22
        if rst > 0.45:
            retained = 0.0
        elif continuous_peak:
            retained = max(retained, vin)
        elif abs((time_ns / sample_period_ns) - round(time_ns / sample_period_ns)) < 1.0e-9:
            retained = max(retained, vin)
        rows.append({
            "time": time_ns * 1e-9,
            "vin": vin,
            "rst": rst,
            "vout": retained,
        })
    return rows


def _single_shot_rows(*, stop_ns: float, second_input_edge: bool, second_output_pulse: bool) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for step in range(int(stop_ns * 10) + 1):
        time_ns = step / 10.0
        vin = 0.9 if 5.0 <= time_ns < 9.0 else 0.0
        if second_input_edge and 25.0 <= time_ns < 29.0:
            vin = 0.9
        vout = 0.9 if 6.0 <= time_ns < 16.0 else 0.0
        if second_output_pulse and 26.0 <= time_ns < 36.0:
            vout = 0.9
        rows.append({"time": time_ns * 1e-9, "vin": vin, "vout": vout})
    return rows


def test_task_075_rejects_continuous_peak_shortcut_between_timer_samples() -> None:
    assert check_v4_peak_detector(_peak_rows(continuous_peak=False))[0]
    ok, detail = check_v4_peak_detector(_peak_rows(continuous_peak=True))
    assert not ok
    assert "P_SAMPLED_MEASUREMENT" in detail or "P_MAX_RETENTION" in detail


def test_task_105_harness_must_reach_second_trigger_edge() -> None:
    # The old score deck stopped at 22 ns, before the 25 ns second rising edge,
    # so an implementation that only handled the first pulse was indistinguishable.
    assert check_v3_single_shot(
        _single_shot_rows(stop_ns=22.0, second_input_edge=False, second_output_pulse=False)
    )[0]

    ok, detail = check_v3_single_shot(
        _single_shot_rows(stop_ns=45.0, second_input_edge=True, second_output_pulse=False)
    )
    assert not ok
    assert "onset_missing@24.95ns" in detail

    assert check_v3_single_shot(
        _single_shot_rows(stop_ns=45.0, second_input_edge=True, second_output_pulse=True)
    )[0]
