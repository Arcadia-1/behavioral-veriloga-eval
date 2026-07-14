"""Task-specific checker for canonical v4 DUT 228."""
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

def _max_signal_value(
    rows: list[dict[str, float]],
    signals: list[str],
    *,
    default: float,
) -> float:
    values: list[float] = []
    for row in rows:
        for signal in signals:
            value = row.get(signal)
            if value is not None:
                values.append(value)
    return max(values) if values else default

def _v3_away_from_edges(row_time: float, edge_times: list[float], margin_s: float = 80e-12) -> bool:
    return all(abs(row_time - edge_time) > margin_s for edge_time in edge_times)

def check_v3_divide_by_two_toggle_v2(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "out"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing divide by two toggle signals"
    vdd = _max_signal_value(rows, ["clk", "out"], default=0.9)
    if vdd < 0.5:
        vdd = 0.9
    threshold = 0.5 * vdd
    edge_times = _signal_threshold_edges(rows, "clk", threshold=threshold, directions=("rising", "falling"))
    state = 0
    toggles = 0
    checked = 0
    max_err = 0.0
    failures: list[str] = []
    prev = rows[0]
    for row in rows[1:]:
        if prev["clk"] <= threshold < row["clk"]:
            state = 1 - state
            toggles += 1
        prev = row
        if row["time"] < 0.05e-9 or not _v3_away_from_edges(row["time"], edge_times, margin_s=90e-12):
            continue
        expected = vdd if state else 0.0
        err = abs(row["out"] - expected)
        max_err = max(max_err, err)
        checked += 1
        if err > 0.08:
            failures.append(f"t={row['time'] * 1e9:.3f}ns out={row['out']:.3f} expected={expected:.3f}")
    if checked < 20 or toggles < 4:
        return False, f"insufficient_div2_coverage checked={checked} toggles={toggles}"
    if failures:
        return False, " ".join(failures[:6])
    return True, f"checked={checked} toggles={toggles} max_err={max_err:.3f}"

CHECKER_ID = "v4_228_divide_by_two_toggle"
CHECKER: Checker = check_v3_divide_by_two_toggle_v2
