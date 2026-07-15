from __future__ import annotations

from ..api import Checker
from ..common.issue109_factory import CheckResult, Row, check_continuous_factory


TASK_LABEL = 'v4_255_reset_polarity_qualifier'
SOURCE_TASK_ID = 'v3_346_reset_polarity_qualifier'
LEGACY_SYMBOL = '346-reset-polarity-qualifier'


def check_v4_255_reset_polarity_qualifier(rows: list[Row]) -> CheckResult:
    """Check v4_255_reset_polarity_qualifier: Reset Polarity Qualifier continuous window behavior."""
    return check_continuous_factory(rows, mode='window', task_name=TASK_LABEL)


CHECKS = {
    TASK_LABEL: check_v4_255_reset_polarity_qualifier,
    SOURCE_TASK_ID: check_v4_255_reset_polarity_qualifier,
    LEGACY_SYMBOL: check_v4_255_reset_polarity_qualifier,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_255_reset_polarity_qualifier
