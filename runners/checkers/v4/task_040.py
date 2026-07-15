"""Task-specific checker for canonical v4 DUT 040."""
from __future__ import annotations

from ..api import Checker
def mean_in_window(rows: list[dict[str, float]], key: str, start: float, stop: float) -> float | None:
    values = [r[key] for r in rows if start <= r["time"] <= stop and key in r]
    if not values:
        return None
    return sum(values) / len(values)

def check_ptat_ctat_reference_generator(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst/vin/out/metric"

    cold_ref = mean_in_window(rows, "out", 8.0e-9, 16.0e-9)
    mid_ref = mean_in_window(rows, "out", 26.0e-9, 38.0e-9)
    hot_ref = mean_in_window(rows, "out", 52.0e-9, 72.0e-9)
    cold_ptat = mean_in_window(rows, "metric", 8.0e-9, 16.0e-9)
    hot_ptat = mean_in_window(rows, "metric", 52.0e-9, 72.0e-9)
    if None in (cold_ref, mid_ref, hot_ref, cold_ptat, hot_ptat):
        return False, "ptat_ctat_missing_sample_windows"
    assert cold_ref is not None
    assert mid_ref is not None
    assert hot_ref is not None
    assert cold_ptat is not None
    assert hot_ptat is not None

    ref_span = max(cold_ref, mid_ref, hot_ref) - min(cold_ref, mid_ref, hot_ref)
    if not (0.42 <= cold_ref <= 0.55 and 0.42 <= mid_ref <= 0.55 and 0.42 <= hot_ref <= 0.55):
        return False, f"ptat_ctat_reference_range={cold_ref:.3f}/{mid_ref:.3f}/{hot_ref:.3f}"
    if ref_span > 0.075:
        return False, f"ptat_ctat_reference_not_compensated span={ref_span:.3f}"
    if hot_ptat <= cold_ptat + 0.12:
        return False, f"ptat_metric_not_monotonic cold={cold_ptat:.3f} hot={hot_ptat:.3f}"
    return True, (
        "ptat_ctat_reference_generator "
        f"ref_span={ref_span:.3f} ptat={cold_ptat:.3f}->{hot_ptat:.3f}"
    )

CHECKER_ID = "v4_040_ptat_ctat_reference_generator"
CHECKER: Checker = check_ptat_ctat_reference_generator
