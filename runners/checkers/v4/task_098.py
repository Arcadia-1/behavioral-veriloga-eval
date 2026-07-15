"""Task-specific checker for canonical v4 DUT 098."""
from __future__ import annotations

from ..api import Checker
def rising_edges(values: list[float], times: list[float], threshold: float = 0.45) -> list[float]:
    edges: list[float] = []
    for i in range(1, len(values)):
        if values[i - 1] < threshold <= values[i]:
            edges.append(times[i])
    return edges

def check_v3_reference_step_clock(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows or not {"time", "CLK"}.issubset(rows[0]):
        return False, "missing time/CLK"

    times = [row["time"] for row in rows]
    clk = [row["CLK"] for row in rows]
    vmin = min(clk)
    vmax = max(clk)
    if vmax - vmin < 0.75:
        return False, f"insufficient_clock_swing={vmax - vmin:.3f}"
    vth = 0.5 * (vmin + vmax)
    rises = rising_edges(clk, times, vth)
    if len(rises) < 80:
        return False, f"too_few_rising_edges={len(rises)}"

    t0 = times[0]
    t1 = times[-1]
    span = t1 - t0
    early_start = t0 + 0.10 * span
    early_stop = t0 + 0.40 * span
    late_start = t0 + 0.70 * span
    late_stop = t0 + 0.95 * span
    early_periods = [b - a for a, b in zip(rises, rises[1:]) if early_start <= a <= early_stop]
    late_periods = [b - a for a, b in zip(rises, rises[1:]) if late_start <= a <= late_stop]
    if len(early_periods) < 10 or len(late_periods) < 10:
        return False, f"insufficient_period_windows early={len(early_periods)} late={len(late_periods)}"
    early = sum(early_periods) / len(early_periods)
    late = sum(late_periods) / len(late_periods)

    high_frac_early = weighted_logic_high_fraction_window(rows, "CLK", vth, early_start, early_stop)
    high_frac_late = weighted_logic_high_fraction_window(rows, "CLK", vth, late_start, late_stop)
    period_tol = 0.35e-9
    period_pair_ok = any(
        abs(early - expected_pre) <= period_tol and abs(late - expected_post) <= period_tol
        for expected_pre, expected_post in ((20.0e-9, 19.5e-9), (18.0e-9, 22.0e-9))
    )
    duty_ok = 0.43 <= high_frac_early <= 0.57 and 0.43 <= high_frac_late <= 0.57
    ok = period_pair_ok and duty_ok
    return ok, (
        f"period_pre={early:.3e} period_post={late:.3e} "
        f"duty_pre={high_frac_early:.3f} duty_post={high_frac_late:.3f} "
        f"period_pair_ok={period_pair_ok}"
    )

def weighted_logic_high_fraction(rows: list[dict[str, float]], signal: str, threshold: float) -> float:
    if len(rows) < 2:
        return 0.0
    total_dt = rows[-1]["time"] - rows[0]["time"]
    if total_dt <= 0.0:
        return 0.0

    high_dt = 0.0
    for idx in range(1, len(rows)):
        dt = rows[idx]["time"] - rows[idx - 1]["time"]
        if dt <= 0.0:
            continue
        v_mid = 0.5 * (rows[idx - 1][signal] + rows[idx][signal])
        if v_mid > threshold:
            high_dt += dt
    return high_dt / total_dt

def time_window(rows: list[dict[str, float]], t_start: float, t_end: float) -> list[dict[str, float]]:
    return [r for r in rows if t_start <= r["time"] <= t_end]

def weighted_logic_high_fraction_window(
    rows: list[dict[str, float]],
    signal: str,
    threshold: float,
    t_start: float,
    t_end: float,
) -> float:
    return weighted_logic_high_fraction(time_window(rows, t_start, t_end), signal, threshold)

CHECKER_ID = "v4_098_reference_step_clock"
CHECKER: Checker = check_v3_reference_step_clock
