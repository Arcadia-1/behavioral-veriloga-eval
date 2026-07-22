from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

from checkers.v4.task_184 import check_v4_offset_rdac_search_flow


SIGNALS = ("vinp", "vinn", "vrefp", "vrefn", "dc0", "dc1", "dc2", "dc3", "dc4", "dc5", "dc6")


def _expected(vin: float, vref: float, codes: list[int]) -> dict[str, float]:
    row = {
        "vinp": 0.6 + 0.5 * vin,
        "vinn": 0.6 - 0.5 * vin,
        "vrefp": 0.6 + 0.5 * vref,
        "vrefn": 0.6 - 0.5 * vref,
    }
    row.update({f"dc{bit}": float(value) for bit, value in enumerate(codes)})
    return row


def _row(time_ns: float, *, ck: float, d: int, values: dict[str, float]) -> dict[str, float]:
    return {"time": time_ns * 1e-9, "ck": ck, "d": float(1 - d), **values}


def _task184_rows(*, fixed_foreground_state: bool) -> list[dict[str, float]]:
    lsb = 1.0 / 16.0
    vref = -17.0 / 2.0 * lsb
    vin = vref
    step = 0.04
    state = 1
    iteration = 6
    offset_phase = False
    codes = [0, 0, 0, 0, 0, 0, 1]
    values = _expected(vin, vref, codes)
    decisions = [1, 0, 1, 0, 1, 0, 1, *([1] * 8), 0, 1]
    rows = [_row(0.0, ck=0.0, d=decisions[0], values=values)]

    for index, decision in enumerate(decisions, start=1):
        edge_ns = float(index)
        rows.append(_row(edge_ns - 0.05, ck=0.0, d=decision, values=values))
        rows.append(_row(edge_ns, ck=1.0, d=decision, values=values))
        if not offset_phase:
            if iteration > 0:
                next_bit = iteration - 1
                codes[next_bit] = 1
                if not decision:
                    codes[iteration] = 0
                if not fixed_foreground_state:
                    state = decision
                iteration -= 1
            else:
                offset_phase = True
                iteration = 0
                step = 0.04
        elif iteration == 8:
            iteration = 6
            step = 0.04
            offset_phase = False
        else:
            if state != decision and step > 0.0:
                step /= 2.0
            state = decision
            vin += (2 * state - 1) * step
            iteration += 1
            if iteration == 8:
                vref += lsb
                vin = vref
                codes = [0, 0, 0, 0, 0, 0, 1]
        values = _expected(vin, vref, codes)
        rows.append(_row(edge_ns + 0.20, ck=1.0, d=decision, values=values))
        rows.append(_row(edge_ns + 0.45, ck=0.0, d=decision, values=values))

    assert set(SIGNALS).issubset(rows[0])
    return rows


def test_task184_uses_last_foreground_direction_for_first_offset_comparison() -> None:
    ok, detail = check_v4_offset_rdac_search_flow(_task184_rows(fixed_foreground_state=False))
    assert ok, detail

    ok, detail = check_v4_offset_rdac_search_flow(_task184_rows(fixed_foreground_state=True))
    assert not ok
    assert "P_OFFSET_SEARCH_BISECTION" in detail
