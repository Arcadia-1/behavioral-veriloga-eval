"""Task-specific checker for canonical v4 DUT 224."""
from __future__ import annotations

from checkers.api import Checker
import math

def _v3_missing_columns(rows: list[dict[str, float]], required: set[str]) -> str | None:
    if not rows:
        return "empty_waveform"
    missing = sorted(required - set(rows[0]))
    if missing:
        return "missing_columns=" + ",".join(missing)
    return None

def check_v3_coarse_qtz_3bit_residue(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "d0", "d1", "d2", "vres"}
    missing = _v3_missing_columns(rows, required)
    if missing:
        return False, missing

    max_bit_error = 0.0
    max_res_error = 0.0
    checked = 0
    saw_low_clip = False
    saw_high_clip = False
    saw_internal = False
    stride = max(1, len(rows) // 80)
    for idx in range(1, len(rows) - 1, stride):
        row = rows[idx]
        prev_row = rows[idx - 1]
        next_row = rows[idx + 1]
        local_vin_span = max(
            abs(prev_row["vin"] - row["vin"]),
            abs(next_row["vin"] - row["vin"]),
        )
        if local_vin_span > 1.0e-6:
            continue
        vin = row["vin"]
        vclip = max(-1.0, min(1.0, vin))
        saw_low_clip = saw_low_clip or vin < -1.0
        saw_high_clip = saw_high_clip or vin > 1.0
        saw_internal = saw_internal or (-0.95 < vin < 0.95)
        lsb = 0.25
        code = math.floor(((vclip + 1.0) / lsb) + 0.5)
        code = max(0, min(7, code))
        vq = code * lsb - 1.0
        expected = {
            "d0": 1.0 if (code & 1) else 0.0,
            "d1": 1.0 if ((code >> 1) & 1) else 0.0,
            "d2": 1.0 if ((code >> 2) & 1) else 0.0,
            "vres": vclip - vq,
        }
        for bit_name in ("d0", "d1", "d2"):
            max_bit_error = max(max_bit_error, abs(row[bit_name] - expected[bit_name]))
        max_res_error = max(max_res_error, abs(row["vres"] - expected["vres"]))
        checked += 1
    if checked < 8:
        return False, f"too_few_quantizer_samples={checked}"
    ok = max_bit_error <= 0.09 and max_res_error <= 0.035
    return (
        ok,
        f"checked={checked} low_clip={saw_low_clip} high_clip={saw_high_clip} "
        f"internal={saw_internal} max_bit_error={max_bit_error:.5f} max_res_error={max_res_error:.5f}",
    )

CHECKER_ID = "v4_224_coarse_qtz_3bit_residue"
CHECKER: Checker = check_v3_coarse_qtz_3bit_residue
