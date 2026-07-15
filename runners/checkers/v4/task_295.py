"""Task-specific checker for canonical v4 DUT 295."""
from __future__ import annotations

from ..api import Checker
def sample_signal_at(rows: list[dict[str, float]], signal: str, time_s: float) -> float | None:
    if not rows or "time" not in rows[0] or signal not in rows[0]:
        return None
    first_time = rows[0]["time"]
    last_time = rows[-1].get("time")
    if last_time is None or time_s < first_time or time_s > last_time:
        return None
    if time_s == first_time:
        return rows[0].get(signal)
    for idx in range(1, len(rows)):
        prev = rows[idx - 1]
        cur = rows[idx]
        t0 = prev.get("time")
        t1 = cur.get("time")
        if t0 is None or t1 is None:
            continue
        if t0 <= time_s <= t1:
            v0 = prev.get(signal)
            v1 = cur.get(signal)
            if v0 is None or v1 is None:
                return None
            if t1 == t0:
                return v1
            alpha = (time_s - t0) / (t1 - t0)
            return v0 + alpha * (v1 - v0)
    return None

def check_v3_candidate_bias_power_mode_supply_current_metric(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vdd", "vss", "en", "pd", "mode", "load", "isup_metric"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing power mode supply current metric signals"
    end_t = rows[-1]["time"]
    sample_t = 0.75e-9
    checked = 0
    max_err = 0.0
    saw_active_low = saw_active_high = saw_powerdown = saw_supply_scaled = saw_load_high = False
    while sample_t < end_t - 0.2e-9:
        values = {name: sample_signal_at(rows, name, sample_t) for name in required if name != "time"}
        if any(value is None for value in values.values()):
            sample_t += 1.0e-9
            continue
        supply_scale = (values["vdd"] - values["vss"]) / 0.9
        supply_scale = min(1.5, max(0.0, supply_scale))
        load_norm = (values["load"] - values["vss"]) / 0.9
        load_norm = min(1.0, max(0.0, load_norm))
        active = values["en"] > 0.45 and values["pd"] <= 0.45
        if active:
            base = 0.14 if values["mode"] > 0.45 else 0.08
            expected = (base + 0.20 * load_norm) * supply_scale
            saw_active_high = saw_active_high or values["mode"] > 0.45
            saw_active_low = saw_active_low or values["mode"] <= 0.45
            saw_load_high = saw_load_high or load_norm > 0.7
        else:
            expected = 0.01 * supply_scale
            saw_powerdown = True
        saw_supply_scaled = saw_supply_scaled or abs(supply_scale - 1.0) > 0.15
        max_err = max(max_err, abs(values["isup_metric"] - expected))
        checked += 1
        sample_t += 1.0e-9
    if checked < 8:
        return False, f"insufficient_supply_metric_samples={checked}"
    if not (saw_active_low and saw_active_high and saw_powerdown and saw_supply_scaled and saw_load_high):
        return False, "insufficient_supply_metric_coverage"
    if max_err > 0.035:
        return False, f"supply_metric_error={max_err:.4f}"
    return True, f"samples={checked} max_err={max_err:.4f}"

CHECKER_ID = "v4_295_power_mode_supply_current_metric"
CHECKER: Checker = check_v3_candidate_bias_power_mode_supply_current_metric
