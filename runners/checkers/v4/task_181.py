"""Task-specific checker for canonical v4 DUT 181."""
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

def check_v3_pipe15_data_align(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "samp", *{f"d{i}" for i in range(15)}, *{f"do{i}" for i in range(15)}}
    if not rows or not required.issubset(rows[0]):
        return False, "missing pipe15 data align outputs"
    times = [row["time"] for row in rows]
    edges = _threshold_crossings([row["samp"] for row in rows], times, threshold=0.45, direction="rising")
    if len(edges) < 5:
        return False, f"too_few_sample_edges={len(edges)}"

    max_err = 0.0
    checked = 0
    failures: list[str] = []
    for edge_idx, edge_t in enumerate(edges):
        sample_t = edge_t + 0.12e-9
        if sample_t > rows[-1]["time"]:
            continue
        for bit in range(15):
            if bit <= 2:
                delay = 0
            elif bit <= 6:
                delay = 1
            elif bit <= 10:
                delay = 2
            else:
                delay = 4
            source_idx = edge_idx - delay
            if source_idx < 0:
                expected = 0.0
            else:
                expected = sample_signal_at(rows, f"d{bit}", edges[source_idx] + 1e-12)
                if expected is None:
                    continue
            observed = sample_signal_at(rows, f"do{bit}", sample_t)
            if observed is None:
                continue
            err = abs(observed - expected)
            max_err = max(max_err, err)
            checked += 1
            if err > 0.12:
                failures.append(
                    f"do{bit}@{edge_t * 1e9:.3f}ns={observed:.3f} expected={expected:.3f} delay={delay}"
                )
    if checked < 45:
        return False, f"insufficient_pipe_align_checks={checked}"
    if failures:
        return False, " ".join(failures[:6])
    return True, f"aligned_bit_samples={checked} max_err={max_err:.4f}"

CHECKER_ID = "v4_181_pipe15_data_align"
CHECKER: Checker = check_v3_pipe15_data_align
