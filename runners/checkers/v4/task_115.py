"""Task-specific checker for canonical v4 DUT 115."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import crossings, diagnostic, max_signal_value, pass_note, probe_time, require_signals, sample


PROPERTY_IDS = (
    "P_INITIAL_LOW",
    "P_RISING_EDGE_COUNT",
    "P_WRAP_MARKER",
    "P_NONWRAP_LOW",
    "P_PERIOD_FOUR",
)


def check_v3_two_bit_counter_marker(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clkin", "mc"}
    missing = require_signals(rows, required, "P_RISING_EDGE_COUNT")
    if missing:
        return False, missing

    vth = 0.5 * max_signal_value(rows, ["clkin", "mc"], default=1.0)
    rises = crossings(rows, "clkin", threshold=vth, direction="rising")
    if len(rises) < 4:
        return False, diagnostic(
            "P_RISING_EDGE_COUNT",
            "insufficient_events",
            expected="clkin_rising_count>=4",
            observed=f"clkin_rising_count={len(rises)}",
            event="clkin_rising_set",
        )

    initial = sample(rows, "mc", rows[0]["time"])
    if initial is None or abs(initial) > 0.08:
        return False, diagnostic(
            "P_INITIAL_LOW",
            "initial_state_mismatch",
            expected="mc=0",
            observed=f"mc={initial}" if initial is not None else "mc=unavailable",
            event="initial_observed_state",
        )

    count = 0
    checked = 0
    saw_marker_high = False
    saw_marker_low_after_high = False
    max_err = 0.0
    for index, edge_t in enumerate(rises):
        if count == 3:
            count = 0
            expected = 1.0
        else:
            count += 1
            expected = 0.0
        next_edge = rises[index + 1] if index + 1 < len(rises) else None
        probe_t = probe_time(rows, edge_t, next_edge, fraction=0.25)
        if probe_t is None:
            continue
        observed = sample(rows, "mc", probe_t)
        if observed is None:
            continue
        checked += 1
        max_err = max(max_err, abs(observed - expected))
        if expected > 0.5:
            saw_marker_high = True
        elif saw_marker_high:
            saw_marker_low_after_high = True
        if abs(observed - expected) > 0.08:
            return False, diagnostic(
                "P_PERIOD_FOUR" if expected > 0.5 else "P_NONWRAP_LOW",
                "marker_state_mismatch",
                expected=f"mc={expected:.1f}",
                observed=f"mc={observed:.3f},err={abs(observed - expected):.3f}",
                event=f"clkin_rising[{index}]",
            )
    if checked < 4:
        return False, diagnostic(
            "P_RISING_EDGE_COUNT",
            "insufficient_checks",
            expected="checked>=4",
            observed=f"checked={checked}",
            event="clkin_rising_set",
        )
    if not saw_marker_high:
        return False, diagnostic(
            "P_WRAP_MARKER",
            "marker_missing",
            expected="one_wrap_marker_high",
            observed="marker_high=False",
            event="clkin_rising_set",
        )
    if len(rises) >= 5 and not saw_marker_low_after_high:
        return False, diagnostic(
            "P_NONWRAP_LOW",
            "marker_return_mismatch",
            expected="marker_returns_low_after_wrap",
            observed="marker_return_low=False",
            event="clkin_rising_set",
        )
    detail = (
        f"edges={len(rises)} checked={checked} max_err={max_err:.4f} "
        f"marker_return_low={saw_marker_low_after_high}"
    )
    return True, pass_note(PROPERTY_IDS, detail)

CHECKER_ID = "v4_115_two_bit_counter_marker"
CHECKER: Checker = check_v3_two_bit_counter_marker
