"""Task-specific checker for canonical v4 DUT 035."""
from __future__ import annotations

from checkers.api import Checker
def mean_in_window(rows: list[dict[str, float]], key: str, start: float, stop: float) -> float | None:
    values = [r[key] for r in rows if start <= r["time"] <= stop and key in r]
    if not values:
        return None
    return sum(values) / len(values)

def check_pa_compression_macro(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst/vin/out/metric"

    small_vin = mean_in_window(rows, "vin", 12.0e-9, 22.0e-9)
    small_out = mean_in_window(rows, "out", 12.0e-9, 22.0e-9)
    high_out = mean_in_window(rows, "out", 32.0e-9, 42.0e-9)
    low_out = mean_in_window(rows, "out", 54.0e-9, 62.0e-9)
    limit_metric = mean_in_window(rows, "metric", 32.0e-9, 62.0e-9)
    if None in (small_vin, small_out, high_out, low_out, limit_metric):
        return False, "pa_missing_sample_windows"
    assert small_vin is not None
    assert small_out is not None
    assert high_out is not None
    assert low_out is not None
    assert limit_metric is not None

    if small_out <= small_vin + 0.07:
        return False, f"pa_gain_missing vin={small_vin:.3f} out={small_out:.3f}"
    if not (0.78 <= high_out <= 0.89):
        return False, f"pa_high_compression_wrong={high_out:.3f}"
    if not (0.02 <= low_out <= 0.14):
        return False, f"pa_low_compression_wrong={low_out:.3f}"
    if limit_metric < 0.55:
        return False, f"pa_limit_metric_low={limit_metric:.3f}"
    return True, f"pa_compression_macro small={small_out:.3f} limits={low_out:.3f}/{high_out:.3f}"

CHECKER_ID = "v4_035_pa_compression"
CHECKER: Checker = check_pa_compression_macro
