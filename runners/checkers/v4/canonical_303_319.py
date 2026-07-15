"""Deterministic registry slice for canonical v4 DUTs 303-319."""
from __future__ import annotations

from ..api import Checker
from .task_303 import CHECKER as CHECKER_303, CHECKER_ID as CHECKER_ID_303
from .task_304 import CHECKER as CHECKER_304, CHECKER_ID as CHECKER_ID_304
from .task_305 import CHECKER as CHECKER_305, CHECKER_ID as CHECKER_ID_305
from .task_306 import CHECKER as CHECKER_306, CHECKER_ID as CHECKER_ID_306
from .task_307 import CHECKER as CHECKER_307, CHECKER_ID as CHECKER_ID_307
from .task_308 import CHECKER as CHECKER_308, CHECKER_ID as CHECKER_ID_308
from .task_309 import CHECKER as CHECKER_309, CHECKER_ID as CHECKER_ID_309
from .task_310 import CHECKER as CHECKER_310, CHECKER_ID as CHECKER_ID_310
from .task_311 import CHECKER as CHECKER_311, CHECKER_ID as CHECKER_ID_311
from .task_312 import CHECKER as CHECKER_312, CHECKER_ID as CHECKER_ID_312
from .task_313 import CHECKER as CHECKER_313, CHECKER_ID as CHECKER_ID_313
from .task_314 import CHECKER as CHECKER_314, CHECKER_ID as CHECKER_ID_314
from .task_315 import CHECKER as CHECKER_315, CHECKER_ID as CHECKER_ID_315
from .task_316 import CHECKER as CHECKER_316, CHECKER_ID as CHECKER_ID_316
from .task_317 import CHECKER as CHECKER_317, CHECKER_ID as CHECKER_ID_317
from .task_318 import CHECKER as CHECKER_318, CHECKER_ID as CHECKER_ID_318
from .task_319 import CHECKER as CHECKER_319, CHECKER_ID as CHECKER_ID_319


CHECKERS: dict[str, Checker] = {
    CHECKER_ID_303: CHECKER_303,
    CHECKER_ID_304: CHECKER_304,
    CHECKER_ID_305: CHECKER_305,
    CHECKER_ID_306: CHECKER_306,
    CHECKER_ID_307: CHECKER_307,
    CHECKER_ID_308: CHECKER_308,
    CHECKER_ID_309: CHECKER_309,
    CHECKER_ID_310: CHECKER_310,
    CHECKER_ID_311: CHECKER_311,
    CHECKER_ID_312: CHECKER_312,
    CHECKER_ID_313: CHECKER_313,
    CHECKER_ID_314: CHECKER_314,
    CHECKER_ID_315: CHECKER_315,
    CHECKER_ID_316: CHECKER_316,
    CHECKER_ID_317: CHECKER_317,
    CHECKER_ID_318: CHECKER_318,
    CHECKER_ID_319: CHECKER_319,
}


def register_checkers_303_319(checks: dict[str, Checker]) -> list[str]:
    duplicate_ids = sorted(set(checks).intersection(CHECKERS))
    if duplicate_ids:
        raise ValueError(f"duplicate checker ids: {duplicate_ids}")
    checks.update(CHECKERS)
    return sorted(CHECKERS)
