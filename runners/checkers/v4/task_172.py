"""Task-specific checker for canonical v4 DUT 172."""
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

def check_v3_pipe_2lane_edge_align(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "din1", "din2", "clk_align", "dout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing pipe 2lane edge align signals"
    times = [row["time"] for row in rows]
    clk = [row["clk_align"] for row in rows]
    events = [(t, "din1") for t in _threshold_crossings(clk, times, threshold=0.45, direction="rising")]
    events += [(t, "din2") for t in _threshold_crossings(clk, times, threshold=0.45, direction="falling")]
    events.sort()
    if len(events) < 4:
        return False, f"too_few_alignment_edges={len(events)}"

    max_err = 0.0
    checked = 0
    failures: list[str] = []
    for edge_t, source in events:
        sample_t = edge_t + 0.15e-9
        if sample_t > rows[-1]["time"]:
            continue
        expected = sample_signal_at(rows, source, edge_t + 1e-12)
        observed = sample_signal_at(rows, "dout", sample_t)
        if expected is None or observed is None:
            continue
        err = abs(observed - expected)
        max_err = max(max_err, err)
        checked += 1
        if err > 0.035:
            failures.append(
                f"dout_after_{source}_edge@{edge_t * 1e9:.3f}ns={observed:.4f} expected={expected:.4f}"
            )
    if checked < 4:
        return False, f"insufficient_alignment_samples={checked}"
    if failures:
        return False, " ".join(failures[:4])
    return True, f"alignment_edges={checked} max_err={max_err:.4f}"

CHECKER_ID = "v4_172_pipe_2lane_edge_align"
CHECKER: Checker = check_v3_pipe_2lane_edge_align
