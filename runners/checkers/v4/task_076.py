"""Task-specific checker for canonical v4 DUT 076."""
from __future__ import annotations

from ..api import Checker
def check_clk_burst_gen(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows or not {"CLK", "RST_N", "CLK_OUT"}.issubset(rows[0]):
        return False, "missing CLK/RST_N/CLK_OUT"
    vth = 0.45
    reset_rows = [r for r in rows if r["RST_N"] <= vth]
    if not reset_rows:
        return False, "active_low_reset_not_observable observed=reset_rows:0 expected=>0 window=full_trace"
    reset_peak = max(r["CLK_OUT"] for r in reset_rows)
    if reset_peak > 0.12:
        return False, f"reset_not_low observed=CLK_OUT_peak:{reset_peak:.3f} expected<=0.12 window=RST_N_low"
    post = [r for r in rows if r["RST_N"] > 0.45]
    if len(post) < 4:
        return False, "no post-reset samples"

    times = [r["time"] for r in post]
    clk = [r["CLK"] for r in post]
    edge_idx = [i for i in range(1, len(post)) if clk[i - 1] < vth <= clk[i]]
    if len(edge_idx) < 16:
        return False, f"too_few_post_reset_clk_edges={len(edge_idx)}"

    periods = [times[edge_idx[i + 1]] - times[edge_idx[i]] for i in range(len(edge_idx) - 1)]
    positive_periods = sorted(period for period in periods if period > 0)
    if not positive_periods:
        return False, "cannot_estimate_clk_period"
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
                    f"burst_high observed={high_sample['CLK_OUT']:.3f} expected=>{vth:.3f} "
                    f"window=cycle{cycle_idx}/frame{frame_pos}"
                )
        else:
            disabled_cycles += 1
            if high_sample["CLK_OUT"] > vth:
                high_phase_failures += 1
                failure_notes.append(
                    f"quiet_high observed={high_sample['CLK_OUT']:.3f} expected<=0.45 "
                    f"window=cycle{cycle_idx}/frame{frame_pos}"
                )
        if low_sample["CLK_OUT"] > vth:
            low_phase_failures += 1
            failure_notes.append(
                f"low_phase observed={low_sample['CLK_OUT']:.3f} expected<=0.45 "
                f"window=cycle{cycle_idx}/frame{frame_pos}"
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
    return ok, (
        f"burst_cycles_checked={checked_cycles} enabled_cycles={enabled_cycles} "
        f"disabled_cycles={disabled_cycles} high_phase_failures={high_phase_failures} "
        f"low_phase_failures={low_phase_failures} reset_peak={reset_peak:.3f}"
    )

CHECKER_ID = "v4_076_burst_clock_source"
CHECKER: Checker = check_clk_burst_gen
