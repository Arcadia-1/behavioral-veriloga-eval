from __future__ import annotations

from pathlib import Path


CATEGORY_DIR_BY_NAME: dict[str, str] = {
    "Data Converter Models": "CT01_data_converter_models",
    "Comparator and Decision Circuits": "CT02_comparator_and_decision_circuits",
    "Sampling and Analog Memory": "CT03_sampling_and_analog_memory",
    "Baseband Signal Conditioning": "CT04_baseband_signal_conditioning",
    "PLL Clock and Timing Systems": "CT05_pll_clock_and_timing_systems",
    "Calibration, DEM, and Control": "CT06_calibration_dem_and_control",
    "Measurement Instrumentation Flows": "SUP01_measurement_instrumentation_flows",
    "Stimulus and Source Generators": "SUP02_stimulus_and_source_generators",
}


def category_dir_name(category: str) -> str:
    try:
        return CATEGORY_DIR_BY_NAME[category]
    except KeyError as exc:
        raise ValueError(f"unknown vaBench release category: {category}") from exc


def iter_release_entry_paths(tasks_root: Path) -> list[Path]:
    return sorted(tasks_root.glob("*/vbr1_*/release_entry.json"))


def iter_release_task_manifest_paths(tasks_root: Path) -> list[Path]:
    return sorted(tasks_root.glob("*/vbr1_*/forms/*/release_task.json"))


def release_entry_dir(tasks_root: Path, entry_id: str) -> Path:
    matches = sorted(tasks_root.glob(f"*/{entry_id}"))
    if len(matches) == 1:
        return matches[0]
    flat = tasks_root / entry_id
    if flat.exists():
        return flat
    if len(matches) > 1:
        raise ValueError(f"ambiguous vaBench release entry id: {entry_id}")
    return flat


def release_entry_path(tasks_root: Path, entry_id: str) -> Path:
    return release_entry_dir(tasks_root, entry_id) / "release_entry.json"


def release_form_dir(tasks_root: Path, entry_id: str, form: str) -> Path:
    return release_entry_dir(tasks_root, entry_id) / "forms" / form


def release_category_entry_dir(tasks_root: Path, entry_id: str, category: str) -> Path:
    return tasks_root / category_dir_name(category) / entry_id
