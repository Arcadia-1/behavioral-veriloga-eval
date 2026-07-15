from __future__ import annotations

from ..api import Checker
from ..common.issue109_split import check_clocked


TASK_LABEL = "v4_290_bounded_window_accumulator"
SOURCE_TASK_ID = "v3_459_bounded_window_accumulator"
TRACE_SIGNALS = ("time", "clk", "rst", "in0", "in1", "in2", "in3", "ctrl0", "ctrl1", "vdd", "vss", "en", "out", "flag", "metric")
PROPERTIES = (
    "clocked bounded sampled-window accumulator",
    "aux = clip01(abs(x0-x1)+0.35*c0) and acc = clip01(0.62*acc+0.32*aux)",
    "reset, disabled, and bad supply clear state; valid samples hold between clock edges",
)


def check_v4_290_bounded_window_accumulator(rows: list[dict[str, float]]) -> tuple[bool, str]:
    return check_clocked(rows, "accum", TASK_LABEL)


CHECKS = {
    TASK_LABEL: check_v4_290_bounded_window_accumulator,
    SOURCE_TASK_ID: check_v4_290_bounded_window_accumulator,
    "459-bounded-window-accumulator": check_v4_290_bounded_window_accumulator,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_290_bounded_window_accumulator
