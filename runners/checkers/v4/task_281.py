from __future__ import annotations

from ..api import Checker
from ..common.issue109_split import check_clocked


TASK_LABEL = "v4_281_async_reset_event_counter"
SOURCE_TASK_ID = "v3_417_async_reset_event_counter"
TRACE_SIGNALS = ("time", "clk", "rst", "in0", "in1", "in2", "in3", "ctrl0", "ctrl1", "vdd", "vss", "en", "out", "flag", "metric")
PROPERTIES = (
    "rising clock and reset events clear or update a saturating count",
    "count increments only when x0 > 0.25 and x1 > 0.20",
    "out encodes count/4, flag asserts for count >= 3, metric is abs(x0-x1)",
)


def check_v4_281_async_reset_event_counter(rows: list[dict[str, float]]) -> tuple[bool, str]:
    return check_clocked(rows, "counter", TASK_LABEL)


CHECKS = {
    TASK_LABEL: check_v4_281_async_reset_event_counter,
    SOURCE_TASK_ID: check_v4_281_async_reset_event_counter,
    "417-async-reset-event-counter": check_v4_281_async_reset_event_counter,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_281_async_reset_event_counter
