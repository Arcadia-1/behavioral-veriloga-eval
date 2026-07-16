"""Task-specific checker for canonical v4 DUT 056."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import Row, diagnostic, pass_note, require_signals


WIDTH = 32
VTH = 0.45
LOW_MAX = 0.18
HIGH_MIN = 0.72
PROPERTIES = (
    "P_ENABLED_PASS",
    "P_DISABLED_CLEAR",
    "P_STATIC_ENABLE_BEHAVIOR",
    "P_BIT_ALIGNMENT",
    "P_OUTPUT_LEVELS",
)


def _logic_word(row: Row, prefix: str) -> int | None:
    word = 0
    for bit in range(WIDTH):
        value = row[f"{prefix}{bit}"]
        if LOW_MAX < value < HIGH_MIN:
            return None
        if value > VTH:
            word |= 1 << bit
    return word


def _settled_vectors(rows: list[Row]) -> list[tuple[bool, int, int]]:
    vectors: list[tuple[bool, int, int]] = []
    last_key: tuple[bool, int, int] | None = None
    for row in rows:
        if LOW_MAX < row["en"] < HIGH_MIN:
            continue
        input_word = _logic_word(row, "d")
        output_word = _logic_word(row, "q")
        if input_word is None or output_word is None:
            continue
        key = (row["en"] > VTH, input_word, output_word)
        if key != last_key:
            vectors.append(key)
            last_key = key
    return vectors

def check_config_latch_32b_clocked(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "en", *{f"d{i}" for i in range(WIDTH)}, *{f"q{i}" for i in range(WIDTH)}}
    missing = require_signals(rows, required, "P_ENABLED_PASS")
    if missing:
        return False, missing
    vectors = _settled_vectors(rows)
    if len(vectors) < 3:
        return False, diagnostic(
            "P_STATIC_ENABLE_BEHAVIOR",
            "insufficient_coverage",
            expected="settled_vectors>=3",
            observed=f"settled_vectors={len(vectors)}",
            event="full_trace",
        )

    enabled_samples = 0
    disabled_samples = 0
    enabled_words: set[int] = set()
    for index, (enabled, input_word, output_word) in enumerate(vectors):
        expected_word = input_word if enabled else 0
        if output_word != expected_word:
            property_id = "P_ENABLED_PASS" if enabled else "P_DISABLED_CLEAR"
            category = "enabled_pass_mismatch" if enabled else "disabled_clear_mismatch"
            return False, diagnostic(
                property_id,
                category,
                expected=f"word=0x{expected_word:08x}",
                observed=f"word=0x{output_word:08x}",
                event=f"settled_vector[{index}]",
            )
        if enabled:
            enabled_samples += 1
            enabled_words.add(input_word)
        else:
            disabled_samples += 1

    if enabled_samples < 2 or disabled_samples < 1 or len(enabled_words) < 2:
        return False, diagnostic(
            "P_STATIC_ENABLE_BEHAVIOR",
            "insufficient_enable_coverage",
            expected="enabled_vectors>=2_disabled_vectors>=1_distinct_enabled_words>=2",
            observed=(
                f"enabled_vectors={enabled_samples},disabled_vectors={disabled_samples},"
                f"distinct_enabled_words={len(enabled_words)}"
            ),
            event="full_trace",
        )
    return True, pass_note(PROPERTIES, f"settled_vectors={len(vectors)}")

CHECKER_ID = "v4_056_config_latch_32b_clocked"
CHECKER: Checker = check_config_latch_32b_clocked
