from __future__ import annotations

from ..api import Checker
from ..common.issue109_factory import CheckResult, Row, check_continuous_factory
from .factory_property_diagnostics import append_continuous_property_diagnostics


TASK_LABEL = 'v4_257_phase_mismatch_qualifier'
SOURCE_TASK_ID = 'v3_348_phase_mismatch_qualifier'
LEGACY_SYMBOL = '348-phase-mismatch-qualifier'


def check_v4_257_phase_mismatch_qualifier(rows: list[Row]) -> CheckResult:
    """Check v4_257_phase_mismatch_qualifier: Phase Mismatch Qualifier continuous phase behavior."""
    ok, note = check_continuous_factory(rows, mode='phase', task_name=TASK_LABEL)
    return ok, append_continuous_property_diagnostics(
        rows,
        note,
        mode='phase',
        normalization_property_id='P_MEASURE_ANALOG_INPUTS_RELATIVE_TO_THE',
        function_property_id='P_COMPUTE_CORE_CLIP01_0_5_X0',
    )


CHECKS = {
    TASK_LABEL: check_v4_257_phase_mismatch_qualifier,
    SOURCE_TASK_ID: check_v4_257_phase_mismatch_qualifier,
    LEGACY_SYMBOL: check_v4_257_phase_mismatch_qualifier,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_257_phase_mismatch_qualifier
