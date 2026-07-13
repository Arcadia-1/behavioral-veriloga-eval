from __future__ import annotations

from checkers.api import Checker
from checkers.common.issue109_split import check_continuous


TASK_LABEL = "v4_280_ready_reduction_fault_monitor"
SOURCE_TASK_ID = "v3_416_ready_reduction_fault_monitor"
TRACE_SIGNALS = ("time", "in0", "in1", "in2", "in3", "ctrl0", "ctrl1", "vdd", "vss", "en", "out", "flag", "metric")
PROPERTIES = (
    "continuous local-rail normalization",
    "readiness reduction counts x0..x3 above 0.50",
    "out/metric encode count/4 and flag marks count >= 3 as the fault-ready condition",
)


def check_v4_280_ready_reduction_fault_monitor(rows: list[dict[str, float]]) -> tuple[bool, str]:
    return check_continuous(rows, "reduction", TASK_LABEL)


CHECKS = {
    TASK_LABEL: check_v4_280_ready_reduction_fault_monitor,
    SOURCE_TASK_ID: check_v4_280_ready_reduction_fault_monitor,
    "416-ready-reduction-fault-monitor": check_v4_280_ready_reduction_fault_monitor,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_280_ready_reduction_fault_monitor
