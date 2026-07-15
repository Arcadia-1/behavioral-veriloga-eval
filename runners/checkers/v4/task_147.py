"""Checker for the static seven-bit control-word encoder."""

from __future__ import annotations

from statistics import median

from ..api import Checker, Row


CONTROL_WORDS = (42, 85, 0, 19, 108, 127)
WIDTH = 7
VHI = 0.9
VLO = 0.0
TOL = 0.08


def _tail_rows(rows: list[Row]) -> list[Row]:
    # Static outputs need only settle; no absolute stop time is part of the
    # public contract. Use the final quarter of whatever trace was supplied.
    start = max(0, len(rows) - max(1, len(rows) // 4))
    return rows[start:]


def check_control_word_encoder_7b(rows: list[Row]) -> tuple[bool, str]:
    available = set(rows[0]) if rows else set()
    if "time" not in available:
        return False, "missing_columns=time"

    complete_groups: list[int] = []
    partial_missing: list[str] = []
    for ctrl in CONTROL_WORDS:
        group = {f"d{bit}_{ctrl}" for bit in range(WIDTH)}
        present = group & available
        if present == group:
            complete_groups.append(ctrl)
        elif present:
            partial_missing.extend(sorted(group - available))
    if partial_missing:
        return False, "missing_columns=" + ",".join(sorted(partial_missing))
    if len(set(complete_groups)) < 2:
        return False, f"insufficient_control_word_coverage={complete_groups}"

    tail = _tail_rows(rows)
    mismatches: list[str] = []
    rail_errors = 0
    for ctrl in complete_groups:
        for bit in range(WIDTH):
            signal = f"d{bit}_{ctrl}"
            observed = median(float(row[signal]) for row in tail)
            expected = VHI if (ctrl >> bit) & 1 else VLO
            if abs(observed - expected) > TOL:
                mismatches.append(f"{signal}={observed:.4f}/{expected:.1f}")
            if min(abs(observed - VLO), abs(observed - VHI)) > TOL:
                rail_errors += 1

    ok = not mismatches and rail_errors == 0
    return ok, (
        f"control_words={complete_groups} mismatch_count={len(mismatches)} "
        f"rail_errors={rail_errors} first_mismatch={mismatches[:1]}"
    )


CHECKER_ID = "v4_147_control_word_encoder_7b"
CHECKER: Checker = check_control_word_encoder_7b
