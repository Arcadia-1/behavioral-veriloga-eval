from __future__ import annotations

from checkers.api import Checker
from checkers.common.issue109_split import check_clocked


TASK_LABEL = "v4_283_mode_latch_calibration_gate"
SOURCE_TASK_ID = "v3_420_mode_latch_calibration_gate"
TRACE_SIGNALS = ("time", "clk", "rst", "in0", "in1", "in2", "in3", "ctrl0", "ctrl1", "vdd", "vss", "en", "out", "flag", "metric")
PROPERTIES = (
    "clocked calibration mode latch gated by ctrl0",
    "when c0 > 0.45, held output updates to 0.70*x0 + 0.30*x1",
    "when c0 <= 0.45, out holds and metric compares held output against x2",
)


def check_v4_283_mode_latch_calibration_gate(rows: list[dict[str, float]]) -> tuple[bool, str]:
    return check_clocked(rows, "latch", TASK_LABEL)


CHECKS = {
    TASK_LABEL: check_v4_283_mode_latch_calibration_gate,
    SOURCE_TASK_ID: check_v4_283_mode_latch_calibration_gate,
    "420-mode-latch-calibration-gate": check_v4_283_mode_latch_calibration_gate,
}

CHECKER_ID = TASK_LABEL
CHECKER: Checker = check_v4_283_mode_latch_calibration_gate
