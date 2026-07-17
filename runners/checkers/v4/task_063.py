"""Task-specific checker for canonical v4 DUT 063."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import (
    diagnostic,
    event_label,
    logic_bits_to_int,
    nearest_row,
    pass_note,
    probe_time,
    require_signals,
    row_at_or_after,
)


PROPERTIES = (
    "P_WINDOW_DEFINITION",
    "P_ENTRY_AND_HOLD",
    "P_EXIT_RESETS_QUALIFICATION",
    "P_ENTRY_TIME_CODE",
    "P_BIT_ORDER_AND_LEVELS",
)


def check_settling_window_detector(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "target", "tol", "settled", *{f"t_code{i}" for i in range(8)}}
    invalid = require_signals(rows, required, "P_WINDOW_DEFINITION")
    if invalid:
        return False, invalid
    time_scale = float(rows[0].get("_time_scale", 1.0))
    time_shift_s = float(rows[0].get("_time_shift_s", 0.0))
    hold = 20e-9 * time_scale
    flags = [abs(row["vin"] - row["target"]) <= row["tol"] + 1e-12 for row in rows]
    intervals: list[tuple[float, float]] = []
    start: float | None = rows[0]["time"] if flags[0] else None
    for idx in range(1, len(rows)):
        if flags[idx] and not flags[idx - 1]:
            start = rows[idx]["time"]
        elif flags[idx - 1] and not flags[idx] and start is not None:
            intervals.append((start, rows[idx]["time"]))
            start = None
    if start is not None:
        intervals.append((start, rows[-1]["time"]))

    long_intervals = [
        (a, b) for a, b in intervals if b - a >= hold + 2e-9 * time_scale
    ]
    if not long_intervals:
        return False, diagnostic(
            "P_ENTRY_AND_HOLD",
            "insufficient_coverage",
            expected="settling_interval_longer_than_hold",
            observed=f"interval_count={len(intervals)}",
            event="full_trace",
        )

    errors = 0
    settled_seen = False
    early_seen = False
    reset_seen = False
    failures: list[str] = []

    unexpected_settled = next(
        (
            row
            for row, expected_in_window in zip(rows, flags)
            if not expected_in_window and row["settled"] > 0.45
        ),
        None,
    )
    if unexpected_settled is not None:
        errors += 1
        failures.append(
            diagnostic(
                "P_WINDOW_DEFINITION",
                "semantic_mismatch",
                expected="settled=low_outside_tolerance_window",
                observed=f"settled={unexpected_settled['settled']:.3f}",
                event=event_label("outside_window", 1, unexpected_settled["time"]),
            )
        )

    for interval_index, (entry, exit_t) in enumerate(long_intervals, start=1):
        early_t = entry + 0.5 * hold
        settled_t = probe_time(rows, entry + hold, exit_t, fraction=0.25)
        interval_samples: list[tuple[str, float, dict[str, float] | None]] = [
            ("early", early_t, nearest_row(rows, early_t)),
            (
                "settled",
                settled_t,
                row_at_or_after(rows, settled_t) if settled_t is not None else None,
            ),
        ]
        for phase, sample_t, row in interval_samples:
            if row is None:
                failures.append(
                    diagnostic(
                        "P_ENTRY_AND_HOLD",
                        "missing_probe",
                        expected=f"{phase}_probe",
                        observed="none",
                        event=event_label("settling_entry", interval_index, entry),
                    )
                )
                continue
            actual_settled = row["settled"] > 0.45
            if phase == "early" and actual_settled:
                early_seen = True
                errors += 1
                failures.append(
                    diagnostic(
                        "P_ENTRY_AND_HOLD",
                        "semantic_mismatch",
                        expected="settled=low_before_hold_time",
                        observed=f"settled={row['settled']:.3f}",
                        event=event_label("settling_entry", interval_index, entry),
                    )
                )
            if phase != "settled":
                continue
            if not actual_settled:
                errors += 1
                failures.append(
                    diagnostic(
                        "P_ENTRY_AND_HOLD",
                        "semantic_mismatch",
                        expected="settled=high_after_hold_time",
                        observed=f"settled={row['settled']:.3f}",
                        event=event_label("settling_entry", interval_index, entry),
                    )
                )
                continue
            settled_seen = True
            physical_entry = (entry - time_shift_s) / time_scale
            expected_code = max(0, min(255, int(round(physical_entry / 1e-9))))
            actual_code = logic_bits_to_int(row, "t_code", 8)
            if abs(actual_code - expected_code) > 1:
                errors += 1
                failures.append(
                    diagnostic(
                        "P_ENTRY_TIME_CODE",
                        "semantic_mismatch",
                        expected=f"entry_code={expected_code}",
                        observed=f"entry_code={actual_code}",
                        event=event_label("settling_entry", interval_index, entry),
                    )
                )

    for interval_index, (_, exit_t) in enumerate(intervals, start=1):
        next_entry = next((entry for entry, _ in intervals if entry > exit_t), None)
        reset_t = probe_time(rows, exit_t, next_entry, fraction=0.25)
        row = nearest_row(rows, reset_t) if reset_t is not None else None
        if row is None:
            continue
        actual_settled = row["settled"] > 0.45
        if actual_settled:
            errors += 1
            failures.append(
                diagnostic(
                    "P_EXIT_RESETS_QUALIFICATION",
                    "semantic_mismatch",
                    expected="settled=low_after_exit",
                    observed=f"settled={row['settled']:.3f}",
                    event=event_label("settling_exit", interval_index, exit_t),
                )
            )
        else:
            reset_seen = True
    if failures:
        return False, " ".join(failures[:5])
    ok = errors == 0 and settled_seen and reset_seen and not early_seen
    summary = (
        f"errors={errors} intervals={[(round(a/1e-9,1), round(b/1e-9,1)) for a,b in long_intervals]} "
        f"settled_seen={settled_seen} reset_seen={reset_seen} early_seen={early_seen}"
    )
    if not ok:
        return False, diagnostic(
            "P_WINDOW_DEFINITION",
            "insufficient_coverage",
            expected="settled_region,exit_reset,no_early_settle",
            observed=summary.replace(" ", "_"),
            event="full_trace",
        )
    return True, pass_note(PROPERTIES, summary)

CHECKER_ID = "v4_063_settling_window_detector"
CHECKER: Checker = check_settling_window_detector
