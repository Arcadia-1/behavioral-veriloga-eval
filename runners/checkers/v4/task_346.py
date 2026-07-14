"""Task-specific checker for canonical v4 DUT 346."""
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

def check_v4_346_tdc_measurement_system(rows: list[dict[str, float]]) -> tuple[bool, str]:
    bits = [f"code_{bit}" for bit in range(8)]
    required = {"time", "start", "stop", "clk", "rst", "valid", "overflow", *bits}
    missing = _missing(rows, required)
    if missing:
        return False, f"v4_346 missing_signals={','.join(missing)}"
    errors: list[str] = []
    reset_clear = any(
        _high(row, "rst") and _code(row, bits) == 0 and not _high(row, "valid") and not _high(row, "overflow")
        for row in rows
    )
    if not reset_clear:
        _mismatch(errors, "P_TDC_RESET_CLEAR", 0.0, "code/valid/overflow clear", "not observed")
    starts = _rising_indices(rows, "start")
    stops = _rising_indices(rows, "stop")
    clocks = _rising_indices(rows, "clk")
    checks = 0
    overflow_seen = False
    for ordinal, start_index in enumerate(starts):
        start_time = float(rows[start_index]["time"])
        next_start = float(rows[starts[ordinal + 1]]["time"]) if ordinal + 1 < len(starts) else float("inf")
        cleared = _row_after(rows, start_time)
        if _high(cleared, "valid") or _high(cleared, "overflow"):
            _mismatch(errors, "P_TDC_RESTART_CLEAR", start_time, "valid=0 overflow=0", f"valid={int(_high(cleared,'valid'))} overflow={int(_high(cleared,'overflow'))}")
        stop_candidates = [index for index in stops if start_time < float(rows[index]["time"]) < next_start]
        stop_time = float(rows[stop_candidates[0]]["time"]) if stop_candidates else float("inf")
        clock_times = [float(rows[index]["time"]) for index in clocks if start_time < float(rows[index]["time"]) < min(stop_time, next_start)]
        if len(clock_times) >= 256 and stop_time > clock_times[255]:
            sample_time = clock_times[255]
            expected_code = 255
            expected_overflow = True
        elif stop_candidates:
            sample_time = stop_time
            expected_code = min(255, len(clock_times))
            expected_overflow = False
        else:
            continue
        observed = _row_after(rows, sample_time)
        observed_code = _code(observed, bits)
        if observed_code != expected_code:
            _mismatch(errors, "P_TDC_INTERVAL_COUNT", sample_time, expected_code, observed_code, abs(expected_code - observed_code))
        if not _high(observed, "valid"):
            _mismatch(errors, "P_TDC_VALID_LATCH", sample_time, 1, 0, 1.0)
        if _high(observed, "overflow") != expected_overflow:
            _mismatch(errors, "P_TDC_OVERFLOW", sample_time, int(expected_overflow), int(_high(observed, "overflow")), 1.0)
        overflow_seen = overflow_seen or expected_overflow
        checks += 1
    return _finish("v4_346", checks, errors, f"reset_clear={reset_clear} overflow_exercised={overflow_seen}", 2)

CHECKER_ID = "v4_346_tdc_measurement_system"
CHECKER: Checker = check_v4_346_tdc_measurement_system
