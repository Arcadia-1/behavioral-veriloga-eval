#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from run_gold_dual_suite import compare_waveforms


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
REPORTS_ROOT = PACKAGE_ROOT / "reports"
DOCS_DATA_ROOT = ROOT / "docs" / "data"

HISTORICAL_FOURWAY_REFERENCE_JSON = (
    ROOT
    / "speed-optimization"
    / "reports"
    / "full_release_fourway_reference_after_cmp_delay_cross_time_fix_20260608.json"
)
SPECTRE_SELF_CONSISTENCY_JSON = (
    ROOT
    / "speed-optimization"
    / "reports"
    / "spectre_ax_classic_self_consistency_clean_repeats_20260522.json"
)
OVERVIEW_JSON = REPORTS_ROOT / "benchmark_overview.json"
FULL300_SPECTRE_STRICT_SUMMARY = (
    ROOT / "results" / "vabench-300-dual-reference-rust-checker29-full-20260622" / "summary.json"
)
FULL300_SPECTRE_AX_SUMMARY = (
    ROOT / "results" / "vabench-300-dual-ax-rust-checker29-full-20260622" / "summary.json"
)
FULL300_EVAS_RUST_SUMMARY = (
    ROOT / "results" / "vabench-300-evas-rust-full-checker29-metaraw-20260622" / "summary.json"
)
FULL300_EVAS_PYTHON_SUMMARY = (
    ROOT / "results" / "vabench-300-evas-python-full-checker29-metaraw-20260622" / "summary.json"
)

PRECISION_JSON = REPORTS_ROOT / "precision_overview.json"
PRECISION_MD = REPORTS_ROOT / "precision_overview.md"
DOCS_PRECISION_JSON = DOCS_DATA_ROOT / "precision_overview.json"

POINTWISE_DIFFERENCE_TAXONOMY = [
    {
        "name": "solver_sampling_grid",
        "label": "Solver sampling grid",
        "what_changes": "EVAS and Spectre may save different accepted transient steps, so the report compares common signals on a resampled grid.",
        "why_expected": "Adaptive solvers choose output points differently even when the circuit-level trajectory is equivalent.",
        "known_shortcoming": "Our comparison does not prove that EVAS reproduced Spectre's internal step acceptance history; it only compares saved observable signals after alignment.",
        "current_handling": "The released report uses a fixed common sample grid and keeps both effective and raw RMS metrics visible.",
        "bug_signal": "Treat it as a bug if the stable regions disagree, if the checker result changes, or if a row only passes after hiding a broad time interval.",
        "feedback_wanted": "Send the row id, both CSV traces, and the first time range where the aligned stable-region values diverge.",
        "reporting_rule": "Use aligned-grid RMS as a diagnostic metric; do not read it as bit-exact equality.",
    },
    {
        "name": "event_time_and_cross",
        "label": "Event time and cross() localization",
        "what_changes": "cross() events and timer events can fire at slightly different localized times.",
        "why_expected": "The two engines use different event scheduling and breakpoint-localization mechanics.",
        "known_shortcoming": "EVAS does not yet claim full Spectre-equivalent ordering for every cross(), timer(), transition(), and simultaneous-event corner case.",
        "current_handling": "Rows with event-heavy behavior are checked by behavior checkers first, then by waveform/event diagnostics on the supported subset.",
        "bug_signal": "Treat it as a bug if an edge is missed, duplicated, ordered differently in a way that changes state, or if EVAS PASS / Spectre FAIL appears.",
        "feedback_wanted": "A minimal Verilog-A snippet with the triggering cross()/timer() statements is the most useful report.",
        "reporting_rule": "Check behavior, event consistency, and edge-window metrics before calling this a mismatch.",
    },
    {
        "name": "edge_window",
        "label": "Edge and discontinuity window",
        "what_changes": "A few samples around fast edges, discontinuities, or digital thresholds can dominate raw pointwise error.",
        "why_expected": "One-sample edge placement differences can produce large instantaneous voltage deltas while stable regions match.",
        "known_shortcoming": "The edge-window rule is a pragmatic acceptance gate. If used carelessly, it could mask a real timing or threshold bug.",
        "current_handling": "Effective metrics may discount only a bounded localized window, and raw metrics remain visible next to the effective metrics.",
        "bug_signal": "Treat it as a bug if the excluded window grows, repeats across many edges, changes a sampled decision, or affects a task metric.",
        "feedback_wanted": "Report the signal name, edge time, raw max error, and whether the post-edge state or checker output changed.",
        "reporting_rule": "Effective metrics may discount a bounded localized window; raw metrics stay visible for audit.",
    },
    {
        "name": "interpolation",
        "label": "Interpolation on the common grid",
        "what_changes": "Saved waveforms are interpolated before RMS comparison.",
        "why_expected": "Different native output times require interpolation to compare like with like.",
        "known_shortcoming": "The current diagnostic uses simple common-grid interpolation; it can overstate or understate error for sparse outputs and very sharp transitions.",
        "current_handling": "We report row-level and worst-signal RMS instead of hiding interpolation-sensitive rows behind a single pass/fail scalar.",
        "bug_signal": "Treat it as a bug if a denser save grid or direct event-time comparison changes the conclusion for a row.",
        "feedback_wanted": "A suggested comparison method or a row where interpolation choice flips the result would be directly actionable.",
        "reporting_rule": "Treat interpolation error as part of the precision diagnostic, not as the task's functional score.",
    },
    {
        "name": "transition_smoothing",
        "label": "transition() smoothing",
        "what_changes": "transition() ramps can differ slightly in breakpoint placement and sampled slope.",
        "why_expected": "EVAS and Spectre do not promise identical internal smoothing schedules.",
        "known_shortcoming": "EVAS transition handling is aligned for the benchmark-supported cases, but it is not a complete public clone of Spectre's internal smoothing implementation.",
        "current_handling": "Stable-region behavior, checker results, and raw/effective waveform metrics are shown together so transition artifacts are not silently ignored.",
        "bug_signal": "Treat it as a bug if transition delay, rise/fall time, or target update semantics change a downstream decision or metric.",
        "feedback_wanted": "A small transition() example with expected timing, target updates, and saved waveforms is the best repair input.",
        "reporting_rule": "Inspect stable-region behavior and checker metrics when transition edges inflate raw RMS.",
    },
    {
        "name": "noise_like_or_dithered_stimulus",
        "label": "Noise-like or dithered stimulus",
        "what_changes": "Rows with dither, pseudo-random control, or measurement stimulus can show poor pointwise phase agreement while preserving the extracted circuit metric.",
        "why_expected": "For these rows the design objective is usually an aggregate metric such as gain, lock, count, or convergence, not identical sample-by-sample noise phase.",
        "known_shortcoming": "If the checker metric is too broad, it may miss waveform-level differences that a circuit designer would care about.",
        "current_handling": "The page lists task-metric rows separately and keeps diagnostic waveform-only RMS visible for the same rows.",
        "bug_signal": "Treat it as a bug if a different seed, window, or stimulus phase changes pass/fail, or if the aggregate metric hides visible functional drift.",
        "feedback_wanted": "Suggestions for stronger metric windows, deterministic seeds, or additional observables are especially useful here.",
        "reporting_rule": "Use deterministic task metrics as the acceptance gate, with pointwise RMS reported as supporting evidence.",
    },
    {
        "name": "task_metric_gate",
        "label": "Task-metric gate",
        "what_changes": "Some rows are accepted by extracted circuit metrics, such as gain or lock/frequency values, not by raw pointwise waveform equality.",
        "why_expected": "Measurement-flow tasks can use dither/noise-like stimulus where pointwise phase is not the design objective.",
        "known_shortcoming": "A task-metric gate is only as good as the checker behind it. Weak checkers can over-accept; overly tight checkers can reject valid simulator differences.",
        "current_handling": "The report names the task-metric policy, metric delta, diagnostic waveform status, and raw/effective RMS side by side.",
        "bug_signal": "Treat it as a bug if the metric tolerance is undocumented, if the metric is not circuit-meaningful, or if a row passes despite an obviously wrong waveform.",
        "feedback_wanted": "Concrete checker improvements are welcome: extra observables, better windows, stricter metric bounds, or task-specific edge cases.",
        "reporting_rule": "Report the task metric and include pointwise waveform diagnostics only as explanatory context.",
    },
]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_json_optional(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "artifact_status": "missing",
            "artifact": rel(path),
            "summary": {},
        }
    payload = read_json(path)
    payload.setdefault("artifact_status", "available")
    payload.setdefault("artifact", rel(path))
    return payload


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_cached_precision_report(benchmark_rows: int | None) -> dict[str, Any] | None:
    if not PRECISION_JSON.exists():
        return None
    cached = read_json(PRECISION_JSON)
    summary = cached.get("summary", {})
    if not isinstance(summary, dict):
        return None
    if cached.get("precision_source") != "full300_current_summaries":
        return None
    if cached.get("status") != "pass":
        return None
    if benchmark_rows is not None and summary.get("precision_evidence_rows") != benchmark_rows:
        return None
    if summary.get("precision_total_comparisons") != summary.get("precision_pass_comparisons"):
        return None
    cached["date"] = date.today().isoformat()
    cached["pointwise_difference_taxonomy"] = POINTWISE_DIFFERENCE_TAXONOMY
    return cached


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def resolve_path(value: Any) -> Path:
    path = Path(str(value))
    return path if path.is_absolute() else ROOT / path


def as_float(value: Any) -> float | None:
    return float(value) if isinstance(value, (int, float)) else None


def fmt(value: Any) -> str:
    if value is None or value == "":
        return "-"
    if isinstance(value, float):
        if value == 0:
            return "0"
        if abs(value) >= 1000 or abs(value) < 0.001:
            return f"{value:.3e}"
        return f"{value:.6g}"
    return str(value)


def ratio(numerator: Any, denominator: Any) -> float | None:
    try:
        top = float(numerator)
        bottom = float(denominator)
    except (TypeError, ValueError):
        return None
    return top / bottom if bottom else None


def policy_name(result: dict[str, Any]) -> str | None:
    policy = result.get("policy")
    if isinstance(policy, dict):
        return str(policy.get("policy") or "")
    if isinstance(policy, str):
        return policy
    return None


def comparison_task_id(meta: dict[str, Any]) -> str:
    legacy = str(meta.get("legacy_task_id") or "")
    if legacy:
        return legacy.replace(":", "_")
    release_entry_id = str(meta.get("release_entry_id") or "")
    form = str(meta.get("form") or "")
    return f"{release_entry_id}_{form}".strip("_")


def metadata_by_key(overview: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    rows = {}
    for row in overview.get("form_rows", []):
        if isinstance(row, dict):
            rows[(str(row.get("release_entry_id")), str(row.get("form")))] = row
    return rows


def load_spectre_summary_rows(path: Path, metadata: dict[tuple[str, str], dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    payload = read_json(path)
    rows = {}
    for row in payload.get("results", []):
        if not isinstance(row, dict):
            continue
        key = (str(row.get("entry_id")), str(row.get("form")))
        spectre = row.get("raw_result", {}).get("spectre", {})
        csv_path = spectre.get("csv_path") if isinstance(spectre, dict) else None
        if not csv_path:
            continue
        meta = metadata.get(key, {"release_entry_id": key[0], "form": key[1]})
        rows[key] = {
            "csv_path": resolve_path(csv_path),
            "behavior_pass": bool(row.get("expected_result_met") and spectre.get("ok")),
            "comparison_task_id": comparison_task_id(meta),
            "metadata": meta,
        }
    return rows


def load_evas_summary_rows(path: Path, metadata: dict[tuple[str, str], dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    payload = read_json(path)
    rows = {}
    for row in payload.get("results", []):
        if not isinstance(row, dict):
            continue
        key = (str(row.get("legacy_entry_id")), str(row.get("form")))
        result_root = row.get("result_root")
        if not result_root:
            continue
        meta = metadata.get(key, {"release_entry_id": key[0], "form": key[1]})
        rows[key] = {
            "csv_path": resolve_path(result_root) / "tran.csv",
            "behavior_pass": bool(row.get("compile_sim_pass") and row.get("behavior_checker_pass")),
            "comparison_task_id": comparison_task_id(meta),
            "metadata": meta,
        }
    return rows


def update_worst(worst: dict[str, float], result: dict[str, Any]) -> None:
    fields = {
        "worst_effective_mean_relative_rms_error": "mean_relative_rms_error",
        "worst_effective_signal_relative_rms_error": "max_relative_rms_error",
        "worst_raw_mean_relative_rms_error": "raw_mean_relative_rms_error",
        "worst_raw_signal_relative_rms_error": "raw_max_relative_rms_error",
        "worst_max_rmse_v": "max_rmse_v",
        "worst_max_abs_v": "max_abs_v",
    }
    for target, source in fields.items():
        value = result.get(source)
        if isinstance(value, (int, float)):
            worst[target] = max(worst.get(target, 0.0), float(value))


def task_metric_detail(
    candidate: dict[str, Any],
    reference: dict[str, Any],
    result: dict[str, Any],
    surface: dict[str, str],
    key: tuple[str, str],
) -> dict[str, Any]:
    meta = candidate["metadata"]
    diagnostic_task_id = str(meta.get("task_id") or meta.get("legacy_task_id") or key[0])
    diagnostic = compare_waveforms(diagnostic_task_id, candidate["csv_path"], reference["csv_path"])
    evas_metric = result.get("evas", {}) if isinstance(result.get("evas"), dict) else {}
    spectre_metric = result.get("spectre", {}) if isinstance(result.get("spectre"), dict) else {}
    return {
        "candidate": surface["candidate"],
        "candidate_label": surface["candidate_label"],
        "release_entry_id": key[0],
        "form": key[1],
        "task_id": meta.get("task_id"),
        "legacy_task_id": meta.get("legacy_task_id"),
        "category": meta.get("category"),
        "provenance": "v1.1_provisional"
        if meta.get("expansion_status") == "provisional_v1.1_management"
        else ("promoted_v1.1" if meta.get("expansion_status") == "certified_v1.1_promoted" else "inherited_v1"),
        "acceptance_policy": policy_name(result),
        "status": result.get("status"),
        "relative_gain_delta": as_float(result.get("relative_gain_delta")),
        "candidate_gain": as_float(evas_metric.get("diff_gain")),
        "reference_gain": as_float(spectre_metric.get("diff_gain")),
        "diagnostic_waveform_status": diagnostic.get("status"),
        "diagnostic_waveform_mean_relative_rms_error": as_float(diagnostic.get("mean_relative_rms_error")),
        "diagnostic_waveform_worst_signal_relative_rms_error": as_float(diagnostic.get("max_relative_rms_error")),
        "diagnostic_note": (
            "Task acceptance uses the extracted circuit metric. The diagnostic waveform-only comparison "
            "is retained to explain why raw pointwise RMS is not the score for this row."
        ),
    }


def compare_surface(
    surface: dict[str, str],
    candidate_rows: dict[tuple[str, str], dict[str, Any]],
    reference_rows: dict[tuple[str, str], dict[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    common_keys = sorted(set(candidate_rows) & set(reference_rows))
    passed = 0
    needs_review = 0
    blocked = 0
    worst: dict[str, float] = {}
    review_details: list[dict[str, Any]] = []
    task_metric_rows: list[dict[str, Any]] = []
    task_metric_count = 0
    max_task_metric_delta: float | None = None

    for key in common_keys:
        candidate = candidate_rows[key]
        reference = reference_rows[key]
        result = compare_waveforms(candidate["comparison_task_id"], candidate["csv_path"], reference["csv_path"])
        update_worst(worst, result)

        status = result.get("status")
        if status == "passed":
            passed += 1
        elif status == "needs_review":
            needs_review += 1
        else:
            blocked += 1

        if policy_name(result) == "gain_extraction_metric_parity_v1":
            task_metric_count += 1
            delta = as_float(result.get("relative_gain_delta"))
            if delta is not None:
                max_task_metric_delta = max(max_task_metric_delta or 0.0, delta)
            task_metric_rows.append(task_metric_detail(candidate, reference, result, surface, key))

        if status != "passed":
            meta = candidate["metadata"]
            review_details.append(
                {
                    "candidate": surface["candidate"],
                    "candidate_label": surface["candidate_label"],
                    "release_entry_id": key[0],
                    "form": key[1],
                    "task_id": meta.get("task_id"),
                    "legacy_task_id": meta.get("legacy_task_id"),
                    "category": meta.get("category"),
                    "status": status,
                    "reason": result.get("reason"),
                    "policy": policy_name(result),
                    "mean_relative_rms_error": as_float(result.get("mean_relative_rms_error")),
                    "max_relative_rms_error": as_float(result.get("max_relative_rms_error")),
                    "max_rmse_v": as_float(result.get("max_rmse_v")),
                    "max_abs_v": as_float(result.get("max_abs_v")),
                }
            )

    compared = len(common_keys)
    behavior_pass = sum(1 for row in candidate_rows.values() if row.get("behavior_pass"))
    summary = {
        "candidate": surface["candidate"],
        "candidate_label": surface["candidate_label"],
        "reference": "spectre_strict",
        "reference_label": "Spectre strict",
        "candidate_rows": len(candidate_rows),
        "reference_usable_rows": len(reference_rows),
        "candidate_behavior_pass": behavior_pass,
        "compared_rows": compared,
        "equivalent_rows": passed,
        "needs_review_rows": needs_review,
        "blocked_rows": blocked,
        "task_metric_rows": task_metric_count,
        "max_task_metric_relative_delta": max_task_metric_delta,
        "equivalence_rate": ratio(passed, compared),
        "claim": (
            "equivalent_to_spectre_strict"
            if compared and passed == compared and needs_review == 0 and blocked == 0
            else "needs_review"
        ),
    }
    for field in (
        "worst_effective_mean_relative_rms_error",
        "worst_effective_signal_relative_rms_error",
        "worst_raw_mean_relative_rms_error",
        "worst_raw_signal_relative_rms_error",
        "worst_max_rmse_v",
        "worst_max_abs_v",
    ):
        summary[field] = worst.get(field)
    return summary, review_details, task_metric_rows


def build_precision_overview() -> dict[str, Any]:
    overview = read_json(OVERVIEW_JSON)
    spectre_self = read_json_optional(SPECTRE_SELF_CONSISTENCY_JSON)
    historical_fourway = read_json(HISTORICAL_FOURWAY_REFERENCE_JSON)
    metadata = metadata_by_key(overview)

    reference_rows = load_spectre_summary_rows(FULL300_SPECTRE_STRICT_SUMMARY, metadata)
    surfaces = [
        {
            "candidate": "evas_python",
            "candidate_label": "EVAS Python full-300",
            "rows": load_evas_summary_rows(FULL300_EVAS_PYTHON_SUMMARY, metadata),
        },
        {
            "candidate": "evas_rust",
            "candidate_label": "EVAS Rust full-300",
            "rows": load_evas_summary_rows(FULL300_EVAS_RUST_SUMMARY, metadata),
        },
        {
            "candidate": "spectre_ax",
            "candidate_label": "Spectre AX full-300",
            "rows": load_spectre_summary_rows(FULL300_SPECTRE_AX_SUMMARY, metadata),
        },
    ]

    rows = []
    review_details: list[dict[str, Any]] = []
    task_metric_rows: list[dict[str, Any]] = []
    common_key_sets = []
    for surface in surfaces:
        row, reviews, metric_rows = compare_surface(surface, surface["rows"], reference_rows)
        rows.append(row)
        review_details.extend(reviews)
        task_metric_rows.extend(metric_rows)
        common_key_sets.append(set(surface["rows"]) & set(reference_rows))

    common_rows = len(set.intersection(*common_key_sets)) if common_key_sets else 0
    benchmark_rows = overview.get("summary", {}).get("form_count")
    precision_total = sum(int(row.get("compared_rows") or 0) for row in rows)
    precision_pass = sum(int(row.get("equivalent_rows") or 0) for row in rows)
    precision_review = sum(int(row.get("needs_review_rows") or 0) for row in rows)
    precision_blocked = sum(int(row.get("blocked_rows") or 0) for row in rows)
    all_equivalent = bool(rows) and precision_total > 0 and precision_pass == precision_total and precision_review == 0 and precision_blocked == 0
    if not all_equivalent and precision_total == 0:
        cached = read_cached_precision_report(benchmark_rows)
        if cached is not None:
            return cached

    spectre_summary = spectre_self.get("summary", {}) if isinstance(spectre_self.get("summary"), dict) else {}
    simulator_summary = spectre_summary.get("simulator_style_summary", {})
    relative = simulator_summary.get("relative_rms_error", {}) if isinstance(simulator_summary, dict) else {}
    absolute = simulator_summary.get("absolute_voltage_error", {}) if isinstance(simulator_summary, dict) else {}
    behavior = simulator_summary.get("behavior", {}) if isinstance(simulator_summary, dict) else {}
    waveform = simulator_summary.get("waveform", {}) if isinstance(simulator_summary, dict) else {}
    historical_scope = historical_fourway.get("scope", {}) if isinstance(historical_fourway.get("scope"), dict) else {}

    payload = {
        "date": date.today().isoformat(),
        "status": "pass" if all_equivalent else "needs_review",
        "precision_source": "full300_current_summaries",
        "summary": {
            "bit_exact_claim": "not_asserted",
            "benchmark_management_rows": benchmark_rows,
            "fourway_common_rows": common_rows,
            "precision_evidence_rows": common_rows,
            "precision_evidence_gap_rows": (
                benchmark_rows - common_rows if isinstance(benchmark_rows, int) else None
            ),
            "historical_fourway_common_rows": historical_scope.get("common_row_count"),
            "fourway_candidate_count": len(rows),
            "precision_total_comparisons": precision_total,
            "precision_pass_comparisons": precision_pass,
            "precision_needs_review_comparisons": precision_review,
            "precision_blocked_comparisons": precision_blocked,
            "all_fourway_candidates_equivalent": all_equivalent,
            "needs_review_or_blocked_rows": precision_review + precision_blocked,
            "task_metric_comparisons": sum(int(row.get("task_metric_rows") or 0) for row in rows),
            "spectre_self_consistency_pairs": spectre_summary.get("compared_pairs"),
            "spectre_self_consistency_pass_pairs": spectre_summary.get("passed_pairs"),
            "spectre_self_consistency_needs_review_pairs": spectre_summary.get("needs_review_pairs"),
            "spectre_self_consistency_pass_fraction": spectre_summary.get("pass_fraction_compared"),
        },
        "claim_boundary": {
            "allowed": [
                "The public benchmark management denominator is 300 released rows.",
                "All 300 rows currently have common-row precision evidence for EVAS Python, EVAS Rust, and Spectre AX versus Spectre strict.",
                "EVAS Python, EVAS Rust, and Spectre AX are equivalent to Spectre strict on the full-300 row set under the stated behavior, waveform, edge-window, and task-metric gates.",
                "Task-metric rows may be reported with their metric gate and diagnostic pointwise waveform drift side by side.",
            ],
            "forbidden": [
                "Do not claim bit-exact waveform equality.",
                "Do not reduce tolerance to one global decimal precision.",
                "Do not treat raw pointwise RMS as the sole acceptance rule for task-metric rows.",
                "Do not claim EVAS is more accurate than Spectre AX.",
                "Do not treat the historical 271-row four-way artifact as the current benchmark denominator.",
            ],
        },
        "historical_reference": {
            "common_rows": historical_scope.get("common_row_count"),
            "role": "provenance_only_superseded_by_full300_current_summaries",
            "artifact": rel(HISTORICAL_FOURWAY_REFERENCE_JSON),
        },
        "simulator_precision_rows": rows,
        "needs_review_rows": review_details,
        "task_metric_rows": task_metric_rows,
        "pointwise_difference_taxonomy": POINTWISE_DIFFERENCE_TAXONOMY,
        "spectre_self_consistency": {
            "artifact_status": spectre_self.get("artifact_status"),
            "artifact": spectre_self.get("artifact"),
            "mode_a": spectre_self.get("mode_a"),
            "mode_b": spectre_self.get("mode_b"),
            "sample_n": spectre_self.get("sample_n"),
            "total_pairs": spectre_summary.get("total_pairs"),
            "compared_pairs": spectre_summary.get("compared_pairs"),
            "passed_pairs": spectre_summary.get("passed_pairs"),
            "needs_review_pairs": spectre_summary.get("needs_review_pairs"),
            "pass_fraction_compared": spectre_summary.get("pass_fraction_compared"),
            "behavior_pass_pairs": behavior.get("pass_pairs"),
            "behavior_fail_pairs": behavior.get("fail_pairs"),
            "waveform_compared_pairs": waveform.get("compared_pairs"),
            "waveform_pass_pairs": waveform.get("pass_pairs"),
            "row_mean_relative_rms_max": relative.get("row_mean_max"),
            "worst_signal_relative_rms_max": relative.get("worst_signal_max"),
            "worst_signal_relative_rms_median": relative.get("worst_signal_median"),
            "max_point_abs_v": absolute.get("max_point_v"),
            "max_rms_v": absolute.get("max_rms_v"),
            "median_rms_v": absolute.get("median_rms_v"),
        },
        "gates": [
            {
                "name": "behavior_checker",
                "label": "Behavior checker",
                "threshold": "deterministic task-specific PASS",
                "meaning": "Circuit-level function is the primary acceptance signal.",
            },
            {
                "name": "relative_waveform",
                "label": "Relative waveform RMS",
                "threshold": "row_mean<=0.10 and worst_signal<=0.22, or row_mean<=0.08 and worst_signal<=0.25",
                "meaning": "Pointwise waveform differences are accepted only when normalized RMS error stays inside the gate.",
            },
            {
                "name": "small_absolute_voltage",
                "label": "Small absolute voltage",
                "threshold": "max_rmse_v<=0.05 and max_abs_v<=0.30",
                "meaning": "Rows with small absolute voltage error can pass even when relative error is inflated by tiny signal spans.",
            },
            {
                "name": "edge_window",
                "label": "Edge/discontinuity window",
                "threshold": "at most 8% of the common sample grid may be excluded when localized to signal activity",
                "meaning": "Solver sampling around discontinuities is not treated as a functional mismatch when the stable region matches.",
            },
            {
                "name": "task_metric",
                "label": "Task metric",
                "threshold": "checker-owned gain, PLL, lock, frequency, or control tolerance",
                "meaning": "Some rows are judged by extracted circuit metrics rather than point-by-point waveform equality.",
            },
        ],
        "interpretation": {
            "are_they_identical": "No. Bit-exact equality is not asserted.",
            "what_is_equal": "The full 300-row release has common-row precision evidence, and the compared surfaces pass the stated acceptance gates.",
            "what_differs": "Remaining numerical differences are dominated by solver sampling, event timing, edge/discontinuity windows, interpolation, transition/cross behavior, and task-specific metric extraction.",
            "how_to_read_tolerance": "Tolerance is not one global decimal precision. It is a set of acceptance gates, with Spectre AX/classic self-consistency used as an anchor for waveform drift that exists inside official Spectre modes.",
            "row_count_scope": "The benchmark management denominator and the current precision evidence row count are both 300. The older 271-row artifact is retained only as historical provenance.",
            "task_metric_scope": "Rows such as gain extraction measurement flows are accepted by extracted circuit metrics; diagnostic pointwise RMS is shown only to prevent misreading waveform drift as a functional failure.",
        },
        "source_reports": {
            "full300_spectre_strict_summary": rel(FULL300_SPECTRE_STRICT_SUMMARY),
            "full300_spectre_ax_summary": rel(FULL300_SPECTRE_AX_SUMMARY),
            "full300_evas_python_summary": rel(FULL300_EVAS_PYTHON_SUMMARY),
            "full300_evas_rust_summary": rel(FULL300_EVAS_RUST_SUMMARY),
            "spectre_ax_classic_self_consistency": rel(SPECTRE_SELF_CONSISTENCY_JSON),
            "historical_fourway_271_reference": rel(HISTORICAL_FOURWAY_REFERENCE_JSON),
        },
    }
    return payload


def write_md(report: dict[str, Any]) -> None:
    summary = report["summary"]
    spectre_self_status = report.get("spectre_self_consistency", {}).get("artifact_status", "available")
    spectre_self_line = (
        "missing"
        if spectre_self_status == "missing"
        else f"{summary['spectre_self_consistency_pass_pairs']} / {summary['spectre_self_consistency_pairs']} pairs passed"
    )
    lines = [
        "# vaBench Precision Overview",
        "",
        f"Date: {report['date']}",
        f"Status: `{report['status']}`",
        f"Precision source: `{report['precision_source']}`",
        "",
        "## Headline",
        "",
        f"- Bit-exact claim: `{summary['bit_exact_claim']}`.",
        f"- Benchmark management rows: {summary['benchmark_management_rows']}.",
        f"- Current common precision rows: {summary['precision_evidence_rows']}.",
        f"- Precision evidence gap rows: {summary['precision_evidence_gap_rows']}.",
        f"- Surface-row comparisons passed: {summary['precision_pass_comparisons']} / {summary['precision_total_comparisons']}.",
        f"- Needs-review or blocked comparisons: {summary['needs_review_or_blocked_rows']}.",
        f"- Task-metric comparisons: {summary['task_metric_comparisons']}.",
        f"- Historical four-way reference rows: {summary['historical_fourway_common_rows']}.",
        f"- Spectre AX/classic self-consistency: {spectre_self_line}.",
        "",
        "## Precision vs Spectre Strict",
        "",
        "| Surface | Equivalent Rows | Task-Metric Rows | Effective Mean Rel RMS | Effective Worst-Signal Rel RMS | Raw Mean Rel RMS | Raw Worst-Signal Rel RMS |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in report["simulator_precision_rows"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["candidate_label"]),
                    f"{row['equivalent_rows']} / {row['compared_rows']}",
                    fmt(row.get("task_metric_rows")),
                    fmt(row["worst_effective_mean_relative_rms_error"]),
                    fmt(row["worst_effective_signal_relative_rms_error"]),
                    fmt(row["worst_raw_mean_relative_rms_error"]),
                    fmt(row["worst_raw_signal_relative_rms_error"]),
                ]
            )
            + " |"
        )
    if report.get("task_metric_rows"):
        lines.extend(
            [
                "",
                "## Task-Metric Rows",
                "",
                "| Surface | Row | Metric Delta | Diagnostic Waveform Status | Diagnostic Mean Rel RMS | Diagnostic Worst-Signal Rel RMS |",
                "| --- | --- | ---: | --- | ---: | ---: |",
            ]
        )
        for row in report["task_metric_rows"]:
            lines.append(
                "| "
                + " | ".join(
                    [
                        str(row["candidate_label"]),
                        f"{row['release_entry_id']}:{row['form']}",
                        fmt(row.get("relative_gain_delta")),
                        str(row.get("diagnostic_waveform_status")),
                        fmt(row.get("diagnostic_waveform_mean_relative_rms_error")),
                        fmt(row.get("diagnostic_waveform_worst_signal_relative_rms_error")),
                    ]
                )
                + " |"
            )
    anchor = report["spectre_self_consistency"]
    lines.extend(
        [
            "",
            "## Spectre AX/Classic Self-Consistency Anchor",
            "",
            "| Metric | Value |",
            "| --- | ---: |",
            f"| compared pairs | {anchor['compared_pairs']} |",
            f"| passed pairs | {anchor['passed_pairs']} |",
            f"| needs review pairs | {anchor['needs_review_pairs']} |",
            f"| row mean relative RMS max | {fmt(anchor['row_mean_relative_rms_max'])} |",
            f"| worst-signal relative RMS max | {fmt(anchor['worst_signal_relative_rms_max'])} |",
            f"| max point absolute voltage | {fmt(anchor['max_point_abs_v'])} |",
            "",
            "## Pointwise Difference Taxonomy",
            "",
        ]
    )
    for item in report["pointwise_difference_taxonomy"]:
        lines.extend(
            [
                f"### {item['label']}",
                "",
                f"- Why expected: {item['why_expected']}",
                f"- What changes: {item['what_changes']}",
                f"- Current shortcoming: {item['known_shortcoming']}",
                f"- Current handling: {item['current_handling']}",
                f"- Bug signal: {item['bug_signal']}",
                f"- Useful feedback: {item['feedback_wanted']}",
                f"- Reporting rule: {item['reporting_rule']}",
                "",
            ]
        )
    lines.extend(["", "## Interpretation", ""])
    for value in report["interpretation"].values():
        lines.append(f"- {value}")
    lines.extend(["", "## Source Reports", ""])
    for label, path in report["source_reports"].items():
        lines.append(f"- `{label}`: `{path}`")
    PRECISION_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def export_precision_overview() -> dict[str, Path]:
    report = build_precision_overview()
    write_json(PRECISION_JSON, report)
    write_json(DOCS_PRECISION_JSON, report)
    write_md(report)
    return {
        "precision_json": PRECISION_JSON,
        "precision_md": PRECISION_MD,
        "docs_precision_json": DOCS_PRECISION_JSON,
    }


def main() -> None:
    written = export_precision_overview()
    for name, path in written.items():
        print(f"{name}: {rel(path)}")


if __name__ == "__main__":
    main()
