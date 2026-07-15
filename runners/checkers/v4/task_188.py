"""Task-specific checker for canonical v4 DUT 188."""
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

def check_v3_cdac_bidirect_residue(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "clks", "dctrl1", "dctrl2", "dctrl3", "dctrl4", "dctrl5", "dctrl6", "dctrl7", "vres"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing cdac bidirect residue signals"

    threshold = 0.5
    events: list[tuple[float, str, str, float]] = []
    for edge_time in _edge_times_for_signal(rows, "clks", threshold=threshold, direction="falling"):
        events.append((edge_time, "sample", "clks", 0.0))
    events.extend((t, "step", "dctrl7", 0.5) for t in _edge_times_for_signal(rows, "dctrl7", threshold=threshold, direction="falling"))
    for bit, weight in ((6, 0.25), (5, 0.125), (4, 0.0625), (3, 0.03125), (2, 0.015625), (1, 0.0078125)):
        signal = f"dctrl{bit}"
        for edge_time in _edge_times_for_signal(rows, signal, threshold=threshold, direction="rising"):
            events.append((edge_time, "step", signal, -weight))
    events.sort(key=lambda item: item[0])

    if not any(kind == "sample" for _, kind, _, _ in events):
        return False, "missing_clks_falling_sample_event"
    if not any(signal == "dctrl7" for _, _, signal, _ in events):
        return False, "missing_dctrl7_half_scale_event"
    lower_step_count = sum(1 for _, _, signal, _ in events if signal in {"dctrl1", "dctrl2", "dctrl3", "dctrl4", "dctrl5", "dctrl6"})
    if lower_step_count < 3:
        return False, f"insufficient_binary_step_coverage={lower_step_count}"

    residue = rows[0]["vin"]
    first_probe = _event_probe_time(rows, rows[0]["time"], delay_s=0.20e-9)
    checked = 0
    max_error = 0.0
    if first_probe is not None:
        value = sample_signal_at(rows, "vres", first_probe)
        if value is not None:
            max_error = max(max_error, abs(value - residue))
            if abs(value - residue) > 0.025:
                return False, f"initial_vres={value:.4f} expected={residue:.4f}"
            checked += 1

    for event_time, kind, signal, delta in events:
        if kind == "sample":
            vin_at_edge = sample_signal_at(rows, "vin", event_time)
            if vin_at_edge is None:
                return False, f"missing_vin_at_clks_edge={event_time * 1e9:g}ns"
            residue = vin_at_edge
        else:
            residue += delta
        probe_time = _event_probe_time(rows, event_time, delay_s=0.14e-9)
        if probe_time is None:
            continue
        value = sample_signal_at(rows, "vres", probe_time)
        if value is None:
            return False, f"missing_vres_after_{signal}"
        error = abs(value - residue)
        max_error = max(max_error, error)
        checked += 1
        if error > 0.025:
            return False, f"vres_after_{signal}={value:.4f} expected={residue:.4f} err={error:.4f}"
    if checked < 4:
        return False, f"insufficient_residue_checks={checked}"
    return True, f"checked={checked} lower_steps={lower_step_count} max_residue_error={max_error:.5f}"

CHECKER_ID = "v4_188_cdac_bidirect_residue"
CHECKER: Checker = check_v3_cdac_bidirect_residue
