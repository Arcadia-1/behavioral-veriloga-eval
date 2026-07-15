"""Task-specific checker for canonical v4 DUT 221."""
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

def check_v3_samplehold_rising_edge(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "control", "vin", "vout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing samplehold rising edge signals"
    times = [r["time"] for r in rows]
    edges = _threshold_crossings(
        [r["control"] for r in rows],
        times,
        threshold=2.5,
        direction="rising",
    )
    if len(edges) < 2:
        return False, f"too_few_control_edges={len(edges)}"

    sample_errors: list[float] = []
    hold_windows = 0
    hold_failures = 0
    nontransparent_windows = 0
    for idx, edge_t in enumerate(edges):
        vin_edge = sample_signal_at(rows, "vin", edge_t)
        vout_settled = sample_signal_at(rows, "vout", edge_t + 0.12e-9)
        if vin_edge is None or vout_settled is None:
            return False, f"missing_edge_sample_at={edge_t:.3e}"
        sample_errors.append(abs(vout_settled - vin_edge))

        if idx + 1 >= len(edges):
            continue
        start = edge_t + 0.25e-9
        stop = edges[idx + 1] - 0.25e-9
        if stop <= start:
            continue
        vout_vals = [r["vout"] for r in rows if start <= r["time"] <= stop]
        vin_vals = [r["vin"] for r in rows if start <= r["time"] <= stop]
        if len(vout_vals) < 4:
            continue
        hold_windows += 1
        vout_span = max(vout_vals) - min(vout_vals)
        vin_span = max(vin_vals) - min(vin_vals) if vin_vals else 0.0
        if vout_span > 0.08:
            hold_failures += 1
        if vin_span > 0.25 and vout_span < 0.10:
            nontransparent_windows += 1

    max_sample_err = max(sample_errors)
    ok = (
        max_sample_err <= 0.08
        and hold_windows >= 1
        and hold_failures == 0
        and nontransparent_windows >= 1
    )
    return ok, (
        f"edges={len(edges)} max_sample_err={max_sample_err:.3f} "
        f"hold_windows={hold_windows} hold_failures={hold_failures} "
        f"nontransparent_windows={nontransparent_windows}"
    )

CHECKER_ID = "v4_221_samplehold_rising_edge"
CHECKER: Checker = check_v3_samplehold_rising_edge
