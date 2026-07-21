from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

from checkers.v4.task_178 import check_v3_onehot_progress_encoder
from checkers.v4.task_187 import check_v3_adc_sample_clock_sequencer


def _rows_178(*, broken_signal: str | None = None) -> list[dict[str, float]]:
    rows = []
    for step in range(171):
        time_ns = step / 10.0
        completed = min(16, max(0, int(time_ns)))
        row = {
            "time": time_ns * 1e-9,
            "ck": 1.0 if any(abs(time_ns - (index + 1.02)) < 0.04 for index in range(16)) else 0.0,
            "sum": float(completed),
        }
        for index in range(16):
            signal = f"d{index}"
            row[signal] = 1.0 if index < completed else 0.0
        if broken_signal is not None:
            row[broken_signal] = 0.0
        rows.append(row)
    return rows


def _rows_187(*, collapse_ss_to_s: bool = False) -> list[dict[str, float]]:
    def high(time_ns: float, windows: list[tuple[float, float]]) -> float:
        phase = time_ns % 18.0
        return 0.9 if any(start <= phase < end for start, end in windows) else 0.0

    rows = []
    for step in range(221):
        time_ns = step / 10.0
        s = high(time_ns, [(0.6, 1.0), (6.6, 7.0), (12.6, 13.0)])
        rows.append({
            "time": time_ns * 1e-9,
            "rst": high(time_ns, [(0.0, 0.25)]),
            "s": s,
            "ss": s if collapse_ss_to_s else high(time_ns, [(0.6, 1.2), (6.6, 7.2), (12.6, 13.2)]),
            "nc_az": high(time_ns, [(1.35, 1.55), (7.35, 7.55), (13.35, 13.55)]),
            "nc": high(time_ns, [(1.7, 2.05), (7.7, 8.05), (13.7, 14.05)]),
            "conv": high(time_ns, [(2.4, 5.4), (8.4, 11.4), (14.4, 17.4)]),
        })
    return rows


def test_task_178_checks_every_progress_output() -> None:
    assert check_v3_onehot_progress_encoder(_rows_178())[0]
    ok, detail = check_v3_onehot_progress_encoder(_rows_178(broken_signal="d8"))
    assert not ok
    assert "d8" in detail


def test_task_187_distinguishes_sample_and_wide_sample_pulses() -> None:
    assert check_v3_adc_sample_clock_sequencer(_rows_187())[0]
    ok, detail = check_v3_adc_sample_clock_sequencer(_rows_187(collapse_ss_to_s=True))
    assert not ok
    assert "ss@1.1ns" in detail
