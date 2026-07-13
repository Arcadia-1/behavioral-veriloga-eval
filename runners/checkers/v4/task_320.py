"""Task-specific checker for canonical v4 DUT 320."""
from __future__ import annotations

from checkers.api import Checker
VCM = 0.45
VDD = 0.9
VTH = 0.45

def _high(row: dict[str, float], name: str, thr: float = VTH) -> bool:
    return float(row.get(name, 0.0)) > thr

def _rising(prev: float, now: float, thr: float = VTH) -> bool:
    return now > thr and prev <= thr

def _code(row: dict[str, float], bits: list[str]) -> int:
    return sum((1 << i) for i, b in enumerate(bits) if _high(row, b))

def _missing(rows: list[dict[str, float]], required: set[str]) -> list[str]:
    if not rows:
        return sorted(required)
    return sorted(required - set(rows[0].keys()))

def check_v4_320_code_dependent_dac_buffer_settling(rows: list[dict[str, float]]) -> tuple[bool, str]:
    req = {
        "time", "clk", "rst", "enable", "code_0", "code_1", "code_2", "code_3",
        "vout", "target_dbg", "settling_metric", "settled",
    }
    miss = _missing(rows, req)
    if miss:
        return False, f"v4_320 missing_signals={','.join(miss)}"
    prev_clk = float(rows[0]["clk"])
    checked = metric_errors = settled_errors = clear_errors = target_errors = 0
    step_errors = edge_update_errors = early_settled_errors = missing_settled_errors = 0
    reset_clear = disabled_clear = False
    settled_seen = False
    ever_enabled = False
    sample_pending = False
    pending_code = 0
    pending_pre_vout = VCM
    sampled_vout: float | None = None
    low_metric_updates = 0
    prev_row = rows[0]
    codes: set[int] = set()
    for row in rows:
        clk = float(row["clk"])
        rst = _high(row, "rst")
        enabled = _high(row, "enable") and not rst
        if not enabled:
            clear = (
                abs(float(row["vout"]) - VCM) < 0.10
                and abs(float(row["settling_metric"])) < 0.08
                and not _high(row, "settled")
            )
            if rst and clear:
                reset_clear = True
            if ever_enabled and (not _high(row, "enable")) and clear:
                disabled_clear = True
            if (rst or (ever_enabled and not _high(row, "enable") and disabled_clear)) and not clear:
                clear_errors += 1
            sample_pending = False
            sampled_vout = None
            low_metric_updates = 0
            prev_clk = clk
            prev_row = row
            continue
        ever_enabled = True
        if _rising(prev_clk, clk):
            sample_pending = True
            pending_code = _code(row, ["code_0", "code_1", "code_2", "code_3"])
            pending_pre_vout = float(row["vout"])
        elif sample_pending and prev_clk > VTH and clk <= VTH:
            # Sample the end of the high phase, after the public transition time,
            # instead of coupling the checker to a deck-specific time offset.
            sample_pending = False
            checked += 1
            codes.add(pending_code)
            target = VDD * pending_code / 15.0
            if abs(float(prev_row["target_dbg"]) - target) > 0.10:
                target_errors += 1
            err = abs(float(prev_row["vout"]) - target)
            if sampled_vout is not None and abs(float(prev_row["vout"]) - sampled_vout) > 0.10:
                step_errors += 1
            if abs(pending_pre_vout - target) > 0.025:
                progress = abs(pending_pre_vout - target) - err
                if progress < 0.03:
                    edge_update_errors += 1
            sampled_vout = float(prev_row["vout"])
            if abs(float(prev_row["settling_metric"]) - err) > 0.05:
                metric_errors += 1
            settled = _high(prev_row, "settled")
            if settled and float(prev_row["settling_metric"]) > 0.025:
                settled_errors += 1
            if float(prev_row["settling_metric"]) <= 0.012:
                low_metric_updates += 1
            else:
                low_metric_updates = 0
            if settled and low_metric_updates < 2:
                early_settled_errors += 1
            if low_metric_updates >= 2 and not settled:
                missing_settled_errors += 1
            settled_seen = settled_seen or settled
        prev_clk = clk
        prev_row = row
    ok = (
        checked >= 8
        and reset_clear
        and disabled_clear
        and len(codes) >= 3
        and settled_seen
        and metric_errors <= max(2, checked // 4)
        and settled_errors <= max(2, checked // 5)
        and target_errors <= max(3, checked // 3)
        and step_errors <= 1
        and edge_update_errors <= 1
        and early_settled_errors == 0
        and missing_settled_errors <= 1
    )
    clear_mismatches = int(not reset_clear) + int(not disabled_clear)
    expose_mismatches = target_errors + metric_errors
    settled_mismatches = (
        settled_errors
        + early_settled_errors
        + missing_settled_errors
        + int(not settled_seen)
    )
    return ok, (
        f"v4_320 checked={checked} codes={sorted(codes)} reset_clear={reset_clear} "
        f"disabled_clear={disabled_clear} metric_errors={metric_errors} "
        f"settled_errors={settled_errors} target_errors={target_errors} clear_errors={clear_errors} "
        f"step_errors={step_errors} edge_update_errors={edge_update_errors} settled_seen={settled_seen} "
        f"early_settled_errors={early_settled_errors} missing_settled_errors={missing_settled_errors}; "
        f"P_ON_RESET_OR_WHEN_DISABLED_CLEAR mismatch_count={clear_mismatches}; "
        f"P_ON_EACH_ENABLED_RISING_CLK_EDGE mismatch_count={edge_update_errors}; "
        f"P_APPLY_A_CODE_DEPENDENT_SETTLING_STEP mismatch_count={step_errors}; "
        f"P_EXPOSE_THE_CURRENT_TARGET_ON_TARGET mismatch_count={expose_mismatches}; "
        f"P_ASSERT_SETTLED_AFTER_THE_REMAINING_ERROR mismatch_count={settled_mismatches}"
    )

CHECKER_ID = "v4_320_code_dependent_dac_buffer_settling"
CHECKER: Checker = check_v4_320_code_dependent_dac_buffer_settling
