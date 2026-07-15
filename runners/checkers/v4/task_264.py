from __future__ import annotations

from ..api import Checker
from ..common.issue109_factory import CheckResult, Row, check_clocked_factory


TASK_LABEL = 'v4_264_enable_qualified_bias_hold'
SOURCE_TASK_ID = 'v3_355_enable_qualified_bias_hold'
LEGACY_SYMBOL = '355-enable-qualified-bias-hold'


def check_v4_264_enable_qualified_bias_hold(rows: list[Row]) -> CheckResult:
    """Check v4_264_enable_qualified_bias_hold: Enable Qualified Bias Hold clocked latch behavior."""
    return check_clocked_factory(rows, mode='latch', edge=1, task_name=TASK_LABEL)


CHECKS = {
    TASK_LABEL: check_v4_264_enable_qualified_bias_hold,
    SOURCE_TASK_ID: check_v4_264_enable_qualified_bias_hold,
    LEGACY_SYMBOL: check_v4_264_enable_qualified_bias_hold,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_264_enable_qualified_bias_hold
