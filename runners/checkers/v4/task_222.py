"""Task-specific checker for canonical v4 DUT 222."""
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

def check_v3_trim_ctrl_5bit(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "ain", "dout0", "dout1", "dout2", "dout3", "dout4"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing trim ctrl 5bit signals"
    edge_times = _signal_threshold_edges(rows, "ain", threshold=0.5, directions=("rising", "falling"))
    edge_times.extend(
        row["time"]
        for prev, row in zip(rows, rows[1:])
        if abs(row["ain"] - prev["ain"]) > 0.25
    )
    checked = 0
    saw_clamp_low = False
    saw_clamp_high = False
    max_err = 0.0
    failures: list[str] = []
    stride = max(1, len(rows) // 120)
    for row in rows[::stride]:
        if row["time"] < 0.05e-9 or not _v3_away_from_edges(row["time"], edge_times, margin_s=90e-12):
            continue
        code = math.floor(row["ain"] + 0.5)
        if code < 0:
            code = 0
            saw_clamp_low = True
        if code > 31:
            code = 31
            saw_clamp_high = True
        checked += 1
        for bit in range(5):
            signal = f"dout{bit}"
            expected = 0.9 if ((code >> bit) & 1) else 0.0
            err = abs(row[signal] - expected)
            max_err = max(max_err, err)
            if err > 0.08:
                failures.append(f"{signal}@{row['time'] * 1e9:.3f}ns={row[signal]:.3f} expected={expected:.3f}")
    if checked < 20:
        return False, f"insufficient_trim_checks={checked}"
    if failures:
        return False, " ".join(failures[:6])
    return True, f"checked={checked} clamp_low={saw_clamp_low} clamp_high={saw_clamp_high} max_err={max_err:.3f}"

CHECKER_ID = "v4_222_trim_ctrl_5bit"
CHECKER: Checker = check_v3_trim_ctrl_5bit
