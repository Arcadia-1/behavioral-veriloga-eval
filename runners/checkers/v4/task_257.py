from __future__ import annotations

from ..api import Checker
from ..common.issue109_factory import CheckResult, Row, check_continuous_factory


TASK_LABEL = 'v4_257_phase_mismatch_qualifier'
SOURCE_TASK_ID = 'v3_348_phase_mismatch_qualifier'
LEGACY_SYMBOL = '348-phase-mismatch-qualifier'


def check_v4_257_phase_mismatch_qualifier(rows: list[Row]) -> CheckResult:
    """Check v4_257_phase_mismatch_qualifier: Phase Mismatch Qualifier continuous phase behavior."""
    return check_continuous_factory(rows, mode='phase', task_name=TASK_LABEL)


CHECKS = {
    TASK_LABEL: check_v4_257_phase_mismatch_qualifier,
    SOURCE_TASK_ID: check_v4_257_phase_mismatch_qualifier,
    LEGACY_SYMBOL: check_v4_257_phase_mismatch_qualifier,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_257_phase_mismatch_qualifier
