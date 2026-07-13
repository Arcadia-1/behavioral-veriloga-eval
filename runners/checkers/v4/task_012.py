"""Task-specific checker for canonical v4 DUT 012."""
from __future__ import annotations

from checkers.api import Checker
def rising_edges(values: list[float], times: list[float], threshold: float = 0.45) -> list[float]:
    edges: list[float] = []
    for i in range(1, len(values)):
        if values[i - 1] < threshold <= values[i]:
            edges.append(times[i])
    return edges

def check_v4_clock_divider(rows: list[dict[str, float]]) -> tuple[bool, str]:
    """Check a static v4 divider code after its source nodes have settled.

    Spectre and EVAS may emit an initial trace row before DC code sources have
    reached their configured values.  The v3 checker reads that first row,
    which can turn the score deck's code 5 into code 3.  v4's contract uses
    static code sources, so their maximum settled level is the intended code.
    """
    if not rows or not {"clk_in", "rst_n", "clk_out", "lock"}.issubset(rows[0]):
        return False, "missing clk_in/rst_n/clk_out/lock"

    div_cols: list[str] = []
    for idx in range(8):
        col = next((candidate for candidate in (f"div_code_{idx}", f"div_code[{idx}]") if candidate in rows[0]), None)
        if col is None:
            return False, "missing div_code_*"
        div_cols.append(col)

    ratio = sum((1 << idx) for idx, col in enumerate(div_cols) if max(row[col] for row in rows) > 0.45)
    if ratio < 1:
        ratio = 1

    reset_segments: list[tuple[int, int]] = []
    segment_start: int | None = None
    for idx, row in enumerate(rows):
        reset_low = row["rst_n"] < 0.20
        if reset_low and segment_start is None:
            segment_start = idx
        elif not reset_low and segment_start is not None:
            reset_segments.append((segment_start, idx))
            segment_start = None
    if segment_start is not None:
        reset_segments.append((segment_start, len(rows)))
    if not reset_segments:
        return False, "reset_not_observed"

    reset_peaks: list[float] = []
    for start, end in reset_segments:
        settled_start = start + max(1, (end - start) // 3)
        settled_rows = rows[min(settled_start, end - 1):end]
        reset_peaks.append(max(max(row["clk_out"], row["lock"]) for row in settled_rows))
    reset_peak = max(reset_peaks)
    if reset_peak > 0.12:
        return False, f"ratio_code={ratio} reset_not_clear reset_segments={len(reset_segments)} reset_peak={reset_peak:.3f}"

    # Divider phase restarts at reset.  Judge period and lock behavior only in
    # the final post-reset epoch so a legal reset gap is not counted as jitter.
    analysis_start = min(reset_segments[-1][1] + 1, len(rows) - 1)
    analysis_rows = rows[analysis_start:]
    if len(analysis_rows) < 2:
        return False, "not enough post-reset samples"
    times = [row["time"] for row in analysis_rows]
    clk_vals = [row["clk_in"] for row in analysis_rows]
    out_vals = [row["clk_out"] for row in analysis_rows]
    lock_vals = [row["lock"] for row in analysis_rows]
    in_edges = rising_edges(clk_vals, times)
    out_edges = rising_edges(out_vals, times)
    lock_edges = rising_edges(lock_vals, times)
    final_lock_high = lock_vals[-1] > 0.45
    reset_clear = True

    if len(in_edges) < max(8, ratio * 2) or len(out_edges) < 2:
        return False, f"ratio_code={ratio} in_edges={len(in_edges)} out_edges={len(out_edges)} lock_edges={len(lock_edges)} final_lock_high={final_lock_high} not_enough_clock_edges"
    if ratio == 1:
        level_match = sum(1 for ci, co in zip(clk_vals, out_vals) if ((ci > 0.45) == (co > 0.45))) / max(len(rows), 1)
        edge_ratio = len(in_edges) / max(len(out_edges), 1)
        ok = level_match > 0.98 and 0.95 <= edge_ratio <= 1.05 and final_lock_high
        return ok, f"ratio_code=1 in_edges={len(in_edges)} out_edges={len(out_edges)} lock_edges={len(lock_edges)} final_lock_high={final_lock_high} reset_clear={reset_clear} level_match={level_match:.3f} edge_ratio={edge_ratio:.3f}"

    if len(out_edges) < 3:
        return False, f"ratio_code={ratio} in_edges={len(in_edges)} out_edges={len(out_edges)} lock_edges={len(lock_edges)} final_lock_high={final_lock_high} not_enough_clock_edges"
    intervals = [
        sum(1 for edge in in_edges if out_edges[idx - 1] < edge <= out_edges[idx])
        for idx in range(1, len(out_edges))
    ]
    measured = intervals[1:] if len(intervals) > 2 else intervals
    mismatch = [interval for interval in measured if interval != ratio]
    period_match = 1.0 - (len(mismatch) / len(measured))
    hist: dict[int, int] = {}
    for interval in measured:
        hist[interval] = hist.get(interval, 0) + 1
    high_seen = any(value > 0.45 for value in out_vals)
    low_seen = any(value <= 0.45 for value in out_vals)
    ok = not mismatch and final_lock_high and high_seen and low_seen
    return ok, f"ratio_code={ratio} in_edges={len(in_edges)} out_edges={len(out_edges)} lock_edges={len(lock_edges)} final_lock_high={final_lock_high} reset_clear={reset_clear} period_match={period_match:.3f} interval_hist={hist}"

CHECKER_ID = "v4_012_clock_divider"
CHECKER: Checker = check_v4_clock_divider
