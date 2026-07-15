"""Task-specific checker for canonical v4 DUT 292."""
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

def check_v3_candidate_bias_supply_bias_validity_gate(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vdd", "vss", "vbias", "en", "pd", "ok", "gated"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing supply bias validity gate signals"
    end_t = rows[-1]["time"]
    sample_t = 0.75e-9
    checked = 0
    max_err = 0.0
    ok_high = ok_low = gated_high = gated_low_while_ok = False
    while sample_t < end_t - 0.2e-9:
        values = {name: sample_signal_at(rows, name, sample_t) for name in required if name != "time"}
        if any(value is None for value in values.values()):
            sample_t += 1.0e-9
            continue
        supply = values["vdd"] - values["vss"]
        vss_abs = abs(values["vss"])
        bias = values["vbias"] - values["vss"]
        ok_expected = 0.9 if (
            0.75 <= supply <= 1.05 and vss_abs <= 0.08 and 0.25 <= bias <= 0.75
        ) else 0.0
        gated_expected = 0.9 if (ok_expected > 0.45 and values["en"] > 0.45 and values["pd"] <= 0.45) else 0.0
        max_err = max(max_err, abs(values["ok"] - ok_expected), abs(values["gated"] - gated_expected))
        ok_high = ok_high or ok_expected > 0.45
        ok_low = ok_low or ok_expected < 0.45
        gated_high = gated_high or gated_expected > 0.45
        gated_low_while_ok = gated_low_while_ok or (ok_expected > 0.45 and gated_expected < 0.45)
        checked += 1
        sample_t += 1.0e-9
    if checked < 8:
        return False, f"insufficient_validity_gate_samples={checked}"
    if not (ok_high and ok_low and gated_high and gated_low_while_ok):
        return False, "insufficient_validity_gate_coverage"
    if max_err > 0.08:
        return False, f"validity_gate_error={max_err:.4f}"
    return True, f"samples={checked} max_err={max_err:.4f}"

CHECKER_ID = "v4_292_supply_bias_validity_gate"
CHECKER: Checker = check_v3_candidate_bias_supply_bias_validity_gate
