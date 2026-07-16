"""Task-specific checker for canonical v4 DUT 108."""
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

def _check_pulse_onset_delay(
    rows: list[dict[str, float]],
    *,
    input_signal: str,
    output_signal: str,
    input_edges: list[float],
    threshold: float,
    minimum_s: float = 0.60e-9,
    maximum_s: float = 1.50e-9,
) -> tuple[list[float], list[str]]:
    output_edges = _edge_times_for_signal(
        rows, output_signal, threshold=threshold, direction="rising"
    )
    delays: list[float] = []
    failures: list[str] = []
    for edge_t in input_edges:
        candidates = [out_t for out_t in output_edges if edge_t <= out_t <= edge_t + 3.0e-9]
        if not candidates:
            failures.append(f"onset_missing@{edge_t * 1e9:.2f}ns")
            continue
        delay = min(candidates) - edge_t
        delays.append(delay)
        if not minimum_s <= delay <= maximum_s:
            failures.append(
                f"onset_delay@{edge_t * 1e9:.2f}ns={delay * 1e9:.3f}ns "
                f"expected={minimum_s * 1e9:.2f}-{maximum_s * 1e9:.2f}ns"
            )
    return delays, failures

def check_v3_crossing_pulse_detector(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "sigin", "sigout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/sigin/sigout"
    vdd = _max_signal_value(rows, ["sigin", "sigout"], default=0.9)
    vth = 0.5 * vdd
    edges = sorted(
        _edge_times_for_signal(rows, "sigin", threshold=vth, direction="rising")
        + _edge_times_for_signal(rows, "sigin", threshold=vth, direction="falling")
    )
    if len(edges) < 2:
        return False, f"too_few_input_crossings={len(edges)}"
    high_checks = 0
    low_checks = 0
    failures: list[str] = []
    onset_delays, onset_failures = _check_pulse_onset_delay(
        rows,
        input_signal="sigin",
        output_signal="sigout",
        input_edges=edges,
        threshold=vth,
    )
    failures.extend(onset_failures)
    for edge_t in edges:
        high_t = edge_t + 2.0e-9
        if high_t <= rows[-1]["time"]:
            value = sample_signal_at(rows, "sigout", high_t)
            if value is not None:
                high_checks += 1
                if value < 0.70 * vdd:
                    failures.append(f"pulse_missing@{high_t * 1e9:.2f}ns={value:.3f}")
        low_t = edge_t + 7.0e-9
        if low_t <= rows[-1]["time"]:
            value = sample_signal_at(rows, "sigout", low_t)
            if value is not None:
                low_checks += 1
                if value > 0.30 * vdd:
                    failures.append(f"pulse_not_cleared@{low_t * 1e9:.2f}ns={value:.3f}")
    if high_checks < 2 or low_checks < 2:
        return False, f"insufficient_pulse_checks high={high_checks} low={low_checks}"
    if failures:
        return False, " ".join(failures[:6])
    return True, (
        f"crossings={len(edges)} high_checks={high_checks} low_checks={low_checks} "
        f"onset_delays_ns={[round(value * 1e9, 3) for value in onset_delays]}"
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

CHECKER_ID = "v4_108_crossing_pulse_detector"
PROPERTY_IDS = (
    "P_RISING_CROSS_PULSE",
    "P_FALLING_CROSS_PULSE",
    "P_PULSE_WIDTH",
    "P_LOW_BETWEEN_EVENTS",
    "P_REPEATABLE_BIDIRECTIONAL_EVENTS",
    "P_TRANSITION_TIMING",
)
CHECKER: Checker = structured_result(check_v3_crossing_pulse_detector, PROPERTY_IDS)
