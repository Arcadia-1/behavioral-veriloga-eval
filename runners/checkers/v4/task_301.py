"""Task-specific checker for canonical v4 DUT 301."""
from __future__ import annotations

from ..api import Checker
def rising_edges(values: list[float], times: list[float], threshold: float = 0.45) -> list[float]:
    edges: list[float] = []
    for i in range(1, len(values)):
        if values[i - 1] < threshold <= values[i]:
            edges.append(times[i])
    return edges

def check_v3_504_charge_pump_pfd_state_machine(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "ref", "fb", "vctrl", "metric"}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing)
    t_end = rows[-1]["time"]
    if t_end < 600e-9:
        return False, f"trace_too_short={t_end * 1e9:g}ns"

    vth = 0.45
    times = [row["time"] for row in rows]
    ref_edges = rising_edges([row["ref"] for row in rows], times, threshold=vth)
    fb_edges = rising_edges([row["fb"] for row in rows], times, threshold=vth)
    if len(ref_edges) < 3 or len(fb_edges) < 3:
        return False, f"too_few_ref_fb_edges ref={len(ref_edges)} fb={len(fb_edges)}"

    deltas: list[float] = []
    for ref_edge in ref_edges:
        nearest_fb = min(fb_edges, key=lambda fb_edge: abs(fb_edge - ref_edge))
        deltas.append(nearest_fb - ref_edge)
    signed_delta = sorted(deltas)[len(deltas) // 2]
    if abs(signed_delta) < 2e-9:
        return False, f"ambiguous_lead_lag_delta={signed_delta * 1e9:.3f}ns"
    ref_leads = signed_delta > 0.0

    vctrl_min = 0.05
    vctrl_max = 0.85
    metric_lo = 0.1
    metric_hi = 0.8
    vctrl_init = 0.45

    def _window_mean(lo_frac: float, hi_frac: float, key: str) -> float:
        lo_t = lo_frac * t_end
        hi_t = hi_frac * t_end
        vals = [row[key] for row in rows if lo_t <= row["time"] <= hi_t]
        return sum(vals) / len(vals) if vals else 0.0

    late_vctrl = _window_mean(0.55, 0.95, "vctrl")
    if ref_leads:
        if late_vctrl < vctrl_max - 0.06:
            return False, f"vctrl_did_not_reach_top_rail late={late_vctrl:.4f}"
    else:
        if late_vctrl > vctrl_min + 0.06:
            return False, f"vctrl_did_not_reach_bottom_rail late={late_vctrl:.4f}"

    vctrl_vals = [row["vctrl"] for row in rows]
    vmin_obs = min(vctrl_vals)
    vmax_obs = max(vctrl_vals)
    if ref_leads and vmax_obs < vctrl_init + 0.10:
        return False, f"vctrl_never_moved_up max={vmax_obs:.4f}"
    if not ref_leads and vmin_obs > vctrl_init - 0.10:
        return False, f"vctrl_never_moved_down min={vmin_obs:.4f}"
    if vmin_obs < vctrl_min - 0.02 or vmax_obs > vctrl_max + 0.02:
        return False, f"vctrl_out_of_clamp min={vmin_obs:.4f} max={vmax_obs:.4f}"

    late_metric_rows = [row for row in rows if 0.55 * t_end <= row["time"] <= 0.95 * t_end]
    if not late_metric_rows:
        return False, "no_late_metric_samples"
    hi_count = sum(1 for row in late_metric_rows if abs(row["metric"] - metric_hi) < 0.12)
    lo_count = sum(1 for row in late_metric_rows if abs(row["metric"] - metric_lo) < 0.12)
    hi_frac = hi_count / len(late_metric_rows)
    lo_frac = lo_count / len(late_metric_rows)
    if ref_leads:
        if hi_frac < 0.02:
            return False, f"metric_no_positive_pulses hi_frac={hi_frac:.3f}"
        if lo_frac > 0.02:
            return False, f"metric_negative_pulses_present lo_frac={lo_frac:.3f}"
    else:
        if lo_frac < 0.02:
            return False, f"metric_no_negative_pulses lo_frac={lo_frac:.3f}"
        if hi_frac > 0.02:
            return False, f"metric_positive_pulses_present hi_frac={hi_frac:.3f}"
    direction = "ref_leads" if ref_leads else "fb_leads"
    return True, (
        f"{direction} delta_ns={signed_delta * 1e9:.3f} late_vctrl={late_vctrl:.4f} "
        f"vctrl_range=[{vmin_obs:.4f},{vmax_obs:.4f}] "
        f"metric_hi_frac={hi_frac:.3f} metric_lo_frac={lo_frac:.3f}"
    )

CHECKER_ID = "v4_301_charge_pump_pfd_state_machine"
CHECKER: Checker = check_v3_504_charge_pump_pfd_state_machine
