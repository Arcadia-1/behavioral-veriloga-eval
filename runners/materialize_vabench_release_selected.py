#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
import shutil
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from vabench_release_paths import release_category_entry_dir


ROOT = Path(__file__).resolve().parents[1]
TRACKER_CSV = ROOT / "docs" / "VABENCH_RELEASE_TRACKER.csv"
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
TASKS_ROOT = ROOT / "tasks"
MANIFEST_CSV = ROOT / "docs" / "VABENCH_RELEASE_SELECTED_MANIFEST.csv"
MANIFEST_MD = ROOT / "docs" / "VABENCH_RELEASE_SELECTED_MANIFEST.md"

FORM_BY_FAMILY = {
    "spec-to-va": "dut",
    "tb-generation": "tb",
    "bugfix": "bugfix",
    "end-to-end": "e2e",
}

FAMILY_BY_FORM = {value: key for key, value in FORM_BY_FAMILY.items()}

SELECTED_SOURCE_LINKS: dict[str, list[str]] = {
    "vbr1_l1_unit_element_thermometer_dac": [
        "tasks/spec-to-va/voltage/dac/vbm1_thermometer_dac_15seg_dut",
        "tasks/tb-generation/voltage/dac/vbm1_thermometer_dac_15seg_tb",
        "tasks/bugfix/voltage/dac/vbm1_thermometer_dac_15seg_bugfix",
        "tasks/end-to-end/voltage/dac/vbm1_thermometer_dac_15seg_e2e",
    ],
    "vbr1_l1_clocked_adc_quantizer": [
        "tasks/end-to-end/voltage/flash_adc_3b_smoke",
    ],
    "vbr1_l1_capacitive_weighted_sar_feedback_dac": [
        "tasks/spec-to-va/voltage/dac/cdac_cal",
    ],
    "vbr1_l2_adc_dac_reconstruction_chain": [
        "tasks/end-to-end/voltage/adc_dac_ideal_4b_smoke",
    ],
    "vbr1_l2_weighted_sar_adc_dac_loop": [
        "tasks/end-to-end/voltage/sar_adc_dac_weighted_8b_smoke",
    ],
    "vbr1_l2_flash_adc_mini_array": [
        "tasks/end-to-end/voltage/flash_adc_3b_smoke",
    ],
    "vbr1_l1_threshold_comparator": [
        "tasks/end-to-end/voltage/comparator_smoke",
    ],
    "vbr1_l1_propagation_delay_comparator": [
        "tasks/end-to-end/voltage/cmp_delay_smoke",
    ],
    "vbr1_l1_hysteresis_comparator": [
        "tasks/end-to-end/voltage/comparator_hysteresis_smoke",
    ],
    "vbr1_l1_window_comparator_detector": [
        "tasks/end-to-end/voltage/window_comparator_smoke",
    ],
    "vbr1_l2_comparator_measurement_flow": [
        "tasks/end-to-end/voltage/comparator_measurement_flow_smoke",
    ],
    "vbr1_l1_pfd_small_phase_error_response": [
        "tasks/spec-to-va/voltage/pll-clock/vbm1_pfd_small_phase_error_response_dut",
        "tasks/end-to-end/voltage/pfd_small_phase_response_smoke",
    ],
    "vbr1_l1_xor_phase_detector": [
        "tasks/end-to-end/voltage/xor_pd_smoke",
    ],
    "vbr1_l1_bang_bang_phase_detector": [
        "tasks/spec-to-va/voltage/pll-clock/bbpd",
        "tasks/end-to-end/voltage/bbpd_data_edge_alignment_smoke",
    ],
    "vbr1_l1_digital_phase_accumulator_with_modulo_wrap": [
        "tasks/end-to-end/voltage/phase_accumulator_timer_wrap_smoke",
    ],
    "vbr1_l2_pll_timing_slice": [
        "tasks/end-to-end/voltage/cppll_tracking_smoke",
    ],
    "vbr1_l2_adpll_lock_ratio_hop_timer_flow": [
        "tasks/end-to-end/voltage/adpll_ratio_hop_smoke",
    ],
    "vbr1_l2_cppll_tracking_and_frequency_step_reacquire_flow": [
        "tasks/end-to-end/voltage/cppll_freq_step_reacquire_smoke",
    ],
    "vbr1_l1_dwa_dem_encoder": [
        "tasks/end-to-end/voltage/dwa_ptr_gen_smoke",
    ],
    "vbr1_l1_lfsr_prbs_generator": [
        "tasks/spec-to-va/voltage/digital-logic/prbs7",
        "tasks/end-to-end/voltage/lfsr_smoke",
    ],
    "vbr1_l1_serializer_frame_aligner": [
        "tasks/end-to-end/voltage/serializer_frame_alignment_smoke",
    ],
    "vbr1_l2_event_controller": [
        "tasks/end-to-end/voltage/simultaneous_event_order_smoke",
    ],
    "vbr1_l2_serializer_frame_alignment_flow": [
        "tasks/end-to-end/voltage/serializer_frame_alignment_smoke",
    ],
    "vbr1_l1_gain_estimator": [
        "tasks/end-to-end/voltage/gain_extraction_smoke",
    ],
    "vbr1_l1_edge_interval_timer": [
        "tasks/end-to-end/voltage/cross_interval_163p333_smoke",
    ],
    "vbr1_l2_measurement_flow": [
        "tasks/end-to-end/voltage/final_step_file_metric_smoke",
    ],
    "vbr1_l2_gain_extraction_convergence_measurement_flow": [
        "tasks/end-to-end/voltage/gain_extraction_smoke",
    ],
    "vbr1_l1_ramp_or_step_source": [
        "tasks/end-to-end/voltage/bound_step_period_guard_smoke",
    ],
    "vbr1_l1_burst_clock_source": [
        "tasks/end-to-end/voltage/clk_burst_gen_smoke",
    ],
    "vbr1_l1_dither_or_noise_like_deterministic_source": [
        "tasks/end-to-end/voltage/noise_gen_smoke",
    ],
    "vbr1_l1_sine_periodic_voltage_source": [
        "tasks/spec-to-va/voltage/signal-source/multitone",
    ],
    "vbr1_l1_clocked_sample_and_hold": [
        "tasks/end-to-end/voltage/sample_hold_smoke",
    ],
    "vbr1_l2_converter_front_end": [
        "tasks/end-to-end/voltage/sample_hold_droop_smoke",
    ],
}

MANIFEST_FIELDS = [
    "entry_id",
    "base_function",
    "package_status",
    "forms_materialized",
    "missing_forms",
    "source_paths",
    "invalid_source_paths",
    "package_task_dir",
    "notes",
]


@dataclass(frozen=True)
class SourceTask:
    form: str
    source_path: Path
    has_prompt: bool
    has_meta: bool
    has_checks: bool
    has_gold: bool
    checks_has_sim_correct: bool
    checks_has_parity: bool

    @property
    def asset_complete(self) -> bool:
        return self.has_prompt and self.has_meta and self.has_checks and self.has_gold

    @property
    def release_ready(self) -> bool:
        return self.asset_complete and self.checks_has_sim_correct

    @property
    def checks_release_ready(self) -> bool:
        return self.checks_has_sim_correct and self.checks_has_parity


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def slugify(value: str) -> str:
    value = value.lower().replace("/", " ")
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def required_forms(row: dict[str, str]) -> list[str]:
    forms = row["required_task_forms"].replace("e2e-form", "e2e").split(";")
    return [form.strip() for form in forms if form.strip() in FAMILY_BY_FORM]


def infer_form(source_path: Path) -> str:
    try:
        family = source_path.relative_to(TASKS_ROOT).parts[0]
    except ValueError as exc:
        raise RuntimeError(f"source path outside tasks root: {source_path}") from exc
    if family not in FORM_BY_FAMILY:
        raise RuntimeError(f"cannot infer release form from source family: {source_path}")
    return FORM_BY_FAMILY[family]


def source_task(source_path: Path) -> SourceTask:
    checks = source_path / "checks.yaml"
    checks_text = checks.read_text(encoding="utf-8", errors="ignore") if checks.exists() else ""
    return SourceTask(
        form=infer_form(source_path),
        source_path=source_path,
        has_prompt=(source_path / "prompt.md").exists(),
        has_meta=(source_path / "meta.json").exists(),
        has_checks=checks.exists(),
        has_gold=(source_path / "gold").is_dir(),
        checks_has_sim_correct=("sim_correct:" in checks_text),
        checks_has_parity=("parity:" in checks_text),
    )


def selected_tracker_rows() -> list[dict[str, str]]:
    return [row for row in read_csv(TRACKER_CSV) if row["package_status"].startswith("selected_")]


def source_tasks_for_entry(entry_id: str) -> tuple[list[SourceTask], list[SourceTask]]:
    ready: list[SourceTask] = []
    invalid: list[SourceTask] = []
    seen_forms: set[str] = set()
    for source in SELECTED_SOURCE_LINKS.get(entry_id, []):
        task = source_task(ROOT / source)
        if task.form in seen_forms:
            invalid.append(task)
            continue
        seen_forms.add(task.form)
        if task.release_ready:
            ready.append(task)
        else:
            invalid.append(task)
    return ready, invalid


def write_source_marker(entry_dir: Path, source: SourceTask) -> None:
    form_dir = entry_dir / "forms" / source.form
    form_dir.mkdir(parents=True, exist_ok=True)
    (form_dir / "SOURCE_TASK.md").write_text(
        "\n".join(
            [
                f"# Selected Source Task: {source.source_path.name}",
                "",
                f"- Source path: `{rel(source.source_path)}`",
                f"- Form: `{source.form}`",
                f"- prompt.md: `{source.has_prompt}`",
                f"- meta.json: `{source.has_meta}`",
                f"- checks.yaml: `{source.has_checks}`",
                f"- gold/: `{source.has_gold}`",
                f"- sim_correct checks: `{source.checks_has_sim_correct}`",
                f"- parity checks: `{source.checks_has_parity}`",
                f"- release-ready checks: `{source.checks_release_ready}`",
                "",
                "This selected release form is copied from an existing source task.",
                "Missing release-schema parity placeholders are normalized in the",
                "release copy when the source task already has behavior checks.",
                "It remains unscored until EVAS and Spectre are rerun or imported",
                "with explicit source-equivalence evidence.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def normalize_release_meta(meta_path: Path, source: SourceTask) -> None:
    payload = json.loads(meta_path.read_text(encoding="utf-8"))
    source_id = str(payload.get("task_id") or payload.get("id") or source.source_path.name)
    payload.setdefault("id", source_id)
    payload.setdefault("task_id", source_id)
    payload["asset_type"] = "vabench_task"
    payload.setdefault("domain", "voltage")
    payload.setdefault("expected_backend", "evas")
    meta_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def normalize_release_prompt(prompt_path: Path, form: str) -> None:
    text = prompt_path.read_text(encoding="utf-8")
    if "Return exactly" in text:
        return
    if form == "tb":
        artifact = "the requested Spectre testbench artifact"
    elif form == "dut":
        artifact = "the requested Verilog-A DUT artifact"
    elif form == "bugfix":
        artifact = "the repaired Verilog-A artifact"
    else:
        artifact = "the requested Verilog-A and Spectre artifacts"
    appendix = "\n".join(
        [
            "",
            "## Output Contract",
            "",
            f"Return exactly {artifact}. Do not include explanatory prose outside",
            "the source file contents. Preserve the module names, ports, saved",
            "waveform columns, and transient simulation contract specified above.",
        ]
    )
    prompt_path.write_text(text.rstrip() + "\n" + appendix + "\n", encoding="utf-8")


def normalize_release_checks(checks_path: Path, source: SourceTask) -> None:
    text = checks_path.read_text(encoding="utf-8")
    additions: list[str] = []
    if not source.checks_has_parity:
        additions.extend(
            [
                "",
                "parity:",
                '  reference: "spectre"',
                '  status: "pending_until_evas_spectre_rerun"',
                "  notes:",
                '    - "Added by the release materializer because the source task predates the release parity schema."',
            ]
        )
    if additions:
        checks_path.write_text(text.rstrip() + "\n" + "\n".join(additions) + "\n", encoding="utf-8")


def copy_release_assets(entry_dir: Path, source: SourceTask) -> dict[str, object]:
    form_dir = entry_dir / "forms" / source.form
    form_dir.mkdir(parents=True, exist_ok=True)
    for name in ("prompt.md", "meta.json", "checks.yaml"):
        shutil.copy2(source.source_path / name, form_dir / name)
    shutil.copytree(source.source_path / "gold", form_dir / "gold")
    normalize_release_meta(form_dir / "meta.json", source)
    normalize_release_prompt(form_dir / "prompt.md", source.form)
    normalize_release_checks(form_dir / "checks.yaml", source)
    gold_files = sorted(path for path in (form_dir / "gold").rglob("*") if path.is_file())
    return {
        "form": source.form,
        "release_path": rel(form_dir),
        "prompt": rel(form_dir / "prompt.md"),
        "meta": rel(form_dir / "meta.json"),
        "checks": rel(form_dir / "checks.yaml"),
        "gold": [rel(path) for path in gold_files],
        "asset_materialized": True,
        "historical_dual_expected": False,
        "source_path": rel(source.source_path),
    }


def write_release_entry(row: dict[str, str], ready: list[SourceTask], invalid: list[SourceTask]) -> dict[str, str]:
    entry_id = row["entry_id"]
    entry_dir = release_category_entry_dir(PACKAGE_ROOT / "tasks", entry_id, row["category"])
    if entry_dir.exists():
        shutil.rmtree(entry_dir)
    entry_dir.mkdir(parents=True)

    release_tasks: list[dict[str, object]] = []
    for source in ready:
        write_source_marker(entry_dir, source)
        release_tasks.append(copy_release_assets(entry_dir, source))

    present_forms = {str(task["form"]) for task in release_tasks}
    missing = [form for form in required_forms(row) if form not in present_forms]
    blockers = [
        *(["source_materialization"] if not release_tasks else []),
        *(["missing_required_forms"] if missing else []),
        "static_validation",
        "evas_certification",
        "spectre_certification",
    ]
    payload = {
        "id": entry_id,
        "benchmark": "vabench-release-v1",
        "release_entry_id": entry_id,
        "level": row["level"],
        "category": row["category"],
        "base_function": row["base_function"],
        "package_status": row["package_status"],
        "score_surface": row["score_surface"],
        "source_base_id": slugify(row["base_function"]),
        "canonical_kernel": "",
        "source_registry_status": "selected_from_existing_task" if release_tasks else "selected_without_source_task",
        "source_evidence_status": "selected_source_pending_dual" if release_tasks else "selected_source_missing",
        "source_tasks": [
            {
                "form": source.form,
                "source_path": rel(source.source_path),
                "prompt": source.has_prompt,
                "meta": source.has_meta,
                "checks": source.has_checks,
                "gold": source.has_gold,
                "asset_complete": source.asset_complete,
                "checks_has_sim_correct": source.checks_has_sim_correct,
                "checks_has_parity": source.checks_has_parity,
                "checks_normalized_for_release": source.release_ready and not source.checks_release_ready,
            }
            for source in [*ready, *invalid]
        ],
        "release_tasks": release_tasks,
        "missing_forms": missing,
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
        "release_blockers": blockers,
    }
    (entry_dir / "release_entry.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    (entry_dir / "README.md").write_text(
        "\n".join(
            [
                f"# {row['base_function']}",
                "",
                f"- Entry: `{entry_id}`",
                f"- Level: `{row['level']}`",
                f"- Category: `{row['category']}`",
                f"- Package status: `{row['package_status']}`",
                f"- Materialized forms: `{', '.join(sorted(present_forms)) if present_forms else 'none'}`",
                f"- Missing forms: `{', '.join(missing) if missing else 'none'}`",
                "",
                "This selected release entry is a long-run materialization target.",
                "It is intentionally unscored until static checks and EVAS/Spectre",
                "dual certification are complete.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return {
        "entry_id": entry_id,
        "base_function": row["base_function"],
        "package_status": row["package_status"],
        "forms_materialized": "|".join(sorted(present_forms)),
        "missing_forms": "|".join(missing),
        "source_paths": "|".join(rel(source.source_path) for source in ready),
        "invalid_source_paths": "|".join(rel(source.source_path) for source in invalid),
        "package_task_dir": rel(entry_dir),
        "notes": "selected source copied; release checks normalized when needed; dual evidence pending rerun"
        if release_tasks
        else "no release-ready source task mapped yet",
    }


def write_manifest(rows: list[dict[str, str]]) -> None:
    with MANIFEST_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    materialized = [row for row in rows if row["forms_materialized"]]
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
        f"| entries with copied source assets | {len(materialized)} |",
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
    MANIFEST_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows: list[dict[str, str]] = []
    for row in selected_tracker_rows():
        ready, invalid = source_tasks_for_entry(row["entry_id"])
        rows.append(write_release_entry(row, ready, invalid))
    write_manifest(rows)
    materialized = sum(1 for row in rows if row["forms_materialized"])
    forms = sum(len(row["forms_materialized"].split("|")) for row in rows if row["forms_materialized"])
    print(
        "materialized selected release entries: {entries}/{total}; copied forms: {forms}".format(
            entries=materialized,
            total=len(rows),
            forms=forms,
        )
    )


if __name__ == "__main__":
    main()
