"""Task-specific checker for canonical v4 DUT 106."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import structured_result


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

def check_v3_clocked_comparator_reset_low(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "cmpck", "vinp", "vinn", "dcmpn", "dcmpp"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/cmpck/vinp/vinn/dcmpn/dcmpp"
    vdd = _max_signal_value(rows, ["cmpck", "dcmpn", "dcmpp"], default=0.9)
    vth = 0.5 * vdd
    rises = _edge_times_for_signal(rows, "cmpck", threshold=vth, direction="rising")
    falls = _edge_times_for_signal(rows, "cmpck", threshold=vth, direction="falling")
    if len(rises) < 2 or not falls:
        return False, f"insufficient_clock_edges rises={len(rises)} falls={len(falls)}"

    failures: list[str] = []
    reset_checks = 0
    decisions = {"positive": 0, "negative": 0}
    for edge_t in falls:
        probe_t = _event_probe_time(rows, edge_t, delay_s=0.30e-9)
        if probe_t is None:
            continue
        outp = sample_signal_at(rows, "dcmpp", probe_t)
        outn = sample_signal_at(rows, "dcmpn", probe_t)
        if outp is None or outn is None:
            continue
        reset_checks += 1
        if outp > 0.30 * vdd or outn > 0.30 * vdd:
            failures.append(f"reset_not_low@{probe_t * 1e9:.2f}ns={outp:.3f}/{outn:.3f}")

    for edge_t in rises:
        probe_t = _event_probe_time(rows, edge_t, delay_s=0.30e-9)
        if probe_t is None:
            continue
        vinp = sample_signal_at(rows, "vinp", edge_t)
        vinn = sample_signal_at(rows, "vinn", edge_t)
        outp = sample_signal_at(rows, "dcmpp", probe_t)
        outn = sample_signal_at(rows, "dcmpn", probe_t)
        if vinp is None or vinn is None or outp is None or outn is None:
            continue
        if vinp > vinn + 0.004:
            decisions["positive"] += 1
            if outp < 0.70 * vdd or outn > 0.30 * vdd:
                failures.append(f"positive_wrong@{probe_t * 1e9:.2f}ns={outp:.3f}/{outn:.3f}")
        elif vinn > vinp + 0.004:
            decisions["negative"] += 1
            if outn < 0.70 * vdd or outp > 0.30 * vdd:
                failures.append(f"negative_wrong@{probe_t * 1e9:.2f}ns={outp:.3f}/{outn:.3f}")
    if reset_checks < 1:
        return False, f"too_few_reset_checks={reset_checks}"
    if decisions["positive"] < 1 or decisions["negative"] < 1:
        return False, f"missing_decision_polarity_counts={decisions}"
    if failures:
        return False, " ".join(failures[:6])
    return True, f"reset_checks={reset_checks} decisions={decisions}"

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

CHECKER_ID = "v4_106_clocked_comparator_reset_low"
PROPERTY_IDS = (
    "P_INITIAL_RESET_LOW",
    "P_FALLING_EDGE_RESET_LOW",
    "P_POSITIVE_DIFFERENTIAL_DECISION",
    "P_NEGATIVE_DIFFERENTIAL_DECISION",
    "P_EQUAL_INPUT_RESET_STATE",
    "P_LATCHED_HOLD_AND_TIMING",
)
CHECKER: Checker = structured_result(check_v3_clocked_comparator_reset_low, PROPERTY_IDS)
