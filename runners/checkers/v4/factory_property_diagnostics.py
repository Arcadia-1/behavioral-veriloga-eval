"""Observable property diagnostics for continuous factory checkers."""
from __future__ import annotations

from checkers.common.issue109_factory import (
    CONT_REQUIRED,
    _cont_expected,
    _normalized_inputs,
    _sample_times,
    _values_at,
)


def append_continuous_property_diagnostics(
    rows: list[dict[str, float]],
    note: str,
    *,
    mode: str,
    normalization_property_id: str,
    function_property_id: str,
    tolerance: float = 0.085,
) -> str:
    """Append black-box mismatch counts without changing checker pass/fail.

    The normalization property is observed end to end, so it counts any
    sampled output-contract mismatch. The downstream function property counts
    mismatches only while the normalized input row is valid.
    """

    normalization_mismatches = 0
    function_mismatches = 0
    if rows and CONT_REQUIRED.issubset(rows[0]):
        names = (
            "in0",
            "in1",
            "in2",
            "in3",
            "ctrl0",
            "ctrl1",
            "vdd",
            "vss",
            "en",
            "out",
            "flag",
            "metric",
        )
        for time_s in _sample_times(rows):
            values = _values_at(rows, names, time_s)
            if values is None:
                continue
            before = _values_at(
                rows,
                names[:9],
                max(float(rows[0]["time"]), time_s - 0.12e-9),
            )
            after = _values_at(
                rows,
                names[:9],
                min(float(rows[-1]["time"]), time_s + 0.12e-9),
            )
            if before is not None and after is not None:
                before_flag = _cont_expected(mode, before)["flag"]
                after_flag = _cont_expected(mode, after)["flag"]
                if abs(before_flag - after_flag) > 0.45:
                    continue

            expected = _cont_expected(mode, values)
            mismatched = any(
                abs(float(values[name]) - expected[name]) > tolerance
                for name in ("out", "flag", "metric")
            )
            if not mismatched:
                continue
            normalization_mismatches += 1
            if _normalized_inputs(values)["valid"] > 0.5:
                function_mismatches += 1

    return (
        f"{note}; {normalization_property_id} "
        f"mismatch_count={normalization_mismatches}; "
        f"{function_property_id} mismatch_count={function_mismatches}"
    )
