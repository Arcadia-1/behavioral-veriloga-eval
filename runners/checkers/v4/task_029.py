"""Stimulus-relative checker for canonical v4 DUT 029."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import event_settle_delay, finish, missing_trace, row_at_or_after


PROPERTY_IDS = [
    "P_INITIAL_DECISION",
    "P_POSITIVE_SWITCH_THRESHOLD",
    "P_NEGATIVE_SWITCH_THRESHOLD",
    "P_HYSTERESIS_HOLD",
    "P_COMPLEMENTARY_RAIL_OUTPUT",
]


def _threshold_crossings(
    rows: list[dict[str, float]],
    *,
    threshold: float,
    rising: bool,
) -> list[float]:
    crossings: list[float] = []
    for index in range(1, len(rows)):
        previous = rows[index - 1]["vinp"] - rows[index - 1]["vinn"]
        current = rows[index]["vinp"] - rows[index]["vinn"]
        hit = previous <= threshold < current if rising else previous >= threshold > current
        if not hit:
            continue
        t0 = float(rows[index - 1]["time"])
        t1 = float(rows[index]["time"])
        fraction = 1.0 if current == previous else (threshold - previous) / (current - previous)
        crossings.append(t0 + fraction * (t1 - t0))
    return crossings


def _check_state(
    result,
    row: dict[str, float],
    *,
    state_high: bool,
    label: str,
) -> None:
    expected_p = row["vdd"] if state_high else row["vss"]
    expected_n = row["vss"] if state_high else row["vdd"]
    result.compare(
        expected=expected_p,
        observed=row["out_p"],
        tolerance=0.075,
        time_s=row["time"],
        label=f"{label}_out_p",
    )
    result.compare(
        expected=expected_n,
        observed=row["out_n"],
        tolerance=0.075,
        time_s=row["time"],
        label=f"{label}_out_n",
    )


def check_hysteresis_comparator(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vdd", "vss", "vinp", "vinn", "out_p", "out_n"}
    results, error = missing_trace(CHECKER_ID, rows, required, PROPERTY_IDS)
    if error is not None:
        return error
    by_id = {result.property_id: result for result in results}

    positive = _threshold_crossings(rows, threshold=0.005, rising=True)
    negative = _threshold_crossings(rows, threshold=-0.005, rising=False)
    events = sorted(
        [(time, True) for time in positive] + [(time, False) for time in negative],
        key=lambda item: item[0],
    )
    event_times = [time for time, _ in events]
    settle = event_settle_delay(event_times)

    first_event = event_times[0] if event_times else float(rows[-1]["time"])
    initial_time = float(rows[0]["time"]) + 0.50 * (first_event - float(rows[0]["time"]))
    initial = row_at_or_after(rows, initial_time)
    initial_diff = initial["vinp"] - initial["vinn"]
    initial_state = initial_diff > 0.005
    _check_state(by_id["P_INITIAL_DECISION"], initial, state_high=initial_state, label="initial")

    for event_time in positive:
        sample = row_at_or_after(rows, event_time + settle)
        _check_state(
            by_id["P_POSITIVE_SWITCH_THRESHOLD"],
            sample,
            state_high=True,
            label="positive_switch",
        )
    for event_time in negative:
        sample = row_at_or_after(rows, event_time + settle)
        _check_state(
            by_id["P_NEGATIVE_SWITCH_THRESHOLD"],
            sample,
            state_high=False,
            label="negative_switch",
        )

    state = initial_state
    event_cursor = 0
    stride = max(1, len(rows) // 240)
    hold_checks = 0
    rail_checks = 0
    for row in rows[::stride]:
        time_s = float(row["time"])
        while event_cursor < len(events) and events[event_cursor][0] <= time_s:
            state = events[event_cursor][1]
            event_cursor += 1
        if any(0.0 <= time_s - event_time <= settle for event_time in event_times):
            continue
        diff = row["vinp"] - row["vinn"]
        if -0.0045 < diff < 0.0045:
            hold_checks += 1
            _check_state(
                by_id["P_HYSTERESIS_HOLD"],
                row,
                state_high=state,
                label="hysteresis_hold",
            )
        rail_checks += 1
        _check_state(
            by_id["P_COMPLEMENTARY_RAIL_OUTPUT"],
            row,
            state_high=state,
            label="local_rails",
        )

    by_id["P_POSITIVE_SWITCH_THRESHOLD"].condition(
        len(positive) >= 1,
        expected="positive_threshold_crossing_exercised",
        observed=f"crossings={len(positive)}",
        time_s=rows[-1]["time"],
        gap=max(0, 1 - len(positive)),
    )
    by_id["P_NEGATIVE_SWITCH_THRESHOLD"].condition(
        len(negative) >= 1,
        expected="negative_threshold_crossing_exercised",
        observed=f"crossings={len(negative)}",
        time_s=rows[-1]["time"],
        gap=max(0, 1 - len(negative)),
    )
    by_id["P_HYSTERESIS_HOLD"].condition(
        hold_checks >= 4,
        expected="interior_band_observed_in_both_sweeps",
        observed=f"hold_checks={hold_checks}",
        time_s=rows[-1]["time"],
        gap=max(0, 4 - hold_checks),
    )
    return finish(
        CHECKER_ID,
        results,
        coverage=(
            f"positive_crossings={len(positive)} negative_crossings={len(negative)} "
            f"hold_checks={hold_checks} rail_checks={rail_checks} settle_s={settle:.6g}"
        ),
    )


CHECKER_ID = "v4_029_hysteresis_comparator"
CHECKER: Checker = check_hysteresis_comparator
