"""Task-specific checker for canonical v4 DUT 168."""
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

def _logic_level_at(
    rows: list[dict[str, float]],
    signal: str,
    time_s: float,
    *,
    threshold: float = 0.45,
) -> int | None:
    value = sample_signal_at(rows, signal, time_s)
    if value is None:
        return None
    return 1 if value > threshold else 0

def _stable_probe_times(
    rows: list[dict[str, float]],
    signals: list[str],
    *,
    threshold: float = 0.45,
    settle_s: float = 0.3e-9,
) -> list[float]:
    if not rows:
        return []
    first_t = rows[0]["time"]
    last_t = rows[-1]["time"]
    cuts = [first_t, last_t]
    for signal in signals:
        cuts.extend(_signal_threshold_edges(rows, signal, threshold=threshold))
    cuts = sorted({t for t in cuts if first_t <= t <= last_t})
    probes: list[float] = []
    for start_t, end_t in zip(cuts, cuts[1:]):
        width = end_t - start_t
        if width <= 2.0 * settle_s:
            continue
        probe_t = 0.5 * (start_t + end_t)
        if start_t + settle_s <= probe_t <= end_t - settle_s:
            probes.append(probe_t)
    return probes

def check_v3_dac_ideal_4b_offset(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "din0", "din1", "din2", "din3", "dout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing dac ideal 4b offset signals"
    probes = _stable_probe_times(rows, ["din0", "din1", "din2", "din3"])
    if len(probes) < 4:
        return False, f"too_few_offset_dac_probe_windows={len(probes)}"
    codes: list[int] = []
    max_err = 0.0
    scaling = 32.0 * 10.0 / 9.0
    for time_s in probes:
        bits = [
            _logic_level_at(rows, "din3", time_s),
            _logic_level_at(rows, "din2", time_s),
            _logic_level_at(rows, "din1", time_s),
            _logic_level_at(rows, "din0", time_s),
        ]
        out = sample_signal_at(rows, "dout", time_s)
        if any(bit is None for bit in bits) or out is None:
            return False, f"missing_offset_dac_sample_at={time_s * 1e9:.3f}ns"
        bit_values = [int(bit) for bit in bits]
        code = 8 * bit_values[0] + 4 * bit_values[1] + 2 * bit_values[2] + bit_values[3]
        expected = 0.239 + code / scaling
        max_err = max(max_err, abs(out - expected))
        codes.append(code)
    if max_err > 0.025:
        return False, f"offset_dac_max_err={max_err:.4f} codes={codes}"
    if len(set(codes)) < 4 or max(codes) < 14:
        return False, f"insufficient_offset_dac_code_coverage={codes}"
    return True, f"codes={codes} max_err={max_err:.4f}"

CHECKER_ID = "v4_168_dac_ideal_4b_offset"
CHECKER: Checker = check_v3_dac_ideal_4b_offset
