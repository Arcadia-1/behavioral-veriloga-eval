"""Task-specific checker for canonical v4 DUT 246."""
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

def _v3_away_from_edges(row_time: float, edge_times: list[float], margin_s: float = 80e-12) -> bool:
    return all(abs(row_time - edge_time) > margin_s for edge_time in edge_times)

def check_v3_mux4_priority(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "sel0", "sel1", "in0", "in1", "in2", "in3", "out"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing mux4 priority signals"
    edge_times: list[float] = []
    for signal in ["sel0", "sel1"]:
        edge_times.extend(_signal_threshold_edges(rows, signal, threshold=0.45, directions=("rising", "falling")))
    max_err = 0.0
    checked = 0
    codes = set()
    for row in rows:
        if row["time"] < 0.15e-9:
            continue
        if not _v3_away_from_edges(row["time"], edge_times, 80e-12):
            continue
        code = (1 if row["sel0"] > 0.45 else 0) + (2 if row["sel1"] > 0.45 else 0)
        expected = row[f"in{code}"]
        max_err = max(max_err, abs(row["out"] - expected))
        codes.add(code)
        checked += 1
    if checked < 20 or codes != {0, 1, 2, 3}:
        return False, f"insufficient_mux4_coverage checked={checked} codes={sorted(codes)}"
    return max_err <= 0.025, f"checked={checked} codes={sorted(codes)} max_err={max_err:.5f}"

CHECKER_ID = "v4_246_mux4_priority"
CHECKER: Checker = check_v3_mux4_priority
