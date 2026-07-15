"""Task-specific checker for canonical v4 DUT 152."""
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

def check_v3_two_channel_sample_demux(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "samp1", "samp2", "clks1", "clks2", "vout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing demux input/output signals"
    events: list[tuple[float, str]] = []
    events.extend((edge, "samp1") for edge in _v3_edge_times(rows, "clks1", threshold=0.45, direction=1))
    events.extend((edge, "samp2") for edge in _v3_edge_times(rows, "clks2", threshold=0.45, direction=1))
    events.sort(key=lambda item: item[0])
    if len(events) < 4:
        return False, f"too_few_demux_events={len(events)}"
    max_err = 0.0
    checked = 0
    covered = {"samp1": 0, "samp2": 0}
    for edge, source in events:
        expected = sample_signal_at(rows, source, edge)
        if expected is None:
            return False, f"missing_{source}_at_edge={edge * 1e9:.3f}ns"
        sample_t = edge + 1.0e-9
        if sample_t > rows[-1]["time"]:
            continue
        observed = sample_signal_at(rows, "vout", sample_t)
        if observed is None:
            return False, f"missing_demux_output_at={sample_t * 1e9:.3f}ns"
        max_err = max(max_err, abs(observed - expected))
        covered[source] += 1
        checked += 1
    if checked < 4:
        return False, f"too_few_demux_checks={checked}"
    if not all(count >= 2 for count in covered.values()):
        return False, f"insufficient_demux_channel_coverage={covered}"
    return max_err <= 0.035, f"checked={checked} max_error={max_err:.5f} covered={covered}"

CHECKER_ID = "v4_152_two_channel_sample_demux"
CHECKER: Checker = check_v3_two_channel_sample_demux
