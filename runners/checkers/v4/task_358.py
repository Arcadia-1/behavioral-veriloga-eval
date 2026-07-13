"""Task-specific checker for canonical v4 DUT 358."""
from __future__ import annotations

from checkers.api import Checker
def _v4_topup_logic_high(row: dict[str, float], name: str, threshold: float = 0.45) -> bool:
    return float(row.get(name, 0.0)) > threshold

def _v4_code_from_bits(row: dict[str, float], bits: list[str]) -> int:
    return sum((1 << idx) for idx, bit in enumerate(bits) if _v4_topup_logic_high(row, bit))

def check_v4_917_quadrature_phase_interpolator(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk_i", "clk_q", "rst", "code_0", "code_1", "code_2", "code_3", "code_4", "clk_out", "quadrant_0", "quadrant_1", "phase_metric"}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "v4_917 missing_columns=" + ",".join(missing)
    checked = metric_errors = quadrant_errors = clear_errors = 0
    reset_clear = mid_reset_clear = code_low = code_high = clk_activity = False
    clk_values: list[float] = []
    prev_code: int | None = None
    settle_until = 0.0
    for row in rows[::6]:
        t = float(row["time"])
        if _v4_topup_logic_high(row, "rst"):
            prev_code = None
            settle_until = t
            clear = row["phase_metric"] < 0.08 and row["quadrant_0"] < 0.08 and row["quadrant_1"] < 0.08 and row["clk_out"] < 0.12
            reset_clear = reset_clear or (t < 4e-9 and clear)
            mid_reset_clear = mid_reset_clear or (53e-9 < t < 55e-9 and clear)
            if ((t < 4e-9) or (53e-9 < t < 55e-9)) and not clear:
                clear_errors += 1
            continue
        code = _v4_code_from_bits(row, ["code_0", "code_1", "code_2", "code_3", "code_4"])
        if prev_code is None or code != prev_code:
            prev_code = code
            settle_until = t + 1.1e-9
            continue
        if t < settle_until:
            continue
        quadrant = code // 8
        expected_metric = 0.9 * code / 31.0
        expected_q1 = quadrant in (2, 3)
        expected_q0 = quadrant in (1, 3)
        code_low = code_low or code <= 4
        code_high = code_high or code >= 24
        clk_values.append(float(row["clk_out"]))
        checked += 1
        if abs(float(row["phase_metric"]) - expected_metric) > 0.08:
            metric_errors += 1
        if _v4_topup_logic_high(row, "quadrant_1") != expected_q1 or _v4_topup_logic_high(row, "quadrant_0") != expected_q0:
            quadrant_errors += 1
    if clk_values and max(clk_values) > 0.65 and min(clk_values) < 0.20:
        clk_activity = True
    ok = checked >= 12 and reset_clear and mid_reset_clear and code_low and code_high and clk_activity and metric_errors <= 3 and quadrant_errors <= 3 and clear_errors <= 2
    return ok, f"v4_917 checked={checked} reset_clear={reset_clear} mid_reset_clear={mid_reset_clear} code_low={code_low} code_high={code_high} clk_activity={clk_activity} metric_errors={metric_errors} quadrant_errors={quadrant_errors} clear_errors={clear_errors}"

CHECKER_ID = "v4_358_quadrature_phase_interpolator"
CHECKER: Checker = check_v4_917_quadrature_phase_interpolator
