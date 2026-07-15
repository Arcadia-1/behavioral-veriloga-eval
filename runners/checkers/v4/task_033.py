"""Task-specific checker for canonical v4 DUT 033."""
from __future__ import annotations

from ..api import Checker
def mean_in_window(rows: list[dict[str, float]], key: str, start: float, stop: float) -> float | None:
    values = [r[key] for r in rows if start <= r["time"] <= stop and key in r]
    if not values:
        return None
    return sum(values) / len(values)

def time_weighted_mean_in_window(
    rows: list[dict[str, float]],
    key: str,
    start: float,
    stop: float,
) -> float | None:
    if stop <= start:
        return None
    ordered = sorted((r for r in rows if "time" in r and key in r), key=lambda r: r["time"])
    area = 0.0
    duration = 0.0
    for left, right in zip(ordered, ordered[1:]):
        t0 = float(left["time"])
        t1 = float(right["time"])
        if t1 <= t0:
            continue
        lo = max(start, t0)
        hi = min(stop, t1)
        if hi <= lo:
            continue
        v0 = float(left[key])
        v1 = float(right[key])

        def interp(t: float) -> float:
            frac = (t - t0) / (t1 - t0)
            return v0 + frac * (v1 - v0)

        area += 0.5 * (interp(lo) + interp(hi)) * (hi - lo)
        duration += hi - lo
    if duration > 0.0:
        return area / duration
    return mean_in_window(rows, key, start, stop)

def check_log_rssi_power_detector(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst/vin/out/metric"

    floor = time_weighted_mean_in_window(rows, "out", 5.0e-9, 7.5e-9)
    small = time_weighted_mean_in_window(rows, "out", 12.0e-9, 22.0e-9)
    mid = time_weighted_mean_in_window(rows, "out", 30.0e-9, 40.0e-9)
    high = time_weighted_mean_in_window(rows, "out", 50.0e-9, 60.0e-9)
    high_metric = time_weighted_mean_in_window(rows, "metric", 50.0e-9, 60.0e-9)
    if None in (floor, small, mid, high, high_metric):
        return False, "rssi_missing_sample_windows"
    assert floor is not None
    assert small is not None
    assert mid is not None
    assert high is not None
    assert high_metric is not None

    if not (0.08 <= floor <= 0.16):
        return False, f"rssi_floor_wrong={floor:.3f}"
    if not (small + 0.12 <= mid <= high - 0.10):
        return False, f"rssi_not_monotonic_loglike small/mid/high={small:.3f}/{mid:.3f}/{high:.3f}"
    if (high - mid) >= (mid - small):
        return False, f"rssi_large_step_not_compressed small/mid/high={small:.3f}/{mid:.3f}/{high:.3f}"
    if high_metric < 0.55:
        return False, f"rssi_metric_low={high_metric:.3f}"
    return True, f"log_rssi_power_detector floor/small/mid/high={floor:.3f}/{small:.3f}/{mid:.3f}/{high:.3f}"

CHECKER_ID = "v4_033_log_rssi_power_detector"
CHECKER: Checker = check_log_rssi_power_detector
