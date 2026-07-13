"""Task-specific checker for canonical v4 DUT 209."""
from __future__ import annotations

from checkers.api import Checker
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

def check_v3_dac_restore_6bit_1p8(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "vout", *{f"d{i}" for i in range(1, 7)}}
    if not rows or not required.issubset(rows[0]):
        return False, "missing dac restore 6bit 1p8 signals"
    vth = 0.5 * _max_signal_value(rows, ["clk", *[f"d{i}" for i in range(1, 7)]], default=1.8)
    rising_edges = _edge_times_for_signal(rows, "clk", threshold=vth, direction="rising")
    if len(rising_edges) < 3:
        return False, f"too_few_restore6_clock_edges={len(rising_edges)}"
    weights = {1: 32, 2: 16, 3: 8, 4: 4, 5: 2, 6: 1}
    checked = 0
    max_err = 0.0
    codes: list[int] = []
    failures: list[str] = []
    for edge_t in rising_edges:
        probe_t = _event_probe_time(rows, edge_t, delay_s=0.12e-9)
        if probe_t is None:
            continue
        code = 0
        for bit, weight in weights.items():
            value = sample_signal_at(rows, f"d{bit}", edge_t + 1e-12)
            if value is None:
                return False, f"missing_d{bit}_at={edge_t * 1e9:.3f}ns"
            code += weight if value > vth else 0
        expected = (code + 0.5) * 3.6 / 64.0 - 1.8
        observed = sample_signal_at(rows, "vout", probe_t)
        if observed is None:
            return False, f"missing_vout_after_clk={edge_t * 1e9:.3f}ns"
        err = abs(observed - expected)
        max_err = max(max_err, err)
        checked += 1
        codes.append(code)
        if err > 0.035:
            failures.append(
                f"vout@{probe_t * 1e9:.3f}ns={observed:.4f} expected={expected:.4f} code={code}"
            )
    if checked < 3:
        return False, f"insufficient_restore6_checks={checked}"
    if len(set(codes)) < 3:
        return False, f"insufficient_restore6_code_coverage={codes}"
    if failures:
        return False, " ".join(failures[:5])
    return True, f"restore6_edges={checked} codes={codes} max_err={max_err:.4f}"

CHECKER_ID = "v4_209_dac_restore_6bit_1p8"
CHECKER: Checker = check_v3_dac_restore_6bit_1p8
