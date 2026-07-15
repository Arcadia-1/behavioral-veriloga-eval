"""Task-specific checker for canonical v4 DUT 171."""
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

def _check_offset_search_driver_behavior(
    rows: list[dict[str, float]],
    *,
    clk: str,
    decision: str,
    vinp: str,
    vinn: str,
    common_signal: str | None,
    fixed_common: float,
    threshold: float,
    step_initial: float,
    high_decreases: bool,
    halve_on_polarity_change_only: bool,
    initial_polarity: int,
    min_edges: int,
) -> tuple[bool, str]:
    times = [row["time"] for row in rows]
    clk_values = [row[clk] for row in rows]
    falling_edges = _threshold_crossings(clk_values, times, threshold=threshold, direction="falling")
    if len(falling_edges) < min_edges:
        return False, f"too_few_falling_edges={len(falling_edges)}"

    diff = 0.0
    step = step_initial
    previous_polarity = initial_polarity
    checked = 0
    max_diff_err = 0.0
    max_cm_err = 0.0
    failures: list[str] = []

    for edge_t in falling_edges:
        decision_value = sample_signal_at(rows, decision, edge_t)
        if decision_value is None:
            continue
        polarity = 1 if decision_value > threshold else 0
        if halve_on_polarity_change_only:
            if polarity != previous_polarity and step > 0.0:
                step *= 0.5
            previous_polarity = polarity
        direction = -1.0 if polarity and high_decreases else 1.0
        if (not polarity) and high_decreases:
            direction = 1.0
        elif polarity and (not high_decreases):
            direction = 1.0
        elif (not polarity) and (not high_decreases):
            direction = -1.0
        diff += direction * step
        if not halve_on_polarity_change_only:
            step *= 0.5

        probe_t = _event_probe_time(rows, edge_t, delay_s=0.25e-9)
        if probe_t is None:
            continue
        observed_p = sample_signal_at(rows, vinp, probe_t)
        observed_n = sample_signal_at(rows, vinn, probe_t)
        if observed_p is None or observed_n is None:
            continue
        observed_diff = observed_p - observed_n
        expected_common = (
            sample_signal_at(rows, common_signal, probe_t)
            if common_signal is not None
            else fixed_common
        )
        if expected_common is None:
            continue
        observed_common = 0.5 * (observed_p + observed_n)
        diff_err = abs(observed_diff - diff)
        cm_err = abs(observed_common - expected_common)
        max_diff_err = max(max_diff_err, diff_err)
        max_cm_err = max(max_cm_err, cm_err)
        checked += 1
        if diff_err > 0.004:
            failures.append(
                f"diff@{probe_t * 1e9:.3f}ns={observed_diff:.5f} expected={diff:.5f}"
            )
        if cm_err > 0.004:
            failures.append(
                f"cm@{probe_t * 1e9:.3f}ns={observed_common:.5f} expected={expected_common:.5f}"
            )

    if checked < min_edges:
        return False, f"insufficient_checked_edges={checked}"
    if failures:
        return False, " ".join(failures[:5])
    return True, f"checked_edges={checked} max_diff_err={max_diff_err:.5f} max_cm_err={max_cm_err:.5f}"

def check_v3_comparator_offset_driver(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "dcmpp", "vinp", "vinn"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing comparator offset driver signals"
    vdd = _max_signal_value(rows, ["clk", "dcmpp"], default=0.9)
    return _check_offset_search_driver_behavior(
        rows,
        clk="clk",
        decision="dcmpp",
        vinp="vinp",
        vinn="vinn",
        common_signal=None,
        fixed_common=0.5 * vdd,
        threshold=0.5 * vdd,
        step_initial=0.100,
        high_decreases=True,
        halve_on_polarity_change_only=False,
        initial_polarity=0,
        min_edges=3,
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

CHECKER_ID = "v4_171_comparator_offset_driver"
CHECKER: Checker = check_v3_comparator_offset_driver
