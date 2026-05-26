#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from typing import Any


TASK_FAMILIES = ("end-to-end", "spec-to-va", "bugfix", "tb-generation")
RELEASE_FORMS = ("normal", "true-bugfix", "behavior-regression", "evidence-only")
PROVENANCE_STATUSES = (
    "clean",
    "badcase_available",
    "historical_bugfix_fixed_only",
    "reconstructed_badcase",
    "provenance_incomplete",
)
BADCASE_ORIGINS = ("original", "recovered", "reconstructed")
COUNT_KEYS = ("model_capability", "benchmark_coverage", "bugfix_claim")

CORE_TRACK = "core"
SUPPORT_TRACK = "support"
TRACKS = (CORE_TRACK, SUPPORT_TRACK)
DIFFICULTY_LEVELS = ("D1", "D2", "D3")

SUPPORT_SUITE_CATEGORIES = {
    "Measurement Instrumentation Flows",
    "Stimulus and Source Generators",
}

SUPPORT_SUITE_ENTRY_IDS = {
    "vbr1_l1_burst_clock_source",
    "vbr1_l1_crossing_metric_writer",
    "vbr1_l1_dither_or_noise_like_deterministic_source",
    "vbr1_l1_edge_interval_timer",
    "vbr1_l1_gain_estimator",
    "vbr1_l1_lfsr_prbs_generator",
    "vbr1_l1_peak_detector",
    "vbr1_l1_ramp_or_step_source",
    "vbr1_l1_settling_time_detector",
    "vbr1_l1_sine_periodic_voltage_source",
    "vbr1_l2_gain_extraction_convergence_measurement_flow",
    "vbr1_l2_measurement_flow",
    "vbr1_l2_programmable_stimulus_sequencer",
}

CONTENT_DENOMINATOR_EXCLUDED_ENTRIES: dict[str, list[str]] = {
    entry_id: ["support_suite_not_core_circuit_score"]
    for entry_id in sorted(SUPPORT_SUITE_ENTRY_IDS)
}


def task_id_from_meta(meta: dict[str, Any], task_dir: Path | None = None) -> str:
    if "task_id" in meta:
        return str(meta["task_id"])
    if "id" in meta:
        return str(meta["id"])
    return task_dir.name if task_dir is not None else "<unknown>"


def count_flags(meta: dict[str, Any]) -> dict[str, bool]:
    raw = meta.get("counts")
    if isinstance(raw, dict):
        return {key: bool(raw.get(key, _default_count(meta, key))) for key in COUNT_KEYS}
    return {key: _default_count(meta, key) for key in COUNT_KEYS}


def should_count_as(meta: dict[str, Any], key: str = "model_capability") -> bool:
    if key not in COUNT_KEYS:
        raise ValueError(f"unknown vaBench count key: {key}")
    if meta.get("asset_type", "vabench_task") != "vabench_task":
        return False
    if meta.get("release_form") == "evidence-only":
        return False
    return count_flags(meta)[key]


def content_denominator_exclusion_reasons(release_entry_id: str) -> list[str]:
    return list(CONTENT_DENOMINATOR_EXCLUDED_ENTRIES.get(release_entry_id, []))


def is_content_denominator_entry(release_entry_id: str) -> bool:
    return release_entry_id not in CONTENT_DENOMINATOR_EXCLUDED_ENTRIES


def validation_errors(
    meta: dict[str, Any],
    task_dir: Path | None = None,
    *,
    require_promotion_fields: bool = False,
) -> list[str]:
    errors: list[str] = []
    task_id = task_id_from_meta(meta, task_dir)

    asset_type = meta.get("asset_type", "vabench_task")
    if asset_type != "vabench_task":
        errors.append(
            f"{task_id}: asset_type={asset_type!r} is not allowed under tasks/; "
            "EVAS/Spectre conformance assets must live outside vaBench task counts"
        )

    family = meta.get("family")
    if family not in TASK_FAMILIES:
        errors.append(f"{task_id}: unsupported family={family!r}")

    release_form = meta.get("release_form")
    if release_form is not None and release_form not in RELEASE_FORMS:
        errors.append(f"{task_id}: unsupported release_form={release_form!r}")

    provenance_status = meta.get("provenance_status")
    if provenance_status is not None and provenance_status not in PROVENANCE_STATUSES:
        errors.append(f"{task_id}: unsupported provenance_status={provenance_status!r}")

    badcase_origin = meta.get("badcase_origin")
    if badcase_origin is not None and badcase_origin not in BADCASE_ORIGINS:
        errors.append(f"{task_id}: unsupported badcase_origin={badcase_origin!r}")

    raw_counts = meta.get("counts")
    if raw_counts is not None:
        if not isinstance(raw_counts, dict):
            errors.append(f"{task_id}: counts must be an object")
        else:
            unknown = sorted(set(raw_counts) - set(COUNT_KEYS))
            if unknown:
                errors.append(f"{task_id}: unknown count flags: {', '.join(unknown)}")
            for key in COUNT_KEYS:
                if key in raw_counts and not isinstance(raw_counts[key], bool):
                    errors.append(f"{task_id}: counts.{key} must be boolean")

    if require_promotion_fields:
        for field in ("asset_type", "benchmark_split", "release_form", "provenance_status", "counts"):
            if field not in meta:
                errors.append(f"{task_id}: promoted tasks must set {field}")

    if release_form == "evidence-only":
        if not isinstance(raw_counts, dict):
            errors.append(f"{task_id}: evidence-only rows must set explicit false count flags")
        else:
            for key in COUNT_KEYS:
                if raw_counts.get(key) is not False:
                    errors.append(f"{task_id}: evidence-only rows must set counts.{key}=false")

    if release_form == "true-bugfix":
        if family != "bugfix":
            errors.append(f"{task_id}: true-bugfix release_form requires family=bugfix")
        if provenance_status not in {"badcase_available", "reconstructed_badcase"}:
            errors.append(
                f"{task_id}: true-bugfix requires provenance_status=badcase_available "
                "or reconstructed_badcase"
            )
        if provenance_status == "reconstructed_badcase" and badcase_origin != "reconstructed":
            errors.append(f"{task_id}: reconstructed_badcase requires badcase_origin=reconstructed")
        if isinstance(raw_counts, dict) and raw_counts.get("bugfix_claim") is not True:
            errors.append(f"{task_id}: true-bugfix rows must set counts.bugfix_claim=true")
        if task_dir is not None and not has_bugfix_pair(task_dir):
            errors.append(f"{task_id}: true-bugfix requires buggy/fixed gold source evidence")

    if family == "bugfix" and release_form not in {None, "true-bugfix"}:
        if isinstance(raw_counts, dict) and raw_counts.get("bugfix_claim"):
            errors.append(f"{task_id}: non-true-bugfix rows cannot count as bugfix_claim")

    return errors


def validate_or_raise(
    meta: dict[str, Any],
    task_dir: Path | None = None,
    *,
    require_promotion_fields: bool = False,
) -> None:
    errors = validation_errors(meta, task_dir, require_promotion_fields=require_promotion_fields)
    if errors:
        raise ValueError("invalid vaBench task metadata:\n" + "\n".join(f"  - {error}" for error in errors))


def has_bugfix_pair(task_dir: Path) -> bool:
    gold_dir = task_dir / "gold"
    if not gold_dir.is_dir():
        return False
    source_names = {path.name.lower() for path in gold_dir.glob("*.va")}
    has_buggy = any(_is_buggy_source_name(name) for name in source_names)
    has_fixed = any(_is_fixed_source_name(name) for name in source_names)
    return has_buggy and has_fixed


def _default_count(meta: dict[str, Any], key: str) -> bool:
    release_form = meta.get("release_form")
    if release_form == "evidence-only":
        return False
    if key == "bugfix_claim":
        return meta.get("family") == "bugfix" and release_form == "true-bugfix"
    return True


def _is_buggy_source_name(name: str) -> bool:
    stem = Path(name).stem
    return any(token in stem for token in ("buggy", "broken", "badcase", "bad"))


def _is_fixed_source_name(name: str) -> bool:
    stem = Path(name).stem
    return any(token in stem for token in ("fixed", "goodcase", "good", "ref"))
