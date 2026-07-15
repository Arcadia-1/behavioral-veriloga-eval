from __future__ import annotations

from ..api import Checker
from ..common.issue109_factory import CheckResult, Row, check_continuous_factory


TASK_LABEL = 'v4_251_weighted_balance_summer'
SOURCE_TASK_ID = 'v3_342_weighted_balance_summer'
LEGACY_SYMBOL = '342-weighted-balance-summer'


def check_v4_251_weighted_balance_summer(rows: list[Row]) -> CheckResult:
    """Check v4_251_weighted_balance_summer: Weighted Balance Summer continuous sum behavior."""
    return check_continuous_factory(rows, mode='sum', task_name=TASK_LABEL)


CHECKS = {
    TASK_LABEL: check_v4_251_weighted_balance_summer,
    SOURCE_TASK_ID: check_v4_251_weighted_balance_summer,
    LEGACY_SYMBOL: check_v4_251_weighted_balance_summer,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_251_weighted_balance_summer
