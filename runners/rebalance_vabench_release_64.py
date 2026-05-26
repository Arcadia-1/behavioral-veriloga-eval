#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import shutil
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
TASKS_ROOT = PACKAGE_ROOT / "tasks"
EVIDENCE_ROOT = PACKAGE_ROOT / "evidence"
TRACKER_CSV = ROOT / "docs" / "VABENCH_RELEASE_TRACKER.csv"
TRACKER_MD = ROOT / "docs" / "VABENCH_RELEASE_TRACKER.md"
SEED_CSV = ROOT / "docs" / "VABENCH_RELEASE_SEED_MANIFEST.csv"
SEED_MD = ROOT / "docs" / "VABENCH_RELEASE_SEED_MANIFEST.md"
SELECTED_CSV = ROOT / "docs" / "VABENCH_RELEASE_SELECTED_MANIFEST.csv"
SELECTED_MD = ROOT / "docs" / "VABENCH_RELEASE_SELECTED_MANIFEST.md"

DELETE_ENTRY_IDS = {
    "vbr1_l1_adc_code_capture_register",
    "vbr1_l1_serializer_frame_aligner",
    "vbr1_l1_serial_readout_deserializer",
    "vbr1_l2_serializer_frame_alignment_flow",
    "vbr1_l2_event_controller",
    "vbr1_l1_pfd_small_phase_error_response",
    "vbr1_l1_xor_phase_detector",
    "vbr1_l2_pll_timing_slice",
    "vbr1_l1_rotating_dem_selector",
    "vbr1_l1_windowed_dem_pointer",
}

CATEGORY_DIRS = {
    "Sampling and Analog Memory": "CT03_sampling_and_analog_memory",
    "Baseband Signal Conditioning": "CT04_baseband_signal_conditioning",
}

FORM_TO_FAMILY = {
    "dut": "spec-to-va",
    "tb": "tb-generation",
    "bugfix": "bugfix",
    "e2e": "end-to-end",
}


@dataclass(frozen=True)
class NewEntrySpec:
    entry_id: str
    category: str
    base_function: str
    source_base_id: str
    canonical_kernel: str
    module_name: str
    dut_file: str
    tb_file: str
    ports: list[str]
    public_nodes: list[str]
    checks: list[str]
    description_title: str
    description: str
    dut_gold: str
    buggy_gold: str
    tb_gold: str
    tb_buggy_gold: str
    complete_circuit_form: str


ACQ_DESCRIPTION = """Write a pure voltage-domain Verilog-A model for an acquisition-limited sample-and-hold.

The model must represent finite acquisition bandwidth rather than an ideal instantaneous sampler:
- `sample` high opens a tracking/acquisition window.
- While tracking, `vout` moves toward the current `V(vin)` in discrete 1 ns acquisition updates.
- A falling `sample` edge freezes the last acquired value.
- High `rst` returns the held output to `vinit`.
- `metric` is high only while the model is actively tracking/acquiring.
"""

ACQ_DUT = """`include "constants.vams"
`include "disciplines.vams"

module acquisition_limited_sample_hold(sample, rst, vin, vout, metric);
    input sample, rst, vin;
    output vout, metric;
    electrical sample, rst, vin, vout, metric;

    parameter real vth = 0.45;
    parameter real vinit = 0.45;
    parameter real alpha = 0.42 from (0:1];
    parameter real tick = 1n from (0:inf);
    parameter real tr = 200p from (0:inf);

    real held;
    real tracking;

    analog begin
        @(initial_step) begin
            held = vinit;
            tracking = 0.0;
        end

        @(cross(V(sample) - vth, +1)) begin
            if (V(rst) > vth) begin
                held = vinit;
                tracking = 0.0;
            end else begin
                tracking = 1.0;
            end
        end

        @(cross(V(sample) - vth, -1)) begin
            tracking = 0.0;
        end

        @(timer(0, tick)) begin
            if (V(rst) > vth) begin
                held = vinit;
                tracking = 0.0;
            end else if (tracking > 0.5) begin
                held = held + alpha * (V(vin) - held);
            end
        end

        V(vout) <+ transition(held, 0, tr, tr);
        V(metric) <+ transition((tracking > 0.5) ? 0.9 : 0.0, 0, tr, tr);
    end
endmodule
"""

ACQ_BUGGY = """`include "constants.vams"
`include "disciplines.vams"

module acquisition_limited_sample_hold(sample, rst, vin, vout, metric);
    input sample, rst, vin;
    output vout, metric;
    electrical sample, rst, vin, vout, metric;

    parameter real vth = 0.45;
    parameter real vinit = 0.45;
    parameter real tick = 1n from (0:inf);
    parameter real tr = 200p from (0:inf);

    real held;
    real tracking;

    analog begin
        @(initial_step) begin
            held = vinit;
            tracking = 0.0;
        end

        @(cross(V(sample) - vth, +1)) begin
            if (V(rst) > vth)
                held = vinit;
            else
                held = V(vin);
            tracking = 1.0;
        end

        @(cross(V(sample) - vth, -1)) begin
            tracking = 0.0;
        end

        @(timer(0, tick)) begin
            if (V(rst) > vth)
                held = vinit;
        end

        V(vout) <+ transition(held, 0, tr, tr);
        V(metric) <+ transition((tracking > 0.5) ? 0.9 : 0.0, 0, tr, tr);
    end
endmodule
"""

ACQ_TB = """simulator lang=spectre
global 0

ahdl_include "acquisition_limited_sample_hold.va"

Vsample (sample 0) vsource type=pulse val0=0 val1=0.9 period=20n width=5n delay=5n rise=100p fall=100p
Vrst (rst 0) vsource type=pwl wave=[0 0.9 2n 0.9 2.1n 0 90n 0]
Vvin (vin 0) vsource type=pwl wave=[0 0.25 7n 0.25 14n 0.80 28n 0.80 34n 0.20 49n 0.20 54n 0.70 70n 0.70 75n 0.35 90n 0.35]

XDUT (sample rst vin vout metric) acquisition_limited_sample_hold

tran tran stop=90n maxstep=250p
save sample rst vin vout metric
"""

ACQ_TB_BUGGY = ACQ_TB.replace('ahdl_include "acquisition_limited_sample_hold.va"', 'ahdl_include "dut_buggy.va"')

PGA_DESCRIPTION = """Write a pure voltage-domain Verilog-A programmable gain amplifier.

The gain code is sampled on rising `clk` edges:
- reset selects unity gain and returns the output to the common-mode voltage.
- `gain_sel=0` selects a low gain.
- `gain_sel=1` selects a high gain.
- The output is `vcm + gain * (V(vin)-vcm)` with rail clamps.
- `metric` is high when the unclamped target clips to either rail.
"""

PGA_DUT = """`include "constants.vams"
`include "disciplines.vams"

module programmable_gain_amplifier(clk, rst, gain_sel, vin, out, metric);
    input clk, rst, gain_sel, vin;
    output out, metric;
    electrical clk, rst, gain_sel, vin, out, metric;

    parameter real vth = 0.45;
    parameter real vcm = 0.45;
    parameter real gain_low = 0.8;
    parameter real gain_high = 2.4;
    parameter real vmin = 0.0;
    parameter real vmax = 0.9;
    parameter real tr = 200p from (0:inf);

    real gain_value;
    real raw;
    real bounded;
    real clipped;

    analog begin
        @(initial_step) begin
            gain_value = 1.0;
        end

        @(cross(V(clk) - vth, +1)) begin
            if (V(rst) > vth)
                gain_value = 1.0;
            else if (V(gain_sel) > vth)
                gain_value = gain_high;
            else
                gain_value = gain_low;
        end

        raw = vcm + gain_value * (V(vin) - vcm);
        bounded = raw;
        clipped = 0.0;
        if (bounded > vmax) begin
            bounded = vmax;
            clipped = 1.0;
        end
        if (bounded < vmin) begin
            bounded = vmin;
            clipped = 1.0;
        end
        if (V(rst) > vth) begin
            bounded = vcm;
            clipped = 0.0;
        end

        V(out) <+ transition(bounded, 0, tr, tr);
        V(metric) <+ transition((clipped > 0.5) ? 0.9 : 0.0, 0, tr, tr);
    end
endmodule
"""

PGA_BUGGY = """`include "constants.vams"
`include "disciplines.vams"

module programmable_gain_amplifier(clk, rst, gain_sel, vin, out, metric);
    input clk, rst, gain_sel, vin;
    output out, metric;
    electrical clk, rst, gain_sel, vin, out, metric;

    parameter real vth = 0.45;
    parameter real vcm = 0.45;
    parameter real vmin = 0.0;
    parameter real vmax = 0.9;
    parameter real tr = 200p from (0:inf);

    real gain_value;
    real raw;
    real bounded;
    real clipped;

    analog begin
        @(initial_step) begin
            gain_value = 1.0;
        end

        @(cross(V(clk) - vth, +1)) begin
            gain_value = 1.0;
        end

        raw = vcm + gain_value * (V(vin) - vcm);
        bounded = raw;
        clipped = 0.0;
        if (bounded > vmax) begin
            bounded = vmax;
            clipped = 1.0;
        end
        if (bounded < vmin) begin
            bounded = vmin;
            clipped = 1.0;
        end
        if (V(rst) > vth) begin
            bounded = vcm;
            clipped = 0.0;
        end

        V(out) <+ transition(bounded, 0, tr, tr);
        V(metric) <+ transition((clipped > 0.5) ? 0.9 : 0.0, 0, tr, tr);
    end
endmodule
"""

PGA_TB = """simulator lang=spectre
global 0

ahdl_include "programmable_gain_amplifier.va"

Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 period=8n width=4n delay=2n rise=80p fall=80p
Vrst (rst 0) vsource type=pwl wave=[0 0.9 2n 0.9 2.1n 0 90n 0]
Vgain (gain_sel 0) vsource type=pwl wave=[0 0 18n 0 20n 0.9 48n 0.9 50n 0 70n 0 72n 0.9 90n 0.9]
Vvin (vin 0) vsource type=pwl wave=[0 0.45 8n 0.60 16n 0.30 28n 0.72 40n 0.20 58n 0.55 70n 0.85 82n 0.10 90n 0.45]

XDUT (clk rst gain_sel vin out metric) programmable_gain_amplifier

tran tran stop=90n maxstep=250p
save clk rst gain_sel vin out metric
"""

PGA_TB_BUGGY = PGA_TB.replace('ahdl_include "programmable_gain_amplifier.va"', 'ahdl_include "dut_buggy.va"')

NEW_ENTRIES = [
    NewEntrySpec(
        entry_id="vbr1_l1_acquisition_limited_sample_and_hold",
        category="Sampling and Analog Memory",
        base_function="Acquisition-limited sample-and-hold",
        source_base_id="acquisition_limited_sample_hold",
        canonical_kernel="finite_bandwidth_track_hold",
        module_name="acquisition_limited_sample_hold",
        dut_file="acquisition_limited_sample_hold.va",
        tb_file="tb_acquisition_limited_sample_hold.scs",
        ports=["sample", "rst", "vin", "vout", "metric"],
        public_nodes=["sample", "rst", "vin", "vout", "metric"],
        checks=[
            "finite_acquisition_does_not_jump_to_vin",
            "longer_sample_window_settles_closer_to_vin",
            "falling_sample_edge_holds_last_acquired_value",
            "reset_returns_to_initial_level",
            "metric_marks_tracking_window",
        ],
        description_title="Acquisition-limited sample-and-hold",
        description=ACQ_DESCRIPTION,
        dut_gold=ACQ_DUT,
        buggy_gold=ACQ_BUGGY,
        tb_gold=ACQ_TB,
        tb_buggy_gold=ACQ_TB_BUGGY,
        complete_circuit_form="Finite-bandwidth track/hold front end with explicit acquisition settling and hold behavior",
    ),
    NewEntrySpec(
        entry_id="vbr1_l1_programmable_gain_amplifier",
        category="Baseband Signal Conditioning",
        base_function="Programmable gain amplifier",
        source_base_id="programmable_gain_amplifier",
        canonical_kernel="sampled_gain_code_with_clamps",
        module_name="programmable_gain_amplifier",
        dut_file="programmable_gain_amplifier.va",
        tb_file="tb_programmable_gain_amplifier.scs",
        ports=["clk", "rst", "gain_sel", "vin", "out", "metric"],
        public_nodes=["clk", "rst", "gain_sel", "vin", "out", "metric"],
        checks=[
            "gain_select_changes_slope",
            "sampled_gain_holds_between_clock_edges",
            "common_mode_is_preserved",
            "rail_clamps_with_clip_metric",
            "reset_returns_to_unity_gain",
        ],
        description_title="Programmable gain amplifier",
        description=PGA_DESCRIPTION,
        dut_gold=PGA_DUT,
        buggy_gold=PGA_BUGGY,
        tb_gold=PGA_TB,
        tb_buggy_gold=PGA_TB_BUGGY,
        complete_circuit_form="Sampled gain-code amplifier with low/high gain modes, common-mode offset, rail clamps, and clip metric",
    ),
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def remove_entry(entry_id: str) -> None:
    for manifest_path in sorted(TASKS_ROOT.glob(f"CT*/{entry_id}/release_entry.json")):
        entry_dir = manifest_path.parent
        if entry_dir.name != entry_id or entry_dir.parent.parent != TASKS_ROOT:
            raise RuntimeError(f"unsafe release entry deletion target: {entry_dir}")
        shutil.rmtree(entry_dir)
    for evidence_family in ("static", "dual"):
        evidence_dir = EVIDENCE_ROOT / evidence_family / entry_id
        if evidence_dir.exists():
            shutil.rmtree(evidence_dir)


def prompt_text(spec: NewEntrySpec, form: str) -> str:
    target_artifacts = {
        "dut": [spec.dut_file],
        "tb": [spec.tb_file],
        "bugfix": ["dut_fixed.va"],
        "e2e": [spec.dut_file, spec.tb_file],
    }[form]
    supplied = {
        "dut": [],
        "tb": [spec.dut_file],
        "bugfix": ["dut_buggy.va"],
        "e2e": [],
    }[form]
    lines = [
        f"# Task: {spec.entry_id}:{form}",
        "",
        "## Release Task Contract",
        "",
        f"- Form: `{form}`",
        "- Level: `L1`",
        f"- Category: {spec.category}",
        f"- Base function: {spec.base_function}",
        "- Domain: `voltage`",
        f"- Target artifact(s): {', '.join(f'`{item}`' for item in target_artifacts)}",
    ]
    if supplied:
        lines.append(f"- Supplied/reference support artifact(s): {', '.join(f'`{item}`' for item in supplied)}")
    lines.extend(
        [
            "- Visible context: public task, interface, artifact, stimulus, and observable contract only.",
            "- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.",
            "",
            "## Form-Specific Requirements",
            "",
        ]
    )
    if form == "dut":
        lines.append("- Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.")
    elif form == "tb":
        lines.append("- Implement only the Spectre transient testbench; use the supplied/reference DUT contract.")
    elif form == "bugfix":
        lines.append("- Repair the supplied buggy Verilog-A artifact while preserving the public module interface and artifact boundary.")
    else:
        lines.append("- Generate both the Verilog-A DUT and the Spectre transient testbench for this end-to-end task.")
    lines.extend(
        [
            "- Preserve the public module names, port order, parameters, and waveform observable names.",
            "",
            "## Public Verilog-A Interface",
            "",
            f"- `{spec.dut_file if form != 'bugfix' else 'dut_fixed.va'}` declares module `{spec.module_name}` with positional ports: "
            + ", ".join(f"`{port}`" for port in spec.ports)
            + ".",
            "",
            "## Public Behavior Checks",
            "",
        ]
    )
    lines.extend(f"- `{check}`" for check in spec.checks)
    lines.extend(
        [
            "",
            "## Output Contract",
            "",
            f"Return exactly {' and '.join(f'`{item}`' for item in target_artifacts)}.",
            "Do not include explanatory prose outside the source artifact contents.",
            "",
            "## Task-Specific Public Description",
            "",
            f"# {spec.description_title} ({form})",
            "",
            spec.description,
            f"Module name: `{spec.module_name}`.",
            "Domain: pure voltage-domain behavioral Verilog-A.",
            "Do not use current contributions, transistor-level devices, AC/noise analysis, or KCL/KVL solving assumptions.",
            "",
            "Public port contract:",
            "",
            "```verilog",
            f"module {spec.module_name}({', '.join(spec.ports)});",
            "```",
            "",
            "Saved waveform columns:",
            "",
            "```text",
            " ".join(spec.public_nodes),
            "```",
            "",
            "Public transient contract:",
            "",
            "```spectre",
            "tran tran stop=90n maxstep=250p",
            "```",
        ]
    )
    return "\n".join(lines)


def checks_yaml(spec: NewEntrySpec) -> str:
    checks = "\n".join(f'    - "{item}"' for item in spec.checks)
    observables = "\n".join(f'    - "{item}"' for item in spec.public_nodes)
    return f"""syntax:
  must_include:
    - "transition("
    - "@(cross("
  must_not_include:
    - "I("
    - "ddt("
    - "idt("
dut_compile:
  backend: "evas"
tb_compile:
  backend: "evas"
sim_correct:
  dut_companion_role: "function_checked_dut"
  strong_benchmark_claim: true
  checks:
{checks}
  public_observables:
{observables}
parity:
  reference: "spectre"
  status: "pending"
  notes:
    - "Fresh EVAS/Spectre dual validation is required after adding this release entry."
"""


def form_gold_paths(spec: NewEntrySpec, form: str, form_dir: Path) -> list[str]:
    gold_dir = form_dir / "gold"
    if form == "dut":
        return [rel(gold_dir / spec.dut_file)]
    if form == "tb":
        return [rel(gold_dir / spec.tb_file), rel(gold_dir / spec.dut_file)]
    if form == "bugfix":
        return [
            rel(gold_dir / "dut_buggy.va"),
            rel(gold_dir / "dut_fixed.va"),
            rel(gold_dir / spec.tb_file),
            rel(gold_dir / f"tb_{spec.source_base_id}_buggy.scs"),
        ]
    return [rel(gold_dir / spec.dut_file), rel(gold_dir / spec.tb_file)]


def release_task(spec: NewEntrySpec, form: str, form_dir: Path) -> dict[str, object]:
    artifacts = {
        "dut": [spec.dut_file],
        "tb": [spec.tb_file],
        "bugfix": ["dut_fixed.va"],
        "e2e": [spec.dut_file, spec.tb_file],
    }[form]
    public_inputs = ["prompt.md"]
    private_reference: list[str] = []
    if form == "tb":
        public_inputs.append(f"gold/{spec.dut_file}")
    if form == "bugfix":
        public_inputs.append("gold/dut_buggy.va")
        private_reference.append("gold/dut_fixed.va")
    return {
        "form": form,
        "release_path": rel(form_dir),
        "prompt": rel(form_dir / "prompt.md"),
        "meta": rel(form_dir / "meta.json"),
        "checks": rel(form_dir / "checks.yaml"),
        "gold": form_gold_paths(spec, form, form_dir),
        "public_inputs": public_inputs,
        "submission_artifacts": artifacts,
        "private_reference_artifacts": private_reference,
        "asset_materialized": True,
        "historical_dual_expected": False,
        "static_status": "pending",
        "evas_status": "pending",
        "spectre_status": "pending",
        "fresh_dual_rerun_required": True,
        "source_path": f"designed_release_spec:{spec.entry_id}",
        "release_source_task_id": f"{spec.entry_id}_{form}",
        "historical_source_task_id": f"{spec.entry_id}_{form}",
    }


def write_form(spec: NewEntrySpec, entry_dir: Path, form: str) -> dict[str, object]:
    form_dir = entry_dir / "forms" / form
    gold_dir = form_dir / "gold"
    write_text(form_dir / "prompt.md", prompt_text(spec, form))
    write_text(form_dir / "checks.yaml", checks_yaml(spec))
    write_text(
        form_dir / "SOURCE_TASK.md",
        f"""# Source Task

Release-designed vaBench entry added during the 64-entry benchmark rebalance.

- Release entry: `{spec.entry_id}`
- Form: `{form}`
- Source base id: `{spec.source_base_id}`
""",
    )
    write_json(
        form_dir / "meta.json",
        {
            "id": f"{spec.entry_id}_{form}",
            "task_id": f"{spec.entry_id}_{form}",
            "asset_type": "vabench_task",
            "benchmark": "vabench-release-v1",
            "release_entry_id": spec.entry_id,
            "family": FORM_TO_FAMILY[form],
            "category": spec.category,
            "domain": "voltage",
            "difficulty": "medium",
            "expected_backend": "evas",
            "provenance_status": "release_designed_pending_dual",
            "designed_source": True,
            "counts": {"model_capability": True, "benchmark_coverage": True, "bugfix_claim": form == "bugfix"},
            "inputs": ["prompt.md"],
            "artifacts": {
                "dut": [spec.dut_file],
                "tb": [spec.tb_file],
                "bugfix": ["dut_fixed.va"],
                "e2e": [spec.dut_file, spec.tb_file],
            }[form],
            "scoring": ["dut_compile", "tb_compile", "sim_correct"],
            "behavior_checks": spec.checks,
        },
    )
    if form == "dut":
        write_text(gold_dir / spec.dut_file, spec.dut_gold)
    elif form == "tb":
        write_text(gold_dir / spec.tb_file, spec.tb_gold)
        write_text(gold_dir / spec.dut_file, spec.dut_gold)
    elif form == "bugfix":
        write_text(gold_dir / "dut_buggy.va", spec.buggy_gold)
        write_text(gold_dir / "dut_fixed.va", spec.dut_gold)
        write_text(gold_dir / spec.tb_file, spec.tb_gold)
        write_text(gold_dir / f"tb_{spec.source_base_id}_buggy.scs", spec.tb_buggy_gold)
    elif form == "e2e":
        write_text(gold_dir / spec.dut_file, spec.dut_gold)
        write_text(gold_dir / spec.tb_file, spec.tb_gold)
    return release_task(spec, form, form_dir)


def write_new_entry(spec: NewEntrySpec) -> None:
    entry_dir = TASKS_ROOT / CATEGORY_DIRS[spec.category] / spec.entry_id
    if entry_dir.exists():
        shutil.rmtree(entry_dir)
    release_tasks = [write_form(spec, entry_dir, form) for form in ("dut", "tb", "bugfix", "e2e")]
    source_tasks = [
        {
            "form": form,
            "source_path": f"designed_release_spec:{spec.entry_id}",
            "prompt": True,
            "meta": True,
            "checks": True,
            "gold": True,
            "asset_complete": True,
            "checks_has_sim_correct": True,
            "checks_has_parity": True,
            "checks_normalized_for_release": False,
        }
        for form in ("dut", "tb", "bugfix", "e2e")
    ]
    write_json(
        entry_dir / "release_entry.json",
        {
            "id": spec.entry_id,
            "benchmark": "vabench-release-v1",
            "release_entry_id": spec.entry_id,
            "level": "L1",
            "category": spec.category,
            "base_function": spec.base_function,
            "package_status": "selected_l1_addition",
            "score_surface": "model-capability",
            "source_base_id": spec.source_base_id,
            "canonical_kernel": spec.canonical_kernel,
            "source_registry_status": "release_designed",
            "source_evidence_status": "fresh_dual_rerun_required",
            "source_tasks": source_tasks,
            "release_tasks": release_tasks,
            "missing_forms": [],
            "certification": {
                "static": "pending",
                "evas": "pending",
                "spectre": "pending",
                "evidence": "benchmark-vabench-release-v1/reports/dual_certification.json",
            },
            "counts": {"benchmark_score": True, "model_capability": False, "l0_conformance": False},
            "release_blockers": ["evas_certification", "spectre_certification"],
        },
    )
    write_text(
        entry_dir / "README.md",
        f"""# {spec.entry_id}

{spec.base_function} release entry for vaBench.

This entry was added during the 64-entry benchmark rebalance to strengthen analog IC signal-path coverage.
It is static-materialized and awaits fresh EVAS/Spectre dual validation.
""",
    )


def update_tracker() -> None:
    fieldnames, rows = read_csv(TRACKER_CSV)
    rows = [row for row in rows if row["entry_id"] not in DELETE_ENTRY_IDS]
    existing_ids = {row["entry_id"] for row in rows}
    for spec in NEW_ENTRIES:
        if spec.entry_id not in existing_ids:
            rows.append(
                {
                    "entry_id": spec.entry_id,
                    "category": spec.category,
                    "base_function": spec.base_function,
                    "level": "L1",
                    "package_status": "selected_l1_addition",
                    "release_status": "Required rebalance addition",
                    "score_surface": "model-capability",
                    "required_task_forms": "dut; tb; bugfix; e2e-form",
                    "complete_circuit_form": spec.complete_circuit_form,
                    "materialization_status": "release_designed",
                    "prompt_status": "complete",
                    "meta_status": "complete",
                    "checks_status": "complete",
                    "gold_status": "complete",
                    "static_status": "pending",
                    "evas_status": "pending",
                    "spectre_status": "pending",
                    "certification_status": "not_certified",
                    "evidence_link": "",
                    "notes": "Added during 64-entry rebalance; fresh dual validation required before full certification.",
                }
            )
    write_csv(TRACKER_CSV, fieldnames, rows)
    counts = Counter(row["package_status"] for row in rows)
    lines = [
        "# vaBench Release Tracker",
        "",
        f"Date: {date.today().isoformat()}",
        "",
        "This tracker is the execution queue for the paper-facing vaBench release package.",
        "It reflects the 64-entry rebalance: 51 core DUT entries and 13 benchmark-support entries.",
        "",
        "## Count Summary",
        "",
        "| Status | Count |",
        "| --- | ---: |",
    ]
    for status, count in sorted(counts.items()):
        lines.append(f"| {status} | {count} |")
    lines.append(f"| total | {len(rows)} |")
    lines.extend(
        [
            "",
            "## Tracker Rows",
            "",
            "| Entry | Level | Category | Function | Package status | Certification |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        lines.append(
            f"| {row['entry_id']} | {row['level']} | {row['category']} | {row['base_function']} | "
            f"{row['package_status']} | {row['certification_status']} |"
        )
    write_text(TRACKER_MD, "\n".join(lines))


def update_seed_manifest() -> None:
    fieldnames, rows = read_csv(SEED_CSV)
    rows = [row for row in rows if row["entry_id"] not in DELETE_ENTRY_IDS]
    write_csv(SEED_CSV, fieldnames, rows)
    lines = [
        "# vaBench Release Seed Manifest",
        "",
        f"Date: {date.today().isoformat()}",
        "",
        "This manifest tracks source-seed rows retained after the 64-entry release rebalance.",
        "",
        "| Entry | Base id | Category | Forms | Package dir |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['entry_id']} | {row['base_id']} | {row['category']} | "
            f"{row['asset_materialized_forms']} | {row['package_task_dir']} |"
        )
    write_text(SEED_MD, "\n".join(lines))


def update_selected_manifest() -> None:
    fieldnames, rows = read_csv(SELECTED_CSV)
    rows = [row for row in rows if row["entry_id"] not in DELETE_ENTRY_IDS]
    existing_ids = {row["entry_id"] for row in rows}
    for spec in NEW_ENTRIES:
        if spec.entry_id not in existing_ids:
            rows.append(
                {
                    "entry_id": spec.entry_id,
                    "base_function": spec.base_function,
                    "package_status": "selected_l1_addition",
                    "forms_materialized": "dut|tb|bugfix|e2e",
                    "missing_forms": "",
                    "source_paths": f"designed_release_spec:{spec.entry_id}",
                    "invalid_source_paths": "",
                    "package_task_dir": (
                        f"benchmark-vabench-release-v1/tasks/{CATEGORY_DIRS[spec.category]}/{spec.entry_id}"
                    ),
                    "notes": "release-designed strong analog entry added during 64-entry rebalance; fresh dual evidence pending",
                }
            )
    write_csv(SELECTED_CSV, fieldnames, rows)
    materialized_count = sum(1 for row in rows if row.get("forms_materialized", ""))
    lines = [
        "# vaBench Release Selected Manifest",
        "",
        f"Date: {date.today().isoformat()}",
        "",
        "This manifest records selected L1/L2 release entries created by the long-run materializer",
        "or by later release-designed rebalance additions.",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| selected entries | {len(rows)} |",
        f"| entries with copied or designed source assets | {materialized_count} |",
        f"| entries pending source design | {len(rows) - materialized_count} |",
        "",
        "## Rows",
        "",
        "| Entry | Forms | Missing forms | Source paths | Notes |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['entry_id']}` | `{row['forms_materialized']}` | `{row['missing_forms']}` | "
            f"`{row['source_paths']}` | {row['notes']} |"
        )
    write_text(SELECTED_MD, "\n".join(lines))


def main() -> None:
    for entry_id in sorted(DELETE_ENTRY_IDS):
        remove_entry(entry_id)
    for spec in NEW_ENTRIES:
        write_new_entry(spec)
    update_tracker()
    update_seed_manifest()
    update_selected_manifest()
    remaining = sorted(path.parent.name for path in TASKS_ROOT.glob("*/vbr1_*/release_entry.json"))
    missing_delete = sorted(DELETE_ENTRY_IDS & set(remaining))
    if missing_delete:
        raise SystemExit(f"deleted entries still present: {missing_delete}")
    print(f"rebuilt vaBench release set: entries={len(remaining)}; deleted={len(DELETE_ENTRY_IDS)}; added={len(NEW_ENTRIES)}")


if __name__ == "__main__":
    main()
