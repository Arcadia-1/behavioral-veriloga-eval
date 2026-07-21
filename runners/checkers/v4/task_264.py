from __future__ import annotations

from ..api import Checker
from .family_261_270_diagnostics import bind_properties
from ..common.issue109_factory import (
    CheckResult,
    Row,
    check_clocked_factory,
    check_clocked_output_hold,
)


TASK_LABEL = 'v4_264_enable_qualified_bias_hold'
SOURCE_TASK_ID = 'v3_355_enable_qualified_bias_hold'
LEGACY_SYMBOL = '355-enable-qualified-bias-hold'


def check_v4_264_enable_qualified_bias_hold(rows: list[Row]) -> CheckResult:
    """Check v4_264_enable_qualified_bias_hold: Enable Qualified Bias Hold clocked latch behavior."""
    result = check_clocked_factory(
        rows,
        mode='latch',
        edge=1,
        task_name=TASK_LABEL,
        asynchronous_reset=True,
    )
    if not result[0]:
        return result
    ok, hold_note = check_clocked_output_hold(rows, edge=1, task_name=TASK_LABEL)
    return ok, f"{result[1]}; {hold_note}" if ok else hold_note


CHECKS = {
    TASK_LABEL: check_v4_264_enable_qualified_bias_hold,
    SOURCE_TASK_ID: check_v4_264_enable_qualified_bias_hold,
    LEGACY_SYMBOL: check_v4_264_enable_qualified_bias_hold,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = bind_properties(check_v4_264_enable_qualified_bias_hold, (
    "P_MEASURE_ANALOG_INPUTS_RELATIVE_TO_THE",
    "P_INITIALIZE_THE_HELD_BIAS_OUTPUT_FLAG",
))
