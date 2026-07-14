"""Task-specific checker for canonical v4 DUT 302."""
from __future__ import annotations

from checkers.api import Checker
def rising_edges(values: list[float], times: list[float], threshold: float = 0.45) -> list[float]:
    edges: list[float] = []
    for i in range(1, len(values)):
        if values[i - 1] < threshold <= values[i]:
            edges.append(times[i])
    return edges

def check_v3_505_fractional_n_divider_accumulator_flow(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "ref_clk", "fb_clk", "dco_clk", "lock", "vctrl_mon"}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing)

    vth = 0.45
    times = [row["time"] for row in rows]
    ref_edges = rising_edges([row["ref_clk"] for row in rows], times, threshold=vth)
    fb_edges = rising_edges([row["fb_clk"] for row in rows], times, threshold=vth)
    dco_edges = rising_edges([row["dco_clk"] for row in rows], times, threshold=vth)
    if len(ref_edges) < 12 or len(fb_edges) < 12 or len(dco_edges) < 80:
        return False, f"not_enough_edges ref={len(ref_edges)} fb={len(fb_edges)} dco={len(dco_edges)}"

    ref_late = [time_s for time_s in ref_edges if 4.5e-6 <= time_s <= 5.9e-6]
    fb_late = [time_s for time_s in fb_edges if 4.5e-6 <= time_s <= 5.9e-6]
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

    lock_edges = rising_edges([row["lock"] for row in rows], times, threshold=vth)
    pre_lock_edges = [time_s for time_s in lock_edges if time_s < 2.0e-6]
    post_lock_edges = [time_s for time_s in lock_edges if 2.2e-6 <= time_s <= 5.9e-6]
    disturb_low_frac = 1.0 - weighted_logic_high_fraction_window(rows, "lock", vth, 2.05e-6, 2.8e-6)

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
    return ok, (
        f"pre_lock_edges={len(pre_lock_edges)} disturb_lock_low_frac={disturb_low_frac:.3f} "
        f"post_lock_edges={len(post_lock_edges)} late_freq_ratio={freq_ratio:.4f} "
        f"dco_counts={dco_counts[:8]} avg_dco_per_fb={avg_dco_per_fb:.3f} "
        f"vctrl_min={vctrl_min:.3f} vctrl_max={vctrl_max:.3f} vctrl_span={vctrl_span:.3f}"
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

def time_window(rows: list[dict[str, float]], t_start: float, t_end: float) -> list[dict[str, float]]:
    return [r for r in rows if t_start <= r["time"] <= t_end]

def weighted_logic_high_fraction_window(
    rows: list[dict[str, float]],
    signal: str,
    threshold: float,
    t_start: float,
    t_end: float,
) -> float:
    return weighted_logic_high_fraction(time_window(rows, t_start, t_end), signal, threshold)

CHECKER_ID = "v4_302_fractional_n_divider_accumulator_flow"
CHECKER: Checker = check_v3_505_fractional_n_divider_accumulator_flow
