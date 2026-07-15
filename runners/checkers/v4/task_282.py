from __future__ import annotations

from ..api import Checker
from ..common.issue109_split import check_clocked


TASK_LABEL = "v4_282_enable_saturating_ready_counter"
SOURCE_TASK_ID = "v3_418_enable_saturating_ready_counter"
TRACE_SIGNALS = ("time", "clk", "rst", "in0", "in1", "in2", "in3", "ctrl0", "ctrl1", "vdd", "vss", "en", "out", "flag", "metric")
PROPERTIES = (
    "enable-qualified rising-clock ready counter",
    "count saturates at 4 when x0 > 0.25 and x1 > 0.20, otherwise clears",
    "reset, disabled, and illegal supply span clear count and observables",
)


def check_v4_282_enable_saturating_ready_counter(rows: list[dict[str, float]]) -> tuple[bool, str]:
    return check_clocked(rows, "counter", TASK_LABEL)


CHECKS = {
    TASK_LABEL: check_v4_282_enable_saturating_ready_counter,
    SOURCE_TASK_ID: check_v4_282_enable_saturating_ready_counter,
    "418-enable-saturating-ready-counter": check_v4_282_enable_saturating_ready_counter,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_282_enable_saturating_ready_counter
