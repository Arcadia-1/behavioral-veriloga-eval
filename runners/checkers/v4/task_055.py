"""Task-specific checker for canonical v4 DUT 055."""
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

def check_v3_496_first_order_sigma_delta_modulator(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "vclk", "bitout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing sigma-delta modulator signals"
    times = [row["time"] for row in rows]
    edges = _threshold_crossings([row["vclk"] for row in rows], times, threshold=0.45, direction="rising")
    if len(edges) < 20:
        return False, f"too_few_clock_edges={len(edges)}"
    acc = 0.0
    bit_state = 0
    mismatches: list[str] = []
    low_bits = 0
    low_total = 0
    high_bits = 0
    high_total = 0
    for edge_t in edges:
        vin = sample_signal_at(rows, "vin", edge_t + 1e-12)
        observed = sample_signal_at(rows, "bitout", edge_t + 0.10e-9)
        if vin is None or observed is None:
            continue
        acc = acc + vin - bit_state
        bit_state = 1 if acc >= 0.0 else 0
        observed_bit = 1 if observed > 0.45 else 0
        if observed_bit != bit_state:
            mismatches.append(
                f"edge@{edge_t * 1e9:.3f}ns bit={observed_bit} expected={bit_state} vin={vin:.3f}"
            )
        if vin < 0.35:
            low_total += 1
            low_bits += observed_bit
        elif vin > 0.55:
            high_total += 1
            high_bits += observed_bit
    if low_total < 8 or high_total < 8:
        return False, f"insufficient_density_windows=low{low_total}_high{high_total}"
    low_density = low_bits / low_total
    high_density = high_bits / high_total
    if mismatches:
        return False, " ".join(mismatches[:6])
    if high_density <= low_density + 0.20:
        return False, f"density_not_separated=low{low_density:.3f}_high{high_density:.3f}"
    return True, f"edges={len(edges)} low_density={low_density:.3f} high_density={high_density:.3f}"

CHECKER_ID = "v4_055_first_order_sigma_delta_modulator"
CHECKER: Checker = check_v3_496_first_order_sigma_delta_modulator
