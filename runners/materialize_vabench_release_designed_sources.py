#!/usr/bin/env python3
from __future__ import annotations

import csv
import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path

from vabench_release_paths import release_category_entry_dir, release_entry_path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
TASKS_ROOT = PACKAGE_ROOT / "tasks"
TRACKER_CSV = ROOT / "docs" / "VABENCH_RELEASE_TRACKER.csv"
SELECTED_MANIFEST_CSV = ROOT / "docs" / "VABENCH_RELEASE_SELECTED_MANIFEST.csv"
SELECTED_MANIFEST_MD = ROOT / "docs" / "VABENCH_RELEASE_SELECTED_MANIFEST.md"

FORM_TO_FAMILY = {
    "dut": "spec-to-va",
    "tb": "tb-generation",
    "bugfix": "bugfix",
    "e2e": "end-to-end",
}

SUPPORT_CATEGORIES = {
    "Measurement Instrumentation Flows",
    "Stimulus and Source Generators",
}

DIFFICULTY_OVERRIDES = {
    # Basic single-block threshold or first-order behavior.
    "vbr1_l1_binary_weighted_voltage_dac": "D1",
    "vbr1_l1_threshold_comparator": "D1",
    "vbr1_l1_offset_comparator": "D1",
    "vbr1_l1_first_order_lowpass": "D1",
    "vbr1_l1_thermometer_code_decoder": "D1",
    "vbr1_l1_unit_element_thermometer_dac": "D1",
    "vbr1_l1_bias_voltage_generator_with_enable_trim": "D1",
    "vbr1_l1_uvlo_brownout_detector": "D1",
    "vbr1_l1_limiting_amplifier_frontend": "D1",
    "vbr1_l1_sine_periodic_voltage_source": "D1",
    # Advanced nonlinear macromodels that need explicit approximation choices.
    "vbr1_l1_pipeline_adc_stage": "D3",
    "vbr1_l1_log_rssi_power_detector": "D3",
    "vbr1_l1_pa_compression_macro": "D3",
}


def track_for_category(category: str) -> str:
    return "support" if category in SUPPORT_CATEGORIES else "core"


def difficulty_for_row(row: dict[str, str]) -> str:
    if row["level"] == "L2":
        return "D3"
    return DIFFICULTY_OVERRIDES.get(row["entry_id"], "D2")


@dataclass(frozen=True)
class DesignedSpec:
    entry_id: str
    module: str
    summary: str
    behavior_checks: tuple[str, ...]
    profile: str
    bug: str


DESIGNED_SPECS: dict[str, DesignedSpec] = {
    "vbr1_l1_dac_mismatch_unit_weighting_model": DesignedSpec(
        "vbr1_l1_dac_mismatch_unit_weighting_model",
        "dac_mismatch_unit_weighting_model",
        "Model a 4-bit voltage DAC using explicit nonideal unit weights and a bounded output range.",
        ("weighted_code_response", "explicit_mismatch_terms", "bounded_reconstruction_voltage"),
        "weighted_dac",
        "The buggy implementation uses ideal binary weights and therefore hides the intended mismatch.",
    ),
    "vbr1_l1_charge_pump_abstraction": DesignedSpec(
        "vbr1_l1_charge_pump_abstraction",
        "charge_pump_abstraction",
        "Represent UP/DN pulse effects as a voltage-domain control-node update without current contributions.",
        ("up_pulse_increases_control", "down_pulse_decreases_control", "control_voltage_clamped"),
        "charge_pump",
        "The buggy implementation swaps UP and DN polarity.",
    ),
    "vbr1_l1_loop_filter_abstraction": DesignedSpec(
        "vbr1_l1_loop_filter_abstraction",
        "loop_filter_abstraction",
        "Approximate the continuous-time proportional/integral loop-filter trend with sampled voltage-domain state updates on clock edges.",
        (
            "proportional_step_decays",
            "integral_residual_accumulates",
            "metric_asserts_after_valid_updates",
            "reset_clears_integrator",
            "filtered_output_bounded",
        ),
        "loop_filter",
        "The buggy implementation omits reset clearing of the integrator state.",
    ),
    "vbr1_l1_calibration_deadband_controller": DesignedSpec(
        "vbr1_l1_calibration_deadband_controller",
        "calibration_deadband_controller",
        "Update a bounded trim code only when the signed error is outside a deadband.",
        ("trim_holds_inside_deadband", "trim_moves_for_large_error", "trim_clamped_to_range"),
        "deadband_cal",
        "The buggy implementation updates the trim inside the deadband.",
    ),
    "vbr1_l1_successive_approximation_calibration_search_fsm": DesignedSpec(
        "vbr1_l1_successive_approximation_calibration_search_fsm",
        "successive_approximation_calibration_search_fsm",
        "Run a clocked successive-approximation trim search with halving step size and completion flag.",
        ("step_size_halves", "trim_direction_follows_error", "done_after_search_window"),
        "sar_cal_fsm",
        "The buggy implementation keeps a constant step size instead of halving it.",
    ),
    "vbr1_l2_complete_calibration_loop": DesignedSpec(
        "vbr1_l2_complete_calibration_loop",
        "complete_calibration_loop",
        "Close a simple calibration loop from error stimulus through controller and actuator output.",
        ("raw_error_is_corrected", "bounded_negative_feedback_response", "metric_tracks_convergence"),
        "cal_loop",
        "The buggy implementation updates correction in the same direction as the residual error.",
    ),
    "vbr1_l1_bandgap_reference_macro_model": DesignedSpec(
        "vbr1_l1_bandgap_reference_macro_model",
        "bandgap_reference_macro_model",
        "Model a startup-gated voltage reference that settles to a supply-insensitive reference after VDD exceeds the startup threshold.",
        ("startup_threshold_blocks_reference", "reference_settles_near_nominal", "line_regulation_is_bounded"),
        "bandgap_reference",
        "The buggy implementation makes the reference track supply directly and never enforces the startup threshold.",
    ),
    "vbr1_l1_ptat_ctat_reference_generator": DesignedSpec(
        "vbr1_l1_ptat_ctat_reference_generator",
        "ptat_ctat_reference_generator",
        "Generate PTAT and CTAT branch abstractions and combine them into a temperature-compensated voltage reference.",
        ("ptat_branch_monotonic_with_temperature", "ctat_compensation_flattens_reference", "reference_common_mode_bounded"),
        "ptat_ctat_reference",
        "The buggy implementation exposes only a PTAT-like reference so the output drifts strongly with temperature.",
    ),
    "vbr1_l1_bias_voltage_generator_with_enable_trim": DesignedSpec(
        "vbr1_l1_bias_voltage_generator_with_enable_trim",
        "bias_voltage_generator_with_enable_trim",
        "Generate an enable-gated bias voltage with bounded trim response and disabled-state collapse.",
        ("disable_forces_bias_low", "trim_code_moves_bias_voltage", "metric_marks_enabled_bias"),
        "bias_trim_generator",
        "The buggy implementation ignores the disable region and keeps driving a bias voltage.",
    ),
    "vbr1_l1_power_on_reset_detector": DesignedSpec(
        "vbr1_l1_power_on_reset_detector",
        "power_on_reset_detector",
        "Detect a supply ramp, hold reset asserted through a release-delay window, and reassert reset on brownout.",
        ("reset_asserted_below_supply_threshold", "release_delay_after_power_good", "brownout_reasserts_reset"),
        "por_detector",
        "The buggy implementation releases reset immediately when supply crosses the threshold.",
    ),
    "vbr1_l1_uvlo_brownout_detector": DesignedSpec(
        "vbr1_l1_uvlo_brownout_detector",
        "uvlo_brownout_detector",
        "Implement an undervoltage-lockout power-good detector with separate rising and falling supply thresholds.",
        ("power_good_has_hysteresis", "brownout_clears_power_good", "recovery_requires_upper_threshold"),
        "uvlo_brownout",
        "The buggy implementation uses a single threshold and loses UVLO hysteresis.",
    ),
    "vbr1_l1_ldo_regulator_macro_model": DesignedSpec(
        "vbr1_l1_ldo_regulator_macro_model",
        "ldo_regulator_macro_model",
        "Approximate an LDO output-voltage macro model with bounded load droop and recovery behavior.",
        ("regulated_output_bounded", "load_step_causes_droop", "output_recovers_after_load_reduction"),
        "ldo_regulator",
        "The buggy implementation ignores the load disturbance and therefore misses the expected load-step droop.",
    ),
    "vbr1_l2_reference_startup_enable_flow": DesignedSpec(
        "vbr1_l2_reference_startup_enable_flow",
        "reference_startup_enable_flow",
        "Compose supply-good detection, enable gating, reference startup, and valid-status observation in one behavioral flow.",
        ("pre_enable_reference_is_held_low", "enabled_reference_startup_settles", "supply_dip_resets_valid_status"),
        "reference_startup_flow",
        "The buggy implementation ignores the enable gate and starts the reference as soon as supply is present.",
    ),
    "vbr1_l2_ldo_load_step_recovery_flow": DesignedSpec(
        "vbr1_l2_ldo_load_step_recovery_flow",
        "ldo_load_step_recovery_flow",
        "Compose a regulator macro model with repeated load-step disturbances and recovery-status observation.",
        ("load_step_transient_droop_visible", "closed_loop_recovery_after_step", "metric_marks_recovered_regulation"),
        "ldo_load_step_flow",
        "The buggy implementation makes the output a static load-code function without transient recovery.",
    ),
    "vbr1_l1_lna_gain_compression_macro": DesignedSpec(
        "vbr1_l1_lna_gain_compression_macro",
        "lna_gain_compression_macro",
        "Model an RF low-noise-amplifier front-end with small-signal gain, soft large-signal compression, and bounded output swing.",
        ("small_signal_gain_present", "large_signal_compression_visible", "compressed_output_bounded"),
        "lna_gain_compression",
        "The buggy implementation stays linear and never raises the compression metric.",
    ),
    "vbr1_l1_rf_mixer_downconverter_macro": DesignedSpec(
        "vbr1_l1_rf_mixer_downconverter_macro",
        "rf_mixer_downconverter_macro",
        "Model a voltage-domain RF mixer/downconverter where the LO polarity modulates the RF input around common mode into a baseband output.",
        ("lo_polarity_controls_conversion_sign", "conversion_gain_visible", "baseband_output_bounded"),
        "rf_mixer_downconverter",
        "The buggy implementation ignores LO polarity and always uses the same conversion sign.",
    ),
    "vbr1_l1_pa_compression_macro": DesignedSpec(
        "vbr1_l1_pa_compression_macro",
        "pa_compression_macro",
        "Model a power-amplifier behavioral macro with high gain at moderate drive and compressed output near large-signal limits.",
        ("pa_gain_above_unity", "pa_large_signal_compression", "pa_output_limit_metric"),
        "pa_compression",
        "The buggy implementation behaves like an unclipped linear gain stage.",
    ),
    "vbr1_l1_log_rssi_power_detector": DesignedSpec(
        "vbr1_l1_log_rssi_power_detector",
        "log_rssi_power_detector",
        "Convert received envelope magnitude into a monotonic logarithmic RSSI-style voltage code.",
        ("rssi_monotonic_with_envelope", "log_spacing_compresses_large_steps", "low_input_floor_bounded"),
        "log_rssi_detector",
        "The buggy implementation reports a linear envelope code rather than a compressed RSSI response.",
    ),
    "vbr1_l1_limiting_amplifier_frontend": DesignedSpec(
        "vbr1_l1_limiting_amplifier_frontend",
        "limiting_amplifier_frontend",
        "Normalize AFE input amplitude with a limiting amplifier that preserves polarity and asserts a limiting status metric.",
        ("small_input_gain_preserved", "large_input_limited_high_low", "limiting_metric_asserted"),
        "limiting_amplifier",
        "The buggy implementation passes the input through without limiting large swings.",
    ),
    "vbr1_l2_agc_receiver_leveling_loop": DesignedSpec(
        "vbr1_l2_agc_receiver_leveling_loop",
        "agc_receiver_leveling_loop",
        "Compose a receiver gain path, envelope/RSSI observation, and gain-control update so output amplitude settles toward a target level.",
        ("agc_reduces_gain_on_large_input", "leveled_output_amplitude", "lock_metric_after_settling"),
        "agc_receiver_loop",
        "The buggy implementation updates gain in the wrong direction during overload.",
    ),
    "vbr1_l2_iq_downconversion_chain": DesignedSpec(
        "vbr1_l2_iq_downconversion_chain",
        "iq_downconversion_chain",
        "Compose quadrature LO sequencing, two mixer paths, and baseband I/Q observables in a voltage-domain receiver chain.",
        ("quadrature_iq_phase_sequence", "i_and_q_outputs_are_distinct", "common_mode_hold_when_input_centered"),
        "iq_downconversion_chain",
        "The buggy implementation drives the Q observable from the I path instead of the quadrature LO phase.",
    ),
    "vbr1_l2_programmable_stimulus_sequencer": DesignedSpec(
        "vbr1_l2_programmable_stimulus_sequencer",
        "programmable_stimulus_sequencer",
        "Generate a programmable ramp, swept/chirp sine, and gated burst/PRBS stimulus schedule.",
        (
            "ramp_segment_monotonic",
            "swept_chirp_segment_frequency_increases",
            "burst_prbs_gate_schedule",
            "mode_switch_continuity",
        ),
        "stimulus_sequencer",
        "The buggy implementation ignores the burst gate.",
    ),
    "vbr1_l1_soft_hysteretic_limiter": DesignedSpec(
        "vbr1_l1_soft_hysteretic_limiter",
        "soft_hysteretic_limiter",
        "Limit a voltage signal with bounded compression and stateful hysteresis memory around high/low thresholds.",
        ("smooth_limiting", "hysteresis_state_memory", "bounded_output"),
        "soft_limiter",
        "The buggy implementation collapses the hysteresis thresholds into a single threshold.",
    ),
    "vbr1_l1_higher_order_filter": DesignedSpec(
        "vbr1_l1_higher_order_filter",
        "higher_order_filter",
        "Approximate a second-order low-pass response with two sampled internal filter states.",
        ("two_filter_states", "step_response_is_smoothed", "reset_clears_states"),
        "two_pole_filter",
        "The buggy implementation updates only one pole state.",
    ),
    "vbr1_l2_amplifier_filter_chain": DesignedSpec(
        "vbr1_l2_amplifier_filter_chain",
        "amplifier_filter_chain",
        "Combine a gain block and low-pass filter; expose the bounded pre-filter amplified target on metric so out can be checked for lagged settling.",
        ("amplified_input", "filtered_output_lags_input", "metric_tracks_settling"),
        "amp_filter_chain",
        "The buggy implementation measures the unfiltered amplifier output.",
    ),
}


PUBLIC_BEHAVIOR_TARGETS: dict[str, tuple[str, ...]] = {
    "bandgap_reference": (
        "Treat logic low/high as 0 V/0.9 V with a 0.45 V threshold.",
        "Treat vin as a sub-1 V supply ramp. Start regulation above about 0.65 V and reset below about 0.50 V.",
        "During reset or below-threshold supply, hold out near 0 V and keep metric low.",
        "After startup, regulate out near a supply-insensitive reference around 0.55 V.",
        "During higher supply, keep the reference nearly constant instead of supply-tracking.",
        "During brownout, reset out near 0 V and mark the output invalid.",
    ),
    "bias_trim_generator": (
        "Treat logic low/high as 0 V/0.9 V with a 0.45 V threshold.",
        "Treat vin as the combined enable/trim control. vin below about 0.25 V disables the bias: out near 0 V and metric low.",
        "When enabled, map vin from about 0.25-0.90 V to a bounded bias target around 0.28-0.82 V.",
        "out should move smoothly toward the trim target on clocked updates, not jump to rails.",
        "Higher trim/control voltage should increase out monotonically.",
        "metric should be high only while the bias generator is enabled and driving a valid bias.",
    ),
    "ptat_ctat_reference": (
        "Treat vin as a voltage-coded temperature/control value in the 0-0.9 V range.",
        "Build opposing PTAT and CTAT internal trends; metric should expose a PTAT-like increasing branch.",
        "Combine PTAT and CTAT so out stays near a bounded reference around mid-scale instead of strongly tracking vin.",
        "Reset should initialize out near mid-scale and keep metric low until valid updates occur.",
        "Clamp out and metric to the public 0-0.9 V voltage-domain range.",
    ),
    "por_detector": (
        "Treat vin as a supply ramp. Keep out reset-asserted high while reset input is high or vin is below about 0.62 V.",
        "After vin is power-good and reset is released, wait about four rising clock updates before deasserting out low.",
        "During the release delay, metric may indicate partial release; after release, metric should be high.",
        "If supply falls below threshold or reset asserts again, immediately assert out high and clear the release delay.",
    ),
    "uvlo_brownout": (
        "Treat vin as the supply. Assert power-good out high only after vin rises above about 0.65 V.",
        "Keep out high while vin remains between about 0.55 V and 0.65 V; this is the UVLO hysteresis band.",
        "Clear out low on brownout below about 0.55 V or reset.",
        "metric should distinguish fault/lockout from the valid power-good state.",
    ),
    "ldo_regulator": (
        "Treat vin as a voltage-coded load/disturbance control, not as the regulator supply rail.",
        "Regulated out should remain bounded near about 0.60 V under light load.",
        "Higher load/disturbance should cause visible droop from the nominal target, not rail-to-rail tracking.",
        "After a load reduction, out should recover gradually toward the regulation target over clocked updates.",
        "metric should be high when regulation error is small and lower during droop/recovery.",
        "Keep all outputs in the 0-0.9 V voltage-domain range.",
    ),
    "lna_gain_compression": (
        "Treat vin around 0.45 V common mode; small-signal out should show gain greater than 1 around that common mode.",
        "For large drive, compress incremental gain and keep output bounded.",
        "Compression should be reasonably symmetric for positive and negative excursions.",
        "metric should be low or small in the linear region and high during compression.",
    ),
    "rf_mixer_downconverter": (
        "Treat clk as the LO-polarity waveform with a 0.45 V logic threshold.",
        "Convert the input envelope around 0.45 V common mode to baseband by flipping sign with LO polarity.",
        "Preserve output common mode near 0.45 V and keep out bounded.",
        "metric should indicate active conversion or LO polarity state.",
    ),
    "pa_compression": (
        "Treat vin as PA drive around 0.45 V common mode.",
        "Moderate drive should show gain above unity.",
        "Large drive should compress toward bounded high/low output limits rather than continuing linear gain.",
        "metric should rise when the output is near compression or limiting.",
        "Keep out and metric within the 0-0.9 V voltage-domain range.",
    ),
    "log_rssi_detector": (
        "Treat vin as an envelope around 0.45 V common mode and estimate amplitude as abs(vin - 0.45).",
        "Use a Spectre/EVAS-friendly compressed or piecewise approximation; do not rely on unsupported log10, round, integer casts, or digital Verilog.",
        "out should be monotonic with amplitude, but large-amplitude steps should be compressed rather than linear.",
        "Keep a low-input floor near the bottom of the RSSI range.",
        "metric should expose normalized envelope magnitude and remain bounded within 0-0.9 V.",
    ),
    "limiting_amplifier": (
        "Treat vin around 0.45 V common mode and preserve signal polarity around that common mode.",
        "For small input excursions, apply gain around common mode.",
        "For large positive or negative excursions, limit/compress output toward bounded high/low levels instead of continuing linearly.",
        "Assert metric high only when limiting/compression is active.",
        "Keep out in the 0-0.9 V range and avoid hard digital switching for small signals.",
    ),
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def slugify(value: str) -> str:
    value = value.lower().replace("/", " ")
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def required_forms(row: dict[str, str]) -> list[str]:
    forms = row["required_task_forms"].replace("e2e-form", "e2e").split(";")
    return [form.strip() for form in forms if form.strip() in FORM_TO_FAMILY]


def va_source(module: str, profile: str, *, buggy: bool = False) -> str:
    variant = "buggy" if buggy else "fixed"
    if profile == "weighted_dac":
        weights = ("1.00, 2.00, 4.00, 8.00" if buggy else "1.00, 2.02, 3.96, 8.08")
        w0, w1, w2, w3 = (("1.00", "2.00", "4.00", "8.00") if buggy else ("1.00", "2.02", "3.96", "8.08"))
        total = "15.00" if buggy else "15.06"
        return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(b0, b1, b2, b3, out);
input b0, b1, b2, b3;
output out;
electrical b0, b1, b2, b3, out;
parameter real vhi = 0.9;
parameter real vlo = 0.0;
parameter real tr = 100p;
real y;
analog begin
    y = (((V(b0) > 0.45) ? {w0} : 0.00)
       + ((V(b1) > 0.45) ? {w1} : 0.00)
       + ((V(b2) > 0.45) ? {w2} : 0.00)
       + ((V(b3) > 0.45) ? {w3} : 0.00)) / {total};
    // {variant}: intended unit weights are [{weights}].
    V(out) <+ transition(vlo + (vhi - vlo) * y, 0, tr, tr);
end
endmodule
"""
    if profile == "charge_pump":
        up_update = "ctrl = ctrl - step;" if buggy else "ctrl = ctrl + step;"
        down_update = "ctrl = ctrl + step;" if buggy else "ctrl = ctrl - step;"
        return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(clk, rst, up, dn, vctrl, metric);
input clk, rst, up, dn;
output vctrl, metric;
electrical clk, rst, up, dn, vctrl, metric;
parameter real tr = 100p;
parameter real vth = 0.45;
parameter real step = 0.06;
parameter real vmin = 0.05;
parameter real vmax = 0.85;
real ctrl, metricv;
analog begin
    @(initial_step) begin
        ctrl = 0.45;
        metricv = 0.45;
    end
    @(cross(V(clk) - vth, +1)) begin
        if (V(rst) > vth) begin
            ctrl = 0.45;
            metricv = 0.45;
        end else if (V(up) > vth && V(dn) <= vth) begin
            {up_update}
            metricv = 0.75;
        end else if (V(dn) > vth && V(up) <= vth) begin
            {down_update}
            metricv = 0.15;
        end else begin
            metricv = 0.45;
        end
        if (ctrl > vmax) ctrl = vmax;
        if (ctrl < vmin) ctrl = vmin;
    end
    V(vctrl) <+ transition(ctrl, 0, tr, tr);
    V(metric) <+ transition(metricv, 0, tr, tr);
end
endmodule
"""
    if profile == "deadband_cal":
        if buggy:
            update_block = """else if (errv < deadband && errv > -deadband) begin
            if (errv >= 0.0) begin
                trimv = trimv + step_size;
            end else begin
                trimv = trimv - step_size;
            end
            metricv = 0.9;
        end else begin
            metricv = 0.0;
        end"""
        else:
            update_block = """else if (errv > deadband) begin
            trimv = trimv + step_size;
            metricv = 0.9;
        end else if (errv < -deadband) begin
            trimv = trimv - step_size;
            metricv = 0.9;
        end else begin
            metricv = 0.0;
        end"""
        return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
parameter real tr = 100p;
parameter real vth = 0.45;
parameter real target = 0.45;
parameter real deadband = 0.05;
parameter real step_size = 0.06;
parameter real vmin = 0.05;
parameter real vmax = 0.85;
real trimv, errv, metricv;
analog begin
    @(initial_step) begin
        trimv = target;
        metricv = 0.0;
    end
    @(cross(V(clk) - vth, +1)) begin
        errv = V(vin) - target;
        if (V(rst) > vth) begin
            trimv = target;
            metricv = 0.0;
        end {update_block}
        if (trimv > vmax) trimv = vmax;
        if (trimv < vmin) trimv = vmin;
    end
    V(out) <+ transition(trimv, 0, tr, tr);
    V(metric) <+ transition(metricv, 0, tr, tr);
end
endmodule
"""
    if profile == "sar_cal_fsm":
        halve = "stepv = stepv * 0.5;" if not buggy else "stepv = stepv;"
        return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
parameter real tr = 100p;
parameter real vth = 0.45;
parameter real target = 0.45;
parameter real step_init = 0.18;
parameter real vmin = 0.05;
parameter real vmax = 0.85;
real trialv, stepv, errv, donev;
integer cycle;
analog begin
    @(initial_step) begin
        trialv = target;
        stepv = step_init;
        cycle = 0;
        donev = 0.0;
    end
    @(cross(V(clk) - vth, +1)) begin
        errv = V(vin) - target;
        if (V(rst) > vth) begin
            trialv = target;
            stepv = step_init;
            cycle = 0;
            donev = 0.0;
        end else if (donev < 0.45) begin
            if (errv > 0.0) begin
                trialv = trialv + stepv;
            end else if (errv < 0.0) begin
                trialv = trialv - stepv;
            end
            {halve}
            cycle = cycle + 1;
            if (cycle >= 4) donev = 0.9;
        end
        if (trialv > vmax) trialv = vmax;
        if (trialv < vmin) trialv = vmin;
    end
    V(out) <+ transition(trialv, 0, tr, tr);
    V(metric) <+ transition(donev, 0, tr, tr);
end
endmodule
"""
    if profile == "cal_loop":
        trim_update = "trimv = trimv + loop_gain * residualv;" if buggy else "trimv = trimv - loop_gain * residualv;"
        return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
parameter real tr = 100p;
parameter real vth = 0.45;
parameter real target = 0.45;
parameter real loop_gain = 0.40;
parameter real plant_alpha = 0.35;
parameter real vmin = 0.05;
parameter real vmax = 0.85;
real trimv, plantv, rawerrv, residualv, desiredv, abserr, metricv;
analog begin
    @(initial_step) begin
        trimv = target;
        plantv = target;
        metricv = 0.9;
    end
    @(cross(V(clk) - vth, +1)) begin
        if (V(rst) > vth) begin
            trimv = target;
            plantv = target;
            metricv = 0.9;
        end else begin
            rawerrv = V(vin) - target;
            residualv = rawerrv + (trimv - target);
            {trim_update}
            if (trimv > vmax) trimv = vmax;
            if (trimv < vmin) trimv = vmin;
            residualv = rawerrv + (trimv - target);
            desiredv = target + residualv;
            plantv = plantv + plant_alpha * (desiredv - plantv);
            if (plantv > vmax) plantv = vmax;
            if (plantv < vmin) plantv = vmin;
            abserr = plantv - target;
            if (abserr < 0.0) abserr = -abserr;
            metricv = 0.9 - 1.5 * abserr;
            if (metricv > 0.9) metricv = 0.9;
            if (metricv < 0.0) metricv = 0.0;
        end
    end
    V(out) <+ transition(plantv, 0, tr, tr);
    V(metric) <+ transition(metricv, 0, tr, tr);
end
endmodule
"""
    if profile in {"charge_pump", "loop_filter", "gain_cal_loop"}:
        update = "state = state - step;" if (buggy and profile in {"charge_pump", "cal_loop", "gain_cal_loop"}) else "state = state + step;"
        deadband_condition = "(errv > deadband || errv < -deadband)"
        if buggy and profile == "deadband_cal":
            deadband_condition = "(errv < deadband && errv > -deadband)"
        halve = "step = step * 0.5;" if not (buggy and profile == "sar_cal_fsm") else "step = step;"
        reset_line = "integ = 0.0;" if not (buggy and profile == "loop_filter") else "integ = integ;"
        done_line = "donev = (cycle >= 4) ? 0.9 : 0.0;" if not (buggy and profile == "sar_loop") else "donev = 0.0;"
        return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
parameter real tr = 100p;
parameter real deadband = 0.05;
real state, step, integ, errv, donev;
integer cycle;
analog begin
    @(initial_step) begin
        state = 0.45;
        step = 0.20;
        integ = 0.0;
        cycle = 0;
        donev = 0.0;
    end
    @(cross(V(clk) - 0.45, +1)) begin
        errv = V(vin) - 0.45;
        if (V(rst) > 0.45) begin
            state = 0.45;
            step = 0.20;
            {reset_line}
            cycle = 0;
            donev = 0.0;
        end else if {deadband_condition} begin
            if (errv > 0.0) begin
                {update}
            end else begin
                state = state - step;
            end
            integ = integ + errv * 0.04;
            {halve}
            cycle = cycle + 1;
            {done_line}
        end
        if (state > 0.85) state = 0.85;
        if (state < 0.05) state = 0.05;
    end
    V(out) <+ transition(state + integ, 0, tr, tr);
    V(metric) <+ transition(donev, 0, tr, tr);
end
endmodule
"""
    if profile == "pulse_stretcher":
        hold_line = "remaining = width;" if not buggy else "if (remaining <= 0.0) remaining = width;"
        metric_expr = "s1 - s2 + 0.45"
        if buggy and profile == "amp_filter_chain":
            metric_expr = "s1"
        return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(trig, rst, pulse);
input trig, rst;
output pulse;
electrical trig, rst, pulse;
parameter real tr = 50p;
parameter real width = 4n;
real level, remaining;
analog begin
    @(initial_step) begin
        level = 0.0;
        remaining = 0.0;
    end
    @(cross(V(trig) - 0.45, +1)) begin
        level = 0.9;
        {hold_line}
    end
    @(timer(0, 0.5n)) begin
        if (V(rst) > 0.45) begin
            level = 0.0;
            remaining = 0.0;
        end else if (remaining > 0.0) begin
            remaining = remaining - 0.5n;
            if (remaining <= 0.0) level = 0.0;
        end
    end
    V(pulse) <+ transition(level, 0, tr, tr);
end
endmodule
"""
    if profile == "soft_limiter":
        hys_update = "hys = 0.0;" if buggy else (
            "if (V(vin) > 0.62) hys = hys_step;\n"
            "            if (V(vin) < 0.38) hys = -hys_step;"
        )
        return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
parameter real tr = 100p;
parameter real gain = 1.8;
parameter real hys_step = 0.08;
real y, hys, target, metricv;
analog begin
    @(initial_step) begin
        y = 0.45;
        hys = 0.0;
        target = 0.45;
        metricv = 0.45;
    end
    @(cross(V(clk) - 0.45, +1)) begin
        if (V(rst) > 0.45) begin
            y = 0.45;
            hys = 0.0;
            target = 0.45;
            metricv = 0.45;
        end else begin
            {hys_update}
            target = gain * (V(vin) - 0.45) + 0.45 + hys;
            y = target;
            if (y > 0.82) y = 0.82; if (y < 0.10) y = 0.10;
            metricv = 0.45 + 2.0 * hys;
        end
    end
    V(out) <+ transition(y, 0, tr, tr);
    V(metric) <+ transition(metricv, 0, tr, tr);
end
endmodule
"""
    if profile == "amp_filter_chain":
        metric_update = "metricv = y;" if buggy else "metricv = target;"
        return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
parameter real tr = 100p;
parameter real gain = 1.8;
parameter real alpha = 0.18;
real s1, s2, y, target, metricv;
analog begin
    @(initial_step) begin
        s1 = 0.45;
        s2 = 0.45;
        y = 0.45;
        target = 0.45;
        metricv = 0.45;
    end
    @(cross(V(clk) - 0.45, +1)) begin
        if (V(rst) > 0.45) begin
            s1 = 0.45;
            s2 = 0.45;
            y = 0.45;
            target = 0.45;
            metricv = 0.45;
        end else begin
            target = gain * (V(vin) - 0.45) + 0.45;
            if (target > 0.9) target = 0.9; if (target < 0.0) target = 0.0;
            s1 = s1 + alpha * (target - s1);
            s2 = s2 + alpha * (s1 - s2);
            y = s2;
            {metric_update}
        end
    end
    V(out) <+ transition(y, 0, tr, tr);
    V(metric) <+ transition(metricv, 0, tr, tr);
end
endmodule
"""
    if profile in {"gain_amp", "two_pole_filter", "conditioning_chain"}:
        clamp = "" if (buggy and profile == "gain_amp") else "if (y > 0.9) y = 0.9; if (y < 0.0) y = 0.0;"
        pole2 = "s2 = s2 + alpha * (s1 - s2);" if not (buggy and profile in {"two_pole_filter", "conditioning_chain", "soft_limiter"}) else "s2 = s1;"
        alpha = "0.45" if profile == "gain_amp" else "0.18"
        state_reset = "0.45" if profile == "two_pole_filter" else "0.0"
        metric_expr = "s1 - s2 + 0.45"
        if buggy and profile == "amp_filter_chain":
            metric_expr = "s1"
        if buggy and profile == "soft_limiter":
            hys_update = "hys = 0.0;"
        else:
            hys_update = "if (V(vin) > 0.62) hys = 0.04;\n            if (V(vin) < 0.38) hys = -0.04;"
        return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
parameter real tr = 100p;
parameter real gain = 1.8;
parameter real alpha = {alpha};
real s1, s2, y, hys;
analog begin
    @(initial_step) begin
        s1 = {state_reset};
        s2 = {state_reset};
        y = {state_reset};
        hys = 0.0;
    end
    @(cross(V(clk) - 0.45, +1)) begin
        if (V(rst) > 0.45) begin
            s1 = {state_reset};
            s2 = {state_reset};
            y = {state_reset};
            hys = 0.0;
        end else begin
            y = gain * (V(vin) - 0.45) + 0.45;
            {hys_update}
            s1 = s1 + alpha * (y + hys - s1);
            {pole2}
            y = s2;
            {clamp}
        end
    end
    V(out) <+ transition(y, 0, tr, tr);
    V(metric) <+ transition({metric_expr}, 0, tr, tr);
end
endmodule
"""
    if profile == "bandgap_reference":
        target_line = "targetv = 0.78 * supplyv;" if buggy else "targetv = vref + 0.020 * (supplyv - 0.75);"
        reset_condition = "supplyv <= 0.05" if buggy else "supplyv < vstart"
        return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
parameter real tr = 100p;
parameter real vth = 0.45;
parameter real vstart = 0.58;
parameter real vref = 0.55;
real refv, metricv, supplyv, targetv;
analog begin
    @(initial_step) begin
        refv = 0.0;
        metricv = 0.0;
    end
    @(cross(V(clk) - vth, +1)) begin
        supplyv = V(vin);
        if (V(rst) > vth || {reset_condition}) begin
            refv = 0.0;
            metricv = 0.0;
        end else begin
            {target_line}
            if (targetv > supplyv - 0.05) targetv = supplyv - 0.05;
            if (targetv < 0.0) targetv = 0.0;
            refv = refv + 0.35 * (targetv - refv);
            metricv = (refv > 0.48) ? 0.9 : 0.2;
        end
        if (refv > 0.9) refv = 0.9;
        if (refv < 0.0) refv = 0.0;
    end
    V(out) <+ transition(refv, 0, tr, tr);
    V(metric) <+ transition(metricv, 0, tr, tr);
end
endmodule
"""
    if profile == "ptat_ctat_reference":
        combine_line = "refv = ptat;" if buggy else "refv = 0.5 * ptat + 0.5 * ctat;"
        return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
parameter real tr = 100p;
parameter real vth = 0.45;
real tempv, ptat, ctat, refv, metricv;
analog begin
    @(initial_step) begin
        refv = 0.45;
        metricv = 0.0;
    end
    @(cross(V(clk) - vth, +1)) begin
        if (V(rst) > vth) begin
            refv = 0.45;
            metricv = 0.0;
        end else begin
            tempv = V(vin);
            if (tempv < 0.0) tempv = 0.0;
            if (tempv > 0.9) tempv = 0.9;
            ptat = 0.18 + 0.34 * tempv;
            ctat = 0.78 - 0.34 * tempv;
            {combine_line}
            metricv = ptat;
        end
        if (refv > 0.9) refv = 0.9;
        if (refv < 0.0) refv = 0.0;
    end
    V(out) <+ transition(refv, 0, tr, tr);
    V(metric) <+ transition(metricv, 0, tr, tr);
end
endmodule
"""
    if profile == "bias_trim_generator":
        disable_condition = "0" if buggy else "ctrlv < 0.25"
        return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
parameter real tr = 100p;
parameter real vth = 0.45;
real ctrlv, targetv, biasv, metricv;
analog begin
    @(initial_step) begin
        biasv = 0.0;
        metricv = 0.0;
    end
    @(cross(V(clk) - vth, +1)) begin
        ctrlv = V(vin);
        if (V(rst) > vth || {disable_condition}) begin
            biasv = 0.0;
            metricv = 0.0;
        end else begin
            targetv = 0.28 + 0.55 * ((ctrlv - 0.25) / 0.65);
            if (targetv > 0.82) targetv = 0.82;
            if (targetv < 0.28) targetv = 0.28;
            biasv = biasv + 0.45 * (targetv - biasv);
            metricv = 0.9;
        end
    end
    V(out) <+ transition(biasv, 0, tr, tr);
    V(metric) <+ transition(metricv, 0, tr, tr);
end
endmodule
"""
    if profile == "por_detector":
        counter_update = "release_count = 4;" if buggy else "release_count = release_count + 1;"
        return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
parameter real tr = 100p;
parameter real vth = 0.45;
parameter real vtrip = 0.62;
real resetv, metricv;
integer release_count;
analog begin
    @(initial_step) begin
        resetv = 0.9;
        metricv = 0.0;
        release_count = 0;
    end
    @(cross(V(clk) - vth, +1)) begin
        if (V(rst) > vth || V(vin) < vtrip) begin
            resetv = 0.9;
            metricv = 0.0;
            release_count = 0;
        end else begin
            {counter_update}
            if (release_count >= 4) begin
                resetv = 0.0;
                metricv = 0.9;
            end else begin
                resetv = 0.9;
                metricv = 0.2;
            end
        end
    end
    V(out) <+ transition(resetv, 0, tr, tr);
    V(metric) <+ transition(metricv, 0, tr, tr);
end
endmodule
"""
    if profile == "uvlo_brownout":
        if buggy:
            update = """if (V(vin) > 0.60) begin
                pgood = 0.9;
            end else begin
                pgood = 0.0;
            end"""
        else:
            update = """if (pgood < 0.45 && V(vin) > 0.65) begin
                pgood = 0.9;
            end else if (pgood > 0.45 && V(vin) < 0.55) begin
                pgood = 0.0;
            end"""
        return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
parameter real tr = 100p;
parameter real vth = 0.45;
real pgood, metricv;
analog begin
    @(initial_step) begin
        pgood = 0.0;
        metricv = 0.9;
    end
    @(cross(V(clk) - vth, +1)) begin
        if (V(rst) > vth) begin
            pgood = 0.0;
        end else begin
            {update}
        end
        metricv = (pgood > 0.45) ? 0.1 : 0.9;
    end
    V(out) <+ transition(pgood, 0, tr, tr);
    V(metric) <+ transition(metricv, 0, tr, tr);
end
endmodule
"""
    if profile == "ldo_regulator":
        target_line = "targetv = 0.62;" if buggy else "targetv = 0.62 - 0.055 * loadv;"
        alpha = "0.85" if buggy else "0.35"
        return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
parameter real tr = 100p;
parameter real vth = 0.45;
real regv, targetv, loadv, errv, metricv;
analog begin
    @(initial_step) begin
        regv = 0.60;
        metricv = 0.9;
    end
    @(cross(V(clk) - vth, +1)) begin
        if (V(rst) > vth) begin
            regv = 0.60;
            metricv = 0.9;
        end else begin
            loadv = V(vin);
            if (loadv < 0.0) loadv = 0.0;
            if (loadv > 0.9) loadv = 0.9;
            {target_line}
            regv = regv + {alpha} * (targetv - regv);
            if (regv > 0.75) regv = 0.75;
            if (regv < 0.25) regv = 0.25;
            errv = regv - targetv;
            if (errv < 0.0) errv = -errv;
            metricv = 0.9 - 4.0 * errv;
            if (metricv < 0.0) metricv = 0.0;
            if (metricv > 0.9) metricv = 0.9;
        end
    end
    V(out) <+ transition(regv, 0, tr, tr);
    V(metric) <+ transition(metricv, 0, tr, tr);
end
endmodule
"""
    if profile == "reference_startup_flow":
        enable_condition = "supply_ok > 0.5" if buggy else "(supply_ok > 0.5 && enablev > 0.5)"
        return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
parameter real tr = 100p;
parameter real vth = 0.45;
real refv, metricv, supply_ok, enablev;
integer settle_count;
analog begin
    @(initial_step) begin
        refv = 0.0;
        metricv = 0.0;
        settle_count = 0;
    end
    @(cross(V(clk) - vth, +1)) begin
        supply_ok = (V(vin) > 0.32) ? 1.0 : 0.0;
        enablev = (V(vin) > 0.55) ? 1.0 : 0.0;
        if (V(rst) > vth || supply_ok < 0.5) begin
            refv = 0.0;
            metricv = 0.0;
            settle_count = 0;
        end else if ({enable_condition}) begin
            refv = refv + 0.32 * (0.55 - refv);
            settle_count = settle_count + 1;
            metricv = (settle_count >= 5 && refv > 0.48) ? 0.9 : 0.25;
        end else begin
            refv = 0.05;
            metricv = 0.1;
            settle_count = 0;
        end
    end
    V(out) <+ transition(refv, 0, tr, tr);
    V(metric) <+ transition(metricv, 0, tr, tr);
end
endmodule
"""
    if profile == "ldo_load_step_flow":
        if buggy:
            update = """targetv = 0.68 - 0.42 * loadv;
            regv = targetv;
            metricv = 0.2;"""
        else:
            update = """targetv = 0.61 - 0.025 * loadv;
            if (loadv > last_load + 0.20) begin
                regv = regv - 0.13;
                recover_count = 0;
            end else if (loadv + 0.20 < last_load) begin
                regv = regv + 0.05;
                recover_count = 0;
            end
            regv = regv + 0.30 * (targetv - regv);
            recover_count = recover_count + 1;
            errv = regv - targetv;
            if (errv < 0.0) errv = -errv;
            metricv = (recover_count >= 5 && errv < 0.045) ? 0.9 : 0.25;"""
        return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
parameter real tr = 100p;
parameter real vth = 0.45;
real regv, targetv, loadv, last_load, errv, metricv;
integer recover_count;
analog begin
    @(initial_step) begin
        regv = 0.60;
        targetv = 0.60;
        last_load = 0.10;
        metricv = 0.9;
        recover_count = 0;
    end
    @(cross(V(clk) - vth, +1)) begin
        if (V(rst) > vth) begin
            regv = 0.60;
            targetv = 0.60;
            last_load = 0.10;
            metricv = 0.9;
            recover_count = 0;
        end else begin
            loadv = V(vin);
            if (loadv < 0.0) loadv = 0.0;
            if (loadv > 0.9) loadv = 0.9;
            {update}
            last_load = loadv;
            if (regv > 0.75) regv = 0.75;
            if (regv < 0.20) regv = 0.20;
        end
    end
    V(out) <+ transition(regv, 0, tr, tr);
    V(metric) <+ transition(metricv, 0, tr, tr);
end
endmodule
"""
    if profile == "lna_gain_compression":
        if buggy:
            body = """linearv = 0.45 + gain * x;
            yv = linearv;
            metricv = 0.1;"""
        else:
            body = """linearv = 0.45 + gain * x;
            yv = linearv;
            metricv = 0.1;
            if (linearv > 0.76) begin
                yv = 0.76 + 0.28 * (linearv - 0.76);
                metricv = 0.8;
            end else if (linearv < 0.14) begin
                yv = 0.14 + 0.28 * (linearv - 0.14);
                metricv = 0.8;
            end"""
        return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
parameter real tr = 100p;
parameter real vth = 0.45;
parameter real gain = 2.2;
real x, linearv, yv, metricv;
analog begin
    @(initial_step) begin
        yv = 0.45;
        metricv = 0.0;
    end
    @(cross(V(clk) - vth, +1)) begin
        if (V(rst) > vth) begin
            yv = 0.45;
            metricv = 0.0;
        end else begin
            x = V(vin) - 0.45;
            {body}
            if (yv > 0.86) yv = 0.86;
            if (yv < 0.04) yv = 0.04;
        end
    end
    V(out) <+ transition(yv, 0, tr, tr);
    V(metric) <+ transition(metricv, 0, tr, tr);
end
endmodule
"""
    if profile == "rf_mixer_downconverter":
        lo_expr = "1.0" if buggy else "((V(clk) > vth) ? 1.0 : -1.0)"
        return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
parameter real tr = 80p;
parameter real vth = 0.45;
parameter real conv_gain = 1.25;
real basev, lov, mixv, metricv;
analog begin
    @(initial_step) begin
        metricv = 0.0;
    end
    @(cross(V(clk) - vth, +1)) begin
        if (V(rst) > vth) begin
            metricv = 0.0;
        end else begin
            metricv = 0.9;
        end
    end
    if (V(rst) > vth) begin
        mixv = 0.45;
    end else begin
        basev = V(vin) - 0.45;
        lov = {lo_expr};
        mixv = 0.45 + conv_gain * basev * lov;
        if (mixv > 0.88) mixv = 0.88;
        if (mixv < 0.02) mixv = 0.02;
    end
    V(out) <+ transition(mixv, 0, tr, tr);
    V(metric) <+ transition(metricv, 0, tr, tr);
end
endmodule
"""
    if profile == "pa_compression":
        if buggy:
            body = """drivev = 0.45 + gain * x;
            yv = drivev;
            metricv = 0.1;"""
        else:
            body = """drivev = 0.45 + gain * x;
            yv = drivev;
            metricv = 0.1;
            if (drivev > 0.78) begin
                yv = 0.78 + 0.18 * (drivev - 0.78);
                metricv = 0.85;
            end else if (drivev < 0.12) begin
                yv = 0.12 + 0.18 * (drivev - 0.12);
                metricv = 0.85;
            end"""
        return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
parameter real tr = 100p;
parameter real vth = 0.45;
parameter real gain = 3.0;
real x, drivev, yv, metricv;
analog begin
    @(initial_step) begin
        yv = 0.45;
        metricv = 0.0;
    end
    @(cross(V(clk) - vth, +1)) begin
        if (V(rst) > vth) begin
            yv = 0.45;
            metricv = 0.0;
        end else begin
            x = V(vin) - 0.45;
            {body}
            if (yv > 0.88) yv = 0.88;
            if (yv < 0.02) yv = 0.02;
        end
    end
    V(out) <+ transition(yv, 0, tr, tr);
    V(metric) <+ transition(metricv, 0, tr, tr);
end
endmodule
"""
    if profile == "log_rssi_detector":
        if buggy:
            code = "rssiv = 0.14 + 2.20 * ampv;"
        else:
            code = """if (ampv < 0.035) begin
                rssiv = 0.12;
            end else if (ampv < 0.11) begin
                rssiv = 0.30;
            end else if (ampv < 0.22) begin
                rssiv = 0.54;
            end else begin
                rssiv = 0.72;
            end"""
        return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
parameter real tr = 100p;
parameter real vth = 0.45;
real ampv, rssiv, metricv;
analog begin
    @(initial_step) begin
        rssiv = 0.12;
        metricv = 0.0;
    end
    @(cross(V(clk) - vth, +1)) begin
        if (V(rst) > vth) begin
            rssiv = 0.12;
            metricv = 0.0;
        end else begin
            ampv = V(vin) - 0.45;
            if (ampv < 0.0) ampv = -ampv;
            {code}
            if (rssiv > 0.82) rssiv = 0.82;
            if (rssiv < 0.08) rssiv = 0.08;
            metricv = ampv * 3.0;
            if (metricv > 0.9) metricv = 0.9;
        end
    end
    V(out) <+ transition(rssiv, 0, tr, tr);
    V(metric) <+ transition(metricv, 0, tr, tr);
end
endmodule
"""
    if profile == "limiting_amplifier":
        if buggy:
            body = """yv = V(vin);
            metricv = 0.0;"""
        else:
            body = """x = V(vin) - 0.45;
            metricv = 0.0;
            if (x > 0.09) begin
                yv = 0.73 + 0.45 * (x - 0.09);
                metricv = 0.85;
            end else if (x < -0.09) begin
                yv = 0.17 + 0.45 * (x + 0.09);
                metricv = 0.85;
            end else begin
                yv = 0.45 + 1.7 * x;
            end"""
        return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
parameter real tr = 100p;
parameter real vth = 0.45;
real x, yv, metricv;
analog begin
    @(initial_step) begin
        yv = 0.45;
        metricv = 0.0;
    end
    @(cross(V(clk) - vth, +1)) begin
        if (V(rst) > vth) begin
            yv = 0.45;
            metricv = 0.0;
        end else begin
            {body}
            if (yv > 0.86) yv = 0.86;
            if (yv < 0.04) yv = 0.04;
        end
    end
    V(out) <+ transition(yv, 0, tr, tr);
    V(metric) <+ transition(metricv, 0, tr, tr);
end
endmodule
"""
    if profile == "agc_receiver_loop":
        if buggy:
            control = """if (ampv > target_amp + deadband) begin
                gainv = gainv + 0.18;
            end else if (ampv < target_amp - deadband) begin
                gainv = gainv - 0.10;
            end"""
        else:
            control = """if (ampv > target_amp + deadband) begin
                gainv = gainv - 0.18;
            end else if (ampv < target_amp - deadband) begin
                gainv = gainv + 0.10;
            end"""
        return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
parameter real tr = 100p;
parameter real vth = 0.45;
parameter real target_amp = 0.18;
parameter real deadband = 0.025;
real gainv, rawv, yv, ampv, errv, metricv;
analog begin
    @(initial_step) begin
        gainv = 2.2;
        yv = 0.45;
        metricv = 0.0;
    end
    @(cross(V(clk) - vth, +1)) begin
        if (V(rst) > vth) begin
            gainv = 2.2;
            yv = 0.45;
            metricv = 0.0;
        end else begin
            rawv = gainv * (V(vin) - 0.45);
            yv = 0.45 + rawv;
            if (yv > 0.88) yv = 0.88;
            if (yv < 0.02) yv = 0.02;
            ampv = yv - 0.45;
            if (ampv < 0.0) ampv = -ampv;
            {control}
            if (gainv > 3.0) gainv = 3.0;
            if (gainv < 0.45) gainv = 0.45;
            errv = ampv - target_amp;
            if (errv < 0.0) errv = -errv;
            metricv = 0.9 - 4.0 * errv;
            if (metricv > 0.9) metricv = 0.9;
            if (metricv < 0.0) metricv = 0.0;
        end
    end
    V(out) <+ transition(yv, 0, tr, tr);
    V(metric) <+ transition(metricv, 0, tr, tr);
end
endmodule
"""
    if profile == "iq_downconversion_chain":
        if buggy:
            qcoef_assign = "qcoef = icoef;"
        else:
            qcoef_assign = """if (phase == 0) qcoef = 0.0;
            else if (phase == 1) qcoef = 1.0;
            else if (phase == 2) qcoef = 0.0;
            else qcoef = -1.0;"""
        return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
parameter real tr = 80p;
parameter real vth = 0.45;
real basev, iv, qv, icoef, qcoef;
integer phase;
analog begin
    @(initial_step) begin
        phase = 3;
        iv = 0.45;
        qv = 0.45;
    end
    @(cross(V(clk) - vth, +1)) begin
        if (V(rst) > vth) begin
            phase = 3;
            iv = 0.45;
            qv = 0.45;
        end else begin
            phase = phase + 1;
            if (phase > 3) phase = 0;
            if (phase == 0) icoef = 1.0;
            else if (phase == 1) icoef = 0.0;
            else if (phase == 2) icoef = -1.0;
            else icoef = 0.0;
            {qcoef_assign}
            basev = V(vin) - 0.45;
            iv = 0.45 + 1.25 * basev * icoef;
            qv = 0.45 + 1.25 * basev * qcoef;
            if (iv > 0.88) iv = 0.88;
            if (iv < 0.02) iv = 0.02;
            if (qv > 0.88) qv = 0.88;
            if (qv < 0.02) qv = 0.02;
        end
    end
    V(out) <+ transition(iv, 0, tr, tr);
    V(metric) <+ transition(qv, 0, tr, tr);
end
endmodule
"""
    if profile == "stimulus_sequencer":
        gate_condition = "V(gate) > 0.45" if not buggy else "V(gate) <= 0.45"
        return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(clk, rst, mode, gate, out, metric);
input clk, rst, mode, gate;
output out, metric;
electrical clk, rst, mode, gate, out, metric;
parameter real tr = 80p;
real y, metricv, ramp_frac, burst_level;
real sweep_t, sweep_k, phase;
integer prbs_state, feedback;
analog begin
    @(initial_step) begin
        y = 0.45;
        metricv = 0.0;
        burst_level = 0.45;
        prbs_state = 7;
    end
    @(cross(V(clk) - 0.45, +1)) begin
        if (V(rst) > 0.45) begin
            prbs_state = 7;
            burst_level = 0.45;
        end else if (V(mode) > 0.60 && {gate_condition}) begin
            feedback = ((prbs_state >> 2) & 1) ^ ((prbs_state >> 1) & 1);
            prbs_state = ((prbs_state & 3) << 1) | feedback;
            burst_level = ((prbs_state & 1) > 0) ? 0.62 : 0.28;
        end
    end
    if (V(rst) > 0.45) begin
        y = 0.45;
        metricv = 0.0;
    end else if (V(mode) < 0.30) begin
        ramp_frac = ($abstime - 3.0e-9) / 23.0e-9;
        if (ramp_frac < 0.0) ramp_frac = 0.0;
        if (ramp_frac > 1.0) ramp_frac = 1.0;
        y = 0.18 + 0.27 * ramp_frac;
        metricv = 0.20;
    end else if (V(mode) < 0.60) begin
        sweep_t = $abstime - 26.0e-9;
        if (sweep_t < 0.0) sweep_t = 0.0;
        if (sweep_t > 36.0e-9) sweep_t = 36.0e-9;
        sweep_k = (116.666666e6 - 50.0e6) / 36.0e-9;
        phase = 2.0 * `M_PI * (50.0e6 * sweep_t + 0.5 * sweep_k * sweep_t * sweep_t);
        y = 0.45 + 0.15 * sin(phase);
        metricv = 0.50;
    end else if (V(gate) > 0.45) begin
        y = burst_level;
        metricv = 0.80;
    end else begin
        y = 0.45;
        metricv = 0.65;
    end
    V(out) <+ transition(y, 0, tr, tr);
    V(metric) <+ transition(metricv, 0, tr, tr);
end
endmodule
"""
    return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(clk, rst, vin, aux, out, metric);
input clk, rst, vin, aux;
output out, metric;
electrical clk, rst, vin, aux, out, metric;
parameter real tr = 100p;
real sample, code, recon, metricv;
integer q;
analog begin
    @(initial_step) begin
        sample = 0.0;
        code = 0.0;
        recon = 0.0;
        metricv = 0.0;
    end
    @(cross(V(clk) - 0.45, +1)) begin
        if (V(rst) > 0.45) begin
            sample = 0.0;
            code = 0.0;
            recon = 0.0;
            metricv = 0.0;
        end else begin
            sample = V(vin);
            q = 0;
            if (sample > 0.9) q = 15;
            else if (sample > 0.0) q = sample / 0.9 * 15.0 + 0.5;
            code = q / 15.0;
            recon = 0.9 * code;
            metricv = (sample > 0.25 && sample < 0.65) ? 0.9 : 0.0;
        end
    end
    V(out) <+ transition(recon, 0, tr, tr);
    V(metric) <+ transition(metricv, 0, tr, tr);
end
endmodule
"""


def tb_source(module: str, form: str) -> str:
    calibration_modules = {
        "calibration_deadband_controller",
        "charge_pump_abstraction",
        "loop_filter_abstraction",
        "successive_approximation_calibration_search_fsm",
        "complete_calibration_loop",
    }
    filter_modules = {
        "soft_hysteretic_limiter",
        "voltage_gain_amplifier",
        "higher_order_filter",
        "amplifier_filter_chain",
    }
    bias_reference_sources = {
        "bandgap_reference_macro_model": """Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 period=2n width=1n rise=50p fall=50p
Vrst (rst 0) vsource type=pwl wave=[0 0.9 2n 0.9 2.1n 0 80n 0]
Vvin (vin 0) vsource type=pwl wave=[0 0.20 7.9n 0.20 8n 0.70 39.9n 0.70 40n 0.85 65n 0.85 65.1n 0.50 72n 0.50 72.1n 0.75 80n 0.75]""",
        "ptat_ctat_reference_generator": """Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 period=2n width=1n rise=50p fall=50p
Vrst (rst 0) vsource type=pwl wave=[0 0.9 2n 0.9 2.1n 0 80n 0]
Vvin (vin 0) vsource type=pwl wave=[0 0.15 18n 0.15 18.1n 0.45 42n 0.45 42.1n 0.80 80n 0.80]""",
        "bias_voltage_generator_with_enable_trim": """Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 period=2n width=1n rise=50p fall=50p
Vrst (rst 0) vsource type=pwl wave=[0 0.9 2n 0.9 2.1n 0 80n 0]
Vvin (vin 0) vsource type=pwl wave=[0 0.10 11.9n 0.10 12n 0.35 31.9n 0.35 32n 0.75 53.9n 0.75 54n 0.10 65.9n 0.10 66n 0.55 80n 0.55]""",
        "power_on_reset_detector": """Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 period=2n width=1n rise=50p fall=50p
Vrst (rst 0) vsource type=pwl wave=[0 0.9 2n 0.9 2.1n 0 80n 0]
Vvin (vin 0) vsource type=pwl wave=[0 0.20 7.9n 0.20 8n 0.75 43.9n 0.75 44n 0.50 53.9n 0.50 54n 0.75 80n 0.75]""",
        "uvlo_brownout_detector": """Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 period=2n width=1n rise=50p fall=50p
Vrst (rst 0) vsource type=pwl wave=[0 0.9 2n 0.9 2.1n 0 80n 0]
Vvin (vin 0) vsource type=pwl wave=[0 0.50 9.9n 0.50 10n 0.70 27.9n 0.70 28n 0.58 42.9n 0.58 43n 0.52 54.9n 0.52 55n 0.62 66.9n 0.62 67n 0.68 80n 0.68]""",
        "ldo_regulator_macro_model": """Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 period=2n width=1n rise=50p fall=50p
Vrst (rst 0) vsource type=pwl wave=[0 0.9 2n 0.9 2.1n 0 80n 0]
Vvin (vin 0) vsource type=pwl wave=[0 0.10 17.9n 0.10 18n 0.80 43.9n 0.80 44n 0.25 65.9n 0.25 66n 0.65 80n 0.65]""",
        "reference_startup_enable_flow": """Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 period=2n width=1n rise=50p fall=50p
Vrst (rst 0) vsource type=pwl wave=[0 0.9 2n 0.9 2.1n 0 80n 0]
Vvin (vin 0) vsource type=pwl wave=[0 0.15 9.9n 0.15 10n 0.40 23.9n 0.40 24n 0.70 53.9n 0.70 54n 0.20 62.9n 0.20 63n 0.70 80n 0.70]""",
        "ldo_load_step_recovery_flow": """Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 period=2n width=1n rise=50p fall=50p
Vrst (rst 0) vsource type=pwl wave=[0 0.9 2n 0.9 2.1n 0 80n 0]
Vvin (vin 0) vsource type=pwl wave=[0 0.10 15.9n 0.10 16n 0.85 41.9n 0.85 42n 0.20 61.9n 0.20 62n 0.75 80n 0.75]""",
    }
    rf_afe_sources = {
        "lna_gain_compression_macro": """Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 period=2n width=1n rise=50p fall=50p
Vrst (rst 0) vsource type=pwl wave=[0 0.9 2n 0.9 2.1n 0 80n 0]
Vvin (vin 0) vsource type=pwl wave=[0 0.45 7.9n 0.45 8n 0.52 23.9n 0.52 24n 0.78 47.9n 0.78 48n 0.26 65.9n 0.26 66n 0.60 80n 0.60]""",
        "rf_mixer_downconverter_macro": """Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 period=4n width=2n rise=50p fall=50p
Vrst (rst 0) vsource type=pwl wave=[0 0.9 2n 0.9 2.1n 0 80n 0]
Vvin (vin 0) vsource type=pwl wave=[0 0.45 8n 0.45 8.1n 0.66 34n 0.66 34.1n 0.24 58n 0.24 58.1n 0.55 80n 0.55]""",
        "pa_compression_macro": """Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 period=2n width=1n rise=50p fall=50p
Vrst (rst 0) vsource type=pwl wave=[0 0.9 2n 0.9 2.1n 0 80n 0]
Vvin (vin 0) vsource type=pwl wave=[0 0.45 7.9n 0.45 8n 0.53 23.9n 0.53 24n 0.74 45.9n 0.74 46n 0.22 65.9n 0.22 66n 0.58 80n 0.58]""",
        "log_rssi_power_detector": """Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 period=2n width=1n rise=50p fall=50p
Vrst (rst 0) vsource type=pwl wave=[0 0.9 2n 0.9 2.1n 0 80n 0]
Vvin (vin 0) vsource type=pwl wave=[0 0.45 8n 0.45 8.1n 0.49 23.9n 0.49 24n 0.56 43.9n 0.56 44n 0.70 63.9n 0.70 64n 0.30 80n 0.30]""",
        "limiting_amplifier_frontend": """Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 period=2n width=1n rise=50p fall=50p
Vrst (rst 0) vsource type=pwl wave=[0 0.9 2n 0.9 2.1n 0 80n 0]
Vvin (vin 0) vsource type=pwl wave=[0 0.45 7.9n 0.45 8n 0.50 21.9n 0.50 22n 0.78 43.9n 0.78 44n 0.18 63.9n 0.18 64n 0.56 80n 0.56]""",
        "agc_receiver_leveling_loop": """Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 period=2n width=1n rise=50p fall=50p
Vrst (rst 0) vsource type=pwl wave=[0 0.9 2n 0.9 2.1n 0 80n 0]
Vvin (vin 0) vsource type=pwl wave=[0 0.45 8n 0.52 21.9n 0.52 22n 0.78 55.9n 0.78 56n 0.55 80n 0.55]""",
        "iq_downconversion_chain": """Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 period=2n width=1n rise=50p fall=50p
Vrst (rst 0) vsource type=pwl wave=[0 0.9 2n 0.9 2.1n 0 80n 0]
Vvin (vin 0) vsource type=pwl wave=[0 0.45 7.9n 0.45 8n 0.72 55.9n 0.72 56n 0.45 65.9n 0.45 66n 0.25 80n 0.25]""",
    }
    if module == "dac_mismatch_unit_weighting_model":
        instance = f"XDUT (b0 b1 b2 b3 out) {module}"
        sources = """Vb0 (b0 0) vsource type=pwl wave=[0 0 5n 0 5.1n 0.9 10n 0.9 10.1n 0 20n 0 20.1n 0.9 40n 0.9]
Vb1 (b1 0) vsource type=pwl wave=[0 0 12n 0 12.1n 0.9 40n 0.9]
Vb2 (b2 0) vsource type=pwl wave=[0 0 20n 0 20.1n 0.9 40n 0.9]
Vb3 (b3 0) vsource type=pwl wave=[0 0 30n 0 30.1n 0.9 40n 0.9]"""
        saves = "save b0 b1 b2 b3 out"
    elif "pulse_stretcher" in module:
        instance = f"XDUT (trig rst pulse) {module}"
        sources = """Vtrig (trig 0) vsource type=pwl wave=[0 0 1n 0 1.1n 0.9 1.3n 0 3n 0 3.1n 0.9 3.3n 0 16n 0 16.1n 0.9 16.3n 0 18n 0 18.1n 0.9 18.3n 0 24n 0 24.1n 0.9 24.3n 0 50n 0]
Vrst  (rst  0) vsource type=pwl wave=[0 0 25n 0 25.1n 0.9 28n 0.9 28.1n 0]"""
        saves = "save trig rst pulse"
    elif module == "programmable_stimulus_sequencer":
        instance = f"XDUT (clk rst mode gate out metric) {module}"
        sources = """Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 period=2n width=1n rise=50p fall=50p
Vrst (rst 0) vsource type=pwl wave=[0 0.9 2n 0.9 2.1n 0 90n 0]
Vmode (mode 0) vsource type=pwl wave=[0 0 25.9n 0 26n 0.45 61.9n 0.45 62n 0.9 90n 0.9]
Vgate (gate 0) vsource type=pwl wave=[0 0 65.9n 0 66n 0.9 75.9n 0.9 76n 0 79.9n 0 80n 0.9 88n 0.9 88.1n 0 90n 0]"""
        saves = "save clk rst mode gate out metric"
    elif module == "charge_pump_abstraction":
        instance = f"XDUT (clk rst up dn vctrl metric) {module}"
        sources = """Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 period=2n width=1n rise=50p fall=50p
Vrst (rst 0) vsource type=pwl wave=[0 0.9 2n 0.9 2.1n 0 62n 0 62.1n 0.9 66n 0.9 66.1n 0 80n 0]
Vup (up 0) vsource type=pwl wave=[0 0 5.8n 0 5.85n 0.9 6.35n 0.9 6.4n 0 7.8n 0 7.85n 0.9 8.35n 0.9 8.4n 0 9.8n 0 9.85n 0.9 10.35n 0.9 10.4n 0 11.8n 0 11.85n 0.9 12.35n 0.9 12.4n 0 13.8n 0 13.85n 0.9 14.35n 0.9 14.4n 0 15.8n 0 15.85n 0.9 16.35n 0.9 16.4n 0 17.8n 0 17.85n 0.9 18.35n 0.9 18.4n 0 80n 0]
Vdn (dn 0) vsource type=pwl wave=[0 0 31.8n 0 31.85n 0.9 32.35n 0.9 32.4n 0 33.8n 0 33.85n 0.9 34.35n 0.9 34.4n 0 35.8n 0 35.85n 0.9 36.35n 0.9 36.4n 0 37.8n 0 37.85n 0.9 38.35n 0.9 38.4n 0 39.8n 0 39.85n 0.9 40.35n 0.9 40.4n 0 80n 0]"""
        saves = "save clk rst up dn vctrl metric"
    elif module in calibration_modules:
        instance = f"XDUT (clk rst vin out metric) {module}"
        sources = """Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 period=2n width=1n rise=50p fall=50p
Vrst (rst 0) vsource type=pwl wave=[0 0.9 2n 0.9 2.1n 0 62n 0 62.1n 0.9 66n 0.9 66.1n 0 80n 0]
Vvin (vin 0) vsource type=pwl wave=[0 0.45 8n 0.47 14n 0.43 20n 0.75 40n 0.18 58n 0.72 68n 0.47 74n 0.78 80n 0.78]"""
        saves = "save clk rst vin out metric"
    elif module in filter_modules:
        instance = f"XDUT (clk rst vin out metric) {module}"
        sources = """Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 period=2n width=1n rise=50p fall=50p
Vrst (rst 0) vsource type=pwl wave=[0 0.9 2n 0.9 2.1n 0 80n 0]
Vvin (vin 0) vsource type=pwl wave=[0 0.45 8n 0.45 12n 0.9 28n 0.9 31n 0.45 37n 0.45 42n 0.1 58n 0.1 61n 0.45 67n 0.45 72n 0.85 80n 0.85]"""
        saves = "save clk rst vin out metric"
    elif module in bias_reference_sources:
        instance = f"XDUT (clk rst vin out metric) {module}"
        sources = bias_reference_sources[module]
        saves = "save clk rst vin out metric"
    elif module in rf_afe_sources:
        instance = f"XDUT (clk rst vin out metric) {module}"
        sources = rf_afe_sources[module]
        saves = "save clk rst vin out metric"
    else:
        instance = f"XDUT (clk rst vin out metric) {module}"
        sources = """Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 period=2n width=1n rise=50p fall=50p
Vrst (rst 0) vsource type=pwl wave=[0 0.9 2n 0.9 2.1n 0 80n 0]
Vvin (vin 0) vsource type=pwl wave=[0 0.2 10n 0.25 25n 0.75 55n 0.35 80n 0.65]"""
        saves = "save clk rst vin out metric"
    include = f'ahdl_include "{module}.va"'
    if form == "bugfix":
        include = 'ahdl_include "dut_fixed.va"'
    tran_line = "tran tran stop=90n maxstep=0.25n" if module == "programmable_stimulus_sequencer" else "tran tran stop=80n maxstep=0.5n"
    return f"""simulator lang=spectre
global 0

{include}

{sources}

{instance}

{tran_line}
{saves}
"""


def port_contract(spec: DesignedSpec) -> dict[str, str]:
    if spec.profile == "weighted_dac":
        return {
            "module": f"module {spec.module}(b0, b1, b2, b3, out);",
            "directions": "input b0, b1, b2, b3;\noutput out;",
            "disciplines": "electrical b0, b1, b2, b3, out",
            "signals": "b0..b3 are voltage-coded logic bits, low=0 V and high=0.9 V with threshold 0.45 V. out is a bounded voltage reconstruction in [0, 0.9] V.",
            "saved": "b0 b1 b2 b3 out",
        }
    if spec.profile == "pulse_stretcher":
        return {
            "module": f"module {spec.module}(trig, rst, pulse);",
            "directions": "input trig, rst;\noutput pulse;",
            "disciplines": "electrical trig, rst, pulse",
            "signals": "trig and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. pulse is a voltage-coded output pulse. Each rising trig edge refreshes the pulse deadline to trigger_time + 4 ns; rst high forces pulse low.",
            "saved": "trig rst pulse",
        }
    if spec.profile == "loop_filter":
        return {
            "module": f"module {spec.module}(clk, rst, vin, out, metric);",
            "directions": "input clk, rst, vin;\noutput out, metric;",
            "disciplines": "electrical clk, rst, vin, out, metric",
            "signals": "clk and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. vin is a signed loop-error stimulus around 0.45 V. out is a bounded loop-control voltage. metric is a voltage-coded update/convergence observable.",
            "saved": "clk rst vin out metric",
        }
    if spec.profile == "charge_pump":
        return {
            "module": f"module {spec.module}(clk, rst, up, dn, vctrl, metric);",
            "directions": "input clk, rst, up, dn;\noutput vctrl, metric;",
            "disciplines": "electrical clk, rst, up, dn, vctrl, metric",
            "signals": "clk, rst, up, and dn are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. A sampled UP-only pulse increases vctrl, a sampled DN-only pulse decreases vctrl, simultaneous or absent pulses hold the control voltage, and rst high resets vctrl to midscale. metric is a voltage-coded UP/DN/hold status observable.",
            "saved": "clk rst up dn vctrl metric",
        }
    if spec.profile == "deadband_cal":
        return {
            "module": f"module {spec.module}(clk, rst, vin, out, metric);",
            "directions": "input clk, rst, vin;\noutput out, metric;",
            "disciplines": "electrical clk, rst, vin, out, metric",
            "signals": "clk and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. vin is a signed calibration error around 0.45 V. out is a bounded trim voltage that holds inside the deadband and steps only outside it. metric is high only on an accepted trim update.",
            "saved": "clk rst vin out metric",
        }
    if spec.profile == "sar_cal_fsm":
        return {
            "module": f"module {spec.module}(clk, rst, vin, out, metric);",
            "directions": "input clk, rst, vin;\noutput out, metric;",
            "disciplines": "electrical clk, rst, vin, out, metric",
            "signals": "clk and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. vin is a signed calibration decision stimulus around 0.45 V. out is the bounded SAR trial trim voltage. metric is a voltage-coded done flag asserted after the search window.",
            "saved": "clk rst vin out metric",
        }
    if spec.profile == "cal_loop":
        return {
            "module": f"module {spec.module}(clk, rst, vin, out, metric);",
            "directions": "input clk, rst, vin;\noutput out, metric;",
            "disciplines": "electrical clk, rst, vin, out, metric",
            "signals": "clk and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. vin is the external offset/error stimulus around 0.45 V. The internal controller drives correction opposite the measured residual error, out is the bounded corrected plant response, and metric is high when out is close to 0.45 V.",
            "saved": "clk rst vin out metric",
        }
    if spec.profile in {"charge_pump", "gain_cal_loop"}:
        return {
            "module": f"module {spec.module}(clk, rst, vin, out, metric);",
            "directions": "input clk, rst, vin;\noutput out, metric;",
            "disciplines": "electrical clk, rst, vin, out, metric",
            "signals": "clk and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. vin is a signed error stimulus around 0.45 V. out is a bounded trim/control voltage. metric is a voltage-coded status or completion observable.",
            "saved": "clk rst vin out metric",
        }
    if spec.profile == "soft_limiter":
        return {
            "module": f"module {spec.module}(clk, rst, vin, out, metric);",
            "directions": "input clk, rst, vin;\noutput out, metric;",
            "disciplines": "electrical clk, rst, vin, out, metric",
            "signals": "clk and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. vin is an analog voltage stimulus. out is the bounded conditioned voltage. metric exposes the limiter hysteresis state: it goes high after upper-threshold excursions, low after lower-threshold excursions, and preserves that state during mid-level hold windows.",
            "saved": "clk rst vin out metric",
        }
    if spec.profile == "amp_filter_chain":
        return {
            "module": f"module {spec.module}(clk, rst, vin, out, metric);",
            "directions": "input clk, rst, vin;\noutput out, metric;",
            "disciplines": "electrical clk, rst, vin, out, metric",
            "signals": "clk and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. vin is an analog voltage stimulus. out is the bounded filtered voltage. metric exposes the bounded pre-filter amplified target used to verify that out lags and settles toward the amplified input.",
            "saved": "clk rst vin out metric",
        }
    if spec.profile in {"gain_amp", "two_pole_filter", "conditioning_chain"}:
        return {
            "module": f"module {spec.module}(clk, rst, vin, out, metric);",
            "directions": "input clk, rst, vin;\noutput out, metric;",
            "disciplines": "electrical clk, rst, vin, out, metric",
            "signals": "clk and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. vin is an analog voltage stimulus. out is the bounded conditioned voltage. metric exposes the filter/settling internal response.",
            "saved": "clk rst vin out metric",
        }
    if spec.profile in {
        "bandgap_reference",
        "ptat_ctat_reference",
        "bias_trim_generator",
        "por_detector",
        "uvlo_brownout",
        "ldo_regulator",
        "reference_startup_flow",
        "ldo_load_step_flow",
    }:
        signal_contracts = {
            "bandgap_reference": "clk and rst are voltage-coded logic signals. vin is the public supply-ramp stimulus. out is the generated reference voltage, held low below startup threshold and regulated near nominal after startup. metric is a voltage-coded reference-valid observable.",
            "ptat_ctat_reference": "clk and rst are voltage-coded logic signals. vin is a normalized temperature-code voltage. out is the compensated reference voltage. metric exposes the PTAT branch trend as a public observable without revealing hidden checker code.",
            "bias_trim_generator": "clk and rst are voltage-coded logic signals. vin is an enable/trim request voltage: low disables the bias, higher values select larger trim. out is the generated bias voltage. metric marks enabled bias operation.",
            "por_detector": "clk and rst are voltage-coded logic signals. vin is the supply-ramp/brownout stimulus. out is an active-high reset voltage that releases only after a power-good delay and reasserts on brownout. metric marks released/reset-valid status.",
            "uvlo_brownout": "clk and rst are voltage-coded logic signals. vin is the supply monitor voltage. out is a power-good voltage with UVLO hysteresis. metric is high during undervoltage/brownout and low during power-good operation.",
            "ldo_regulator": "clk and rst are voltage-coded logic signals. vin is a bounded load/disturbance-control voltage. out is the regulated output-voltage macro-model response. metric marks regulation error/recovery quality.",
            "reference_startup_flow": "clk and rst are voltage-coded logic signals. vin encodes the public supply/enable schedule: low is supply-off, mid is supply-good with enable low, and high is supply-good with enable asserted. out is the reference startup voltage. metric marks valid settled reference status.",
            "ldo_load_step_flow": "clk and rst are voltage-coded logic signals. vin is the public load-step stimulus. out is the regulator output after transient droop and recovery. metric marks recovered regulation after each load transition.",
        }
        return {
            "module": f"module {spec.module}(clk, rst, vin, out, metric);",
            "directions": "input clk, rst, vin;\noutput out, metric;",
            "disciplines": "electrical clk, rst, vin, out, metric",
            "signals": signal_contracts[spec.profile],
            "saved": "clk rst vin out metric",
        }
    if spec.profile in {
        "lna_gain_compression",
        "rf_mixer_downconverter",
        "pa_compression",
        "log_rssi_detector",
        "limiting_amplifier",
        "agc_receiver_loop",
        "iq_downconversion_chain",
    }:
        signal_contracts = {
            "lna_gain_compression": "clk and rst are voltage-coded logic signals. vin is an RF/AFE input envelope around 0.45 V common mode. out is the amplified voltage with soft large-signal compression. metric is high when compression is active.",
            "rf_mixer_downconverter": "clk is the public LO-polarity waveform and rst is voltage-coded reset. vin is an RF input envelope around 0.45 V common mode. out is the LO-polarity-converted baseband voltage. metric marks active conversion.",
            "pa_compression": "clk and rst are voltage-coded logic signals. vin is the PA drive voltage around 0.45 V common mode. out is the amplified output with large-signal compression and rail limits. metric marks compression/limit operation.",
            "log_rssi_detector": "clk and rst are voltage-coded logic signals. vin is the received signal envelope around 0.45 V common mode. out is a monotonic logarithmic RSSI voltage code. metric exposes normalized envelope magnitude.",
            "limiting_amplifier": "clk and rst are voltage-coded logic signals. vin is the receiver front-end voltage around 0.45 V common mode. out is a bounded limiting-amplifier output that preserves polarity. metric marks limiting operation.",
            "agc_receiver_loop": "clk and rst are voltage-coded logic signals. vin is the receiver input envelope around 0.45 V common mode. The internal gain-control loop reduces gain under overload and restores a target output amplitude. out is the leveled receiver output and metric is high near target amplitude.",
            "iq_downconversion_chain": "clk is the quadrature LO phase-advance clock and rst is voltage-coded reset. vin is the RF input envelope around 0.45 V common mode. out is the I-path baseband observable and metric is the Q-path baseband observable.",
        }
        return {
            "module": f"module {spec.module}(clk, rst, vin, out, metric);",
            "directions": "input clk, rst, vin;\noutput out, metric;",
            "disciplines": "electrical clk, rst, vin, out, metric",
            "signals": signal_contracts[spec.profile],
            "saved": "clk rst vin out metric",
        }
    if spec.profile == "stimulus_sequencer":
        return {
            "module": f"module {spec.module}(clk, rst, mode, gate, out, metric);",
            "directions": "input clk, rst, mode, gate;\noutput out, metric;",
            "disciplines": "electrical clk, rst, mode, gate, out, metric",
            "signals": "clk and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. mode selects ramp, sine, or burst/PRBS behavior. gate enables the burst segment. out is the generated stimulus waveform. metric is a voltage-coded segment-status observable.",
            "saved": "clk rst mode gate out metric",
        }
    return {
        "module": f"module {spec.module}(clk, rst, vin, aux, out, metric);",
        "directions": "input clk, rst, vin, aux;\noutput out, metric;",
        "disciplines": "electrical clk, rst, vin, aux, out, metric",
        "signals": "clk and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. vin is the analog stimulus. aux is a reserved analog control input. out is the reconstructed output voltage. metric is a voltage-coded public observable.",
        "saved": "clk rst vin out metric",
    }


def prompt_text(row: dict[str, str], spec: DesignedSpec, form: str) -> str:
    family = FORM_TO_FAMILY[form]
    tran_line = "tran tran stop=90n maxstep=0.25n" if spec.profile == "stimulus_sequencer" else "tran tran stop=80n maxstep=0.5n"
    target_artifacts = {
        "dut": [f"{spec.module}.va"],
        "tb": [f"tb_{spec.module}.scs"],
        "bugfix": ["dut_fixed.va"],
        "e2e": [f"{spec.module}.va", f"tb_{spec.module}.scs"],
    }[form]
    target_list = ", ".join(f"`{name}`" for name in target_artifacts)
    output_lines = "\n".join(f"- `{name}`" for name in target_artifacts)
    if form == "tb":
        task_line = "Write a Spectre transient testbench for the described behavioral Verilog-A module."
        form_requirements = (
            f"- Generate the target artifact: {target_list}.\n"
            "- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic."
        )
    elif form == "bugfix":
        task_line = (
            "Repair the supplied buggy Verilog-A implementation using the public behavior checks and "
            "task description above. Treat the failing implementation as an observable mismatch; infer the repair "
            "from the source and public behavior rather than assuming a named root cause."
        )
        form_requirements = (
            f"- Generate the repaired target artifact: {target_list}.\n"
            "- Preserve the public module name, positional ports, voltage-domain behavior, and observable contract."
        )
    elif form == "e2e":
        task_line = "Write both the Verilog-A behavioral module and a Spectre transient testbench."
        form_requirements = (
            f"- Generate all target artifacts: {target_list}.\n"
            "- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic."
        )
    else:
        task_line = "Write the Verilog-A behavioral module only."
        form_requirements = (
            f"- Generate the target artifact: {target_list}.\n"
            "- The module must satisfy the public interface and observable behavior contract."
        )
    checks = "\n".join(f"- {item}" for item in spec.behavior_checks)
    target_lines = PUBLIC_BEHAVIOR_TARGETS.get(spec.profile, ())
    targets = ""
    if target_lines:
        targets = "\n## Public Behavioral Targets\n\n" + "\n".join(f"- {item}" for item in target_lines) + "\n"
    ports = port_contract(spec)
    disciplines = ports["disciplines"]
    if not disciplines.rstrip().endswith(";"):
        disciplines = disciplines.rstrip() + ";"
    abstraction_note = ""
    if spec.profile == "loop_filter":
        abstraction_note = (
            "\nThis is a sampled/event-driven behavioral abstraction of the loop-filter "
            "control trend. It must not require current-domain charge storage, true "
            "continuous-time RC integration, or KCL/KVL solving.\n"
        )
    elif spec.profile in {
        "bandgap_reference",
        "ptat_ctat_reference",
        "bias_trim_generator",
        "por_detector",
        "uvlo_brownout",
        "ldo_regulator",
        "reference_startup_flow",
        "ldo_load_step_flow",
    }:
        abstraction_note = (
            "\nThis is a voltage-domain macro-model task for bias/reference/power "
            "management behavior. Model observable startup, threshold, trim, "
            "hysteresis, droop, or recovery behavior with event-driven voltage "
            "state updates. Do not use branch currents, transistor devices, "
            "process-device equations, or true current-mode regulation loops.\n"
        )
    elif spec.profile in {
        "lna_gain_compression",
        "rf_mixer_downconverter",
        "pa_compression",
        "log_rssi_detector",
        "limiting_amplifier",
        "agc_receiver_loop",
        "iq_downconversion_chain",
    }:
        abstraction_note = (
            "\nThis is a voltage-domain RF/AFE behavioral macromodel task. "
            "Model observable gain, compression, LO polarity, RSSI, limiting, "
            "AGC, or I/Q baseband behavior with event-driven voltage states. "
            "Do not implement transistor RF physics, S-parameters, current-domain "
            "loads, communication modem algorithms, or full link-level decoding.\n"
        )
    return f"""# Task: {row['entry_id']}:{form}

## Release Task Contract

- Form: `{form}`
- Level: `{row['level']}`
- Category: {row['category']}
- Base function: {row['base_function']}
- Domain: `voltage`
- Target artifact(s): {target_list}
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

{form_requirements}

## Public Verilog-A Interface

- `{spec.module}.va` declares module `{spec.module}` with positional ports from the public port contract below.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
{tran_line}
```

The release harness expects these exact public scalar observables:

```text
{ports['saved']}
```

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

## Public Behavior Checks

{checks}
{targets}

## Output Contract

Return exactly these source artifacts:

{output_lines}

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

### {row['base_function']} ({family})

{task_line}

Behavioral intent:

{spec.summary}

Module name: `{spec.module}`.
Domain: pure voltage-domain behavioral Verilog-A.
Do not use current contributions, transistor-level devices, AC/noise analysis,
or KCL/KVL solving assumptions.
{abstraction_note}

Public port contract:

```verilog
{ports['module']}
{ports['directions']}
{disciplines}
```

Signal contract:

{ports['signals']}

Saved waveform columns:

```text
{ports['saved']}
```

Public behavior checks:

{checks}

Public transient contract:

```spectre
{tran_line}
```
"""


def meta_payload(row: dict[str, str], spec: DesignedSpec, form: str) -> dict[str, object]:
    task_id = f"{row['entry_id']}_{form}"
    family = FORM_TO_FAMILY[form]
    artifacts = {
        "dut": [f"{spec.module}.va"],
        "tb": [f"tb_{spec.module}.scs"],
        "bugfix": ["dut_fixed.va"],
        "e2e": [f"{spec.module}.va", f"tb_{spec.module}.scs"],
    }[form]
    inputs = ["prompt.md"]
    payload: dict[str, object] = {
        "id": task_id,
        "task_id": task_id,
        "asset_type": "vabench_task",
        "benchmark": "vabench-release-v1",
        "release_entry_id": row["entry_id"],
        "family": family,
        "category": row["category"],
        "domain": "voltage",
        "track": track_for_category(row["category"]),
        "difficulty": difficulty_for_row(row),
        "expected_backend": "evas",
        "inputs": inputs,
        "artifacts": artifacts,
        "scoring": ["dut_compile", "tb_compile", "sim_correct"],
        "behavior_checks": list(spec.behavior_checks),
        "designed_source": True,
    }
    if form == "bugfix":
        payload["inputs"] = ["prompt.md", "gold/dut_buggy.va"]
        payload["public_inputs"] = ["prompt.md", "gold/dut_buggy.va"]
        payload["submission_artifacts"] = ["dut_fixed.va"]
        payload["private_reference_artifacts"] = ["gold/dut_fixed.va"]
    return payload


def checks_text(spec: DesignedSpec, form: str) -> str:
    if form == "tb":
        must_include = ['"tran"', '"save"']
    else:
        must_include = ['"transition("']
        if spec.profile in {"pulse_stretcher"}:
            must_include.append('"@(timer("')
        elif spec.profile != "weighted_dac":
            must_include.append('"@(cross("')
    checks = "\n".join(f"    - {token}" for token in must_include)
    behavior = "\n".join(f"    - \"{item}\"" for item in spec.behavior_checks)
    role_lines = ""
    if form == "dut":
        role_lines = 'dut_companion_role: "function_checked_dut"\nstrong_benchmark_claim: true\n'
    return f"""syntax:
  must_include:
{checks}
  must_not_include:
    - "I("
    - "ddt("
{role_lines}\
dut_compile:
  backend: "evas"
tb_compile:
  backend: "evas"
sim_correct:
  checks:
{behavior}
parity:
  reference: "spectre"
  status: "pending_until_evas_spectre_rerun"
  notes:
    - "Designed release source; no imported historical EVAS/Spectre dual evidence yet."
"""


def write_form_assets(entry_dir: Path, row: dict[str, str], spec: DesignedSpec, form: str) -> dict[str, object]:
    form_dir = entry_dir / "forms" / form
    gold_dir = form_dir / "gold"
    gold_dir.mkdir(parents=True, exist_ok=True)
    (form_dir / "prompt.md").write_text(prompt_text(row, spec, form), encoding="utf-8")
    (form_dir / "meta.json").write_text(json.dumps(meta_payload(row, spec, form), indent=2) + "\n", encoding="utf-8")
    (form_dir / "checks.yaml").write_text(checks_text(spec, form), encoding="utf-8")
    gold_files: list[Path] = []
    if form in {"dut", "e2e"}:
        path = gold_dir / f"{spec.module}.va"
        path.write_text(va_source(spec.module, spec.profile), encoding="utf-8")
        gold_files.append(path)
    if form in {"tb", "e2e"}:
        path = gold_dir / f"tb_{spec.module}.scs"
        path.write_text(tb_source(spec.module, form), encoding="utf-8")
        gold_files.append(path)
    if form == "bugfix":
        buggy = gold_dir / "dut_buggy.va"
        fixed = gold_dir / "dut_fixed.va"
        buggy.write_text(va_source(spec.module, spec.profile, buggy=True), encoding="utf-8")
        fixed.write_text(va_source(spec.module, spec.profile), encoding="utf-8")
        gold_files.extend([buggy, fixed])
    (form_dir / "SOURCE_TASK.md").write_text(
        "\n".join(
            [
                f"# Designed Release Source: {row['entry_id']} {form}",
                "",
                f"- Source: `designed_release_spec:{row['entry_id']}`",
                f"- Behavior: {spec.summary}",
                "- EVAS/Spectre status: pending rerun",
                "",
                "This form was materialized directly from the release taxonomy",
                "because no existing source task matched the requested function.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return {
        "form": form,
        "release_path": rel(form_dir),
        "prompt": rel(form_dir / "prompt.md"),
        "meta": rel(form_dir / "meta.json"),
        "checks": rel(form_dir / "checks.yaml"),
        "gold": [rel(path) for path in gold_files],
        "public_inputs": ["prompt.md", "gold/dut_buggy.va"] if form == "bugfix" else ["prompt.md"],
        "submission_artifacts": ["dut_fixed.va"] if form == "bugfix" else meta_payload(row, spec, form)["artifacts"],
        "private_reference_artifacts": ["gold/dut_fixed.va"] if form == "bugfix" else [],
        "asset_materialized": True,
        "historical_dual_expected": False,
        "static_status": "pending",
        "evas_status": "pending",
        "spectre_status": "pending",
        "dual_evidence": f"benchmark-vabench-release-v1/evidence/dual/{row['entry_id']}/{form}/evidence.json",
        "fresh_dual_rerun_required": True,
        "source_path": f"designed_release_spec:{row['entry_id']}",
    }


def materialize_entry(row: dict[str, str], spec: DesignedSpec, *, refresh_existing: bool = False) -> bool:
    entry_path = release_entry_path(TASKS_ROOT, row["entry_id"])
    if not entry_path.exists():
        entry_dir = release_category_entry_dir(TASKS_ROOT, row["entry_id"], row["category"])
        entry_dir.mkdir(parents=True, exist_ok=True)
        entry_path = entry_dir / "release_entry.json"
        entry = {
            "id": row["entry_id"],
            "benchmark": "vabench-release-v1",
            "release_entry_id": row["entry_id"],
            "level": row["level"],
            "track": track_for_category(row["category"]),
            "difficulty": difficulty_for_row(row),
            "category": row["category"],
            "base_function": row["base_function"],
            "package_status": row["package_status"],
            "score_surface": row["score_surface"],
            "source_base_id": slugify(row["base_function"]),
            "canonical_kernel": "",
            "source_registry_status": "designed_from_release_taxonomy",
            "source_evidence_status": "designed_source_pending_dual",
            "source_tasks": [],
            "release_tasks": [],
            "missing_forms": required_forms(row),
            "certification": {
                "static": "pending",
                "evas": "pending",
                "spectre": "pending",
                "evidence": "",
            },
            "counts": {
                "benchmark_score": False,
                "model_capability": False,
                "l0_conformance": False,
            },
            "release_blockers": ["source_materialization"],
        }
    else:
        entry = json.loads(entry_path.read_text(encoding="utf-8"))
    existing_tasks_by_form = {
        str(task.get("form")): task
        for task in entry.get("release_tasks", [])
        if isinstance(task, dict)
    }
    existing_certification = entry.get("certification") if isinstance(entry.get("certification"), dict) else None
    existing_release_blockers = (
        list(entry.get("release_blockers", [])) if isinstance(entry.get("release_blockers"), list) else None
    )
    if entry.get("release_tasks") and not refresh_existing:
        return False
    entry_dir = entry_path.parent
    forms = required_forms(row)
    release_tasks = [write_form_assets(entry_dir, row, spec, form) for form in forms]
    for task in release_tasks:
        previous = existing_tasks_by_form.get(str(task.get("form")))
        if not isinstance(previous, dict):
            continue
        for key in (
            "static_status",
            "evas_status",
            "spectre_status",
            "dual_evidence",
            "fresh_dual_rerun_required",
            "historical_dual_expected",
        ):
            if key in previous:
                task[key] = previous[key]
    entry["canonical_kernel"] = spec.module
    entry["track"] = track_for_category(row["category"])
    entry["difficulty"] = difficulty_for_row(row)
    entry["source_registry_status"] = "designed_from_release_taxonomy"
    entry["source_evidence_status"] = "designed_source_pending_dual"
    entry["source_tasks"] = [
        {
            "form": form,
            "source_path": f"designed_release_spec:{row['entry_id']}",
            "prompt": True,
            "meta": True,
            "checks": True,
            "gold": True,
            "asset_complete": True,
            "checks_has_sim_correct": True,
            "checks_has_parity": True,
            "checks_normalized_for_release": False,
        }
        for form in forms
    ]
    entry["release_tasks"] = release_tasks
    entry["missing_forms"] = []
    if existing_certification is not None:
        entry["certification"] = existing_certification
    else:
        entry.setdefault(
            "certification",
            {
                "static": "pending",
                "evas": "pending",
                "spectre": "pending",
                "evidence": "",
            },
        )
    entry.setdefault(
        "counts",
        {
            "benchmark_score": False,
            "model_capability": False,
            "l0_conformance": False,
        },
    )
    entry["release_blockers"] = (
        existing_release_blockers
        if existing_release_blockers is not None
        else ["static_validation", "evas_certification", "spectre_certification"]
    )
    entry_path.write_text(json.dumps(entry, indent=2) + "\n", encoding="utf-8")
    (entry_dir / "README.md").write_text(
        "\n".join(
            [
                f"# {row['base_function']}",
                "",
                f"- Entry: `{row['entry_id']}`",
                f"- Level: `{row['level']}`",
                f"- Category: `{row['category']}`",
                f"- Materialized forms: `{', '.join(forms)}`",
                "- Source: designed from the release taxonomy",
                "- Certification: static pending; EVAS/Spectre pending rerun",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return True


def update_selected_manifest(materialized_ids: set[str]) -> None:
    rows = read_csv(SELECTED_MANIFEST_CSV)
    if not rows:
        return
    tracker = {row["entry_id"]: row for row in read_csv(TRACKER_CSV)}
    row_by_id = {row["entry_id"]: row for row in rows}
    fieldnames = list(rows[0].keys())
    for entry_id in sorted(materialized_ids - set(row_by_id)):
        tracker_row = tracker[entry_id]
        rows.append(
            {
                "entry_id": entry_id,
                "base_function": tracker_row["base_function"],
                "package_status": tracker_row["package_status"],
                "forms_materialized": "",
                "missing_forms": "",
                "source_paths": "",
                "invalid_source_paths": "",
                "package_task_dir": rel(release_category_entry_dir(TASKS_ROOT, entry_id, tracker_row["category"])),
                "notes": "",
            }
        )
    for row in rows:
        if row["entry_id"] not in materialized_ids:
            continue
        forms = required_forms(tracker[row["entry_id"]])
        row["forms_materialized"] = "|".join(forms)
        row["missing_forms"] = ""
        row["source_paths"] = f"designed_release_spec:{row['entry_id']}"
        row["invalid_source_paths"] = ""
        row["notes"] = "designed release source generated; dual evidence pending rerun"
    rows = sorted(rows, key=lambda item: item["entry_id"])
    if fieldnames:
        with SELECTED_MANIFEST_CSV.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    else:
        write_csv(SELECTED_MANIFEST_CSV, rows)

    materialized = [row for row in rows if row["forms_materialized"]]
    lines = [
        "# vaBench Release Selected Manifest",
        "",
        "Date: 2026-05-15",
        "",
        "This manifest records selected L1/L2 release entries created by the",
        "long-run materializer. Rows without release-ready source tasks are kept",
        "as explicit pending package entries rather than hidden missing work.",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| selected entries | {len(rows)} |",
        f"| entries with copied or designed source assets | {len(materialized)} |",
        f"| entries pending source design | {len(rows) - len(materialized)} |",
        "",
        "## Rows",
        "",
        "| Entry | Forms | Missing forms | Source paths | Notes |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['entry_id']}` | `{row['forms_materialized']}` | `{row['missing_forms']}` | `{row['source_paths']}` | {row['notes']} |"
        )
    SELECTED_MANIFEST_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Materialize designed vaBench release source tasks.")
    parser.add_argument(
        "--refresh-existing",
        action="store_true",
        help="Regenerate existing designed release source assets from current templates.",
    )
    args = parser.parse_args()

    rows = read_csv(TRACKER_CSV)
    materialized: set[str] = set()
    for row in rows:
        spec = DESIGNED_SPECS.get(row["entry_id"])
        if spec and materialize_entry(row, spec, refresh_existing=args.refresh_existing):
            materialized.add(row["entry_id"])
    update_selected_manifest(materialized)
    forms = 0
    tracker = {row["entry_id"]: row for row in rows}
    for entry_id in materialized:
        forms += len(required_forms(tracker[entry_id]))
    print(f"materialized designed release entries: {len(materialized)}; forms: {forms}")


if __name__ == "__main__":
    main()
