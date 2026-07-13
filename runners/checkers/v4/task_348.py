"""Task-specific checker for canonical v4 DUT 348."""
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

def check_v4_348_vga_gain_calibration_loop(rows: list[dict[str, float]]) -> tuple[bool, str]:
    bits = ["gain_0", "gain_1", "gain_2", "gain_3"]
    required = {"time", "vin", "target", "clk", "rst", "start", "vout", "locked", "peak_metric", *bits}
    missing = _missing(rows, required)
    if missing:
        return False, f"v4_348 missing_signals={','.join(missing)}"
    errors: list[str] = []
    gain_code = 4
    peak = 0.0
    lock_count = 0
    locked = False
    checks = 0
    directions: set[str] = set()
    observed_codes: set[int] = set()
    for index in _rising_indices(rows, "clk"):
        edge = rows[index]
        time_s = float(edge["time"])
        if _high(edge, "rst"):
            gain_code = 4
            peak = 0.0
            lock_count = 0
            locked = False
        elif _high(edge, "start"):
            target = float(edge["target"])
            if peak < target - 20e-3:
                new_code = min(15, gain_code + 1)
                if new_code > gain_code:
                    directions.add("up")
                gain_code = new_code
            elif peak > target + 20e-3:
                new_code = max(0, gain_code - 1)
                if new_code < gain_code:
                    directions.add("down")
                gain_code = new_code
            if abs(peak - target) <= 20e-3:
                lock_count = min(3, lock_count + 1)
            else:
                lock_count = 0
            locked = lock_count >= 3
            peak = abs(float(edge["vin"]))
        observed = _row_after(rows, time_s)
        observed_code = _code(observed, bits)
        observed_codes.add(observed_code)
        if observed_code != gain_code:
            _mismatch(errors, "P_VGA_GAIN_DIRECTION", time_s, gain_code, observed_code, abs(gain_code - observed_code))
        if _gap(peak, float(observed["peak_metric"])) > 0.025:
            _mismatch(errors, "P_VGA_PEAK_SAMPLE", time_s, peak, float(observed["peak_metric"]), _gap(peak, float(observed["peak_metric"])))
        if _high(observed, "locked") != locked:
            _mismatch(errors, "P_VGA_LOCK_QUALIFICATION", time_s, int(locked), int(_high(observed, "locked")), 1.0)
        expected_vout = (0.5 + 0.1 * observed_code) * float(observed["vin"])
        if _gap(expected_vout, float(observed["vout"])) > 0.04:
            _mismatch(errors, "P_VGA_OUTPUT_GAIN", time_s, expected_vout, float(observed["vout"]), _gap(expected_vout, float(observed["vout"])))
        checks += 1
    return _finish("v4_348", checks, errors, f"directions={sorted(directions)} codes={sorted(observed_codes)} locked_seen={any(_high(r,'locked') for r in rows)}", 12)

CHECKER_ID = "v4_348_vga_gain_calibration_loop"
CHECKER: Checker = check_v4_348_vga_gain_calibration_loop
