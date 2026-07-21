from __future__ import annotations

from ..api import Checker
from .family_261_270_diagnostics import bind_properties
from ..common.issue109_factory import (
    CheckResult,
    Row,
    check_clocked_factory,
    check_clocked_output_hold,
)


TASK_LABEL = 'v4_263_settling_progress_counter'
SOURCE_TASK_ID = 'v3_354_settling_progress_counter'
LEGACY_SYMBOL = '354-settling-progress-counter'


def check_v4_263_settling_progress_counter(rows: list[Row]) -> CheckResult:
    """Check v4_263_settling_progress_counter: Settling Progress Counter clocked counter behavior."""
    result = check_clocked_factory(rows, mode='counter', edge=1, task_name=TASK_LABEL)
    if not result[0]:
        return result
    ok, hold_note = check_clocked_output_hold(rows, edge=1, task_name=TASK_LABEL)
    return ok, f"{result[1]}; {hold_note}" if ok else hold_note


CHECKS = {
    TASK_LABEL: check_v4_263_settling_progress_counter,
    SOURCE_TASK_ID: check_v4_263_settling_progress_counter,
    LEGACY_SYMBOL: check_v4_263_settling_progress_counter,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = bind_properties(check_v4_263_settling_progress_counter, (
    "P_MEASURE_ANALOG_INPUTS_RELATIVE_TO_THE",
    "P_INITIALIZE_A_SAMPLED_PROGRESS_COUNT_TO",
))
