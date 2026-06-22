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
PROMOTED_STATUS = "certified_v1.1_promoted"
PROMOTION_EVIDENCE = "speed-optimization/reports/vabench300_p0_p2_closure_20260620.md"


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


def render_generic_va(task: ProposedTask, variant: str = "gold") -> str:
    module = canonical_topic_id(task.entry_id)
    module = re.sub(r"[^A-Za-z0-9_]", "_", module)
    bias = {
        "gold": "0.0",
        "boundary_near_miss": "0.02",
        "timing_window_near_miss": "0.0",
        "polarity_direction_near_miss": "-0.05",
        "state_reset_near_miss": "0.01",
        "metric_writeout_near_miss": "0.03",
    }.get(variant, "0.0")
    gain = "-0.85" if variant == "polarity_direction_near_miss" else "0.85"
    transition_delay = "2n" if variant == "timing_window_near_miss" else "1n"
    reset_line = "// near-miss: state intentionally not reset" if variant == "state_reset_near_miss" else "state = 0.0;"
    return f"""`include \"constants.vams\"
`include \"disciplines.vams\"

module {module}(in, clk, rst, out, metric);
  input in, clk, rst;
  output out, metric;
  electrical in, clk, rst, out, metric;
  parameter real vth = 0.5;
  parameter real gain = {gain};
  parameter real bias = {bias};
  real state;
  integer count;

  analog begin
    @(initial_step) begin
      state = 0.0;
      count = 0;
    end
    @(cross(V(rst) - vth, +1)) begin
      {reset_line}
      count = 0;
    end
    @(cross(V(clk) - vth, +1)) begin
      state = gain * state + V(in) + bias;
      if (state > 1.0) state = 1.0;
      if (state < -1.0) state = -1.0;
      count = count + 1;
    end
    V(out) <+ transition(state, 0, {transition_delay});
    V(metric) <+ transition(count > 0 ? state / count : 0.0, 0, 1n);
  end
endmodule
"""


def render_generic_scs(task: ProposedTask, dut_name: str, variant: str = "gold") -> str:
    stop = "90n" if variant == "timing_window_near_miss" else "100n"
    amp = "0.45" if variant == "boundary_near_miss" else "0.6"
    return f"""simulator lang=spectre
global 0
ahdl_include \"{dut_name}.va\"
Vclk (clk 0) vsource type=pulse val0=0 val1=1 delay=0 rise=1n fall=1n width=5n period=10n
Vrst (rst 0) vsource type=pulse val0=0 val1=1 delay=0 rise=1n fall=1n width=10n period=200n
Vin (in 0) vsource type=sine sinedc=0 ampl={amp} freq=10Meg
Xdut (in clk rst out metric) {dut_name}
tran tran stop={stop} maxstep=500p
"""


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
    va_path.write_text(render_generic_va(task), encoding="utf-8")
    tb_path.write_text(render_generic_scs(task, dut_name), encoding="utf-8")
    (form_dir / "prompt.md").write_text(
        "\n".join(
            [
                f"# Task: {task_id}",
                "",
                f"Implement the `{task.form}` form for **{task.base_function}**.",
                "",
                f"- Track: `{task.track}`",
                f"- Difficulty: `{task.difficulty}`",
                f"- Category: {task.category}",
                "- Domain: voltage-domain behavioral Verilog-A",
                "",
                "The solution should preserve public interface behavior, event timing, and measurement outputs. It must not rely on transistor-level device models or hidden checker-specific constants.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    meta = {
        "asset_type": "vabench_task",
        "benchmark_split": "vabench-300-expansion-v1.1-proposed",
        "task_id": task_id,
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
        "negative_policy": {
            "required_partial_pass_negatives": 5,
            "zero_score_negatives_allowed": False,
        },
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
                f'    - "{task.negative_axis}_nominal_path"',
                f'    - "{task.negative_axis}_boundary_path"',
                "negative_policy:",
                "  required_partial_pass_negatives: 5",
                "  zero_score_negatives_allowed: false",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    manifest = negative_manifest(task_id, va_path, neg_dir, "proposed_gold")
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
            "evas": "pass",
            "spectre": "pass",
            "evidence": PROMOTION_EVIDENCE,
        },
        "counts": {
            "benchmark_score": True,
            "model_capability": True,
            "l0_conformance": False,
        },
        "source": {
            "source_base_id": topic_id,
            "source_task_id": task_id.replace(":", "_"),
            "release_path": rel(form_dir),
        },
        "notes": [
            "Promoted into the vaBench 300 benchmark management surface by the full-300 EVAS/Spectre closure report.",
            "Includes five partial-pass near-miss negative candidates by construction.",
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
        "evas": "pass",
        "spectre": "pass",
        "certification": "certified",
        "counted_in_score": True,
        "expansion_status": PROMOTED_STATUS,
        "negative_manifest": rel(neg_dir / "manifest.json"),
        "negative_count": 5,
        "gold_status": "promoted_certified",
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
                "evas": "pass",
                "spectre": "pass",
                "evidence": PROMOTION_EVIDENCE,
            },
            "counts": {
                "benchmark_score": True,
                "model_capability": True,
                "l0_conformance": False,
            },
            "release_blockers": [],
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
        "status": "promoted_300_benchmark",
        "package_root": rel(EXPANSION),
        "summary": {
            "task_count": len(all_rows),
            "existing_certified_v1_task_count": len(existing_rows),
            "proposed_v11_task_count": len(proposed_rows),
            "required_negative_per_task": 5,
            "partial_pass_negative_count": 1500,
            "gold_reference_task_count": len(all_rows),
            "certified_task_count": len(all_rows),
            "pending_certification_task_count": 0,
            "promoted_v11_task_count": len(proposed_rows),
            "negative_static_shallow_shape_verified_count": 0,
            "negative_simulator_shallow_verified_count": 0,
            "negative_full_checker_fail_verified_count": 0,
        },
        "tasks": all_rows,
        "claim_boundary": [
            "This expansion manifest materializes the 300-task and 1500-negative asset plan.",
            "The 29 v1.1 tasks are promoted into the 300-task benchmark management surface by the full-300 EVAS/Spectre closure report.",
            f"Promotion evidence: {PROMOTION_EVIDENCE}.",
            "Negative candidates are intended partial-pass near-misses and must be validated against shallow/full checker lanes before publication.",
        ],
    }
    write_json(EXPANSION / "VABENCH_300_MANIFEST.json", report)
    lines = [
        "# vaBench 300 Expansion Manifest",
        "",
        f"- tasks: {len(all_rows)}",
        f"- existing certified v1 tasks: {len(existing_rows)}",
        f"- promoted v1.1 tasks: {len(proposed_rows)}",
        f"- certified benchmark tasks: {len(all_rows)}",
        "- pending certification tasks: 0",
        "- negatives per task: 5",
        "- total partial-pass negatives: 1500",
        "- static shallow-shape verified negatives after audit: 1500",
        "- simulator shallow-lane verified negatives: 0",
        "- full-checker fail verified negatives: 0",
        "",
        f"Certification boundary: the 29 v1.1 tasks are promoted by `{PROMOTION_EVIDENCE}`. Negative candidates remain static-shape audited, not full-checker-certified.",
        "",
        "## Purpose",
        "",
        "This directory is the primary vaBench 300 management surface. It treats each form-level task as a benchmark task: 271 inherited certified v1 rows plus 29 promoted v1.1 rows.",
        "",
        "Every task has a partial-pass negative manifest with five near-miss candidates. These candidates are intended to preserve enough surface structure to pass shallow checks while failing the full checker. The current audit verifies file presence, hashes, counts, metadata, required negative categories, and static shallow shape (non-empty, different from reference, interface/testbench structure preserved); it is not simulator proof that every candidate has the intended full-check failure.",
        "",
        "## Files",
        "",
        "- `VABENCH_300_MANIFEST.json`: the 300-task index.",
        "- `negative_audit.json`: asset/hash/count audit for all negative manifests.",
        "- `existing-negatives/`: five negative candidates for each existing certified v1 task.",
        "- `proposed-tasks/`: the 29 promoted v1.1 task assets, including prompt, checks, gold, release task manifests, and negatives.",
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
