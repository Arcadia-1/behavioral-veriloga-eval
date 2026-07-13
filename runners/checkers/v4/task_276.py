from __future__ import annotations

from checkers.api import Checker
from checkers.common.issue109_split import check_clocked


TASK_LABEL = "v4_276_bounded_tail_dither_shaper"
SOURCE_TASK_ID = "v3_395_bounded_tail_dither_shaper"
TRACE_SIGNALS = ("time", "clk", "rst", "in0", "in1", "in2", "in3", "ctrl0", "ctrl1", "vdd", "vss", "en", "out", "flag", "metric")
PROPERTIES = (
    "bounded-tail update uses x0/x1/c0 and preserves in2/in3/ctrl1 only as interface inputs",
    "valid rising-clock samples update acc and metric from aux",
    "reset, low enable, and out-of-range supply clear prior accumulator state",
)


def check_v4_276_bounded_tail_dither_shaper(rows: list[dict[str, float]]) -> tuple[bool, str]:
    return check_clocked(rows, "accum", TASK_LABEL)


CHECKS = {
    TASK_LABEL: check_v4_276_bounded_tail_dither_shaper,
    SOURCE_TASK_ID: check_v4_276_bounded_tail_dither_shaper,
    "395-bounded-tail-dither-shaper": check_v4_276_bounded_tail_dither_shaper,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_276_bounded_tail_dither_shaper
