"""Task-specific checker for canonical v4 DUT 213."""
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

def check_v3_tool_4bit_sar_signed_dac(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "sh", "aout", *{f"d{i}" for i in range(4)}}
    if not rows or not required.issubset(rows[0]):
        return False, "missing tool 4bit sar signed dac signals"
    times = [row["time"] for row in rows]
    high_level = max(max(row[signal] for row in rows) for signal in ("sh", "d0", "d1", "d2", "d3"))
    if high_level < 1.0:
        high_level = 1.8
    threshold = high_level / 2.0
    sample_edges = _threshold_crossings([row["sh"] for row in rows], times, threshold=threshold, direction="rising")
    if len(sample_edges) < 3:
        return False, f"too_few_sample_edges={len(sample_edges)}"

    weights = {3: 8.0, 2: 4.0, 1: 2.0, 0: 1.0}
    gain = high_level / 16.0
    checked = 0
    hold_checks = 0
    max_err = 0.0
    failures: list[str] = []
    for edge_t in sample_edges:
        total = 0.0
        bit_text: list[str] = []
        for bit, weight in weights.items():
            value = sample_signal_at(rows, f"d{bit}", edge_t + 1e-12)
            if value is None:
                continue
            high = value > threshold
            bit_text.append("1" if high else "0")
            total += weight if high else -weight
        expected = total * gain
        observed = sample_signal_at(rows, "aout", edge_t + 0.08e-9)
        if observed is None:
            continue
        err = abs(observed - expected)
        max_err = max(max_err, err)
        checked += 1
        if err > 0.04:
            failures.append(
                f"aout@{edge_t * 1e9:.3f}ns={observed:.4f} expected={expected:.4f} bits={''.join(bit_text)}"
            )
        next_index = checked
        if next_index < len(sample_edges):
            next_edge = sample_edges[next_index]
            hold_t = next_edge - 0.08e-9
            held = sample_signal_at(rows, "aout", hold_t)
            if held is None:
                return False, f"missing_aout_pre_edge_hold_at={hold_t * 1e9:.3f}ns"
            hold_checks += 1
            if abs(held - expected) > 0.04:
                failures.append(
                    f"aout_hold@{hold_t * 1e9:.3f}ns={held:.4f} expected={expected:.4f}"
                )
    if checked < 3:
        return False, f"insufficient_signed_dac_checks={checked}"
    if failures:
        return False, " ".join(failures[:5])
    return True, (
        f"signed_dac_samples={checked} hold_checks={hold_checks} "
        f"max_err={max_err:.4f}"
    )

CHECKER_ID = "v4_213_tool_4bit_sar_signed_dac"
CHECKER: Checker = check_v3_tool_4bit_sar_signed_dac
