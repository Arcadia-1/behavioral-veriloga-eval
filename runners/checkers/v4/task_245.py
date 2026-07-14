"""Task-specific checker for canonical v4 DUT 245."""
from __future__ import annotations

from checkers.api import Checker
import math

def _v3_away_from_edges(row_time: float, edge_times: list[float], margin_s: float = 80e-12) -> bool:
    return all(abs(row_time - edge_time) > margin_s for edge_time in edge_times)

def check_v3_cal4bit_modulo(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "ain", "d0", "d1", "d2", "d3"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing cal4bit modulo signals"
    code_by_time = [(row["time"], max(0, min(15, math.floor(row["ain"])))) for row in rows]
    code_change_times = [
        t
        for (prev_t, prev_code), (t, code) in zip(code_by_time, code_by_time[1:])
        if code != prev_code and t >= prev_t
    ]
    max_err = 0.0
    checked = 0
    codes = set()
    for row in rows:
        if row["time"] < 0.15e-9:
            continue
        if not _v3_away_from_edges(row["time"], code_change_times, 80e-12):
            continue
        code = math.floor(row["ain"])
        code = max(0, min(15, code))
        codes.add(code)
        expected = {
            "d0": 0.9 if (code & 1) else 0.0,
            "d1": 0.9 if ((code >> 1) & 1) else 0.0,
            "d2": 0.9 if ((code >> 2) & 1) else 0.0,
            "d3": 0.9 if ((code >> 3) & 1) else 0.0,
        }
        for signal, want in expected.items():
            max_err = max(max_err, abs(row[signal] - want))
        checked += 1
    if checked < 20 or len(codes) < 3 or 0 not in codes or 15 not in codes:
        return False, f"insufficient_cal4bit_coverage checked={checked} codes={sorted(codes)}"
    return max_err <= 0.08, f"checked={checked} codes={sorted(codes)} max_err={max_err:.4f}"

CHECKER_ID = "v4_245_cal4bit_modulo"
CHECKER: Checker = check_v3_cal4bit_modulo
