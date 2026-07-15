"""Task-specific checker for canonical v4 DUT 042."""
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

def check_release_vin_sampled_droop_hold(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "sample", "rst", "vin", "vout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/sample/rst/vin/vout"

    times = [r["time"] for r in rows]
    sample_edges = _threshold_crossings([r["sample"] for r in rows], times, threshold=0.45, direction="rising")
    if len(sample_edges) < 3:
        return False, f"too_few_sample_edges={len(sample_edges)}"

    expected: list[float] = []
    observed: list[float] = []
    errors: list[float] = []
    for edge_t in sample_edges[:3]:
        want = sample_signal_at(rows, "vin", edge_t + 0.05e-9)
        got = sample_signal_at(rows, "vout", edge_t + 1.20e-9)
        if want is None or got is None:
            return False, f"missing_sample_window_at={edge_t:.3e}"
        expected.append(want)
        observed.append(got)
        errors.append(abs(got - want))

    max_err = max(errors)
    expected_span = max(expected) - min(expected)
    observed_span = max(observed) - min(observed)
    sample_match = max_err <= 0.045 and expected_span >= 0.35 and observed_span >= 0.30

    # Use the high second sample as the droop window; reset begins well after it.
    second_edge = sample_edges[1]
    droop_start_t = second_edge + 2.0e-9
    reset_edges = _threshold_crossings([r["rst"] for r in rows], times, threshold=0.45, direction="rising")
    droop_end_t = (reset_edges[0] - 2.0e-9) if reset_edges else (second_edge + 35.0e-9)
    droop_values = [r["vout"] for r in rows if droop_start_t <= r["time"] <= droop_end_t]
    if len(droop_values) < 8:
        return False, f"insufficient_droop_window_samples={len(droop_values)}"
    droop = droop_values[0] - droop_values[-1]
    upward_steps = sum(1 for a, b in zip(droop_values[:-1], droop_values[1:]) if b - a > 0.004)
    droop_ok = 0.04 <= droop <= 0.45 and upward_steps <= max(1, len(droop_values) // 10)

    reset_t = reset_edges[0] if reset_edges else 125.0e-9
    reset_sample = sample_signal_at(rows, "vout", reset_t + 8.0e-9)
    reset_clear = reset_sample is not None and reset_sample < 0.05

    ok = sample_match and droop_ok and reset_clear
    exp_text = ",".join(f"{value:.3f}" for value in expected)
    obs_text = ",".join(f"{value:.3f}" for value in observed)
    return ok, (
        f"vin_samples={exp_text} held_samples={obs_text} "
        f"max_sample_err={max_err:.3f} expected_span={expected_span:.3f} "
        f"observed_span={observed_span:.3f} droop={droop:.3f} "
        f"upward_steps={upward_steps} reset_clear={reset_clear}"
    )

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

CHECKER_ID = "v4_042_sample_and_hold_with_droop_leakage"
CHECKER: Checker = check_release_vin_sampled_droop_hold
