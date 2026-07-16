"""Task-specific checker for canonical v4 DUT 307."""
from __future__ import annotations

from ..api import Checker
from ..common.v4_topup import (
    _v4_topup_logic_high,
    _v4_topup_near,
    _v4_topup_span,
)
from ..common.relative_events import active_start, first_disable, sample_after_event

def check_v4_307_switched_capacitor_integrator_phase_pair(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1005 empty_trace"
    activation = active_start(rows, enable="enable", reset="rst")
    disable = first_disable(rows, "enable", activation)

    reset_clear = any(
        _v4_topup_logic_high(row, "rst")
        and _v4_topup_near(row["vout"], 0.45, 0.08)
        and row["valid"] < 0.15
        for row in rows
    )
    overlap_low = any(
        row["time"] >= activation
        and _v4_topup_logic_high(row, "phi1")
        and _v4_topup_logic_high(row, "phi2")
        and row["valid"] < 0.25
        for row in rows
    )
    accepted = [
        row
        for row in rows
        if row["time"] >= activation
        and _v4_topup_logic_high(row, "enable")
        and not _v4_topup_logic_high(row, "rst")
        and row["valid"] > 0.45
    ]
    direction_checks = direction_errors = overlap_events = 0
    last_vout: float | None = None
    previous = rows[0]
    for row in rows[1:]:
        phi2_rise = (not _v4_topup_logic_high(previous, "phi2")) and _v4_topup_logic_high(row, "phi2")
        previous = row
        if not phi2_rise or row["time"] < activation or _v4_topup_logic_high(row, "rst"):
            continue
        sample = sample_after_event(rows, float(row["time"]), clock_signal="phi2", fraction_of_period=0.05)
        if sample is None or not _v4_topup_logic_high(sample, "enable"):
            continue
        if _v4_topup_logic_high(row, "phi1"):
            overlap_events += int(float(sample["valid"]) < 0.3)
            continue
        if float(sample["valid"]) <= 0.45:
            continue
        sample_dev = float(sample["phase_metric"]) - 0.45
        if last_vout is not None and abs(sample_dev) > 0.04:
            delta = float(sample["vout"]) - last_vout
            if abs(delta) > 0.006:
                direction_checks += 1
                if delta * sample_dev < 0.0:
                    direction_errors += 1
        last_vout = float(sample["vout"])
    phase_tracks_input = any(
        row["time"] >= activation
        and row["valid"] > 0.45
        and abs(float(row["phase_metric"]) - float(row["vin"])) < 0.12
        for row in rows
    )
    held_when_disabled = any(
        disable is not None and row["time"] >= disable
        and not _v4_topup_logic_high(row, "enable")
        and _v4_topup_near(row["vout"], 0.45, 0.08)
        and row["valid"] < 0.2
        for row in rows
    )
    ok = (
        reset_clear
        and overlap_low
        and overlap_events >= 1
        and len(accepted) >= 10
        and _v4_topup_span(rows, "vout") >= 0.045
        and _v4_topup_span(rows, "phase_metric") > 0.10
        and phase_tracks_input
        and held_when_disabled
        and direction_checks >= 1
        and direction_errors == 0
    )
    vout_span = _v4_topup_span(rows, "vout")
    phase_span = _v4_topup_span(rows, "phase_metric")
    clear_mismatches = int(not reset_clear) + int(not held_when_disabled)
    sample_mismatches = int(not phase_tracks_input) + int(phase_span <= 0.10)
    integrate_mismatches = (
        direction_errors
        + int(direction_checks < 1)
        + int(vout_span < 0.045)
    )
    overlap_mismatches = int(not overlap_low) + int(overlap_events < 1)
    expose_mismatches = (
        int(not phase_tracks_input)
        + int(vout_span < 0.045)
        + int(phase_span <= 0.10)
    )
    diagnostics = {
        "P_ON_RESET_OR_WHEN_DISABLED_CLEAR": clear_mismatches,
        "P_ON_A_RISING_PHI1_CROSSING_SAMPLE": sample_mismatches,
        "P_ON_THE_FOLLOWING_RISING_PHI2_CROSSING": integrate_mismatches,
        "P_REJECT_OVERLAPPING_PHI1_AND_PHI2_UPDATES": overlap_mismatches,
        "P_EXPOSE_THE_MOST_RECENT_ACCEPTED_PHASE": expose_mismatches,
        "P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE": 0,
    }
    return ok, (
        f"v4_307 accepted={len(accepted)} reset_clear={reset_clear} overlap_low={overlap_low} "
        f"overlap_events={overlap_events} phase_tracks_input={phase_tracks_input} held_disabled={held_when_disabled} "
        f"direction_checks={direction_checks} direction_errors={direction_errors} "
        f"vout_span={vout_span:.3f} phase_span={phase_span:.3f}; "
        + "; ".join(f"{key} mismatch_count={value}" for key, value in diagnostics.items())
    )

CHECKER_ID = "v4_307_switched_capacitor_integrator_phase_pair"
CHECKER: Checker = check_v4_307_switched_capacitor_integrator_phase_pair
