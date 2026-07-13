"""Task-specific checker for canonical v4 DUT 231."""
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

def check_v3_decision_router_logic(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin1", "vin2", "valid", "x", "y", "z", "dm", "dl"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing decision router logic signals"
    input_signals = ["vin1", "vin2", "valid"]
    threshold = 0.5 * _max_signal_value(rows, input_signals, default=0.9)
    edge_times: list[float] = []
    for signal in input_signals:
        edge_times.extend(_signal_threshold_edges(rows, signal, threshold=threshold, directions=("rising", "falling")))
    checked = 0
    combos_seen: set[tuple[int, int, int]] = set()
    max_err = 0.0
    failures: list[str] = []
    stride = max(1, len(rows) // 120)
    for row in rows[::stride]:
        if row["time"] < 0.05e-9 or not _v3_away_from_edges(row["time"], edge_times, margin_s=90e-12):
            continue
        a = 1 if row["vin1"] > threshold else 0
        b = 1 if row["vin2"] > threshold else 0
        ok = 1 if row["valid"] > threshold else 0
        combos_seen.add((a, b, ok))
        expected = {
            "dm": 0.9 if a else 0.0,
            "dl": 0.9 if ((not a) and b) else 0.0,
            "x": 0.9 if ((not a) and (not b) and ok) else 0.0,
            "y": 0.9 if (a and b and ok) else 0.0,
            "z": 0.9 if ((not a) and b and ok) else 0.0,
        }
        checked += 1
        for signal, exp in expected.items():
            err = abs(row[signal] - exp)
            max_err = max(max_err, err)
            if err > 0.08:
                failures.append(f"{signal}@{row['time'] * 1e9:.3f}ns={row[signal]:.3f} expected={exp:.3f}")
    if checked < 20 or len(combos_seen) < 4:
        return False, f"insufficient_router_coverage checked={checked} combos={sorted(combos_seen)}"
    if failures:
        return False, " ".join(failures[:6])
    return True, f"checked={checked} combos={sorted(combos_seen)} max_err={max_err:.3f}"

CHECKER_ID = "v4_231_decision_router_logic"
CHECKER: Checker = check_v3_decision_router_logic
