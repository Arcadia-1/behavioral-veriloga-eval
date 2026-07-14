"""Checker for the 32-bit masked configuration update utility."""

from __future__ import annotations

from ..api import Checker, Row


WIDTH = 32
VTH = 0.45
LOW_MAX = 0.15
HIGH_MIN = 0.75


def _logic(value: float) -> int:
    return int(float(value) > VTH)


def _word(row: Row, prefix: str) -> int:
    return sum(_logic(row[f"{prefix}{bit}"]) << bit for bit in range(WIDTH))


def _required_signals() -> set[str]:
    return {"time"} | {
        f"{prefix}{bit}"
        for prefix in ("old", "new", "mask", "out")
        for bit in range(WIDTH)
    }


def check_masked_config_update_32b(rows: list[Row]) -> tuple[bool, str]:
    required = _required_signals()
    missing = sorted(required - (set(rows[0]) if rows else set()))
    if missing:
        return False, "missing_columns=" + ",".join(missing[:12])

    # Collapse each stable input vector to its latest row. This makes the
    # checker independent of the submitter's start time and vector duration.
    samples: dict[tuple[int, int, int], Row] = {}
    for row in rows:
        key = (_word(row, "old"), _word(row, "new"), _word(row, "mask"))
        samples[key] = row

    mismatch_count = 0
    rail_errors = 0
    exercised_mask_zero = False
    exercised_mask_full = False
    exercised_mask_mixed = False
    observed_mask_values = [set() for _ in range(WIDTH)]
    observable_choices = [False] * WIDTH

    for (old_word, new_word, mask_word), row in samples.items():
        exercised_mask_zero |= mask_word == 0
        exercised_mask_full |= mask_word == (1 << WIDTH) - 1
        exercised_mask_mixed |= mask_word not in {0, (1 << WIDTH) - 1}
        expected_word = (new_word & mask_word) | (old_word & ~mask_word)
        for bit in range(WIDTH):
            observed_mask_values[bit].add((mask_word >> bit) & 1)
            observable_choices[bit] |= ((old_word ^ new_word) >> bit) & 1 == 1
            expected = (expected_word >> bit) & 1
            value = float(row[f"out{bit}"])
            if _logic(value) != expected:
                mismatch_count += 1
            if expected == 0 and value > LOW_MAX:
                rail_errors += 1
            if expected == 1 and value < HIGH_MIN:
                rail_errors += 1

    uncovered_bits = [
        bit
        for bit in range(WIDTH)
        if observed_mask_values[bit] != {0, 1} or not observable_choices[bit]
    ]
    coverage_ok = (
        len(samples) >= 3
        and exercised_mask_zero
        and exercised_mask_full
        and exercised_mask_mixed
        and not uncovered_bits
    )
    ok = coverage_ok and mismatch_count == 0 and rail_errors == 0
    return ok, (
        f"masked_vectors={len(samples)} mismatch_count={mismatch_count} "
        f"rail_errors={rail_errors} zero={exercised_mask_zero} "
        f"full={exercised_mask_full} mixed={exercised_mask_mixed} "
        f"uncovered_bits={uncovered_bits}"
    )


CHECKER_ID = "v4_058_masked_config_update_32b"
CHECKER: Checker = check_masked_config_update_32b
