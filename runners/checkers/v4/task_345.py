"""Task-specific checker for canonical v4 DUT 345."""
from __future__ import annotations

from ..api import Checker
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

def check_v4_345_offset_calibrated_comparator_system(rows: list[dict[str, float]]) -> tuple[bool, str]:
    bits = ["offset_0", "offset_1", "offset_2", "offset_3"]
    required = {"time", "vinp", "vinn", "clk", "rst", "cal_en", "cal_ref", "decision", "ready", "threshold_dbg", *bits}
    missing = _missing(rows, required)
    if missing:
        return False, f"v4_345 missing_signals={','.join(missing)}"
    errors: list[str] = []
    reset_clear = any(
        _high(row, "rst") and _code(row, bits) == 0 and not _high(row, "decision")
        and not _high(row, "ready") and abs(float(row["threshold_dbg"])) < 0.01
        for row in rows
    )
    if not reset_clear:
        _mismatch(errors, "P_CAL_RESET_CLEAR", 0.0, "code/decision/ready/threshold clear", "not observed")
    code = 0
    updates = 0
    in_window = False
    ready = False
    checks = 0
    directions: set[str] = set()
    for index in _rising_indices(rows, "clk"):
        edge = rows[index]
        time_s = float(edge["time"])
        if _high(edge, "rst"):
            code = 0
            updates = 0
            in_window = False
            ready = False
        elif _high(edge, "cal_en"):
            if not in_window:
                updates = 0
                ready = False
                in_window = True
            if _high(edge, "cal_ref"):
                code = min(15, code + 1)
                directions.add("up")
            else:
                code = max(0, code - 1)
                directions.add("down")
            updates += 1
            if updates >= 4:
                ready = True
        else:
            in_window = False
        observed = _row_after(rows, time_s)
        observed_code = _code(observed, bits)
        expected_threshold = 0.0 if _high(edge, "rst") else (code - 8) * 5e-3
        if observed_code != code:
            _mismatch(errors, "P_CAL_CODE_UPDATE", time_s, code, observed_code, abs(code - observed_code))
        if _gap(expected_threshold, float(observed["threshold_dbg"])) > 0.008:
            _mismatch(errors, "P_CAL_OFFSET_DAC", time_s, expected_threshold, float(observed["threshold_dbg"]), _gap(expected_threshold, float(observed["threshold_dbg"])))
        if _high(observed, "ready") != ready:
            _mismatch(errors, "P_CAL_READY_QUALIFICATION", time_s, int(ready), int(_high(observed, "ready")), 1.0)
        expected_decision = False if _high(edge, "rst") else (float(observed["vinp"]) - float(observed["vinn"]) + float(observed["threshold_dbg"]) >= 0.0)
        if _high(observed, "decision") != expected_decision:
            _mismatch(errors, "P_CAL_COMPARATOR_DECISION", time_s, int(expected_decision), int(_high(observed, "decision")), 1.0)
        checks += 1
    return _finish("v4_345", checks, errors, f"reset_clear={reset_clear} directions={sorted(directions)} final_code={code}", 8)

CHECKER_ID = "v4_345_offset_calibrated_comparator_system"
CHECKER: Checker = check_v4_345_offset_calibrated_comparator_system
