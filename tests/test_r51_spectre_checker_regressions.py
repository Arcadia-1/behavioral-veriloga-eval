from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

from checkers.v4.task_249 import check_v3_pfd_active_low_reset


def _pfd_level(time_ns: float, intervals: list[tuple[float, float]]) -> float:
    return 0.9 if any(start <= time_ns < stop for start, stop in intervals) else 0.0


def _pfd_rows(*, reset_delay_ns: float = 0.08, zero_outputs: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for step in range(76):
        time_ns = 0.04 * step
        ref = _pfd_level(time_ns, [(0.46, 0.66), (1.26, 1.46), (2.46, 2.66)])
        fb = _pfd_level(time_ns, [(1.06, 1.26), (2.06, 2.26), (2.86, 3.06)])
        rstb = _pfd_level(time_ns, [(0.18, 1.50), (1.78, 3.50)])

        up = down = 0.0
        if 0.46 <= time_ns < 1.06 + reset_delay_ns:
            up = 0.9
        if 1.06 <= time_ns < 1.06 + reset_delay_ns:
            down = 0.9
        if 1.26 <= time_ns < 1.50:
            up = 0.9
        if 2.06 <= time_ns < 2.46 + reset_delay_ns:
            down = 0.9
        if 2.46 <= time_ns < 2.46 + reset_delay_ns:
            up = 0.9
        if 2.86 <= time_ns:
            down = 0.9
        if not rstb or zero_outputs:
            up = down = 0.0

        rows.append(
            {
                "time": time_ns * 1.0e-9,
                "ref": ref,
                "fb": fb,
                "rstb": rstb,
                "up": up,
                "down": down,
            }
        )
    return rows


def test_task249_accepts_correct_behavior_when_sparse_rows_miss_the_both_window() -> None:
    ok, detail = check_v3_pfd_active_low_reset(_pfd_rows())
    assert ok, detail


def test_task249_classifies_zero_and_no_delay_as_behavior_errors() -> None:
    for rows in (_pfd_rows(zero_outputs=True), _pfd_rows(reset_delay_ns=0.001)):
        ok, detail = check_v3_pfd_active_low_reset(rows)
        assert not ok
        assert "pfd_external_reset_level_error" in detail
        assert "insufficient" not in detail
