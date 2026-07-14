"""Task-specific checker for canonical v4 DUT 297."""
from __future__ import annotations

from checkers.api import Checker
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

def check_v3_candidate_bias_rail_ramp_rate_startup_monitor(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "vdd", "vss", "en", "rail_ok", "ramp_ok", "startup_ready", "slew_metric"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing rail ramp rate startup monitor signals"
    times = [row["time"] for row in rows]
    clk_edges = _threshold_crossings([row["clk"] for row in rows], times, threshold=0.45, direction="rising")
    if len(clk_edges) < 10:
        return False, f"too_few_rail_startup_clk_edges={len(clk_edges)}"
    min_period = min((b - a for a, b in zip(clk_edges, clk_edges[1:])), default=1.0e-9)
    output_delay = min(0.45e-9, 0.45 * min_period)
    initial_vdd = sample_signal_at(rows, "vdd", times[0])
    initial_vss = sample_signal_at(rows, "vss", times[0])
    if initial_vdd is None or initial_vss is None:
        return False, "missing_initial_supply"
    previous_supply = initial_vdd - initial_vss
    settled_count = 0
    checked = 0
    max_err = 0.0
    rail_errors = ramp_errors = ready_errors = metric_errors = 0
    rail_high = rail_low = ramp_high = ramp_low = ready_high = delayed_low = False
    settled_clear = high_fault_seen = enable_clear_seen = metric_nonzero = False
    for edge_t in clk_edges:
        output_t = edge_t + output_delay
        if output_t >= times[-1] - 0.05e-9:
            continue
        input_values = {
            name: sample_signal_at(rows, name, edge_t + 1.0e-12)
            for name in ("vdd", "vss", "en")
        }
        output_values = {
            name: sample_signal_at(rows, name, output_t)
            for name in ("rail_ok", "ramp_ok", "startup_ready", "slew_metric")
        }
        if any(value is None for value in input_values.values()) or any(value is None for value in output_values.values()):
            continue
        prior_count = settled_count
        supply = input_values["vdd"] - input_values["vss"]
        delta_v = supply - previous_supply
        delta_abs = abs(delta_v)
        enabled = input_values["en"] > 0.45
        rail_valid = enabled and 0.72 <= supply <= 1.08
        if not enabled:
            ramp_valid = False
        elif supply < 0.86:
            ramp_valid = 0.025 <= delta_v <= 0.20
        else:
            ramp_valid = delta_abs <= 0.030
        if rail_valid and ramp_valid and supply >= 0.86:
            settled_count = min(settled_count + 1, 3)
        else:
            settled_count = 0
        rail_expected = 0.9 if rail_valid else 0.0
        ramp_expected = 0.9 if ramp_valid else 0.0
        ready_expected = 0.9 if settled_count >= 3 else 0.0
        metric_expected = min(1.0, max(0.0, delta_abs / 0.20)) * 0.9
        rail_err = abs(output_values["rail_ok"] - rail_expected)
        ramp_err = abs(output_values["ramp_ok"] - ramp_expected)
        ready_err = abs(output_values["startup_ready"] - ready_expected)
        metric_err = abs(output_values["slew_metric"] - metric_expected)
        max_err = max(max_err, rail_err, ramp_err, ready_err, metric_err)
        rail_errors += int(rail_err > 0.10)
        ramp_errors += int(ramp_err > 0.10)
        ready_errors += int(ready_err > 0.10)
        metric_errors += int(metric_err > 0.10)
        rail_high = rail_high or rail_expected > 0.45
        rail_low = rail_low or rail_expected < 0.45
        ramp_high = ramp_high or ramp_expected > 0.45
        ramp_low = ramp_low or ramp_expected < 0.45
        ready_high = ready_high or ready_expected > 0.45
        delayed_low = delayed_low or (rail_expected > 0.45 and ramp_expected > 0.45 and ready_expected < 0.45)
        settled_clear = settled_clear or (prior_count > 0 and settled_count == 0 and ready_expected < 0.45)
        high_fault_seen = high_fault_seen or (enabled and supply > 1.08)
        enable_clear_seen = enable_clear_seen or (not enabled)
        metric_nonzero = metric_nonzero or metric_expected > 0.25
        previous_supply = supply
        checked += 1
    if checked < 10:
        return False, f"insufficient_rail_startup_samples={checked}"
    if not (
        rail_high
        and rail_low
        and ramp_high
        and ramp_low
        and ready_high
        and delayed_low
        and settled_clear
        and high_fault_seen
        and enable_clear_seen
        and metric_nonzero
    ):
        return False, "insufficient_rail_startup_coverage"
    ok = max_err <= 0.10
    detail = f"samples={checked} max_err={max_err:.4f}"
    if not ok:
        detail = f"rail_startup_error={max_err:.4f}"
    return ok, (
        f"{detail}; P_RAIL_OK_ENFORCES_ENABLE_AND_SUPPLY_WINDOW mismatch_count={rail_errors}; "
        f"P_RAMP_OK_QUALIFIES_STARTUP_AND_SETTLING_SLEW mismatch_count={ramp_errors}; "
        f"P_STARTUP_READY_REQUIRES_CONSECUTIVE_SETTLED_SAMPLES mismatch_count={ready_errors}; "
        f"P_SLEW_METRIC_REPORTS_BOUNDED_DELTA mismatch_count={metric_errors}"
    )

CHECKER_ID = "v4_297_rail_ramp_rate_startup_monitor"
CHECKER: Checker = check_v3_candidate_bias_rail_ramp_rate_startup_monitor
