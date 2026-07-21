"""Task-specific checker for canonical v4 DUT 305."""
from __future__ import annotations

from ..api import Checker
from ..common.v4_topup import (
    _v4_topup_clip01,
    _v4_topup_logic_high,
)
from ..common.relative_events import event_period, rising_edges, sample_after_event, sample_step

def check_v4_305_capacitive_feedback_amplifier_macro(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1003 empty_trace"
    active_edges = inactive_edges = 0
    sample_errors = gain_errors = settled_errors = 0
    hold_checked = hold_errors = 0
    codes_seen: set[int] = set()
    settled_seen = False
    settle_count = 0
    previous_target = 0.45
    edges = rising_edges(rows, "clk")
    period = event_period(rows, "clk")
    guard = max(period * 0.15, sample_step(rows) * 3.0)

    for index, edge in enumerate(edges):
        edge_index = next((i for i, row in enumerate(rows) if float(row["time"]) >= edge), None)
        edge_row = rows[max(0, edge_index - 1)] if edge_index is not None else None
        post = sample_after_event(rows, edge, clock_signal="clk", fraction_of_period=0.15)
        if edge_row is None or post is None:
            continue
        active = _v4_topup_logic_high(edge_row, "enable") and not _v4_topup_logic_high(edge_row, "rst")
        if active:
            code = int(_v4_topup_logic_high(edge_row, "gain_0")) + 2 * int(_v4_topup_logic_high(edge_row, "gain_1"))
            sample_value = float(edge_row["vin"])
            expected_gain = 1.0 + 0.75 * code
            expected_vout = _v4_topup_clip01(0.45 + expected_gain * (sample_value - 0.45))
            settle_count = settle_count + 1 if abs(previous_target - expected_vout) < 10e-3 else 0
            expected_settled = settle_count >= 2
            previous_target = expected_vout
            active_edges += 1
            codes_seen.add(code)
        else:
            sample_value = 0.0
            expected_vout = 0.45
            expected_settled = False
            settle_count = 0
            previous_target = expected_vout
            inactive_edges += 1

        if abs(float(post["sampled_metric"]) - sample_value) > 0.08:
            sample_errors += 1
        if abs(float(post["vout"]) - expected_vout) > 0.10:
            gain_errors += 1
        observed_settled = float(post["settled"]) > 0.45
        if observed_settled != expected_settled:
            settled_errors += 1
        settled_seen = settled_seen or (active and observed_settled)

        next_edge = edges[index + 1] if index + 1 < len(edges) else float(rows[-1]["time"])
        for hold_row in rows:
            hold_time = float(hold_row["time"])
            if hold_time < edge + guard or hold_time >= next_edge - sample_step(rows) * 2.0:
                continue
            hold_checked += 1
            if (
                abs(float(hold_row["sampled_metric"]) - sample_value) > 0.08
                or abs(float(hold_row["vout"]) - expected_vout) > 0.10
                or (float(hold_row["settled"]) > 0.45) != expected_settled
            ):
                hold_errors += 1

    allowed_hold_errors = max(6, hold_checked // 50)
    ok = (
        active_edges >= 8
        and inactive_edges >= 1
        and len(codes_seen) >= 3
        and settled_seen
        and sample_errors <= 1
        and gain_errors <= 1
        and settled_errors <= 1
        and hold_checked >= 20
        and hold_errors <= allowed_hold_errors
    )
    diagnostics = {
        "P_ON_RESET_OR_WHEN_DISABLED_DRIVE": int(inactive_edges < 1) + sample_errors + gain_errors,
        "P_ON_EACH_RISING_CLK_EDGE_WHILE": max(0, sample_errors - 1),
        "P_DRIVE_SAMPLED_METRIC_WITH_THE_HELD": max(0, hold_errors - allowed_hold_errors),
        "P_MOVE_VOUT_TOWARD_VCM_GAIN_SAMPLE": max(0, gain_errors - 1),
        "P_ASSERT_SETTLED_AFTER_THE_OUTPUT_HAS": int(not settled_seen) + max(0, settled_errors - 1),
        "P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE": 0,
    }
    return ok, (
        f"v4_305 active_edges={active_edges} inactive_edges={inactive_edges} codes={sorted(codes_seen)} "
        f"settled_seen={settled_seen} sample_errors={sample_errors} gain_errors={gain_errors} "
        f"settled_errors={settled_errors} hold_checked={hold_checked} hold_errors={hold_errors}; "
        + "; ".join(f"{key} mismatch_count={value}" for key, value in diagnostics.items())
    )

CHECKER_ID = "v4_305_capacitive_feedback_amplifier_macro"
CHECKER: Checker = check_v4_305_capacitive_feedback_amplifier_macro
