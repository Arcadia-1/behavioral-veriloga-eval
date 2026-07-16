"""Task-specific checker for canonical v4 DUT 302."""
from __future__ import annotations

from ..api import Checker
from ..common.relative_events import (
    event_period,
    period_step_anchor,
    relative_rows,
    rising_edges,
    rows_between,
    trace_bounds,
    weighted_logic_high_fraction,
)

def check_v3_505_fractional_n_divider_accumulator_flow(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "ref_clk", "fb_clk", "dco_clk", "lock", "vctrl_mon"}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing)

    ref_edges = rising_edges(rows, "ref_clk")
    fb_edges = rising_edges(rows, "fb_clk")
    dco_edges = rising_edges(rows, "dco_clk")
    if len(ref_edges) < 12 or len(fb_edges) < 12 or len(dco_edges) < 80:
        return False, f"not_enough_edges ref={len(ref_edges)} fb={len(fb_edges)} dco={len(dco_edges)}"

    _, trace_end, _ = trace_bounds(rows)
    late_rows = relative_rows(rows, 0.75, 0.99)
    late_start = float(late_rows[0]["time"]) if late_rows else trace_end
    late_end = float(late_rows[-1]["time"]) if late_rows else trace_end
    ref_late = [time_s for time_s in ref_edges if late_start <= time_s <= late_end]
    fb_late = [time_s for time_s in fb_edges if late_start <= time_s <= late_end]
    if len(ref_late) < 4 or len(fb_late) < 4:
        return False, f"not_enough_late_edges ref_late={len(ref_late)} fb_late={len(fb_late)}"

    ref_periods = [b - a for a, b in zip(ref_late, ref_late[1:])]
    fb_periods = [b - a for a, b in zip(fb_late, fb_late[1:])]
    ref_period = sum(ref_periods) / len(ref_periods)
    fb_period = sum(fb_periods) / len(fb_periods)
    if ref_period <= 0.0 or fb_period <= 0.0:
        return False, "non_positive_period"
    freq_ratio = ref_period / fb_period

    dco_counts: list[int] = []
    for start_t, stop_t in zip(fb_late, fb_late[1:]):
        dco_counts.append(sum(1 for edge_t in dco_edges if start_t < edge_t <= stop_t))
    if len(dco_counts) < 3:
        return False, f"not_enough_dco_count_windows={len(dco_counts)}"
    avg_dco_per_fb = sum(dco_counts) / len(dco_counts)
    if not (14.0 <= avg_dco_per_fb <= 17.0):
        return False, f"dco_edges_per_fb_period_out_of_range avg={avg_dco_per_fb:.3f} counts={dco_counts}"
    if min(dco_counts) >= 16:
        return False, f"fractional_short_count_not_observed counts={dco_counts}"

    lock_edges = rising_edges(rows, "lock")
    step_anchor = period_step_anchor(rows, "ref_clk")
    if step_anchor is None:
        step_anchor = ref_edges[len(ref_edges) // 3]
    ref_period = event_period(rows, "ref_clk")
    disturb_start = step_anchor + 2.0 * ref_period
    disturb_end = step_anchor + 40.0 * ref_period
    pre_lock_edges = [time_s for time_s in lock_edges if time_s < step_anchor]
    post_lock_edges = [time_s for time_s in lock_edges if time_s >= disturb_end]
    disturb_rows = rows_between(rows, disturb_start, disturb_end)
    disturb_low_frac = 1.0 - weighted_logic_high_fraction(disturb_rows, "lock", 0.45)

    vctrl_vals = [row["vctrl_mon"] for row in rows]
    vctrl_min = min(vctrl_vals)
    vctrl_max = max(vctrl_vals)
    vctrl_span = vctrl_max - vctrl_min
    vctrl_in_range = all(-1e-6 <= value <= 0.95 for value in vctrl_vals)

    ok = (
        bool(pre_lock_edges)
        and disturb_low_frac >= 0.20
        and bool(post_lock_edges)
        and 0.95 <= freq_ratio <= 1.05
        and vctrl_in_range
        and vctrl_span >= 0.01
    )
    diagnostics = {
        "P_USE_REF_CLK_AS_THE_REFERENCE": int(len(ref_edges) < 12),
        "P_GENERATE_A_BEHAVIORAL_DCO_CLOCK_ON": int(len(dco_edges) < 80),
        "P_GENERATE_FB_CLK_BY_TOGGLING_IT": int(len(fb_edges) < 12),
        "P_UPDATE_A_BOUNDED_CONTROL_VOLTAGE_MONITOR": int(not vctrl_in_range),
        "P_DRIVE_LOCK_HIGH_AFTER_STABLE_TRACKING": int(not (pre_lock_edges and post_lock_edges and disturb_low_frac >= 0.20)),
    }
    return ok, (
        f"pre_lock_edges={len(pre_lock_edges)} disturb_lock_low_frac={disturb_low_frac:.3f} "
        f"post_lock_edges={len(post_lock_edges)} late_freq_ratio={freq_ratio:.4f} "
        f"dco_counts={dco_counts[:8]} avg_dco_per_fb={avg_dco_per_fb:.3f} "
        f"vctrl_min={vctrl_min:.3f} vctrl_max={vctrl_max:.3f} vctrl_span={vctrl_span:.3f}; "
        + "; ".join(f"{key} mismatch_count={value}" for key, value in diagnostics.items())
    )

def weighted_logic_high_fraction(rows: list[dict[str, float]], signal: str, threshold: float) -> float:
    if len(rows) < 2:
        return 0.0
    total_dt = rows[-1]["time"] - rows[0]["time"]
    if total_dt <= 0.0:
        return 0.0

    high_dt = 0.0
    for idx in range(1, len(rows)):
        dt = rows[idx]["time"] - rows[idx - 1]["time"]
        if dt <= 0.0:
            continue
        v_mid = 0.5 * (rows[idx - 1][signal] + rows[idx][signal])
        if v_mid > threshold:
            high_dt += dt
    return high_dt / total_dt

CHECKER_ID = "v4_302_fractional_n_divider_accumulator_flow"
CHECKER: Checker = check_v3_505_fractional_n_divider_accumulator_flow
