from __future__ import annotations

from ..api import Checker
from ..common.issue109_factory import CheckResult, Row, check_continuous_factory
from .factory_property_diagnostics import append_continuous_property_diagnostics


TASK_LABEL = 'v4_256_multi_condition_enable_combiner'
SOURCE_TASK_ID = 'v3_347_multi_condition_enable_combiner'
LEGACY_SYMBOL = '347-multi-condition-enable-combiner'


def check_v4_256_multi_condition_enable_combiner(rows: list[Row]) -> CheckResult:
    """Check v4_256_multi_condition_enable_combiner: Multi Condition Enable Combiner continuous reduction behavior."""
    ok, note = check_continuous_factory(rows, mode='reduction', task_name=TASK_LABEL)
    return ok, append_continuous_property_diagnostics(
        rows,
        note,
        mode='reduction',
        normalization_property_id='P_MEASURE_ANALOG_INPUTS_RELATIVE_TO_THE',
        function_property_id='P_COUNT_THE_NUMBER_OF_NORMALIZED_INPUTS',
    )


CHECKS = {
    TASK_LABEL: check_v4_256_multi_condition_enable_combiner,
    SOURCE_TASK_ID: check_v4_256_multi_condition_enable_combiner,
    LEGACY_SYMBOL: check_v4_256_multi_condition_enable_combiner,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_256_multi_condition_enable_combiner
