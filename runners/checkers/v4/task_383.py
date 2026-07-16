"""Task-specific checker for canonical v4 DUT 383."""
from __future__ import annotations

from ..api import Checker


def _level(row: dict[str, float], name: str, threshold: float = 0.45) -> bool | None:
    value = float(row.get(name, 0.0))
    if 0.1 < value < 0.8:
        return None
    return value > threshold


def _property_note(property_id: str, mismatch_count: int, expected: str, observed: str) -> str:
    return (
        f"{property_id} mismatch_count={mismatch_count} "
        f"expected={expected} observed={observed}"
    )

def check_v4_942_fixed_frequency_oscillator_source(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, _property_note("P_TRACE_CONTRACT", 1, "non_empty_trace", "empty_trace")
    checked = metric_errors = clear_errors = 0
    reset_clear = disabled_clear = osc_activity = valid_seen = reenable_seen = False
    osc_vals: list[float] = []
    previous_enable: bool | None = None
    previous_osc = float(rows[0].get("osc_out", 0.0))
    saw_inactive = False
    pending_enable_rises: list[float] = []
    startup_delay: float | None = None
    restart_delay: float | None = None
    for index, row in enumerate(rows):
        t = float(row["time"])
        rst = _level(row, "rst")
        enable = _level(row, "enable")
        if rst is None or enable is None:
            continue
        enabled = enable and not rst
        if previous_enable is not None and not previous_enable and enable and saw_inactive:
            pending_enable_rises.append(t)
            reenable_seen = True
        previous_enable = enable
        if not enabled:
            clear = row["osc_out"] < 0.12 and row["period_metric"] < 0.08 and row["valid"] < 0.10
            if index % 6 == 0:
                if rst and clear:
                    reset_clear = True
                if not rst and not enable and clear:
                    disabled_clear = True
                if not clear:
                    clear_errors += 1
            saw_inactive = True
            previous_osc = float(row["osc_out"])
            continue
        osc = float(row["osc_out"])
        if index % 6 == 0:
            osc_vals.append(osc)
        # Detect the settled high side of the transition rather than relying
        # on one exact waveform sample; this remains stable under time scaling.
        if previous_osc < 0.65 <= osc and pending_enable_rises:
            rise_time = pending_enable_rises.pop(0)
            delay = t - rise_time
            if startup_delay is None:
                startup_delay = delay
            elif restart_delay is None:
                restart_delay = delay
        if index % 6 == 0:
            valid_seen = valid_seen or bool(_level(row, "valid"))
            checked += 1
            if abs(float(row["period_metric"]) - 0.45) > 0.10:
                metric_errors += 1
        previous_osc = osc
    osc_activity = bool(osc_vals) and max(osc_vals) > 0.65 and min(osc_vals) < 0.20
    # The controller resets phase on a timer tick, so the first edge may move
    # within one transition interval when the stimulus edge is shifted.  Keep
    # the tolerance relative to the observed startup delay; a materially
    # different restart edge remains a semantic phase-reset failure.
    timing_tolerance = 0.15 * startup_delay if startup_delay is not None else 0.0
    restart_timing_ok = (
        startup_delay is not None
        and restart_delay is not None
        and abs(restart_delay - startup_delay) <= timing_tolerance
    )
    timing_errors = int(not reenable_seen) + int(not restart_timing_ok)
    ok = (
        checked >= 12
        and reset_clear
        and disabled_clear
        and timing_errors == 0
        and osc_activity
        and valid_seen
        and metric_errors <= 4
        and clear_errors <= 4
    )
    notes = [
        _property_note(
            "P_RESET_DISABLE_CLEAR",
            max(0, clear_errors - 4) + int(not reset_clear) + int(not disabled_clear),
            "clear_on_reset_and_disable",
            f"reset_clear={reset_clear},disabled_clear={disabled_clear},raw_clear_errors={clear_errors}",
        ),
        _property_note("P_PERIOD_METRIC", max(0, metric_errors - 4), "period_metric=0.45_after_cycle", f"checked={checked},raw_errors={metric_errors}"),
        _property_note("P_OSCILLATOR_ACTIVITY", int(not osc_activity), "osc_out_has_low_high_activity", str(osc_activity)),
        _property_note("P_VALID_AFTER_CYCLE", int(not valid_seen), "valid_asserted_after_cycle", str(valid_seen)),
        _property_note(
            "P_RELATIVE_RESTART_PHASE",
            timing_errors,
            "restart_delay_matches_initial_enable_delay",
            f"startup_delay={startup_delay},restart_delay={restart_delay}",
        ),
    ]
    return ok, "; ".join(notes)

CHECKER_ID = "v4_383_fixed_frequency_oscillator_source"
CHECKER: Checker = check_v4_942_fixed_frequency_oscillator_source
