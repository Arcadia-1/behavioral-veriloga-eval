"""Task-specific checker for canonical v4 DUT 328."""
from __future__ import annotations

from checkers.api import Checker
def _v4_topup_logic_high(row: dict[str, float], name: str, threshold: float = 0.45) -> bool:
    return float(row.get(name, 0.0)) > threshold

def _v4_code_from_bits(row: dict[str, float], bits: list[str]) -> int:
    return sum((1 << idx) for idx, bit in enumerate(bits) if _v4_topup_logic_high(row, bit))

def _v4_rising(prev_v: float, now_v: float, vth: float = 0.45) -> bool:
    return now_v > vth and prev_v <= vth

def check_v4_1026_pam4_linearity_monitor(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1026 empty_trace"
    prev_clk = float(rows[0].get("clk", 0.0))
    expected_level = metric = 0.0
    update_time = -1.0
    checked = level_errors = metric_errors = valid_errors = clear_errors = 0
    reset_clear = disabled_clear = False
    codes_seen: set[int] = set()
    for row in rows:
        t = float(row["time"])
        clk = float(row["clk"])
        rst = _v4_topup_logic_high(row, "rst")
        enabled = _v4_topup_logic_high(row, "enable") and not rst
        if not enabled:
            clear = abs(float(row["level_out"])) < 0.08 and abs(float(row["linearity_metric"])) < 0.08 and not _v4_topup_logic_high(row, "valid")
            if rst and t < 5e-9 and clear:
                reset_clear = True
            if t > 82e-9 and not _v4_topup_logic_high(row, "enable") and clear:
                disabled_clear = True
            if ((rst and t < 5e-9) or t > 82e-9) and not clear:
                clear_errors += 1
            prev_clk = clk
            continue
        if _v4_rising(prev_clk, clk):
            code = _v4_code_from_bits(row, ["symbol_0", "symbol_1"])
            codes_seen.add(code)
            expected_level = 0.9 * code / 3.0
            metric = 0.9
            update_time = t
        prev_clk = clk
        if update_time < 0 or t < update_time + 0.7e-9:
            continue
        checked += 1
        if abs(float(row["level_out"]) - expected_level) > 0.08:
            level_errors += 1
        if abs(float(row["linearity_metric"]) - metric) > 0.08:
            metric_errors += 1
        if not _v4_topup_logic_high(row, "valid"):
            valid_errors += 1
    level_budget = max(5, checked // 20)
    metric_budget = max(5, checked // 20)
    valid_budget = 3
    clear_budget = 4
    ok = (
        checked >= 35
        and len(codes_seen) >= 4
        and reset_clear
        and disabled_clear
        and level_errors <= level_budget
        and metric_errors <= metric_budget
        and valid_errors <= valid_budget
        and clear_errors <= clear_budget
    )
    return ok, (
        f"v4_1026 checked={checked} codes={sorted(codes_seen)} reset_clear={reset_clear} "
        f"disabled_clear={disabled_clear} level_errors={level_errors} metric_errors={metric_errors} "
        f"valid_errors={valid_errors} clear_errors={clear_errors}; "
        f"P_ON_RESET_OR_WHEN_DISABLED_CLEAR mismatch_count={max(0, clear_errors - clear_budget) + int(not reset_clear) + int(not disabled_clear)}; "
        f"P_ON_EACH_ENABLED_RISING_CLK_EDGE mismatch_count={max(0, level_errors - level_budget)}; "
        f"P_DRIVE_LEVEL_OUT_TO_EVENLY_SPACED mismatch_count={max(0, level_errors - level_budget)}; "
        f"P_EXPOSE_A_LINEARITY_METRIC_THAT_IS mismatch_count={max(0, metric_errors - metric_budget)}; "
        f"P_ASSERT_VALID_AFTER_EACH_SAMPLED_SYMBOL mismatch_count={max(0, valid_errors - valid_budget)}"
    )

CHECKER_ID = "v4_328_pam4_linearity_monitor"
CHECKER: Checker = check_v4_1026_pam4_linearity_monitor
