"""Task-specific checker for canonical v4 DUT 019."""
from __future__ import annotations

from checkers.api import Checker
def sample_signal(rows: list[dict[str, float]], signal: str, time_s: float) -> float | None:
    if not rows or signal not in rows[0] or "time" not in rows[0]:
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
    return rows[-1].get(signal)

def _crossing_times(
    rows: list[dict[str, float]],
    signal: str,
    *,
    threshold: float = 0.45,
    direction: str = "rising",
) -> list[float]:
    if not rows or "time" not in rows[0] or signal not in rows[0]:
        return []
    crossings: list[float] = []
    for idx in range(1, len(rows)):
        prev = rows[idx - 1]
        cur = rows[idx]
        t0 = prev.get("time")
        t1 = cur.get("time")
        v0 = prev.get(signal)
        v1 = cur.get(signal)
        if t0 is None or t1 is None or v0 is None or v1 is None:
            continue
        if direction == "rising":
            hit = v0 <= threshold < v1
        elif direction == "falling":
            hit = v0 >= threshold > v1
        else:
            raise ValueError(f"unsupported direction={direction!r}")
        if not hit:
            continue
        if v1 == v0:
            crossings.append(t1)
        else:
            alpha = (threshold - v0) / (v1 - v0)
            crossings.append(t0 + alpha * (t1 - t0))
    return crossings

def check_vco_phase_integrator(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vctrl", "phase", "clk"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/vctrl/phase/clk"

    phase_values = [row["phase"] for row in rows]
    phase_span = max(phase_values) - min(phase_values)
    clk_edges = _crossing_times(rows, "clk")
    early_edges = [time for time in clk_edges if 10e-9 <= time <= 80e-9]
    late_edges = [time for time in clk_edges if 90e-9 <= time <= rows[-1]["time"]]
    phase_1ns = sample_signal(rows, "phase", 1e-9)
    phase_10ns = sample_signal(rows, "phase", 10e-9)
    startup_ok = phase_1ns is not None and 0.025 <= phase_1ns <= 0.06
    phase_progress = phase_10ns is not None and phase_10ns > 0.25
    span_ok = phase_span > 0.85
    edge_rate_ok = len(clk_edges) >= 5 and len(late_edges) >= len(early_edges)
    ok = startup_ok and phase_progress and span_ok and edge_rate_ok
    return ok, (
        f"phase_1ns={(phase_1ns if phase_1ns is not None else float('nan')):.3f} "
        f"phase_10ns={(phase_10ns if phase_10ns is not None else float('nan')):.3f} "
        f"phase_span={phase_span:.3f} clk_edges={len(clk_edges)} "
        f"early_edges={len(early_edges)} late_edges={len(late_edges)}"
    )

CHECKER_ID = "v4_019_vco_phase_integrator"
CHECKER: Checker = check_vco_phase_integrator
