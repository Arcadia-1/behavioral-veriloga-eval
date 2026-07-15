from __future__ import annotations

from ..api import Checker
from ..common.issue109_factory import CheckResult, Row, check_continuous_factory


TASK_LABEL = 'v4_265_dynamic_supply_enable_driver'
SOURCE_TASK_ID = 'v3_356_dynamic_supply_enable_driver'
LEGACY_SYMBOL = '356-dynamic-supply-enable-driver'


def check_v4_265_dynamic_supply_enable_driver(rows: list[Row]) -> CheckResult:
    """Check v4_265_dynamic_supply_enable_driver: Dynamic Supply Enable Driver continuous translate behavior."""
    return check_continuous_factory(rows, mode='translate', task_name=TASK_LABEL)


CHECKS = {
    TASK_LABEL: check_v4_265_dynamic_supply_enable_driver,
    SOURCE_TASK_ID: check_v4_265_dynamic_supply_enable_driver,
    LEGACY_SYMBOL: check_v4_265_dynamic_supply_enable_driver,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_265_dynamic_supply_enable_driver
