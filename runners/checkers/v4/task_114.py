"""Task-specific checker for canonical v4 DUT 114."""
from __future__ import annotations

from collections.abc import Callable

from ..api import Checker
from .stimulus_relative import diagnostic, pass_note, require_signals


PROPERTY_IDS = (
    "P_HIGH_SELECTS_VIN1",
    "P_LOW_SELECTS_VIN2",
    "P_BIDIRECTIONAL_SELECTION",
    "P_NO_MIXING",
)


def _v3_formula_check(
    rows: list[dict[str, float]],
    *,
    required: set[str],
    output: str,
    expected_fn: Callable[[dict[str, float]], float | None],
    tol: float,
    min_checked: int,
    max_rows: int = 240,
    stable_fn: Callable[[dict[str, float]], bool] | None = None,
    property_id: str,
    label: str,
) -> tuple[bool, str]:
    missing = require_signals(rows, required, property_id)
    if missing:
        return False, missing

    stride = max(1, len(rows) // max_rows)
    checked = 0
    max_err = 0.0
    for index, row in enumerate(rows[::stride]):
        if stable_fn is not None and not stable_fn(row):
            continue
        expected = expected_fn(row)
        if expected is None:
            continue
        observed = row.get(output)
        if observed is None:
            return False, diagnostic(
                property_id,
                "missing_sample",
                expected=output,
                observed="unavailable",
                event=f"{label}[{index}]",
            )
        err = abs(observed - expected)
        max_err = max(max_err, err)
        checked += 1
        if err > tol:
            return False, diagnostic(
                property_id,
                "formula_mismatch",
                expected=f"{output}={expected:.4f}",
                observed=f"{output}={observed:.4f},err={err:.4f}",
                event=f"{label}[{index}]",
            )
    if checked < min_checked:
        return False, diagnostic(
            property_id,
            "insufficient_checks",
            expected=f"checked>={min_checked}",
            observed=f"checked={checked}",
            event=f"{label}_set",
        )
    return True, f"checked={checked} max_error={max_err:.5f}"

def check_v3_analog_mux_threshold(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin1", "vin2", "vsel", "vout"}
    modes: set[int] = set()

    def expected(row: dict[str, float]) -> float:
        mode = 1 if row["vsel"] > 0.45 else 0
        modes.add(mode)
        return row["vin1"] if mode else row["vin2"]

    ok, detail = _v3_formula_check(
        rows,
        required=required,
        output="vout",
        expected_fn=expected,
        stable_fn=lambda row: abs(row["vsel"] - 0.45) > 0.05,
        tol=0.035,
        min_checked=20,
        property_id="P_NO_MIXING",
        label="mux_observation",
    )
    if not ok:
        return ok, detail
    if modes != {0, 1}:
        return False, diagnostic(
            "P_BIDIRECTIONAL_SELECTION",
            "insufficient_mode_coverage",
            expected="modes=0,1",
            observed="modes=" + ",".join(str(value) for value in sorted(modes)),
            event="mux_observation_set",
        )
    return True, pass_note(PROPERTY_IDS, detail + " modes=0,1")

CHECKER_ID = "v4_114_analog_mux_threshold"
CHECKER: Checker = check_v3_analog_mux_threshold
