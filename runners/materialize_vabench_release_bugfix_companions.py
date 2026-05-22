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
SELECTED_MANIFEST_CSV = ROOT / "docs" / "VABENCH_RELEASE_SELECTED_MANIFEST.csv"
SELECTED_MANIFEST_MD = ROOT / "docs" / "VABENCH_RELEASE_SELECTED_MANIFEST.md"
SEED_MANIFEST_CSV = ROOT / "docs" / "VABENCH_RELEASE_SEED_MANIFEST.csv"
SEED_MANIFEST_MD = ROOT / "docs" / "VABENCH_RELEASE_SEED_MANIFEST.md"
FORM_ORDER = ["dut", "tb", "bugfix", "e2e"]


@dataclass(frozen=True)
class BugfixSpec:
    entry_id: str
    source_form: str
    fixed_va_name: str
    tb_name: str
    bug_summary: str
    behavior_checks: tuple[str, ...]
    replacements: tuple[tuple[str, str], ...]
    extra_gold_names: tuple[str, ...] = ()
    tb_replacements: tuple[tuple[str, str], ...] = ()


BUGFIX_SPECS: dict[str, BugfixSpec] = {
    "vbr1_l1_bang_bang_phase_detector": BugfixSpec(
        entry_id="vbr1_l1_bang_bang_phase_detector",
        source_form="dut",
        fixed_va_name="bbpd_ref.va",
        tb_name="tb_bbpd_ref.scs",
        bug_summary="The buggy bang-bang phase detector swaps the UP and DOWN output drives.",
        behavior_checks=("up_pulse_when_data_lags_clock", "down_pulse_when_data_leads_clock", "outputs_clear_on_next_clock_edge"),
        replacements=(
            ("V(up)   <+ transition(up_state ? vdd : 0.0, td, trf, trf);", "V(up)   <+ transition(down_state ? vdd : 0.0, td, trf, trf);"),
            ("V(down) <+ transition(down_state ? vdd : 0.0, td, trf, trf);", "V(down) <+ transition(up_state ? vdd : 0.0, td, trf, trf);"),
        ),
    ),
    "vbr1_l1_capacitive_weighted_sar_feedback_dac": BugfixSpec(
        entry_id="vbr1_l1_capacitive_weighted_sar_feedback_dac",
        source_form="dut",
        fixed_va_name="cdac_cal.va",
        tb_name="tb_cdac_cal_ref.scs",
        bug_summary="The buggy feedback DAC ignores the calibration bits when computing the differential output.",
        behavior_checks=("binary_code_sets_nominal_dac_level", "calibration_bits_shift_feedback_level", "differential_outputs_move_complementarily"),
        replacements=(("code + 32 * cal", "code"),),
    ),
    "vbr1_l1_threshold_comparator": BugfixSpec(
        entry_id="vbr1_l1_threshold_comparator",
        source_form="dut",
        fixed_va_name="comparator.va",
        tb_name="tb_comparator_ref.scs",
        bug_summary="The buggy comparator drives the output with reversed polarity.",
        behavior_checks=("output_low_before_threshold", "output_high_after_threshold", "polarity_matches_vinp_minus_vinn"),
        replacements=(
            ("out_level = (V(VINP) > V(VINN)) ? V(VDD) : V(VSS);", "out_level = (V(VINP) > V(VINN)) ? V(VSS) : V(VDD);"),
            ("out_level = V(VDD);", "__TMP_CMP_HIGH__ = V(VDD);"),
            ("out_level = V(VSS);", "out_level = V(VDD);"),
            ("__TMP_CMP_HIGH__ = V(VDD);", "out_level = V(VSS);"),
        ),
    ),
    "vbr1_l1_clock_divider": BugfixSpec(
        entry_id="vbr1_l1_clock_divider",
        source_form="dut",
        fixed_va_name="clk_divider_ref.va",
        tb_name="tb_clk_divider_ref.scs",
        bug_summary="The buggy clock divider uses the low segment length for both halves of an odd divide ratio.",
        behavior_checks=("ratio_code_selects_output_period", "odd_ratio_uses_floor_and_ceil_half_cycles", "lock_asserts_after_complete_output_period"),
        replacements=(("high_len = ratio - low_len;", "high_len = low_len;"),),
    ),
    "vbr1_l1_clocked_comparator": BugfixSpec(
        entry_id="vbr1_l1_clocked_comparator",
        source_form="dut",
        fixed_va_name="cmp_strongarm.va",
        tb_name="tb_cmp_strongarm_ref.scs",
        bug_summary="The buggy clocked comparator never asserts the negative-side decision output.",
        behavior_checks=("positive_input_difference_asserts_dcmpp", "negative_input_difference_asserts_dcmpn", "outputs_reset_when_clock_falls"),
        replacements=(("xoutn = (v_diff_offset < 0);", "xoutn = 0;"),),
    ),
    "vbr1_l1_differential_output_driver": BugfixSpec(
        entry_id="vbr1_l1_differential_output_driver",
        source_form="dut",
        fixed_va_name="differential_voltage_output_ref.va",
        tb_name="tb_differential_voltage_output_ref.scs",
        bug_summary="The buggy differential output driver ignores the enable input and continues driving a nonzero differential output while disabled.",
        behavior_checks=("disabled_window_returns_to_common_mode", "enabled_output_polarity_tracks_din", "output_common_mode_stays_bounded"),
        replacements=(("if (V(en, VSS) > vth) begin", "if (1) begin"),),
    ),
    "vbr1_l1_dwa_dem_encoder": BugfixSpec(
        entry_id="vbr1_l1_dwa_dem_encoder",
        source_form="dut",
        fixed_va_name="dwa_ptr_gen.va",
        tb_name="tb_dwa_ptr_gen_ref.scs",
        bug_summary="The buggy DWA/DEM encoder computes the cell mask but never advances the rotating pointer.",
        behavior_checks=("pointer_advances_by_input_code", "cell_enable_mask_wraps_around_sixteen_elements", "pointer_output_is_one_hot"),
        replacements=(("start_idx_q = (start_idx_q + msb_count_q) % 16;", "start_idx_q = start_idx_q;"),),
        extra_gold_names=("v2b_4b.va",),
        tb_replacements=(('ahdl_include "v2b_4b.va"\nahdl_include "dwa_ptr_gen.va"', 'ahdl_include "dwa_ptr_gen.va"\nahdl_include "v2b_4b.va"'),),
    ),
    "vbr1_l1_clocked_sample_and_hold": BugfixSpec(
        entry_id="vbr1_l1_clocked_sample_and_hold",
        source_form="dut",
        fixed_va_name="sample_hold.va",
        tb_name="tb_sample_hold_ref.scs",
        bug_summary="The buggy sample-and-hold ignores the input sample and always holds zero.",
        behavior_checks=("samples_on_rising_clock_edge", "output_holds_between_edges", "sample_value_tracks_input_at_edge"),
        replacements=(("held = V(IN);", "held = 0.0;"),),
    ),
    "vbr1_l1_clocked_adc_quantizer": BugfixSpec(
        entry_id="vbr1_l1_clocked_adc_quantizer",
        source_form="dut",
        fixed_va_name="flash_adc_3b.va",
        tb_name="tb_flash_adc_3b_ref.scs",
        bug_summary="The buggy quantizer saturates at code 6 and never emits the top ADC code.",
        behavior_checks=("all_eight_codes_reachable", "code_monotonic_with_input", "top_code_saturates_at_7"),
        replacements=(("if (code > 7) code = 7;", "if (code > 6) code = 6;"),),
    ),
    "vbr1_l1_hysteresis_comparator": BugfixSpec(
        entry_id="vbr1_l1_hysteresis_comparator",
        source_form="dut",
        fixed_va_name="cmp_hysteresis.va",
        tb_name="tb_cmp_hysteresis_ref.scs",
        bug_summary="The buggy comparator collapses the hysteresis window to a zero-threshold comparator.",
        behavior_checks=("rising_trip_uses_positive_hysteresis_threshold", "falling_trip_uses_negative_hysteresis_threshold", "output_state_retains_memory_inside_window"),
        replacements=(
            ("@(cross(diff - 0.5 * vhys, +1))", "@(cross(diff, +1))"),
            ("@(cross(diff + 0.5 * vhys, -1))", "@(cross(diff, -1))"),
        ),
    ),
    "vbr1_l1_lfsr_prbs_generator": BugfixSpec(
        entry_id="vbr1_l1_lfsr_prbs_generator",
        source_form="dut",
        fixed_va_name="prbs7_ref.va",
        tb_name="tb_prbs7_ref.scs",
        bug_summary="The buggy PRBS generator uses the wrong feedback tap and shortens the intended sequence.",
        behavior_checks=("reset_loads_nonzero_seed", "enabled_clock_edges_advance_lfsr_state", "feedback_uses_prbs7_taps"),
        replacements=(("feedback = state_6_i ^ state_5_i;", "feedback = state_6_i ^ state_4_i;"),),
    ),
    "vbr1_l1_pfd_small_phase_error_response": BugfixSpec(
        entry_id="vbr1_l1_pfd_small_phase_error_response",
        source_form="dut",
        fixed_va_name="pfd_updn.va",
        tb_name="tb_pfd_small_phase_ref.scs",
        bug_summary="The buggy PFD omits the mutual reset path when both REF and DIV edges have arrived.",
        behavior_checks=("ref_lead_asserts_up", "div_lead_asserts_dn", "opposite_edge_resets_both_outputs"),
        replacements=(
            ("if (dn_state) begin", "if (0) begin"),
            ("if (up_state) begin", "if (0) begin"),
        ),
    ),
    "vbr1_l1_propagation_delay_comparator": BugfixSpec(
        entry_id="vbr1_l1_propagation_delay_comparator",
        source_form="dut",
        fixed_va_name="cmp_delay.va",
        tb_name="tb_cmp_delay_ref.scs",
        bug_summary="The buggy propagation-delay comparator removes the input-amplitude dependent regeneration delay.",
        behavior_checks=("comparator_polarity_matches_input_difference", "small_input_difference_has_larger_delay", "delay_is_clamped_between_min_and_max"),
        replacements=(("td = td_0 + tau * ln(vdd / vdiff_eff);", "td = td_0;"),),
        extra_gold_names=("edge_interval_timer.va",),
    ),
    "vbr1_l1_digital_phase_accumulator_with_modulo_wrap": BugfixSpec(
        entry_id="vbr1_l1_digital_phase_accumulator_with_modulo_wrap",
        source_form="dut",
        fixed_va_name="phase_accumulator_timer_wrap_ref.va",
        tb_name="tb_phase_accumulator_timer_wrap_ref.scs",
        bug_summary="The buggy accumulator omits modulo wrap after the phase reaches one cycle.",
        behavior_checks=("phase_advances_by_step", "phase_wraps_modulo_one", "clock_state_follows_wrapped_phase"),
        replacements=(("if (phase_q >= 1.0) phase_q = phase_q - 1.0;", "if (phase_q >= 1.0) phase_q = phase_q;"),),
    ),
    "vbr1_l1_serializer_frame_aligner": BugfixSpec(
        entry_id="vbr1_l1_serializer_frame_aligner",
        source_form="dut",
        fixed_va_name="serializer_frame_alignment_ref.va",
        tb_name="tb_serializer_frame_alignment_ref.scs",
        bug_summary="The buggy serializer emits the loaded word in the reverse bit order.",
        behavior_checks=("load_captures_parallel_word", "serial_output_emits_msb_first", "frame_pulse_marks_first_serial_bit"),
        replacements=(("sout_val = (((shreg >> bit_idx) & 1) == 1) ? vdd_now : 0.0;", "sout_val = (((shreg >> (7 - bit_idx)) & 1) == 1) ? vdd_now : 0.0;"),),
    ),
    "vbr1_l1_vco_phase_integrator": BugfixSpec(
        entry_id="vbr1_l1_vco_phase_integrator",
        source_form="dut",
        fixed_va_name="vco_phase_integrator.va",
        tb_name="tb_vco_phase_integrator_ref.scs",
        bug_summary="The buggy VCO phase integrator wraps phase but never toggles the clock output on wrap.",
        behavior_checks=("phase_increments_with_control_voltage", "phase_wraps_modulo_one", "clock_toggles_when_phase_wraps"),
        replacements=(("c=1-c;", "c=c;"),),
    ),
    "vbr1_l1_window_comparator_detector": BugfixSpec(
        entry_id="vbr1_l1_window_comparator_detector",
        source_form="dut",
        fixed_va_name="cross_hysteresis_window_ref.va",
        tb_name="tb_cross_hysteresis_window_ref.scs",
        bug_summary="The buggy window comparator collapses the falling threshold onto the rising threshold.",
        behavior_checks=("rising_crossing_uses_upper_threshold", "falling_crossing_uses_lower_threshold", "output_retains_state_between_thresholds"),
        replacements=(("@(cross(V(vin, VSS) - vth_fall, -1))", "@(cross(V(vin, VSS) - vth_rise, -1))"),),
    ),
    "vbr1_l1_xor_phase_detector": BugfixSpec(
        entry_id="vbr1_l1_xor_phase_detector",
        source_form="dut",
        fixed_va_name="xor_phase_detector_ref.va",
        tb_name="tb_xor_phase_detector_ref.scs",
        bug_summary="The buggy phase detector implements XNOR instead of XOR.",
        behavior_checks=("output_high_when_inputs_differ", "output_low_when_inputs_match", "average_output_tracks_phase_difference"),
        replacements=(("xor_out = ref_hi ^ div_hi;", "xor_out = (ref_hi == div_hi) ? 1 : 0;"),),
    ),
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


def apply_replacements(text: str, replacements: tuple[tuple[str, str], ...], *, entry_id: str) -> str:
    updated = text
    for old, new in replacements:
        if old not in updated:
            raise RuntimeError(f"{entry_id}: replacement source not found: {old!r}")
        updated = updated.replace(old, new)
    if updated == text:
        raise RuntimeError(f"{entry_id}: mutation did not change source")
    return updated


def source_file(entry_id: str, form: str, name: str) -> Path:
    path = TASKS_ROOT / entry_id / "forms" / form / "gold" / name
    if not path.exists():
        raise RuntimeError(f"{entry_id}: source file missing: {rel(path)}")
    return path


def prompt_text(entry: dict[str, object], spec: BugfixSpec) -> str:
    checks = "\n".join(f"- {item}" for item in spec.behavior_checks)
    return f"""# {entry['base_function']} Bugfix

Repair the supplied buggy Verilog-A implementation for `{entry['base_function']}`.

Bug to fix: {spec.bug_summary}

The fixed implementation must preserve the public module name and ports used by
the reference Spectre testbench. Domain: pure voltage-domain behavioral
Verilog-A. Do not use current contributions, transistor-level devices,
AC/noise analysis, or KCL/KVL solving assumptions.

Public behavior checks:

{checks}

## Output Contract

Return exactly the repaired Verilog-A artifact. Do not include explanatory
prose outside the source file contents. Preserve the module names, ports, saved
waveform columns, and transient simulation contract used by the companion
testbench.
"""


def meta_payload(entry: dict[str, object], spec: BugfixSpec) -> dict[str, object]:
    task_id = f"{entry['release_entry_id']}_bugfix"
    artifacts = ["dut_buggy.va", "dut_fixed.va", spec.tb_name, *spec.extra_gold_names]
    return {
        "id": task_id,
        "task_id": task_id,
        "asset_type": "vabench_task",
        "benchmark": "vabench-release-v1",
        "release_entry_id": entry["release_entry_id"],
        "family": "bugfix",
        "category": entry["category"],
        "domain": "voltage",
        "difficulty": "medium" if entry["level"] == "L1" else "hard",
        "expected_backend": "evas",
        "inputs": ["prompt.md", "gold/dut_buggy.va"],
        "artifacts": artifacts,
        "scoring": ["dut_compile", "tb_compile", "sim_correct"],
        "behavior_checks": list(spec.behavior_checks),
        "source": f"bugfix_companion_from_{spec.source_form}",
    }


def checks_text(spec: BugfixSpec) -> str:
    behavior = "\n".join(f'    - "{item}"' for item in spec.behavior_checks)
    return f"""syntax:
  must_include:
    - "transition("
  must_not_include:
    - "I("
    - "ddt("
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
    - "Bugfix companion has explicit buggy/fixed Verilog-A sources and awaits fresh EVAS/Spectre dual rerun."
"""


def write_bugfix(entry_path: Path, spec: BugfixSpec) -> bool:
    entry = read_json(entry_path)
    missing_forms = list(entry.get("missing_forms", []))
    if "bugfix" not in missing_forms:
        return False
    if any(task.get("form") == "bugfix" for task in entry.get("release_tasks", [])):
        return False

    fixed_src = source_file(spec.entry_id, spec.source_form, spec.fixed_va_name)
    tb_src = source_file(spec.entry_id, spec.source_form, spec.tb_name)
    extra_srcs = [source_file(spec.entry_id, spec.source_form, name) for name in spec.extra_gold_names]
    fixed_text = fixed_src.read_text(encoding="utf-8")
    buggy_text = apply_replacements(fixed_text, spec.replacements, entry_id=spec.entry_id)
    tb_text = tb_src.read_text(encoding="utf-8")
    if spec.tb_replacements:
        tb_text = apply_replacements(tb_text, spec.tb_replacements, entry_id=f"{spec.entry_id}:{spec.tb_name}")

    form_dir = entry_path.parent / "forms" / "bugfix"
    gold_dir = form_dir / "gold"
    if form_dir.exists():
        shutil.rmtree(form_dir)
    gold_dir.mkdir(parents=True, exist_ok=True)
    (gold_dir / "dut_fixed.va").write_text(fixed_text, encoding="utf-8")
    (gold_dir / "dut_buggy.va").write_text(buggy_text, encoding="utf-8")
    (gold_dir / spec.tb_name).write_text(tb_text, encoding="utf-8")
    for extra_src in extra_srcs:
        shutil.copy2(extra_src, gold_dir / extra_src.name)
    (form_dir / "prompt.md").write_text(prompt_text(entry, spec), encoding="utf-8")
    write_json(form_dir / "meta.json", meta_payload(entry, spec))
    (form_dir / "checks.yaml").write_text(checks_text(spec), encoding="utf-8")
    (form_dir / "SOURCE_TASK.md").write_text(
        "\n".join(
            [
                f"# Bugfix Companion: {entry['release_entry_id']}",
                "",
                f"- Fixed source: `{rel(fixed_src)}`",
                f"- Reference testbench: `{rel(tb_src)}`",
                *[f"- Companion dependency: `{rel(extra_src)}`" for extra_src in extra_srcs],
                f"- Bug: {spec.bug_summary}",
                "- EVAS/Spectre status: pending fresh dual rerun",
                "",
                "This bugfix form was created only where a single-cause badcase",
                "could be reconstructed from existing release gold. It is not",
                "imported as historical certification evidence.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    release_task = {
        "form": "bugfix",
        "release_path": rel(form_dir),
        "prompt": rel(form_dir / "prompt.md"),
        "meta": rel(form_dir / "meta.json"),
        "checks": rel(form_dir / "checks.yaml"),
        "gold": [
            rel(gold_dir / "dut_buggy.va"),
            rel(gold_dir / "dut_fixed.va"),
            rel(gold_dir / spec.tb_name),
            *[rel(gold_dir / name) for name in spec.extra_gold_names],
        ],
        "asset_materialized": True,
        "historical_dual_expected": False,
        "source_path": f"bugfix_companion_from_{spec.source_form}:{spec.fixed_va_name}",
    }
    source_task = {
        "form": "bugfix",
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
    entry.setdefault("release_tasks", []).append(release_task)
    entry.setdefault("source_tasks", []).append(source_task)
    entry["release_tasks"] = sorted(entry["release_tasks"], key=lambda task: FORM_ORDER.index(task["form"]))
    entry["source_tasks"] = sorted(entry["source_tasks"], key=lambda task: FORM_ORDER.index(task["form"]))
    entry["missing_forms"] = [form for form in missing_forms if form != "bugfix"]
    if not entry["missing_forms"]:
        entry["release_blockers"] = [
            blocker for blocker in entry.get("release_blockers", []) if blocker != "missing_required_forms"
        ]
    write_json(entry_path, entry)
    return True


def materialize_bugfixes() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for entry_id, spec in sorted(BUGFIX_SPECS.items()):
        entry_path = TASKS_ROOT / entry_id / "release_entry.json"
        if not entry_path.exists():
            continue
        if write_bugfix(entry_path, spec):
            entry = read_json(entry_path)
            rows.append(
                {
                    "entry_id": entry_id,
                    "base_function": str(entry["base_function"]),
                    "form": "bugfix",
                    "source": f"{spec.source_form}/{spec.fixed_va_name}",
                    "bug": spec.bug_summary,
                }
            )
    return rows


def update_selected_manifest(materialized: list[dict[str, str]]) -> None:
    if not materialized:
        return
    materialized_ids = {row["entry_id"] for row in materialized}
    rows = read_csv(SELECTED_MANIFEST_CSV)
    for row in rows:
        if row["entry_id"] not in materialized_ids:
            continue
        forms = [form for form in row["forms_materialized"].split("|") if form]
        if "bugfix" not in forms:
            forms.append("bugfix")
        missing = [form for form in row["missing_forms"].split("|") if form and form != "bugfix"]
        row["forms_materialized"] = "|".join(sorted(forms, key=lambda item: FORM_ORDER.index(item)))
        row["missing_forms"] = "|".join(missing)
        suffix = "true-bugfix companion generated from existing release gold"
        row["notes"] = row["notes"] if suffix in row["notes"] else f"{row['notes']}; {suffix}"
    write_csv(SELECTED_MANIFEST_CSV, rows)

    lines = [
        "# vaBench Release Selected Manifest",
        "",
        "Date: 2026-05-16",
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
        f"| generated true-bugfix companions | {len(materialized)} |",
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


def update_seed_manifest(materialized: list[dict[str, str]]) -> None:
    if not materialized:
        return
    materialized_ids = {row["entry_id"] for row in materialized}
    rows = read_csv(SEED_MANIFEST_CSV)
    if not rows:
        return
    touched = 0
    for row in rows:
        if row["entry_id"] not in materialized_ids:
            continue
        touched += 1
        forms = [form for form in row["asset_materialized_forms"].split("|") if form]
        if "bugfix" not in forms:
            forms.append("bugfix")
        missing = [form for form in row["missing_forms"].split("|") if form and form != "bugfix"]
        row["asset_materialized_forms"] = "|".join(sorted(forms, key=lambda item: FORM_ORDER.index(item)))
        row["asset_complete_forms"] = row["asset_materialized_forms"]
        row["missing_forms"] = "|".join(missing)
        suffix = "true-bugfix companion generated from existing release gold"
        row["notes"] = row["notes"] if suffix in row["notes"] else f"{row['notes']}; {suffix}"
    write_csv(SEED_MANIFEST_CSV, rows)
    if touched == 0:
        return

    lines = [
        "# vaBench Release Seed Manifest",
        "",
        "Date: 2026-05-16",
        "",
        "This manifest records current L1 seed entries copied from reviewed",
        "source tasks plus generated true-bugfix companions where a single-cause",
        "badcase could be reconstructed from existing release gold.",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| seed entries | {len(rows)} |",
        f"| seed entries with all required forms present | {sum(1 for row in rows if not row['missing_forms'])} |",
        f"| generated true-bugfix companions in seed rows | {touched} |",
        "",
        "## Rows",
        "",
        "| Entry | Base ID | Forms | Missing forms | Package task dir | Notes |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['entry_id']}` | `{row['base_id']}` | `{row['asset_materialized_forms']}` | `{row['missing_forms']}` | `{row['package_task_dir']}` | {row['notes']} |"
        )
    SEED_MANIFEST_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    materialized = materialize_bugfixes()
    update_selected_manifest(materialized)
    update_seed_manifest(materialized)
    print(f"materialized true-bugfix companion forms: {len(materialized)}")


if __name__ == "__main__":
    main()
