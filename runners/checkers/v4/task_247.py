"""Task-specific checker for canonical v4 DUT 247."""
from __future__ import annotations

from ..api import Checker
def _v3_away_from_edges(row_time: float, edge_times: list[float], margin_s: float = 80e-12) -> bool:
    return all(abs(row_time - edge_time) > margin_s for edge_time in edge_times)

def check_v3_voltage_match_window(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin1", "vin2", "vout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing voltage match window signals"
    change_times: list[float] = []
    for signal in ["vin1", "vin2"]:
        for prev, cur in zip(rows, rows[1:]):
            if abs(cur[signal] - prev[signal]) > 0.01:
                change_times.append(cur["time"])
    match_tol = 0.05
    vh = 0.9
    max_err = 0.0
    checked = 0
    matched = 0
    mismatched = 0
    near_boundary = 0
    for row in rows:
        if row["time"] < 0.15e-9:
            continue
        if not _v3_away_from_edges(row["time"], change_times, 80e-12):
            continue
        diff = abs(row["vin1"] - row["vin2"])
        expected = vh if diff <= match_tol else 0.0
        max_err = max(max_err, abs(row["vout"] - expected))
        checked += 1
        if expected > 0.45:
            matched += 1
        else:
            mismatched += 1
        if 0.02 <= diff <= 0.08:
            near_boundary += 1
    if checked < 20 or matched == 0 or mismatched == 0 or near_boundary == 0:
        return False, (
            f"insufficient_voltage_match_coverage checked={checked} "
            f"matched={matched} mismatched={mismatched} near_boundary={near_boundary}"
        )
    return max_err <= 0.08, (
        f"checked={checked} matched={matched} mismatched={mismatched} "
        f"near_boundary={near_boundary} max_err={max_err:.4f}"
    )

CHECKER_ID = "v4_247_voltage_match_window"
CHECKER: Checker = check_v3_voltage_match_window
