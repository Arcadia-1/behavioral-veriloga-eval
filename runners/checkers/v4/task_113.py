"""Task-specific checker for canonical v4 DUT 113."""
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

def check_v3_sar_weighted_sum(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "d10", "d9", "d8", "d7", "d6", "d5", "d4", "d3", "d2", "d1", "d0", "vout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/d10/d9/d8/d7/d6/d5/d4/d3/d2/d1/d0/vout"
    bit_signals = ["d10", "d9", "d8", "d7", "d6", "d5", "d4", "d3", "d2", "d1", "d0"]
    weights = [448, 256, 128, 80, 48, 32, 16, 8, 4, 2, 1]
    vth = 0.5 * _max_signal_value(rows, bit_signals, default=0.9)
    change_times: list[float] = []
    for signal in bit_signals:
        change_times.extend(_edge_times_for_signal(rows, signal, threshold=vth, direction="rising"))
        change_times.extend(_edge_times_for_signal(rows, signal, threshold=vth, direction="falling"))
    change_times = sorted(set(round(t, 15) for t in change_times))
    candidates: list[float] = []
    if change_times:
        candidates.append(max(rows[0]["time"], change_times[0] - 2.0e-9))
    else:
        candidates.append(rows[0]["time"])
    candidates.extend(t + 0.50e-9 for t in change_times)
    candidates = [t for t in candidates if rows[0]["time"] <= t <= rows[-1]["time"]]

    checked = 0
    distinct_codes: set[int] = set()
    max_err = 0.0
    failures: list[str] = []
    for t in candidates:
        code_weight = 0
        code_bits = 0
        for idx, signal in enumerate(bit_signals):
            value = sample_signal_at(rows, signal, t)
            if value is None:
                break
            if value > vth:
                code_weight += weights[idx]
                code_bits |= 1 << (len(bit_signals) - 1 - idx)
        else:
            observed = sample_signal_at(rows, "vout", t)
            if observed is None:
                continue
            expected = code_weight / 512.0 - 1.0
            err = abs(observed - expected)
            max_err = max(max_err, err)
            distinct_codes.add(code_bits)
            checked += 1
            if err > 0.025:
                failures.append(
                    f"code=0x{code_bits:03x}@{t * 1e9:.2f}ns={observed:.4f} expected={expected:.4f}"
                )
    if checked < 4:
        return False, f"too_few_weighted_sum_states={checked}"
    if len(distinct_codes) < 4:
        return False, f"insufficient_distinct_codes={len(distinct_codes)}"
    if failures:
        return False, " ".join(failures[:5])
    return True, f"checked={checked} distinct_codes={len(distinct_codes)} max_err={max_err:.5f}"

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

CHECKER_ID = "v4_113_sar_weighted_sum"
CHECKER: Checker = check_v3_sar_weighted_sum
