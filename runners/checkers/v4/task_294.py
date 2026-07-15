"""Task-specific checker for canonical v4 DUT 294."""
from __future__ import annotations

from ..api import Checker
def _threshold_crossings(
    values: list[float],
    times: list[float],
    *,
    threshold: float = 0.0,
    direction: str,
) -> list[float]:
    edges: list[float] = []
    for idx in range(1, len(values)):
        v0 = values[idx - 1]
        v1 = values[idx]
        if direction == "rising":
            hit = v0 <= threshold < v1
        elif direction == "falling":
            hit = v0 >= threshold > v1
        else:
            raise ValueError(f"unsupported direction={direction!r}")
        if not hit:
            continue
        t0 = times[idx - 1]
        t1 = times[idx]
        if v1 == v0:
            edges.append(t1)
        else:
            alpha = (threshold - v0) / (v1 - v0)
            edges.append(t0 + alpha * (t1 - t0))
    return edges

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

def check_v3_candidate_bias_power_enable_turnon_delay_gate(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "vdd", "vss", "vbias", "en", "pd", "pwr_ok", "drive_en", "delay_mon"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing power enable turn-on delay gate signals"
    times = [row["time"] for row in rows]
    clk_edges = _threshold_crossings([row["clk"] for row in rows], times, threshold=0.45, direction="rising")
    if len(clk_edges) < 8:
        return False, f"too_few_turnon_delay_clk_edges={len(clk_edges)}"
    min_period = min((b - a for a, b in zip(clk_edges, clk_edges[1:])), default=1.0e-9)
    output_delay = min(0.45e-9, 0.45 * min_period)
    valid_count = 0
    checked = 0
    max_err = 0.0
    pwr_ok_high = pwr_ok_low = drive_high = delayed_low = invalid_cleared = False
    for edge_t in clk_edges:
        output_t = edge_t + output_delay
        if output_t >= times[-1] - 0.05e-9:
            continue
        input_values = {
            name: sample_signal_at(rows, name, edge_t + 1.0e-12)
            for name in ("vdd", "vss", "vbias", "en", "pd")
        }
        output_values = {
            name: sample_signal_at(rows, name, output_t)
            for name in ("pwr_ok", "drive_en", "delay_mon")
        }
        if any(value is None for value in input_values.values()) or any(value is None for value in output_values.values()):
            continue
        prior_count = valid_count
        supply = input_values["vdd"] - input_values["vss"]
        bias = input_values["vbias"] - input_values["vss"]
        sampled_valid = (
            0.75 <= supply <= 1.05
            and 0.25 <= bias <= 0.75
            and input_values["en"] > 0.45
            and input_values["pd"] <= 0.45
        )
        if sampled_valid:
            valid_count = min(valid_count + 1, 3)
        else:
            valid_count = 0
        pwr_ok_expected = 0.9 if sampled_valid else 0.0
        drive_expected = 0.9 if valid_count >= 3 else 0.0
        delay_expected = 0.9 * valid_count / 3.0
        max_err = max(
            max_err,
            abs(output_values["pwr_ok"] - pwr_ok_expected),
            abs(output_values["drive_en"] - drive_expected),
            abs(output_values["delay_mon"] - delay_expected),
        )
        pwr_ok_high = pwr_ok_high or pwr_ok_expected > 0.45
        pwr_ok_low = pwr_ok_low or pwr_ok_expected < 0.45
        drive_high = drive_high or drive_expected > 0.45
        delayed_low = delayed_low or (pwr_ok_expected > 0.45 and drive_expected < 0.45)
        invalid_cleared = invalid_cleared or ((not sampled_valid) and prior_count > 0 and valid_count == 0)
        checked += 1
    if checked < 10:
        return False, f"insufficient_turnon_delay_samples={checked}"
    if not (pwr_ok_high and pwr_ok_low and drive_high and delayed_low and invalid_cleared):
        return False, "insufficient_turnon_delay_coverage"
    if max_err > 0.10:
        return False, f"turnon_delay_gate_error={max_err:.4f}"
    return True, f"samples={checked} max_err={max_err:.4f}"

CHECKER_ID = "v4_294_power_enable_turnon_delay_gate"
CHECKER: Checker = check_v3_candidate_bias_power_enable_turnon_delay_gate
