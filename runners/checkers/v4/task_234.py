"""Task-specific checker for canonical v4 DUT 234."""
from __future__ import annotations

from checkers.api import Checker
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

def check_v3_programmable_divider_by_n(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "divctrl", "out"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing programmable divider by n signals"
    edges = _signal_threshold_edges(rows, "clk", threshold=0.45, directions=("rising",))
    if len(edges) < 4:
        return False, f"too_few_divider_edges={len(edges)}"
    state = 0
    checks = 0
    max_err = 0.0
    highs = 0
    lows = 0
    for edge_t in edges:
        ratio_v = sample_signal_at(rows, "divctrl", edge_t + 1e-12)
        if ratio_v is None:
            return False, f"missing_divctrl_at={edge_t * 1e9:.3f}ns"
        ratio = int(math.floor(ratio_v + 0.5))
        if ratio < 1:
            ratio = 1
        state += 1
        if state >= ratio:
            state = 0
        out_t = edge_t + 0.12e-9
        got = sample_signal_at(rows, "out", out_t)
        if got is None:
            return False, f"missing_out_at={out_t * 1e9:.3f}ns"
        want = 0.9 if state == 0 else 0.0
        max_err = max(max_err, abs(got - want))
        checks += 1
        if want > 0.45:
            highs += 1
        else:
            lows += 1
    if checks < 4 or highs == 0 or lows == 0:
        return False, f"insufficient_divider_coverage checks={checks} highs={highs} lows={lows}"
    if max_err > 0.08:
        return False, f"divider_max_err={max_err:.4f} edges={len(edges)}"
    return True, f"edges={len(edges)} checks={checks} highs={highs} lows={lows} max_err={max_err:.4f}"

CHECKER_ID = "v4_234_programmable_divider_by_n"
CHECKER: Checker = check_v3_programmable_divider_by_n
