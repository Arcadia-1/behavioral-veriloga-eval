"""Task-specific checker for canonical v4 DUT 334."""
from __future__ import annotations

from checkers.api import Checker
def _v4_topup_logic_high(row: dict[str, float], name: str, threshold: float = 0.45) -> bool:
    return float(row.get(name, 0.0)) > threshold

def _v4_code_from_bits(row: dict[str, float], bits: list[str]) -> int:
    return sum((1 << idx) for idx, bit in enumerate(bits) if _v4_topup_logic_high(row, bit))

def _v4_rising(prev_v: float, now_v: float, vth: float = 0.45) -> bool:
    return now_v > vth and prev_v <= vth

def check_v4_1032_baseband_antialias_filter_macro(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1032 empty_trace"
    prev_clk = float(rows[0].get("clk", 0.0))
    expected_vout = 0.45
    expected_metric = 0.0
    update_time = -1.0
    checked = vout_errors = metric_errors = valid_errors = clear_errors = 0
    reset_clear = disabled_clear = high_bw_seen = low_bw_seen = moved_toward_input = False
    codes_seen: set[int] = set()
    for row in rows:
        t = float(row["time"])
        clk = float(row["clk"])
        rst = _v4_topup_logic_high(row, "rst")
        enabled = _v4_topup_logic_high(row, "enable") and not rst
        if not enabled:
            expected_vout = 0.45
            expected_metric = 0.0
            clear = abs(float(row["vout"]) - 0.45) < 0.08 and abs(float(row["bandwidth_metric"])) < 0.08 and not _v4_topup_logic_high(row, "valid")
            if rst and t < 5e-9 and clear:
                reset_clear = True
            if t > 82e-9 and not _v4_topup_logic_high(row, "enable") and clear:
                disabled_clear = True
            if ((rst and t < 5e-9) or t > 82e-9) and not clear:
                clear_errors += 1
            prev_clk = clk
            continue
        if _v4_rising(prev_clk, clk):
            code = _v4_code_from_bits(row, ["bw_0", "bw_1"])
            codes_seen.add(code)
            alpha = (code + 1) / 4.0
            old = expected_vout
            expected_vout = old + alpha * (float(row["vin"]) - old)
            expected_metric = 0.9 * code / 3.0
            if code >= 3:
                high_bw_seen = True
            if code <= 1:
                low_bw_seen = True
            if abs(expected_vout - float(row["vin"])) + 0.02 < abs(old - float(row["vin"])):
                moved_toward_input = True
            update_time = t
        prev_clk = clk
        if update_time < 0 or t < update_time + 0.7e-9:
            continue
        checked += 1
        if abs(float(row["vout"]) - expected_vout) > 0.05:
            vout_errors += 1
        if abs(float(row["bandwidth_metric"]) - expected_metric) > 0.08:
            metric_errors += 1
        if not _v4_topup_logic_high(row, "valid"):
            valid_errors += 1
    vout_budget = max(6, checked // 15)
    metric_budget = max(5, checked // 20)
    valid_budget = 3
    clear_budget = 4
    ok = (
        checked >= 35
        and len(codes_seen) >= 4
        and reset_clear
        and disabled_clear
        and high_bw_seen
        and low_bw_seen
        and moved_toward_input
        and vout_errors <= vout_budget
        and metric_errors <= metric_budget
        and valid_errors <= valid_budget
        and clear_errors <= clear_budget
    )
    return ok, (
        f"v4_1032 checked={checked} codes={sorted(codes_seen)} reset_clear={reset_clear} "
        f"disabled_clear={disabled_clear} high_bw_seen={high_bw_seen} low_bw_seen={low_bw_seen} "
        f"moved_toward_input={moved_toward_input} vout_errors={vout_errors} metric_errors={metric_errors} "
        f"valid_errors={valid_errors} clear_errors={clear_errors}; "
        f"P_ON_RESET_OR_WHEN_DISABLED_DRIVE mismatch_count={max(0, clear_errors - clear_budget) + int(not reset_clear) + int(not disabled_clear)}; "
        f"P_ON_EACH_ENABLED_RISING_CLK_EDGE mismatch_count={max(0, vout_errors - vout_budget)}; "
        f"P_UPDATE_VOUT_AS_A_FIRST_ORDER mismatch_count={max(0, vout_errors - vout_budget)}; "
        f"P_HIGHER_BANDWIDTH_CODE_MUST_MOVE_VOUT mismatch_count={max(0, vout_errors - vout_budget) + int(not high_bw_seen) + int(not low_bw_seen)}; "
        f"P_EXPOSE_THE_ACTIVE_BANDWIDTH_CODE_ON mismatch_count={max(0, metric_errors - metric_budget) + max(0, valid_errors - valid_budget)}"
    )

CHECKER_ID = "v4_334_baseband_anti_alias_filter_macro"
CHECKER: Checker = check_v4_1032_baseband_antialias_filter_macro
