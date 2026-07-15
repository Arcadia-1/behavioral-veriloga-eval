"""Task-specific checker for canonical v4 DUT 023."""
from __future__ import annotations

from ..api import Checker
def check_flash_adc_3b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    """3-bit flash ADC: all 8 codes present, monotonic with ramp input."""
    if not rows or not {"vin", "clk", "dout2", "dout1", "dout0"}.issubset(rows[0]):
        return False, "missing vin/clk/dout2/dout1/dout0"
    vth = 0.45
    clk = [r["clk"] for r in rows]
    edge_idx = [i for i in range(1, len(clk)) if clk[i - 1] <= vth < clk[i]]
    if len(edge_idx) < 20:
        return False, f"too_few_edges={len(edge_idx)}"
    codes = []
    for idx in edge_idx:
        settle = min(idx + 5, len(rows) - 1)
        c = (int(rows[settle]["dout2"] > vth) << 2 |
             int(rows[settle]["dout1"] > vth) << 1 |
             int(rows[settle]["dout0"] > vth))
        codes.append(c)
    unique = set(codes)
    if len(unique) < 8:
        return False, f"only_{len(unique)}_codes (need 8)"
    # monotonicity: fewer than 5% reversals
    reversals = sum(1 for i in range(1, len(codes)) if codes[i] < codes[i - 1] - 1)
    if reversals > len(codes) * 0.05:
        return False, f"not_monotonic reversals={reversals}"
    return True, f"codes={len(unique)}/8 reversals={reversals}"

CHECKER_ID = "v4_023_clocked_adc_quantizer"
CHECKER: Checker = check_flash_adc_3b
