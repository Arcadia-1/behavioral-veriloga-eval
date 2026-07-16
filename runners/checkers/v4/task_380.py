"""Task-specific checker for canonical v4 DUT 380."""
from __future__ import annotations

from ..api import Checker
def _v4_topup_clip01(value: float, low: float = 0.0, high: float = 0.9) -> float:
    return max(low, min(high, value))

def _v4_topup_logic_high(row: dict[str, float], name: str, threshold: float = 0.45) -> bool:
    return float(row.get(name, 0.0)) > threshold

def check_v4_380_am_modulator_source_macro(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_380 empty_trace"
    checked = vout_errors = dbg_errors = valid_errors = clear_errors = 0
    reset_clear = disabled_clear = high_mod_seen = low_mod_seen = False
    reset_seen = enabled_seen = False
    stride = max(1, len(rows) // 240)
    for row in rows[::stride]:
        rst = _v4_topup_logic_high(row, "rst")
        enabled = _v4_topup_logic_high(row, "enable") and not rst
        if not enabled:
            clear = abs(row["vout"] - 0.45) < 0.08 and row["envelope_dbg"] < 0.10 and row["valid"] < 0.10
            if rst:
                reset_seen = True
                reset_clear = reset_clear or clear
                if not clear:
                    clear_errors += 1
            elif enabled_seen:
                # Enable falling is the observed disable event.  Do not tie
                # this contract to a secret final timestamp.
                disabled_clear = disabled_clear or clear
            continue
        enabled_seen = True
        mult = 1.0 + 0.5 * ((float(row["mod_in"]) - 0.45) / 0.45)
        expected_vout = _v4_topup_clip01(0.45 + (float(row["carrier_in"]) - 0.45) * mult)
        expected_dbg = _v4_topup_clip01(mult * 0.45)
        checked += 1
        high_mod_seen = high_mod_seen or mult > 1.05
        low_mod_seen = low_mod_seen or mult < 0.95
        if abs(float(row["vout"]) - expected_vout) > 0.10:
            vout_errors += 1
        if abs(float(row["envelope_dbg"]) - expected_dbg) > 0.10:
            dbg_errors += 1
        if not _v4_topup_logic_high(row, "valid"):
            valid_errors += 1
    ok = checked >= 15 and reset_seen and reset_clear and enabled_seen and disabled_clear and high_mod_seen and low_mod_seen and vout_errors <= 4 and dbg_errors <= 4 and valid_errors == 0 and clear_errors <= 3
    return ok, f"v4_380 checked={checked} reset_seen={reset_seen} reset_clear={reset_clear} disabled_clear={disabled_clear} high_mod_seen={high_mod_seen} low_mod_seen={low_mod_seen} vout_errors={vout_errors} dbg_errors={dbg_errors} valid_errors={valid_errors} clear_errors={clear_errors}"

CHECKER_ID = "v4_380_am_modulator_source_macro"
CHECKER: Checker = check_v4_380_am_modulator_source_macro
