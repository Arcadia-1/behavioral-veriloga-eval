"""Task-specific checker for canonical v4 DUT 309."""
from __future__ import annotations

from checkers.api import Checker
from checkers.v4.diagnostics import excess_count
from checkers.common.v4_topup import (
    _v4_topup_logic_high,
    _v4_topup_near,
    _v4_topup_span,
)

def check_v4_309_autozero_comparator_preamplifier(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1007 empty_trace"
    def first_after(target_time: float) -> dict[str, float] | None:
        for candidate in rows:
            if float(candidate["time"]) >= target_time:
                return candidate
        return None

    reset_clear = any(
        _v4_topup_logic_high(row, "rst")
        and row["decision"] < 0.15
        and _v4_topup_near(row["offset_store"], 0.45, 0.08)
        and row["ready"] < 0.15
        for row in rows
    )
    late_reset_clear = any(
        row["time"] > 50e-9
        and _v4_topup_logic_high(row, "rst")
        and row["decision"] < 0.15
        and _v4_topup_near(row["offset_store"], 0.45, 0.08)
        and row["ready"] < 0.15
        for row in rows
    )
    premature_ready = sum(1 for row in rows if 3e-9 < row["time"] < 7e-9 and row["ready"] > 0.45)
    checked = decision_errors = 0
    high_expected = low_expected = False
    previous = rows[0]
    for row in rows[1:]:
        clk_rise = (not _v4_topup_logic_high(previous, "clk")) and _v4_topup_logic_high(row, "clk")
        previous = row
        if row["time"] < 12e-9 or not clk_rise or not _v4_topup_logic_high(row, "eval_en"):
            continue
        sample = first_after(float(row["time"]) + 1.0e-9)
        if sample is None or sample["ready"] <= 0.45:
            continue
        corrected = float(row["vinp"]) - float(row["vinn"]) - (float(sample["offset_store"]) - 0.45)
        expected_high = corrected >= 0.0
        high_expected = high_expected or expected_high
        low_expected = low_expected or not expected_high
        checked += 1
        if (float(sample["decision"]) > 0.45) != expected_high:
            decision_errors += 1
    offset_dynamic = _v4_topup_span(rows, "offset_store") > 0.04
    ready_seen = any(row["time"] > 7e-9 and row["ready"] > 0.45 for row in rows)
    ok = (
        reset_clear
        and late_reset_clear
        and premature_ready <= 3
        and ready_seen
        and offset_dynamic
        and checked >= 4
        and high_expected
        and low_expected
        and decision_errors <= 1
    )
    decision_mismatches = excess_count(decision_errors, 1)
    reset_mismatches = int(not reset_clear) + int(not late_reset_clear)
    autozero_mismatches = int(not offset_dynamic)
    evaluation_mismatches = decision_mismatches
    expose_mismatches = (
        int(not offset_dynamic)
        + int(not ready_seen)
        + excess_count(premature_ready, 3)
    )
    return ok, (
        f"v4_309 checked={checked} reset_clear={reset_clear} late_reset_clear={late_reset_clear} premature_ready={premature_ready} "
        f"ready_seen={ready_seen} offset_dynamic={offset_dynamic} high_expected={high_expected} "
        f"low_expected={low_expected} decision_errors={decision_errors}; "
        f"P_ON_RESET_CLEAR_STORED_OFFSET_DECISION mismatch_count={reset_mismatches}; "
        f"P_DURING_AN_AUTO_ZERO_CLOCK_UPDATE mismatch_count={autozero_mismatches}; "
        f"P_DURING_AN_EVALUATION_CLOCK_UPDATE_WITH mismatch_count={evaluation_mismatches}; "
        f"P_DRIVE_DECISION_HIGH_FOR_CORRECTED_NONNEGATIVE mismatch_count={decision_mismatches}; "
        f"P_EXPOSE_STORED_OFFSET_ON_OFFSET_STORE mismatch_count={expose_mismatches}"
    )

CHECKER_ID = "v4_309_autozero_comparator_preamplifier"
CHECKER: Checker = check_v4_309_autozero_comparator_preamplifier
