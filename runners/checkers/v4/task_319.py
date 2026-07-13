"""Task-specific checker for canonical v4 DUT 319."""
from __future__ import annotations

from checkers.api import Checker
from checkers.common.v4_topup import (
    _v4_code_from_bits,
    _v4_rising,
    _v4_topup_logic_high,
)

def check_v4_1017_unary_dac_glitch_energy_metric(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1017 empty_trace"
    prev_clk = float(rows[0].get("clk", 0.0))
    prev_code = 0
    expected_vout = expected_glitch = 0.0
    expected_valid = False
    update_time = -1.0
    checked = vout_errors = metric_errors = valid_errors = clear_errors = 0
    reset_clear = disabled_clear = glitch_seen = False
    codes_seen: set[int] = set()
    for row in rows:
        t = float(row["time"])
        clk = float(row["clk"])
        rst = _v4_topup_logic_high(row, "rst")
        enabled = _v4_topup_logic_high(row, "enable") and not rst
        if not enabled:
            expected_vout = expected_glitch = 0.0
            expected_valid = False
            prev_code = 0
            clear = abs(float(row["vout"])) < 0.08 and abs(float(row["glitch_metric"])) < 0.08 and not _v4_topup_logic_high(row, "valid")
            if rst and t < 5e-9 and clear:
                reset_clear = True
            if t > 82e-9 and not _v4_topup_logic_high(row, "enable") and clear:
                disabled_clear = True
            if ((rst and t < 5e-9) or t > 82e-9) and not clear:
                clear_errors += 1
            prev_clk = clk
            continue
        if _v4_rising(prev_clk, clk):
            code = _v4_code_from_bits(row, ["code_0", "code_1", "code_2"])
            codes_seen.add(code)
            expected_vout = 0.9 * code / 7.0
            expected_glitch = 0.9 * abs(code - prev_code) / 7.0
            expected_valid = True
            if expected_glitch > 0.05:
                glitch_seen = True
            prev_code = code
            update_time = t
        prev_clk = clk
        if update_time < 0 or t < update_time + 0.7e-9:
            continue
        checked += 1
        if abs(float(row["vout"]) - expected_vout) > 0.08:
            vout_errors += 1
        if abs(float(row["glitch_metric"]) - expected_glitch) > 0.08:
            metric_errors += 1
        if _v4_topup_logic_high(row, "valid") != expected_valid:
            valid_errors += 1
    ok = (
        checked >= 40
        and len(codes_seen) >= 5
        and reset_clear
        and disabled_clear
        and glitch_seen
        and vout_errors <= max(5, checked // 20)
        and metric_errors <= max(5, checked // 20)
        and valid_errors <= 3
        and clear_errors <= 4
    )
    return ok, (
        f"v4_1017 checked={checked} codes={sorted(codes_seen)} reset_clear={reset_clear} "
        f"disabled_clear={disabled_clear} glitch_seen={glitch_seen} vout_errors={vout_errors} "
        f"metric_errors={metric_errors} valid_errors={valid_errors} clear_errors={clear_errors}"
    )

CHECKER_ID = "v4_1017_unary_dac_glitch_energy_metric"
CHECKER: Checker = check_v4_1017_unary_dac_glitch_energy_metric
