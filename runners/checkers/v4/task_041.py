"""Task-specific checker for canonical v4 DUT 041."""
from __future__ import annotations

from ..api import Checker
def mean_in_window(rows: list[dict[str, float]], key: str, start: float, stop: float) -> float | None:
    values = [r[key] for r in rows if start <= r["time"] <= stop and key in r]
    if not values:
        return None
    return sum(values) / len(values)

def check_rf_mixer_downconverter_macro(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst/vin/out/metric"

    def mean_selected(start: float, stop: float, key: str, *, clk_high: bool, vin_high: bool) -> float | None:
        total = 0.0
        duration = 0.0

        def interp(a: dict[str, float], b: dict[str, float], t: float, field: str) -> float:
            t0 = a["time"]
            t1 = b["time"]
            if t1 <= t0:
                return a[field]
            frac = max(0.0, min(1.0, (t - t0) / (t1 - t0)))
            return a[field] + frac * (b[field] - a[field])

        for row, nxt in zip(rows, rows[1:]):
            left = max(start, row["time"])
            right = min(stop, nxt["time"])
            if right <= left:
                continue
            mid = 0.5 * (left + right)
            rst_mid = interp(row, nxt, mid, "rst")
            clk_mid = interp(row, nxt, mid, "clk")
            vin_mid = interp(row, nxt, mid, "vin")
            if rst_mid > 0.45:
                continue
            if clk_high and clk_mid <= 0.75:
                continue
            if (not clk_high) and clk_mid >= 0.15:
                continue
            if vin_high and vin_mid <= 0.55:
                continue
            if (not vin_high) and vin_mid >= 0.38:
                continue
            value_left = interp(row, nxt, left, key)
            value_right = interp(row, nxt, right, key)
            total += 0.5 * (value_left + value_right) * (right - left)
            duration += right - left
        if duration <= 0.0:
            return None
        return total / duration

    pos_hi = mean_selected(10.0e-9, 30.0e-9, "out", clk_high=True, vin_high=True)
    pos_lo = mean_selected(10.0e-9, 30.0e-9, "out", clk_high=False, vin_high=True)
    neg_hi = mean_selected(38.0e-9, 54.0e-9, "out", clk_high=True, vin_high=False)
    neg_lo = mean_selected(38.0e-9, 54.0e-9, "out", clk_high=False, vin_high=False)
    active_metric = mean_in_window(rows, "metric", 12.0e-9, 52.0e-9)
    if None in (pos_hi, pos_lo, neg_hi, neg_lo, active_metric):
        return False, "mixer_missing_sample_windows"
    assert pos_hi is not None
    assert pos_lo is not None
    assert neg_hi is not None
    assert neg_lo is not None
    assert active_metric is not None

    if pos_hi <= 0.58 or pos_lo >= 0.34:
        return False, f"mixer_positive_lo_polarity_wrong hi={pos_hi:.3f} lo={pos_lo:.3f}"
    if neg_hi >= 0.34 or neg_lo <= 0.56:
        return False, f"mixer_negative_lo_polarity_wrong hi={neg_hi:.3f} lo={neg_lo:.3f}"
    if active_metric < 0.40:
        return False, f"mixer_active_metric_low={active_metric:.3f}"
    return True, (
        "rf_mixer_downconverter_macro "
        f"pos={pos_hi:.3f}/{pos_lo:.3f} neg={neg_hi:.3f}/{neg_lo:.3f}"
    )

CHECKER_ID = "v4_041_rf_mixer_downconverter_macro"
CHECKER: Checker = check_rf_mixer_downconverter_macro
