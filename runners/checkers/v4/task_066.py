"""Task-specific checker for canonical v4 DUT 066."""
from __future__ import annotations

from ..api import Checker
def check_configurable_polarity_edge_detector(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "sig", "rise_en", "pulse"}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing[:12])
    edge_times: list[float] = []
    last_sig = rows[0]["sig"] > 0.45
    for row in rows[1:]:
        sig = row["sig"] > 0.45
        rise_mode = row["rise_en"] > 0.45
        edge = (not last_sig and sig) if rise_mode else (last_sig and not sig)
        if edge:
            edge_times.append(row["time"])
        last_sig = sig
    missed = 0
    for edge_t in edge_times:
        if not any(edge_t <= row["time"] <= edge_t + 3e-9 and row["pulse"] > 0.45 for row in rows):
            missed += 1
    false_pulses = 0
    for row in rows:
        if row["pulse"] <= 0.45:
            continue
        if not any(edge_t <= row["time"] <= edge_t + 4e-9 for edge_t in edge_times):
            false_pulses += 1
    return len(edge_times) >= 3 and missed == 0 and false_pulses == 0, (
        f"events={len(edge_times)} missed={missed} false_pulses={false_pulses}"
    )

CHECKER_ID = "v4_066_configurable_polarity_edge_detector"
CHECKER: Checker = check_configurable_polarity_edge_detector
