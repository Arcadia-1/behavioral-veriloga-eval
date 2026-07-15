"""Task-specific checker for canonical v4 DUT 273."""
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

def _v3_values_at(
    rows: list[dict[str, float]],
    names: tuple[str, ...],
    time_s: float,
) -> dict[str, float] | None:
    values = {name: sample_signal_at(rows, name, time_s) for name in names}
    if any(value is None for value in values.values()):
        return None
    return {name: float(value) for name, value in values.items() if value is not None}

def check_v3_377_adaptive_threshold_tracker(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "adapt", "trip", "threshold_mon", "margin_metric"}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing)
    times = [row["time"] for row in rows]
    clk_edges = _threshold_crossings([row["clk"] for row in rows], times, threshold=0.45, direction="rising")
    if len(clk_edges) < 8:
        return False, f"too_few_threshold_tracker_edges={len(clk_edges)}"
    min_period = min((b - a for a, b in zip(clk_edges, clk_edges[1:])), default=1.0e-9)
    output_delay = min(0.42e-9, 0.42 * min_period)
    threshold_q = 0.45
    checked = 0
    max_err = 0.0
    base_errors = adaptation_errors = 0
    saw_reset = saw_adapt = saw_hold = saw_trip_high = saw_trip_low = saw_clip_high = saw_margin = False
    for edge_t in clk_edges:
        output_t = edge_t + output_delay
        if output_t >= times[-1] - 0.05e-9:
            continue
        inputs = _v3_values_at(rows, ("rst", "vin", "adapt"), edge_t + 1.0e-12)
        outputs = _v3_values_at(rows, ("trip", "threshold_mon", "margin_metric"), output_t)
        if inputs is None or outputs is None:
            continue
        if inputs["rst"] > 0.45:
            threshold_q = 0.45
            trip_expected = 0.0
            margin_expected = 0.0
            saw_reset = True
        else:
            old_threshold = threshold_q
            trip_expected = 0.9 if inputs["vin"] > old_threshold else 0.0
            margin_expected = 0.9 * min(1.0, max(0.0, abs(inputs["vin"] - old_threshold) / 0.45))
            if inputs["adapt"] > 0.45:
                threshold_q = min(0.70, max(0.25, 0.75 * old_threshold + 0.25 * inputs["vin"]))
                saw_adapt = True
            else:
                saw_hold = True
        threshold_expected = threshold_q
        trip_err = abs(outputs["trip"] - trip_expected)
        threshold_err = abs(outputs["threshold_mon"] - threshold_expected)
        margin_err = abs(outputs["margin_metric"] - margin_expected)
        max_err = max(max_err, trip_err, threshold_err, margin_err)
        if inputs["rst"] > 0.45:
            base_errors += sum(err > 0.10 for err in (trip_err, threshold_err, margin_err))
        else:
            base_errors += int(trip_err > 0.10) + int(margin_err > 0.10)
            adaptation_errors += int(threshold_err > 0.10)
        saw_trip_high = saw_trip_high or trip_expected > 0.45
        saw_trip_low = saw_trip_low or trip_expected < 0.45
        saw_clip_high = saw_clip_high or abs(threshold_expected - 0.70) < 0.015
        saw_margin = saw_margin or margin_expected > 0.35
        checked += 1
    if checked < 8:
        return False, f"insufficient_threshold_tracker_samples={checked}"
    if not (saw_reset and saw_adapt and saw_hold and saw_trip_high and saw_trip_low and saw_clip_high and saw_margin):
        return False, "insufficient_threshold_tracker_coverage"
    ok = max_err <= 0.10
    detail = f"samples={checked} max_err={max_err:.4f}"
    if not ok:
        detail = f"adaptive_threshold_error={max_err:.4f}"
    return ok, (
        f"{detail}; P_INITIALIZE_THE_STORED_THRESHOLD_TO_THRESHOLD mismatch_count={base_errors}; "
        f"P_WHEN_ADAPT_VTH_UPDATE_THE_STORED mismatch_count={adaptation_errors}"
    )

CHECKER_ID = "v4_273_adaptive_threshold_tracker"
CHECKER: Checker = check_v3_377_adaptive_threshold_tracker
