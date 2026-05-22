#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import shutil
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
TASKS_ROOT = PACKAGE_ROOT / "tasks"
SELECTED_MANIFEST_CSV = ROOT / "docs" / "VABENCH_RELEASE_SELECTED_MANIFEST.csv"
SELECTED_MANIFEST_MD = ROOT / "docs" / "VABENCH_RELEASE_SELECTED_MANIFEST.md"
FORM_ORDER = ["dut", "tb", "bugfix", "e2e"]
FAMILY_BY_FORM = {
    "dut": "spec-to-va",
    "tb": "tb-generation",
    "bugfix": "bugfix",
    "e2e": "end-to-end",
}

DUT_FUNCTION_CONTRACTS: dict[str, dict[str, object]] = {
    "vbr1_l1_burst_clock_source": {
        "module": "clk_burst_gen(CLK, RST_N, CLK_OUT)",
        "ports": [
            "`CLK`: input electrical clock, 0 V low and 0.9 V high",
            "`RST_N`: input electrical active-low reset, deasserted high during checking",
            "`CLK_OUT`: output electrical burst clock",
        ],
        "behavior": [
            "parameter `div` defaults to 8 and sets the burst repeat period in input-clock cycles",
            "`CLK_OUT` mirrors `CLK` for the first two cycles of each `div`-cycle window",
            "`CLK_OUT` stays low for the remaining cycles and while reset is asserted",
            "use `@(cross(...))` edge detection and `transition(...)` output drive",
        ],
        "observables": ["CLK", "RST_N", "CLK_OUT"],
        "syntax": ["@(cross(", "transition("],
        "checks": ["clk_out_present", "clk_out_duty_cycle_is_burst"],
    },
    "vbr1_l1_clocked_adc_quantizer": {
        "module": "flash_adc_3b(vdd, vss, vin, clk, dout2, dout1, dout0)",
        "ports": [
            "`vdd`, `vss`: electrical supply rails",
            "`vin`: input electrical analog voltage, clamped to the 0 V to 0.9 V conversion range",
            "`clk`: input electrical sampling clock",
            "`dout2`, `dout1`, `dout0`: output electrical code bits, MSB to LSB",
        ],
        "behavior": [
            "on each rising `clk` edge, quantize `V(vin)` into one of eight uniform bins",
            "clamp the converted code to `[0, 7]`",
            "drive output bits to `V(vdd)` for logic 1 and `V(vss)` for logic 0",
            "hold the sampled code between clock edges",
        ],
        "observables": ["vin", "clk", "dout2", "dout1", "dout0"],
        "syntax": ["@(cross(", "transition("],
        "checks": ["flash_adc_all_8_codes_present", "flash_adc_monotonic_with_ramp"],
    },
    "vbr1_l1_clocked_sample_and_hold": {
        "module": "sample_hold(vdd, vss, in, clk, out)",
        "ports": [
            "`vdd`, `vss`: electrical supply rails",
            "`in`: input electrical sampled voltage",
            "`clk`: input electrical sampling clock",
            "`out`: output electrical held voltage",
        ],
        "behavior": [
            "sample `V(in)` only on rising `clk` crossings",
            "hold the sampled value between clock edges without continuously tracking the input",
            "drive `out` with bounded voltage-domain `transition(...)` behavior",
        ],
        "observables": ["in", "clk", "out"],
        "syntax": ["@(cross(", "transition("],
        "checks": ["sh_output_tracks_input_at_edges", "sh_output_held_between_edges"],
    },
    "vbr1_l1_digital_phase_accumulator_with_modulo_wrap": {
        "module": "phase_accumulator_timer_wrap_ref(VDD, VSS, clk_out, phase_out)",
        "ports": [
            "`VDD`, `VSS`: electrical supply rails",
            "`clk_out`: output electrical derived clock",
            "`phase_out`: output electrical normalized phase monitor",
        ],
        "behavior": [
            "advance phase by `phase_step` every `dt` using `@(timer(...))`",
            "wrap phase manually into `[0, 1)` rather than letting it grow unbounded",
            "drive `phase_out` as a normalized monitor and toggle `clk_out` from the wrapped phase",
        ],
        "observables": ["time", "clk_out", "phase_out"],
        "syntax": ["@(timer(", "transition("],
        "checks": ["phase_accumulator_timer_wrap"],
    },
    "vbr1_l1_differential_output_driver": {
        "module": "differential_voltage_output_ref(VDD, VSS, din, en, outp, outn)",
        "ports": [
            "`VDD`, `VSS`: electrical supply rails",
            "`din`: input electrical logic-like data control, 0 V low and 0.9 V high",
            "`en`: input electrical enable control, 0 V disabled and 0.9 V enabled",
            "`outp`, `outn`: output electrical differential driver outputs",
        ],
        "behavior": [
            "when `en` is low, drive both outputs to the common-mode level",
            "when `en` is high and `din` is low, drive `outp-outn` negative",
            "when `en` is high and `din` is high, drive `outp-outn` positive",
            "keep both outputs bounded between `VSS` and `VDD` with finite `transition(...)` edges",
        ],
        "observables": ["din", "en", "outp", "outn"],
        "syntax": ["din", "en", "transition("],
        "checks": ["driver_disabled_common_mode", "driver_polarity_tracks_din", "driver_common_mode_stable"],
    },
    "vbr1_l1_dither_or_noise_like_deterministic_source": {
        "module": "noise_gen(vin_i, vout_o)",
        "ports": [
            "`vin_i`: input electrical baseline voltage",
            "`vout_o`: output electrical baseline plus sampled dither/noise-like perturbation",
        ],
        "behavior": [
            "add zero-mean sampled perturbation to `V(vin_i)`",
            "the public task checks non-trivial variation and bounded standard deviation; it does not claim physical noise analysis",
            "drive the output with pure voltage-domain `transition(...)` behavior",
        ],
        "observables": ["vin_i", "vout_o"],
        "syntax": ["transition("],
        "checks": ["noise_is_nontrivial", "noise_std_in_range"],
    },
    "vbr1_l1_dwa_dem_encoder": {
        "module": "dwa_ptr_gen(clk_i, rst_ni, code_msb_i[3:0], cell_en_o[15:0], ptr_o[15:0])",
        "ports": [
            "`clk_i`: input electrical clock",
            "`rst_ni`: input electrical active-low reset",
            "`code_msb_i[3:0]`: input electrical 4-bit code bus",
            "`cell_en_o[15:0]`: output electrical selected unit-element window",
            "`ptr_o[15:0]`: output electrical one-hot rotating pointer",
        ],
        "behavior": [
            "reset initializes the one-hot pointer to `ptr_init`",
            "on each post-reset rising clock edge, update `ptr = (ptr + code) % 16`",
            "assert a contiguous rotating cell-enable window derived from the effective code",
            "expose vector bits as scalar waveform columns in the companion testbench",
        ],
        "observables": ["clk_i", "rst_ni", "code_3..code_0", "cell_en_15..cell_en_0", "ptr_15..ptr_0"],
        "syntax": ["@(cross(", "transition("],
        "checks": ["ptr_is_one_hot_after_reset", "cell_en_nonzero_after_reset", "dwa_rotation_correct"],
    },
    "vbr1_l1_hysteresis_comparator": {
        "module": "cmp_hysteresis(vinn, vinp, out_n, out_p, vss, vdd)",
        "ports": [
            "`vinn`, `vinp`: input electrical differential pair",
            "`out_n`, `out_p`: output electrical complementary decisions",
            "`vss`, `vdd`: electrical supply rails",
        ],
        "behavior": [
            "trip high when `V(vinp)-V(vinn)` exceeds `+vhys/2`",
            "trip low when `V(vinp)-V(vinn)` falls below `-vhys/2`",
            "hold the previous decision inside the hysteresis band",
            "drive complementary rail-referenced outputs with `transition(...)`",
        ],
        "observables": ["time", "out_p", "out_n"],
        "syntax": ["@(cross(", "transition("],
        "checks": ["output_shows_hysteresis_window", "upward_and_downward_trip_points_are_separated"],
    },
    "vbr1_l1_propagation_delay_comparator": {
        "module": "cmp_delay(clk, vinn, vinp, out_n, out_p, lp, lm, vss, vdd)",
        "ports": [
            "`clk`: input electrical decision clock",
            "`vinn`, `vinp`: input electrical differential pair",
            "`out_n`, `out_p`: output electrical complementary decisions",
            "`lp`, `lm`: output electrical delay monitor nodes",
            "`vss`, `vdd`: electrical supply rails",
        ],
        "behavior": [
            "on rising `clk`, resolve the positive input polarity to `out_p` high",
            "model a longer clock-to-output delay as `abs(V(vinp)-V(vinn))` shrinks",
            "keep the delay bounded by public minimum and maximum delay parameters",
        ],
        "observables": ["time", "clk", "vinp", "vinn", "out_p"],
        "syntax": ["@(cross(", "transition("],
        "checks": ["output_goes_high_in_each_phase", "clk_to_output_delay_increases_as_diff_shrinks"],
    },
    "vbr1_l1_ramp_or_step_source": {
        "module": "bound_step_period_guard_ref(VDD, VSS, guard_out, phase_out)",
        "ports": [
            "`VDD`, `VSS`: electrical supply rails",
            "`guard_out`: output electrical guard pulse that marks the beginning of each period",
            "`phase_out`: output electrical normalized phase ramp within each period",
        ],
        "behavior": [
            "generate an 8 ns periodic phase ramp from 0 V toward `VDD`",
            "wrap the phase ramp at each new period",
            "drive `guard_out` high only during the first 1.5 ns of each period",
            "`$bound_step(...)` may be used to keep the narrow guard pulse observable, but the scored function is the ramp and guard timing",
        ],
        "observables": ["time", "guard_out", "phase_out"],
        "syntax": ["@(timer(", "$bound_step(", "transition("],
        "checks": ["periodic_phase_ramp_wraps", "guard_pulse_repeats_each_period", "guard_pulse_width_fraction"],
    },
    "vbr1_l1_serializer_frame_aligner": {
        "module": "serializer_frame_alignment_ref(vdd, vss, clk, load, din7, din6, din5, din4, din3, din2, din1, din0, sout, frame)",
        "ports": [
            "`vdd`, `vss`: electrical supply rails",
            "`clk`: input electrical shift clock",
            "`load`: input electrical word-load control",
            "`din7..din0`: input electrical parallel data word",
            "`sout`: output electrical serial data",
            "`frame`: output electrical first-bit frame marker",
        ],
        "behavior": [
            "latch the 8-bit input word when `load` is high on a clock edge",
            "shift data MSB-first on subsequent clock edges",
            "assert `frame` for the first serialized bit of each loaded word only",
        ],
        "observables": ["clk", "frame", "sout"],
        "syntax": ["@(cross(", "transition("],
        "checks": ["frame_pulse_present_for_each_loaded_word", "serialized_bits_match_word0xA5_then_0x3C", "frame_pulse_width_is_single_bit_window"],
    },
    "vbr1_l1_threshold_comparator": {
        "module": "comparator(vdd, vss, vinp, vinn, out_p)",
        "ports": [
            "`vdd`, `vss`: electrical supply rails",
            "`vinp`, `vinn`: input electrical differential pair",
            "`out_p`: output electrical single-ended decision",
        ],
        "behavior": [
            "drive `out_p` high when `V(vinp) > V(vinn)` by a visible margin",
            "drive `out_p` low when `V(vinp) < V(vinn)` by a visible margin",
            "use rail-referenced output levels and finite `transition(...)` edges",
        ],
        "observables": ["vinp", "vinn", "out_p"],
        "syntax": ["transition("],
        "checks": ["output_high_when_vinp_above_vinn", "output_low_when_vinp_below_vinn"],
    },
    "vbr1_l1_window_comparator_detector": {
        "module": "cross_hysteresis_window_ref(VDD, VSS, vin, out)",
        "ports": [
            "`VDD`, `VSS`: electrical supply rails",
            "`vin`: input electrical waveform",
            "`out`: output electrical window/hysteresis state",
        ],
        "behavior": [
            "start low",
            "switch high when `vin` rises above 0.6 V",
            "switch low when `vin` falls below 0.3 V",
            "hold state between thresholds and drive output with `transition(...)`",
        ],
        "observables": ["time", "vin", "out"],
        "syntax": ["@(cross(", "transition("],
        "checks": ["cross_hysteresis_window"],
    },
    "vbr1_l1_xor_phase_detector": {
        "module": "xor_phase_detector(vdd, vss, ref, div, pd_out)",
        "ports": [
            "`vdd`, `vss`: electrical supply rails",
            "`ref`, `div`: input electrical clock waveforms",
            "`pd_out`: output electrical XOR phase-detector waveform",
        ],
        "behavior": [
            "`pd_out` is high exactly when `ref` and `div` are at different logic levels",
            "update on both input clock edges",
            "the average high fraction should reflect the phase offset in the companion testbench",
        ],
        "observables": ["ref", "div", "pd_out"],
        "syntax": ["@(cross(", "transition("],
        "checks": ["xor_logic_matches_ref_div", "xor_pd_output_toggles", "xor_pd_duty_cycle_proportional_to_phase"],
    },
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_task_id(task: dict[str, object]) -> str:
    meta_path = ROOT / str(task["meta"])
    if not meta_path.exists():
        return str(task.get("historical_source_task_id", "unknown_e2e_source"))
    meta = read_json(meta_path)
    return str(meta.get("task_id") or meta.get("id") or task.get("historical_source_task_id", "unknown_e2e_source"))


def tb_gold_from_e2e(task: dict[str, object]) -> list[Path]:
    paths = [ROOT / str(path) for path in task.get("gold", [])]
    if not any(path.suffix == ".scs" for path in paths):
        return []
    return [path for path in paths if path.exists() and path.is_file()]


def gold_from_task(task: dict[str, object]) -> list[Path]:
    return [ROOT / str(path) for path in task.get("gold", []) if (ROOT / str(path)).exists()]


def has_suffix(paths: list[Path], suffix: str) -> bool:
    return any(path.suffix == suffix for path in paths)


def prompt_text(entry: dict[str, object], e2e_task: dict[str, object], scs_names: list[str]) -> str:
    return f"""# {entry['base_function']} Testbench Companion

Write a Spectre transient testbench for the `{entry['base_function']}` behavioral
Verilog-A release task. This is the testbench-generation companion for an
already materialized end-to-end task.

The testbench should instantiate the same behavioral DUT or system module used
by the corresponding end-to-end form, drive the public transient scenario, save
the observable waveform or metric signals, and preserve the EVAS/Spectre
validation contract.

Reference testbench artifact names: `{', '.join(scs_names)}`.
Domain: pure voltage-domain behavioral Verilog-A.

Public requirements:

- include a transient `tran` analysis
- save the public observables needed by the checker
- include or instantiate the Verilog-A behavioral module under test
- avoid transistor-level devices, AC/noise analysis, and current-domain
  solver assumptions

## Output Contract

Return exactly the Spectre testbench artifact. Do not include explanatory prose
outside the source file contents. Preserve the module names, ports, saved
waveform columns, and transient simulation contract specified above.
"""


def meta_payload(entry: dict[str, object], gold_files: list[Path]) -> dict[str, object]:
    task_id = f"{entry['release_entry_id']}_tb"
    return {
        "id": task_id,
        "task_id": task_id,
        "asset_type": "vabench_task",
        "benchmark": "vabench-release-v1",
        "release_entry_id": entry["release_entry_id"],
        "family": "tb-generation",
        "category": entry["category"],
        "domain": "voltage",
        "difficulty": "medium" if entry["level"] == "L1" else "hard",
        "expected_backend": "evas",
        "inputs": ["prompt.md"],
        "artifacts": [path.name for path in gold_files],
        "scoring": ["tb_compile", "sim_correct"],
        "source": "tb_companion_from_e2e",
    }


def checks_text() -> str:
    return """syntax:
  must_include:
    - "tran"
    - "save"
  must_not_include: []
tb_compile:
  backend: "evas"
sim_correct:
  checks:
    - "transient_analysis_present"
    - "public_observables_saved"
    - "dut_or_system_instantiated"
parity:
  reference: "spectre"
  status: "pending_until_evas_spectre_rerun"
  notes:
    - "TB companion copied from the release E2E gold and awaits fresh EVAS/Spectre dual rerun."
"""


def function_checked_dut_prompt(
    *,
    entry: dict[str, object],
    contract: dict[str, object],
    artifact_names: list[str],
) -> str:
    ports = "\n".join(f"- {item}" for item in contract["ports"])
    behavior = "\n".join(f"- {item}" for item in contract["behavior"])
    observables = "\n".join(f"- `{item}`" for item in contract["observables"])
    artifacts = ", ".join(f"`{name}`" for name in artifact_names)
    return f"""# {entry['base_function']} DUT

Write the Verilog-A DUT artifact(s) for `{entry['base_function']}`.

This is a function-checked DUT task, not a generic companion wrapper. The
public contract below defines the exact module interface, voltage-domain
behavior, and waveform observables used by the release checker.

Reference artifact name(s): {artifacts}.
Domain: pure voltage-domain behavioral Verilog-A.

## Module Contract

- Declaration: `{contract['module']}`

Ports:

{ports}

## Behavioral Contract

{behavior}

## Public Evaluation Observables

The companion validation testbench saves these waveform columns:

{observables}

## Output Contract

Return exactly the requested Verilog-A DUT artifact(s). Do not include
explanatory prose outside the source file contents. Preserve the module name,
port order, port directions, electrical discipline, and public waveform
observable names described above.
"""


def companion_prompt_text(
    *,
    entry: dict[str, object],
    target_form: str,
    source_form: str,
    artifact_names: list[str],
) -> str:
    contract = DUT_FUNCTION_CONTRACTS.get(str(entry["release_entry_id"]))
    if target_form == "dut" and contract is not None:
        return function_checked_dut_prompt(entry=entry, contract=contract, artifact_names=artifact_names)

    if target_form == "dut":
        task_line = "Write the Verilog-A DUT for this behavioral release task."
        artifact = "the Verilog-A DUT artifact"
        requirements = [
            "preserve the public module name and ports used by the companion validation testbench",
            "implement the pure voltage-domain behavioral function",
            "drive public outputs with bounded voltage-domain behavior",
        ]
    elif target_form == "tb":
        task_line = "Write a Spectre transient testbench for this behavioral release task."
        artifact = "the Spectre testbench artifact"
        requirements = [
            "include a transient `tran` analysis",
            "save the public observables needed by the checker",
            "include or instantiate the behavioral module under test",
        ]
    else:
        task_line = "Write both the Verilog-A behavioral module and a Spectre transient testbench."
        artifact = "the Verilog-A module and Spectre testbench artifacts"
        requirements = [
            "include the behavioral Verilog-A module",
            "include a transient `tran` analysis",
            "save the public observables needed by the checker",
        ]
    bullet_requirements = "\n".join(f"- {item}" for item in requirements)
    return f"""# {entry['base_function']} {target_form.upper()} Companion

{task_line}

This task form is materialized from the already source-controlled `{source_form}`
release gold for `{entry['base_function']}`. It exists to make the public
benchmark split complete without inventing a new circuit kernel or a fake
bugfix.

Reference artifact names: `{', '.join(artifact_names)}`.
Domain: pure voltage-domain behavioral Verilog-A.

Public requirements:

{bullet_requirements}
- avoid transistor-level devices, AC/noise analysis, and current-domain
  solver assumptions

## Output Contract

Return exactly {artifact}. Do not include explanatory prose outside the source
file contents. Preserve the module names, ports, saved waveform columns, and
transient simulation contract specified above.
"""


def companion_meta_payload(
    *,
    entry: dict[str, object],
    target_form: str,
    source_form: str,
    gold_files: list[Path],
) -> dict[str, object]:
    task_id = f"{entry['release_entry_id']}_{target_form}"
    scoring = {
        "dut": ["dut_compile", "tb_compile", "sim_correct"],
        "tb": ["tb_compile", "sim_correct"],
        "e2e": ["dut_compile", "tb_compile", "sim_correct"],
    }[target_form]
    return {
        "id": task_id,
        "task_id": task_id,
        "asset_type": "vabench_task",
        "benchmark": "vabench-release-v1",
        "release_entry_id": entry["release_entry_id"],
        "family": FAMILY_BY_FORM[target_form],
        "category": entry["category"],
        "domain": "voltage",
        "difficulty": "medium" if entry["level"] == "L1" else "hard",
        "expected_backend": "evas",
        "inputs": ["prompt.md"],
        "artifacts": [path.name for path in gold_files],
        "scoring": scoring,
        "source": f"{target_form}_companion_from_{source_form}",
    }


def function_checked_dut_checks_text(contract: dict[str, object], source_form: str) -> str:
    include_lines = "\n".join(f'    - "{token}"' for token in contract["syntax"])
    checks = "\n".join(f'    - "{item}"' for item in contract["checks"])
    observables = "\n".join(f'    - "{item}"' for item in contract["observables"])
    return f"""syntax:
  must_include:
{include_lines}
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
  status: "pending_until_evas_spectre_rerun"
  notes:
    - "Function-checked DUT companion copied from release {source_form} gold and awaits fresh EVAS/Spectre dual rerun."
"""


def companion_checks_text(entry: dict[str, object], target_form: str, source_form: str) -> str:
    contract = DUT_FUNCTION_CONTRACTS.get(str(entry["release_entry_id"]))
    if target_form == "dut" and contract is not None:
        return function_checked_dut_checks_text(contract, source_form)

    must_include = {
        "dut": ["module"],
        "tb": ["tran", "save"],
        "e2e": ["module", "tran", "save"],
    }[target_form]
    include_lines = "\n".join(f'    - "{token}"' for token in must_include)
    must_not = "[]"
    if target_form in {"dut", "e2e"}:
        must_not = '\n    - "I("\n    - "ddt("'
    checks = {
        "dut": ["behavioral_module_present", "companion_testbench_available", "voltage_domain_outputs"],
        "tb": ["transient_analysis_present", "public_observables_saved", "dut_or_system_instantiated"],
        "e2e": ["behavioral_module_present", "transient_analysis_present", "public_observables_saved"],
    }[target_form]
    behavior = "\n".join(f'    - "{item}"' for item in checks)
    return f"""syntax:
  must_include:
{include_lines}
  must_not_include:{must_not}
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
    - "{target_form} companion copied from release {source_form} gold and awaits fresh EVAS/Spectre dual rerun."
"""


def source_form_for(entry: dict[str, object], form: str) -> dict[str, object] | None:
    for task in entry.get("release_tasks", []):
        if isinstance(task, dict) and task.get("form") == form:
            return task
    return None


def copied_companion_gold(target_form: str, source_task: dict[str, object]) -> list[Path]:
    sources = gold_from_task(source_task)
    if target_form == "dut" and not has_suffix(sources, ".va"):
        return []
    if target_form == "tb" and not has_suffix(sources, ".scs"):
        return []
    if target_form == "e2e" and not (has_suffix(sources, ".va") and has_suffix(sources, ".scs")):
        return []
    return sources


def write_generic_companion(
    *,
    entry_path: Path,
    entry: dict[str, object],
    target_form: str,
    source_form: str,
    source_task: dict[str, object],
) -> bool:
    missing_forms = list(entry.get("missing_forms", []))
    if target_form not in missing_forms:
        return False
    if any(task.get("form") == target_form for task in entry.get("release_tasks", [])):
        return False

    gold_sources = copied_companion_gold(target_form, source_task)
    if not gold_sources:
        return False

    entry_dir = entry_path.parent
    form_dir = entry_dir / "forms" / target_form
    gold_dir = form_dir / "gold"
    if form_dir.exists():
        shutil.rmtree(form_dir)
    gold_dir.mkdir(parents=True, exist_ok=True)

    copied_gold: list[Path] = []
    for source in gold_sources:
        dest = gold_dir / source.name
        shutil.copy2(source, dest)
        copied_gold.append(dest)

    source_id = source_task_id(source_task)
    artifact_names = [path.name for path in copied_gold]
    (form_dir / "prompt.md").write_text(
        companion_prompt_text(
            entry=entry,
            target_form=target_form,
            source_form=source_form,
            artifact_names=artifact_names,
        ),
        encoding="utf-8",
    )
    write_json(
        form_dir / "meta.json",
        companion_meta_payload(
            entry=entry,
            target_form=target_form,
            source_form=source_form,
            gold_files=copied_gold,
        ),
    )
    (form_dir / "checks.yaml").write_text(companion_checks_text(entry, target_form, source_form), encoding="utf-8")
    source_label = f"{target_form}_companion_from_{source_form}:{source_id}"
    (form_dir / "SOURCE_TASK.md").write_text(
        "\n".join(
            [
                f"# {target_form.upper()} Companion From {source_form.upper()}: {entry['release_entry_id']}",
                "",
                f"- Source form: `{source_task['release_path']}`",
                f"- Source task id: `{source_id}`",
                "- EVAS/Spectre status: pending fresh dual rerun",
                "",
                "This companion form is materialized by promoting existing",
                f"release `{source_form}` gold assets into the `{target_form}`",
                "public task split. It is not imported as historical",
                "certification evidence.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    release_task = {
        "form": target_form,
        "release_path": rel(form_dir),
        "prompt": rel(form_dir / "prompt.md"),
        "meta": rel(form_dir / "meta.json"),
        "checks": rel(form_dir / "checks.yaml"),
        "gold": [rel(path) for path in sorted(copied_gold)],
        "asset_materialized": True,
        "historical_dual_expected": False,
        "source_path": source_label,
    }
    source_task_record = {
        "form": target_form,
        "source_path": source_label,
        "prompt": True,
        "meta": True,
        "checks": True,
        "gold": True,
        "asset_complete": True,
        "checks_has_sim_correct": True,
        "checks_has_parity": True,
        "checks_normalized_for_release": False,
    }

    entry.setdefault("source_tasks", []).append(source_task_record)
    entry.setdefault("release_tasks", []).append(release_task)
    entry["release_tasks"] = sorted(entry["release_tasks"], key=lambda task: FORM_ORDER.index(task["form"]))
    entry["source_tasks"] = sorted(entry["source_tasks"], key=lambda task: FORM_ORDER.index(task["form"]))
    entry["missing_forms"] = [form for form in missing_forms if form != target_form]
    if not entry["missing_forms"]:
        entry["release_blockers"] = [
            blocker for blocker in entry.get("release_blockers", []) if blocker != "missing_required_forms"
        ]
    write_json(entry_path, entry)
    return True


def write_tb_companion(entry_path: Path, entry: dict[str, object], e2e_task: dict[str, object]) -> bool:
    missing_forms = list(entry.get("missing_forms", []))
    if "tb" not in missing_forms:
        return False
    if any(task.get("form") == "tb" for task in entry.get("release_tasks", [])):
        return False

    gold_sources = tb_gold_from_e2e(e2e_task)
    if not gold_sources:
        return False

    entry_dir = entry_path.parent
    form_dir = entry_dir / "forms" / "tb"
    gold_dir = form_dir / "gold"
    if form_dir.exists():
        shutil.rmtree(form_dir)
    gold_dir.mkdir(parents=True, exist_ok=True)

    copied_gold: list[Path] = []
    for source in gold_sources:
        dest = gold_dir / source.name
        shutil.copy2(source, dest)
        copied_gold.append(dest)

    scs_names = [path.name for path in copied_gold if path.suffix == ".scs"]
    (form_dir / "prompt.md").write_text(prompt_text(entry, e2e_task, scs_names), encoding="utf-8")
    write_json(form_dir / "meta.json", meta_payload(entry, copied_gold))
    (form_dir / "checks.yaml").write_text(checks_text(), encoding="utf-8")
    (form_dir / "SOURCE_TASK.md").write_text(
        "\n".join(
            [
                f"# TB Companion From E2E: {entry['release_entry_id']}",
                "",
                f"- Source E2E form: `{e2e_task['release_path']}`",
                f"- Source E2E task id: `{source_task_id(e2e_task)}`",
                "- EVAS/Spectre status: pending fresh dual rerun",
                "",
                "This tb-generation form is materialized by promoting the",
                "release E2E Spectre testbench into its own public testbench",
                "task. It is not imported as historical certification evidence.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    release_task = {
        "form": "tb",
        "release_path": rel(form_dir),
        "prompt": rel(form_dir / "prompt.md"),
        "meta": rel(form_dir / "meta.json"),
        "checks": rel(form_dir / "checks.yaml"),
        "gold": [rel(path) for path in sorted(copied_gold)],
        "asset_materialized": True,
        "historical_dual_expected": False,
        "source_path": f"tb_companion_from_e2e:{source_task_id(e2e_task)}",
    }
    source_task = {
        "form": "tb",
        "source_path": release_task["source_path"],
        "prompt": True,
        "meta": True,
        "checks": True,
        "gold": True,
        "asset_complete": True,
        "checks_has_sim_correct": True,
        "checks_has_parity": True,
        "checks_normalized_for_release": False,
    }

    entry.setdefault("source_tasks", []).append(source_task)
    entry.setdefault("release_tasks", []).append(release_task)
    entry["release_tasks"] = sorted(entry["release_tasks"], key=lambda task: ["dut", "tb", "bugfix", "e2e"].index(task["form"]))
    entry["source_tasks"] = sorted(entry["source_tasks"], key=lambda task: ["dut", "tb", "bugfix", "e2e"].index(task["form"]))
    entry["missing_forms"] = [form for form in missing_forms if form != "tb"]
    if not entry["missing_forms"]:
        entry["release_blockers"] = [
            blocker for blocker in entry.get("release_blockers", []) if blocker != "missing_required_forms"
        ]
    write_json(entry_path, entry)
    return True


def materialize_tb_companions() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for entry_path in sorted(TASKS_ROOT.glob("*/release_entry.json")):
        entry = read_json(entry_path)
        e2e_task = next((task for task in entry.get("release_tasks", []) if task.get("form") == "e2e"), None)
        if not isinstance(e2e_task, dict):
            e2e_task = None
        if isinstance(e2e_task, dict) and write_tb_companion(entry_path, entry, e2e_task):
            rows.append(
                {
                    "entry_id": str(entry["release_entry_id"]),
                    "base_function": str(entry["base_function"]),
                    "form": "tb",
                    "source_e2e": str(e2e_task["release_path"]),
                }
            )
        entry = read_json(entry_path)
        e2e_task = source_form_for(entry, "e2e")
        dut_task = source_form_for(entry, "dut")
        if isinstance(e2e_task, dict) and write_generic_companion(
            entry_path=entry_path,
            entry=entry,
            target_form="dut",
            source_form="e2e",
            source_task=e2e_task,
        ):
            rows.append(
                {
                    "entry_id": str(entry["release_entry_id"]),
                    "base_function": str(entry["base_function"]),
                    "form": "dut",
                    "source_e2e": str(e2e_task["release_path"]),
                }
            )
        entry = read_json(entry_path)
        dut_task = source_form_for(entry, "dut")
        if isinstance(dut_task, dict):
            for target_form in ("tb", "e2e"):
                if write_generic_companion(
                    entry_path=entry_path,
                    entry=entry,
                    target_form=target_form,
                    source_form="dut",
                    source_task=dut_task,
                ):
                    rows.append(
                        {
                            "entry_id": str(entry["release_entry_id"]),
                            "base_function": str(entry["base_function"]),
                            "form": target_form,
                            "source_e2e": str(dut_task["release_path"]),
                        }
                    )
                    entry = read_json(entry_path)
    return rows


def update_selected_manifest(companions: list[dict[str, str]]) -> None:
    if not companions:
        return
    companion_forms: dict[str, set[str]] = {}
    for row in companions:
        companion_forms.setdefault(row["entry_id"], set()).add(row["form"])
    rows = read_csv(SELECTED_MANIFEST_CSV)
    for row in rows:
        forms_to_add = companion_forms.get(row["entry_id"])
        if not forms_to_add:
            continue
        forms = [form for form in row["forms_materialized"].split("|") if form]
        for form in forms_to_add:
            if form not in forms:
                forms.append(form)
        missing = [form for form in row["missing_forms"].split("|") if form and form not in forms_to_add]
        row["forms_materialized"] = "|".join(sorted(forms, key=lambda item: FORM_ORDER.index(item)))
        row["missing_forms"] = "|".join(missing)
        suffix = "companion forms generated from existing release gold"
        row["notes"] = row["notes"] if suffix in row["notes"] else f"{row['notes']}; {suffix}"
    write_csv(SELECTED_MANIFEST_CSV, rows)

    lines = [
        "# vaBench Release Selected Manifest",
        "",
        f"Date: {date.today().isoformat()}",
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
        f"| entries with copied or designed source assets | {sum(1 for row in rows if row['forms_materialized'])} |",
        f"| generated companion forms | {len(companions)} |",
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
    companions = materialize_tb_companions()
    update_selected_manifest(companions)
    print(f"materialized companion forms from existing release gold: {len(companions)}")


if __name__ == "__main__":
    main()
