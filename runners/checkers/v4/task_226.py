"""Task-specific checker for canonical v4 DUT 226."""
from __future__ import annotations

from bisect import bisect_right

from ..api import Checker


def _interp(rows: list[dict[str, float]], times: list[float], signal: str, target: float) -> float:
    right = bisect_right(times, target)
    if right == 0:
        return float(rows[0][signal])
    left = right - 1
    if right == len(rows) or times[left] == target:
        return float(rows[left][signal])
    t0 = times[left]
    t1 = times[right]
    if t1 == t0:
        return float(rows[right][signal])
    alpha = (target - t0) / (t1 - t0)
    return float(rows[left][signal]) + alpha * (float(rows[right][signal]) - float(rows[left][signal]))


def _probe_times(rows: list[dict[str, float]], start: float, count: int = 33) -> list[float]:
    end = float(rows[-1]["time"])
    explicit = [float(row["time"]) for row in rows if start <= float(row["time"]) <= end]
    if end <= start:
        return explicit
    uniform = [start + (end - start) * index / (count - 1) for index in range(count)]
    return sorted(set(explicit + uniform))


def check_v3_level_shifter_offset(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "sigin", "sigout"}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0])) if rows else sorted(required)
        return False, "missing_level_shifter_columns=" + ",".join(missing)
    start = 0.10e-9
    times = [float(row["time"]) for row in rows]
    probes = _probe_times(rows, start)
    checked = len(probes)
    if checked < 8:
        return False, f"insufficient_level_shifter_samples={checked}"
    max_err = 0.0
    worst: tuple[float, float, float] | None = None
    input_min = input_max = _interp(rows, times, "sigin", probes[0])
    saw_rise = saw_fall = False
    prior_min = prior_max = input_min
    for time_s in probes:
        sigin = _interp(rows, times, "sigin", time_s)
        sigout = _interp(rows, times, "sigout", time_s)
        expected = sigin + 0.35
        error = abs(sigout - expected)
        if error >= max_err:
            max_err = error
            worst = (time_s, sigout, expected)
        saw_rise = saw_rise or sigin - prior_min > 0.20
        saw_fall = saw_fall or prior_max - sigin > 0.20
        input_min = min(input_min, sigin)
        input_max = max(input_max, sigin)
        prior_min = min(prior_min, sigin)
        prior_max = max(prior_max, sigin)
    if input_max - input_min < 0.50 or not (saw_rise and saw_fall):
        return False, (
            f"insufficient_level_shifter_coverage range={input_min:.3f}:{input_max:.3f} "
            f"rise={saw_rise} fall={saw_fall}"
        )
    if max_err > 0.025:
        assert worst is not None
        time_s, observed, expected = worst
        return False, (
            f"level_shift_error@{time_s * 1e9:.3f}ns observed={observed:.4f} "
            f"expected={expected:.4f} max_err={max_err:.4f}"
        )
    return True, (
        f"checked={checked} input_range={input_min:.3f}:{input_max:.3f} "
        f"rise={saw_rise} fall={saw_fall} max_err={max_err:.4f}"
    )

CHECKER_ID = "v4_226_level_shifter_offset"
CHECKER: Checker = check_v3_level_shifter_offset
