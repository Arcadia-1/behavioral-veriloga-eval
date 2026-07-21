"""Task-specific checker for canonical v4 DUT 248."""
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

def _signal_threshold_edges(
    rows: list[dict[str, float]],
    signal: str,
    *,
    threshold: float = 0.45,
    directions: tuple[str, ...] = ("rising", "falling"),
) -> list[float]:
    times = [row["time"] for row in rows]
    values = [row[signal] for row in rows]
    edges: list[float] = []
    for direction in directions:
        edges.extend(_threshold_crossings(values, times, threshold=threshold, direction=direction))
    return sorted(edges)

def check_v3_bipolar_dff_sample(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin_d", "vclk", "vout_q", "vout_qbar"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing bipolar dff sample signals"
    edges = _signal_threshold_edges(rows, "vclk", threshold=0.45, directions=("rising",))
    if len(edges) < 3:
        return False, f"too_few_bipolar_dff_edges={len(edges)}"
    max_err = 0.0
    checked = 0
    hold_checks = 0
    high = 0
    low = 0
    for edge_index, edge_t in enumerate(edges):
        vin = sample_signal_at(rows, "vin_d", edge_t)
        q = sample_signal_at(rows, "vout_q", edge_t + 0.10e-9)
        qb = sample_signal_at(rows, "vout_qbar", edge_t + 0.10e-9)
        if vin is None or q is None or qb is None:
            return False, f"missing_bipolar_dff_sample_at={edge_t * 1e9:.3f}ns"
        is_high = vin > 0.0
        if is_high:
            high += 1
        else:
            low += 1
        want_q = 1.0 if is_high else -1.0
        want_qb = -want_q
        max_err = max(max_err, abs(q - want_q), abs(qb - want_qb))
        checked += 1
        if edge_index + 1 < len(edges):
            hold_t = edges[edge_index + 1] - 0.08e-9
            held_q = sample_signal_at(rows, "vout_q", hold_t)
            held_qb = sample_signal_at(rows, "vout_qbar", hold_t)
            if held_q is None or held_qb is None:
                return False, f"missing_bipolar_dff_hold_at={hold_t * 1e9:.3f}ns"
            if abs(held_q - want_q) > 0.10 or abs(held_qb - want_qb) > 0.10:
                return False, (
                    f"bipolar_dff_hold@{hold_t * 1e9:.3f}ns="
                    f"{held_q:.4f}/{held_qb:.4f} expected={want_q:.4f}/{want_qb:.4f}"
                )
            hold_checks += 1
    if checked < 3 or high == 0 or low == 0:
        return False, f"insufficient_bipolar_dff_coverage checked={checked} high={high} low={low}"
    return max_err <= 0.10, (
        f"edges={len(edges)} high={high} low={low} "
        f"hold_checks={hold_checks} max_err={max_err:.4f}"
    )

CHECKER_ID = "v4_248_bipolar_dff_sample"
CHECKER: Checker = check_v3_bipolar_dff_sample
