"""Task-specific checker for canonical v4 DUT 242."""
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

def check_v3_flash_folded_dac4(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vd4", "vd3", "vd2", "vd1", "vout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing flash folded dac4 signals"
    edge_times: list[float] = []
    for signal in ["vd4", "vd3", "vd2", "vd1"]:
        edge_times.extend(_signal_threshold_edges(rows, signal, threshold=0.45, directions=("rising", "falling")))
    max_err = 0.0
    checked = 0
    msb_low = 0
    msb_high = 0
    for row in rows:
        if row["time"] < 0.15e-9:
            continue
        if not _v3_away_from_edges(row["time"], edge_times, 80e-12):
            continue
        lower = 0.0
        lower += 4.0 if row["vd3"] > 0.45 else 0.0
        lower += 2.0 if row["vd2"] > 0.45 else 0.0
        lower += 1.0 if row["vd1"] > 0.45 else 0.0
        if row["vd4"] > 0.45:
            code = 8.0 + lower
            msb_high += 1
        else:
            code = 8.0 - lower
            msb_low += 1
        expected = code / 16.0
        max_err = max(max_err, abs(row["vout"] - expected))
        checked += 1
    if checked < 20 or msb_low == 0 or msb_high == 0:
        return False, f"insufficient_flash_folded_dac4_coverage checked={checked} low={msb_low} high={msb_high}"
    return max_err <= 0.035, f"checked={checked} msb_low={msb_low} msb_high={msb_high} max_err={max_err:.5f}"

CHECKER_ID = "v4_242_flash_folded_dac4"
CHECKER: Checker = check_v3_flash_folded_dac4
