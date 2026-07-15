"""Task-specific checker for canonical v4 DUT 233."""
from __future__ import annotations

from ..api import Checker
def _v3_away_from_edges(row_time: float, edge_times: list[float], margin_s: float = 80e-12) -> bool:
    return all(abs(row_time - edge_time) > margin_s for edge_time in edge_times)

def check_v3_vargain_diffamp_clip(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "sigin_p", "sigin_n", "sigctrl_p", "sigctrl_n", "sigout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing vargain diffamp clip signals"
    edge_times: list[float] = []
    for signal in ("sigin_p", "sigin_n", "sigctrl_p", "sigctrl_n"):
        edge_times.extend(
            row["time"]
            for prev, row in zip(rows, rows[1:])
            if abs(row[signal] - prev[signal]) > 1.0e-6
        )
    checked = 0
    saw_hi_clip = False
    saw_lo_clip = False
    saw_linear = False
    max_err = 0.0
    failures: list[str] = []
    stride = max(1, len(rows) // 120)
    for row in rows[::stride]:
        if row["time"] < 0.05e-9 or not _v3_away_from_edges(row["time"], edge_times, margin_s=90e-12):
            continue
        raw = 3.0 * (row["sigctrl_p"] - row["sigctrl_n"]) * (row["sigin_p"] - row["sigin_n"] - 0.05)
        expected = max(-1.0, min(1.0, raw))
        saw_hi_clip = saw_hi_clip or raw > 1.0
        saw_lo_clip = saw_lo_clip or raw < -1.0
        saw_linear = saw_linear or (-1.0 <= raw <= 1.0)
        err = abs(row["sigout"] - expected)
        max_err = max(max_err, err)
        checked += 1
        if err > 0.05:
            failures.append(f"t={row['time'] * 1e9:.3f}ns sigout={row['sigout']:.3f} expected={expected:.3f}")
    if checked < 20 or not (saw_hi_clip and saw_lo_clip and saw_linear):
        return False, f"insufficient_vargain_coverage checked={checked} hi={saw_hi_clip} lo={saw_lo_clip} linear={saw_linear}"
    if failures:
        return False, " ".join(failures[:6])
    return True, f"checked={checked} hi_clip={saw_hi_clip} lo_clip={saw_lo_clip} linear={saw_linear} max_err={max_err:.3f}"

CHECKER_ID = "v4_233_vargain_diffamp_clip"
CHECKER: Checker = check_v3_vargain_diffamp_clip
