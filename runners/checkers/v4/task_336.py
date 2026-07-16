"""Task-specific checker for canonical v4 DUT 336."""
from __future__ import annotations

from ..api import Checker
from .diagnostics import with_diagnostic_contract
def _v4_topup_logic_high(row: dict[str, float], name: str, threshold: float = 0.45) -> bool:
    return float(row.get(name, 0.0)) > threshold

def _v4_rising(prev_v: float, now_v: float, vth: float = 0.45) -> bool:
    return now_v > vth and prev_v <= vth

def _v4_batch001_first_after(rows: list[dict[str, float]], target_time: float) -> dict[str, float] | None:
    for row in rows:
        if float(row["time"]) >= target_time:
            return row
    return None

def check_v4_1034_rf_envelope_detector_attack_release(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1034 empty_trace"
    env = 0.0
    prev_clk = float(rows[0].get("clk", 0.0))
    checked = env_errors = attack_errors = valid_errors = clear_errors = 0
    reset_clear = disabled_clear = attack_seen = release_seen = False
    ever_enabled = False
    disable_time: float | None = None
    for row in rows:
        t = float(row["time"])
        rst = _v4_topup_logic_high(row, "rst")
        enabled = _v4_topup_logic_high(row, "enable") and not rst
        if not enabled:
            env = 0.0
            clear = row["envelope"] < 0.10 and row["attack_metric"] < 0.10 and row["valid"] < 0.10
            reset_clear = reset_clear or (rst and clear)
            disabled = ever_enabled and not _v4_topup_logic_high(row, "enable")
            if disabled and disable_time is None:
                disable_time = t
            disabled_ready = (
                disabled
                and disable_time is not None
                and t >= disable_time + 0.7e-9
            )
            disabled_clear = disabled_clear or (disabled_ready and clear)
            if (rst or disabled_ready) and not clear:
                clear_errors += 1
            prev_clk = float(row["clk"])
            continue
        ever_enabled = True
        disable_time = None
        if _v4_rising(prev_clk, float(row["clk"])):
            mag = min(0.9, abs(float(row["vin"]) - 0.45) * 2.0)
            attacking = mag > env
            env = min(mag, env + 0.120) if attacking else max(mag, env - 0.030)
            sample = _v4_batch001_first_after(rows, t + 0.7e-9)
            if sample is not None:
                checked += 1
                attack_seen = attack_seen or attacking
                release_seen = release_seen or (not attacking)
                if abs(float(sample["envelope"]) - env) > 0.06:
                    env_errors += 1
                if (_v4_topup_logic_high(sample, "attack_metric") != attacking):
                    attack_errors += 1
                if not _v4_topup_logic_high(sample, "valid"):
                    valid_errors += 1
        prev_clk = float(row["clk"])
    ok = checked >= 6 and reset_clear and disabled_clear and attack_seen and release_seen and env_errors == 0 and attack_errors <= 1 and valid_errors == 0 and clear_errors <= 3
    return ok, (
        f"v4_1034 checked={checked} reset_clear={reset_clear} disabled_clear={disabled_clear} "
        f"attack_seen={attack_seen} release_seen={release_seen} env_errors={env_errors} "
        f"attack_errors={attack_errors} valid_errors={valid_errors} clear_errors={clear_errors}; "
        f"P_ON_RESET_OR_WHEN_DISABLED_CLEAR mismatch_count={max(0, clear_errors - 3) + int(not reset_clear) + int(not disabled_clear)}; "
        f"P_ON_EACH_ENABLED_RISING_CLK_EDGE mismatch_count={valid_errors + int(checked < 6)}; "
        f"P_USE_A_FASTER_ATTACK_STEP_WHEN mismatch_count={env_errors + int(not attack_seen) + int(not release_seen)}; "
        f"P_DRIVE_ENVELOPE_WITH_THE_TRACKED_MAGNITUDE mismatch_count={env_errors}; "
        f"P_EXPOSE_WHETHER_THE_LAST_UPDATE_USED mismatch_count={max(0, attack_errors - 1)}"
    )

CHECKER_ID = "v4_336_rf_envelope_detector_attack_release"
CHECKER: Checker = with_diagnostic_contract(check_v4_1034_rf_envelope_detector_attack_release)
