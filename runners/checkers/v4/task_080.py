"""Task-specific checker for canonical v4 DUT 080."""
from __future__ import annotations

import math

from ..api import Checker
from .stimulus_relative import diagnostic, pass_note, require_signals


PROPERTY_IDS = (
    "P_FIRST_TONE",
    "P_SECOND_TONE",
    "P_THIRD_TONE",
    "P_LINEAR_SUPERPOSITION",
    "P_ZERO_INITIAL_PHASE",
)


def _expected(time_s: float) -> float:
    return (
        0.2 * math.sin(2 * math.pi * 1e6 * time_s)
        + 0.1 * math.sin(2 * math.pi * 2e6 * time_s)
        + 0.05 * math.sin(2 * math.pi * 3e6 * time_s)
    )


def check_multitone(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, diagnostic(
            "P_LINEAR_SUPERPOSITION",
            "invalid_trace",
            expected="nonempty_trace",
            observed="empty_trace",
            event="full_trace",
        )
    out_col = next((key for key in rows[0] if key.lower() in {"out", "vout"}), None)
    if out_col is None:
        return False, diagnostic(
            "P_LINEAR_SUPERPOSITION",
            "invalid_trace",
            expected="signal:OUT",
            observed="missing:OUT",
            event="full_trace",
        )
    missing = require_signals(rows, {"time", out_col}, "P_LINEAR_SUPERPOSITION")
    if missing is not None:
        return False, missing

    if len(rows) < 8:
        return False, diagnostic(
            "P_LINEAR_SUPERPOSITION",
            "invalid_trace",
            expected="samples>=8",
            observed=f"samples:{len(rows)}",
            event="full_trace",
        )

    stride = max(1, len(rows) // 24)
    checked_rows = rows[1::stride]
    if len(checked_rows) > 24:
        checked_rows = checked_rows[:24]
    errs = [abs(row[out_col] - _expected(row["time"])) for row in checked_rows]
    max_err = max(errs)
    if max_err >= 0.03:
        worst_index, worst_err = max(enumerate(errs), key=lambda item: item[1])
        row = checked_rows[worst_index]
        return False, diagnostic(
            "P_LINEAR_SUPERPOSITION",
            "value_mismatch",
            expected=f"out:{_expected(row['time']):.4f}",
            observed=f"out:{row[out_col]:.4f}",
            event=f"sample[{worst_index}]",
        )

    zero_phase_rows = [row for row in rows[: max(3, len(rows) // 20)] if abs(row["time"]) <= 2e-9]
    if zero_phase_rows and abs(zero_phase_rows[0][out_col]) > 0.03:
        return False, diagnostic(
            "P_ZERO_INITIAL_PHASE",
            "value_mismatch",
            expected="out:0.0000",
            observed=f"out:{zero_phase_rows[0][out_col]:.4f}",
            event="initial_sample",
        )

    return True, pass_note(
        PROPERTY_IDS,
        f"multitone checked_samples={len(checked_rows)} max_err={max_err:.4f}",
    )


CHECKER_ID = "v4_080_sine_periodic_voltage_source"
CHECKER: Checker = check_multitone
