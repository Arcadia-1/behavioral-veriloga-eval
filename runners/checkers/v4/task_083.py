"""Task-specific checker for canonical v4 DUT 083."""
from __future__ import annotations

from checkers.api import Checker
def mean_in_window(rows: list[dict[str, float]], key: str, start: float, stop: float) -> float | None:
    values = [r[key] for r in rows if start <= r["time"] <= stop and key in r]
    if not values:
        return None
    return sum(values) / len(values)

def check_release_amplifier_filter_chain(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {
        "time",
        "clk",
        "rst",
        "vin",
        "out",
        "metric",
        "preamp_mon",
        "filt1_mon",
        "filt2_mon",
        "settle_metric",
    }
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, f"missing_columns={','.join(missing)}"

    early_high_out = mean_in_window(rows, "out", 12.5e-9, 15.0e-9)
    late_high_out = mean_in_window(rows, "out", 24.0e-9, 28.0e-9)
    early_high_metric = mean_in_window(rows, "metric", 12.5e-9, 15.0e-9)
    late_high_metric = mean_in_window(rows, "metric", 24.0e-9, 28.0e-9)
    mid_metric = mean_in_window(rows, "metric", 33.0e-9, 36.0e-9)
    low_metric = mean_in_window(rows, "metric", 46.0e-9, 55.0e-9)
    early_high_preamp = mean_in_window(rows, "preamp_mon", 12.5e-9, 15.0e-9)
    late_high_preamp = mean_in_window(rows, "preamp_mon", 24.0e-9, 28.0e-9)
    low_preamp = mean_in_window(rows, "preamp_mon", 46.0e-9, 55.0e-9)
    early_high_filt1 = mean_in_window(rows, "filt1_mon", 12.5e-9, 15.0e-9)
    late_high_filt1 = mean_in_window(rows, "filt1_mon", 24.0e-9, 28.0e-9)
    early_high_filt2 = mean_in_window(rows, "filt2_mon", 12.5e-9, 15.0e-9)
    late_high_filt2 = mean_in_window(rows, "filt2_mon", 24.0e-9, 28.0e-9)
    low_filt2 = mean_in_window(rows, "filt2_mon", 54.0e-9, 58.0e-9)
    settle_low = mean_in_window(rows, "settle_metric", 12.5e-9, 15.0e-9)
    settle_high = mean_in_window(rows, "settle_metric", 24.0e-9, 28.0e-9)
    low_out = mean_in_window(rows, "out", 54.0e-9, 58.0e-9)
    if None in (
        early_high_out,
        late_high_out,
        early_high_metric,
        late_high_metric,
        mid_metric,
        low_metric,
        early_high_preamp,
        late_high_preamp,
        low_preamp,
        early_high_filt1,
        late_high_filt1,
        early_high_filt2,
        late_high_filt2,
        low_filt2,
        settle_low,
        settle_high,
        low_out,
    ):
        return False, "amp_filter_missing_sample_windows"
    assert early_high_out is not None
    assert late_high_out is not None
    assert early_high_metric is not None
    assert late_high_metric is not None
    assert mid_metric is not None
    assert low_metric is not None
    assert early_high_preamp is not None
    assert late_high_preamp is not None
    assert low_preamp is not None
    assert early_high_filt1 is not None
    assert late_high_filt1 is not None
    assert early_high_filt2 is not None
    assert late_high_filt2 is not None
    assert low_filt2 is not None
    assert settle_low is not None
    assert settle_high is not None
    assert low_out is not None

    post_rows = [r for r in rows if r["rst"] <= 0.45 and 3e-9 < r["time"] < 70e-9]
    if len(post_rows) < 10:
        return False, f"amp_filter_too_few_post_reset_rows={len(post_rows)}"
    out_vals = [r["out"] for r in post_rows]
    metric_vals = [r["metric"] for r in post_rows]
    preamp_vals = [r["preamp_mon"] for r in post_rows]
    filt1_vals = [r["filt1_mon"] for r in post_rows]
    filt2_vals = [r["filt2_mon"] for r in post_rows]
    settle_vals = [r["settle_metric"] for r in post_rows]
    if not (-0.02 <= min(out_vals) <= max(out_vals) <= 0.92):
        return False, f"amp_filter_out_range=({min(out_vals):.3f},{max(out_vals):.3f})"
    if not (-0.02 <= min(metric_vals) <= max(metric_vals) <= 0.92):
        return False, f"amp_filter_metric_range=({min(metric_vals):.3f},{max(metric_vals):.3f})"
    if not (-0.02 <= min(preamp_vals) <= max(preamp_vals) <= 0.92):
        return False, f"amp_filter_preamp_range=({min(preamp_vals):.3f},{max(preamp_vals):.3f})"
    if not (-0.02 <= min(filt1_vals) <= max(filt1_vals) <= 0.92):
        return False, f"amp_filter_filt1_range=({min(filt1_vals):.3f},{max(filt1_vals):.3f})"
    if not (-0.02 <= min(filt2_vals) <= max(filt2_vals) <= 0.92):
        return False, f"amp_filter_filt2_range=({min(filt2_vals):.3f},{max(filt2_vals):.3f})"
    if early_high_metric < 0.84 or late_high_metric < 0.84 or low_metric > 0.08:
        return False, (
            "amp_filter_metric_not_preamp_target "
            f"early={early_high_metric:.3f} late={late_high_metric:.3f} low={low_metric:.3f}"
        )
    if (
        abs(early_high_metric - early_high_preamp) > 0.04
        or abs(late_high_metric - late_high_preamp) > 0.04
        or abs(low_metric - low_preamp) > 0.04
    ):
        return False, (
            "amp_filter_preamp_monitor_mismatch "
            f"metric/preamp early={early_high_metric:.3f}/{early_high_preamp:.3f} "
            f"late={late_high_metric:.3f}/{late_high_preamp:.3f} "
            f"low={low_metric:.3f}/{low_preamp:.3f}"
        )
    if abs(mid_metric - 0.45) > 0.08:
        return False, f"amp_filter_mid_metric_not_common_mode={mid_metric:.3f}"
    if late_high_out <= early_high_out + 0.09:
        return False, f"amp_filter_missing_lagged_settling early={early_high_out:.3f} late={late_high_out:.3f}"
    if early_high_metric - early_high_out < 0.12:
        return False, f"amp_filter_output_not_lagging_metric gap={early_high_metric - early_high_out:.3f}"
    if early_high_filt1 <= early_high_filt2 + 0.05:
        return False, (
            "amp_filter_first_pole_not_leading_second "
            f"f1={early_high_filt1:.3f} f2={early_high_filt2:.3f}"
        )
    if (
        abs(early_high_out - early_high_filt2) > 0.04
        or abs(late_high_out - late_high_filt2) > 0.04
        or abs(low_out - low_filt2) > 0.04
    ):
        return False, (
            "amp_filter_output_not_second_state "
            f"out/f2 early={early_high_out:.3f}/{early_high_filt2:.3f} "
            f"late={late_high_out:.3f}/{late_high_filt2:.3f} "
            f"low={low_out:.3f}/{low_filt2:.3f}"
        )
    if max(settle_vals) < 0.75 or min(settle_vals) > 0.25:
        return False, (
            "amp_filter_settle_metric_not_voltage_coded "
            f"range=({min(settle_vals):.3f},{max(settle_vals):.3f})"
        )
    if settle_low > 0.35 or settle_high < 0.65:
        return False, (
            "amp_filter_settle_status_not_recovering "
            f"early={settle_low:.3f} late={settle_high:.3f}"
        )
    if low_out > 0.35:
        return False, f"amp_filter_output_not_falling low={low_out:.3f}"
    return True, (
        "release_amplifier_filter_chain "
        f"metric_high_low={early_high_metric:.3f}/{low_metric:.3f} "
        f"out_lag={early_high_out:.3f}->{late_high_out:.3f} "
        f"settle={settle_low:.3f}->{settle_high:.3f}"
    )

CHECKER_ID = "v4_083_amplifier_filter_chain"
CHECKER: Checker = check_release_amplifier_filter_chain
