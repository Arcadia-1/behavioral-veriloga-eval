"""Task-specific checker for canonical v4 DUT 296."""
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

def check_v3_candidate_bias_dynamic_supply_level_driver(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "din", "vdd", "vss", "out"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing dynamic supply level driver signals"
    end_t = rows[-1]["time"]
    sample_t = 0.75e-9
    checked = 0
    max_err = 0.0
    saw_local_high = saw_local_low = saw_invalid_supply = saw_vss_offset = False
    while sample_t < end_t - 0.2e-9:
        values = {name: sample_signal_at(rows, name, sample_t) for name in required if name != "time"}
        if any(value is None for value in values.values()):
            sample_t += 1.0e-9
            continue
        supply = values["vdd"] - values["vss"]
        if supply < 0.55:
            expected = values["vss"]
            saw_invalid_supply = True
        else:
            normalized = (values["din"] - values["vss"]) / supply
            expected = values["vss"] + (supply if normalized > 0.5 else 0.0)
            saw_local_high = saw_local_high or expected > values["vss"] + 0.4
            saw_local_low = saw_local_low or expected <= values["vss"] + 0.05
        saw_vss_offset = saw_vss_offset or abs(values["vss"]) > 0.04
        max_err = max(max_err, abs(values["out"] - expected))
        checked += 1
        sample_t += 1.0e-9
    if checked < 6:
        return False, f"insufficient_dynamic_supply_samples={checked}"
    if not (saw_local_high and saw_local_low and saw_invalid_supply and saw_vss_offset):
        return False, "insufficient_dynamic_supply_coverage"
    if max_err > 0.08:
        return False, f"dynamic_supply_driver_error={max_err:.4f}"
    return True, f"samples={checked} max_err={max_err:.4f}"

CHECKER_ID = "v4_296_dynamic_supply_level_driver"
CHECKER: Checker = check_v3_candidate_bias_dynamic_supply_level_driver
