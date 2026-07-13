"""Task-specific checker for canonical v4 DUT 110."""
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

def check_v3_start_gated_offset_search(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "start", "vout", "vinp", "vinn"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/start/vout/vinp/vinn"
    vdd = _max_signal_value(rows, ["clk", "start", "vout"], default=0.9)
    vth = 0.5 * vdd
    clk_falls = _edge_times_for_signal(rows, "clk", threshold=vth, direction="falling")
    if len(clk_falls) < 3:
        return False, f"too_few_clock_falls={len(clk_falls)}"

    diff = 0.0
    step = 20e-3
    state = 1
    checked = 0
    active_edges = 0
    max_diff_err = 0.0
    max_cm_err = 0.0
    failures: list[str] = []
    for edge_t in clk_falls:
        start_value = sample_signal_at(rows, "start", edge_t)
        if start_value is None or start_value <= vth:
            continue
        active_edges += 1
        decision = sample_signal_at(rows, "vout", edge_t)
        if decision is None:
            continue
        sign = 1 if decision > vth else 0
        if state != sign and step > 0.0:
            step *= 0.5
        state = sign
        diff = diff + (2 * state - 1) * step
        probe_t = _event_probe_time(rows, edge_t, delay_s=0.25e-9)
        if probe_t is None:
            continue
        vinp = sample_signal_at(rows, "vinp", probe_t)
        vinn = sample_signal_at(rows, "vinn", probe_t)
        if vinp is None or vinn is None:
            continue
        observed_diff = vinp - vinn
        observed_cm = 0.5 * (vinp + vinn)
        diff_err = abs(observed_diff - diff)
        cm_err = abs(observed_cm - 0.70)
        max_diff_err = max(max_diff_err, diff_err)
        max_cm_err = max(max_cm_err, cm_err)
        checked += 1
        if diff_err > 0.0035:
            failures.append(
                f"diff@{probe_t * 1e9:.2f}ns={observed_diff:.5f} expected={diff:.5f}"
            )
        if cm_err > 0.0035:
            failures.append(f"cm@{probe_t * 1e9:.2f}ns={observed_cm:.5f}")
    if active_edges < 3 or checked < 3:
        return False, f"insufficient_active_search_edges active={active_edges} checked={checked}"
    if failures:
        return False, " ".join(failures[:5])
    return True, (
        f"active_edges={active_edges} checked={checked} "
        f"max_diff_err={max_diff_err:.5f} max_cm_err={max_cm_err:.5f}"
    )

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

def _edge_times_for_signal(
    rows: list[dict[str, float]],
    signal: str,
    *,
    threshold: float,
    direction: str,
) -> list[float]:
    times = [row["time"] for row in rows if "time" in row and signal in row]
    values = [row[signal] for row in rows if "time" in row and signal in row]
    if len(times) < 2:
        return []
    return _threshold_crossings(values, times, threshold=threshold, direction=direction)

def _event_probe_time(
    rows: list[dict[str, float]],
    event_time_s: float,
    *,
    delay_s: float = 0.18e-9,
) -> float | None:
    if not rows:
        return None
    last_time = rows[-1].get("time")
    if last_time is None:
        return None
    probe_time = event_time_s + delay_s
    if probe_time <= last_time:
        return probe_time
    fallback = last_time - 0.02e-9
    return fallback if fallback > event_time_s else None

CHECKER_ID = "v4_110_start_gated_offset_search"
CHECKER: Checker = check_v3_start_gated_offset_search
