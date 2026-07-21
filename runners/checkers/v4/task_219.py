"""Task-specific checker for canonical v4 DUT 219."""
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

def check_v3_bin2ther_2b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vdd", "gnd", "b1", "b0", "t0", "t1", "t2"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing bin2ther 2b signals"
    logic_signals = ("b1", "b0")
    input_states = {
        (
            row["b1"] > 0.5 * (row["vdd"] + row["gnd"]),
            row["b0"] > 0.5 * (row["vdd"] + row["gnd"]),
        )
        for row in rows
    }
    if len(input_states) < 2:
        return False, f"insufficient_logic_excitation={len(input_states)}"
    edge_times = [
        current["time"]
        for previous, current in zip(rows, rows[1:])
        if any(
            abs(current[signal] - previous[signal]) > 0.01
            for signal in (*logic_signals, "vdd", "gnd")
        )
    ]
    checked = 0
    max_err = 0.0
    failures: list[str] = []
    saw_local_threshold_distinction = False
    spans_seen: list[float] = []
    stride = max(1, len(rows) // 120)
    for row in rows[::stride]:
        if row["time"] < 0.05e-9 or not _v3_away_from_edges(row["time"], edge_times, margin_s=90e-12):
            continue
        vh = row["vdd"]
        vl = row["gnd"]
        vth = 0.5 * (vh + vl)
        spans_seen.append(vh - vl)
        saw_local_threshold_distinction = saw_local_threshold_distinction or any(
            (row[signal] > vth) != (row[signal] > 0.45)
            for signal in logic_signals
        )
        expected = {
            "t0": vh if row["b1"] > vth else vl,
            "t1": vh if row["b1"] > vth else vl,
            "t2": vh if row["b0"] > vth else vl,
        }
        checked += 1
        for signal, exp in expected.items():
            err = abs(row[signal] - exp)
            max_err = max(max_err, err)
            if err > 0.08:
                failures.append(f"{signal}@{row['time'] * 1e9:.3f}ns={row[signal]:.3f} expected={exp:.3f}")
    if checked < 16:
        return False, f"insufficient_bin2ther_checks={checked}"
    if max(spans_seen) - min(spans_seen) < 0.20:
        return False, "missing_local_rail_span_coverage"
    if not saw_local_threshold_distinction:
        return False, "missing_local_threshold_distinction"
    if failures:
        return False, " ".join(failures[:6])
    return True, (
        f"checked={checked} rail_span_range={max(spans_seen) - min(spans_seen):.3f} "
        f"local_threshold_distinction={saw_local_threshold_distinction} max_err={max_err:.3f}"
    )

CHECKER_ID = "v4_219_bin2ther_2b"
CHECKER: Checker = check_v3_bin2ther_2b
