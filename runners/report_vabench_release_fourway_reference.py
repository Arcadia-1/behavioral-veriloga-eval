#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import Any

from run_gold_dual_suite import WAVEFORM_EQUIVALENCE_POLICY, compare_waveforms

try:
    from simulate_evas import (
        behavior_checker_policy,
        evaluate_behavior_with_timeout,
        has_behavior_check,
    )
except ImportError:
    def behavior_checker_policy(checker_id: str, notes: list[str]) -> dict[str, object]:
        return {
            "checker_id": checker_id,
            "implementation": "unavailable_in_report_only_split",
            "notes": list(notes),
        }

    def evaluate_behavior_with_timeout(
        checker_id: str,
        csv_path: Path,
        *,
        timeout_s: int,
    ) -> tuple[float, list[str]]:
        raise RuntimeError(
            "behavior refresh requires the runner/checker split that provides "
            "simulate_evas.evaluate_behavior_with_timeout"
        )

    def has_behavior_check(checker_id: str) -> bool:
        return False


ROOT = Path(__file__).resolve().parents[1]
REPORTS_ROOT = ROOT / "speed-optimization" / "reports"
DEFAULT_SOURCE_JSONS = (
    REPORTS_ROOT / "full_release_evas_py_rust_after_fixes_20260606.json",
    REPORTS_ROOT / "full_release_evas2_sidefx_persist_20260606.json",
    REPORTS_ROOT / "full_release_spectre_ax_strict_20260606.json",
)
DEFAULT_COVERAGE_JSON = REPORTS_ROOT / "current_release_rust_coverage_manifest_rustsim_gate_after_while_20260606.json"
DEFAULT_REPORT_JSON = REPORTS_ROOT / "full_release_fourway_reference_20260606.json"
DEFAULT_REPORT_MD = REPORTS_ROOT / "full_release_fourway_reference_20260606.md"
DEFAULT_BEHAVIOR_REFRESH_TIMEOUT_S = 30

SCHEMA_VERSION = "fourway-reference.v1"
ARTIFACT_KIND = "vabench_release_fourway_reference_experiment"
FROZEN_EXPERIMENT_ID = "vabench-release-fourway-rust-evas2-spectreax-strict-20260606"
FROZEN_ON = "2026-06-08"
FROZEN_REPORT_PATH = "speed-optimization/reports/full_release_fourway_reference_20260606.json"

MODE_ORDER = ("py_strict", "rust_evas2", "spectre_ax", "spectre_strict")
MODE_SPECS: dict[str, dict[str, str]] = {
    "py_strict": {
        "backend": "evas",
        "mode": "strict_current",
        "label": "EVAS1.0 Python strict",
    },
    "rust_evas2": {
        "backend": "evas",
        "mode": "profile_fast_evas2",
        "label": "EVAS2 Rust",
    },
    "spectre_ax": {
        "backend": "spectre",
        "mode": "ax_speed",
        "label": "Spectre AX",
    },
    "spectre_strict": {
        "backend": "spectre",
        "mode": "reference_strict_primary",
        "label": "Spectre strict",
    },
}


def float_or_none(value: object) -> float | None:
    if value is None:
        return None
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(parsed) or math.isinf(parsed):
        return None
    return parsed


def ratio_or_none(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator is None or denominator <= 0:
        return None
    return numerator / denominator


def percentile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    pos = (len(ordered) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return ordered[lo]
    return ordered[lo] * (hi - pos) + ordered[hi] * (pos - lo)


def geomean(values: list[float]) -> float | None:
    positives = [value for value in values if value > 0]
    if not positives:
        return None
    return math.exp(sum(math.log(value) for value in positives) / len(positives))


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path | None) -> str | None:
    if path is None or not path.exists():
        return None
    return sha256_bytes(path.read_bytes())


def sha256_json(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(payload)


def resolve_artifact_path(value: object) -> Path | None:
    if not value:
        return None
    path = Path(str(value))
    if path.is_absolute():
        return path
    return ROOT / path


def row_key(row: dict[str, Any]) -> tuple[str, str, str, str]:
    return (
        str(row.get("entry_id")),
        str(row.get("form")),
        str(row.get("variant") or "gold"),
        str(row.get("task_id")),
    )


def mode_key(row: dict[str, Any]) -> tuple[str, str]:
    return str(row.get("backend")), str(row.get("mode"))


def alias_for(row: dict[str, Any]) -> str | None:
    backend, mode = mode_key(row)
    for alias, spec in MODE_SPECS.items():
        if backend == spec["backend"] and mode == spec["mode"]:
            return alias
    return None


def refresh_behavior_from_csv(
    row: dict[str, Any],
    *,
    timeout_s: int = DEFAULT_BEHAVIOR_REFRESH_TIMEOUT_S,
) -> dict[str, Any]:
    checker_id = str(row.get("checker_id") or "")
    csv_path = resolve_artifact_path(row.get("csv_path"))
    if not checker_id or csv_path is None or not csv_path.exists():
        return row
    refreshed = dict(row)
    try:
        score, notes = evaluate_behavior_with_timeout(checker_id, csv_path, timeout_s=timeout_s)
    except Exception as exc:  # noqa: BLE001 - preserve the source row if the refresh path is broken.
        refreshed["behavior_refresh_error"] = f"{type(exc).__name__}: {exc}"
        return refreshed
    available = has_behavior_check(checker_id)
    behavior_ok = available and score >= 1.0
    refreshed["raw_behavior_score"] = row.get("behavior_score")
    refreshed["raw_behavior_ok"] = row.get("behavior_ok")
    refreshed["raw_ok"] = row.get("ok")
    refreshed["raw_notes"] = row.get("notes", [])
    refreshed["behavior_score"] = score
    refreshed["behavior_ok"] = behavior_ok
    refreshed["ok"] = row.get("simulation_ok") is True and behavior_ok
    refreshed["notes"] = notes
    refreshed["checker_policy"] = behavior_checker_policy(checker_id, notes)
    refreshed["behavior_refreshed_from_csv"] = True
    refreshed["behavior_refresh_timeout_s"] = timeout_s
    return refreshed


def needs_behavior_refresh(row: dict[str, Any]) -> bool:
    # The frozen four-way report only needs to repair stale non-pass fields in
    # source artifacts. Rechecking every PASS row makes report generation slow
    # and can unintentionally turn a fixed reference report into a new run.
    return row.get("ok") is not True or row.get("behavior_ok") is not True


def load_sources(
    paths: list[Path],
    *,
    refresh_behavior: bool = True,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    sources: list[dict[str, Any]] = []
    selected: dict[tuple[tuple[str, str, str, str], tuple[str, str]], dict[str, Any]] = {}
    for source_path in paths:
        artifact = json.loads(source_path.read_text(encoding="utf-8"))
        results = artifact.get("results", [])
        if not isinstance(results, list):
            raise ValueError(f"{source_path} does not contain a list-valued results field")
        source_record = {
            "path": rel(source_path),
            "sha256": sha256_file(source_path),
            "artifact_kind": artifact.get("artifact_kind"),
            "schema_version": artifact.get("schema_version"),
            "created_at": artifact.get("created_at"),
            "selected_rows": artifact.get("selected_rows"),
            "evas_modes": artifact.get("evas_modes", []),
            "spectre_modes": artifact.get("spectre_modes", []),
            "spectre_backend": artifact.get("spectre_backend"),
            "sui_host": artifact.get("sui_host"),
            "host": artifact.get("host"),
            "result_count": len(results),
        }
        sources.append(source_record)
        for row in results:
            if not isinstance(row, dict) or alias_for(row) is None:
                continue
            if refresh_behavior and needs_behavior_refresh(row):
                enriched = refresh_behavior_from_csv(row)
            else:
                enriched = dict(row)
            enriched["_source_report"] = rel(source_path)
            selected[(row_key(enriched), mode_key(enriched))] = enriched
    return list(selected.values()), sources


def values_for(rows: list[dict[str, Any]], key: str) -> list[float]:
    values: list[float] = []
    for row in rows:
        parsed = float_or_none(row.get(key))
        if parsed is not None:
            values.append(parsed)
    return values


def timing_split_value(row: dict[str, Any], *keys: str) -> float | None:
    split = row.get("timing_split", {})
    if not isinstance(split, dict):
        return None
    total = 0.0
    found = False
    for key in keys:
        parsed = float_or_none(split.get(key))
        if parsed is None:
            continue
        total += parsed
        found = True
    return total if found else None


def timing_value(row: dict[str, Any], *keys: str) -> float | None:
    timing = row.get("timing", {})
    if not isinstance(timing, dict):
        return None
    total = 0.0
    found = False
    for key in keys:
        parsed = float_or_none(timing.get(key))
        if parsed is None:
            continue
        total += parsed
        found = True
    return total if found else None


def component_values(row: dict[str, Any]) -> dict[str, float]:
    backend = str(row.get("backend"))
    e2e = float_or_none(row.get("wall_time_s")) or 0.0
    subprocess = float_or_none(row.get("simulator_subprocess_wall_s")) or 0.0
    reported_tran = timing_value(row, "tran_elapsed_s") or 0.0
    if backend == "evas":
        checker = timing_split_value(row, "run_case_behavior_checker_s") or 0.0
        csv_or_psf = timing_split_value(row, "run_case_evas_runner_csv_write_s") or 0.0
        fixture = timing_split_value(row, "fixture_materialize_s") or 0.0
        parse_or_log = timing_split_value(row, "run_case_evas_runner_derive_bus_signals_s") or 0.0
    else:
        checker = timing_split_value(row, "behavior_checker_s") or 0.0
        csv_or_psf = timing_split_value(row, "psf_parse_s") or 0.0
        fixture = timing_split_value(row, "fixture_materialize_s") or 0.0
        parse_or_log = timing_split_value(row, "spectre_log_read_s", "spectre_log_parse_s") or 0.0
    known = subprocess + checker + csv_or_psf + fixture + parse_or_log
    return {
        "e2e_wall_s": e2e,
        "subprocess_wall_s": subprocess,
        "reported_tran_s": reported_tran,
        "checker_s": checker,
        "csv_or_psf_s": csv_or_psf,
        "fixture_or_staging_s": fixture,
        "parse_or_log_s": parse_or_log,
        "other_overhead_s": max(0.0, e2e - known),
    }


def summarize_mode(alias: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    e2e_values = values_for(rows, "wall_time_s")
    subprocess_values = values_for(rows, "simulator_subprocess_wall_s")
    components = defaultdict(float)
    checker_policies: Counter[str] = Counter()
    nonpass_rows: list[dict[str, Any]] = []
    for row in rows:
        for key, value in component_values(row).items():
            components[key] += value
        policy = row.get("checker_policy", {})
        implementation = "missing"
        if isinstance(policy, dict):
            implementation = str(policy.get("implementation") or "missing")
        checker_policies[implementation] += 1
        if row.get("ok") is not True:
            nonpass_rows.append(
                {
                    "entry_id": row.get("entry_id"),
                    "form": row.get("form"),
                    "variant": row.get("variant") or "gold",
                    "task_id": row.get("task_id"),
                    "status": row.get("status"),
                    "simulation_ok": row.get("simulation_ok"),
                    "behavior_ok": row.get("behavior_ok"),
                    "notes": row.get("notes", []),
                }
            )
    spec = MODE_SPECS[alias]
    e2e_sum = sum(e2e_values)
    subprocess_sum = sum(subprocess_values)
    return {
        "alias": alias,
        "label": spec["label"],
        "backend": spec["backend"],
        "mode": spec["mode"],
        "rows": len(rows),
        "simulation_ok": sum(1 for row in rows if row.get("simulation_ok") is True),
        "behavior_pass": sum(1 for row in rows if row.get("ok") is True),
        "behavior_nonpass": sum(1 for row in rows if row.get("ok") is not True),
        "e2e_wall_sum_s": e2e_sum,
        "e2e_wall_mean_s": (e2e_sum / len(e2e_values)) if e2e_values else None,
        "e2e_wall_median_s": percentile(e2e_values, 0.5),
        "e2e_wall_p25_s": percentile(e2e_values, 0.25),
        "e2e_wall_p75_s": percentile(e2e_values, 0.75),
        "e2e_wall_geomean_s": geomean(e2e_values),
        "subprocess_wall_sum_s": subprocess_sum,
        "subprocess_wall_mean_s": (subprocess_sum / len(subprocess_values)) if subprocess_values else None,
        "subprocess_wall_median_s": percentile(subprocess_values, 0.5),
        "component_totals_s": dict(sorted(components.items())),
        "component_percentages": {
            key: ratio_or_none(value, e2e_sum) for key, value in sorted(components.items())
        },
        "checker_policy_counts": dict(sorted(checker_policies.items())),
        "nonpass_rows": nonpass_rows,
        "source_reports": sorted({str(row.get("_source_report")) for row in rows}),
    }


def build_speed_tables(by_alias: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    modes = {alias: summarize_mode(alias, by_alias.get(alias, [])) for alias in MODE_ORDER}
    ax = modes["spectre_ax"]
    strict = modes["spectre_strict"]
    py_strict = modes["py_strict"]
    rust = modes["rust_evas2"]
    comparisons: list[dict[str, Any]] = []
    for alias in MODE_ORDER:
        row = modes[alias]
        comparisons.append(
            {
                "alias": alias,
                "label": row["label"],
                "speedup_vs_spectre_ax_e2e": ratio_or_none(ax["e2e_wall_sum_s"], row["e2e_wall_sum_s"]),
                "speedup_vs_spectre_ax_subprocess": ratio_or_none(
                    ax["subprocess_wall_sum_s"], row["subprocess_wall_sum_s"]
                ),
                "speedup_vs_spectre_strict_e2e": ratio_or_none(
                    strict["e2e_wall_sum_s"], row["e2e_wall_sum_s"]
                ),
                "speedup_vs_spectre_strict_subprocess": ratio_or_none(
                    strict["subprocess_wall_sum_s"], row["subprocess_wall_sum_s"]
                ),
                "speedup_vs_py_strict_e2e": ratio_or_none(py_strict["e2e_wall_sum_s"], row["e2e_wall_sum_s"]),
                "speedup_vs_py_strict_subprocess": ratio_or_none(
                    py_strict["subprocess_wall_sum_s"], row["subprocess_wall_sum_s"]
                ),
                "speedup_vs_rust_evas2_e2e": ratio_or_none(rust["e2e_wall_sum_s"], row["e2e_wall_sum_s"]),
                "speedup_vs_rust_evas2_subprocess": ratio_or_none(
                    rust["subprocess_wall_sum_s"], row["subprocess_wall_sum_s"]
                ),
            }
        )
    return {"modes": modes, "comparisons": comparisons}


def precision_summary_by_candidate(precision: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(row.get("candidate")): row
        for row in precision.get("summary", [])
        if isinstance(row, dict)
    }


def build_claim_status(speed: dict[str, Any], precision: dict[str, Any]) -> dict[str, Any]:
    comparison_by_alias = {
        str(row.get("alias")): row
        for row in speed.get("comparisons", [])
        if isinstance(row, dict)
    }
    rust_vs_ax = comparison_by_alias.get("rust_evas2", {})
    summaries = precision_summary_by_candidate(precision)
    rust_precision = summaries.get("rust_evas2", {})
    ax_precision = summaries.get("spectre_ax", {})
    rust_equivalent = (
        rust_precision.get("reference_usable_rows") == rust_precision.get("equivalent_rows")
        and rust_precision.get("blocked_rows") == 0
        and rust_precision.get("needs_review_rows") == 0
    )
    ax_equivalent = (
        ax_precision.get("reference_usable_rows") == ax_precision.get("equivalent_rows")
        and ax_precision.get("blocked_rows") == 0
        and ax_precision.get("needs_review_rows") == 0
    )
    return {
        "status": "frozen_engineering_reference",
        "allowed_wording": [
            (
                "On this frozen four-way vaBench release slice, Rust EVAS2 is faster than "
                "Spectre AX in aggregate E2E and subprocess wall time."
            ),
            (
                "Rust EVAS2 and Spectre AX both pass the Spectre-strict-referenced "
                "behavior/waveform equivalence gate on this slice."
            ),
        ],
        "forbidden_wording": [
            "Rust EVAS2 is more accurate than Spectre AX.",
            "Rust EVAS2 is faster than Spectre AX on every row.",
            "This four-way cross-host artifact alone is a final paper-facing same-server speed claim.",
            "Rust EVAS2 fully covers all Verilog-A language semantics.",
        ],
        "speed_aggregate_vs_spectre_ax": {
            "allowed": True,
            "e2e_speedup": rust_vs_ax.get("speedup_vs_spectre_ax_e2e"),
            "subprocess_speedup": rust_vs_ax.get("speedup_vs_spectre_ax_subprocess"),
            "scope": "aggregate over common rows in this frozen four-way reference",
            "caveats": [
                "Do not claim every row is faster.",
                "Cross-host EVAS/Spectre wall ratios are diagnostic unless promoted by a same-host protocol.",
                "Subprocess wall is a runner boundary metric, not pure kernel time.",
            ],
        },
        "precision_equivalence_vs_spectre_strict": {
            "allowed": bool(rust_equivalent and ax_equivalent),
            "rust_evas2_equivalent_rows": rust_precision.get("equivalent_rows"),
            "spectre_ax_equivalent_rows": ax_precision.get("equivalent_rows"),
            "reference_usable_rows": rust_precision.get("reference_usable_rows"),
            "scope": "Spectre strict is the reference for equivalence, not a precision ranking target.",
        },
        "precision_better_than_spectre_ax": {
            "allowed": False,
            "reason": (
                "The frozen metrics support equivalence to Spectre strict, not superiority over AX; "
                "AX has smaller worst effective RMS values in this artifact."
            ),
            "rust_evas2_worst_effective_mean_rel_rms": rust_precision.get(
                "worst_effective_mean_relative_rms_error"
            ),
            "rust_evas2_worst_effective_signal_rel_rms": rust_precision.get(
                "worst_effective_signal_relative_rms_error"
            ),
            "spectre_ax_worst_effective_mean_rel_rms": ax_precision.get(
                "worst_effective_mean_relative_rms_error"
            ),
            "spectre_ax_worst_effective_signal_rel_rms": ax_precision.get(
                "worst_effective_signal_relative_rms_error"
            ),
        },
        "paper_facing_speed_claim_from_this_artifact_alone": {
            "allowed": False,
            "reason": (
                "This artifact freezes the four-way engineering reference. A final paper-facing "
                "Rust-default speed claim still needs the same-slice same-host/approved-bridge "
                "protocol to be promoted as the paper speed artifact."
            ),
        },
    }


def compare_pair(task_id: str, candidate_csv: object, reference_csv: object) -> dict[str, Any]:
    left = resolve_artifact_path(candidate_csv)
    right = resolve_artifact_path(reference_csv)
    if left is None or right is None:
        return {"status": "blocked", "reason": "missing csv"}
    if not left.exists() or not right.exists():
        return {"status": "blocked", "reason": "csv path not found"}
    try:
        return compare_waveforms(task_id, left, right)
    except Exception as exc:  # noqa: BLE001 - report comparison failures as data.
        return {"status": "blocked", "reason": f"{type(exc).__name__}: {exc}"}


def build_precision_table(by_alias: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    reference_rows = {row_key(row): row for row in by_alias.get("spectre_strict", [])}
    rows_by_alias = {alias: {row_key(row): row for row in rows} for alias, rows in by_alias.items()}
    candidate_aliases = ("py_strict", "rust_evas2", "spectre_ax")
    summary: list[dict[str, Any]] = []
    details: list[dict[str, Any]] = []
    for alias in candidate_aliases:
        candidate_rows = rows_by_alias.get(alias, {})
        all_keys = sorted(set(candidate_rows) | set(reference_rows))
        passed = needs_review = blocked = compared = reference_usable = candidate_behavior_pass = 0
        max_abs_values: list[float] = []
        mean_rel_values: list[float] = []
        max_rel_values: list[float] = []
        raw_mean_rel_values: list[float] = []
        raw_max_rel_values: list[float] = []
        for key in all_keys:
            candidate = candidate_rows.get(key)
            reference = reference_rows.get(key)
            entry_id, form, variant, task_id = key
            if candidate is not None and candidate.get("ok") is True:
                candidate_behavior_pass += 1
            detail = {
                "entry_id": entry_id,
                "form": form,
                "variant": variant,
                "task_id": task_id,
                "candidate": alias,
                "candidate_label": MODE_SPECS[alias]["label"],
                "reference": "spectre_strict",
                "reference_label": MODE_SPECS["spectre_strict"]["label"],
                "status": "blocked",
                "reason": None,
                "candidate_behavior_ok": candidate.get("behavior_ok") if candidate else None,
                "reference_behavior_ok": reference.get("behavior_ok") if reference else None,
                "max_abs_saved_units": None,
                "max_abs_v": None,
                "effective_mean_relative_rms_error": None,
                "effective_signal_relative_rms_error": None,
                "mean_relative_rms_error": None,
                "max_relative_rms_error": None,
                "raw_mean_relative_rms_error": None,
                "raw_signal_relative_rms_error": None,
                "signals_compared": None,
            }
            if candidate is None:
                detail["reason"] = "missing candidate row"
            elif reference is None:
                detail["reason"] = "missing Spectre strict row"
            elif reference.get("simulation_ok") is not True:
                detail["reason"] = "reference simulation not ok"
            elif reference.get("behavior_ok") is not True:
                detail["reason"] = "reference behavior non-pass"
            elif candidate.get("simulation_ok") is not True:
                detail["reason"] = "candidate simulation not ok"
            else:
                reference_usable += 1
                comparison = compare_pair(task_id, candidate.get("csv_path"), reference.get("csv_path"))
                status = str(comparison.get("status", "blocked"))
                detail["status"] = status
                detail["reason"] = comparison.get("reason")
                detail["max_abs_saved_units"] = comparison.get("max_abs_v")
                # Backward-compatible alias for older consumers.  New reports
                # label this as saved-signal units because not every saved
                # column is a voltage; e.g. delay_ps is a measurement trace.
                detail["max_abs_v"] = comparison.get("max_abs_v")
                detail["effective_mean_relative_rms_error"] = comparison.get("mean_relative_rms_error")
                detail["effective_signal_relative_rms_error"] = comparison.get("max_relative_rms_error")
                detail["mean_relative_rms_error"] = comparison.get("mean_relative_rms_error")
                detail["max_relative_rms_error"] = comparison.get("max_relative_rms_error")
                detail["raw_mean_relative_rms_error"] = comparison.get("raw_mean_relative_rms_error")
                detail["raw_signal_relative_rms_error"] = comparison.get("raw_max_relative_rms_error")
                detail["signals_compared"] = comparison.get("signals_compared")
                if status in {"passed", "needs_review"}:
                    compared += 1
                    for target, values in (
                        ("max_abs_saved_units", max_abs_values),
                        ("effective_mean_relative_rms_error", mean_rel_values),
                        ("effective_signal_relative_rms_error", max_rel_values),
                        ("raw_mean_relative_rms_error", raw_mean_rel_values),
                        ("raw_signal_relative_rms_error", raw_max_rel_values),
                    ):
                        parsed = float_or_none(detail.get(target))
                        if parsed is not None:
                            values.append(parsed)
            if detail["status"] == "passed":
                passed += 1
            elif detail["status"] == "needs_review":
                needs_review += 1
            else:
                blocked += 1
            details.append(detail)
        summary.append(
            {
                "candidate": alias,
                "candidate_label": MODE_SPECS[alias]["label"],
                "reference": "spectre_strict",
                "reference_label": MODE_SPECS["spectre_strict"]["label"],
                "candidate_rows": len(candidate_rows),
                "candidate_behavior_pass": candidate_behavior_pass,
                "reference_rows": len(reference_rows),
                "reference_usable_rows": reference_usable,
                "compared_rows": compared,
                "equivalent_rows": passed,
                "needs_review_rows": needs_review,
                "blocked_rows": blocked,
                "worst_max_abs_saved_units": max(max_abs_values) if max_abs_values else None,
                "worst_effective_mean_relative_rms_error": max(mean_rel_values) if mean_rel_values else None,
                "worst_effective_signal_relative_rms_error": max(max_rel_values) if max_rel_values else None,
                "worst_raw_mean_relative_rms_error": max(raw_mean_rel_values) if raw_mean_rel_values else None,
                "worst_raw_signal_relative_rms_error": max(raw_max_rel_values) if raw_max_rel_values else None,
                # Backward-compatible aliases.
                "worst_max_abs_v": max(max_abs_values) if max_abs_values else None,
                "worst_mean_relative_rms_error": max(mean_rel_values) if mean_rel_values else None,
                "worst_signal_relative_rms_error": max(max_rel_values) if max_rel_values else None,
            }
        )
    interesting = [
        row
        for row in details
        if row["status"] != "passed"
        or row.get("candidate_behavior_ok") is not True
        or row.get("reference_behavior_ok") is not True
    ]
    return {
        "policy": WAVEFORM_EQUIVALENCE_POLICY,
        "summary": summary,
        "needs_review_or_blocked_rows": interesting,
    }


def build_rust_runtime_coverage(rows: list[dict[str, Any]], coverage_json: Path | None) -> dict[str, Any]:
    counter_totals: Counter[str] = Counter()
    enabled_rows = 0
    sim_program_rows = 0
    sim_program_rejection_rows = 0
    full_model_fallback_rows = 0
    for row in rows:
        perf = row.get("perf_counters", {})
        if not isinstance(perf, dict):
            continue
        numeric = {key: float_or_none(value) or 0.0 for key, value in perf.items()}
        for key, value in numeric.items():
            if value:
                counter_totals[key] += value
        if numeric.get("rust_full_model_fastpath_enabled", 0.0) > 0:
            enabled_rows += 1
        if numeric.get("rust_sim_program_enabled", 0.0) > 0:
            sim_program_rows += 1
        if numeric.get("rust_sim_program_rejections", 0.0) > 0:
            sim_program_rejection_rows += 1
        if numeric.get("rust_full_model_fastpath_fallbacks_total", 0.0) > 0:
            full_model_fallback_rows += 1
    static_gate: dict[str, Any] | None = None
    if coverage_json is not None and coverage_json.exists():
        coverage = json.loads(coverage_json.read_text(encoding="utf-8"))
        summary = coverage.get("summary", {})
        static_gate = {
            "source": rel(coverage_json),
            "compile_pass_rows": summary.get("compile_pass_rows")
            or summary.get("model_rows")
            or (summary.get("compile_status_counts") or {}).get("pass"),
            "strict_rustsim_program_supported_rows": summary.get(
                "strict_rustsim_program_supported_rows"
            ),
            "strict_rustsim_program_gate_counts": summary.get("strict_rustsim_program_gate_counts"),
            "strict_rustsim_program_blocker_counts": summary.get(
                "strict_rustsim_program_blocker_counts"
            ),
            "strict_rustsim_program_opcode_totals": summary.get(
                "strict_rustsim_program_opcode_totals"
            ),
        }
    selected_counters = {
        key: counter_totals.get(key, 0.0)
        for key in (
            "rust_full_model_fastpath_enabled",
            "rust_full_model_fastpath_fallbacks_total",
            "rust_sim_program_enabled",
            "rust_sim_program_rejections",
            "rust_sim_program_event_count",
            "rust_sim_program_body_stmt_ops",
            "rust_sim_program_body_expr_ops",
            "rust_sim_program_transition_count",
            "rust_sim_program_record_count",
            "rust_sim_program_event_fires",
            "rust_sim_program_points",
            "rust_sim_program_side_effects",
            "rust_sim_program_lower_elapsed_s",
            "rust_sim_program_abi_build_elapsed_s",
            "rust_sim_program_time_grid_elapsed_s",
            "rust_sim_program_runtime_elapsed_s",
            "rust_sim_program_runtime_attempts",
            "rust_sim_program_final_capacity",
            "rust_sim_program_record_replay_elapsed_s",
            "rust_sim_program_state_sync_elapsed_s",
            "rust_sim_program_fastpath_total_elapsed_s",
        )
    }
    return {
        "runtime_rows": len(rows),
        "rust_full_model_enabled_rows": enabled_rows,
        "rust_sim_program_enabled_rows": sim_program_rows,
        "rust_sim_program_rejection_rows": sim_program_rejection_rows,
        "rust_full_model_fallback_rows": full_model_fallback_rows,
        "selected_counter_totals": selected_counters,
        "static_gate": static_gate,
    }


def build_top_rows(by_alias: dict[str, list[dict[str, Any]]], limit: int) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str, str], dict[str, dict[str, Any]]] = defaultdict(dict)
    for alias, rows in by_alias.items():
        for row in rows:
            grouped[row_key(row)][alias] = row
    out: list[dict[str, Any]] = []
    for key, cells in grouped.items():
        rust = cells.get("rust_evas2")
        if rust is None:
            continue
        components = component_values(rust)
        dominant_key, dominant_value = max(
            ((key, value) for key, value in components.items() if key != "e2e_wall_s"),
            key=lambda item: item[1],
        )
        perf = rust.get("perf_counters", {})
        if not isinstance(perf, dict):
            perf = {}
        row = {
            "entry_id": key[0],
            "form": key[1],
            "variant": key[2],
            "task_id": key[3],
            "rust_evas2_e2e_s": components["e2e_wall_s"],
            "rust_evas2_subprocess_s": components["subprocess_wall_s"],
            "dominant_rust_evas2_cost": dominant_key,
            "dominant_rust_evas2_cost_s": dominant_value,
            "rust_full_model_fastpath_enabled": perf.get("rust_full_model_fastpath_enabled"),
            "rust_sim_program_enabled": perf.get("rust_sim_program_enabled"),
        }
        for alias in ("py_strict", "spectre_ax", "spectre_strict"):
            other = cells.get(alias)
            row[f"{alias}_e2e_s"] = float_or_none(other.get("wall_time_s")) if other else None
            row[f"speedup_{alias}_over_rust_evas2_e2e"] = ratio_or_none(
                row[f"{alias}_e2e_s"], row["rust_evas2_e2e_s"]
            )
        out.append(row)
    out.sort(key=lambda row: float(row["rust_evas2_e2e_s"]), reverse=True)
    return out[:limit]


def build_experiment_lock(
    *,
    common_rows: set[tuple[str, str, str, str]],
    sources: list[dict[str, Any]],
    coverage_json: Path | None,
) -> dict[str, Any]:
    common_row_payload = [
        {"entry_id": key[0], "form": key[1], "variant": key[2], "task_id": key[3]}
        for key in sorted(common_rows)
    ]
    coverage_record = None
    if coverage_json is not None:
        coverage_record = {
            "path": rel(coverage_json),
            "sha256": sha256_file(coverage_json),
        }
    return {
        "status": "frozen",
        "experiment_id": FROZEN_EXPERIMENT_ID,
        "frozen_on": FROZEN_ON,
        "frozen_report": FROZEN_REPORT_PATH,
        "row_set_size": len(common_rows),
        "row_set_sha256": sha256_json(common_row_payload),
        "fixed_modes": MODE_SPECS,
        "source_artifacts": [
            {
                "path": source.get("path"),
                "sha256": source.get("sha256"),
                "created_at": source.get("created_at"),
                "artifact_kind": source.get("artifact_kind"),
                "schema_version": source.get("schema_version"),
                "result_count": source.get("result_count"),
            }
            for source in sources
        ],
        "coverage_artifact": coverage_record,
        "rerun_required_when": [
            "EVAS simulator code or Rust EVAS2 default/fastpath semantics change.",
            "Release row set, checker policy, or waveform equivalence policy changes.",
            "Spectre AX/strict options, host class, bridge route, or runner timing boundary changes.",
            "Any source artifact hash in this lock no longer matches the frozen source file.",
        ],
        "reuse_rule": (
            "Use this report as the stable four-way reference until one of the rerun triggers fires; "
            "do not replace the conclusion with ad-hoc smoke numbers."
        ),
    }


def build_report(
    source_jsons: list[Path],
    coverage_json: Path | None,
    top_limit: int = 20,
    *,
    refresh_behavior: bool = True,
) -> dict[str, Any]:
    results, sources = load_sources(source_jsons, refresh_behavior=refresh_behavior)
    by_alias: dict[str, list[dict[str, Any]]] = {alias: [] for alias in MODE_ORDER}
    for row in results:
        alias = alias_for(row)
        if alias in by_alias:
            by_alias[alias].append(row)
    for rows in by_alias.values():
        rows.sort(key=row_key)

    row_sets = {alias: {row_key(row) for row in rows} for alias, rows in by_alias.items()}
    common_rows = set.intersection(*(row_sets[alias] for alias in MODE_ORDER if row_sets[alias]))
    missing_by_mode = {
        alias: len(set.union(*(row_sets.values())) - rows) if row_sets else 0
        for alias, rows in row_sets.items()
    }
    speed = build_speed_tables(by_alias)
    precision = build_precision_table(by_alias)

    return {
        "schema_version": SCHEMA_VERSION,
        "artifact_kind": ARTIFACT_KIND,
        "date": date.today().isoformat(),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "experiment_lock": build_experiment_lock(
            common_rows=common_rows,
            sources=sources,
            coverage_json=coverage_json,
        ),
        "claim_status": build_claim_status(speed, precision),
        "scope": {
            "purpose": "Reusable four-way reference experiment for EVAS1, EVAS2, Spectre AX, and Spectre strict.",
            "mode_order": list(MODE_ORDER),
            "mode_specs": MODE_SPECS,
            "row_count_by_mode": {alias: len(rows) for alias, rows in by_alias.items()},
            "common_row_count": len(common_rows),
            "missing_row_count_by_mode": missing_by_mode,
            "claim_boundary": (
                "Cross-host Spectre/EVAS wall ratios are diagnostic unless the raw source artifact "
                "records a controlled same-host protocol. Use subprocess/E2E labels literally; "
                "subprocess wall is not pure simulator kernel time."
            ),
            "behavior_refresh_from_csv": refresh_behavior,
            "behavior_refresh_policy": (
                "refresh stale non-pass source rows from existing CSV checkers only"
                if refresh_behavior
                else "use behavior fields stored in source artifacts"
            ),
        },
        "sources": sources,
        "speed": speed,
        "precision": precision,
        "rust_coverage": build_rust_runtime_coverage(by_alias.get("rust_evas2", []), coverage_json),
        "top_rust_evas2_rows": build_top_rows(by_alias, top_limit),
    }


def fmt(value: object, digits: int = 3) -> str:
    parsed = float_or_none(value)
    if parsed is None:
        return "-"
    return f"{parsed:.{digits}f}"


def fmt_ratio(value: object) -> str:
    parsed = float_or_none(value)
    if parsed is None:
        return "-"
    return f"{parsed:.2f}x"


def md_cell(value: object, *, code: bool = False) -> str:
    if value is None:
        return "-"
    text = str(value).replace("\n", "<br>").replace("|", "\\|")
    if not text:
        return "-"
    return f"`{text}`" if code else text


def write_markdown(path: Path, report: dict[str, Any]) -> None:
    speed = report["speed"]
    modes = speed["modes"]
    precision = report["precision"]
    rust = report["rust_coverage"]
    lock = report["experiment_lock"]
    claim_status = report["claim_status"]
    lines = [
        "# vaBench Four-Way Reference Experiment",
        "",
        f"Date: {report['date']}",
        f"Artifact: `{report['artifact_kind']}`",
        "",
        "## Scope",
        "",
        f"- Common rows across all four modes: `{report['scope']['common_row_count']}`",
        f"- Behavior checker fields refreshed from existing CSVs: `{report['scope'].get('behavior_refresh_from_csv')}`",
        f"- Behavior refresh policy: {report['scope'].get('behavior_refresh_policy')}",
        f"- Claim boundary: {report['scope']['claim_boundary']}",
        "- Reuse rule: cite this derived JSON/Markdown together with its source raw JSONs; rerun only when EVAS code, benchmark rows, checker policy, host class, or Spectre settings change.",
        "- `Reported tran` is simulator-reported diagnostic time and is not added into E2E percentages; for Spectre it can exceed subprocess wall because of tool reporting semantics.",
        "",
        "## Frozen Claim Contract",
        "",
        f"- Experiment ID: `{lock['experiment_id']}`",
        f"- Frozen on: `{lock['frozen_on']}`",
        f"- Frozen report: `{lock['frozen_report']}`",
        f"- Row-set size: `{lock['row_set_size']}`",
        f"- Row-set SHA256: `{lock['row_set_sha256']}`",
        f"- Reuse rule: {lock['reuse_rule']}",
        "",
        "Allowed wording:",
    ]
    for item in claim_status["allowed_wording"]:
        lines.append(f"- {item}")
    lines.extend(["", "Forbidden wording:"])
    for item in claim_status["forbidden_wording"]:
        lines.append(f"- {item}")
    paper_gate = claim_status["paper_facing_speed_claim_from_this_artifact_alone"]
    lines.extend(
        [
            "",
            f"Paper-facing boundary: `{paper_gate['allowed']}` from this artifact alone. {paper_gate['reason']}",
            "",
            "Rerun triggers:",
        ]
    )
    for item in lock["rerun_required_when"]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
        "## Source Raw Artifacts",
        "",
            "| Source | Results | EVAS modes | Spectre modes | Backend | Host | SHA256 |",
            "| --- | ---: | --- | --- | --- | --- | --- |",
        ]
    )
    for source in report["sources"]:
        lines.append(
            "| {path} | {count} | {evas} | {spectre} | {backend} | {host} | `{sha}` |".format(
                path=md_cell(source["path"], code=True),
                count=source["result_count"],
                evas=md_cell(", ".join(str(item) for item in source.get("evas_modes", [])), code=True),
                spectre=md_cell(", ".join(str(item) for item in source.get("spectre_modes", [])), code=True),
                backend=md_cell(source.get("spectre_backend") or "-", code=True),
                host=md_cell(source.get("host") or source.get("sui_host") or "-", code=True),
                sha=str(source.get("sha256") or "-")[:12],
            )
        )

    lines.extend(
        [
            "",
            "## Speed Overview",
            "",
            "| Simulator | Mode | Rows | Sim OK | Behavior PASS | E2E total s | Subprocess total s | Geomean E2E/row s | vs AX E2E | vs AX subprocess |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    comparison_by_alias = {row["alias"]: row for row in speed["comparisons"]}
    for alias in MODE_ORDER:
        row = modes[alias]
        comp = comparison_by_alias[alias]
        lines.append(
            "| {label} | `{mode}` | {rows} | {sim} | {behavior} | {e2e} | {sub} | {geo} | {vs_ax_e2e} | {vs_ax_sub} |".format(
                label=row["label"],
                mode=row["mode"],
                rows=row["rows"],
                sim=row["simulation_ok"],
                behavior=row["behavior_pass"],
                e2e=fmt(row["e2e_wall_sum_s"]),
                sub=fmt(row["subprocess_wall_sum_s"]),
                geo=fmt(row["e2e_wall_geomean_s"]),
                vs_ax_e2e=fmt_ratio(comp["speedup_vs_spectre_ax_e2e"]),
                vs_ax_sub=fmt_ratio(comp["speedup_vs_spectre_ax_subprocess"]),
            )
        )

    lines.extend(
        [
            "",
            "## Component Time Breakdown",
            "",
            "| Simulator | E2E total | Subprocess | Reported tran | Checker | CSV/PSF | Fixture/staging | Parse/log | Other overhead | Checker % | Subprocess % |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for alias in MODE_ORDER:
        row = modes[alias]
        c = row["component_totals_s"]
        p = row["component_percentages"]
        lines.append(
            "| {label} | {e2e} | {sub} | {tran} | {checker} | {csv} | {fixture} | {parse} | {other} | {checker_pct} | {sub_pct} |".format(
                label=row["label"],
                e2e=fmt(c.get("e2e_wall_s")),
                sub=fmt(c.get("subprocess_wall_s")),
                tran=fmt(c.get("reported_tran_s")),
                checker=fmt(c.get("checker_s")),
                csv=fmt(c.get("csv_or_psf_s")),
                fixture=fmt(c.get("fixture_or_staging_s")),
                parse=fmt(c.get("parse_or_log_s")),
                other=fmt(c.get("other_overhead_s")),
                checker_pct=fmt((p.get("checker_s") or 0.0) * 100, 1) + "%",
                sub_pct=fmt((p.get("subprocess_wall_s") or 0.0) * 100, 1) + "%",
            )
        )

    lines.extend(
        [
            "",
            "## Precision Against Spectre Strict",
            "",
            "Rows where Spectre strict itself fails the behavior checker are not treated as usable precision references.",
            "",
            "`effective` metrics are the simulator-equivalence metrics after allowed edge-window treatment. "
            "`raw` metrics keep the original pointwise waveform difference for diagnosis. "
            "`abs saved units` is intentionally not called voltage because some saved columns are measurements such as `delay_ps`.",
            "",
            "| Candidate | Reference usable | Candidate PASS | Compared | Equivalent | Needs review | Blocked | Worst abs saved units | Worst effective mean rel RMS | Worst effective signal rel RMS | Worst raw mean rel RMS | Worst raw signal rel RMS |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in precision["summary"]:
        lines.append(
            "| {candidate} | {usable} | {pass_count} | {compared} | {equiv} | {review} | {blocked} | {max_abs} | {eff_mean_rel} | {eff_max_rel} | {raw_mean_rel} | {raw_max_rel} |".format(
                candidate=row["candidate_label"],
                usable=row["reference_usable_rows"],
                pass_count=row["candidate_behavior_pass"],
                compared=row["compared_rows"],
                equiv=row["equivalent_rows"],
                review=row["needs_review_rows"],
                blocked=row["blocked_rows"],
                max_abs=fmt(row["worst_max_abs_saved_units"], 6),
                eff_mean_rel=fmt(row["worst_effective_mean_relative_rms_error"], 6),
                eff_max_rel=fmt(row["worst_effective_signal_relative_rms_error"], 6),
                raw_mean_rel=fmt(row["worst_raw_mean_relative_rms_error"], 6),
                raw_max_rel=fmt(row["worst_raw_signal_relative_rms_error"], 6),
            )
        )

    policy_name = WAVEFORM_EQUIVALENCE_POLICY.get("policy", "spectre_equivalence_core")
    lines.extend(
        [
            "",
            "## Precision Gate",
            "",
            "| Gate | Meaning | Pass condition |",
            "| --- | --- | --- |",
            "| Behavior checker | Circuit-level functional acceptance | Current row checker returns PASS |",
            "| Waveform absolute gate | Low-swing / near-zero guard for voltage-like saved signals | `max_rmse_v <= 0.05` and `max_abs_v <= 0.30` in the waveform comparator |",
            f"| Waveform relative gate | Simulator-style relative waveform agreement | effective row mean relative RMS and effective worst-signal relative RMS satisfy `{policy_name}` |",
            "| Special functional parity | PLL/gain/ADC rows where pointwise waveform is not the right acceptance metric | Task-specific parity helper in `run_gold_dual_suite.py` returns `passed` |",
        ]
    )

    interesting = precision["needs_review_or_blocked_rows"][:30]
    if interesting:
        lines.extend(
            [
                "",
                "## Needs Review Or Blocked Rows",
                "",
                "| Entry | Form | Candidate | Status | Reason | Abs saved units | Effective signal rel RMS |",
                "| --- | --- | --- | --- | --- | ---: | ---: |",
            ]
        )
        for row in interesting:
            lines.append(
                "| `{entry}` | `{form}` | {candidate} | `{status}` | {reason} | {max_abs} | {max_rel} |".format(
                    entry=row["entry_id"],
                    form=row["form"],
                    candidate=row["candidate_label"],
                    status=row["status"],
                    reason=md_cell(row.get("reason") or "-"),
                    max_abs=fmt(row.get("max_abs_saved_units"), 6),
                    max_rel=fmt(row.get("effective_signal_relative_rms_error"), 6),
                )
            )

    lines.extend(
        [
            "",
            "## Rust Runtime Coverage",
            "",
            "| Metric | Value |",
            "| --- | ---: |",
            f"| Runtime rows | {rust['runtime_rows']} |",
            f"| Rust full-model enabled rows | {rust['rust_full_model_enabled_rows']} |",
            f"| RustSimProgram enabled rows | {rust['rust_sim_program_enabled_rows']} |",
            f"| RustSimProgram rejection rows | {rust['rust_sim_program_rejection_rows']} |",
            f"| Rust full-model fallback rows | {rust['rust_full_model_fallback_rows']} |",
        ]
    )
    static_gate = rust.get("static_gate")
    if isinstance(static_gate, dict):
        lines.extend(
            [
                f"| Static compile-pass model rows | {static_gate.get('compile_pass_rows')} |",
                f"| Static strict RustSimProgram supported rows | {static_gate.get('strict_rustsim_program_supported_rows')} |",
            ]
        )
    for key, value in rust["selected_counter_totals"].items():
        lines.append(f"| `{key}` | {fmt(value, 0)} |")

    lines.extend(
        [
            "",
            "## Top Rust EVAS2 E2E Rows",
            "",
            "| Entry | Form | Rust E2E s | Rust subprocess s | Dominant Rust cost | Py strict / Rust | AX / Rust | Strict / Rust | RustSimProgram |",
            "| --- | --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in report["top_rust_evas2_rows"]:
        lines.append(
            "| `{entry}` | `{form}` | {rust_e2e} | {rust_sub} | `{dominant}` | {py} | {ax} | {strict} | {sim_program} |".format(
                entry=row["entry_id"],
                form=row["form"],
                rust_e2e=fmt(row["rust_evas2_e2e_s"]),
                rust_sub=fmt(row["rust_evas2_subprocess_s"]),
                dominant=row["dominant_rust_evas2_cost"],
                py=fmt_ratio(row["speedup_py_strict_over_rust_evas2_e2e"]),
                ax=fmt_ratio(row["speedup_spectre_ax_over_rust_evas2_e2e"]),
                strict=fmt_ratio(row["speedup_spectre_strict_over_rust_evas2_e2e"]),
                sim_program=md_cell(row.get("rust_sim_program_enabled")),
            )
        )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source-json", action="append", type=Path, default=[])
    ap.add_argument("--coverage-json", type=Path, default=DEFAULT_COVERAGE_JSON)
    ap.add_argument("--report-json", type=Path, default=DEFAULT_REPORT_JSON)
    ap.add_argument("--report-md", type=Path, default=DEFAULT_REPORT_MD)
    ap.add_argument("--top-limit", type=int, default=20)
    ap.add_argument(
        "--no-refresh-behavior",
        action="store_true",
        help="Use behavior fields stored in source artifacts instead of rechecking existing CSVs.",
    )
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    source_jsons = args.source_json or list(DEFAULT_SOURCE_JSONS)
    report = build_report(
        source_jsons,
        args.coverage_json,
        top_limit=args.top_limit,
        refresh_behavior=not args.no_refresh_behavior,
    )
    args.report_json.parent.mkdir(parents=True, exist_ok=True)
    args.report_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(args.report_md, report)
    print(
        "wrote {json_path} and {md_path}; common_rows={rows}".format(
            json_path=args.report_json,
            md_path=args.report_md,
            rows=report["scope"]["common_row_count"],
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
