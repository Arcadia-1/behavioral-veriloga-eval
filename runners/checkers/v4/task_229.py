"""Task-specific checker for canonical v4 DUT 229."""
from __future__ import annotations

from ..api import Checker
def rising_edges(values: list[float], times: list[float], threshold: float = 0.45) -> list[float]:
    edges: list[float] = []
    for i in range(1, len(values)):
        if values[i - 1] < threshold <= values[i]:
            edges.append(times[i])
    return edges

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

def check_v3_accum3_pulse(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "out"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing accum3 pulse signals"
    vdd = _max_signal_value(rows, ["clk", "out"], default=0.9)
    if vdd < 0.5:
        vdd = 0.9
    threshold = 0.5 * vdd
    edge_times = _signal_threshold_edges(rows, "clk", threshold=threshold, directions=("rising", "falling"))
    count = 7
    rising_edges = 0
    pulse_rows = 0
    low_rows = 0
    max_err = 0.0
    failures: list[str] = []
    prev = rows[0]
    for row in rows[1:]:
        if prev["clk"] <= threshold < row["clk"]:
            count = (count + 1) % 8
            rising_edges += 1
        prev = row
        if row["time"] < 0.05e-9 or not _v3_away_from_edges(row["time"], edge_times, margin_s=90e-12):
            continue
        expected = vdd if count == 0 else 0.0
        if count == 0:
            pulse_rows += 1
        else:
            low_rows += 1
        err = abs(row["out"] - expected)
        max_err = max(max_err, err)
        if err > 0.08:
            failures.append(f"t={row['time'] * 1e9:.3f}ns out={row['out']:.3f} expected={expected:.3f}")
    if rising_edges < 8 or pulse_rows < 4 or low_rows < 12:
        return False, f"insufficient_accum3_coverage edges={rising_edges} pulse_rows={pulse_rows} low_rows={low_rows}"
    if failures:
        return False, " ".join(failures[:6])
    return True, f"edges={rising_edges} pulse_rows={pulse_rows} low_rows={low_rows} max_err={max_err:.3f}"

CHECKER_ID = "v4_229_accum3_pulse"
CHECKER: Checker = check_v3_accum3_pulse
