from __future__ import annotations

from ..api import Checker
from ..common.issue109_factory import CheckResult, Row, check_continuous_factory


TASK_LABEL = 'v4_252_supply_qualified_window_flag'
SOURCE_TASK_ID = 'v3_343_supply_qualified_window_flag'
LEGACY_SYMBOL = '343-supply-qualified-window-flag'


def check_v4_252_supply_qualified_window_flag(rows: list[Row]) -> CheckResult:
    """Check v4_252_supply_qualified_window_flag: Supply Qualified Window Flag continuous window behavior."""
    return check_continuous_factory(rows, mode='window', task_name=TASK_LABEL)


CHECKS = {
    TASK_LABEL: check_v4_252_supply_qualified_window_flag,
    SOURCE_TASK_ID: check_v4_252_supply_qualified_window_flag,
    LEGACY_SYMBOL: check_v4_252_supply_qualified_window_flag,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_252_supply_qualified_window_flag
