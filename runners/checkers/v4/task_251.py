from __future__ import annotations

from ..api import Checker
from ..common.issue109_factory import CheckResult, Row, check_continuous_factory
from .factory_property_diagnostics import append_continuous_property_diagnostics


TASK_LABEL = 'v4_251_weighted_balance_summer'
SOURCE_TASK_ID = 'v3_342_weighted_balance_summer'
LEGACY_SYMBOL = '342-weighted-balance-summer'


def check_v4_251_weighted_balance_summer(rows: list[Row]) -> CheckResult:
    """Check v4_251_weighted_balance_summer: Weighted Balance Summer continuous sum behavior."""
    ok, note = check_continuous_factory(rows, mode='sum', task_name=TASK_LABEL)
    return ok, append_continuous_property_diagnostics(
        rows,
        note,
        mode='sum',
        normalization_property_id='P_MEASURE_ANALOG_INPUTS_RELATIVE_TO_THE',
        function_property_id='P_COMPUTE_THE_WEIGHTED_BALANCE_SUM_AS',
    )


CHECKS = {
    TASK_LABEL: check_v4_251_weighted_balance_summer,
    SOURCE_TASK_ID: check_v4_251_weighted_balance_summer,
    LEGACY_SYMBOL: check_v4_251_weighted_balance_summer,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_251_weighted_balance_summer
