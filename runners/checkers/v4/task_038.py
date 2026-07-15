"""Task-specific checker for canonical v4 DUT 038."""
from __future__ import annotations

from ..api import Checker
def mean_in_window(rows: list[dict[str, float]], key: str, start: float, stop: float) -> float | None:
    values = [r[key] for r in rows if start <= r["time"] <= stop and key in r]
    if not values:
        return None
    return sum(values) / len(values)

def check_programmable_gain_amplifier(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "gain_sel", "vin", "out", "metric"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst/gain_sel/vin/out/metric"

    reset_out = mean_in_window(rows, "out", 0.5e-9, 2.0e-9)
    high_clip_out = mean_in_window(rows, "out", 28.0e-9, 34.0e-9)
    high_clip_metric = mean_in_window(rows, "metric", 28.0e-9, 34.0e-9)
    low_clip_out = mean_in_window(rows, "out", 38.0e-9, 43.0e-9)
    low_clip_metric = mean_in_window(rows, "metric", 38.0e-9, 43.0e-9)
    low_gain_out = mean_in_window(rows, "out", 58.0e-9, 66.0e-9)
    low_gain_vin = mean_in_window(rows, "vin", 58.0e-9, 66.0e-9)
    low_gain_metric = mean_in_window(rows, "metric", 58.0e-9, 66.0e-9)
    late_clip_out = mean_in_window(rows, "out", 76.0e-9, 82.0e-9)
    late_clip_metric = mean_in_window(rows, "metric", 76.0e-9, 82.0e-9)
    if None in (
        reset_out,
        high_clip_out,
        high_clip_metric,
        low_clip_out,
        low_clip_metric,
        low_gain_out,
        low_gain_vin,
        low_gain_metric,
        late_clip_out,
        late_clip_metric,
    ):
        return False, "pga_missing_sample_windows"
    assert reset_out is not None
    assert high_clip_out is not None
    assert high_clip_metric is not None
    assert low_clip_out is not None
    assert low_clip_metric is not None
    assert low_gain_out is not None
    assert low_gain_vin is not None
    assert low_gain_metric is not None
    assert late_clip_out is not None
    assert late_clip_metric is not None

    post_reset_rows = [r for r in rows if r["rst"] <= 0.45 and r["time"] > 3e-9]
    if not post_reset_rows:
        return False, "pga_no_post_reset_rows"
    out_min = min(r["out"] for r in post_reset_rows)
    out_max = max(r["out"] for r in post_reset_rows)
    if not (-0.02 <= out_min <= out_max <= 0.92):
        return False, f"pga_unclamped_range=({out_min:.3f},{out_max:.3f})"
    if abs(reset_out - 0.45) > 0.05:
        return False, f"pga_reset_out={reset_out:.3f}"
    if high_clip_out < 0.84 or late_clip_out < 0.84:
        return False, f"pga_high_gain_not_railed high={high_clip_out:.3f} late={late_clip_out:.3f}"
    if low_clip_out > 0.08:
        return False, f"pga_negative_swing_not_railed low={low_clip_out:.3f}"
    if not (0.48 <= low_gain_out <= 0.75):
        return False, f"pga_low_gain_unclipped_out={low_gain_out:.3f}"
    if abs(low_gain_out - low_gain_vin) < 0.015:
        return False, f"pga_gain_select_passthrough out={low_gain_out:.3f} vin={low_gain_vin:.3f}"
    if high_clip_metric < 0.65 or low_clip_metric < 0.65 or late_clip_metric < 0.65 or low_gain_metric > 0.20:
        return False, (
            "pga_clip_metric_wrong "
            f"high={high_clip_metric:.3f} low={low_clip_metric:.3f} "
            f"late={late_clip_metric:.3f} unclipped={low_gain_metric:.3f}"
        )
    return True, (
        "programmable_gain_amplifier "
        f"out_high_low_unclipped_late={high_clip_out:.3f}/{low_clip_out:.3f}/"
        f"{low_gain_out:.3f}/{late_clip_out:.3f} "
        f"metric={high_clip_metric:.3f}/{low_clip_metric:.3f}/{low_gain_metric:.3f}/{late_clip_metric:.3f}"
    )

CHECKER_ID = "v4_038_programmable_gain_amplifier"
CHECKER: Checker = check_programmable_gain_amplifier
