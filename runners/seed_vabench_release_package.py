#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import shutil
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from vabench_release_paths import release_category_entry_dir


ROOT = Path(__file__).resolve().parents[1]
TRACKER_CSV = ROOT / "docs" / "VABENCH_RELEASE_TRACKER.csv"
REGISTRY_CSV = ROOT / "docs" / "VABENCH_BASE_FUNCTION_REGISTRY.csv"
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
TASKS_ROOT = ROOT / "tasks"
SEED_MANIFEST_CSV = ROOT / "docs" / "VABENCH_RELEASE_SEED_MANIFEST.csv"
SEED_MANIFEST_MD = ROOT / "docs" / "VABENCH_RELEASE_SEED_MANIFEST.md"


ENTRY_TO_BASE_ID = {
    "vbr1_l1_binary_weighted_voltage_dac": "simple_binary_voltage_dac_4b",
    "vbr1_l1_segmented_dac": "segmented_dac",
    "vbr1_l1_thermometer_code_decoder": "thermometer_decoder_guarded",
    "vbr1_l1_sar_logic": "sar_logic_4b",
    "vbr1_l1_offset_comparator": "offset_comparator",
    "vbr1_l1_strongarm_style_latch_comparator": "strongarm_comparator_behavior",
    "vbr1_l1_vco_phase_integrator": "vco_phase_integrator",
    "vbr1_l1_pfd_up_dn_logic": "pfd_reset_race",
    "vbr1_l1_clock_divider": "resettable_counter_divider",
    "vbr1_l1_lock_detector": "lock_detector",
    "vbr1_l1_trim_calibration_controller": "cdac_calibration",
    "vbr1_l1_gain_trim_controller": "gain_trim_controller",
    "vbr1_l1_rotating_dem_selector": "rotating_element_selector",
    "vbr1_l1_windowed_dem_pointer": "barrel_pointer_window",
    "vbr1_l1_element_shuffler": "element_shuffler",
    "vbr1_l1_edge_detector": "edge_detector",
    "vbr1_l1_debounce_latch": "debounce_latch",
    "vbr1_l1_one_shot_timer": "one_shot_timer",
    "vbr1_l1_crossing_metric_writer": "file_metric_writer",
    "vbr1_l1_settling_time_detector": "settling_time_measurement_tb",
    "vbr1_l1_peak_detector": "peak_detector",
    "vbr1_l1_first_order_lowpass": "first_order_lowpass",
    "vbr1_l1_resettable_integrator": "resettable_integrator",
    "vbr1_l1_precision_rectifier": "precision_rectifier",
    "vbr1_l1_voltage_clamp_or_limiter": "voltage_clamp",
    "vbr1_l1_slew_rate_limiter": "slew_rate_limiter",
    "vbr1_l1_aperture_delay_track_and_hold": "track_hold_aperture",
    "vbr1_l1_sample_and_hold_with_droop_leakage": "leaky_hold",
}

FORM_TO_FAMILY = {
    "dut": "spec-to-va",
    "tb": "tb-generation",
    "bugfix": "bugfix",
    "e2e": "end-to-end",
}

MANIFEST_FIELDS = [
    "entry_id",
    "base_id",
    "base_function",
    "category",
    "package_status",
    "source_forms_found",
    "missing_forms",
    "asset_complete_forms",
    "asset_materialized_forms",
    "certification_status",
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

    @property
    def asset_complete(self) -> bool:
        return self.has_prompt and self.has_meta and self.has_checks and self.has_gold


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def find_source_task(base_id: str, form: str) -> SourceTask | None:
    family = FORM_TO_FAMILY[form]
    expected_name = f"vbm1_{base_id}_{form}"
    matches = sorted((TASKS_ROOT / family / "voltage").rglob(expected_name))
    dirs = [path for path in matches if path.is_dir()]
    if not dirs:
        return None
    if len(dirs) > 1:
        raise RuntimeError(f"ambiguous source task for {base_id}/{form}: {dirs}")
    task_dir = dirs[0]
    return SourceTask(
        form=form,
        source_path=task_dir,
        has_prompt=(task_dir / "prompt.md").exists(),
        has_meta=(task_dir / "meta.json").exists(),
        has_checks=(task_dir / "checks.yaml").exists(),
        has_gold=(task_dir / "gold").is_dir(),
    )


def registry_by_base() -> dict[str, dict[str, str]]:
    return {row["base_id"]: row for row in read_csv(REGISTRY_CSV)}


def tracker_rows() -> list[dict[str, str]]:
    rows = read_csv(TRACKER_CSV)
    current = [row for row in rows if row["package_status"].startswith("current_l1_seed")]
    if len(current) != 28:
        raise RuntimeError(f"expected 28 current seed rows, found {len(current)}")
    return current


def source_tasks_for_entry(base_id: str, task_forms: str) -> tuple[list[SourceTask], list[str]]:
    wanted = [form.strip() for form in task_forms.replace("e2e-form", "e2e").split(";")]
    wanted = [form for form in wanted if form in FORM_TO_FAMILY]
    found: list[SourceTask] = []
    missing: list[str] = []
    for form in wanted:
        source = find_source_task(base_id, form)
        if source is None:
            missing.append(form)
        else:
            found.append(source)
    return found, missing


def write_source_marker(entry_dir: Path, source: SourceTask) -> None:
    form_dir = entry_dir / "forms" / source.form
    form_dir.mkdir(parents=True, exist_ok=True)
    marker = form_dir / "SOURCE_TASK.md"
    marker.write_text(
        "\n".join(
            [
                f"# Source Task: {source.source_path.name}",
                "",
                f"- Source path: `{rel(source.source_path)}`",
                f"- Form: `{source.form}`",
                f"- prompt.md: `{source.has_prompt}`",
                f"- meta.json: `{source.has_meta}`",
                f"- checks.yaml: `{source.has_checks}`",
                f"- gold/: `{source.has_gold}`",
                "",
                "This release form was copied from the source-controlled task",
                "for release review. Do not score it until static validation,",
                "EVAS certification, and Spectre certification are attached.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def copy_release_assets(entry_dir: Path, source: SourceTask) -> dict[str, object]:
    form_dir = entry_dir / "forms" / source.form
    form_dir.mkdir(parents=True, exist_ok=True)

    for name in ("prompt.md", "meta.json", "checks.yaml"):
        shutil.copy2(source.source_path / name, form_dir / name)

    gold_src = source.source_path / "gold"
    gold_dst = form_dir / "gold"
    shutil.copytree(gold_src, gold_dst)

    gold_files = sorted(path for path in gold_dst.rglob("*") if path.is_file())
    return {
        "form": source.form,
        "release_path": rel(form_dir),
        "prompt": rel(form_dir / "prompt.md"),
        "meta": rel(form_dir / "meta.json"),
        "checks": rel(form_dir / "checks.yaml"),
        "gold": [rel(path) for path in gold_files],
        "asset_materialized": True,
    }


def write_release_entry(entry: dict[str, str], base_id: str, reg: dict[str, str], sources: list[SourceTask], missing: list[str]) -> None:
    entry_dir = release_category_entry_dir(PACKAGE_ROOT / "tasks", entry["entry_id"], entry["category"])
    if entry_dir.exists():
        shutil.rmtree(entry_dir)
    entry_dir.mkdir(parents=True)
    release_tasks = []
    for source in sources:
        write_source_marker(entry_dir, source)
        if source.asset_complete:
            release_tasks.append(copy_release_assets(entry_dir, source))

    payload = {
        "id": entry["entry_id"],
        "benchmark": "vabench-release-v1",
        "release_entry_id": entry["entry_id"],
        "level": entry["level"],
        "category": entry["category"],
        "base_function": entry["base_function"],
        "package_status": entry["package_status"],
        "score_surface": entry["score_surface"],
        "source_base_id": base_id,
        "canonical_kernel": reg.get("canonical_kernel", ""),
        "source_registry_status": reg.get("release_status", ""),
        "source_evidence_status": reg.get("evidence_status", ""),
        "source_tasks": [
            {
                "form": source.form,
                "source_path": rel(source.source_path),
                "prompt": source.has_prompt,
                "meta": source.has_meta,
                "checks": source.has_checks,
                "gold": source.has_gold,
                "asset_complete": source.asset_complete,
            }
            for source in sources
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
        "release_blockers": [
            *(["missing_required_forms"] if missing else []),
            "static_validation",
            "evas_certification",
            "spectre_certification",
        ],
    }
    (entry_dir / "release_entry.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    (entry_dir / "README.md").write_text(
        "\n".join(
            [
                f"# {entry['base_function']}",
                "",
                f"- Entry: `{entry['entry_id']}`",
                f"- Level: `{entry['level']}`",
                f"- Category: `{entry['category']}`",
                f"- Source base: `{base_id}`",
                f"- Package status: `{entry['package_status']}`",
                f"- Certification: `not_certified`",
                "",
                "This directory is a source-linked release-entry skeleton.",
                "It intentionally does not count in benchmark scores yet.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def seed_current_entries() -> list[dict[str, str]]:
    registry = registry_by_base()
    rows: list[dict[str, str]] = []
    for entry in tracker_rows():
        entry_id = entry["entry_id"]
        base_id = ENTRY_TO_BASE_ID.get(entry_id)
        if base_id is None:
            raise RuntimeError(f"missing ENTRY_TO_BASE_ID mapping for {entry_id}")
        reg = registry.get(base_id)
        if reg is None:
            raise RuntimeError(f"missing registry row for {base_id}")
        if reg.get("counts_as_distinct_function") != "yes":
            raise RuntimeError(f"refusing to seed non-counted base {base_id}")
        sources, missing = source_tasks_for_entry(base_id, entry["required_task_forms"])
        if not sources:
            raise RuntimeError(f"no source task forms found for {entry_id}/{base_id}")
        write_release_entry(entry, base_id, reg, sources, missing)
        asset_complete = [source.form for source in sources if source.asset_complete]
        asset_materialized = asset_complete
        rows.append(
            {
                "entry_id": entry_id,
                "base_id": base_id,
                "base_function": entry["base_function"],
                "category": entry["category"],
                "package_status": entry["package_status"],
                "source_forms_found": "|".join(source.form for source in sources),
                "missing_forms": "|".join(missing),
                "asset_complete_forms": "|".join(asset_complete),
                "asset_materialized_forms": "|".join(asset_materialized),
                "certification_status": "not_certified",
                "package_task_dir": rel(release_category_entry_dir(PACKAGE_ROOT / "tasks", entry_id, entry["category"])),
                "notes": "release assets copied from source tasks; not scored until certified",
            }
        )
    return rows


def write_seed_manifest(rows: list[dict[str, str]]) -> None:
    with SEED_MANIFEST_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    complete_entries = sum(1 for row in rows if not row["missing_forms"])
    lines = [
        "# vaBench Release Seed Manifest",
        "",
        f"Date: {date.today().isoformat()}",
        "",
        "This manifest records current L1 seed entries that have been linked to",
        "existing source-controlled task assets and copied into the release",
        "package for review. These rows are not certified or scored yet.",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| current seed entries linked | {len(rows)} |",
        f"| entries with all requested forms present | {complete_entries} |",
        f"| entries with missing optional/review forms | {len(rows) - complete_entries} |",
        "",
        "## Rows",
        "",
        "| Entry | Base | Forms found | Materialized forms | Missing forms | Package dir |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['entry_id']}` | `{row['base_id']}` | `{row['source_forms_found']}` | `{row['asset_materialized_forms']}` | `{row['missing_forms']}` | `{row['package_task_dir']}` |"
        )
    SEED_MANIFEST_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = seed_current_entries()
    if len(rows) != 28:
        raise SystemExit(f"expected to seed 28 entries, seeded {len(rows)}")
    write_seed_manifest(rows)
    print(f"seeded {len(rows)} current L1 seed release entries")


if __name__ == "__main__":
    main()
