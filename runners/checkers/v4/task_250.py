from __future__ import annotations

from checkers.api import Checker
from checkers.common.issue109_factory import CheckResult, Row, check_continuous_factory
from checkers.v4.factory_property_diagnostics import append_continuous_property_diagnostics


TASK_LABEL = 'v4_250_rail_referenced_gain_buffer'
SOURCE_TASK_ID = 'v3_341_rail_referenced_gain_buffer'
LEGACY_SYMBOL = '341-rail-referenced-gain-buffer'


def check_v4_250_rail_referenced_gain_buffer(rows: list[Row]) -> CheckResult:
    """Check v4_250_rail_referenced_gain_buffer: Rail Referenced Gain Buffer continuous gain behavior."""
    ok, note = check_continuous_factory(rows, mode='gain', task_name=TASK_LABEL)
    return ok, append_continuous_property_diagnostics(
        rows,
        note,
        mode='gain',
        normalization_property_id='P_MEASURE_ANALOG_INPUTS_RELATIVE_TO_THE',
        function_property_id='P_COMPUTE_THE_RAIL_REFERENCED_BUFFER_VALUE',
    )


CHECKS = {
    TASK_LABEL: check_v4_250_rail_referenced_gain_buffer,
    SOURCE_TASK_ID: check_v4_250_rail_referenced_gain_buffer,
    LEGACY_SYMBOL: check_v4_250_rail_referenced_gain_buffer,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_250_rail_referenced_gain_buffer
