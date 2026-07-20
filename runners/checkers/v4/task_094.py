"""Stimulus-relative checker for canonical v4 DUT 094."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import (
    edge_times,
    event_settle_delay,
    finish,
    missing_trace,
    row_at_or_after,
    row_before,
)


PROPERTY_IDS = [
    "P_RESET_COMMON_MODE",
    "P_QUADRATURE_SEQUENCE",
    "P_LO_MONITORS",
    "P_MIXER_MONITORS",
    "P_BASEBAND_UPDATES",
    "P_PHASE_MONITOR",
]


def _clip(value: float) -> float:
    return min(0.88, max(0.02, value))


def check_iq_downconversion_chain(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {
        "time", "clk", "rst", "vin", "out", "metric", "lo_i", "lo_q",
        "mix_i", "mix_q", "phase_mon",
    }
    results, missing = missing_trace("v4_094", rows, required, PROPERTY_IDS)
    if missing is not None:
        return missing
    reset, sequence, lo_monitors, mixer_monitors, baseband, phase_monitor = results
    rises = edge_times(rows, "clk", threshold=0.45, rising=True)
    settle = event_settle_delay(rises)
    phase = 3
    i_state = q_state = 0.45
    phases_seen: set[int] = set()
    vin_regions: set[str] = set()
    reset_edges = 0

    for edge in rises:
        stimulus = row_before(rows, edge)
        probe_time = edge + settle
        if probe_time > rows[-1]["time"]:
            continue
        probe = row_at_or_after(rows, probe_time)
        if stimulus["rst"] > 0.45:
            # The reset may release between the clock edge and the normal
            # post-edge probe. Do not grade post-reset outputs as reset state.
            if probe["rst"] <= 0.45:
                continue
            phase = 3
            i_state = q_state = 0.45
            reset_edges += 1
            for signal, expected in (
                ("out", 0.45), ("metric", 0.45), ("lo_i", 0.45),
                ("lo_q", 0.45), ("mix_i", 0.45), ("mix_q", 0.45),
                ("phase_mon", 0.9),
            ):
                reset.compare(expected=expected, observed=probe[signal], tolerance=0.08,
                              time_s=probe_time, label=signal)
            continue

        phase = (phase + 1) % 4
        phases_seen.add(phase)
        vin = float(stimulus["vin"])
        if vin >= 0.62:
            vin_regions.add("high")
        elif vin <= 0.28:
            vin_regions.add("low")
        else:
            vin_regions.add("mid")
        i_coefficient = (1.0, 0.0, -1.0, 0.0)[phase]
        q_coefficient = (0.0, 1.0, 0.0, -1.0)[phase]
        expected_lo_i = 0.45 + 0.40 * i_coefficient
        expected_lo_q = 0.45 + 0.40 * q_coefficient
        expected_mix_i = _clip(0.45 + 1.25 * (vin - 0.45) * i_coefficient)
        expected_mix_q = _clip(0.45 + 1.25 * (vin - 0.45) * q_coefficient)
        i_state = _clip(i_state + 0.85 * (expected_mix_i - i_state))
        q_state = _clip(q_state + 0.85 * (expected_mix_q - q_state))
        expected_phase = 0.3 * phase

        sequence.condition(
            phase in {0, 1, 2, 3}, expected="quadrature_phase_0_to_3",
            observed=f"phase={phase}", time_s=probe_time,
        )
        for signal, expected in (("lo_i", expected_lo_i), ("lo_q", expected_lo_q)):
            lo_monitors.compare(expected=expected, observed=probe[signal], tolerance=0.08,
                                time_s=probe_time, label=signal)
        for signal, expected in (("mix_i", expected_mix_i), ("mix_q", expected_mix_q)):
            mixer_monitors.compare(expected=expected, observed=probe[signal], tolerance=0.08,
                                   time_s=probe_time, label=signal)
        baseband.compare(expected=i_state, observed=probe["out"], tolerance=0.08,
                         time_s=probe_time, label="i_state")
        baseband.compare(expected=q_state, observed=probe["metric"], tolerance=0.08,
                         time_s=probe_time, label="q_state")
        phase_monitor.compare(expected=expected_phase, observed=probe["phase_mon"], tolerance=0.08,
                              time_s=probe_time, label="phase_mon")

    reset.condition(
        reset_edges >= 1, expected="reset_clock_edge>=1", observed=f"reset_edges={reset_edges}",
        time_s=rows[-1]["time"],
    )
    sequence.condition(
        phases_seen == {0, 1, 2, 3}, expected="phases=0,1,2,3",
        observed=f"phases={sorted(phases_seen)}", time_s=rows[-1]["time"],
    )
    baseband.condition(
        len(vin_regions) >= 2, expected="at_least_two_vin_regions",
        observed=f"vin_regions={sorted(vin_regions)}", time_s=rows[-1]["time"],
    )
    for result in results:
        result.require_coverage(2)
    return finish(
        "v4_094", results,
        coverage=(f"clock_rises={len(rises)} reset_edges={reset_edges} "
                  f"phases={sorted(phases_seen)} vin_regions={sorted(vin_regions)}"),
    )


CHECKER_ID = "v4_094_iq_downconversion_chain"
CHECKER: Checker = check_iq_downconversion_chain
