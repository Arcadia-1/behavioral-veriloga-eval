#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import shutil
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
TASKS_ROOT = PACKAGE_ROOT / "tasks"
EVIDENCE_ROOT = PACKAGE_ROOT / "evidence"
DOCS_ROOT = ROOT / "docs"
TRACKER_CSV = DOCS_ROOT / "VABENCH_RELEASE_TRACKER.csv"
TRACKER_MD = DOCS_ROOT / "VABENCH_RELEASE_TRACKER.md"
SELECTED_CSV = DOCS_ROOT / "VABENCH_RELEASE_SELECTED_MANIFEST.csv"
SELECTED_MD = DOCS_ROOT / "VABENCH_RELEASE_SELECTED_MANIFEST.md"

FORM_TO_FAMILY = {
    "dut": "spec-to-va",
    "tb": "tb-generation",
    "bugfix": "bugfix",
    "e2e": "end-to-end",
}

CATEGORY_DIRS = {
    "Data Converter Models": "CT01_data_converter_models",
    "Baseband Signal Conditioning": "CT04_baseband_signal_conditioning",
}


@dataclass(frozen=True)
class EntrySpec:
    entry_id: str
    replacement_for: str
    category: str
    level: str
    package_status: str
    score_surface: str
    base_function: str
    source_base_id: str
    canonical_kernel: str
    forms: tuple[str, ...]
    module_name: str
    dut_file: str
    tb_file: str
    ports: tuple[str, ...]
    public_nodes: tuple[str, ...]
    checks: tuple[str, ...]
    description: str
    dut_gold: str | None
    buggy_gold: str | None
    tb_gold: str
    tb_buggy_gold: str | None = None


CONVERTER_DESCRIPTION = """Build a voltage-domain static-linearity characterization flow for a 4-bit converter pair.

The circuit samples an input ramp, quantizes it to a 4-bit code, reconstructs a deliberately
non-ideal DAC voltage, and uses a lightweight measurement stage to derive DNL/INL-like
metric voltages from the observed reconstruction. This is a converter measurement flow:
the checker observes code coverage, monotonic reconstruction, non-uniform code steps, and
metric consistency against the measured code/reconstruction history.
"""

CONVERTER_VA = """`include "constants.vams"
`include "disciplines.vams"

module converter_static_linearity_measurement_flow(clk, rst, vin, code, recon, dnl, inl);
    input clk, rst, vin;
    output code, recon, dnl, inl;
    electrical clk, rst, vin, code, recon, dnl, inl;

    parameter real vth = 0.45;
    parameter real vfs = 0.9;
    parameter real tr = 120p from (0:inf);

    integer code_state;
    integer prev_valid;
    integer prev_code;
    real recon_v;
    real prev_recon;
    real ideal_recon;
    real ideal_step;
    real step_err;
    real dnl_v;
    real inl_v;

    analog begin
        @(initial_step) begin
            code_state = 0;
            prev_valid = 0;
            prev_code = 0;
            recon_v = 0.0;
            prev_recon = 0.0;
            dnl_v = 0.45;
            inl_v = 0.45;
        end

        @(cross(V(clk) - vth, +1)) begin
            if (V(rst) > vth) begin
                code_state = 0;
                prev_valid = 0;
                prev_code = 0;
                prev_recon = 0.0;
                recon_v = 0.0;
                dnl_v = 0.45;
                inl_v = 0.45;
            end else begin
                code_state = floor((V(vin) / vfs) * 15.0 + 0.5);
                if (code_state < 0) code_state = 0;
                if (code_state > 15) code_state = 15;

                case (code_state)
                    0:  recon_v = 0.000;
                    1:  recon_v = 0.055;
                    2:  recon_v = 0.118;
                    3:  recon_v = 0.182;
                    4:  recon_v = 0.245;
                    5:  recon_v = 0.303;
                    6:  recon_v = 0.366;
                    7:  recon_v = 0.428;
                    8:  recon_v = 0.491;
                    9:  recon_v = 0.553;
                    10: recon_v = 0.612;
                    11: recon_v = 0.674;
                    12: recon_v = 0.735;
                    13: recon_v = 0.798;
                    14: recon_v = 0.855;
                    default: recon_v = 0.900;
                endcase

                ideal_recon = 0.06 * code_state;
                inl_v = 0.45 + 3.0 * (recon_v - ideal_recon);
                if (inl_v < 0.05) inl_v = 0.05;
                if (inl_v > 0.85) inl_v = 0.85;

                if (prev_valid > 0 && code_state > prev_code) begin
                    ideal_step = 0.06 * (code_state - prev_code);
                    step_err = (recon_v - prev_recon) - ideal_step;
                    dnl_v = 0.45 + 4.0 * step_err;
                    if (dnl_v < 0.05) dnl_v = 0.05;
                    if (dnl_v > 0.85) dnl_v = 0.85;
                end else begin
                    dnl_v = 0.45;
                end

                prev_code = code_state;
                prev_recon = recon_v;
                prev_valid = 1;
            end
        end

        V(code) <+ transition(0.06 * code_state, 0, tr, tr);
        V(recon) <+ transition(recon_v, 0, tr, tr);
        V(dnl) <+ transition(dnl_v, 0, tr, tr);
        V(inl) <+ transition(inl_v, 0, tr, tr);
    end
endmodule
"""

CONVERTER_TB = """simulator lang=spectre
global 0

ahdl_include "converter_static_linearity_measurement_flow.va"

Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 period=4n width=2n delay=1n rise=100p fall=100p
Vrst (rst 0) vsource type=pwl wave=[0 0.9 2n 0.9 2.1n 0 96n 0]
Vvin (vin 0) vsource type=pwl wave=[0 0.0 4n 0.0 88n 0.9 96n 0.9]

XDUT (clk rst vin code recon dnl inl) converter_static_linearity_measurement_flow

tran tran stop=96n maxstep=250p
save clk rst vin code recon dnl inl
"""

RECTIFIER_DESCRIPTION = """Write a voltage-domain precision rectifier with an envelope output.

The module rectifies the absolute deviation around the common-mode voltage rather than around
ground. It also tracks a peak envelope: the envelope updates quickly to new rectified peaks and
decays slowly when the rectified input falls. The metric output is high when the envelope is
holding above the instantaneous rectified value.
"""

RECTIFIER_VA = """`include "constants.vams"
`include "disciplines.vams"

module precision_rectifier_envelope_detector(clk, rst, vin, rect, env, metric);
    input clk, rst, vin;
    output rect, env, metric;
    electrical clk, rst, vin, rect, env, metric;

    parameter real vth = 0.45;
    parameter real vcm = 0.45;
    parameter real decay = 0.018 from [0:inf);
    parameter real tr = 150p from (0:inf);

    real rect_v;
    real env_state;
    real metric_v;

    analog begin
        @(initial_step) begin
            env_state = vcm;
            metric_v = 0.0;
        end

        rect_v = vcm + abs(V(vin) - vcm);
        if (rect_v > 0.9) rect_v = 0.9;

        @(cross(V(clk) - vth, +1)) begin
            if (V(rst) > vth) begin
                env_state = vcm;
            end else if (rect_v > env_state) begin
                env_state = rect_v;
            end else begin
                env_state = env_state - decay;
                if (env_state < rect_v) env_state = rect_v;
                if (env_state < vcm) env_state = vcm;
            end
        end

        metric_v = (env_state - rect_v > 0.030) ? 0.9 : 0.0;

        V(rect) <+ transition(rect_v, 0, tr, tr);
        V(env) <+ transition(env_state, 0, tr, tr);
        V(metric) <+ transition(metric_v, 0, tr, tr);
    end
endmodule
"""

RECTIFIER_BUGGY = """`include "constants.vams"
`include "disciplines.vams"

module precision_rectifier_envelope_detector(clk, rst, vin, rect, env, metric);
    input clk, rst, vin;
    output rect, env, metric;
    electrical clk, rst, vin, rect, env, metric;

    parameter real vth = 0.45;
    parameter real vcm = 0.45;
    parameter real tr = 150p from (0:inf);

    real rect_v;
    real env_state;

    analog begin
        @(initial_step) begin
            env_state = vcm;
        end

        rect_v = (V(vin) > vcm) ? V(vin) : vcm;

        @(cross(V(clk) - vth, +1)) begin
            if (V(rst) > vth)
                env_state = vcm;
            else
                env_state = rect_v;
        end

        V(rect) <+ transition(rect_v, 0, tr, tr);
        V(env) <+ transition(env_state, 0, tr, tr);
        V(metric) <+ transition(0.0, 0, tr, tr);
    end
endmodule
"""

RECTIFIER_TB = """simulator lang=spectre
global 0

ahdl_include "precision_rectifier_envelope_detector.va"

Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 period=2n width=1n delay=0.5n rise=100p fall=100p
Vrst (rst 0) vsource type=pwl wave=[0 0.9 2n 0.9 2.1n 0 90n 0]
Vvin (vin 0) vsource type=pwl wave=[0 0.45 8n 0.75 16n 0.45 24n 0.15 32n 0.45 42n 0.85 54n 0.45 66n 0.35 78n 0.45 90n 0.45]

XDUT (clk rst vin rect env metric) precision_rectifier_envelope_detector

tran tran stop=90n maxstep=250p
save clk rst vin rect env metric
"""

RECTIFIER_TB_BUGGY = RECTIFIER_TB.replace(
    'ahdl_include "precision_rectifier_envelope_detector.va"',
    'ahdl_include "dut_buggy.va"',
)

SPECS = [
    EntrySpec(
        entry_id="vbr1_l2_converter_static_linearity_measurement_flow",
        replacement_for="vbr1_l2_adc_dac_reconstruction_chain",
        category="Data Converter Models",
        level="L2",
        package_status="selected_l2_target",
        score_surface="benchmark-e2e",
        base_function="Converter static linearity measurement flow",
        source_base_id="converter_static_linearity_measurement_flow",
        canonical_kernel="converter_static_linearity_measurement_flow",
        forms=("e2e", "tb"),
        module_name="converter_static_linearity_measurement_flow",
        dut_file="converter_static_linearity_measurement_flow.va",
        tb_file="tb_converter_static_linearity_measurement_flow.scs",
        ports=("clk", "rst", "vin", "code", "recon", "dnl", "inl"),
        public_nodes=("clk", "rst", "vin", "code", "recon", "dnl", "inl"),
        checks=(
            "ramp_code_coverage",
            "monotonic_reconstruction",
            "nonuniform_dnl_metric",
            "inl_metric_matches_reconstruction_error",
            "dnl_metric_matches_step_error",
        ),
        description=CONVERTER_DESCRIPTION,
        dut_gold=CONVERTER_VA,
        buggy_gold=None,
        tb_gold=CONVERTER_TB,
    ),
    EntrySpec(
        entry_id="vbr1_l1_precision_rectifier_envelope_detector",
        replacement_for="vbr1_l1_voltage_gain_amplifier",
        category="Baseband Signal Conditioning",
        level="L1",
        package_status="selected_l1_addition",
        score_surface="model-capability",
        base_function="Precision rectifier/envelope detector",
        source_base_id="precision_rectifier_envelope_detector",
        canonical_kernel="precision_rectifier_envelope_detector",
        forms=("dut", "tb", "bugfix", "e2e"),
        module_name="precision_rectifier_envelope_detector",
        dut_file="precision_rectifier_envelope_detector.va",
        tb_file="tb_precision_rectifier_envelope_detector.scs",
        ports=("clk", "rst", "vin", "rect", "env", "metric"),
        public_nodes=("clk", "rst", "vin", "rect", "env", "metric"),
        checks=(
            "full_wave_rectification_around_common_mode",
            "envelope_peak_hold_and_decay",
            "negative_half_cycle_rectifies",
            "hold_metric_marks_envelope_memory",
        ),
        description=RECTIFIER_DESCRIPTION,
        dut_gold=RECTIFIER_VA,
        buggy_gold=RECTIFIER_BUGGY,
        tb_gold=RECTIFIER_TB,
        tb_buggy_gold=RECTIFIER_TB_BUGGY,
    ),
]

SEQUENCER_ENTRY_ID = "vbr1_l2_programmable_stimulus_sequencer"
SEQUENCER_CATEGORY_DIR = "SUP02_stimulus_and_source_generators"
SEQUENCER_VA = """`include "constants.vams"
`include "disciplines.vams"

module programmable_stimulus_sequencer(clk, rst, mode, gate, out, metric);
input clk, rst, mode, gate;
output out, metric;
electrical clk, rst, mode, gate, out, metric;
parameter real tr = 80p;
parameter real vth = 0.45;
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
        end else if (V(mode) > 0.60 && V(gate) > 0.45) begin
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


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def safe_rmtree(path: Path) -> None:
    if not path.exists():
        return
    path = path.resolve()
    allowed_roots = [
        TASKS_ROOT.resolve(),
        (EVIDENCE_ROOT / "static").resolve(),
        (EVIDENCE_ROOT / "dual").resolve(),
    ]
    if not any(root in path.parents for root in allowed_roots):
        raise RuntimeError(f"refuse to remove out-of-scope path: {path}")
    shutil.rmtree(path)


def remove_entry(entry_id: str) -> None:
    for task_dir in TASKS_ROOT.glob(f"CT*/{entry_id}"):
        safe_rmtree(task_dir)
    safe_rmtree(EVIDENCE_ROOT / "static" / entry_id)
    safe_rmtree(EVIDENCE_ROOT / "dual" / entry_id)


def port_contract(spec: EntrySpec) -> str:
    inputs = ", ".join(spec.ports[:3])
    outputs = ", ".join(spec.ports[3:])
    electrical = ", ".join(spec.ports)
    return (
        f"module {spec.module_name}({', '.join(spec.ports)});\n"
        f"input {inputs};\n"
        f"output {outputs};\n"
        f"electrical {electrical}"
    )


def form_prompt(spec: EntrySpec, form: str) -> str:
    artifacts = {
        "dut": [spec.dut_file],
        "tb": [spec.tb_file],
        "bugfix": ["dut_fixed.va"],
        "e2e": [spec.dut_file, spec.tb_file],
    }[form]
    artifact_text = ", ".join(f"`{item}`" for item in artifacts)
    if form == "dut":
        form_req = "Implement only the requested Verilog-A DUT artifact; do not generate a Spectre testbench."
        title = "spec-to-va"
    elif form == "tb":
        form_req = f"Implement only the Spectre testbench artifact. Instantiate `{spec.module_name}` using the public ports."
        title = "testbench generation"
    elif form == "bugfix":
        form_req = "Repair `gold/dut_buggy.va` and return exactly `dut_fixed.va` with the same module and port contract."
        title = "bugfix"
    else:
        form_req = "Implement both the Verilog-A DUT and the Spectre testbench artifacts."
        title = "end-to-end"

    return f"""# Task: {spec.entry_id}:{form}

## Release Task Contract

- Form: `{form}`
- Level: `{spec.level}`
- Category: {spec.category}
- Base function: {spec.base_function}
- Domain: `voltage`
- Target artifact(s): {artifact_text}
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- {form_req}
- Preserve the public module names, port order, parameters, and waveform observable names.

## Public Verilog-A Interface

- `{spec.dut_file}` declares module `{spec.module_name}` with positional ports: {", ".join(f"`{port}`" for port in spec.ports)}.

## Public Behavior Checks

{chr(10).join(f"- `{check}`" for check in spec.checks)}

## Output Contract

Return exactly {artifact_text}. Do not include explanatory prose outside the requested artifact contents.

## Task-Specific Public Description

# {spec.base_function} ({title})

{spec.description.strip()}

Public port contract:

```verilog
{port_contract(spec)}
```

Signal contract:

All logic controls are voltage-coded, low=0 V and high=0.9 V with threshold 0.45 V. The design remains pure voltage-domain behavioral Verilog-A: no current contributions, transistor devices, AC/noise analysis, or KCL/KVL solving assumptions.

Saved waveform columns:

```text
{" ".join(spec.public_nodes)}
```

Public transient contract:

```spectre
tran tran stop=96n maxstep=0.25n
```
"""


def meta_payload(spec: EntrySpec, form: str) -> dict[str, object]:
    artifacts = {
        "dut": [spec.dut_file],
        "tb": [spec.tb_file],
        "bugfix": ["dut_fixed.va"],
        "e2e": [spec.dut_file, spec.tb_file],
    }[form]
    inputs = ["prompt.md"]
    public_inputs = ["prompt.md"]
    private_reference_artifacts: list[str] = []
    if form == "bugfix":
        inputs = ["prompt.md", "gold/dut_buggy.va"]
        public_inputs = ["prompt.md", "gold/dut_buggy.va"]
        private_reference_artifacts = ["gold/dut_fixed.va"]
    return {
        "id": f"{spec.entry_id}_{form}",
        "task_id": f"{spec.entry_id}_{form}",
        "asset_type": "vabench_task",
        "benchmark": "vabench-release-v1",
        "release_entry_id": spec.entry_id,
        "family": FORM_TO_FAMILY[form],
        "category": spec.category,
        "domain": "voltage",
        "difficulty": "hard" if spec.level == "L2" or form == "e2e" else "medium",
        "expected_backend": "evas",
        "inputs": inputs,
        "artifacts": artifacts,
        "scoring": ["dut_compile", "tb_compile", "sim_correct"],
        "behavior_checks": list(spec.checks),
        "designed_source": True,
        "public_inputs": public_inputs,
        "submission_artifacts": artifacts,
        "private_reference_artifacts": private_reference_artifacts,
    }


def checks_yaml(spec: EntrySpec, form: str) -> str:
    includes: list[str] = []
    if form in {"dut", "bugfix", "e2e"}:
        includes.append("transition(")
        includes.append("@(cross(")
    if form in {"tb", "e2e"}:
        includes.extend(["tran", "save"])
    if spec.entry_id.endswith("precision_rectifier_envelope_detector") and form in {"dut", "bugfix", "e2e"}:
        includes.append("abs(")
    public = "\n".join(f"    - \"{node}\"" for node in spec.public_nodes)
    checks = "\n".join(f"    - \"{check}\"" for check in spec.checks)
    return f"""syntax:
  must_include:
{chr(10).join(f'    - "{item}"' for item in includes)}
  must_not_include:
    - "I("
    - "ddt("
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
{public}
parity:
  reference: "spectre"
  status: "pending"
  notes:
    - "Fresh EVAS/Spectre dual validation is required after the ahdlLib-guided quality refinement."
"""


def gold_files_for_form(spec: EntrySpec, form: str) -> list[str]:
    if form == "dut":
        return [spec.dut_file]
    if form == "tb":
        return [spec.tb_file]
    if form == "bugfix":
        return ["dut_buggy.va", "dut_fixed.va"]
    return [spec.dut_file, spec.tb_file]


def write_form(spec: EntrySpec, form: str, entry_dir: Path) -> dict[str, object]:
    form_dir = entry_dir / "forms" / form
    gold_dir = form_dir / "gold"
    gold_dir.mkdir(parents=True, exist_ok=True)
    if form in {"dut", "e2e"} and spec.dut_gold is not None:
        write_text(gold_dir / spec.dut_file, spec.dut_gold)
    if form == "tb":
        write_text(gold_dir / spec.tb_file, spec.tb_gold)
    if form == "e2e":
        write_text(gold_dir / spec.tb_file, spec.tb_gold)
    if form == "bugfix":
        assert spec.buggy_gold is not None
        write_text(gold_dir / "dut_buggy.va", spec.buggy_gold)
        write_text(gold_dir / "dut_fixed.va", spec.dut_gold or "")

    write_text(form_dir / "prompt.md", form_prompt(spec, form))
    write_json(form_dir / "meta.json", meta_payload(spec, form))
    write_text(form_dir / "checks.yaml", checks_yaml(spec, form))
    write_text(
        form_dir / "SOURCE_TASK.md",
        f"""# Designed Release Source: {spec.entry_id} {form}

- Source: `designed_release_spec:{spec.entry_id}`
- Replacement rationale: clean-room ahdlLib-inspired coverage refinement; no Cadence source copied.
""",
    )

    gold = [rel(gold_dir / name) for name in gold_files_for_form(spec, form)]
    return {
        "form": form,
        "release_path": rel(form_dir),
        "prompt": rel(form_dir / "prompt.md"),
        "meta": rel(form_dir / "meta.json"),
        "checks": rel(form_dir / "checks.yaml"),
        "gold": gold,
        "public_inputs": ["prompt.md", "gold/dut_buggy.va"] if form == "bugfix" else ["prompt.md"],
        "submission_artifacts": ["dut_fixed.va"] if form == "bugfix" else (
            [spec.tb_file] if form == "tb" else [spec.dut_file] if form == "dut" else [spec.dut_file, spec.tb_file]
        ),
        "private_reference_artifacts": ["gold/dut_fixed.va"] if form == "bugfix" else [],
        "asset_materialized": True,
        "historical_dual_expected": False,
        "static_status": "pending",
        "evas_status": "pending",
        "spectre_status": "pending",
        "dual_evidence": rel(EVIDENCE_ROOT / "dual" / spec.entry_id / form / "evidence.json"),
        "fresh_dual_rerun_required": True,
        "source_path": f"designed_release_spec:{spec.entry_id}",
        "static_evidence": rel(EVIDENCE_ROOT / "static" / spec.entry_id / form / "evidence.json"),
        "static_result": rel(EVIDENCE_ROOT / "static" / spec.entry_id / form / "result.json"),
        "evas_result": rel(EVIDENCE_ROOT / "dual" / spec.entry_id / form / "evas_result.json"),
        "spectre_result": rel(EVIDENCE_ROOT / "dual" / spec.entry_id / form / "spectre_result.json"),
        "release_source_task_id": f"{spec.entry_id}_{form}",
        "historical_source_task_id": f"{spec.entry_id}_{form}",
    }


def write_entry(spec: EntrySpec) -> None:
    entry_dir = TASKS_ROOT / CATEGORY_DIRS[spec.category] / spec.entry_id
    release_tasks = [write_form(spec, form, entry_dir) for form in spec.forms]
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
        for form in spec.forms
    ]
    entry = {
        "id": spec.entry_id,
        "benchmark": "vabench-release-v1",
        "release_entry_id": spec.entry_id,
        "level": spec.level,
        "category": spec.category,
        "base_function": spec.base_function,
        "package_status": spec.package_status,
        "score_surface": spec.score_surface,
        "source_base_id": spec.source_base_id,
        "canonical_kernel": spec.canonical_kernel,
        "source_registry_status": "designed_from_ahdllib_coverage_review",
        "source_evidence_status": "designed_source_pending_dual",
        "source_tasks": source_tasks,
        "release_tasks": release_tasks,
        "missing_forms": [],
        "certification": {
            "static": "pending",
            "evas": "pending",
            "spectre": "pending",
            "evidence": rel(PACKAGE_ROOT / "reports" / "dual_certification.json"),
        },
        "counts": {
            "benchmark_score": True,
            "model_capability": False,
            "l0_conformance": False,
        },
        "release_blockers": ["static_validation", "evas_certification", "spectre_certification"],
    }
    write_json(entry_dir / "release_entry.json", entry)
    write_text(
        entry_dir / "README.md",
        f"""# {spec.entry_id}

- Level: `{spec.level}`
- Category: {spec.category}
- Base function: {spec.base_function}
- Forms: {", ".join(spec.forms)}

This entry is a clean-room ahdlLib-guided coverage refinement. It replaces
`{spec.replacement_for}` to improve circuit-function coverage without growing
the release denominator.
""",
    )


def update_tracker(specs: list[EntrySpec]) -> None:
    fields, rows = read_csv(TRACKER_CSV)
    replacements = {spec.replacement_for: spec for spec in specs}
    for idx, row in enumerate(rows):
        spec = replacements.get(row["entry_id"])
        if not spec:
            continue
        rows[idx] = {
            "entry_id": spec.entry_id,
            "category": spec.category,
            "base_function": spec.base_function,
            "level": spec.level,
            "package_status": spec.package_status,
            "release_status": "Required expansion",
            "score_surface": spec.score_surface,
            "required_task_forms": "; ".join("e2e-form" if form == "e2e" and spec.level == "L1" else form for form in spec.forms),
            "complete_circuit_form": "e2e-form" if "e2e" in spec.forms and spec.level == "L1" else "e2e",
            "materialization_status": "ahdlLib-guided clean-room replacement",
            "prompt_status": "missing",
            "meta_status": "pending",
            "checks_status": "pending",
            "gold_status": "pending",
            "static_status": "pending",
            "evas_status": "pending",
            "spectre_status": "pending",
            "certification_status": "not_certified",
            "evidence_link": "",
            "notes": f"Replaces {spec.replacement_for}; fresh static and dual evidence required.",
        }
    write_csv(TRACKER_CSV, fields, rows)
    lines = [
        "# vaBench Release Tracker",
        "",
        "| Entry | Level | Category | Base function | Status | Certification |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['entry_id']} | {row['level']} | {row['category']} | {row['base_function']} | "
            f"{row['package_status']} | {row['certification_status']} |"
        )
    write_text(TRACKER_MD, "\n".join(lines))


def update_selected_manifest(specs: list[EntrySpec]) -> None:
    fields, rows = read_csv(SELECTED_CSV)
    replacements = {spec.replacement_for: spec for spec in specs}
    for idx, row in enumerate(rows):
        spec = replacements.get(row["entry_id"])
        if not spec:
            continue
        rows[idx] = {
            "entry_id": spec.entry_id,
            "base_function": spec.base_function,
            "package_status": spec.package_status,
            "forms_materialized": "|".join(spec.forms),
            "missing_forms": "",
            "source_paths": f"designed_release_spec:{spec.entry_id}",
            "invalid_source_paths": "",
            "package_task_dir": rel(TASKS_ROOT / CATEGORY_DIRS[spec.category] / spec.entry_id),
            "notes": f"ahdlLib-guided clean-room replacement for {spec.replacement_for}; dual evidence pending rerun",
        }
    write_csv(SELECTED_CSV, fields, rows)
    lines = [
        "# vaBench Release Selected Manifest",
        "",
        "| Entry | Forms | Source | Notes |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['entry_id']}` | `{row['forms_materialized']}` | `{row['source_paths']}` | {row['notes']} |"
        )
    write_text(SELECTED_MD, "\n".join(lines))


def update_sequencer_assets() -> None:
    entry_dir = TASKS_ROOT / SEQUENCER_CATEGORY_DIR / SEQUENCER_ENTRY_ID
    write_text(entry_dir / "forms" / "e2e" / "gold" / "programmable_stimulus_sequencer.va", SEQUENCER_VA)

    for form in ("e2e", "tb"):
        form_dir = entry_dir / "forms" / form
        meta_path = form_dir / "meta.json"
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        meta["behavior_checks"] = [
            "ramp_segment_monotonic",
            "swept_chirp_segment_frequency_increases",
            "burst_prbs_gate_schedule",
            "mode_switch_continuity",
        ]
        write_json(meta_path, meta)

        checks_path = form_dir / "checks.yaml"
        checks = checks_path.read_text(encoding="utf-8")
        checks = checks.replace("sine_segment_amplitude_frequency", "swept_chirp_segment_frequency_increases")
        checks = checks.replace(
            "Certified by release dual evidence for this form.",
            "Fresh EVAS/Spectre dual validation is required after the swept-source refinement.",
        )
        checks = checks.replace("status: \"pass\"", "status: \"pending\"")
        write_text(checks_path, checks)

        prompt_path = form_dir / "prompt.md"
        prompt = prompt_path.read_text(encoding="utf-8")
        prompt = prompt.replace("swept/chirp swept/chirp sine", "swept/chirp sine")
        prompt = prompt.replace(
            "Ramp + sine + gated burst/PRBS schedule with mode-switch continuity checker",
            "Ramp + swept/chirp sine + gated burst/PRBS schedule with mode-switch continuity checker",
        )
        prompt = prompt.replace(
            "segments: a ramp, a sinusoidal segment, and a gated burst/PRBS segment.",
            "segments: a ramp, a swept/chirp sine segment, and a gated burst/PRBS segment.",
        )
        prompt = prompt.replace(
            "sine_segment_amplitude_frequency",
            "swept_chirp_segment_frequency_increases",
        )
        prompt = prompt.replace("mid selects sine", "mid selects swept/chirp sine")
        write_text(prompt_path, prompt)

    release_entry_path = entry_dir / "release_entry.json"
    entry = json.loads(release_entry_path.read_text(encoding="utf-8"))
    entry["source_evidence_status"] = "designed_source_pending_dual_after_swept_source_refinement"
    for task in entry.get("release_tasks", []):
        if isinstance(task, dict):
            task["fresh_dual_rerun_required"] = True
            task["historical_dual_expected"] = False
            task["evas_status"] = "pending"
            task["spectre_status"] = "pending"
    write_json(release_entry_path, entry)


def main() -> None:
    for spec in SPECS:
        remove_entry(spec.replacement_for)
        remove_entry(spec.entry_id)
        write_entry(spec)
    update_tracker(SPECS)
    update_selected_manifest(SPECS)
    update_sequencer_assets()
    print(
        "applied ahdlLib-guided quality refinements: "
        + ", ".join(f"{spec.replacement_for}->{spec.entry_id}" for spec in SPECS)
        + f"; strengthened {SEQUENCER_ENTRY_ID}"
    )


if __name__ == "__main__":
    main()
