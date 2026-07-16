from __future__ import annotations

from ..api import Checker
from .family_261_270_diagnostics import bind_properties
from ..common.issue109_factory import CheckResult, Row, check_clocked_factory


TASK_LABEL = 'v4_263_settling_progress_counter'
SOURCE_TASK_ID = 'v3_354_settling_progress_counter'
LEGACY_SYMBOL = '354-settling-progress-counter'


def check_v4_263_settling_progress_counter(rows: list[Row]) -> CheckResult:
    """Check v4_263_settling_progress_counter: Settling Progress Counter clocked counter behavior."""
    return check_clocked_factory(rows, mode='counter', edge=1, task_name=TASK_LABEL)


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
