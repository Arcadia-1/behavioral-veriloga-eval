"""Task-specific checker for canonical v4 DUT 344."""
from __future__ import annotations

from ..api import Checker
from _bisect import bisect_left

SETTLE = 6.5e-10
VDD = 0.9
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

def check_v4_344_segmented_dac_dem_system(rows: list[dict[str, float]]) -> tuple[bool, str]:
    code_bits = [f"code_{bit}" for bit in range(6)]
    sel_bits = [f"sel_{bit}" for bit in range(8)]
    ptr_bits = [f"ptr_{bit}" for bit in range(3)]
    required = {"time", "clk", "rst", "vout", *code_bits, *sel_bits, *ptr_bits}
    missing = _missing(rows, required)
    if missing:
        return False, f"v4_344 missing_signals={','.join(missing)}"
    errors: list[str] = []
    reset_clear = any(
        _high(row, "rst") and abs(float(row["vout"])) < 0.04
        and _code(row, sel_bits) == 0 and _code(row, ptr_bits) == 0
        for row in rows
    )
    if not reset_clear:
        _mismatch(errors, "P_DEM_RESET_CLEAR", 0.0, "vout/mask/pointer clear", "not observed")
    pointer = 0
    checks = 0
    request_coverage: set[int] = set()
    for index in _rising_indices(rows, "clk"):
        edge = rows[index]
        time_s = float(edge["time"])
        if _high(edge, "rst"):
            pointer = 0
            continue
        code = _code(edge, code_bits)
        request = code >> 3
        fine = code & 7
        old_pointer = pointer
        pointer = (pointer + request) % 8
        expected_mask = sum(1 << ((old_pointer + offset) % 8) for offset in range(request))
        observed = _row_after(rows, time_s)
        observed_mask = _code(observed, sel_bits)
        observed_pointer = _code(observed, ptr_bits)
        expected_vout = VDD * (request * 8 + fine) / 63.0
        if observed_mask != expected_mask:
            _mismatch(errors, "P_DEM_ROTATED_MASK", time_s, expected_mask, observed_mask, abs(expected_mask - observed_mask))
        if observed_pointer != pointer:
            _mismatch(errors, "P_DEM_POINTER_ADVANCE", time_s, pointer, observed_pointer, abs(pointer - observed_pointer))
        if _gap(expected_vout, float(observed["vout"])) > 0.035:
            _mismatch(errors, "P_DEM_DAC_TRANSFER", time_s, expected_vout, float(observed["vout"]), _gap(expected_vout, float(observed["vout"])))
        request_coverage.add(request)
        checks += 1
    return _finish("v4_344", checks, errors, f"reset_clear={reset_clear} request_counts={sorted(request_coverage)}", 6)

CHECKER_ID = "v4_344_segmented_dac_dem_system"
CHECKER: Checker = check_v4_344_segmented_dac_dem_system
