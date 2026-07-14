"""Task-specific checker for canonical v4 DUT 243."""
from __future__ import annotations

from checkers.api import Checker
def check_v3_subradix_dac10(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vd9", "vd8", "vd7", "vd6", "vd5", "vd4", "vd3", "vd2", "vd1", "vd0", "vout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing subradix dac10 signals"
    weights = {f"vd{i}": 1.8 ** i for i in range(10)}
    denom = sum(weights.values())
    max_err = 0.0
    checked = 0
    varied = set()
    for row in rows:
        if row["time"] < 0.15e-9:
            continue
        code = 0.0
        for name, weight in weights.items():
            if row[name] > 0.45:
                code += weight
                varied.add(name)
        expected = code / denom
        max_err = max(max_err, abs(row["vout"] - expected))
        checked += 1
    if checked < 20 or len(varied) < 3:
        return False, f"insufficient_subradix_coverage checked={checked} active_bits={sorted(varied)}"
    return max_err <= 0.025, f"checked={checked} active_bits={sorted(varied)} max_err={max_err:.5f}"

CHECKER_ID = "v4_243_subradix_dac10"
CHECKER: Checker = check_v3_subradix_dac10
