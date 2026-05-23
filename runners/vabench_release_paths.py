from __future__ import annotations

from pathlib import Path


CATEGORY_DIR_BY_NAME: dict[str, str] = {
    "Data Converters": "CT01_data_converters",
    "Comparators and Decision Circuits": "CT02_comparators_and_decision_circuits",
    "Sample, Hold, and Analog Memory": "CT03_sample_hold_and_analog_memory",
    "Analog Behavioral Signal Conditioning": "CT04_analog_behavioral_signal_conditioning",
    "PLL / Clock / Event Timing": "CT05_pll_clock_event_timing",
    "Calibration, DEM, and Control": "CT07_calibration_dem_and_control",
    "Measurement and Testbench Instrumentation": "CT08_measurement_and_testbench_instrumentation",
    "Stimulus and Sources": "CT09_stimulus_and_sources",
}


def category_dir_name(category: str) -> str:
    try:
        return CATEGORY_DIR_BY_NAME[category]
    except KeyError as exc:
        raise ValueError(f"unknown vaBench release category: {category}") from exc


def iter_release_entry_paths(tasks_root: Path) -> list[Path]:
    return sorted(tasks_root.glob("CT*/vbr1_*/release_entry.json"))


def iter_release_task_manifest_paths(tasks_root: Path) -> list[Path]:
    return sorted(tasks_root.glob("CT*/vbr1_*/forms/*/release_task.json"))


def release_entry_dir(tasks_root: Path, entry_id: str) -> Path:
    matches = sorted(tasks_root.glob(f"CT*/{entry_id}"))
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
