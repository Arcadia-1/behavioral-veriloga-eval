"""Task-specific checker for canonical v4 DUT 073."""
from __future__ import annotations

from ..api import Checker
def mean_in_window(rows: list[dict[str, float]], key: str, start: float, stop: float) -> float | None:
    values = [r[key] for r in rows if start <= r["time"] <= stop and key in r]
    if not values:
        return None
    return sum(values) / len(values)

def check_bias_voltage_generator_with_enable_trim(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst/vin/out/metric"

    disabled_early = mean_in_window(rows, "out", 5.0e-9, 10.0e-9)
    low_trim = mean_in_window(rows, "out", 24.0e-9, 30.0e-9)
    high_trim = mean_in_window(rows, "out", 45.0e-9, 52.0e-9)
    disabled_late = mean_in_window(rows, "out", 58.0e-9, 64.0e-9)
    enabled_metric = mean_in_window(rows, "metric", 24.0e-9, 52.0e-9)
    disabled_metric = mean_in_window(rows, "metric", 58.0e-9, 64.0e-9)
    if None in (disabled_early, low_trim, high_trim, disabled_late, enabled_metric, disabled_metric):
        return False, "bias_trim_missing_sample_windows"
    assert disabled_early is not None
    assert low_trim is not None
    assert high_trim is not None
    assert disabled_late is not None
    assert enabled_metric is not None
    assert disabled_metric is not None

    if disabled_early > 0.08 or disabled_late > 0.08:
        return False, (
            f"bias_not_disabled observed=early:{disabled_early:.3f},late:{disabled_late:.3f} "
            "expected<=0.08 window=5-10ns/58-64ns"
        )
    if not (0.30 <= low_trim <= 0.50):
        return False, f"bias_low_trim_wrong observed={low_trim:.3f} expected=0.30..0.50 window=24-30ns"
    if high_trim <= low_trim + 0.14 or high_trim > 0.85:
        return False, (
            f"bias_trim_span_wrong observed=low:{low_trim:.3f},high:{high_trim:.3f} "
            "expected=high>low+0.14,high<=0.85 window=24-52ns"
        )
    if enabled_metric < 0.65 or disabled_metric > 0.15:
        return False, (
            f"bias_metric_wrong observed=enabled:{enabled_metric:.3f},disabled:{disabled_metric:.3f} "
            "expected=enabled>=0.65,disabled<=0.15 window=24-52ns/58-64ns"
        )
    return True, (
        "bias_voltage_generator_with_enable_trim "
        f"disabled={disabled_early:.3f}/{disabled_late:.3f} trim={low_trim:.3f}->{high_trim:.3f}"
    )

CHECKER_ID = "v4_073_bias_voltage_generator_with_enable_trim"
CHECKER: Checker = check_bias_voltage_generator_with_enable_trim
