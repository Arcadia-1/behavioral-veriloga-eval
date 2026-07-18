"""Task-specific checker for canonical v4 DUT 314."""
from __future__ import annotations

from ..api import Checker
def check_v4_314_hysteretic_window_comparator(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {
        "time", "vin", "rst", "enable", "low_trip", "high_trip",
        "inside_flag", "state_metric", "toggled",
    }
    if not rows:
        return False, "v4_314 missing_columns=" + ",".join(sorted(required))
    missing = sorted(required - set(rows[0]))
    if missing:
        return False, "v4_314 missing_columns=" + ",".join(missing)

    ordered = sorted(rows, key=lambda row: float(row["time"]))
    state = False
    previous_reset = float(ordered[0]["rst"]) > 0.45
    previous_enabled = float(ordered[0]["enable"]) > 0.45
    hyst = 10e-3
    band_margin = 1e-3
    expected_toggle_times: list[float] = []
    toggle_seen: list[bool] = []
    pending_toggle: int | None = None
    last_semantic_change_index = 0
    settle_samples = 8
    checked = state_errors = metric_errors = clear_errors = 0
    reset_samples = disabled_samples = 0
    inside_seen = outside_seen = False
    low_hold_seen = high_hold_seen = False
    first_error = ""

    def remember_error(kind: str, row: dict[str, float], expected: float, observed: float, extra: str = "") -> None:
        nonlocal first_error
        if first_error:
            return
        first_error = (
            f"v4_314_{kind} time={float(row['time']):.6e} vin={float(row['vin']):.6g} "
            f"low_trip={float(row['low_trip']):.6g} high_trip={float(row['high_trip']):.6g} "
            f"expected={expected:.6g} observed={observed:.6g} "
            f"mismatch={abs(observed - expected):.6g} {extra}"
        ).rstrip()

    def stable_output(index: int) -> bool:
        if index < 2:
            return False
        names = ("inside_flag", "state_metric")
        for current in range(index - 1, index + 1):
            previous = ordered[current - 1]
            row = ordered[current]
            if any(abs(float(row[name]) - float(previous[name])) > 1e-4 for name in names):
                return False
        return True

    for index, row in enumerate(ordered):
        t = float(row["time"])
        reset = float(row["rst"]) > 0.45
        enabled = float(row["enable"]) > 0.45
        old_state = state
        if reset or not enabled:
            state = False
        else:
            vin = float(row["vin"])
            low = float(row["low_trip"])
            high = float(row["high_trip"])
            if not state and low + hyst < vin < high - hyst:
                state = True
            elif state and (vin < low - hyst or vin > high + hyst):
                state = False

        control_changed = reset != previous_reset or enabled != previous_enabled
        state_changed = state != old_state
        if control_changed or state_changed:
            last_semantic_change_index = index
            pending_toggle = None
        if state_changed and not reset and enabled:
            expected_toggle_times.append(t)
            toggle_seen.append(False)
            pending_toggle = len(toggle_seen) - 1
        if pending_toggle is not None and float(row["toggled"]) > 0.35:
            toggle_seen[pending_toggle] = True
        previous_reset = reset
        previous_enabled = enabled

        # The grace period is relative to the observed semantic transition,
        # not to a deck-specific timestamp.  Stability still gates scoring so
        # a solver breakpoint cannot be mistaken for a settled output.
        if index <= last_semantic_change_index + settle_samples or not stable_output(index):
            continue
        checked += 1
        expected_level = 0.9 if state else 0.0
        observed_inside = float(row["inside_flag"])
        observed_metric = float(row["state_metric"])
        observed_toggle = float(row["toggled"])

        if reset or not enabled:
            clear_ok = observed_inside < 0.18 and observed_metric < 0.18 and observed_toggle < 0.25
            reset_samples += int(reset)
            disabled_samples += int(not enabled and not reset)
            if not clear_ok:
                clear_errors += 1
                kind = "reset_clear" if reset else "disabled_clear"
                remember_error(kind, row, 0.0, max(observed_inside, observed_metric, observed_toggle))
            continue

        inside_seen = inside_seen or state
        outside_seen = outside_seen or not state
        vin = float(row["vin"])
        low = float(row["low_trip"])
        high = float(row["high_trip"])
        in_low_hold = state and low - hyst + band_margin < vin < low - band_margin
        in_high_hold = state and high + band_margin < vin < high + hyst - band_margin
        low_hold_seen = low_hold_seen or in_low_hold
        high_hold_seen = high_hold_seen or in_high_hold

        if (observed_inside > 0.45) != state:
            state_errors += 1
            if in_low_hold or in_high_hold:
                band = "low" if in_low_hold else "high"
                remember_error(
                    "hysteresis_chatter_release",
                    row,
                    expected_level,
                    observed_inside,
                    f"band={band} expected_hold_inside=true",
                )
            elif state:
                remember_error("missing_window_assertion", row, expected_level, observed_inside)
            else:
                remember_error("missing_window_release", row, expected_level, observed_inside)
        if (observed_metric > 0.45) != state:
            metric_errors += 1
            remember_error("state_metric", row, expected_level, observed_metric)

    missing_toggle_times = [
        event_time
        for event_time, seen in zip(expected_toggle_times, toggle_seen)
        if not seen
    ]
    if missing_toggle_times and not first_error:
        event_time = missing_toggle_times[0]
        first_error = (
            f"v4_314_missing_toggle time={event_time:.6e} expected=0.9 observed=0.0 "
            f"mismatch_count={len(missing_toggle_times)} event_relative=true"
        )

    coverage_ok = inside_seen and outside_seen and low_hold_seen and high_hold_seen
    ok = (
        checked >= 20
        and reset_samples > 0
        and disabled_samples > 0
        and coverage_ok
        and clear_errors == 0
        and state_errors == 0
        and metric_errors == 0
        and not missing_toggle_times
    )
    if not ok and not first_error:
        first_error = (
            f"v4_314_insufficient_coverage checked={checked} reset_samples={reset_samples} "
            f"disabled_samples={disabled_samples} inside={inside_seen} outside={outside_seen} "
            f"low_hold={low_hold_seen} high_hold={high_hold_seen}"
        )
    note = (
        f"v4_314 checked={checked} reset_samples={reset_samples} disabled_samples={disabled_samples} "
        f"inside={inside_seen} outside={outside_seen} low_hold={low_hold_seen} high_hold={high_hold_seen} "
        f"state_errors={state_errors} metric_errors={metric_errors} clear_errors={clear_errors} "
        f"missing_toggle_count={len(missing_toggle_times)}"
    )
    return ok, note if ok else first_error + " " + note

CHECKER_ID = "v4_314_hysteretic_window_comparator"
CHECKER: Checker = check_v4_314_hysteretic_window_comparator
