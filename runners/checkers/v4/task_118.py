"""Task-specific checker for canonical v4 DUT 118."""
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

def check_v3_differential_buffer(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vinp", "vinn", "voutp", "voutn"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/vinp/vinn/voutp/voutn"
    probes = _stable_probe_times(rows, ["vinp", "vinn"], threshold=0.45, settle_s=0.5e-9)
    if len(probes) < 2:
        return False, f"too_few_buffer_probe_windows={len(probes)}"
    max_err = 0.0
    diff_signs: set[int] = set()
    checked = 0
    for time_s in probes:
        vinp = sample_signal_at(rows, "vinp", time_s)
        vinn = sample_signal_at(rows, "vinn", time_s)
        voutp = sample_signal_at(rows, "voutp", time_s)
        voutn = sample_signal_at(rows, "voutn", time_s)
        if vinp is None or vinn is None or voutp is None or voutn is None:
            return False, f"missing_buffer_pair_sample@{time_s * 1e9:.3f}ns"
        max_err = max(max_err, abs(voutp - vinp), abs(voutn - vinn))
        diff = vinp - vinn
        if abs(diff) > 0.05:
            diff_signs.add(1 if diff > 0.0 else -1)
        checked += 1
    if checked < 2:
        return False, f"too_few_buffer_checks={checked}"
    if diff_signs != {-1, 1}:
        return False, f"insufficient_differential_polarity_coverage={sorted(diff_signs)}"
    return max_err <= 0.025, f"checked={checked} diff_signs={sorted(diff_signs)} max_pair_error={max_err:.4f}"

CHECKER_ID = "v4_118_differential_buffer"
CHECKER: Checker = check_v3_differential_buffer
