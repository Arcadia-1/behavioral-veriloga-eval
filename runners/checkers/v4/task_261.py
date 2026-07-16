from __future__ import annotations

from ..api import Checker
from .family_261_270_diagnostics import bind_properties
from ..common.issue109_factory import CheckResult, Row, check_clocked_factory


TASK_LABEL = 'v4_261_falling_edge_calibration_sampler'
SOURCE_TASK_ID = 'v3_352_falling_edge_calibration_sampler'
LEGACY_SYMBOL = '352-falling-edge-calibration-sampler'


def check_v4_261_falling_edge_calibration_sampler(rows: list[Row]) -> CheckResult:
    """Check v4_261_falling_edge_calibration_sampler: Falling Edge Calibration Sampler clocked sample_fall behavior."""
    return check_clocked_factory(rows, mode='sample_fall', edge=-1, task_name=TASK_LABEL)


CHECKS = {
    TASK_LABEL: check_v4_261_falling_edge_calibration_sampler,
    SOURCE_TASK_ID: check_v4_261_falling_edge_calibration_sampler,
    LEGACY_SYMBOL: check_v4_261_falling_edge_calibration_sampler,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = bind_properties(check_v4_261_falling_edge_calibration_sampler, (
    "P_MEASURE_ANALOG_INPUTS_RELATIVE_TO_THE",
    "P_INITIALIZE_OUT_FLAG_AND_METRIC_TO",
))
