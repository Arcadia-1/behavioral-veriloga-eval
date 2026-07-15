from __future__ import annotations

from ..api import Checker
from ..common.issue109_factory import CheckResult, Row, check_continuous_factory


TASK_LABEL = 'v4_256_multi_condition_enable_combiner'
SOURCE_TASK_ID = 'v3_347_multi_condition_enable_combiner'
LEGACY_SYMBOL = '347-multi-condition-enable-combiner'


def check_v4_256_multi_condition_enable_combiner(rows: list[Row]) -> CheckResult:
    """Check v4_256_multi_condition_enable_combiner: Multi Condition Enable Combiner continuous reduction behavior."""
    return check_continuous_factory(rows, mode='reduction', task_name=TASK_LABEL)


CHECKS = {
    TASK_LABEL: check_v4_256_multi_condition_enable_combiner,
    SOURCE_TASK_ID: check_v4_256_multi_condition_enable_combiner,
    LEGACY_SYMBOL: check_v4_256_multi_condition_enable_combiner,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_256_multi_condition_enable_combiner
