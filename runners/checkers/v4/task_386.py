"""Task-specific checker for canonical v4 DUT 386."""
from __future__ import annotations

from ..api import Checker


def _v4_topup_clip01(value: float, low: float = 0.0, high: float = 0.9) -> float:
    return max(low, min(high, value))


def _level(row: dict[str, float], name: str, threshold: float = 0.45) -> bool | None:
    value = float(row.get(name, 0.0))
    if 0.1 < value < 0.8:
        return None
    return value > threshold


def _property_note(property_id: str, mismatch_count: int, expected: str, observed: str) -> str:
    return (
        f"{property_id} mismatch_count={mismatch_count} "
        f"expected={expected} observed={observed}"
    )

def check_v4_945_pa_gain_compression_ampm_macro(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, _property_note("P_TRACE_CONTRACT", 1, "non_empty_trace", "empty_trace")
    checked = vout_errors = gain_errors = phase_errors = flag_errors = clear_errors = 0
    reset_clear = disabled_clear = compressed_seen = uncompressed_seen = False
    for row in rows[::6]:
        rst = _level(row, "rst")
        enable = _level(row, "enable")
        if rst is None or enable is None:
            continue
        enabled = enable and not rst
        if not enabled:
            clear = abs(row["vout"] - 0.45) < 0.08 and row["gain_metric"] < 0.10 and row["phase_metric"] < 0.10 and row["compressed"] < 0.10
            if rst and clear:
                reset_clear = True
            if not rst and not enable and clear:
                disabled_clear = True
            if not clear:
                clear_errors += 1
            continue
        excess = max(0.0, abs(float(row["envelope"]) - 0.45) - 0.2)
        gain = 3.0 / (1.0 + excess / 0.25)
        expected_vout = _v4_topup_clip01(0.45 + gain * (float(row["vin"]) - 0.45))
        expected_gain = _v4_topup_clip01(0.9 * gain / 3.0)
        expected_phase = _v4_topup_clip01(0.9 * excess / 0.45)
        expected_flag = gain < 3.0 * 0.85
        checked += 1
        compressed_seen = compressed_seen or expected_flag
        uncompressed_seen = uncompressed_seen or not expected_flag
        if abs(float(row["vout"]) - expected_vout) > 0.12:
            vout_errors += 1
        if abs(float(row["gain_metric"]) - expected_gain) > 0.10:
            gain_errors += 1
        if abs(float(row["phase_metric"]) - expected_phase) > 0.10:
            phase_errors += 1
        if bool(_level(row, "compressed")) != expected_flag:
            flag_errors += 1
    coverage_errors = int(not compressed_seen) + int(not uncompressed_seen)
    ok = (
        checked >= 15
        and reset_clear
        and disabled_clear
        and coverage_errors == 0
        and vout_errors <= 4
        and gain_errors <= 4
        and phase_errors <= 4
        and flag_errors <= 3
        and clear_errors <= 3
    )
    notes = [
        _property_note(
            "P_RESET_DISABLE_CLEAR",
            clear_errors + int(not reset_clear) + int(not disabled_clear),
            "vout=0.45,metrics=0,compressed=0_when_inactive",
            f"reset_clear={reset_clear},disabled_clear={disabled_clear}",
        ),
        _property_note("P_PA_OUTPUT_TRANSFER", vout_errors, "vout=bounded_gain(vin,envelope)", f"checked={checked}"),
        _property_note("P_GAIN_METRIC", gain_errors, "gain_metric=bounded_gain", f"errors={gain_errors}"),
        _property_note("P_PHASE_METRIC", phase_errors, "phase_metric=bounded_excess", f"errors={phase_errors}"),
        _property_note("P_COMPRESSION_FLAG", flag_errors, "flag=1_when_compressed", f"errors={flag_errors}"),
        _property_note("P_COMPRESSION_COVERAGE", coverage_errors, "compressed_and_uncompressed_regions", f"compressed={compressed_seen},uncompressed={uncompressed_seen}"),
    ]
    return ok, "; ".join(notes)

CHECKER_ID = "v4_386_pa_gain_compression_ampm_macro"
CHECKER: Checker = check_v4_945_pa_gain_compression_ampm_macro
