"""Task-specific checker for canonical v4 DUT 309."""
from __future__ import annotations

from ..api import Checker
from ..common.v4_topup import _v4_topup_clip01, _v4_topup_logic_high
from ..common.relative_events import event_period, rising_edges, sample_after_event, sample_step

def check_v4_309_autozero_comparator_preamplifier(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1007 empty_trace"
    edges = rising_edges(rows, "clk")
    period = event_period(rows, "clk")
    guard = max(period * 0.15, sample_step(rows) * 3.0)
    expected_offset = 0.45
    expected_decision = False
    expected_ready = False
    reset_edges = autozero_edges = evaluation_edges = 0
    edge_errors = hold_checked = hold_errors = order_errors = 0
    captured_offsets: list[float] = []
    high_expected = low_expected = False
    for index, edge in enumerate(edges):
        edge_index = next((i for i, row in enumerate(rows) if float(row["time"]) >= edge), None)
        edge_row = rows[max(0, edge_index - 1)] if edge_index is not None else None
        post = sample_after_event(rows, edge, clock_signal="clk", fraction_of_period=0.15)
        if edge_row is None or post is None:
            continue
        decision_check_required = True
        if _v4_topup_logic_high(edge_row, "rst"):
            expected_offset = 0.45
            expected_decision = False
            expected_ready = False
            reset_edges += 1
        elif _v4_topup_logic_high(edge_row, "az_en"):
            stored = float(edge_row["vinp"]) - float(edge_row["vinn"])
            expected_offset = _v4_topup_clip01(0.45 + stored)
            expected_ready = True
            autozero_edges += 1
            captured_offsets.append(expected_offset)
        elif _v4_topup_logic_high(edge_row, "eval_en"):
            evaluation_edges += 1
            if not expected_ready:
                order_errors += 1
            else:
                corrected = (
                    float(edge_row["vinp"])
                    - float(edge_row["vinn"])
                    - (expected_offset - 0.45)
                )
                expected_decision = corrected >= 0.0
                decision_check_required = abs(corrected) > 10e-3
                high_expected = high_expected or expected_decision
                low_expected = low_expected or not expected_decision

        edge_mismatch = (
            abs(float(post["offset_store"]) - expected_offset) > 0.08
            or (float(post["ready"]) > 0.45) != expected_ready
            or (
                decision_check_required
                and (float(post["decision"]) > 0.45) != expected_decision
            )
        )
        if edge_mismatch:
            edge_errors += 1
        if not decision_check_required:
            expected_decision = float(post["decision"]) > 0.45

        next_edge = edges[index + 1] if index + 1 < len(edges) else float(rows[-1]["time"])
        for hold_row in rows:
            hold_time = float(hold_row["time"])
            if hold_time < edge + guard or hold_time >= next_edge - sample_step(rows) * 2.0:
                continue
            if _v4_topup_logic_high(hold_row, "rst"):
                continue
            hold_checked += 1
            if (
                abs(float(hold_row["offset_store"]) - expected_offset) > 0.08
                or (float(hold_row["ready"]) > 0.45) != expected_ready
                or (float(hold_row["decision"]) > 0.45) != expected_decision
            ):
                hold_errors += 1

    offset_span = (
        max(captured_offsets) - min(captured_offsets)
        if len(captured_offsets) >= 2
        else 0.0
    )
    allowed_hold_errors = max(4, hold_checked // 100)
    ok = (
        reset_edges >= 1
        and autozero_edges >= 2
        and evaluation_edges >= 4
        and order_errors == 0
        and edge_errors == 0
        and hold_checked >= 20
        and hold_errors <= allowed_hold_errors
        and offset_span > 0.04
        and high_expected
        and low_expected
    )
    diagnostics = {
        "P_ON_RESET_CLEAR_STORED_OFFSET_DECISION": int(reset_edges < 1) + edge_errors,
        "P_DURING_AN_AUTO_ZERO_CLOCK_UPDATE": int(autozero_edges < 2) + int(offset_span <= 0.04),
        "P_DURING_AN_EVALUATION_CLOCK_UPDATE_WITH": int(evaluation_edges < 4) + order_errors,
        "P_DRIVE_DECISION_HIGH_FOR_CORRECTED_NONNEGATIVE": edge_errors,
        "P_EXPOSE_STORED_OFFSET_ON_OFFSET_STORE": int(offset_span <= 0.04) + max(0, hold_errors - allowed_hold_errors),
        "P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE": 0,
    }
    return ok, (
        f"v4_309 reset_edges={reset_edges} autozero_edges={autozero_edges} evaluation_edges={evaluation_edges} "
        f"order_errors={order_errors} edge_errors={edge_errors} hold_checked={hold_checked} hold_errors={hold_errors} "
        f"offset_span={offset_span:.3f} high_expected={high_expected} low_expected={low_expected}; "
        + "; ".join(f"{key} mismatch_count={value}" for key, value in diagnostics.items())
    )

CHECKER_ID = "v4_309_autozero_comparator_preamplifier"
CHECKER: Checker = check_v4_309_autozero_comparator_preamplifier
