from __future__ import annotations

from checkers.api import Checker
from checkers.common.issue109_factory import CheckResult, Row, check_continuous_factory


TASK_LABEL = 'v4_266_local_domain_buffer_translator'
SOURCE_TASK_ID = 'v3_357_local_domain_buffer_translator'
LEGACY_SYMBOL = '357-local-domain-buffer-translator'


def check_v4_266_local_domain_buffer_translator(rows: list[Row]) -> CheckResult:
    """Check v4_266_local_domain_buffer_translator: Local Domain Buffer Translator continuous translate behavior."""
    return check_continuous_factory(rows, mode='translate', task_name=TASK_LABEL)


CHECKS = {
    TASK_LABEL: check_v4_266_local_domain_buffer_translator,
    SOURCE_TASK_ID: check_v4_266_local_domain_buffer_translator,
    LEGACY_SYMBOL: check_v4_266_local_domain_buffer_translator,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_266_local_domain_buffer_translator
