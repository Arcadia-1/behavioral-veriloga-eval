"""Task-specific checker for canonical v4 DUT 205."""
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

def _v3_edge_times(
    rows: list[dict[str, float]],
    signal: str,
    *,
    threshold: float,
    direction: int,
) -> list[float]:
    edges: list[float] = []
    for idx in range(1, len(rows)):
        prev = rows[idx - 1]
        cur = rows[idx]
        v0 = prev.get(signal)
        v1 = cur.get(signal)
        t0 = prev.get("time")
        t1 = cur.get("time")
        if v0 is None or v1 is None or t0 is None or t1 is None:
            continue
        crossed = (v0 < threshold <= v1) if direction > 0 else (v0 > threshold >= v1)
        if not crossed:
            continue
        if v1 == v0:
            edges.append(t1)
        else:
            frac = (threshold - v0) / (v1 - v0)
            edges.append(t0 + frac * (t1 - t0))
    return edges

def check_v3_offset_halving_search(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "dcmpp", "vinp", "vinn"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing offset halving search signals"
    falling_edges = _v3_edge_times(rows, "clk", threshold=0.45, direction=-1)
    if len(falling_edges) < 4:
        return False, f"too_few_halving_clock_edges={len(falling_edges)}"
    vin = 0.0
    step = 0.16
    locked = False
    max_err = 0.0
    checked = 0
    decisions: list[int] = []
    for edge in falling_edges:
        if not locked:
            dcmpp = sample_signal_at(rows, "dcmpp", edge)
            if dcmpp is None:
                return False, f"missing_dcmpp_at={edge * 1e9:.3f}ns"
            decision_high = dcmpp > 0.45
            decisions.append(1 if decision_high else 0)
            vin += -step if decision_high else step
            vin = max(-0.12, min(0.12, vin))
            if step <= 0.02:
                locked = True
            else:
                step *= 0.5
                if step < 0.02:
                    locked = True
        sample_t = edge + 0.25e-9
        if sample_t > rows[-1]["time"]:
            continue
        expected_vinp = 0.45 + 0.5 * vin
        expected_vinn = 0.45 - 0.5 * vin
        vinp = sample_signal_at(rows, "vinp", sample_t)
        vinn = sample_signal_at(rows, "vinn", sample_t)
        if vinp is None or vinn is None:
            return False, f"missing_halving_output_at={sample_t * 1e9:.3f}ns"
        max_err = max(max_err, abs(vinp - expected_vinp), abs(vinn - expected_vinn))
        checked += 1
    if checked < 4:
        return False, f"too_few_halving_output_checks={checked}"
    if set(decisions) != {0, 1}:
        return False, f"insufficient_halving_decision_coverage={decisions}"
    return max_err <= 0.015, f"checked={checked} decisions={decisions} max_error={max_err:.5f}"

CHECKER_ID = "v4_205_offset_halving_search"
CHECKER: Checker = check_v3_offset_halving_search
