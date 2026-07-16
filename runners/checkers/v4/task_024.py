"""Stimulus-relative checker for canonical v4 DUT 024."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import event_settle_delay, finish, missing_trace, row_at_or_after


PROPERTY_IDS = [
    "P_RISING_EDGE_SAMPLE",
    "P_INTERSAMPLE_HOLD",
    "P_NO_HIGH_PHASE_TRACKING",
    "P_LOCAL_RAIL_REFERENCE",
]


def _relative_crossings(
    rows: list[dict[str, float]],
    *,
    rising: bool,
    threshold: float = 0.45,
) -> list[int]:
    indices: list[int] = []
    for index in range(1, len(rows)):
        previous = rows[index - 1]["clk"] - rows[index - 1]["vss"]
        current = rows[index]["clk"] - rows[index]["vss"]
        hit = previous <= threshold < current if rising else previous >= threshold > current
        if hit:
            indices.append(index)
    return indices


def check_clocked_sample_and_hold(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vdd", "vss", "in", "clk", "out"}
    results, error = missing_trace(CHECKER_ID, rows, required, PROPERTY_IDS)
    if error is not None:
        return error
    by_id = {result.property_id: result for result in results}

    rising = _relative_crossings(rows, rising=True)
    falling = _relative_crossings(rows, rising=False)
    edge_times = [float(rows[index]["time"]) for index in rising]
    settle = event_settle_delay(edge_times)

    for index in rising:
        edge = rows[index]
        event_time = float(edge["time"])
        sample = row_at_or_after(rows, event_time + settle)
        local_span = sample["vdd"] - sample["vss"]
        absolute_gap = max(
            sample["vss"] - sample["out"],
            sample["out"] - sample["vdd"],
            0.0,
        )
        branch_gap = max(-sample["out"], sample["out"] - local_span, 0.0)
        by_id["P_RISING_EDGE_SAMPLE"].compare(
            expected=edge["in"],
            observed=sample["out"],
            tolerance=0.022,
            time_s=sample["time"],
            label="sampled_voltage",
        )
        by_id["P_LOCAL_RAIL_REFERENCE"].condition(
            absolute_gap <= 0.025 or branch_gap <= 0.025,
            expected="out_within_local_rails_in_trace_voltage_encoding",
            observed=(
                f"vss={sample['vss']:.6g},out={sample['out']:.6g},"
                f"vdd={sample['vdd']:.6g},local_span={local_span:.6g}"
            ),
            time_s=sample["time"],
            gap=min(absolute_gap, branch_gap),
        )

    for left, right in zip(edge_times, edge_times[1:]):
        spacing = right - left
        if spacing <= 2.5 * settle:
            continue
        early = row_at_or_after(rows, left + max(settle, 0.28 * spacing))
        late = row_at_or_after(rows, left + 0.80 * spacing)
        by_id["P_INTERSAMPLE_HOLD"].compare(
            expected=early["out"],
            observed=late["out"],
            tolerance=0.012,
            time_s=late["time"],
            label="held_out",
        )

    fall_cursor = 0
    high_phase_checks = 0
    for rise_index in rising:
        while fall_cursor < len(falling) and falling[fall_cursor] <= rise_index:
            fall_cursor += 1
        if fall_cursor >= len(falling):
            break
        fall_index = falling[fall_cursor]
        left = float(rows[rise_index]["time"])
        right = float(rows[fall_index]["time"])
        if right - left <= 2.5 * settle:
            continue
        early = row_at_or_after(rows, left + max(settle, 0.30 * (right - left)))
        late = row_at_or_after(rows, left + 0.82 * (right - left))
        if abs(late["in"] - early["in"]) < 0.004:
            continue
        high_phase_checks += 1
        by_id["P_NO_HIGH_PHASE_TRACKING"].compare(
            expected=early["out"],
            observed=late["out"],
            tolerance=0.012,
            time_s=late["time"],
            label="high_phase_out",
        )

    by_id["P_RISING_EDGE_SAMPLE"].condition(
        len(rising) >= 4,
        expected="at_least_4_rising_edge_samples",
        observed=f"rising_edges={len(rising)}",
        time_s=edge_times[-1] if edge_times else 0.0,
        gap=max(0, 4 - len(rising)),
    )
    by_id["P_INTERSAMPLE_HOLD"].condition(
        max(0, len(rising) - 1) >= 3,
        expected="at_least_3_hold_intervals",
        observed=f"hold_intervals={max(0, len(rising) - 1)}",
        time_s=edge_times[-1] if edge_times else 0.0,
        gap=max(0, 4 - len(rising)),
    )
    by_id["P_NO_HIGH_PHASE_TRACKING"].condition(
        high_phase_checks >= 2,
        expected="at_least_2_high_phase_input_changes",
        observed=f"high_phase_changes={high_phase_checks}",
        time_s=edge_times[-1] if edge_times else 0.0,
        gap=max(0, 2 - high_phase_checks),
    )

    return finish(
        CHECKER_ID,
        results,
        coverage=(
            f"rising_edges={len(rising)} high_phase_changes={high_phase_checks} "
            f"settle_s={settle:.6g}"
        ),
    )


CHECKER_ID = "v4_024_clocked_sample_and_hold"
CHECKER: Checker = check_clocked_sample_and_hold
