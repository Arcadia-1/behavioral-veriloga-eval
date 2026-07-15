"""Task-specific checker for canonical v4 DUT 077."""
from __future__ import annotations

from ..api import Checker
def check_noise_gen(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows or not {"vin_i", "vout_o"}.issubset(rows[0]):
        return False, "missing vin_i/vout_o"
    noises = [r["vout_o"] - r["vin_i"] for r in rows]
    mean = sum(noises) / len(noises)
    var = sum((x - mean) ** 2 for x in noises) / len(noises)
    std = var ** 0.5
    max_abs = max(abs(x) for x in noises)
    ok = 0.025 <= std <= 0.12 and abs(mean) <= 0.025 and 0.05 <= max_abs <= 0.22
    return ok, f"noise_mean={mean:.4f} noise_std={std:.4f} max_abs={max_abs:.4f}"

CHECKER_ID = "v4_077_dither_noise_like_deterministic_source"
CHECKER: Checker = check_noise_gen
