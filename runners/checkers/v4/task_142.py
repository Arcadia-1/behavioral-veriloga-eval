"""Task-specific checker for canonical v4 DUT 142."""
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

def check_v3_ideal_dac_4bit_differential(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "digital", "vcm", "vop", "von"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/digital/vcm/vop/von"
    edges = _signal_threshold_edges(rows, "clk", threshold=0.5, directions=("falling",))
    if len(edges) < 4:
        return False, f"too_few_differential_dac_falling_edges={len(edges)}"
    codes: list[int] = []
    max_err = 0.0
    max_cm_error = 0.0
    for edge_t in edges:
        code_sample = sample_signal_at(rows, "digital", edge_t)
        out_t = edge_t + 0.8e-9
        vcm = sample_signal_at(rows, "vcm", out_t)
        vop = sample_signal_at(rows, "vop", out_t)
        von = sample_signal_at(rows, "von", out_t)
        if code_sample is None or vcm is None or vop is None or von is None:
            return False, f"missing_differential_dac_sample_at={out_t * 1e9:.3f}ns"
        code = max(0, min(15, int(code_sample)))
        lsb = 2.0 / 16.0
        vod = code * lsb - 1.0 + lsb / 2.0
        max_err = max(max_err, abs(vop - (vcm + vod / 2.0)), abs(von - (vcm - vod / 2.0)))
        max_cm_error = max(max_cm_error, abs(0.5 * (vop + von) - vcm))
        codes.append(code)
    if max_err > 0.03 or max_cm_error > 0.02:
        return False, f"differential_dac_max_err={max_err:.4f} max_cm_error={max_cm_error:.4f} codes={codes}"
    if len(set(codes)) < 4 or min(codes) > 2 or max(codes) != 15:
        return False, f"insufficient_differential_dac_code_coverage={codes}"
    return True, f"codes={codes} max_err={max_err:.4f} max_cm_error={max_cm_error:.4f}"

CHECKER_ID = "v4_142_ideal_dac_4bit_differential"
CHECKER: Checker = check_v3_ideal_dac_4bit_differential
