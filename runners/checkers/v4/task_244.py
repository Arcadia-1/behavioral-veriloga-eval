"""Task-specific checker for canonical v4 DUT 244."""
from __future__ import annotations

from ..api import Checker
import math

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

def check_v3_clocked_adc3bit(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "vclk", "vd0", "vd1", "vd2"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing clocked adc3bit signals"
    edges = _signal_threshold_edges(rows, "vclk", threshold=0.45, directions=("rising",))
    if len(edges) < 4:
        return False, f"too_few_clocked_adc3bit_rising_edges={len(edges)}"
    codes: list[int] = []
    max_err = 0.0
    for edge_t in edges:
        vin = sample_signal_at(rows, "vin", edge_t)
        out_t = edge_t + 0.08e-9
        if vin is None:
            return False, f"missing_clocked_adc3bit_input_at={edge_t * 1e9:.3f}ns"
        code = math.floor(8.0 * vin)
        code = max(0, min(7, code))
        expected = {
            "vd0": 0.9 if (code & 1) else 0.0,
            "vd1": 0.9 if ((code >> 1) & 1) else 0.0,
            "vd2": 0.9 if ((code >> 2) & 1) else 0.0,
        }
        for signal, want in expected.items():
            got = sample_signal_at(rows, signal, out_t)
            if got is None:
                return False, f"missing_{signal}_sample_at={out_t * 1e9:.3f}ns"
            max_err = max(max_err, abs(got - want))
        codes.append(code)
    if max_err > 0.06:
        return False, f"clocked_adc3bit_max_err={max_err:.4f} codes={codes}"
    if len(set(codes)) < 3 or min(codes) != 0 or max(codes) != 7:
        return False, f"insufficient_clocked_adc3bit_code_coverage={codes}"
    return True, f"codes={codes} max_err={max_err:.4f}"

CHECKER_ID = "v4_244_clocked_adc3bit"
CHECKER: Checker = check_v3_clocked_adc3bit
