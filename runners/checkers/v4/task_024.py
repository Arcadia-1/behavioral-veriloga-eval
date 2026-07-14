"""Task-specific checker for canonical v4 DUT 024."""
from __future__ import annotations

from checkers.api import Checker
def check_sample_hold(rows: list[dict[str, float]]) -> tuple[bool, str]:
    """S&H: output steps at clock edges, held between them."""
    if not rows or not {"in", "clk", "out"}.issubset(rows[0]):
        return False, "missing in/clk/out columns"
    vth = 0.45
    times = [r["time"] for r in rows]
    clk  = [r["clk"]  for r in rows]
    vin  = [r["in"]   for r in rows]
    vout = [r["out"]  for r in rows]
    edge_idx = [i for i in range(1, len(clk)) if clk[i - 1] <= vth < clk[i]]
    if len(edge_idx) < 10:
        return False, f"too_few_clock_edges={len(edge_idx)}"
    # Check hold stability: for 3 consecutive hold windows, skip 2ns after edge, stop 2ns before next
    for i in range(min(3, len(edge_idx) - 1)):
        t_start = times[edge_idx[i]] + 2e-9
        t_end   = times[edge_idx[i + 1]] - 2e-9
        window = [vout[j] for j in range(edge_idx[i], edge_idx[i + 1])
                  if t_start <= times[j] <= t_end]
        if len(window) < 2:
            continue
        jitter = max(window) - min(window)
        if jitter > 0.02:
            return False, f"output_not_held jitter={jitter:.4f}V"
    # Output should track input at edges (settled 2ns after edge)
    mismatches = 0
    for idx in edge_idx[:20]:
        t_settle = times[idx] + 2e-9
        settle_idx = next((j for j in range(idx, len(times)) if times[j] >= t_settle), idx)
        if abs(vout[settle_idx] - vin[idx]) > 0.015:
            mismatches += 1
    if mismatches > 4:
        return False, f"sample_mismatch={mismatches}/20"
    return True, f"edges={len(edge_idx)} hold_ok"

CHECKER_ID = "v4_024_clocked_sample_and_hold"
CHECKER: Checker = check_sample_hold
