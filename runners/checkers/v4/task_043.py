"""Task-specific checker for canonical v4 DUT 043."""
from __future__ import annotations

from checkers.api import Checker
def mean_in_window(rows: list[dict[str, float]], key: str, start: float, stop: float) -> float | None:
    values = [r[key] for r in rows if start <= r["time"] <= stop and key in r]
    if not values:
        return None
    return sum(values) / len(values)

def check_release_soft_hysteretic_limiter(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst/vin/out/metric"

    high_limited = mean_in_window(rows, "out", 16.0e-9, 24.0e-9)
    low_limited = mean_in_window(rows, "out", 46.0e-9, 55.0e-9)
    high_memory = mean_in_window(rows, "out", 31.0e-9, 36.0e-9)
    low_memory = mean_in_window(rows, "out", 61.0e-9, 66.0e-9)
    high_metric = mean_in_window(rows, "metric", 16.0e-9, 24.0e-9)
    low_metric = mean_in_window(rows, "metric", 46.0e-9, 55.0e-9)
    high_memory_metric = mean_in_window(rows, "metric", 31.0e-9, 36.0e-9)
    low_memory_metric = mean_in_window(rows, "metric", 61.0e-9, 66.0e-9)
    if None in (
        high_limited,
        low_limited,
        high_memory,
        low_memory,
        high_metric,
        low_metric,
        high_memory_metric,
        low_memory_metric,
    ):
        return False, "soft_limiter_missing_sample_windows"
    assert high_limited is not None
    assert low_limited is not None
    assert high_memory is not None
    assert low_memory is not None
    assert high_metric is not None
    assert low_metric is not None
    assert high_memory_metric is not None
    assert low_memory_metric is not None

    post_rows = [r for r in rows if r["rst"] <= 0.45 and 3e-9 < r["time"] < 70e-9]
    if len(post_rows) < 10:
        return False, f"soft_limiter_too_few_post_reset_rows={len(post_rows)}"
    out_min = min(r["out"] for r in post_rows)
    out_max = max(r["out"] for r in post_rows)
    metric_span = max(r["metric"] for r in post_rows) - min(r["metric"] for r in post_rows)
    if not (-0.02 <= out_min <= out_max <= 0.92):
        return False, f"soft_limiter_out_range=({out_min:.3f},{out_max:.3f})"
    if high_limited > 0.84 or high_limited < 0.70:
        return False, f"soft_limiter_high_compression={high_limited:.3f}"
    if low_limited < 0.08 or low_limited > 0.22:
        return False, f"soft_limiter_low_compression={low_limited:.3f}"
    if high_memory <= low_memory + 0.10:
        return False, f"soft_limiter_hysteresis_not_visible high={high_memory:.3f} low={low_memory:.3f}"
    if high_metric < 0.58 or high_memory_metric < 0.58 or low_metric > 0.32 or low_memory_metric > 0.32:
        return False, (
            "soft_limiter_metric_not_stateful "
            f"high={high_metric:.3f}/{high_memory_metric:.3f} low={low_metric:.3f}/{low_memory_metric:.3f}"
        )
    if metric_span < 0.30:
        return False, f"soft_limiter_metric_span_too_small={metric_span:.3f}"
    return True, (
        "release_soft_hysteretic_limiter "
        f"limited={low_limited:.3f}/{high_limited:.3f} "
        f"memory={low_memory:.3f}/{high_memory:.3f} metric_span={metric_span:.3f}"
    )

CHECKER_ID = "v4_043_soft_hysteretic_limiter"
CHECKER: Checker = check_release_soft_hysteretic_limiter
