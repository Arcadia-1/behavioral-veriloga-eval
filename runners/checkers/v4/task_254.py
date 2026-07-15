from __future__ import annotations

from ..api import Checker
from ..common.issue109_factory import CheckResult, Row, check_continuous_factory
from .factory_property_diagnostics import append_continuous_property_diagnostics


TASK_LABEL = 'v4_254_bias_trim_affine_mapper'
SOURCE_TASK_ID = 'v3_345_bias_trim_affine_mapper'
LEGACY_SYMBOL = '345-bias-trim-affine-mapper'


def check_v4_254_bias_trim_affine_mapper(rows: list[Row]) -> CheckResult:
    """Check v4_254_bias_trim_affine_mapper: Bias Trim Affine Mapper continuous gain behavior."""
    ok, note = check_continuous_factory(rows, mode='gain', task_name=TASK_LABEL)
    return ok, append_continuous_property_diagnostics(
        rows,
        note,
        mode='gain',
        normalization_property_id='P_MEASURE_ANALOG_INPUTS_RELATIVE_TO_THE',
        function_property_id='P_COMPUTE_THE_BIAS_TRIM_AFFINE_VALUE',
    )


CHECKS = {
    TASK_LABEL: check_v4_254_bias_trim_affine_mapper,
    SOURCE_TASK_ID: check_v4_254_bias_trim_affine_mapper,
    LEGACY_SYMBOL: check_v4_254_bias_trim_affine_mapper,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_254_bias_trim_affine_mapper
