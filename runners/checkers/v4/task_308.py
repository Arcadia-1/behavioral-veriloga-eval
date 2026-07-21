"""Task-specific checker for canonical v4 DUT 308."""
from __future__ import annotations

from ..api import Checker
from ..common.v4_topup import _v4_topup_clip01, _v4_topup_logic_high
from ..common.relative_events import event_period, rising_edges, sample_after_event, sample_step

def check_v4_308_correlated_double_sampler_offset_cancel(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1006 empty_trace"
    edges = rising_edges(rows, "clk")
    period = event_period(rows, "clk")
    guard = max(period * 0.15, sample_step(rows) * 3.0)
    reset_sample = 0.45
    expected_vout = 0.45
    expected_offset = 0.0
    expected_valid = False
    have_reset_sample = False
    reset_edges = reset_capture_edges = signal_edges = 0
    edge_errors = hold_checked = hold_errors = order_errors = 0
    captured_reset_values: list[float] = []
    polarity_pos = polarity_neg = False
    for index, edge in enumerate(edges):
        edge_index = next((i for i, row in enumerate(rows) if float(row["time"]) >= edge), None)
        edge_row = rows[max(0, edge_index - 1)] if edge_index is not None else None
        post = sample_after_event(rows, edge, clock_signal="clk", fraction_of_period=0.15)
        if edge_row is None or post is None:
            continue
        if _v4_topup_logic_high(edge_row, "rst"):
            reset_sample = 0.45
            expected_vout = 0.45
            expected_offset = 0.0
            expected_valid = False
            have_reset_sample = False
            reset_edges += 1
        elif _v4_topup_logic_high(edge_row, "sample_reset"):
            reset_sample = float(edge_row["vin"])
            have_reset_sample = True
            reset_capture_edges += 1
            captured_reset_values.append(reset_sample)
        elif _v4_topup_logic_high(edge_row, "sample_signal"):
            signal_edges += 1
            if not have_reset_sample:
                order_errors += 1
            else:
                signal_value = float(edge_row["vin"])
                expected_vout = _v4_topup_clip01(0.45 + signal_value - reset_sample)
                expected_offset = _v4_topup_clip01(reset_sample)
                expected_valid = True
                polarity_pos = polarity_pos or signal_value > reset_sample + 0.04
                polarity_neg = polarity_neg or signal_value < reset_sample - 0.04

        if (
            abs(float(post["vout"]) - expected_vout) > 0.10
            or abs(float(post["offset_dbg"]) - expected_offset) > 0.08
            or (float(post["valid"]) > 0.45) != expected_valid
        ):
            edge_errors += 1

        next_edge = edges[index + 1] if index + 1 < len(edges) else float(rows[-1]["time"])
        for hold_row in rows:
            hold_time = float(hold_row["time"])
            if hold_time < edge + guard or hold_time >= next_edge - sample_step(rows) * 2.0:
                continue
            hold_checked += 1
            if (
                abs(float(hold_row["vout"]) - expected_vout) > 0.10
                or abs(float(hold_row["offset_dbg"]) - expected_offset) > 0.08
                or (float(hold_row["valid"]) > 0.45) != expected_valid
            ):
                hold_errors += 1

    reset_span = (
        max(captured_reset_values) - min(captured_reset_values)
        if len(captured_reset_values) >= 2
        else 0.0
    )
    allowed_hold_errors = max(4, hold_checked // 100)
    ok = (
        reset_edges >= 1
        and reset_capture_edges >= 2
        and signal_edges >= 2
        and order_errors == 0
        and edge_errors == 0
        and hold_checked >= 20
        and hold_errors <= allowed_hold_errors
        and polarity_pos
        and polarity_neg
        and reset_span > 0.12
    )
    diagnostics = {
        "P_ON_RESET_CLEAR_RESET_SAMPLE_SIGNAL": int(reset_edges < 1) + edge_errors,
        "P_ON_A_RISING_CLK_EDGE_WITH": int(reset_capture_edges < 2) + int(reset_span <= 0.12),
        "P_ON_A_LATER_RISING_CLK_EDGE": int(signal_edges < 2) + order_errors,
        "P_DRIVE_VOUT_AS_VCM_PLUS_THE": edge_errors + max(0, hold_errors - allowed_hold_errors),
        "P_EXPOSE_THE_RESET_SAMPLE_ON_OFFSET": edge_errors + int(reset_span <= 0.12),
        "P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE": 0,
    }
    return ok, (
        f"v4_308 reset_edges={reset_edges} reset_capture_edges={reset_capture_edges} signal_edges={signal_edges} "
        f"order_errors={order_errors} edge_errors={edge_errors} hold_checked={hold_checked} hold_errors={hold_errors} "
        f"polarity_pos={polarity_pos} polarity_neg={polarity_neg} reset_span={reset_span:.3f}; "
        + "; ".join(f"{key} mismatch_count={value}" for key, value in diagnostics.items())
    )

CHECKER_ID = "v4_308_correlated_double_sampler_offset_cancel"
CHECKER: Checker = check_v4_308_correlated_double_sampler_offset_cancel
