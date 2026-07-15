from __future__ import annotations

from ..api import Checker
from ..common.issue109_factory import CheckResult, Row, check_continuous_factory


TASK_LABEL = 'v4_259_lane_validity_reduction_monitor'
SOURCE_TASK_ID = 'v3_350_lane_validity_reduction_monitor'
LEGACY_SYMBOL = '350-lane-validity-reduction-monitor'


def check_v4_259_lane_validity_reduction_monitor(rows: list[Row]) -> CheckResult:
    """Check v4_259_lane_validity_reduction_monitor: Lane Validity Reduction Monitor continuous reduction behavior."""
    return check_continuous_factory(rows, mode='reduction', task_name=TASK_LABEL)


CHECKS = {
    TASK_LABEL: check_v4_259_lane_validity_reduction_monitor,
    SOURCE_TASK_ID: check_v4_259_lane_validity_reduction_monitor,
    LEGACY_SYMBOL: check_v4_259_lane_validity_reduction_monitor,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_259_lane_validity_reduction_monitor
