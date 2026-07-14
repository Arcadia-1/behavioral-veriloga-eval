"""Task-specific checker for canonical v4 DUT 028."""
from __future__ import annotations

from checkers.api import Checker
def mean_in_window(rows: list[dict[str, float]], key: str, start: float, stop: float) -> float | None:
    values = [r[key] for r in rows if start <= r["time"] <= stop and key in r]
    if not values:
        return None
    return sum(values) / len(values)

def check_release_two_pole_filter(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst/vin/out/metric"

    reset_out = mean_in_window(rows, "out", 0.5e-9, 2.0e-9)
    early_high = mean_in_window(rows, "out", 14.0e-9, 16.0e-9)
    late_high = mean_in_window(rows, "out", 24.0e-9, 28.0e-9)
    early_low = mean_in_window(rows, "out", 44.0e-9, 47.0e-9)
    late_low = mean_in_window(rows, "out", 54.0e-9, 58.0e-9)
    metric_high = mean_in_window(rows, "metric", 14.0e-9, 20.0e-9)
    metric_low = mean_in_window(rows, "metric", 44.0e-9, 52.0e-9)
    if None in (reset_out, early_high, late_high, early_low, late_low, metric_high, metric_low):
        return False, "two_pole_missing_sample_windows"
    assert reset_out is not None
    assert early_high is not None
    assert late_high is not None
    assert early_low is not None
    assert late_low is not None
    assert metric_high is not None
    assert metric_low is not None

    post_rows = [r for r in rows if r["rst"] <= 0.45 and 3e-9 < r["time"] < 70e-9]
    if len(post_rows) < 10:
        return False, f"two_pole_too_few_post_reset_rows={len(post_rows)}"
    out_vals = [r["out"] for r in post_rows]
    metric_vals = [r["metric"] for r in post_rows]
    metric_span = max(metric_vals) - min(metric_vals)
    if not (-0.02 <= min(out_vals) <= max(out_vals) <= 0.92):
        return False, f"two_pole_out_range=({min(out_vals):.3f},{max(out_vals):.3f})"
    if abs(reset_out - 0.45) > 0.12:
        return False, f"two_pole_reset_out={reset_out:.3f}"
    if late_high <= early_high + 0.10 or early_high > 0.68:
        return False, f"two_pole_missing_lagged_rise early={early_high:.3f} late={late_high:.3f}"
    if late_low >= early_low - 0.06 or early_low < 0.20:
        return False, f"two_pole_missing_lagged_fall early={early_low:.3f} late={late_low:.3f}"
    if metric_span < 0.09 or metric_high <= 0.50 or metric_low >= 0.40:
        return False, (
            "two_pole_metric_not_state_difference "
            f"span={metric_span:.3f} high={metric_high:.3f} low={metric_low:.3f}"
        )
    return True, (
        "release_two_pole_filter "
        f"rise={early_high:.3f}->{late_high:.3f} "
        f"fall={early_low:.3f}->{late_low:.3f} metric_span={metric_span:.3f}"
    )

CHECKER_ID = "v4_028_higher_order_filter"
CHECKER: Checker = check_release_two_pole_filter
