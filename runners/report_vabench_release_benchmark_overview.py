#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
REPORTS_ROOT = PACKAGE_ROOT / "reports"
REPORT_JSON = REPORTS_ROOT / "benchmark_overview.json"
REPORT_MD = REPORTS_ROOT / "benchmark_overview.md"
ENTRY_CSV = REPORTS_ROOT / "benchmark_overview_entries.csv"
FORM_CSV = REPORTS_ROOT / "benchmark_overview_forms.csv"
CATEGORY_CSV = REPORTS_ROOT / "benchmark_overview_categories.csv"
VABENCH300_MANIFEST = PACKAGE_ROOT / "vabench-300-expansion" / "VABENCH_300_MANIFEST.json"
CONTENT_CONTRACT_REPORT = REPORTS_ROOT / "content_contract_audit.json"
VABENCH300_CLOSURE_REPORT = ROOT / "speed-optimization" / "reports" / "vabench300_p0_p2_closure_20260620.md"
SPECTRE_AX_SUBSET_REPORT = (
    ROOT / "speed-optimization" / "reports" / "e2e_wall_unified_full_20260602_r14_core_fastpath_exactrows.json"
)
EVAS_PYTHON_RUST_SUBSET_REPORT = (
    ROOT / "speed-optimization" / "reports" / "current_rust_python_evas_topwall10_20260603.json"
)
SPECTRE_REFERENCE_FULL300_SUMMARY = (
    ROOT / "results" / "vabench-300-dual-reference-rust-checker29-full-20260622" / "summary.json"
)
SPECTRE_AX_FULL300_SUMMARY = (
    ROOT / "results" / "vabench-300-dual-ax-rust-checker29-full-20260622" / "summary.json"
)
EVAS_RUST_FULL300_SUMMARY = (
    ROOT / "results" / "vabench-300-evas-rust-full-checker29-metaraw-20260622" / "summary.json"
)
EVAS_PYTHON_FULL300_SUMMARY = (
    ROOT / "results" / "vabench-300-evas-python-full-checker29-metaraw-20260622" / "summary.json"
)
V11_FRESH_SPECTRE_REPORT = REPORTS_ROOT / "vabench_300_v11_fresh_spectre_rerun.json"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def as_bool(value: Any) -> bool:
    return bool(value) if value is not None else False


def as_float(value: Any) -> float | None:
    return value if isinstance(value, (int, float)) else None


def as_int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def level_from_legacy_entry(entry_id: str) -> str:
    if "_l1_" in entry_id:
        return "L1"
    if "_l2_" in entry_id:
        return "L2"
    return ""


def csv_value(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, sort_keys=True)
    if value is True:
        return "True"
    if value is False:
        return "False"
    return "" if value is None else str(value)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_value(row.get(field)) for field in fieldnames})


def fmt(value: Any, digits: int = 3) -> str:
    if value is None:
        return "-"
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if value == 0:
            return "0"
        if abs(value) >= 1000 or abs(value) < 0.001:
            return f"{value:.{digits}e}"
        return f"{value:.{digits}g}"
    return str(value)


def max_or_none(values: list[float | None]) -> float | None:
    present = [value for value in values if value is not None]
    return max(present) if present else None


def first_present(*values: Any) -> Any:
    for value in values:
        if value is not None:
            return value
    return None


def policy_name(policy: Any, parity: dict[str, Any]) -> str:
    if isinstance(policy, dict):
        return str(policy.get("policy", "waveform_policy"))
    if isinstance(policy, str):
        return policy
    mode = parity.get("mode")
    if mode:
        return str(mode)
    return "unknown"


def digital_mismatch_max(parity: dict[str, Any]) -> float | None:
    values: list[float] = []
    per_signal = parity.get("per_signal")
    if isinstance(per_signal, dict):
        for signal in per_signal.values():
            if isinstance(signal, dict) and isinstance(signal.get("mismatch_ratio"), (int, float)):
                values.append(float(signal["mismatch_ratio"]))
    return max(values) if values else None


def special_metric_summary(parity: dict[str, Any]) -> dict[str, Any]:
    metrics = parity.get("metrics")
    deltas: dict[str, Any] = {}
    if isinstance(metrics, dict):
        for key, value in parity.items():
            if key.endswith("_delta") or key.endswith("_delta_s") or key.endswith("_delta_v") or key.endswith("_rel_delta"):
                deltas[key] = value
    if isinstance(parity.get("relative_gain_delta"), (int, float)):
        deltas["relative_gain_delta"] = parity["relative_gain_delta"]
    return {
        "mode": parity.get("mode"),
        "task_family": parity.get("task_family"),
        "policy": parity.get("policy"),
        "gain_gate": parity.get("gain_gate"),
        "deltas": deltas,
    }


def build_form_rows(
    dual: dict[str, Any],
    score_forms: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], Counter[str]]:
    rows: list[dict[str, Any]] = []
    evidence_by_task: dict[str, dict[str, Any]] = {}
    policy_counts: Counter[str] = Counter()

    for task_report in dual.get("task_reports", []):
        if not isinstance(task_report, dict):
            continue
        evidence_path = str(task_report.get("evidence", ""))
        evidence = read_json(ROOT / evidence_path) if evidence_path else {}
        task_id = str(evidence.get("task_id") or task_report.get("task_id") or "")
        entry_id = str(evidence.get("release_entry_id") or task_report.get("entry_id") or "")
        form = str(evidence.get("task_form") or task_report.get("form") or "")
        taxonomy = evidence.get("taxonomy", {}) if isinstance(evidence.get("taxonomy"), dict) else {}
        parity = evidence.get("release_rerun", {}).get("parity", {})
        if not isinstance(parity, dict):
            parity = {}
        policy = policy_name(parity.get("policy"), parity)
        policy_counts[policy] += 1
        score_row = score_forms.get(task_id, {})
        source_equivalence = evidence.get("source_equivalence", {})
        if not isinstance(source_equivalence, dict):
            source_equivalence = {}
        artifacts = evidence.get("artifacts", [])
        gold_assets = source_equivalence.get("release_gold") or [
            item for item in artifacts if isinstance(item, str) and "/gold/" in item
        ]
        if not isinstance(gold_assets, list):
            gold_assets = []
        special = special_metric_summary(parity)

        row = {
            "release_entry_id": entry_id,
            "task_id": task_id,
            "form": form,
            "level": taxonomy.get("level") or score_row.get("level"),
            "track": score_row.get("track"),
            "difficulty": score_row.get("difficulty"),
            "category": taxonomy.get("category") or score_row.get("category"),
            "base_function": taxonomy.get("base_function") or score_row.get("base_function"),
            "counted_in_score": as_bool(score_row.get("counted_in_score")),
            "content_denominator_included": as_bool(score_row.get("content_denominator_included")),
            "static": evidence.get("static"),
            "evas": evidence.get("evas"),
            "spectre": evidence.get("spectre"),
            "verdict": evidence.get("verdict"),
            "source_equivalence_pass": as_bool(source_equivalence.get("pass")),
            "parity_status": parity.get("status"),
            "parity_policy": policy,
            "signals_compared": parity.get("signals_compared"),
            "samples": parity.get("samples"),
            "common_window_s": parity.get("common_window_s"),
            "mean_relative_rms_error": parity.get("mean_relative_rms_error"),
            "max_relative_rms_error": parity.get("max_relative_rms_error"),
            "max_rmse_v": parity.get("max_rmse_v"),
            "max_abs_v": parity.get("max_abs_v"),
            "max_digital_mismatch_ratio": digital_mismatch_max(parity),
            "relative_gain_delta": parity.get("relative_gain_delta"),
            "special_metric_summary": special,
            "evidence": evidence_path,
            "gold_assets": gold_assets,
        }
        rows.append(row)
        evidence_by_task[task_id] = row

    rows.sort(key=lambda item: (str(item.get("release_entry_id")), str(item.get("form"))))
    return rows, evidence_by_task, policy_counts


def build_entry_rows(manifest: dict[str, Any], form_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    forms_by_entry: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in form_rows:
        forms_by_entry[str(row.get("release_entry_id"))].append(row)

    rows: list[dict[str, Any]] = []
    for entry in manifest.get("entries", []):
        if not isinstance(entry, dict):
            continue
        entry_id = str(entry.get("release_entry_id"))
        forms = forms_by_entry.get(entry_id, [])
        waveform_forms = [
            row
            for row in forms
            if row.get("mean_relative_rms_error") is not None or row.get("max_relative_rms_error") is not None
        ]
        gain_forms = [row for row in forms if row.get("relative_gain_delta") is not None]
        special_forms = [row for row in forms if row.get("parity_policy") in {"pll_task_aware", "gain_extraction_metric_parity_v1"}]
        policies = sorted({str(row.get("parity_policy")) for row in forms if row.get("parity_policy")})
        evidence_paths = sorted({str(row.get("evidence")) for row in forms if row.get("evidence")})
        form_count = len(forms) if forms else entry.get("form_count")
        row = {
            "release_entry_id": entry_id,
            "level": entry.get("level") or (forms[0].get("level") if forms else ""),
            "track": entry.get("track") or (forms[0].get("track") if forms else ""),
            "difficulty": entry.get("difficulty") or (forms[0].get("difficulty") if forms else ""),
            "category": entry.get("category") or (forms[0].get("category") if forms else ""),
            "base_function": entry.get("base_function") or (forms[0].get("base_function") if forms else ""),
            "form_count": form_count,
            "forms": sorted({str(form.get("form")) for form in forms}) if forms else entry.get("forms", []),
            "counted_in_score": any(as_bool(form.get("counted_in_score")) for form in forms)
            if forms
            else as_bool(entry.get("counted_in_score")),
            "content_denominator_included": any(as_bool(form.get("content_denominator_included")) for form in forms)
            if forms
            else as_bool(entry.get("content_denominator_included")),
            "certification": "certified" if forms and all(form.get("certification") == "certified" for form in forms) else entry.get("certification"),
            "static": "pass" if forms and all(form.get("static") == "pass" for form in forms) else entry.get("static"),
            "evas": "pass" if forms and all(form.get("evas") == "pass" for form in forms) else entry.get("evas"),
            "spectre": "pass" if forms and all(form.get("spectre") == "pass" for form in forms) else entry.get("spectre"),
            "waveform_form_count": len(waveform_forms),
            "special_metric_form_count": len(special_forms),
            "gain_metric_form_count": len(gain_forms),
            "worst_mean_relative_rms_error": max_or_none([as_float(row.get("mean_relative_rms_error")) for row in waveform_forms]),
            "worst_signal_relative_rms_error": max_or_none([as_float(row.get("max_relative_rms_error")) for row in waveform_forms]),
            "worst_max_rmse_v": max_or_none([as_float(row.get("max_rmse_v")) for row in waveform_forms]),
            "worst_max_abs_v": max_or_none([as_float(row.get("max_abs_v")) for row in waveform_forms]),
            "max_digital_mismatch_ratio": max_or_none([as_float(row.get("max_digital_mismatch_ratio")) for row in waveform_forms]),
            "max_relative_gain_delta": max_or_none([as_float(row.get("relative_gain_delta")) for row in gain_forms]),
            "parity_policies": policies,
            "evidence_count": len(evidence_paths),
            "evidence_paths": evidence_paths,
        }
        rows.append(row)
    known_entries = {str(row["release_entry_id"]) for row in rows}
    for entry_id, forms in sorted(forms_by_entry.items()):
        if not entry_id or entry_id in known_entries:
            continue
        waveform_forms = [
            row
            for row in forms
            if row.get("mean_relative_rms_error") is not None or row.get("max_relative_rms_error") is not None
        ]
        gain_forms = [row for row in forms if row.get("relative_gain_delta") is not None]
        special_forms = [row for row in forms if row.get("parity_policy") in {"pll_task_aware", "gain_extraction_metric_parity_v1"}]
        policies = sorted({str(row.get("parity_policy")) for row in forms if row.get("parity_policy")})
        evidence_paths = sorted({str(row.get("evidence")) for row in forms if row.get("evidence")})
        first = forms[0]
        rows.append(
            {
                "release_entry_id": entry_id,
                "level": first.get("level"),
                "track": first.get("track"),
                "difficulty": first.get("difficulty"),
                "category": first.get("category"),
                "base_function": first.get("base_function"),
                "form_count": len(forms),
                "forms": sorted({str(form.get("form")) for form in forms}),
                "counted_in_score": any(as_bool(form.get("counted_in_score")) for form in forms),
                "content_denominator_included": any(
                    as_bool(form.get("content_denominator_included")) for form in forms
                ),
                "certification": "certified" if all(form.get("certification") == "certified" for form in forms) else "",
                "static": "pass" if all(form.get("static") == "pass" for form in forms) else "",
                "evas": "pass" if all(form.get("evas") == "pass" for form in forms) else "",
                "spectre": "pass" if all(form.get("spectre") == "pass" for form in forms) else "",
                "waveform_form_count": len(waveform_forms),
                "special_metric_form_count": len(special_forms),
                "gain_metric_form_count": len(gain_forms),
                "worst_mean_relative_rms_error": max_or_none(
                    [as_float(row.get("mean_relative_rms_error")) for row in waveform_forms]
                ),
                "worst_signal_relative_rms_error": max_or_none(
                    [as_float(row.get("max_relative_rms_error")) for row in waveform_forms]
                ),
                "worst_max_rmse_v": max_or_none([as_float(row.get("max_rmse_v")) for row in waveform_forms]),
                "worst_max_abs_v": max_or_none([as_float(row.get("max_abs_v")) for row in waveform_forms]),
                "max_digital_mismatch_ratio": max_or_none(
                    [as_float(row.get("max_digital_mismatch_ratio")) for row in waveform_forms]
                ),
                "max_relative_gain_delta": max_or_none([as_float(row.get("relative_gain_delta")) for row in gain_forms]),
                "parity_policies": policies,
                "evidence_count": len(evidence_paths),
                "evidence_paths": evidence_paths,
            }
        )
    rows.sort(key=lambda item: str(item["release_entry_id"]))
    return rows


def build_category_rows(entry_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in entry_rows:
        groups[str(row.get("category"))].append(row)
    rows: list[dict[str, Any]] = []
    for category, items in sorted(groups.items()):
        rows.append(
            {
                "category": category,
                "entry_count": len(items),
                "form_count": sum(as_int(item.get("form_count")) for item in items),
                "core_entry_count": sum(1 for item in items if item.get("track") == "core"),
                "support_entry_count": sum(1 for item in items if item.get("track") == "support"),
                "l1_entry_count": sum(1 for item in items if item.get("level") == "L1"),
                "l2_entry_count": sum(1 for item in items if item.get("level") == "L2"),
                "scored_entry_count": sum(1 for item in items if item.get("counted_in_score")),
                "scored_form_count": sum(as_int(item.get("form_count")) for item in items if item.get("counted_in_score")),
                "certified_entry_count": sum(1 for item in items if item.get("certification") == "certified"),
            }
        )
    return rows


def build_vabench300_expansion(manifest_summary: dict[str, Any]) -> dict[str, Any]:
    expansion = read_json(VABENCH300_MANIFEST)
    if not expansion:
        return {
            "status": "absent_in_current_checkout",
            "manifest": rel(VABENCH300_MANIFEST),
            "release_v1_form_count": as_int(manifest_summary.get("form_count")),
            "explanation": "The current checkout source of truth is the release-v1 manifest. A 300-task expansion package is a separate v1.1/closure surface and must not be counted as certified release-v1 forms unless it is present and promoted with certification evidence.",
        }

    summary = expansion.get("summary", {}) if isinstance(expansion.get("summary"), dict) else {}
    tasks = [row for row in expansion.get("tasks", []) if isinstance(row, dict)]
    return {
        "status": "present",
        "manifest": rel(VABENCH300_MANIFEST),
        "task_count": as_int(summary.get("task_count")),
        "certified_task_count": as_int(summary.get("certified_task_count")),
        "existing_certified_v1_task_count": as_int(summary.get("existing_certified_v1_task_count")),
        "proposed_v11_task_count": as_int(summary.get("proposed_v11_task_count")),
        "promoted_v11_task_count": as_int(summary.get("promoted_v11_task_count")),
        "provisional_v11_task_count": as_int(summary.get("provisional_v11_task_count")),
        "task_specific_v11_task_count": as_int(summary.get("task_specific_v11_task_count")),
        "provisional_generic_v11_task_count": as_int(summary.get("provisional_generic_v11_task_count")),
        "pending_certification_task_count": as_int(summary.get("pending_certification_task_count")),
        "paper_score_ready_task_count": as_int(summary.get("paper_score_ready_task_count")),
        "paper_score_disabled_v11_task_count": as_int(summary.get("paper_score_disabled_v11_task_count")),
        "counted_in_score_task_count": sum(1 for row in tasks if as_bool(row.get("counted_in_score"))),
        "partial_pass_negative_count": as_int(summary.get("partial_pass_negative_count")),
        "negative_static_shallow_shape_verified_count": as_int(
            summary.get("negative_static_shallow_shape_verified_count")
        ),
        "negative_simulator_shallow_verified_count": as_int(summary.get("negative_simulator_shallow_verified_count")),
        "negative_full_checker_fail_verified_count": as_int(summary.get("negative_full_checker_fail_verified_count")),
        "task_specific_v11_gold_pass_count": as_int(summary.get("task_specific_v11_gold_pass_count")),
        "task_specific_v11_negative_full_checker_fail_count": as_int(
            summary.get("task_specific_v11_negative_full_checker_fail_count")
        ),
        "fresh_spectre_v11_pass_count": as_int(summary.get("fresh_spectre_v11_pass_count")),
        "fresh_spectre_v11_nonpass_count": as_int(summary.get("fresh_spectre_v11_nonpass_count")),
        "fresh_spectre_v11_parity_pass_count": as_int(summary.get("fresh_spectre_v11_parity_pass_count")),
        "score_denominator_pending_v11_task_count": as_int(
            summary.get("score_denominator_pending_v11_task_count")
        ),
        "score_denominator_admitted_v11_task_count": as_int(
            summary.get("score_denominator_admitted_v11_task_count")
        ),
        "v11_task_specific_quality_evidence": expansion.get("v11_task_specific_quality_evidence"),
        "v11_fresh_spectre_rerun_evidence": expansion.get("v11_fresh_spectre_rerun_evidence"),
        "closure_report": rel(VABENCH300_CLOSURE_REPORT),
        "explanation": "This is the primary vaBench 300 management surface: 271 inherited certified v1 rows plus 29 task-specific v1.1 rows with fresh EVAS/Spectre PASS evidence. After score-denominator admission, all 300 rows are simulator-certified assets and 265 core rows are counted in the paper-facing model-evaluation denominator after support-suite exclusions.",
    }


def build_backend_coverage(
    task_count: int,
    provisional_v11_task_count: int = 0,
    score_denominator_pending_v11_task_count: int = 0,
) -> dict[str, Any]:
    blocker_note = ""
    if provisional_v11_task_count:
        blocker_note = f" {provisional_v11_task_count} provisional v1.1 rows block a 300-row certification claim."
    elif score_denominator_pending_v11_task_count:
        blocker_note = (
            f" {score_denominator_pending_v11_task_count} fresh-certified v1.1 rows are still score-denominator pending."
        )

    def no_checker_count(summary: dict[str, Any]) -> int:
        count = 0
        for item in summary.get("results", []):
            raw = item.get("raw_result") if isinstance(item, dict) else None
            if not isinstance(raw, dict):
                continue
            notes = raw.get("notes", [])
            if not isinstance(notes, list):
                notes = []
            evas_notes = []
            evas = raw.get("evas")
            if isinstance(evas, dict) and isinstance(evas.get("notes"), list):
                evas_notes = evas["notes"]
            all_notes = [str(note) for note in [*notes, *evas_notes]]
            if any("no behavior check implemented" in note for note in all_notes):
                count += 1
        return count

    def spectre_ok_count(summary: dict[str, Any]) -> int:
        count = 0
        for item in summary.get("results", []):
            raw = item.get("raw_result") if isinstance(item, dict) else None
            spectre = raw.get("spectre") if isinstance(raw, dict) else None
            if isinstance(spectre, dict) and spectre.get("ok") is True:
                count += 1
        return count

    def dual_row(backend: str, label: str, path: Path) -> dict[str, Any]:
        summary = read_json(path)
        if not summary:
            return {
                "backend": backend,
                "label": label,
                "full_300_status": "missing_full_300",
                "run_completed": False,
                "certification_passed": False,
                "rows": None,
                "total": task_count,
                "evidence": rel(path),
                "notes": "No current full-300 summary is present.",
            }
        pass_count = as_int(summary.get("pass_count"))
        nonpass_count = as_int(summary.get("nonpass_count"))
        no_checker = no_checker_count(summary)
        spectre_ok = spectre_ok_count(summary)
        raw_status = "pass" if pass_count == task_count and nonpass_count == 0 else "checker_pending"
        if raw_status == "pass" and provisional_v11_task_count:
            status = "pass_with_provisional_rows"
        elif raw_status == "pass" and score_denominator_pending_v11_task_count:
            status = "pass_with_score_pending_v11_rows"
        else:
            status = raw_status
        return {
            "backend": backend,
            "label": label,
            "full_300_status": status,
            "run_completed": summary.get("status") == "complete",
            "certification_passed": raw_status == "pass"
            and provisional_v11_task_count == 0
            and score_denominator_pending_v11_task_count == 0,
            "rows": pass_count,
            "total": task_count,
            "nonpass_rows": nonpass_count,
            "spectre_ok_rows": spectre_ok,
            "no_checker_rows": no_checker,
            "evidence": rel(path),
            "notes": (
                f"dual PASS {pass_count}/{task_count}; Spectre ok {spectre_ok}/{task_count}; "
                f"{no_checker} rows lack behavior checkers.{blocker_note}"
            ),
        }

    def evas_row(backend: str, label: str, path: Path) -> dict[str, Any]:
        summary = read_json(path)
        if not summary:
            return {
                "backend": backend,
                "label": label,
                "full_300_status": "missing_full_300",
                "run_completed": False,
                "certification_passed": False,
                "rows": None,
                "total": task_count,
                "evidence": rel(path),
                "notes": "No current full-300 EVAS-only summary is present.",
            }
        compile_pass = as_int(summary.get("compile_sim_pass_count"))
        behavior_pass = as_int(summary.get("behavior_checker_pass_count"))
        behavior_nonpass = as_int(summary.get("behavior_checker_nonpass_count"))
        behavior_missing = as_int(summary.get("behavior_checker_missing_count"))
        raw_status = "pass" if behavior_pass == task_count and behavior_nonpass == 0 else "compile_sim_pass_behavior_partial"
        if raw_status == "pass" and provisional_v11_task_count:
            status = "pass_with_provisional_rows"
        elif raw_status == "pass" and score_denominator_pending_v11_task_count:
            status = "pass_with_score_pending_v11_rows"
        else:
            status = raw_status
        return {
            "backend": backend,
            "label": label,
            "full_300_status": status,
            "run_completed": summary.get("status") == "pass" and compile_pass == task_count,
            "certification_passed": raw_status == "pass"
            and provisional_v11_task_count == 0
            and score_denominator_pending_v11_task_count == 0,
            "rows": compile_pass,
            "total": task_count,
            "behavior_checker_pass_rows": behavior_pass,
            "behavior_checker_nonpass_rows": behavior_nonpass,
            "behavior_checker_missing_rows": behavior_missing,
            "provisional_v11_behavior_checker_missing_rows": as_int(
                summary.get("provisional_v11_behavior_checker_missing_count")
            ),
            "evidence": rel(path),
            "notes": (
                f"compile/sim PASS {compile_pass}/{task_count}; behavior checker PASS "
                f"{behavior_pass}/{task_count}; missing/nonpass {behavior_missing}/{task_count}.{blocker_note}"
            ),
        }

    rows = [
        dual_row("spectre_reference", "Spectre reference + EVAS Rust dual", SPECTRE_REFERENCE_FULL300_SUMMARY),
        dual_row("spectre_ax", "Spectre AX + EVAS Rust dual", SPECTRE_AX_FULL300_SUMMARY),
        evas_row("evas_rust", "EVAS Rust only", EVAS_RUST_FULL300_SUMMARY),
        evas_row("evas_python", "EVAS Python only", EVAS_PYTHON_FULL300_SUMMARY),
    ]
    completed = sum(1 for row in rows if row.get("run_completed"))
    certified = sum(1 for row in rows if row.get("certification_passed"))
    status = "pass" if certified == len(rows) else "incomplete"
    if provisional_v11_task_count:
        status = "provisional_v11_blocked"
    elif score_denominator_pending_v11_task_count:
        status = "score_denominator_pending_v11_blocked"
    claim_boundary = (
        "Four-backend execution coverage, simulator certification, and score-denominator admission are separate. "
        "All 29 fresh v1.1 rows are admitted to the current score denominator; support-suite exclusions still apply."
        if score_denominator_pending_v11_task_count == 0
        else "Four-backend execution coverage, simulator certification, and score-denominator admission are separate. Fresh v1.1 EVAS/Spectre evidence certifies behavior, but paper scoring still requires score-denominator admission."
    )
    return {
        "status": status,
        "required_backend_count": len(rows),
        "completed_backend_count": completed,
        "certified_backend_count": certified,
        "rows": rows,
        "claim_boundary": claim_boundary,
    }


def build_vabench300_form_rows(
    expansion: dict[str, Any],
    release_v1_form_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if not expansion:
        return release_v1_form_rows
    release_by_entry_form = {
        (str(row.get("release_entry_id")), str(row.get("form"))): row for row in release_v1_form_rows
    }
    fresh_report = read_json(V11_FRESH_SPECTRE_REPORT)
    fresh_by_task = {
        str(row.get("task_id")): row
        for row in fresh_report.get("rows", [])
        if isinstance(row, dict) and row.get("task_id")
    }
    rows: list[dict[str, Any]] = []
    for task in expansion.get("tasks", []):
        if not isinstance(task, dict):
            continue
        entry_id = str(task.get("legacy_entry_id") or task.get("topic_id") or "")
        form = str(task.get("form") or "")
        inherited = dict(release_by_entry_form.get((entry_id, form), {}))
        release_task = read_json(ROOT / str(task.get("release_task_manifest", "")))
        artifacts = release_task.get("artifacts", {}) if isinstance(release_task.get("artifacts"), dict) else {}
        gold_assets = artifacts.get("gold", [])
        if not isinstance(gold_assets, list):
            gold_assets = []
        is_v11 = task.get("expansion_status") in {
            "certified_v1.1_promoted",
            "provisional_v1.1_management",
        }
        fresh = fresh_by_task.get(str(task.get("task_id")), {})
        is_certified = task.get("certification") in {"certified", "fresh_evas_spectre_certified"}
        inherited.update(
            {
                "release_entry_id": entry_id,
                "legacy_task_id": task.get("legacy_task_id"),
                "task_id": task.get("task_id"),
                "form": form,
                "level": inherited.get("level") or level_from_legacy_entry(entry_id),
                "track": task.get("track"),
                "difficulty": task.get("difficulty"),
                "category": task.get("category"),
                "base_function": task.get("base_function"),
                "counted_in_score": as_bool(task.get("counted_in_score")),
                "content_denominator_included": as_bool(task.get("counted_in_score")),
                "static": task.get("static"),
                "evas": task.get("evas"),
                "spectre": task.get("spectre"),
                "certification": "certified" if is_certified else task.get("certification"),
                "verdict": "pass" if is_certified else task.get("certification"),
                "source_equivalence_pass": as_bool(inherited.get("source_equivalence_pass")) if inherited else is_certified,
                "parity_status": inherited.get("parity_status")
                or fresh.get("parity_status")
                or ("provisional" if is_v11 else None),
                "parity_policy": inherited.get("parity_policy")
                or fresh.get("parity_policy")
                or ("full_300_closure_not_score_enabling" if is_v11 else None),
                "signals_compared": first_present(inherited.get("signals_compared"), fresh.get("signals_compared")),
                "samples": first_present(inherited.get("samples"), fresh.get("samples")),
                "common_window_s": first_present(inherited.get("common_window_s"), fresh.get("common_window_s")),
                "mean_relative_rms_error": first_present(
                    inherited.get("mean_relative_rms_error"), fresh.get("mean_relative_rms_error")
                ),
                "max_relative_rms_error": first_present(
                    inherited.get("max_relative_rms_error"), fresh.get("max_relative_rms_error")
                ),
                "max_rmse_v": first_present(inherited.get("max_rmse_v"), fresh.get("max_rmse_v")),
                "max_abs_v": first_present(inherited.get("max_abs_v"), fresh.get("max_abs_v")),
                "evidence": inherited.get("evidence")
                or task.get("fresh_spectre_evidence")
                or (rel(VABENCH300_CLOSURE_REPORT) if is_v11 else ""),
                "gold_assets": gold_assets or inherited.get("gold_assets", []),
                "expansion_status": task.get("expansion_status"),
                "gold_status": task.get("gold_status"),
            }
        )
        rows.append(inherited)
    rows.sort(key=lambda item: (str(item.get("release_entry_id")), str(item.get("form"))))
    return rows


def build_report() -> dict[str, Any]:
    manifest = read_json(PACKAGE_ROOT / "MANIFEST.json")
    dual = read_json(REPORTS_ROOT / "dual_certification.json")
    score = read_json(REPORTS_ROOT / "score_denominator_manifest.json")
    content_contract = read_json(CONTENT_CONTRACT_REPORT)
    dual_staging = read_json(REPORTS_ROOT / "dual_rerun_staging_manifest.json")
    speed_staging = read_json(REPORTS_ROOT / "speed_remaining_staging_manifest.json")

    score_forms = {
        str(row.get("task_id")): row
        for row in score.get("form_rows", [])
        if isinstance(row, dict) and row.get("task_id")
    }
    release_v1_form_rows, _, policy_counts = build_form_rows(dual, score_forms)
    expansion_manifest = read_json(VABENCH300_MANIFEST)
    form_rows = build_vabench300_form_rows(expansion_manifest, release_v1_form_rows)
    entry_rows = build_entry_rows(manifest, form_rows)
    category_rows = build_category_rows(entry_rows)

    manifest_summary = manifest.get("summary", {}) if isinstance(manifest.get("summary"), dict) else {}
    score_summary = score.get("summary", {}) if isinstance(score.get("summary"), dict) else {}
    waveform_rows = [row for row in form_rows if row.get("mean_relative_rms_error") is not None]
    gain_rows = [row for row in form_rows if row.get("relative_gain_delta") is not None]
    pll_rows = [row for row in form_rows if row.get("parity_policy") == "pll_task_aware"]
    parity_passed = [row for row in form_rows if row.get("parity_status") == "passed"]
    all_backend_pass = all(
        row.get("static") == "pass" and row.get("evas") == "pass" and row.get("spectre") == "pass"
        for row in form_rows
    )

    waveform_policy = {
        "bit_exact_claim": "not_asserted",
        "acceptance_basis": "behavior/spec pass plus EVAS/Spectre waveform or task-metric parity",
        "small_absolute_gate": "max_rmse_v<=0.05 and max_abs_v<=0.30",
        "relative_rms_gate": "row_mean_relative_rms_error<=0.10 and worst_signal_relative_rms_error<=0.22; or row_mean_relative_rms_error<=0.08 and worst_signal_relative_rms_error<=0.25",
        "edge_window_policy": "core_v2 rows may exclude a bounded edge/discontinuity window only when local to signal activity, at most 8% of the common sample grid, and stable-region error remains small; raw metrics remain reported.",
        "gain_metric_gate": "evas_gain>4 and spectre_gain>4 and relative_gain_delta<=0.25",
        "pll_task_aware": "PLL rows use task-level lock/frequency/control metrics; status=passed is the certification gate for those special rows.",
    }

    aggregate = {
        "parity_form_count": len(form_rows),
        "parity_passed_form_count": len(parity_passed),
        "waveform_metric_form_count": len(waveform_rows),
        "gain_metric_form_count": len(gain_rows),
        "pll_task_aware_form_count": len(pll_rows),
        "policy_counts": dict(policy_counts),
        "max_mean_relative_rms_error": max_or_none([as_float(row.get("mean_relative_rms_error")) for row in waveform_rows]),
        "max_worst_signal_relative_rms_error": max_or_none([as_float(row.get("max_relative_rms_error")) for row in waveform_rows]),
        "max_rmse_v": max_or_none([as_float(row.get("max_rmse_v")) for row in waveform_rows]),
        "max_abs_v": max_or_none([as_float(row.get("max_abs_v")) for row in waveform_rows]),
        "max_digital_mismatch_ratio": max_or_none([as_float(row.get("max_digital_mismatch_ratio")) for row in waveform_rows]),
        "max_relative_gain_delta": max_or_none([as_float(row.get("relative_gain_delta")) for row in gain_rows]),
    }
    current_rerun_bundles = as_int(dual_staging.get("bundle_count"))
    speed_remaining_bundles = as_int(speed_staging.get("bundle_count"))
    current_primary_rows = as_int(dual_staging.get("queue_row_count"))
    speed_remaining_primary_rows = as_int(speed_staging.get("queue_row_count"))
    current_variants = dual_staging.get("variant_counts", {})
    speed_variants = speed_staging.get("variant_counts", {})
    if not isinstance(current_variants, dict):
        current_variants = {}
    if not isinstance(speed_variants, dict):
        speed_variants = {}
    buggy_companion_bundles = as_int(current_variants.get("buggy")) + as_int(speed_variants.get("buggy"))
    staging_counts = {
        "current_dual_staging_bundles": current_rerun_bundles,
        "speed_remaining_staging_bundles": speed_remaining_bundles,
        "total_staging_bundles": current_rerun_bundles + speed_remaining_bundles,
        "current_primary_queue_rows": current_primary_rows,
        "speed_remaining_primary_queue_rows": speed_remaining_primary_rows,
        "total_primary_queue_rows": current_primary_rows + speed_remaining_primary_rows,
        "buggy_companion_bundles": buggy_companion_bundles,
        "explanation": "Staging bundles are runnable EVAS/Spectre directories. They exceed benchmark forms because bugfix rows also stage buggy companion bundles expected to fail, and those companions are not benchmark denominator rows.",
    }
    vabench300_expansion = build_vabench300_expansion(manifest_summary)
    if vabench300_expansion.get("status") == "present":
        manifest_summary = {
            **manifest_summary,
            "entry_count": len(entry_rows),
            "form_count": vabench300_expansion.get("task_count"),
            "certified_form_count": vabench300_expansion.get("certified_task_count"),
            "pending_form_count": vabench300_expansion.get("pending_certification_task_count"),
            "scored_form_count": vabench300_expansion.get("counted_in_score_task_count"),
            "promoted_v11_task_count": vabench300_expansion.get("promoted_v11_task_count"),
            "provisional_v11_task_count": vabench300_expansion.get("provisional_v11_task_count"),
            "paper_score_ready_task_count": vabench300_expansion.get("paper_score_ready_task_count"),
            "paper_score_disabled_v11_task_count": vabench300_expansion.get("paper_score_disabled_v11_task_count"),
            "existing_certified_v1_task_count": vabench300_expansion.get("existing_certified_v1_task_count"),
            "fresh_spectre_v11_pass_count": vabench300_expansion.get("fresh_spectre_v11_pass_count"),
            "fresh_spectre_v11_nonpass_count": vabench300_expansion.get("fresh_spectre_v11_nonpass_count"),
            "fresh_spectre_v11_parity_pass_count": vabench300_expansion.get("fresh_spectre_v11_parity_pass_count"),
            "score_denominator_pending_v11_task_count": vabench300_expansion.get(
                "score_denominator_pending_v11_task_count"
            ),
            "score_denominator_admitted_v11_task_count": vabench300_expansion.get(
                "score_denominator_admitted_v11_task_count"
            ),
        }

    provisional_v11_task_count = as_int(manifest_summary.get("provisional_v11_task_count"))
    score_denominator_pending_v11_task_count = as_int(
        manifest_summary.get("score_denominator_pending_v11_task_count")
    )
    backend_coverage = build_backend_coverage(
        as_int(manifest_summary.get("form_count")) or len(form_rows),
        provisional_v11_task_count,
        score_denominator_pending_v11_task_count,
    )
    status = "ready" if all_backend_pass and len(parity_passed) == len(form_rows) else "incomplete"
    if provisional_v11_task_count:
        status = "provisional"
    elif score_denominator_pending_v11_task_count:
        status = "score_denominator_pending"
    claim_boundary = [
        "This overview is a derived navigation/reporting table; VABENCH_300_MANIFEST.json is the benchmark management manifest.",
        "Current full-300 backend evidence is grounded by the explicit results/*/summary.json files listed in backend_coverage.",
        "Do not state bit-exact EVAS/Spectre equality; state behavior/spec pass plus tolerance-gated waveform or task-metric parity.",
        "Negative candidates are static-shape audited partial-pass assets unless a separate full-checker validation report is produced.",
    ]
    if score_denominator_pending_v11_task_count:
        claim_boundary.append(
            "Do not count v1.1 rows in the paper score denominator while score_denominator_pending_v11_task_count is nonzero; use paper_score_ready_task_count for paper-facing scoring."
        )
    else:
        claim_boundary.append(
            "All 29 fresh-certified v1.1 rows are score-denominator admitted; support-suite exclusions still apply to paper-facing scores."
        )
    return {
        "release": manifest.get("release", "vabench-release-v1"),
        "date": str(date.today()),
        "status": status,
        "summary": {
            **manifest_summary,
            "score_denominator_status": score.get("status", "missing"),
            "content_contract_status": content_contract.get("status", "missing"),
            "dual_certification_status": "pass" if full300_parity_count == full300_parity_total else "incomplete",
            "dual_certified_release_task_count": full300_parity_count,
            "legacy_dual_certified_v1_task_count": legacy_dual_certified_count,
            "evas_pass_spectre_fail_count": dual.get("evas_pass_spectre_fail_count", 0),
            "dual_failed_release_task_count": max(full300_parity_total - full300_parity_count, 0),
            "dual_pending_release_task_count": 0,
            "score_enabled_entry_count": score_summary.get("scored_entry_count", 0),
            "score_enabled_form_count": score_summary.get("scored_form_count", 0),
            "four_backend_status": backend_coverage["status"],
            "four_backend_completed_backend_count": backend_coverage["completed_backend_count"],
            "four_backend_certified_backend_count": backend_coverage["certified_backend_count"],
            "four_backend_required_backend_count": backend_coverage["required_backend_count"],
        },
        "equivalence_contract": waveform_policy,
        "aggregate_parity_metrics": aggregate,
        "backend_coverage": backend_coverage,
        "vabench300_expansion": vabench300_expansion,
        "staging_bundle_counts": staging_counts,
        "source_reports": {
            "package_manifest": vabench300_expansion.get("manifest") or rel(PACKAGE_ROOT / "MANIFEST.json"),
            "release_v1_manifest": rel(PACKAGE_ROOT / "MANIFEST.json"),
            "vabench300_closure_report": rel(VABENCH300_CLOSURE_REPORT),
            "dual_certification": rel(REPORTS_ROOT / "dual_certification.json"),
            "score_denominator_manifest": rel(REPORTS_ROOT / "score_denominator_manifest.json"),
            "content_contract_audit": rel(CONTENT_CONTRACT_REPORT),
            "dual_rerun_staging_manifest": rel(REPORTS_ROOT / "dual_rerun_staging_manifest.json"),
            "speed_remaining_staging_manifest": rel(REPORTS_ROOT / "speed_remaining_staging_manifest.json"),
            "spectre_ax_subset_report": rel(SPECTRE_AX_SUBSET_REPORT),
            "evas_python_rust_subset_report": rel(EVAS_PYTHON_RUST_SUBSET_REPORT),
            "spectre_reference_full300_summary": rel(SPECTRE_REFERENCE_FULL300_SUMMARY),
            "spectre_ax_full300_summary": rel(SPECTRE_AX_FULL300_SUMMARY),
            "evas_rust_full300_summary": rel(EVAS_RUST_FULL300_SUMMARY),
            "evas_python_full300_summary": rel(EVAS_PYTHON_FULL300_SUMMARY),
            "v11_fresh_spectre_rerun": rel(V11_FRESH_SPECTRE_REPORT),
        },
        "exports": {
            "markdown": rel(REPORT_MD),
            "entries_csv": rel(ENTRY_CSV),
            "forms_csv": rel(FORM_CSV),
            "categories_csv": rel(CATEGORY_CSV),
        },
        "claim_boundary": claim_boundary,
        "category_rows": category_rows,
        "entry_rows": entry_rows,
        "form_rows": form_rows,
    }


def parity_summary(row: dict[str, Any]) -> str:
    parts: list[str] = []
    if as_int(row.get("waveform_form_count")):
        parts.append(
            "wave "
            f"{row.get('waveform_form_count')}/{row.get('form_count')}, "
            f"mean<={fmt(row.get('worst_mean_relative_rms_error'))}, "
            f"worst<={fmt(row.get('worst_signal_relative_rms_error'))}, "
            f"abs<={fmt(row.get('worst_max_abs_v'))}V"
        )
    if as_int(row.get("gain_metric_form_count")):
        parts.append(f"gain delta<={fmt(row.get('max_relative_gain_delta'))}")
    special_count = as_int(row.get("special_metric_form_count")) - as_int(row.get("gain_metric_form_count"))
    if special_count > 0:
        parts.append(f"task metrics {special_count} forms")
    return "; ".join(parts) if parts else "task-specific parity"


def write_markdown(report: dict[str, Any]) -> None:
    summary = report["summary"]
    metrics = report["aggregate_parity_metrics"]
    contract = report["equivalence_contract"]
    backend_coverage = report["backend_coverage"]
    backend_by_id = {row["backend"]: row for row in backend_coverage["rows"]}
    reference_backend = backend_by_id.get("spectre_reference", {})
    expansion = report["vabench300_expansion"]
    staging = report["staging_bundle_counts"]
    pending_v11 = as_int(summary.get("score_denominator_pending_v11_task_count"))
    management_note = (
        f"Use {summary.get('form_count')} as the asset-management and certified-task row count. "
        f"The paper-facing score-ready surface is now {summary.get('paper_score_ready_task_count')} rows; "
        f"{summary.get('promoted_v11_task_count')} fresh-certified v1.1 rows are admitted through the score-denominator audit. "
        "Staging bundle counts are execution inputs, not benchmark size."
        if pending_v11 == 0
        else f"Use {summary.get('form_count')} as the asset-management row count, not as the current paper-scored count. "
        f"The paper-facing score-ready surface is {summary.get('paper_score_ready_task_count')} inherited v1 rows; "
        f"{summary.get('promoted_v11_task_count')} v1.1 rows have task-specific fresh EVAS/Spectre evidence but remain score-disabled until score-denominator admission. "
        "Staging bundle counts are execution inputs, not benchmark size."
    )
    management_row_label = (
        "asset-management and simulator-certified surface"
        if pending_v11 == 0
        else "asset-management surface, including score-pending v1.1 rows"
    )
    score_ready_label = (
        "rows admitted to the current paper-facing score surface"
        if pending_v11 == 0
        else "inherited v1 rows with current paper-facing evidence"
    )
    v11_pending_label = (
        "fresh-certified score-admitted v1.1 rows"
        if pending_v11 == 0
        else "fresh-certified score-pending v1.1 rows"
    )
    v11_pending_meaning = (
        "admitted by v1.1 score admission audit"
        if pending_v11 == 0
        else "excluded from score until denominator admission"
    )
    lines = [
        "# vaBench 300 Benchmark Overview",
        "",
        f"Date: {report['date']}",
        "",
        "This is the single navigation surface for the benchmark. The primary management manifest is the vaBench 300 manifest; release-v1 rows are composition/provenance, not a separate benchmark denominator.",
        "",
        "## Headline Counts",
        "",
        "| Question | Answer | Evidence |",
        "| --- | ---: | --- |",
        f"| vaBench management rows | {summary.get('form_count')} | `{report['source_reports']['package_manifest']}` |",
        f"| paper-score-ready rows | {summary.get('paper_score_ready_task_count')} | `{report['source_reports']['package_manifest']}` |",
        f"| pending certification rows | {summary.get('pending_form_count')} | `{report['source_reports']['package_manifest']}` |",
        f"| score-counted rows | {summary.get('scored_form_count')} | `{report['source_reports']['package_manifest']}` |",
        f"| inherited v1 rows + fresh-certified v1.1 rows | {summary.get('existing_certified_v1_task_count')} + {summary.get('promoted_v11_task_count')} | `{report['source_reports']['package_manifest']}` |",
        f"| partial-pass negative candidates | {expansion.get('partial_pass_negative_count')} | `{report['source_reports']['package_manifest']}` |",
        f"| current Spectre reference dual PASS | {reference_backend.get('rows')} / {reference_backend.get('total')} | `{reference_backend.get('evidence')}` |",
        f"| current Spectre reference no-checker rows | {reference_backend.get('no_checker_rows')} | `{reference_backend.get('evidence')}` |",
        f"| EVAS PASS / Spectre FAIL mismatches | {summary.get('evas_pass_spectre_fail_count')} | `{report['source_reports']['dual_certification']}` plus current full-300 summaries |",
        "",
        "## Backend Coverage",
        "",
        f"Four-backend certification status: `{backend_coverage['status']}`. Full-300 runs completed for {backend_coverage['completed_backend_count']} / {backend_coverage['required_backend_count']} backend rows; currently claimable full-300 behavior certification exists for {backend_coverage['certified_backend_count']} / {backend_coverage['required_backend_count']}.",
        "",
        "| Backend | Full-300 Status | Rows | Evidence | Notes |",
        "| --- | --- | ---: | --- | --- |",
    ]
    for row in backend_coverage["rows"]:
        rows = f"{row['rows']} / {row['total']}" if row.get("rows") is not None else f"missing / {row['total']}"
        if row.get("historical_subset_rows") is not None:
            rows += f"; historical subset {row['historical_subset_rows']}"
        lines.append(
            "| "
            + " | ".join(
                [
                    row["label"],
                    f"`{row['full_300_status']}`",
                    rows,
                    f"`{row['evidence']}`",
                    row["notes"],
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
        "## Equivalence Contract",
        "",
        f"- Bit-exact equality claim: `{contract['bit_exact_claim']}`.",
        f"- Acceptance basis: {contract['acceptance_basis']}.",
        f"- Waveform small-absolute gate: `{contract['small_absolute_gate']}`.",
        f"- Waveform relative-RMS gate: `{contract['relative_rms_gate']}`.",
        f"- Edge-window policy: {contract['edge_window_policy']}",
        f"- Gain metric gate: `{contract['gain_metric_gate']}`.",
        f"- PLL task-aware rows: {contract['pll_task_aware']}",
        "",
        ]
    )
    lines.extend(
        [
        "## Observed Parity Metrics",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| certified/pass rows | {metrics.get('parity_passed_form_count')} / {metrics.get('parity_form_count')} |",
        f"| detailed waveform-metric rows | {metrics.get('waveform_metric_form_count')} |",
        f"| gain-metric forms | {metrics.get('gain_metric_form_count')} |",
        f"| PLL task-aware forms | {metrics.get('pll_task_aware_form_count')} |",
        f"| max row mean relative RMS error | {fmt(metrics.get('max_mean_relative_rms_error'))} |",
        f"| max worst-signal relative RMS error | {fmt(metrics.get('max_worst_signal_relative_rms_error'))} |",
        f"| max RMSE voltage | {fmt(metrics.get('max_rmse_v'))} V |",
        f"| max absolute voltage error | {fmt(metrics.get('max_abs_v'))} V |",
        f"| max digital mismatch ratio | {fmt(metrics.get('max_digital_mismatch_ratio'))} |",
        f"| max relative gain delta | {fmt(metrics.get('max_relative_gain_delta'))} |",
        "",
        "## Management Surface",
        "",
        management_note,
        "",
        "| Count | Value | Meaning |",
        "| --- | ---: | --- |",
        f"| management rows | {summary.get('form_count')} | {management_row_label} |",
        f"| paper-score-ready rows | {summary.get('paper_score_ready_task_count')} | {score_ready_label} |",
        f"| {v11_pending_label} | {summary.get('score_denominator_pending_v11_task_count') if pending_v11 else summary.get('promoted_v11_task_count')} | {v11_pending_meaning} |",
        f"| task-specific v1.1 EVAS gold pass | {expansion.get('task_specific_v11_gold_pass_count')} | local EVAS full-checker evidence |",
        f"| task-specific v1.1 fresh Spectre pass | {expansion.get('fresh_spectre_v11_pass_count')} | fresh Spectre + EVAS dual rerun evidence |",
        f"| task-specific v1.1 negative full-checker fail | {expansion.get('task_specific_v11_negative_full_checker_fail_count')} | local negative quality evidence for v1.1 rows |",
        f"| score-counted rows | {summary.get('scored_form_count')} | current counted score surface |",
        f"| negative candidates | {expansion.get('partial_pass_negative_count')} | static-shape audited partial-pass candidates |",
        f"| runnable staging bundles | {staging.get('total_staging_bundles')} | execution inputs only; not a benchmark count |",
        "",
        f"Promotion note: {expansion.get('explanation')}",
        "",
        "## Category Overview",
        "",
        "| Category | Entries | Forms | Core | Support | L1 | L2 | Scored Entries | Certified Entries |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    )
    for row in report["category_rows"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["category"]),
                    str(row["entry_count"]),
                    str(row["form_count"]),
                    str(row["core_entry_count"]),
                    str(row["support_entry_count"]),
                    str(row["l1_entry_count"]),
                    str(row["l2_entry_count"]),
                    str(row["scored_entry_count"]),
                    str(row["certified_entry_count"]),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Complete Entry List",
            "",
            "| Entry | Level | Track | Difficulty | Category | Base function | Forms | Score | EVAS/Spectre | Parity summary |",
            "| --- | --- | --- | --- | --- | --- | ---: | --- | --- | --- |",
        ]
    )
    for row in report["entry_rows"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['release_entry_id']}`",
                    str(row.get("level")),
                    str(row.get("track")),
                    str(row.get("difficulty")),
                    str(row.get("category")),
                    str(row.get("base_function")),
                    str(row.get("form_count")),
                    "counted" if row.get("counted_in_score") else "not counted",
                    f"{row.get('evas')}/{row.get('spectre')}",
                    parity_summary(row),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Exports",
            "",
            f"- Entry CSV: `{report['exports']['entries_csv']}`",
            f"- Form CSV: `{report['exports']['forms_csv']}`",
            f"- Category CSV: `{report['exports']['categories_csv']}`",
            "",
            "## Claim Boundary",
            "",
        ]
    )
    for item in report["claim_boundary"]:
        lines.append(f"- {item}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    report = build_report()
    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_csv(
        CATEGORY_CSV,
        report["category_rows"],
        [
            "category",
            "entry_count",
            "form_count",
            "core_entry_count",
            "support_entry_count",
            "l1_entry_count",
            "l2_entry_count",
            "scored_entry_count",
            "scored_form_count",
            "certified_entry_count",
        ],
    )
    write_csv(
        ENTRY_CSV,
        report["entry_rows"],
        [
            "release_entry_id",
            "level",
            "track",
            "difficulty",
            "category",
            "base_function",
            "form_count",
            "forms",
            "counted_in_score",
            "content_denominator_included",
            "certification",
            "static",
            "evas",
            "spectre",
            "waveform_form_count",
            "special_metric_form_count",
            "gain_metric_form_count",
            "worst_mean_relative_rms_error",
            "worst_signal_relative_rms_error",
            "worst_max_rmse_v",
            "worst_max_abs_v",
            "max_digital_mismatch_ratio",
            "max_relative_gain_delta",
            "parity_policies",
            "evidence_count",
            "evidence_paths",
        ],
    )
    write_csv(
        FORM_CSV,
        report["form_rows"],
        [
            "release_entry_id",
            "legacy_task_id",
            "task_id",
            "form",
            "level",
            "track",
            "difficulty",
            "category",
            "base_function",
            "counted_in_score",
            "content_denominator_included",
            "static",
            "evas",
            "spectre",
            "verdict",
            "source_equivalence_pass",
            "parity_status",
            "parity_policy",
            "signals_compared",
            "samples",
            "common_window_s",
            "mean_relative_rms_error",
            "max_relative_rms_error",
            "max_rmse_v",
            "max_abs_v",
            "max_digital_mismatch_ratio",
            "relative_gain_delta",
            "special_metric_summary",
            "expansion_status",
            "gold_status",
            "evidence",
            "gold_assets",
        ],
    )
    write_markdown(report)


if __name__ == "__main__":
    main()
