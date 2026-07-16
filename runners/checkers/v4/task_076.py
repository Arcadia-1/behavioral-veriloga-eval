"""Task-specific checker for canonical v4 DUT 076."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import diagnostic, pass_note, require_signals


PROPERTY_IDS = (
    "P_ACTIVE_LOW_RESET",
    "P_FRAME_START",
    "P_TWO_CYCLE_BURST",
    "P_QUIET_REMAINDER",
    "P_FRAME_REPEAT",
    "P_OUTPUT_LEVELS",
)


def check_clk_burst_gen(rows: list[dict[str, float]]) -> tuple[bool, str]:
    missing = require_signals(rows, {"time", "CLK", "RST_N", "CLK_OUT"}, "P_ACTIVE_LOW_RESET")
    if missing is not None:
        return False, missing
    vth = 0.45
    reset_rows = [r for r in rows if r["RST_N"] <= vth]
    if not reset_rows:
        return False, diagnostic(
            "P_ACTIVE_LOW_RESET",
            "missing_event",
            expected="reset_rows>0",
            observed="reset_rows:0",
            event="full_trace",
        )
    reset_peak = max(r["CLK_OUT"] for r in reset_rows)
    if reset_peak > 0.12:
        return False, diagnostic(
            "P_ACTIVE_LOW_RESET",
            "value_mismatch",
            expected="CLK_OUT_peak<=0.12",
            observed=f"CLK_OUT_peak:{reset_peak:.3f}",
            event="RST_N_low",
        )
    post = [r for r in rows if r["RST_N"] > 0.45]
    if len(post) < 4:
        return False, diagnostic(
            "P_FRAME_START",
            "missing_event",
            expected="post_reset_samples>=4",
            observed=f"post_reset_samples:{len(post)}",
            event="RST_N_high",
        )

    times = [r["time"] for r in post]
    clk = [r["CLK"] for r in post]
    edge_idx = [i for i in range(1, len(post)) if clk[i - 1] < vth <= clk[i]]
    if len(edge_idx) < 16:
        return False, diagnostic(
            "P_FRAME_REPEAT",
            "missing_event",
            expected="post_reset_clk_edges>=16",
            observed=f"post_reset_clk_edges:{len(edge_idx)}",
            event="RST_N_high",
        )

    periods = [times[edge_idx[i + 1]] - times[edge_idx[i]] for i in range(len(edge_idx) - 1)]
    positive_periods = sorted(period for period in periods if period > 0)
    if not positive_periods:
        return False, diagnostic(
            "P_FRAME_START",
            "invalid_trace",
            expected="positive_clk_period",
            observed="positive_clk_period:none",
            event="post_reset_clk_edges",
        )
    period = positive_periods[len(positive_periods) // 2]

    def sample_at_or_after(target_t: float, limit_t: float | None = None) -> dict[str, float] | None:
        for row in post:
            t = row["time"]
            if t >= target_t and (limit_t is None or t < limit_t):
                return row
        return None

    high_phase_failures = 0
    low_phase_failures = 0
    checked_cycles = 0
    enabled_cycles = 0
    disabled_cycles = 0
    failure_notes: list[str] = []

    # Contract for the release task/testbench: div=8, pass cycles 0 and 1,
    # suppress cycles 2..7, then repeat. Sample away from transitions so the
    # checker is not sensitive to simulator breakpoint placement.
    for cycle_idx, edge in enumerate(edge_idx[:-1]):
        edge_t = times[edge]
        next_edge_t = times[edge_idx[cycle_idx + 1]]
        frame_pos = cycle_idx % 8
        should_pass = frame_pos < 2

        high_sample = sample_at_or_after(edge_t + 0.25 * period, next_edge_t)
        low_sample = sample_at_or_after(edge_t + 0.75 * period, next_edge_t)
        if high_sample is None or low_sample is None:
            continue

        checked_cycles += 1
        if should_pass:
            enabled_cycles += 1
            if high_sample["CLK_OUT"] <= vth:
                high_phase_failures += 1
                failure_notes.append(
                    diagnostic(
                        "P_TWO_CYCLE_BURST",
                        "value_mismatch",
                        expected=f"CLK_OUT>{vth:.3f}",
                        observed=f"CLK_OUT:{high_sample['CLK_OUT']:.3f}",
                        event=f"frame_cycle[{frame_pos}]",
                    )
                )
        else:
            disabled_cycles += 1
            if high_sample["CLK_OUT"] > vth:
                high_phase_failures += 1
                failure_notes.append(
                    diagnostic(
                        "P_QUIET_REMAINDER",
                        "value_mismatch",
                        expected="CLK_OUT<=0.45",
                        observed=f"CLK_OUT:{high_sample['CLK_OUT']:.3f}",
                        event=f"frame_cycle[{frame_pos}]",
                    )
                )
        if low_sample["CLK_OUT"] > vth:
            low_phase_failures += 1
            failure_notes.append(
                diagnostic(
                    "P_OUTPUT_LEVELS",
                    "value_mismatch",
                    expected="CLK_OUT_low_phase<=0.45",
                    observed=f"CLK_OUT:{low_sample['CLK_OUT']:.3f}",
                    event=f"frame_cycle[{frame_pos}]",
                )
            )
    if failure_notes:
        return False, " ".join(failure_notes[:5])

    ok = (
        checked_cycles >= 16
        and enabled_cycles >= 4
        and disabled_cycles >= 8
        and high_phase_failures == 0
        and low_phase_failures == 0
    )
    note = (
        f"burst_cycles_checked={checked_cycles} enabled_cycles={enabled_cycles} "
        f"disabled_cycles={disabled_cycles} high_phase_failures={high_phase_failures} "
        f"low_phase_failures={low_phase_failures} reset_peak={reset_peak:.3f}"
    )
    if not ok:
        return False, diagnostic(
            "P_FRAME_REPEAT",
            "missing_event",
            expected="checked>=16,enabled>=4,disabled>=8",
            observed=f"checked:{checked_cycles},enabled:{enabled_cycles},disabled:{disabled_cycles}",
            event="post_reset_frames",
        )
    return True, pass_note(PROPERTY_IDS, note)

CHECKER_ID = "v4_076_burst_clock_source"
CHECKER: Checker = check_clk_burst_gen
