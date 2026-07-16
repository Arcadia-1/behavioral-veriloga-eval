"""Task-specific checker for canonical v4 DUT 337."""
from __future__ import annotations

from ..api import Checker
from .diagnostics import with_diagnostic_contract
def _v4_topup_clip01(value: float, low: float = 0.0, high: float = 0.9) -> float:
    return max(low, min(high, value))

def _v4_topup_logic_high(row: dict[str, float], name: str, threshold: float = 0.45) -> bool:
    return float(row.get(name, 0.0)) > threshold

def _v4_code_from_bits(row: dict[str, float], bits: list[str]) -> int:
    return sum((1 << idx) for idx, bit in enumerate(bits) if _v4_topup_logic_high(row, bit))

def _v4_rising(prev_v: float, now_v: float, vth: float = 0.45) -> bool:
    return now_v > vth and prev_v <= vth

def check_v4_1035_vga_step_response_classifier(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1035 empty_trace"
    prev_clk = float(rows[0].get("clk", 0.0))
    prev_code = 0
    stable_count = 0
    expected_vout = 0.45
    expected_metric = 0.0
    expected_settled = False
    update_time = -1.0
    checked = vout_errors = metric_errors = settled_errors = clear_errors = 0
    reset_clear = disabled_clear = high_gain_seen = overshoot_seen = settled_seen = False
    ever_enabled = False
    disable_time: float | None = None
    codes_seen: set[int] = set()
    for row in rows:
        t = float(row["time"])
        clk = float(row["clk"])
        rst = _v4_topup_logic_high(row, "rst")
        enabled = _v4_topup_logic_high(row, "enable") and not rst
        if not enabled:
            prev_code = 0
            stable_count = 0
            expected_vout = 0.45
            expected_metric = 0.0
            expected_settled = False
            clear = abs(float(row["vout"]) - 0.45) < 0.08 and abs(float(row["overshoot_metric"])) < 0.08 and not _v4_topup_logic_high(row, "settled")
            if rst and clear:
                reset_clear = True
            disabled = ever_enabled and not _v4_topup_logic_high(row, "enable")
            if disabled and disable_time is None:
                disable_time = t
            disabled_ready = (
                disabled
                and disable_time is not None
                and t >= disable_time + 0.7e-9
            )
            if disabled_ready and clear:
                disabled_clear = True
            if (rst or disabled_ready) and not clear:
                clear_errors += 1
            prev_clk = clk
            continue
        ever_enabled = True
        disable_time = None
        if _v4_rising(prev_clk, clk):
            code = _v4_code_from_bits(row, ["gain_0", "gain_1", "gain_2"])
            codes_seen.add(code)
            target = _v4_topup_clip01(0.45 + (1.0 + 0.5 * code) * (float(row["vin"]) - 0.45))
            expected_metric = 0.9 * abs(code - prev_code) / 7.0
            expected_vout = target
            stable_count = stable_count + 1 if code == prev_code else 0
            expected_settled = stable_count >= 2
            if code >= 5:
                high_gain_seen = True
            if expected_metric > 0.05:
                overshoot_seen = True
            prev_code = code
            update_time = t
        prev_clk = clk
        if update_time < 0 or t < update_time + 0.7e-9:
            continue
        checked += 1
        if abs(float(row["vout"]) - expected_vout) > 0.09:
            vout_errors += 1
        if abs(float(row["overshoot_metric"]) - expected_metric) > 0.08:
            metric_errors += 1
        settled = _v4_topup_logic_high(row, "settled")
        settled_seen = settled_seen or settled
        if settled != expected_settled:
            settled_errors += 1
    vout_budget = max(6, checked // 15)
    metric_budget = max(5, checked // 20)
    settled_budget = max(5, checked // 20)
    clear_budget = 4
    ok = (
        checked >= 35
        and len(codes_seen) >= 5
        and reset_clear
        and disabled_clear
        and high_gain_seen
        and overshoot_seen
        and settled_seen
        and vout_errors <= vout_budget
        and metric_errors <= metric_budget
        and settled_errors <= settled_budget
        and clear_errors <= clear_budget
    )
    return ok, (
        f"v4_1035 checked={checked} codes={sorted(codes_seen)} reset_clear={reset_clear} "
        f"disabled_clear={disabled_clear} high_gain_seen={high_gain_seen} overshoot_seen={overshoot_seen} "
        f"settled_seen={settled_seen} vout_errors={vout_errors} metric_errors={metric_errors} "
        f"settled_errors={settled_errors} clear_errors={clear_errors}; "
        f"P_ON_RESET_OR_WHEN_DISABLED_DRIVE mismatch_count={max(0, clear_errors - clear_budget) + int(not reset_clear) + int(not disabled_clear)}; "
        f"P_ON_EACH_ENABLED_RISING_CLK_EDGE mismatch_count={max(0, vout_errors - vout_budget)}; "
        f"P_APPLY_BOUNDED_SETTLING_WITH_A_CODE mismatch_count={max(0, vout_errors - vout_budget)}; "
        f"P_EXPOSE_OVERSHOOT_MAGNITUDE_ON_OVERSHOOT_METRIC mismatch_count={max(0, metric_errors - metric_budget)}; "
        f"P_ASSERT_SETTLED_AFTER_TWO_CONSECUTIVE_UPDATES mismatch_count={max(0, settled_errors - settled_budget) + int(not settled_seen)}"
    )

CHECKER_ID = "v4_337_vga_step_response_classifier"
CHECKER: Checker = with_diagnostic_contract(check_v4_1035_vga_step_response_classifier)
