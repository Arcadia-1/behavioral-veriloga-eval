"""Task-specific checker for canonical v4 DUT 026."""
from __future__ import annotations

from checkers.api import Checker
def rising_edges(values: list[float], times: list[float], threshold: float = 0.45) -> list[float]:
    edges: list[float] = []
    for i in range(1, len(values)):
        if values[i - 1] < threshold <= values[i]:
            edges.append(times[i])
    return edges

def check_phase_accumulator_timer_wrap(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk_out", "phase_out"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk_out/phase_out"
    phase_vals = [r["phase_out"] for r in rows]
    clk_vals = [r["clk_out"] for r in rows]
    times = [r["time"] for r in rows]
    phase_span = max(phase_vals) - min(phase_vals)
    if phase_span < 0.4:
        return False, f"phase_span_too_small={phase_span:.3f}"
    phase_lo = min(phase_vals)
    high_th = phase_lo + 0.70 * phase_span
    low_th = phase_lo + 0.30 * phase_span
    wraps = 0
    armed = False
    for phase in phase_vals:
        if phase >= high_th:
            armed = True
        elif armed and phase <= low_th:
            wraps += 1
            armed = False
    cth = 0.5 * (max(clk_vals) + min(clk_vals))
    clk_rises = len(rising_edges(clk_vals, times, threshold=cth))
    ok = wraps >= 3 and clk_rises >= 3
    return ok, f"wraps={wraps} clk_rises={clk_rises} phase_span={phase_span:.3f}"

CHECKER_ID = "v4_026_digital_phase_accumulator_with_modulo_wrap"
CHECKER: Checker = check_phase_accumulator_timer_wrap
