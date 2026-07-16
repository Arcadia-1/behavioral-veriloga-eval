"""Task-specific checker for canonical v4 DUT 077."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import diagnostic, pass_note, require_signals


PROPERTY_IDS = (
    "P_PERIODIC_UPDATE",
    "P_SAMPLE_HOLD",
    "P_ADDITIVE_OUTPUT",
    "P_DETERMINISTIC_SEQUENCE",
    "P_ZERO_MEAN_DITHER",
)


def check_noise_gen(rows: list[dict[str, float]]) -> tuple[bool, str]:
    missing = require_signals(rows, {"vin_i", "vout_o"}, "P_ADDITIVE_OUTPUT")
    if missing is not None:
        return False, missing
    noises = [r["vout_o"] - r["vin_i"] for r in rows]
    mean = sum(noises) / len(noises)
    var = sum((x - mean) ** 2 for x in noises) / len(noises)
    std = var ** 0.5
    max_abs = max(abs(x) for x in noises)
    ok = 0.025 <= std <= 0.12 and abs(mean) <= 0.025 and 0.05 <= max_abs <= 0.22
    note = f"noise_mean={mean:.4f} noise_std={std:.4f} max_abs={max_abs:.4f}"
    if not ok:
        return False, diagnostic(
            "P_ZERO_MEAN_DITHER",
            "value_mismatch",
            expected="std:0.025..0.12,abs_mean<=0.025,max_abs:0.05..0.22",
            observed=f"std:{std:.4f},mean:{mean:.4f},max_abs:{max_abs:.4f}",
            event="full_trace",
        )
    return True, pass_note(PROPERTY_IDS, note)

CHECKER_ID = "v4_077_dither_noise_like_deterministic_source"
CHECKER: Checker = check_noise_gen
