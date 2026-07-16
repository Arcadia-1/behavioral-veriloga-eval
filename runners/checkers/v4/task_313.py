"""Task-specific checker for canonical v4 DUT 313."""
from __future__ import annotations

from ..api import Checker
from .diagnostics import excess_count
from ..common.v4_topup import (
    _v4_topup_clip01,
    _v4_topup_logic_high,
    _v4_rising,
)

def check_v4_313_dynamic_comparator_kickback_metric(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1011 empty_trace"
    def clock_period() -> float:
        rises: list[float] = []
        previous_clk = float(rows[0].get("clk", 0.0))
        for candidate in rows[1:]:
            now = float(candidate.get("clk", 0.0))
            if _v4_rising(previous_clk, now):
                rises.append(float(candidate["time"]))
            previous_clk = now
        periods = [right - left for left, right in zip(rises, rises[1:]) if right > left]
        return sorted(periods)[len(periods) // 2] if periods else 1.0

    def first_after(target_time: float) -> dict[str, float] | None:
        for candidate in rows:
            if float(candidate["time"]) >= target_time:
                return candidate
        return None

    period = clock_period()
    reset_clear = late_reset_clear = late_reset_violation = disabled_clear = False
    checked = decision_errors = metric_errors = valid_errors = 0
    premature_valid = False
    high_seen = low_seen = small_overdrive_seen = large_overdrive_seen = False
    metric_small: list[float] = []
    metric_large: list[float] = []
    decision_seen_since_clear = False
    saw_active = False
    previous = rows[0]
    for row in rows[1:]:
        clk_rise = (not _v4_topup_logic_high(previous, "clk")) and _v4_topup_logic_high(row, "clk")
        rst = _v4_topup_logic_high(row, "rst")
        enabled = _v4_topup_logic_high(row, "enable")
        clear = (
            row["decision"] < 0.15
            and row["kickback_metric"] < 0.15
            and row["valid"] < 0.15
        )
        if rst:
            if saw_active:
                late_reset_clear = late_reset_clear or clear
                late_reset_violation = late_reset_violation or not clear
            else:
                reset_clear = reset_clear or clear
            decision_seen_since_clear = False
        elif not enabled:
            if saw_active:
                disabled_clear = disabled_clear or clear
            decision_seen_since_clear = False
        elif clk_rise:
            saw_active = True
            decision_seen_since_clear = True
        elif float(row["valid"]) > 0.45 and not decision_seen_since_clear:
            premature_valid = True
        previous = row
        if not clk_rise or rst or not enabled:
            continue
        sample = first_after(float(row["time"]) + 0.15 * period)
        if sample is None:
            continue
        if _v4_topup_logic_high(row, "rst") or not _v4_topup_logic_high(row, "enable"):
            continue
        diff = float(row["vinp"]) - float(row["vinn"])
        overdrive = abs(diff)
        expected_decision = diff >= 0.0
        expected_metric = _v4_topup_clip01(0.45 + 0.30 / (1.0 + overdrive / 0.030))
        checked += 1
        high_seen = high_seen or expected_decision
        low_seen = low_seen or not expected_decision
        if overdrive < 0.07:
            small_overdrive_seen = True
            metric_small.append(float(sample["kickback_metric"]))
        if overdrive > 0.22:
            large_overdrive_seen = True
            metric_large.append(float(sample["kickback_metric"]))
        if (float(sample["decision"]) > 0.45) != expected_decision:
            decision_errors += 1
        if abs(float(sample["kickback_metric"]) - expected_metric) > 0.10:
            metric_errors += 1
        if sample["valid"] <= 0.45:
            valid_errors += 1
    monotonic_metric = bool(metric_small and metric_large and min(metric_small) > max(metric_large) + 0.04)
    metric_allowance = max(1, checked // 10)
    ok = (
        checked >= 6
        and reset_clear
        and late_reset_clear
        and not late_reset_violation
        and disabled_clear
        and high_seen
        and low_seen
        and small_overdrive_seen
        and large_overdrive_seen
        and monotonic_metric
        and decision_errors == 0
        and metric_errors <= metric_allowance
        and valid_errors == 0
        and not premature_valid
    )
    clear_mismatches = (
        int(not reset_clear)
        + int(not late_reset_clear)
        + int(late_reset_violation)
        + int(not disabled_clear)
    )
    decision_mismatches = decision_errors
    metric_mismatches = excess_count(metric_errors, metric_allowance)
    monotonic_mismatches = int(not monotonic_metric)
    valid_mismatches = valid_errors + int(premature_valid)
    return ok, (
        f"v4_313 checked={checked} reset_clear={reset_clear} late_reset_clear={late_reset_clear} "
        f"late_reset_violation={late_reset_violation} "
        f"disabled_clear={disabled_clear} "
        f"high={high_seen} low={low_seen} small={small_overdrive_seen} large={large_overdrive_seen} "
        f"monotonic_metric={monotonic_metric} decision_errors={decision_errors} "
        f"metric_errors={metric_errors} valid_errors={valid_errors} premature_valid={premature_valid}; "
        f"P_ON_RESET_OR_WHEN_DISABLED_CLEAR mismatch_count={clear_mismatches}; "
        f"P_ON_EACH_ENABLED_RISING_CLK_EDGE mismatch_count={decision_mismatches}; "
        f"P_DRIVE_KICKBACK_METRIC_AS_A_VOLTAGE mismatch_count={metric_mismatches}; "
        f"P_SMALL_OVERDRIVE_MUST_PRODUCE_A_LARGER mismatch_count={monotonic_mismatches}; "
        f"P_ASSERT_VALID_AFTER_EACH_COMPLETED_DECISION mismatch_count={valid_mismatches}"
    )

CHECKER_ID = "v4_313_dynamic_comparator_kickback_metric"
CHECKER: Checker = check_v4_313_dynamic_comparator_kickback_metric
