from __future__ import annotations

from ..api import Checker
from ..common.issue109_factory import CheckResult, Row, check_continuous_factory
from .factory_property_diagnostics import append_continuous_property_diagnostics


TASK_LABEL = 'v4_259_lane_validity_reduction_monitor'
SOURCE_TASK_ID = 'v3_350_lane_validity_reduction_monitor'
LEGACY_SYMBOL = '350-lane-validity-reduction-monitor'


def check_v4_259_lane_validity_reduction_monitor(rows: list[Row]) -> CheckResult:
    """Check v4_259_lane_validity_reduction_monitor: Lane Validity Reduction Monitor continuous reduction behavior."""
    ok, note = check_continuous_factory(rows, mode='reduction', task_name=TASK_LABEL)
    return ok, append_continuous_property_diagnostics(
        rows,
        note,
        mode='reduction',
        normalization_property_id='P_MEASURE_ANALOG_INPUTS_RELATIVE_TO_THE',
        function_property_id='P_COUNT_HOW_MANY_OF_X0_X1',
    )


CHECKS = {
    TASK_LABEL: check_v4_259_lane_validity_reduction_monitor,
    SOURCE_TASK_ID: check_v4_259_lane_validity_reduction_monitor,
    LEGACY_SYMBOL: check_v4_259_lane_validity_reduction_monitor,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_259_lane_validity_reduction_monitor
