from __future__ import annotations

from checkers.api import Checker
from checkers.common.issue109_factory import CheckResult, Row, check_continuous_factory
from checkers.v4.factory_property_diagnostics import append_continuous_property_diagnostics


TASK_LABEL = 'v4_258_priority_fault_code_driver'
SOURCE_TASK_ID = 'v3_349_priority_fault_code_driver'
LEGACY_SYMBOL = '349-priority-fault-code-driver'


def check_v4_258_priority_fault_code_driver(rows: list[Row]) -> CheckResult:
    """Check v4_258_priority_fault_code_driver: Priority Fault Code Driver continuous priority behavior."""
    ok, note = check_continuous_factory(rows, mode='priority', task_name=TASK_LABEL)
    return ok, append_continuous_property_diagnostics(
        rows,
        note,
        mode='priority',
        normalization_property_id='P_MEASURE_ANALOG_INPUTS_RELATIVE_TO_THE',
        function_property_id='P_ENCODE_THE_HIGHEST_PRIORITY_FAULT_CODE',
    )


CHECKS = {
    TASK_LABEL: check_v4_258_priority_fault_code_driver,
    SOURCE_TASK_ID: check_v4_258_priority_fault_code_driver,
    LEGACY_SYMBOL: check_v4_258_priority_fault_code_driver,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_258_priority_fault_code_driver
