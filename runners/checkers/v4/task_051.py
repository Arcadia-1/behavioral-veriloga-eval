"""Task-specific checker for canonical v4 DUT 051."""
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

def check_v3_499_latched_bus_dac8(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vclk", "vout", *{f"b{i}" for i in range(8)}}
    if not rows or not required.issubset(rows[0]):
        return False, "missing latched bus dac8 signals"
    times = [row["time"] for row in rows]
    edges = _threshold_crossings([row["vclk"] for row in rows], times, threshold=0.45, direction="rising")
    if len(edges) < 4:
        return False, f"too_few_latched_dac_edges={len(edges)}"
    max_err = 0.0
    max_hold_err = 0.0
    checked = 0
    hold_checked = 0
    codes: list[int] = []
    for edge_t in edges:
        if edge_t + 0.18e-9 > times[-1]:
            continue
        code = 0
        for bit in range(8):
            value = sample_signal_at(rows, f"b{bit}", edge_t + 1e-12)
            if value is None:
                return False, f"missing_b{bit}_at_edge={edge_t * 1e9:.3f}ns"
            code += (1 << bit) if value > 0.45 else 0
        expected = code / 255.0
        got = sample_signal_at(rows, "vout", edge_t + 0.18e-9)
        if got is None:
            return False, f"missing_vout_after_edge={edge_t * 1e9:.3f}ns"
        max_err = max(max_err, abs(got - expected))
        checked += 1
        codes.append(code)
        hold_t = edge_t + 1.45e-9
        if hold_t < times[-1]:
            held = sample_signal_at(rows, "vout", hold_t)
            if held is None:
                return False, f"missing_vout_hold={hold_t * 1e9:.3f}ns"
            max_hold_err = max(max_hold_err, abs(held - expected))
            hold_checked += 1
    if checked < 4 or hold_checked < 3:
        return False, f"insufficient_latched_dac_checks=edge{checked}_hold{hold_checked}"
    if len(set(codes)) < 4:
        return False, f"insufficient_latched_dac_code_coverage={codes}"
    if max_err > 0.045:
        return False, f"max_latched_dac_edge_err={max_err:.4f} codes={codes}"
    if max_hold_err > 0.045:
        return False, f"max_latched_dac_hold_err={max_hold_err:.4f} codes={codes}"
    return True, (
        f"edges={checked} hold={hold_checked} codes={codes} "
        f"max_err={max_err:.4f} max_hold_err={max_hold_err:.4f}"
    )

CHECKER_ID = "v4_051_latched_bus_dac8"
CHECKER: Checker = check_v3_499_latched_bus_dac8
