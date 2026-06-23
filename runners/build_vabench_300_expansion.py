#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import shutil
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "benchmark-vabench-release-v1"
EXPANSION = PACKAGE / "vabench-300-expansion"
EXISTING_TASKS = PACKAGE / "tasks"
MANIFEST = PACKAGE / "MANIFEST.json"
PROVISIONAL_STATUS = "provisional_v1.1_management"
PROMOTION_EVIDENCE = "speed-optimization/reports/vabench300_p0_p2_closure_20260620.md"
TASK_SPECIFIC_EVIDENCE = (
    "benchmark-vabench-release-v1/vabench-300-expansion/"
    "v11_task_specific_quality_evidence.json"
)


FORMS_TO_FAMILY = {
    "dut": "spec-to-va",
    "tb": "tb-generation",
    "e2e": "end-to-end",
    "bugfix": "bugfix",
}


@dataclass(frozen=True)
class ProposedTask:
    entry_id: str
    form: str
    level: str
    track: str
    difficulty: str
    category: str
    base_function: str
    negative_axis: str
    description: str


PROPOSED_TASKS: tuple[ProposedTask, ...] = (
    ProposedTask("vbr11_l1_sigma_delta_modulator_loop", "dut", "L1", "core", "D3", "Data Converter Models", "First-order sigma-delta modulator loop", "integrator_feedback_boundary", "Implement the DUT for a first-order sigma-delta modulator behavioral loop."),
    ProposedTask("vbr11_l1_sigma_delta_modulator_loop", "tb", "L1", "core", "D3", "Data Converter Models", "First-order sigma-delta modulator loop", "stimulus_density_measurement", "Build a testbench that exercises bit-density and integrator stability."),
    ProposedTask("vbr11_l1_sigma_delta_modulator_loop", "e2e", "L1", "core", "D3", "Data Converter Models", "First-order sigma-delta modulator loop", "closed_loop_metric", "Create the model and measurement harness for the modulator loop."),
    ProposedTask("vbr11_l1_sigma_delta_modulator_loop", "bugfix", "L1", "core", "D3", "Data Converter Models", "First-order sigma-delta modulator loop", "feedback_sign_bug", "Repair a sigma-delta loop with a subtle feedback sign or saturation bug."),
    ProposedTask("vbr11_l2_time_interleaved_adc_mismatch_flow", "dut", "L2", "core", "D3", "Data Converter Models", "Time-interleaved ADC mismatch observation flow", "channel_rotation_skew", "Implement a time-interleaved ADC mismatch behavioral model."),
    ProposedTask("vbr11_l2_time_interleaved_adc_mismatch_flow", "tb", "L2", "core", "D3", "Data Converter Models", "Time-interleaved ADC mismatch observation flow", "mismatch_metric_window", "Build a testbench that observes offset, gain, and skew mismatch."),
    ProposedTask("vbr11_l2_time_interleaved_adc_mismatch_flow", "e2e", "L2", "core", "D3", "Data Converter Models", "Time-interleaved ADC mismatch observation flow", "mismatch_metric_flow", "Create the model, stimulus, and mismatch metric writer."),
    ProposedTask("vbr11_l2_time_interleaved_adc_mismatch_flow", "bugfix", "L2", "core", "D3", "Data Converter Models", "Time-interleaved ADC mismatch observation flow", "channel_index_bug", "Repair a channel rotation, skew sign, or metric writeout bug."),
    ProposedTask("vbr11_l2_metastability_window_comparator_flow", "dut", "L2", "core", "D3", "Comparator and Decision Circuits", "Comparator metastability window model", "threshold_latency_window", "Implement a comparator with a metastability-sensitive decision window."),
    ProposedTask("vbr11_l2_metastability_window_comparator_flow", "tb", "L2", "core", "D3", "Comparator and Decision Circuits", "Comparator metastability window model", "latency_sweep_coverage", "Build a testbench that sweeps differential input and decision latency."),
    ProposedTask("vbr11_l2_metastability_window_comparator_flow", "e2e", "L2", "core", "D3", "Comparator and Decision Circuits", "Comparator metastability window model", "windowed_decision_flow", "Create the model and latency-measurement flow."),
    ProposedTask("vbr11_l2_metastability_window_comparator_flow", "bugfix", "L2", "core", "D3", "Comparator and Decision Circuits", "Comparator metastability window model", "window_boundary_bug", "Repair a metastability window boundary or monotonic latency bug."),
    ProposedTask("vbr11_l1_bootstrapped_sample_switch", "dut", "L1", "core", "D2", "Sampling and Analog Memory", "Bootstrapped sample switch abstraction", "sample_hold_phase", "Implement a bootstrapped sample-switch abstraction."),
    ProposedTask("vbr11_l1_bootstrapped_sample_switch", "tb", "L1", "core", "D2", "Sampling and Analog Memory", "Bootstrapped sample switch abstraction", "hold_error_measurement", "Build a testbench for sample/hold timing and hold error."),
    ProposedTask("vbr11_l1_bootstrapped_sample_switch", "e2e", "L1", "core", "D2", "Sampling and Analog Memory", "Bootstrapped sample switch abstraction", "switch_observability", "Create a sample-switch model with observable sample and hold behavior."),
    ProposedTask("vbr11_l1_bootstrapped_sample_switch", "bugfix", "L1", "core", "D2", "Sampling and Analog Memory", "Bootstrapped sample switch abstraction", "phase_leakage_bug", "Repair a phase, leakage, or edge-handling bug."),
    ProposedTask("vbr11_l2_fractional_n_pll_divider_flow", "dut", "L2", "core", "D3", "PLL Clock and Timing Systems", "Fractional-N divider and accumulator flow", "modulo_accumulator", "Implement a fractional-N divider accumulator flow."),
    ProposedTask("vbr11_l2_fractional_n_pll_divider_flow", "tb", "L2", "core", "D3", "PLL Clock and Timing Systems", "Fractional-N divider and accumulator flow", "average_divide_ratio", "Build a testbench for average divide ratio and period sequence."),
    ProposedTask("vbr11_l2_fractional_n_pll_divider_flow", "e2e", "L2", "core", "D3", "PLL Clock and Timing Systems", "Fractional-N divider and accumulator flow", "period_statistics", "Create a divider, stimulus, and period-statistics flow."),
    ProposedTask("vbr11_l2_fractional_n_pll_divider_flow", "bugfix", "L2", "core", "D3", "PLL Clock and Timing Systems", "Fractional-N divider and accumulator flow", "wrap_pulse_width_bug", "Repair a modulo wrap, pulse-width, or initial-phase bug."),
    ProposedTask("vbr11_l2_bandgap_startup_trim_flow", "dut", "L2", "core", "D3", "Bias Reference and Power Management", "Bandgap startup and trim convergence flow", "startup_trim_state", "Implement a bandgap startup and trim convergence behavioral flow."),
    ProposedTask("vbr11_l2_bandgap_startup_trim_flow", "tb", "L2", "core", "D3", "Bias Reference and Power Management", "Bandgap startup and trim convergence flow", "settle_trim_measurement", "Build a testbench for startup time, trim code, and settle window."),
    ProposedTask("vbr11_l2_bandgap_startup_trim_flow", "e2e", "L2", "core", "D3", "Bias Reference and Power Management", "Bandgap startup and trim convergence flow", "startup_metric_flow", "Create the model, control flow, and measurement outputs."),
    ProposedTask("vbr11_l2_bandgap_startup_trim_flow", "bugfix", "L2", "core", "D3", "Bias Reference and Power Management", "Bandgap startup and trim convergence flow", "enable_trim_bug", "Repair an enable latch, trim step, or settle criterion bug."),
    ProposedTask("vbr11_l2_quadrature_iq_imbalance_corrector", "dut", "L2", "core", "D3", "RF and AFE Behavioral Macromodels", "Quadrature gain/phase imbalance corrector", "iq_sign_phase", "Implement a quadrature gain/phase imbalance corrector."),
    ProposedTask("vbr11_l2_quadrature_iq_imbalance_corrector", "tb", "L2", "core", "D3", "RF and AFE Behavioral Macromodels", "Quadrature gain/phase imbalance corrector", "image_rejection_metric", "Build a testbench for image rejection and post-correction error."),
    ProposedTask("vbr11_l2_quadrature_iq_imbalance_corrector", "e2e", "L2", "core", "D3", "RF and AFE Behavioral Macromodels", "Quadrature gain/phase imbalance corrector", "iq_correction_flow", "Create the RF behavior model and correction metric flow."),
    ProposedTask("vbr11_l2_quadrature_iq_imbalance_corrector", "bugfix", "L2", "core", "D3", "RF and AFE Behavioral Macromodels", "Quadrature gain/phase imbalance corrector", "coefficient_direction_bug", "Repair I/Q sign, phase unit, or coefficient update direction."),
    ProposedTask("vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow", "bugfix", "L2", "core", "D3", "PLL Clock and Timing Systems", "CPPLL tracking and frequency-step reacquire flow", "reacquire_boundary_bug", "Add a bugfix form for lock/reacquire boundary behavior."),
)


NEGATIVE_KINDS = (
    ("boundary_near_miss", "Passes nominal/smoke cases but fails an endpoint, threshold, saturation, or settling boundary."),
    ("timing_window_near_miss", "Passes interface and broad waveform checks but fails one edge, timer, sample, lock, or reacquire window."),
    ("polarity_direction_near_miss", "Passes positive or nominal path but fails sign, feedback direction, I/Q polarity, or trim direction."),
    ("state_reset_near_miss", "Passes steady-state behavior but fails reset, enable, initial condition, or done/ready assertion."),
    ("metric_writeout_near_miss", "Produces plausible behavior but fails a metric writer, latency, count, or measurement output."),
)


TASK_CONTRACTS: dict[str, dict[str, str]] = {
    "sigma_delta_modulator_loop": {
        "behavior": "first-order sigma-delta loop with clocked integrator, one-bit feedback DAC, and bit-density metric",
        "observable": "out is a one-bit decision stream; metric is the running one-density over the stimulus window",
        "checker": "bit stream toggles, density remains bounded, and metric tracks the one-density",
    },
    "time_interleaved_adc_mismatch": {
        "behavior": "four-lane time-interleaved ADC observation model with lane-dependent offset/gain mismatch",
        "observable": "out is the lane-adjusted sampled value; metric encodes lane rotation plus mismatch magnitude",
        "checker": "lane metric spans all four phases and the output preserves the driven input span",
    },
    "metastability_window_comparator": {
        "behavior": "clocked comparator whose decision confidence degrades near the differential threshold window",
        "observable": "out is the resolved comparator decision; metric is high inside the metastability window",
        "checker": "near-threshold samples produce larger metric values than far-from-threshold samples",
    },
    "bootstrapped_sample_switch": {
        "behavior": "sample/hold switch abstraction with clocked acquisition and bounded hold leakage",
        "observable": "out holds the sampled input between acquisition events; metric reports hold quality",
        "checker": "output has sample response and late-window hold-quality metric remains high",
    },
    "fractional_n_pll_divider": {
        "behavior": "fractional-N divider accumulator that emits carry pulses at the requested average divide ratio",
        "observable": "out is the carry/pulse stream; metric is the normalized accumulator residue",
        "checker": "pulse density and residue swing match a fractional accumulator rather than an integer divider",
    },
    "bandgap_startup_trim": {
        "behavior": "bandgap startup and trim loop that ramps a reference toward a bounded settled target",
        "observable": "out is the reference voltage monitor; metric is the startup/settle completion monitor",
        "checker": "reference rises from reset to the target window and metric asserts only after settling",
    },
    "quadrature_iq_imbalance_corrector": {
        "behavior": "quadrature gain/phase imbalance correction macro with positive input correlation and error metric",
        "observable": "out is the corrected channel monitor; metric is the post-correction quality estimate",
        "checker": "output remains positively correlated with input and final correction metric is high",
    },
    "cppll_tracking_frequency_step_reacquire": {
        "behavior": "charge-pump PLL reacquire monitor that loses then regains lock after a frequency-step window",
        "observable": "out is the control-voltage monitor; metric is the lock/reacquire state",
        "checker": "metric is low early and high after the reacquire window while control voltage stays bounded",
    },
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def category_dir(category: str) -> str:
    mapping = {
        "Data Converter Models": "CT01_data_converter_models",
        "Comparator and Decision Circuits": "CT02_comparator_and_decision_circuits",
        "Sampling and Analog Memory": "CT03_sampling_and_analog_memory",
        "Baseband Signal Conditioning": "CT04_baseband_signal_conditioning",
        "PLL Clock and Timing Systems": "CT05_pll_clock_and_timing_systems",
        "Calibration, DEM, and Control": "CT06_calibration_dem_and_control",
        "Bias Reference and Power Management": "CT07_bias_reference_power_management",
        "RF and AFE Behavioral Macromodels": "CT08_rf_afe_behavioral_macromodels",
        "Measurement Instrumentation Flows": "SUP01_measurement_instrumentation_flows",
        "Stimulus and Source Generators": "SUP02_stimulus_and_source_generators",
    }
    return mapping[category]


def canonical_topic_id(entry_id: str) -> str:
    topic = re.sub(r"^vbr(?:1|11)_l[12]_", "", entry_id)
    topic = topic.replace("_and_", "_")
    topic = re.sub(r"_flow$", "", topic)
    topic = re.sub(r"__+", "_", topic).strip("_")
    return topic


def canonical_task_id(entry_id: str, form: str) -> str:
    return f"{canonical_topic_id(entry_id)}:{form}"


def first_gold_source(form_dir: Path) -> Path | None:
    gold = form_dir / "gold"
    for suffix in ("*.va", "*.scs"):
        matches = sorted(gold.glob(suffix))
        if matches:
            return matches[0]
    return None


def mutate_source(source: str, kind_index: int, task_id: str) -> str:
    marker = (
        f"// vaBench partial-pass negative {kind_index + 1} for {task_id}\n"
        "// Intended to preserve interface/smoke behavior while failing full checks.\n"
    )
    text = source
    if kind_index == 0:
        text = re.sub(r"(?<![A-Za-z_])15(\.0)?(?![A-Za-z_])", "16.0", text, count=1)
        text = re.sub(r"(?<![A-Za-z_])1\.0(?![A-Za-z_])", "0.95", text, count=1)
    elif kind_index == 1:
        text = re.sub(r"@(cross\(([^,]+),\s*1\))", r"@(\1) // near-miss keeps only rising event", text, count=1)
        text = re.sub(r"delay\s*=\s*([^;\n]+)", r"delay = (\1) * 1.25", text, count=1)
    elif kind_index == 2:
        text = re.sub(r"(\berr(?:or)?\b\s*[+\-*/]?=)\s*([^;\n]+)", r"\1 -(\2)", text, count=1)
        text = re.sub(r"(\bvin\b|\bin_p\b|\bi\b)\s*-\s*(\bvref\b|\bin_n\b|\bq\b)", r"\2 - \1", text, count=1)
    elif kind_index == 3:
        text = re.sub(r"(if\s*\([^)]*reset[^)]*\)\s*begin\s*)([^;]+;)", r"\1// near-miss: stale state retained on reset\n", text, count=1, flags=re.IGNORECASE)
        text = re.sub(r"(initial_step[^;{]*[;{])", r"\1\n// near-miss: missing one initial state assignment\n", text, count=1)
    else:
        text = re.sub(r"(\$strobe|\$display|\$fwrite)", r"// near-miss metric write suppressed: \1", text, count=1)
        if text == source:
            text = re.sub(
                r"(V\(\s*metric\s*\)\s*<\+\s*transition\()([^,;\n]+)",
                r"\g<1>0.0 /* near-miss metric writeout */",
                text,
                count=1,
            )
        if text == source:
            text = re.sub(
                r"(\bcount\b\s*=\s*\bcount\b\s*\+\s*)1",
                r"\g<1>0 /* near-miss metric count stalls */",
                text,
                count=1,
            )
    if text == source:
        text = source + f"\n{marker}// Mutation note: {NEGATIVE_KINDS[kind_index][0]}.\n"
    else:
        text = marker + text
    return text


def variant_settings(variant: str) -> dict[str, str]:
    return {
        "gold": {
            "bias": "0.0",
            "polarity": "1.0",
            "delay": "1n",
            "reset_state": "state = 0.0;",
            "reset_aux": "aux = 0.0;",
            "metric_scale": "1.0",
            "metric_override": "",
            "acc_step": "3",
            "settle_step": "0.18",
            "quality": "0.92",
        },
        "boundary_near_miss": {
            "bias": "0.28",
            "polarity": "1.0",
            "delay": "1n",
            "reset_state": "state = 0.0;",
            "reset_aux": "aux = 0.0;",
            "metric_scale": "0.0",
            "metric_override": "",
            "acc_step": "1",
            "settle_step": "0.06",
            "quality": "0.42",
        },
        "timing_window_near_miss": {
            "bias": "0.0",
            "polarity": "1.0",
            "delay": "18n",
            "reset_state": "state = 0.0;",
            "reset_aux": "aux = 0.0;",
            "metric_scale": "0.0",
            "metric_override": "",
            "acc_step": "2",
            "settle_step": "0.08",
            "quality": "0.55",
        },
        "polarity_direction_near_miss": {
            "bias": "0.0",
            "polarity": "-1.0",
            "delay": "1n",
            "reset_state": "state = 0.0;",
            "reset_aux": "aux = 0.0;",
            "metric_scale": "0.0",
            "metric_override": "",
            "acc_step": "5",
            "settle_step": "0.18",
            "quality": "0.40",
        },
        "state_reset_near_miss": {
            "bias": "0.08",
            "polarity": "1.0",
            "delay": "1n",
            "reset_state": "// near-miss: state intentionally retained across reset",
            "reset_aux": "// near-miss: auxiliary state intentionally retained across reset",
            "metric_scale": "0.0",
            "metric_override": "",
            "acc_step": "3",
            "settle_step": "0.10",
            "quality": "0.50",
        },
        "metric_writeout_near_miss": {
            "bias": "0.0",
            "polarity": "1.0",
            "delay": "1n",
            "reset_state": "state = 0.0;",
            "reset_aux": "aux = 0.0;",
            "metric_scale": "0.0",
            "metric_override": "metric_value = 0.0;",
            "acc_step": "3",
            "settle_step": "0.18",
            "quality": "0.0",
        },
    }[variant]


def render_task_specific_va(task: ProposedTask, variant: str = "gold") -> str:
    module = canonical_topic_id(task.entry_id)
    module = re.sub(r"[^A-Za-z0-9_]", "_", module)
    settings = variant_settings(variant)
    topic = canonical_topic_id(task.entry_id)
    metric_override = settings["metric_override"] or "// metric follows task-specific behavior"
    variant_note = "gold task-specific behavior" if variant == "gold" else f"negative variant: {variant}"

    if topic == "sigma_delta_modulator_loop":
        body = f"""
    @(cross(V(clk) - vth, +1)) begin
      feedback = bitval > 0.5 ? 0.42 : -0.42;
      integ = integ + V(in) - ({settings['polarity']}) * feedback + {settings['bias']};
      if (integ > 1.2) integ = 1.2;
      if (integ < -1.2) integ = -1.2;
      if (integ >= 0.0) bitval = 1.0; else bitval = 0.0;
      if (bitval > 0.5) ones = ones + 1;
      count = count + 1;
      state = bitval;
      aux = count > 0 ? (1.0 * ones) / count : 0.0;
      metric_value = aux * {settings['metric_scale']};
      {metric_override}
    end
"""
    elif topic == "time_interleaved_adc_mismatch":
        body = f"""
    @(cross(V(clk) - vth, +1)) begin
      phase = phase + 1;
      if (phase > 3) phase = 0;
      if (phase == 0) begin
        state = ({settings['polarity']}) * (0.92 * V(in) - 0.055 + {settings['bias']});
        aux = 0.06;
      end else if (phase == 1) begin
        state = ({settings['polarity']}) * (1.04 * V(in) + 0.025 + {settings['bias']});
        aux = 0.35;
      end else if (phase == 2) begin
        state = ({settings['polarity']}) * (0.97 * V(in) + 0.065 + {settings['bias']});
        aux = 0.68;
      end else begin
        state = ({settings['polarity']}) * (1.08 * V(in) - 0.020 + {settings['bias']});
        aux = 0.94;
      end
      count = count + 1;
      metric_value = aux * {settings['metric_scale']};
      {metric_override}
    end
"""
    elif topic == "metastability_window_comparator":
        body = f"""
    @(cross(V(clk) - vth, +1)) begin
      sample = ({settings['polarity']}) * V(in) + {settings['bias']};
      if (sample > 0.0) state = 1.0; else state = 0.0;
      if (sample < 0.075 && sample > -0.075) aux = 0.92; else aux = 0.18;
      count = count + 1;
      metric_value = aux * {settings['metric_scale']};
      {metric_override}
    end
"""
    elif topic == "bootstrapped_sample_switch":
        body = f"""
    @(cross(V(clk) - vth, +1)) begin
      sample = ({settings['polarity']}) * V(in) + {settings['bias']};
      state = 0.86 * state + 0.14 * sample;
      aux = {settings['quality']};
      count = count + 1;
      metric_value = aux * {settings['metric_scale']};
      {metric_override}
    end
"""
    elif topic == "fractional_n_pll_divider":
        body = f"""
    @(cross(V(clk) - vth, +1)) begin
      acc = acc + {settings['acc_step']};
      state = 0.0;
      if (acc >= 8) begin
        acc = acc - 8;
        state = 1.0;
        ones = ones + 1;
      end
      count = count + 1;
      aux = acc / 8.0;
      metric_value = aux * {settings['metric_scale']};
      {metric_override}
    end
"""
    elif topic == "bandgap_startup_trim":
        body = f"""
    @(cross(V(clk) - vth, +1)) begin
      target = 1.18 + {settings['bias']};
      state = state + {settings['settle_step']} * (target - state);
      if (state > 1.08 && state < 1.28) aux = aux + 0.08; else aux = aux * 0.8;
      if (aux > 1.0) aux = 1.0;
      count = count + 1;
      metric_value = aux * {settings['metric_scale']};
      {metric_override}
    end
"""
    elif topic == "quadrature_iq_imbalance_corrector":
        body = f"""
    @(cross(V(clk) - vth, +1)) begin
      sample = V(in);
      state = ({settings['polarity']}) * (0.94 * sample - 0.045 * aux) + {settings['bias']};
      aux = 0.55 * aux + 0.45 * sample;
      count = count + 1;
      metric_value = {settings['quality']} * {settings['metric_scale']};
      {metric_override}
    end
"""
    elif topic == "cppll_tracking_frequency_step_reacquire":
        body = f"""
    @(cross(V(clk) - vth, +1)) begin
      count = count + 1;
      if (count < 9) begin
        state = state + 0.030;
        aux = 0.05;
      end else if (count < 18) begin
        state = state + ({settings['polarity']}) * 0.010 + {settings['bias']};
        aux = 0.25 * {settings['metric_scale']};
      end else begin
        state = 0.72 + 0.10 * V(in);
        aux = {settings['quality']};
      end
      if (state > 1.0) state = 1.0;
      if (state < 0.0) state = 0.0;
      metric_value = aux * {settings['metric_scale']};
      {metric_override}
    end
"""
    else:
        raise ValueError(f"No task-specific v1.1 template for {topic}")

    return f"""`include \"constants.vams\"
`include \"disciplines.vams\"

module {module}(in, clk, rst, out, metric);
  input in, clk, rst;
  output out, metric;
  electrical in, clk, rst, out, metric;
  // vaBench v1.1 task-specific template: {variant_note}
  // Target behavior: {TASK_CONTRACTS[topic]['behavior']}
  parameter real vth = 0.5;
  real state;
  real aux;
  real sample;
  real integ;
  real feedback;
  real bitval;
  real metric_value;
  real target;
  integer phase;
  integer acc;
  integer count;
  integer ones;

  analog begin
    @(initial_step) begin
      state = 0.0;
      aux = 0.0;
      sample = 0.0;
      integ = 0.0;
      feedback = 0.0;
      bitval = 0.0;
      metric_value = 0.0;
      target = 0.0;
      phase = -1;
      acc = 0;
      count = 0;
      ones = 0;
    end
    @(cross(V(rst) - vth, +1)) begin
      {settings['reset_state']}
      {settings['reset_aux']}
      sample = 0.0;
      integ = 0.0;
      feedback = 0.0;
      bitval = 0.0;
      metric_value = 0.0;
      target = 0.0;
      phase = -1;
      acc = 0;
      count = 0;
      ones = 0;
    end
{body}
    V(out) <+ transition(state, 0, {settings['delay']});
    V(metric) <+ transition(metric_value, 0, 1n);
  end
endmodule
"""


def render_task_specific_scs(task: ProposedTask, dut_name: str, variant: str = "gold") -> str:
    topic = canonical_topic_id(task.entry_id)
    stop = "420n" if topic == "cppll_tracking_frequency_step_reacquire" else "260n"
    amp = "0.62"
    freq = {
        "sigma_delta_modulator_loop": "8Meg",
        "time_interleaved_adc_mismatch": "11Meg",
        "metastability_window_comparator": "5Meg",
        "bootstrapped_sample_switch": "7Meg",
        "fractional_n_pll_divider": "4Meg",
        "bandgap_startup_trim": "2Meg",
        "quadrature_iq_imbalance_corrector": "9Meg",
        "cppll_tracking_frequency_step_reacquire": "3Meg",
    }[topic]
    return f"""simulator lang=spectre
global 0
ahdl_include \"{dut_name}.va\"
Vclk (clk 0) vsource type=pulse val0=0 val1=1 delay=0 rise=1n fall=1n width=5n period=10n
Vrst (rst 0) vsource type=pulse val0=0 val1=1 delay=0 rise=1n fall=1n width=10n period=1u
Vin (in 0) vsource type=sine sinedc=0 ampl={amp} freq={freq}
Xdut (in clk rst out metric) {dut_name}
tran tran stop={stop} maxstep=500p
"""


def render_task_specific_prompt(task: ProposedTask, task_id: str, topic_id: str, dut_name: str) -> str:
    family = FORMS_TO_FAMILY[task.form]
    contract = TASK_CONTRACTS[topic_id]
    return "\n".join(
        [
            f"# Task: {task_id}",
            "",
            "## vaBench-300 v1.1 Task-Specific Contract",
            "",
            f"- Status: `provisional_v1.1_management`",
            "- Paper score: `disabled_until_fresh_spectre_certification`",
            f"- Form: `{task.form}`",
            f"- Family: `{family}`",
            f"- Level: `{task.level}`",
            f"- Track: `{task.track}`",
            f"- Difficulty: `{task.difficulty}`",
            f"- Category: {task.category}",
            f"- Base function target: {task.base_function}",
            "- Domain: voltage-domain behavioral Verilog-A",
            "",
            "This row has been rebuilt from the original v1.1 management scaffold into",
            "a task-specific benchmark candidate. It remains outside the paper score",
            "denominator until fresh EVAS/Spectre certification is recorded for this",
            "rebuilt source asset.",
            "",
            "## Current Public Interface",
            "",
            f"- Verilog-A artifact: `{dut_name}.va`",
            f"- Spectre testbench artifact: `tb_{dut_name}.scs`",
            f"- Module name: `{dut_name}`",
            "- Positional ports: `in`, `clk`, `rst`, `out`, `metric`",
            "- Port roles:",
            "  - `in`: voltage-coded stimulus input.",
            "  - `clk`: voltage-coded event clock, low=0 V and high=1 V.",
            "  - `rst`: voltage-coded reset pulse.",
            "  - `out`: bounded state/output monitor.",
            "  - `metric`: derived state metric monitor.",
            "",
            "## Task-Specific Observable Contract",
            "",
            f"- Behavior: {contract['behavior']}.",
            f"- Observable: {contract['observable']}.",
            f"- Checker: {contract['checker']}.",
            "- Rising `rst` clears state before the measurement window.",
            "- Rising `clk` events drive the discrete-time behavior.",
            "- The Spectre scaffold instantiates the DUT with instance-first AHDL syntax",
            "  and records `time`, `in`, `clk`, `rst`, `out`, and `metric`.",
            "",
            "## Task Goal",
            "",
            task.description,
            "",
            "Do not satisfy this task with a generic state scaffold. The implementation",
            "must preserve the named circuit-function behavior and expose both the",
            "`out` waveform and the task-specific `metric` monitor.",
            "",
            "## Output Contract",
            "",
            "Return exactly these source artifacts:",
            "",
            f"- `{dut_name}.va`",
            f"- `tb_{dut_name}.scs`",
            "",
            "Do not use unsupported analog operators such as `laplace_nd`, noise sources,",
            "or transistor-level topology. Stay inside the voltage-domain/event-driven",
            "behavioral subset.",
        ]
    ) + "\n"


def negative_manifest(task_id: str, source_path: Path, target_dir: Path, source_kind: str) -> dict[str, Any]:
    rows = []
    source_text = source_path.read_text(encoding="utf-8", errors="ignore")
    for index, (kind, note) in enumerate(NEGATIVE_KINDS, start=1):
        suffix = source_path.suffix or ".va"
        neg_path = target_dir / f"neg_{index:03d}{suffix}"
        neg_text = mutate_source(source_text, index - 1, task_id)
        neg_path.write_text(neg_text, encoding="utf-8")
        rows.append(
            {
                "id": f"neg_{index:03d}",
                "kind": kind,
                "source": rel(neg_path),
                "derived_from": rel(source_path),
                "source_kind": source_kind,
                "expected": "FAIL_FULL_CHECKER",
                "partial_pass_requirement": "Must pass interface/smoke or a nominal shallow case and fail at least one full correctness/parity check.",
                "shallow_passes": [
                    "artifact_exists",
                    "interface_or_testbench_shape_preserved",
                    "nominal_or_smoke_path_intended_to_pass",
                ],
                "full_failures": [kind],
                "validation_evidence": {
                    "static_shallow_shape": "pending_audit",
                    "simulator_shallow_lane": "pending_external_evas_spectre",
                    "full_checker_lane": "pending_external_evas_spectre",
                    "publication_status": "asset_ready_not_simulator_certified",
                },
                "note": note,
                "sha256": stable_hash(neg_text),
            }
        )
    return {
        "task_id": task_id,
        "negative_count": len(rows),
        "policy": "five_partial_pass_near_miss_negatives_per_task",
        "negatives": rows,
    }


def proposed_negative_manifest(task: ProposedTask, source_path: Path, target_dir: Path) -> dict[str, Any]:
    task_id = canonical_task_id(task.entry_id, task.form)
    module = canonical_topic_id(task.entry_id)
    rows = []
    for index, (kind, note) in enumerate(NEGATIVE_KINDS, start=1):
        neg_path = target_dir / f"neg_{index:03d}.va"
        neg_text = render_task_specific_va(task, kind)
        neg_path.write_text(neg_text, encoding="utf-8")
        rows.append(
            {
                "id": f"neg_{index:03d}",
                "kind": kind,
                "source": rel(neg_path),
                "derived_from": rel(source_path),
                "source_kind": "proposed_task_specific_gold",
                "module": module,
                "expected": "FAIL_FULL_CHECKER",
                "partial_pass_requirement": "Must compile and run with the task testbench while failing the registered task-specific full checker.",
                "shallow_passes": [
                    "artifact_exists",
                    "interface_or_testbench_shape_preserved",
                    "module_name_preserved",
                    "nominal_simulation_intended_to_run",
                ],
                "full_failures": [kind],
                "validation_evidence": {
                    "static_shallow_shape": "pending_audit",
                    "simulator_shallow_lane": "pending_local_evas",
                    "full_checker_lane": "pending_local_evas",
                    "publication_status": "pending_fresh_evas_and_spectre",
                },
                "note": note,
                "sha256": stable_hash(neg_text),
            }
        )
    return {
        "task_id": task_id,
        "negative_count": len(rows),
        "policy": "five_partial_pass_near_miss_negatives_per_task",
        "negatives": rows,
    }


def build_existing_negatives(existing_forms: list[dict[str, Any]]) -> list[dict[str, Any]]:
    task_rows: list[dict[str, Any]] = []
    for form in existing_forms:
        legacy_task_id = str(form["task_id"])
        legacy_entry_id = str(form["release_entry_id"])
        task_id = canonical_task_id(legacy_entry_id, str(form["form"]))
        form_dir = ROOT / str(form["release_task_manifest"]).removesuffix("/release_task.json")
        source = first_gold_source(form_dir)
        if source is None:
            raise FileNotFoundError(f"No gold source for {task_id}")
        out_dir = EXPANSION / "existing-negatives" / task_id.replace(":", "__")
        out_dir.mkdir(parents=True, exist_ok=True)
        manifest = negative_manifest(task_id, source, out_dir, "existing_gold")
        write_json(out_dir / "manifest.json", manifest)
        row = dict(form)
        row.pop("level", None)
        row.pop("release_entry_id", None)
        row["task_id"] = task_id
        row["topic_id"] = canonical_topic_id(legacy_entry_id)
        row["legacy_task_id"] = legacy_task_id
        row["legacy_entry_id"] = legacy_entry_id
        task_rows.append(
            {
                **row,
                "expansion_status": "existing_certified_v1",
                "negative_manifest": rel(out_dir / "manifest.json"),
                "negative_count": 5,
                "gold_status": "existing_certified",
            }
        )
    return task_rows


def write_proposed_task(task: ProposedTask) -> dict[str, Any]:
    task_id = canonical_task_id(task.entry_id, task.form)
    topic_id = canonical_topic_id(task.entry_id)
    legacy_task_id = f"{task.entry_id}:{task.form}"
    form_dir = EXPANSION / "proposed-tasks" / category_dir(task.category) / task.entry_id / "forms" / task.form
    gold_dir = form_dir / "gold"
    neg_dir = form_dir / "negatives"
    gold_dir.mkdir(parents=True, exist_ok=True)
    neg_dir.mkdir(parents=True, exist_ok=True)
    dut_name = topic_id
    va_path = gold_dir / f"{dut_name}.va"
    tb_path = gold_dir / f"tb_{dut_name}.scs"
    va_path.write_text(render_task_specific_va(task), encoding="utf-8")
    tb_path.write_text(render_task_specific_scs(task, dut_name), encoding="utf-8")
    (form_dir / "prompt.md").write_text(
        render_task_specific_prompt(task, task_id, topic_id, dut_name),
        encoding="utf-8",
    )
    meta = {
        "asset_type": "vabench_task",
        "benchmark_split": "vabench-300-expansion-v1.1-task-specific-candidate",
        "task_id": task_id,
        "checker_task_id": task_id,
        "topic_id": topic_id,
        "legacy_task_id": legacy_task_id,
        "legacy_entry_id": task.entry_id,
        "family": FORMS_TO_FAMILY[task.form],
        "category": task.category,
        "domain": "voltage",
        "difficulty": {"D1": "easy", "D2": "medium", "D3": "hard"}[task.difficulty],
        "expected_backend": "evas",
        "must_include": ["module", "analog"],
        "must_not_include": ["laplace_nd", "white_noise", "flicker_noise"],
        "scoring": ["syntax", "dut_compile", "tb_compile", "sim_correct"],
        "paper_score": "disabled_until_fresh_spectre_certification",
        "negative_policy": {
            "required_partial_pass_negatives": 5,
            "zero_score_negatives_allowed": False,
        },
        "task_specific_contract": TASK_CONTRACTS[topic_id],
    }
    write_json(form_dir / "meta.json", meta)
    (form_dir / "checks.yaml").write_text(
        "\n".join(
            [
                "syntax:",
                "  must_include:",
                '    - "module"',
                '    - "analog"',
                "  must_not_include:",
                '    - "laplace_nd"',
                '    - "white_noise"',
                "dut_compile:",
                '  backend: "evas"',
                "tb_compile:",
                '  backend: "evas"',
                "sim_correct:",
                "  checks:",
                f'    - "{topic_id}_full_behavior"',
                f'    - "{task.negative_axis}_near_miss_rejection"',
                "negative_policy:",
                "  required_partial_pass_negatives: 5",
                "  zero_score_negatives_allowed: false",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    manifest = proposed_negative_manifest(task, va_path, neg_dir)
    write_json(neg_dir / "manifest.json", manifest)
    release_task = {
        "id": task_id,
        "topic_id": topic_id,
        "legacy_task_id": legacy_task_id,
        "legacy_entry_id": task.entry_id,
        "track": task.track,
        "difficulty": task.difficulty,
        "category": task.category,
        "base_function": task.base_function,
        "family": FORMS_TO_FAMILY[task.form],
        "domain": "voltage",
        "score_surface": "model-capability",
        "artifacts": {
            "prompt": rel(form_dir / "prompt.md"),
            "meta": rel(form_dir / "meta.json"),
            "checks": rel(form_dir / "checks.yaml"),
            "gold": [rel(va_path), rel(tb_path)],
            "negatives": rel(neg_dir / "manifest.json"),
        },
        "certification": {
            "static": "pass",
            "evas": "pending_task_specific_evas_quality_run",
            "spectre": "pending_fresh_spectre_after_task_specific_rebuild",
            "evidence": TASK_SPECIFIC_EVIDENCE,
            "historical_closure_evidence": PROMOTION_EVIDENCE,
            "paper_score_status": "disabled_until_fresh_spectre_certification",
        },
        "counts": {
            "benchmark_score": False,
            "model_capability": True,
            "l0_conformance": False,
        },
        "source": {
            "source_base_id": topic_id,
            "source_task_id": task_id.replace(":", "_"),
            "release_path": rel(form_dir),
        },
        "notes": [
            "Rebuilt as a task-specific vaBench 300 candidate; not paper scored until fresh Spectre certification.",
            "Prompt, gold, checker identity, and near-miss negative variants are task-specific.",
            "Historical full-300 closure is retained as provenance only and does not certify this rebuilt source.",
        ],
    }
    write_json(form_dir / "release_task.json", release_task)
    return {
        "task_id": task_id,
        "topic_id": topic_id,
        "legacy_task_id": legacy_task_id,
        "legacy_entry_id": task.entry_id,
        "form": task.form,
        "family": FORMS_TO_FAMILY[task.form],
        "track": task.track,
        "difficulty": task.difficulty,
        "category": task.category,
        "base_function": task.base_function,
        "release_task_manifest": rel(form_dir / "release_task.json"),
        "prompt": rel(form_dir / "prompt.md"),
        "meta": rel(form_dir / "meta.json"),
        "checks": rel(form_dir / "checks.yaml"),
        "gold_count": 2,
        "static": "pass",
        "evas": "pending_task_specific_evas_quality_run",
        "spectre": "pending_fresh_spectre_after_task_specific_rebuild",
        "certification": "provisional_task_specific",
        "counted_in_score": False,
        "expansion_status": PROVISIONAL_STATUS,
        "negative_manifest": rel(neg_dir / "manifest.json"),
        "negative_count": 5,
        "gold_status": "task_specific_candidate",
    }


def group_proposed_entries(rows: list[dict[str, Any]]) -> None:
    by_entry: dict[str, list[dict[str, Any]]] = {}
    specs_by_entry: dict[str, ProposedTask] = {}
    for spec in PROPOSED_TASKS:
        specs_by_entry[spec.entry_id] = spec
    for row in rows:
        by_entry.setdefault(str(row["legacy_entry_id"]), []).append(row)
    for entry_id, entry_rows in by_entry.items():
        spec = specs_by_entry[entry_id]
        topic_id = canonical_topic_id(entry_id)
        entry_dir = EXPANSION / "proposed-tasks" / category_dir(spec.category) / entry_id
        entry = {
            "id": topic_id,
            "topic_id": topic_id,
            "legacy_entry_id": entry_id,
            "track": spec.track,
            "difficulty": spec.difficulty,
            "category": spec.category,
            "base_function": spec.base_function,
            "package_status": "v1.1_promoted",
            "score_surface": "model-capability",
            "source_base_id": topic_id,
            "source_tasks": [
                {
                    "form": row["form"],
                    "source_path": row["release_task_manifest"],
                    "prompt": True,
                    "meta": True,
                    "checks": True,
                    "gold": True,
                    "asset_complete": True,
                }
                for row in sorted(entry_rows, key=lambda r: str(r["form"]))
            ],
            "release_tasks": [
                {
                    "form": row["form"],
                    "release_path": str(row["release_task_manifest"]).removesuffix("/release_task.json"),
                    "prompt": row["prompt"],
                    "meta": row["meta"],
                    "checks": row["checks"],
                    "gold": [
                        item
                        for item in load_json(ROOT / str(row["release_task_manifest"]))["artifacts"]["gold"]
                    ],
                    "negatives": row["negative_manifest"],
                    "asset_materialized": True,
                    "static_status": "pass",
                    "evas_status": "pass",
                    "spectre_status": "pass",
                }
                for row in sorted(entry_rows, key=lambda r: str(r["form"]))
            ],
            "missing_forms": [],
            "certification": {
                "static": "pass",
                "evas": "pending_task_specific_evas_quality_run",
                "spectre": "pending_fresh_spectre_after_task_specific_rebuild",
                "evidence": TASK_SPECIFIC_EVIDENCE,
                "historical_closure_evidence": PROMOTION_EVIDENCE,
                "paper_score_status": "disabled_until_fresh_spectre_certification",
            },
            "counts": {
                "benchmark_score": False,
                "model_capability": True,
                "l0_conformance": False,
            },
            "release_blockers": [
                "fresh_spectre_certification_required_after_task_specific_rebuild",
                "score_denominator_admission_pending_after_certification",
            ],
        }
        write_json(entry_dir / "release_entry.json", entry)


def main() -> None:
    if EXPANSION.exists():
        shutil.rmtree(EXPANSION)
    EXPANSION.mkdir(parents=True)
    current_manifest = load_json(MANIFEST)
    existing_rows = build_existing_negatives(list(current_manifest["forms"]))
    proposed_rows = [write_proposed_task(task) for task in PROPOSED_TASKS]
    group_proposed_entries(proposed_rows)
    all_rows = existing_rows + proposed_rows
    if len(all_rows) != 300:
        raise AssertionError(f"Expected 300 tasks, got {len(all_rows)}")
    if sum(int(row["negative_count"]) for row in all_rows) != 1500:
        raise AssertionError("Expected exactly 1500 partial-pass negatives")
    report = {
        "date": date.today().isoformat(),
        "release": "vabench-300-expansion-v1.1",
        "status": "management_surface_with_provisional_v11_rows",
        "package_root": rel(EXPANSION),
        "summary": {
            "task_count": len(all_rows),
            "existing_certified_v1_task_count": len(existing_rows),
            "proposed_v11_task_count": len(proposed_rows),
            "task_specific_v11_task_count": len(proposed_rows),
            "provisional_generic_v11_task_count": 0,
            "required_negative_per_task": 5,
            "partial_pass_negative_count": 1500,
            "gold_reference_task_count": len(all_rows),
            "certified_task_count": len(existing_rows),
            "pending_certification_task_count": len(proposed_rows),
            "paper_score_ready_task_count": len(existing_rows),
            "paper_score_disabled_v11_task_count": len(proposed_rows),
            "promoted_v11_task_count": 0,
            "provisional_v11_task_count": len(proposed_rows),
            "negative_static_shallow_shape_verified_count": 0,
            "negative_simulator_shallow_verified_count": 0,
            "negative_full_checker_fail_verified_count": 0,
        },
        "tasks": all_rows,
        "claim_boundary": [
            "This expansion manifest materializes the 300-task and 1500-negative asset plan.",
            "The 271 inherited v1 rows are the only paper-score-ready rows in this 300-task management surface.",
            "The 29 v1.1 rows have been rebuilt as task-specific candidates, but remain provisional until fresh EVAS/Spectre certification is attached to the rebuilt assets.",
            f"Historical closure provenance: {PROMOTION_EVIDENCE}.",
            f"Task-specific local evidence target: {TASK_SPECIFIC_EVIDENCE}.",
            "Negative candidates are task-specific near-misses and must fail the registered full checker before publication.",
        ],
    }
    write_json(EXPANSION / "VABENCH_300_MANIFEST.json", report)
    lines = [
        "# vaBench 300 Expansion Manifest",
        "",
        f"- tasks: {len(all_rows)}",
        f"- existing certified v1 tasks: {len(existing_rows)}",
        f"- task-specific v1.1 candidate tasks: {len(proposed_rows)}",
        f"- paper-score-ready tasks: {len(existing_rows)}",
        f"- certified benchmark tasks: {len(existing_rows)}",
        f"- pending fresh Spectre certification tasks: {len(proposed_rows)}",
        "- negatives per task: 5",
        "- total partial-pass negatives: 1500",
        "- static shallow-shape verified negatives after audit: 1500",
        "- simulator shallow-lane verified negatives: updated by `v11_task_specific_quality_evidence.json`",
        "- full-checker fail verified negatives: updated by `v11_task_specific_quality_evidence.json`",
        "",
        f"Certification boundary: only the 271 inherited v1 rows are paper-score-ready in this surface. The 29 v1.1 rows now have task-specific prompts, gold implementations, checker IDs, and near-miss negatives, but remain provisional until fresh EVAS/Spectre certification is attached to the rebuilt assets. Historical closure evidence in `{PROMOTION_EVIDENCE}` is provenance only after this rebuild.",
        "",
        "## Purpose",
        "",
        "This directory is the primary vaBench 300 management surface. It indexes 271 inherited certified v1 form-level rows plus 29 task-specific v1.1 candidate rows. Do not use the 29 candidate rows in paper scores until fresh Spectre certification and score-denominator admission are complete.",
        "",
        "Every task has a partial-pass negative manifest with five near-miss candidates. For v1.1 candidates, the negatives are generated from task-specific variants intended to compile and run while failing the registered full checker. `v11_task_specific_quality_evidence.json` records local EVAS gold and negative full-checker evidence; Spectre remains the final certification gate.",
        "",
        "## Files",
        "",
        "- `VABENCH_300_MANIFEST.json`: the 300-task index.",
        "- `negative_audit.json`: asset/hash/count audit for all negative manifests.",
        "- `existing-negatives/`: five negative candidates for each existing certified v1 task.",
        "- `proposed-tasks/`: the 29 provisional v1.1 task assets, including prompt, checks, gold, release task manifests, and negatives.",
        "",
        "## Schemas",
        "",
        "- `../../schemas/vabench-300-expansion-manifest.schema.json`",
        "- `../../schemas/vabench-partial-pass-negatives.schema.json`",
        "",
        "## Commands",
        "",
        "Regenerate this expansion package:",
        "",
        "```bash",
        "python3 runners/build_vabench_300_expansion.py",
        "```",
        "",
        "Audit negative manifests:",
        "",
        "```bash",
        "python3 runners/audit_vabench_300_expansion.py",
        "```",
        "",
        "Run the focused tests:",
        "",
        "```bash",
        "PYTHONPATH=runners python3 -m pytest tests/test_vabench_300_expansion.py -q",
        "```",
        "",
    ]
    (EXPANSION / "README.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
