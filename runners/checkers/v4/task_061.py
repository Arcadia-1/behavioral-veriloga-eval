"""Task-specific checker for canonical v4 DUT 061."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import (
    crossings,
    diagnostic,
    event_label,
    logic_bits_to_int,
    nearest_row,
    pass_note,
    probe_time,
    require_signals,
)


PROPERTIES = (
    "P_WINDOW_OPEN",
    "P_IN_WINDOW_COUNT",
    "P_OUT_OF_WINDOW_IGNORE",
    "P_WINDOW_CLOSE_HOLD",
    "P_BIT_ORDER_AND_LEVELS",
)


def check_event_counter_windowed_16b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "gate", "event", "done", *{f"count{i}" for i in range(16)}}
    invalid = require_signals(rows, required, "P_WINDOW_OPEN")
    if invalid:
        return False, invalid
    gate_rises = crossings(rows, "gate", threshold=0.45, direction="rising")
    gate_falls = crossings(rows, "gate", threshold=0.45, direction="falling")
    event_rises = crossings(rows, "event", threshold=0.45, direction="rising")
    errors = 0
    checked: list[int] = []
    outside_events_checked = 0
    reset_checks = 0
    hold_checks = 0
    failures: list[str] = []
    for window_index, (start_t, stop_t) in enumerate(zip(gate_rises, gate_falls), start=1):
        next_event = next((event_t for event_t in event_rises if event_t > start_t), stop_t)
        open_t = probe_time(rows, start_t, min(next_event, stop_t), fraction=0.35)
        open_row = nearest_row(rows, open_t) if open_t is not None else None
        if open_row is None:
            failures.append(
                diagnostic(
                    "P_WINDOW_OPEN",
                    "missing_probe",
                    expected="observable_open_window_probe",
                    observed="none",
                    event=event_label("gate_rise", window_index, start_t),
                )
            )
            continue
        open_count = logic_bits_to_int(open_row, "count", 16)
        if open_row["done"] > 0.45 or open_count != 0:
            failures.append(
                diagnostic(
                    "P_WINDOW_OPEN",
                    "semantic_mismatch",
                    expected="count=0,done=low",
                    observed=f"count={open_count},done={open_row['done']:.3f}",
                    event=event_label("gate_rise", window_index, start_t),
                )
            )
        else:
            reset_checks += 1
        expected = sum(1 for t in event_rises if start_t < t < stop_t)
        next_start = next((rise for rise in gate_rises if rise > stop_t), None)
        close_t = probe_time(rows, stop_t, next_start, fraction=0.25)
        row = nearest_row(rows, close_t) if close_t is not None else None
        if row is None:
            failures.append(
                diagnostic(
                    "P_WINDOW_CLOSE_HOLD",
                    "missing_probe",
                    expected="observable_close_window_probe",
                    observed="none",
                    event=event_label("gate_fall", window_index, stop_t),
                )
            )
            continue
        actual = logic_bits_to_int(row, "count", 16)
        if row["done"] <= 0.45 or actual != expected:
            errors += 1
            failures.append(
                diagnostic(
                    "P_IN_WINDOW_COUNT",
                    "semantic_mismatch",
                    expected=f"count={expected},done=high",
                    observed=f"count={actual},done={row['done']:.3f}",
                    event=event_label("gate_fall", window_index, stop_t),
                )
            )
        checked.append(expected)
        hold_stop = next_start if next_start is not None else rows[-1]["time"]
        for event_t in event_rises:
            if not (stop_t < event_t < hold_stop):
                continue
            hold_t = probe_time(rows, event_t, hold_stop, fraction=0.25)
            if hold_t is None:
                continue
            hold_row = nearest_row(rows, hold_t)
            if hold_row is None:
                continue
            held = logic_bits_to_int(hold_row, "count", 16)
            outside_events_checked += 1
            hold_checks += 1
            if held != expected or hold_row["done"] <= 0.45:
                errors += 1
                failures.append(
                    diagnostic(
                        "P_OUT_OF_WINDOW_IGNORE",
                        "semantic_mismatch",
                        expected=f"count={expected},done=high",
                        observed=f"count={held},done={hold_row['done']:.3f}",
                        event=event_label("event_rise", outside_events_checked, event_t),
                    )
                )
                break
    if failures:
        return False, " ".join(failures[:5])
    ok = (
        errors == 0
        and len(checked) >= 2
        and max(checked, default=0) > 0
        and outside_events_checked >= 1
        and reset_checks >= 1
        and hold_checks >= 1
    )
    summary = (
        f"checked={checked} errors={errors} reset_checks={reset_checks} "
        f"outside_events_checked={outside_events_checked} hold_checks={hold_checks}"
    )
    if not ok:
        return False, diagnostic(
            "P_WINDOW_CLOSE_HOLD",
            "insufficient_coverage",
            expected="two_windows,nonzero_count,outside_event,reset,hold",
            observed=summary.replace(" ", "_"),
            event="full_trace",
        )
    return True, pass_note(PROPERTIES, summary)

CHECKER_ID = "v4_061_event_counter_windowed_16b"
CHECKER: Checker = check_event_counter_windowed_16b
