"""Task-specific checker for canonical v4 DUT 203."""
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

def check_v3_cdac_8b_monodown(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "clks", "vres", *{f"dctrl{i}" for i in range(0, 8)}}
    if not rows or not required.issubset(rows[0]):
        return False, "missing cdac 8b monodown signals"
    times = [row["time"] for row in rows]
    threshold = 0.5
    events: list[tuple[float, str, int | None]] = []
    events += [
        (t, "sample", None)
        for t in _threshold_crossings([row["clks"] for row in rows], times, threshold=threshold, direction="falling")
    ]
    for bit in range(0, 8):
        signal = f"dctrl{bit}"
        events += [
            (t, "subtract", bit)
            for t in _threshold_crossings([row[signal] for row in rows], times, threshold=threshold, direction="rising")
        ]
    events.sort()
    if len(events) < 5:
        return False, f"too_few_cdac_events={len(events)}"

    residue = sample_signal_at(rows, "vin", rows[0]["time"]) or 0.0
    checked = 0
    max_err = 0.0
    failures: list[str] = []
    for event_t, kind, bit in events:
        if kind == "sample":
            sampled = sample_signal_at(rows, "vin", event_t + 1e-12)
            if sampled is None:
                continue
            residue = sampled
        elif bit is not None:
            residue -= 1.0 / (2 ** (8 - bit))
        sample_t = event_t + 0.12e-9
        if sample_t > rows[-1]["time"]:
            continue
        observed = sample_signal_at(rows, "vres", sample_t)
        if observed is None:
            continue
        err = abs(observed - residue)
        max_err = max(max_err, err)
        checked += 1
        if err > 0.035:
            detail = "sample" if kind == "sample" else f"dctrl{bit}"
            failures.append(f"vres_after_{detail}@{event_t * 1e9:.3f}ns={observed:.4f} expected={residue:.4f}")
    if checked < 5:
        return False, f"insufficient_cdac_checks={checked}"
    if failures:
        return False, " ".join(failures[:6])
    return True, f"cdac_events={checked} max_err={max_err:.4f}"

CHECKER_ID = "v4_203_cdac_8b_monodown"
CHECKER: Checker = check_v3_cdac_8b_monodown
