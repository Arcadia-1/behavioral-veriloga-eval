"""Task-specific checker for canonical v4 DUT 027."""
from __future__ import annotations

from ..api import Checker
import re

def rising_edges(values: list[float], times: list[float], threshold: float = 0.45) -> list[float]:
    edges: list[float] = []
    for i in range(1, len(values)):
        if values[i - 1] < threshold <= values[i]:
            edges.append(times[i])
    return edges

def sample_rows_at_or_after_times(
    rows: list[dict[str, float]],
    target_times: list[float],
    *,
    rst_key: str | None = None,
    rst_threshold: float = 0.45,
) -> list[dict[str, float]]:
    """Return rows whose time is the first sample at/after each target time.

    This function is linear in len(rows) + len(target_times). It replaces
    repeated per-target full scans that become O(n^2) on large tran.csv files.
    """
    if not rows or not target_times:
        return []

    sampled: list[dict[str, float]] = []
    row_idx = 0
    n_rows = len(rows)
    for t in target_times:
        while row_idx < n_rows and rows[row_idx]["time"] < t:
            row_idx += 1
        if row_idx >= n_rows:
            break
        row = rows[row_idx]
        if rst_key is None or row.get(rst_key, 0.0) > rst_threshold:
            sampled.append(row)
    return sampled

def indexed_columns(keys: set[str], prefix: str) -> list[str]:
    cols = [k for k in keys if re.fullmatch(rf"{re.escape(prefix)}\d+", k)]
    return sorted(cols, key=lambda name: int(re.search(r"(\d+)$", name).group(1)))

def check_dwa_dem_encoder_release(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "no rows"

    keys = set(rows[0].keys())
    required = {"time", "clk_i", "rst_ni", "ptr_0", "cell_en_0", "code_0"}
    if not required.issubset(keys):
        return False, "missing time/clk_i/rst_ni/ptr_0/cell_en_0/code_0"

    ptr_cols = indexed_columns(keys, "ptr_")
    cell_cols = indexed_columns(keys, "cell_en_")
    code_cols = indexed_columns(keys, "code_")
    if len(ptr_cols) != 16 or len(cell_cols) != 16 or len(code_cols) != 4:
        return False, "expected ptr_0..15, cell_en_0..15, and code_0..3 columns"

    times = [r["time"] for r in rows]
    edge_times = rising_edges([r["clk_i"] for r in rows], times)
    sampled_rows = sample_rows_at_or_after_times(rows, [t + 1.0e-9 for t in edge_times], rst_key="rst_ni")
    if len(sampled_rows) < 5:
        return False, f"insufficient_post_reset_samples count={len(sampled_rows)}"

    ptr = 0
    previous_code: int | None = None
    bad_ptr_rows = 0
    bad_span_rows = 0
    wrap_events = 0
    split_wrap_rows = 0
    active_counts: list[int] = []
    ptr_sequence: list[int] = []

    for row_idx, row in enumerate(sampled_rows):
        row_code = sum(int(row[col] > 0.45) << int(col[5:]) for col in code_cols)
        effective_code = row_code if previous_code is None else previous_code
        prev_ptr = ptr
        ptr = (ptr + effective_code) % 16
        if row_idx > 0 and ptr < prev_ptr:
            wrap_events += 1

        ptr_active = [idx for idx, col in enumerate(ptr_cols) if row[col] > 0.45]
        if ptr_active != [ptr]:
            bad_ptr_rows += 1

        # The release gold emits an MSB span plus the LSB boundary unit, so a
        # code of N drives a contiguous circular run of N+1 active cells ending
        # at the pointer.
        expected_cells = {(ptr - offset) % 16 for offset in range(effective_code + 1)}
        active_cells = {idx for idx, col in enumerate(cell_cols) if row[col] > 0.45}
        active_counts.append(len(active_cells))
        if active_cells != expected_cells:
            bad_span_rows += 1
        if active_cells and (max(active_cells) - min(active_cells) + 1) > len(active_cells):
            split_wrap_rows += 1

        ptr_sequence.append(ptr)
        previous_code = row_code

    ok = (
        bad_ptr_rows == 0
        and bad_span_rows == 0
        and wrap_events >= 2
        and split_wrap_rows >= 2
        and len(set(ptr_sequence)) >= 5
        and max(active_counts) >= 8
    )
    return ok, (
        f"sampled_cycles={len(sampled_rows)} bad_ptr_rows={bad_ptr_rows} "
        f"bad_span_rows={bad_span_rows} ptr_unique={len(set(ptr_sequence))} "
        f"wrap_events={wrap_events} split_wrap_rows={split_wrap_rows} "
        f"max_active_cells={max(active_counts)}"
    )

CHECKER_ID = "v4_027_dwa_dem_encoder"
CHECKER: Checker = check_dwa_dem_encoder_release
