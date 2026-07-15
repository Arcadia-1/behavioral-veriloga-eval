from __future__ import annotations

from ..api import Checker
from ..common.issue109_factory import CheckResult, Row, check_clocked_factory


TASK_LABEL = 'v4_260_comparator_decision_capture'
SOURCE_TASK_ID = 'v3_351_comparator_decision_capture'
LEGACY_SYMBOL = '351-comparator-decision-capture'


def check_v4_260_comparator_decision_capture(rows: list[Row]) -> CheckResult:
    """Check v4_260_comparator_decision_capture: Comparator Decision Capture clocked edge behavior."""
    return check_clocked_factory(rows, mode='edge', edge=1, task_name=TASK_LABEL)


CHECKS = {
    TASK_LABEL: check_v4_260_comparator_decision_capture,
    SOURCE_TASK_ID: check_v4_260_comparator_decision_capture,
    LEGACY_SYMBOL: check_v4_260_comparator_decision_capture,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_260_comparator_decision_capture
