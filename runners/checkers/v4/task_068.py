"""Task-specific checker for canonical v4 DUT 068."""
from __future__ import annotations

from ..api import Checker
def _rising_times(rows: list[dict[str, float]], col: str, vth: float = 0.45) -> list[float]:
    times: list[float] = []
    last = rows[0][col] > vth
    for row in rows[1:]:
        cur = row[col] > vth
        if not last and cur:
            times.append(row["time"])
        last = cur
    return times

def check_multiphase_clock_generator_4ph(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk0", "clk90", "clk180", "clk270"}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing[:12])
    rises = {col: _rising_times(rows, col)[:4] for col in ("clk0", "clk90", "clk180", "clk270")}
    if any(len(v) < 2 for v in rises.values()):
        return False, f"too_few_edges={ {k: len(v) for k, v in rises.items()} }"
    errors = 0
    period_errors = 0
    clk0_periods = [b - a for a, b in zip(rises["clk0"], rises["clk0"][1:])]
    for period in clk0_periods:
        if abs(period - 20e-9) > 1.5e-9:
            period_errors += 1
    for base in rises["clk0"][:3]:
        targets = [base + 5e-9, base + 10e-9, base + 15e-9]
        cols = ["clk90", "clk180", "clk270"]
        for col, target in zip(cols, targets):
            if min(abs(t - target) for t in rises[col]) > 1.5e-9:
                errors += 1
    return errors == 0 and period_errors == 0, (
        f"edge_counts={ {k: len(v) for k, v in rises.items()} } "
        f"phase_errors={errors} period_errors={period_errors}"
    )

CHECKER_ID = "v4_068_multiphase_clock_generator_4ph"
CHECKER: Checker = check_multiphase_clock_generator_4ph
