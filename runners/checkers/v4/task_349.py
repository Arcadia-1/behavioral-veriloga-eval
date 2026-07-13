"""Task-specific checker for canonical v4 DUT 349."""
from __future__ import annotations

from checkers.api import Checker
from _bisect import bisect_left

SETTLE = 6.5e-10
VTH = 0.45

def _high(row: dict[str, float], signal: str, threshold: float = VTH) -> bool:
    return float(row.get(signal, 0.0)) > threshold

def _missing(rows: list[dict[str, float]], required: set[str]) -> list[str]:
    if not rows:
        return sorted(required)
    return sorted(required - set(rows[0]))

def _rising_indices(rows: list[dict[str, float]], signal: str, threshold: float = VTH) -> list[int]:
    result: list[int] = []
    previous = float(rows[0][signal])
    for index, row in enumerate(rows[1:], 1):
        value = float(row[signal])
        if previous <= threshold < value:
            result.append(index)
        previous = value
    return result

def _row_after(rows: list[dict[str, float]], time_s: float, delay_s: float = SETTLE) -> dict[str, float]:
    times = [float(row["time"]) for row in rows]
    index = bisect_left(times, time_s + delay_s)
    return rows[min(index, len(rows) - 1)]

def _code(row: dict[str, float], lsb_first: list[str]) -> int:
    return sum((1 << bit) for bit, signal in enumerate(lsb_first) if _high(row, signal))

def _gap(expected: float, observed: float) -> float:
    return abs(float(expected) - float(observed))

def _mismatch(
    errors: list[str], property_id: str, time_s: float, expected: object, observed: object, gap: float | None = None
) -> None:
    detail = (
        f"{property_id} mismatch_count=1 sample_time={time_s:.12g} "
        f"expected={expected} observed={observed}"
    )
    if gap is not None:
        detail += f" metric_gap={gap:.6g}"
    errors.append(detail)

def _finish(task_id: str, checks: int, errors: list[str], coverage: str, minimum: int) -> tuple[bool, str]:
    ok = checks >= minimum and not errors
    detail = "; ".join(errors[:6])
    return ok, (
        f"{task_id} checked={checks} mismatch_count={len(errors)} {coverage}"
        + (f" mismatch_detail={detail}" if detail else "")
    )

def check_v4_349_multichannel_sample_readout(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {
        "time", "ch0", "ch1", "ch2", "ch3", "clk", "rst", "sample", "read",
        "out", "ch_sel_1", "ch_sel_0", "valid",
    }
    missing = _missing(rows, required)
    if missing:
        return False, f"v4_349 missing_signals={','.join(missing)}"
    errors: list[str] = []
    held = [0.0, 0.0, 0.0, 0.0]
    pointer = 0
    selected = 0
    out_value = 0.0
    checks = 0
    samples = reads = holds = 0
    for index in _rising_indices(rows, "clk"):
        edge = rows[index]
        time_s = float(edge["time"])
        if _high(edge, "rst"):
            held = [0.0, 0.0, 0.0, 0.0]
            pointer = selected = 0
            out_value = 0.0
            valid = False
        else:
            if _high(edge, "sample"):
                held = [float(edge[f"ch{channel}"]) for channel in range(4)]
                samples += 1
            if _high(edge, "read"):
                selected = pointer
                pointer = (pointer + 1) % 4
                out_value = held[selected]
                valid = True
                reads += 1
            else:
                valid = False
                holds += 1
        observed = _row_after(rows, time_s)
        observed_selected = _code(observed, ["ch_sel_0", "ch_sel_1"])
        if observed_selected != selected:
            _mismatch(errors, "P_READOUT_CHANNEL_ORDER", time_s, selected, observed_selected, abs(selected - observed_selected))
        if _gap(out_value, float(observed["out"])) > 0.035:
            _mismatch(errors, "P_READOUT_HELD_VALUE", time_s, out_value, float(observed["out"]), _gap(out_value, float(observed["out"])))
        if _high(observed, "valid") != valid:
            _mismatch(errors, "P_READOUT_VALID_TIMING", time_s, int(valid), int(_high(observed, "valid")), 1.0)
        checks += 1
    return _finish("v4_349", checks, errors, f"sample_cycles={samples} read_cycles={reads} hold_cycles={holds}", 10)

CHECKER_ID = "v4_349_multichannel_sample_readout"
CHECKER: Checker = check_v4_349_multichannel_sample_readout
