from __future__ import annotations

from checkers.api import Checker
from checkers.common.issue109_split import check_continuous


TASK_LABEL = "v4_286_explicit_replicated_stage_chain"
SOURCE_TASK_ID = "v3_449_explicit_replicated_stage_chain"
TRACE_SIGNALS = ("time", "in0", "in1", "in2", "in3", "ctrl0", "ctrl1", "vdd", "vss", "en", "out", "flag", "metric")
PROPERTIES = (
    "explicit weighted stage-chain composition over x0..x3",
    "core = 0.36*x0 + 0.28*x1 + 0.18*x2 + 0.10*x3 + 0.04",
    "flag asserts when composed core exceeds 0.48 and metric tracks abs(x0-x1)/0.55",
)


def check_v4_286_explicit_replicated_stage_chain(rows: list[dict[str, float]]) -> tuple[bool, str]:
    return check_continuous(rows, "sum", TASK_LABEL)


CHECKS = {
    TASK_LABEL: check_v4_286_explicit_replicated_stage_chain,
    SOURCE_TASK_ID: check_v4_286_explicit_replicated_stage_chain,
    "449-explicit-replicated-stage-chain": check_v4_286_explicit_replicated_stage_chain,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_286_explicit_replicated_stage_chain
