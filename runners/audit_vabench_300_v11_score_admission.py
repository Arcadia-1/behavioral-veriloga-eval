#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any

from vabench_policy import content_denominator_exclusion_reasons, is_content_denominator_entry


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
EXPANSION_ROOT = PACKAGE_ROOT / "vabench-300-expansion"
MANIFEST_JSON = EXPANSION_ROOT / "VABENCH_300_MANIFEST.json"
QUALITY_JSON = EXPANSION_ROOT / "v11_task_specific_quality_evidence.json"
NEGATIVE_AUDIT_JSON = EXPANSION_ROOT / "negative_audit.json"
FRESH_SPECTRE_JSON = PACKAGE_ROOT / "reports" / "vabench_300_v11_fresh_spectre_rerun.json"
REPORT_JSON = PACKAGE_ROOT / "reports" / "vabench_300_v11_score_admission.json"
REPORT_MD = PACKAGE_ROOT / "reports" / "vabench_300_v11_score_admission.md"
README_MD = EXPANSION_ROOT / "README.md"

EXPECTED_V11_ROWS = 29
EXPECTED_V11_NEGATIVES = EXPECTED_V11_ROWS * 5


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def root_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else ROOT / path


def task_entry_manifest_path(task_manifest: Path) -> Path:
    return task_manifest.parent.parent.parent / "release_entry.json"


def row_key(row: dict[str, Any]) -> tuple[str, str]:
    return str(row.get("legacy_entry_id") or ""), str(row.get("form") or "")


def infer_level(entry_id: str) -> str:
    if "_l1_" in entry_id:
        return "L1"
    if "_l2_" in entry_id:
        return "L2"
    return ""


def fail(reasons: list[str], reason: str) -> None:
    reasons.append(reason)


def v11_rows(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        row
        for row in manifest.get("tasks", [])
        if isinstance(row, dict) and row.get("expansion_status") == "certified_v1.1_promoted"
    ]


def fresh_spectre_by_key(report: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    return {row_key(row): row for row in report.get("rows", []) if isinstance(row, dict)}


def quality_gold_by_manifest(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(row.get("release_task_manifest")): row
        for row in report.get("gold_results", [])
        if isinstance(row, dict) and row.get("release_task_manifest")
    }


def quality_negatives_by_task(report: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in report.get("negative_results", []):
        if isinstance(row, dict) and row.get("task_id"):
            rows[str(row["task_id"])].append(row)
    return rows


def prompt_leak_warnings(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    lower = text.lower()
    warnings: list[str] = []
    forbidden = [
        "gold/",
        "release_task.json",
        "checks.yaml",
        "negative",
        "reference solution",
        "solution code",
    ]
    for token in forbidden:
        if token in lower:
            warnings.append(f"prompt_contains_{token.replace('/', '').replace(' ', '_')}")
    if "task-specific benchmark candidate" in lower:
        warnings.append("prompt_uses_candidate_wording")
    return warnings


def checks_strength(path: Path) -> tuple[bool, list[str]]:
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    warnings: list[str] = []
    has_full = "_full_behavior" in text
    has_near_miss = "_near_miss_rejection" in text
    has_negative_policy = "required_partial_pass_negatives: 5" in text
    if not has_full:
        warnings.append("checks_missing_full_behavior_gate")
    if not has_near_miss:
        warnings.append("checks_missing_near_miss_rejection_gate")
    if not has_negative_policy:
        warnings.append("checks_missing_required_partial_pass_negatives_5")
    return has_full and has_near_miss and has_negative_policy, warnings


def audit_row(
    row: dict[str, Any],
    fresh_rows: dict[tuple[str, str], dict[str, Any]],
    quality_gold_rows: dict[str, dict[str, Any]],
    quality_negative_rows: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    blockers: list[str] = []
    warnings: list[str] = []
    task_manifest_path = root_path(str(row.get("release_task_manifest", "")))
    task_manifest = read_json(task_manifest_path)
    entry_manifest_path = task_entry_manifest_path(task_manifest_path)
    entry_manifest = read_json(entry_manifest_path)
    key = row_key(row)
    fresh_row = fresh_rows.get(key, {})
    quality_gold = quality_gold_rows.get(str(row.get("release_task_manifest")), {})
    quality_negatives = quality_negative_rows.get(str(row.get("task_id")), [])

    for field in ("prompt", "meta", "checks", "negative_manifest", "release_task_manifest"):
        if not row.get(field) or not root_path(str(row[field])).exists():
            fail(blockers, f"missing_{field}")

    artifacts = task_manifest.get("artifacts", {}) if isinstance(task_manifest.get("artifacts"), dict) else {}
    gold = artifacts.get("gold", [])
    if not isinstance(gold, list) or len(gold) < 1:
        fail(blockers, "missing_gold_artifacts")
    else:
        for artifact in gold:
            if not root_path(str(artifact)).exists():
                fail(blockers, f"missing_gold_artifact:{artifact}")

    if row.get("track") != "core":
        fail(blockers, f"non_core_track:{row.get('track')}")
    if row.get("family") not in {"spec-to-va", "tb-generation", "end-to-end", "bugfix"}:
        fail(blockers, f"unsupported_family:{row.get('family')}")
    if not is_content_denominator_entry(str(row.get("legacy_entry_id"))):
        fail(blockers, "content_denominator_excluded")
    if content_denominator_exclusion_reasons(str(row.get("legacy_entry_id"))):
        fail(blockers, "content_denominator_exclusion_reason_present")
    if row.get("static") != "pass" or row.get("evas") != "pass" or row.get("spectre") != "pass":
        fail(blockers, "manifest_backend_not_all_pass")
    if row.get("certification") != "fresh_evas_spectre_certified":
        fail(blockers, f"manifest_certification_not_fresh:{row.get('certification')}")

    cert = task_manifest.get("certification", {}) if isinstance(task_manifest.get("certification"), dict) else {}
    counts = task_manifest.get("counts", {}) if isinstance(task_manifest.get("counts"), dict) else {}
    if cert.get("static") != "pass" or cert.get("evas") != "pass" or cert.get("spectre") != "pass":
        fail(blockers, "release_task_backend_not_all_pass")
    if counts.get("model_capability") is not True or counts.get("l0_conformance") is not False:
        fail(blockers, "release_task_count_flags_not_model_capability")
    if counts.get("benchmark_score") is not False and counts.get("benchmark_score") is not True:
        fail(blockers, "release_task_benchmark_score_not_boolean")

    entry_counts = entry_manifest.get("counts", {}) if isinstance(entry_manifest.get("counts"), dict) else {}
    if entry_manifest.get("missing_forms"):
        fail(blockers, "entry_missing_forms")
    unexpected_blockers = [
        item
        for item in entry_manifest.get("release_blockers", [])
        if item != "score_denominator_admission_pending_after_certification"
    ]
    if unexpected_blockers:
        fail(blockers, f"entry_has_unexpected_blockers:{','.join(map(str, unexpected_blockers))}")
    if not isinstance(entry_counts.get("benchmark_score", False), bool) or entry_counts.get("l0_conformance") is not False:
        fail(blockers, "entry_count_flags_invalid")

    if not fresh_row:
        fail(blockers, "missing_fresh_spectre_row")
    else:
        if fresh_row.get("raw_status") != "PASS":
            fail(blockers, f"fresh_spectre_raw_status:{fresh_row.get('raw_status')}")
        if fresh_row.get("spectre_ok") is not True:
            fail(blockers, "fresh_spectre_not_ok")
        if fresh_row.get("spectre_behavior_score") != 1.0:
            fail(blockers, f"fresh_spectre_behavior_score:{fresh_row.get('spectre_behavior_score')}")
        if fresh_row.get("parity_status") != "passed":
            fail(blockers, f"fresh_spectre_parity:{fresh_row.get('parity_status')}")

    if not quality_gold:
        fail(blockers, "missing_quality_gold_row")
    else:
        if quality_gold.get("compile_sim_pass") is not True:
            fail(blockers, "quality_gold_compile_sim_not_pass")
        if quality_gold.get("behavior_checker_pass") is not True:
            fail(blockers, "quality_gold_behavior_checker_not_pass")
        if quality_gold.get("raw_status") != "PASS":
            fail(blockers, f"quality_gold_raw_status:{quality_gold.get('raw_status')}")

    if len(quality_negatives) != 5:
        fail(blockers, f"quality_negative_count:{len(quality_negatives)}")
    for negative in quality_negatives:
        if negative.get("compile_sim_pass") is not True:
            fail(blockers, f"quality_negative_compile_sim_not_pass:{negative.get('negative_id')}")
        if negative.get("full_checker_fail") is not True:
            fail(blockers, f"quality_negative_full_checker_not_fail:{negative.get('negative_id')}")

    negative_manifest_path = root_path(str(row.get("negative_manifest", "")))
    negative_manifest = read_json(negative_manifest_path)
    negatives = negative_manifest.get("negatives", []) if isinstance(negative_manifest.get("negatives"), list) else []
    if negative_manifest.get("negative_count") != 5 or len(negatives) != 5:
        fail(blockers, f"negative_manifest_count:{negative_manifest.get('negative_count')}:{len(negatives)}")
    for negative in negatives:
        evidence = negative.get("validation_evidence", {}) if isinstance(negative.get("validation_evidence"), dict) else {}
        result = negative.get("validation_result", {}) if isinstance(negative.get("validation_result"), dict) else {}
        if evidence.get("static_shallow_shape") != "pass":
            fail(blockers, f"negative_static_lane_not_pass:{negative.get('id')}")
        if evidence.get("simulator_shallow_lane") != "pass":
            fail(blockers, f"negative_simulator_lane_not_pass:{negative.get('id')}")
        if evidence.get("full_checker_lane") != "pass":
            fail(blockers, f"negative_full_checker_lane_not_pass:{negative.get('id')}")
        if result.get("compile_sim_pass") is not True:
            fail(blockers, f"negative_manifest_compile_sim_not_pass:{negative.get('id')}")
        if result.get("full_checker_fail") is not True:
            fail(blockers, f"negative_manifest_full_checker_not_fail:{negative.get('id')}")

    prompt_path = root_path(str(row.get("prompt", "")))
    checks_path = root_path(str(row.get("checks", "")))
    if prompt_path.exists():
        warnings.extend(prompt_leak_warnings(prompt_path))
    strong_checks, check_warnings = checks_strength(checks_path)
    warnings.extend(check_warnings)
    if not strong_checks:
        fail(blockers, "checker_strength_gate_failed")

    return {
        "release_entry_id": row.get("legacy_entry_id"),
        "task_id": row.get("task_id"),
        "form": row.get("form"),
        "category": row.get("category"),
        "base_function": row.get("base_function"),
        "manifest": row.get("release_task_manifest"),
        "admission_ready": not blockers,
        "blockers": blockers,
        "warnings": sorted(set(warnings)),
        "fresh_spectre": {
            "raw_status": fresh_row.get("raw_status"),
            "spectre_ok": fresh_row.get("spectre_ok"),
            "behavior_score": fresh_row.get("spectre_behavior_score"),
            "parity_status": fresh_row.get("parity_status"),
            "mean_relative_rms_error": fresh_row.get("mean_relative_rms_error"),
            "max_relative_rms_error": fresh_row.get("max_relative_rms_error"),
        },
        "negative_count": len(negatives),
    }


def build_report() -> dict[str, Any]:
    manifest = read_json(MANIFEST_JSON)
    fresh = read_json(FRESH_SPECTRE_JSON)
    quality = read_json(QUALITY_JSON)
    negative_audit = read_json(NEGATIVE_AUDIT_JSON)
    rows = v11_rows(manifest)
    fresh_rows = fresh_spectre_by_key(fresh)
    quality_gold_rows = quality_gold_by_manifest(quality)
    quality_negative_rows = quality_negatives_by_task(quality)

    global_blockers: list[str] = []
    if len(rows) != EXPECTED_V11_ROWS:
        fail(global_blockers, f"v11_row_count:{len(rows)}")
    summary = manifest.get("summary", {}) if isinstance(manifest.get("summary"), dict) else {}
    if summary.get("certified_task_count") != 300:
        fail(global_blockers, f"manifest_certified_task_count:{summary.get('certified_task_count')}")
    if fresh.get("status") != "pass":
        fail(global_blockers, f"fresh_spectre_status:{fresh.get('status')}")
    fresh_summary = fresh.get("summary", {}) if isinstance(fresh.get("summary"), dict) else {}
    for key, expected in {
        "pass_count": EXPECTED_V11_ROWS,
        "parity_pass_count": EXPECTED_V11_ROWS,
        "evas_pass_spectre_fail_count": 0,
    }.items():
        if fresh_summary.get(key) != expected:
            fail(global_blockers, f"fresh_spectre_summary_{key}:{fresh_summary.get(key)}")
    if quality.get("status") != "pass":
        fail(global_blockers, f"quality_status:{quality.get('status')}")
    for key, expected in {
        "task_count": EXPECTED_V11_ROWS,
        "gold_behavior_checker_pass_count": EXPECTED_V11_ROWS,
        "gold_behavior_checker_fail_count": 0,
        "negative_count": EXPECTED_V11_NEGATIVES,
        "negative_compile_sim_pass_count": EXPECTED_V11_NEGATIVES,
        "negative_full_checker_fail_count": EXPECTED_V11_NEGATIVES,
    }.items():
        if quality.get(key) != expected:
            fail(global_blockers, f"quality_{key}:{quality.get(key)}")
    if negative_audit.get("status") != "pass":
        fail(global_blockers, f"negative_audit_status:{negative_audit.get('status')}")
    if negative_audit.get("issue_count") != 0:
        fail(global_blockers, f"negative_audit_issue_count:{negative_audit.get('issue_count')}")
    if negative_audit.get("negative_count") != 1500:
        fail(global_blockers, f"negative_audit_negative_count:{negative_audit.get('negative_count')}")

    row_reports = [
        audit_row(row, fresh_rows, quality_gold_rows, quality_negative_rows)
        for row in sorted(rows, key=lambda item: (str(item.get("legacy_entry_id")), str(item.get("form"))))
    ]
    blocker_counts: Counter[str] = Counter()
    warning_counts: Counter[str] = Counter()
    for row in row_reports:
        blocker_counts.update(row["blockers"])
        warning_counts.update(row["warnings"])

    all_rows_ready = len(row_reports) == EXPECTED_V11_ROWS and all(row["admission_ready"] for row in row_reports)
    verdict = "admit_all" if all_rows_ready and not global_blockers else "blocked"
    return {
        "date": date.today().isoformat(),
        "status": "pass" if verdict == "admit_all" else "fail",
        "verdict": verdict,
        "summary": {
            "expected_v11_rows": EXPECTED_V11_ROWS,
            "audited_v11_rows": len(row_reports),
            "admission_ready_rows": sum(1 for row in row_reports if row["admission_ready"]),
            "blocked_rows": sum(1 for row in row_reports if not row["admission_ready"]),
            "fresh_spectre_pass_count": fresh_summary.get("pass_count"),
            "fresh_spectre_parity_pass_count": fresh_summary.get("parity_pass_count"),
            "evas_pass_spectre_fail_count": fresh_summary.get("evas_pass_spectre_fail_count"),
            "quality_negative_full_checker_fail_count": quality.get("negative_full_checker_fail_count"),
            "negative_audit_issue_count": negative_audit.get("issue_count"),
            "row_blocker_counts": dict(sorted(blocker_counts.items())),
            "row_warning_counts": dict(sorted(warning_counts.items())),
        },
        "global_blockers": global_blockers,
        "rows": row_reports,
        "evidence_sources": {
            "vabench_300_manifest": rel(MANIFEST_JSON),
            "fresh_spectre_rerun": rel(FRESH_SPECTRE_JSON),
            "task_specific_quality": rel(QUALITY_JSON),
            "negative_audit": rel(NEGATIVE_AUDIT_JSON),
        },
        "claim_boundary": [
            "This report only admits fresh-certified v1.1 rows to the score denominator; support-suite exclusions still apply globally.",
            "Spectre remains the final paper-facing judge; EVAS evidence is a fast evaluator and checker-strength signal.",
            "Warnings flag wording hygiene or non-blocking prompt text; blockers prevent admission.",
        ],
    }


def write_markdown(report: dict[str, Any]) -> None:
    summary = report["summary"]
    lines = [
        "# vaBench 300 v1.1 Score Admission Audit",
        "",
        f"Date: {report['date']}",
        "",
        "This report gates whether the 29 fresh-certified v1.1 rows may enter the",
        "paper score denominator.",
        "",
        "## Verdict",
        "",
        f"- status: `{report['status']}`",
        f"- verdict: `{report['verdict']}`",
        f"- audited rows: {summary['audited_v11_rows']} / {summary['expected_v11_rows']}",
        f"- admission-ready rows: {summary['admission_ready_rows']}",
        f"- blocked rows: {summary['blocked_rows']}",
        f"- EVAS PASS / Spectre FAIL rows: {summary['evas_pass_spectre_fail_count']}",
        "",
        "## Evidence",
        "",
        f"- fresh Spectre pass rows: {summary['fresh_spectre_pass_count']}",
        f"- fresh Spectre parity pass rows: {summary['fresh_spectre_parity_pass_count']}",
        f"- task-specific negative full-checker fails: {summary['quality_negative_full_checker_fail_count']}",
        f"- negative audit issues: {summary['negative_audit_issue_count']}",
        "",
        "## Blockers",
        "",
    ]
    if report["global_blockers"]:
        for item in report["global_blockers"]:
            lines.append(f"- `{item}`")
    elif summary["row_blocker_counts"]:
        for key, value in summary["row_blocker_counts"].items():
            lines.append(f"- `{key}`: {value}")
    else:
        lines.append("- none")
    lines.extend(["", "## Warnings", ""])
    if summary["row_warning_counts"]:
        for key, value in summary["row_warning_counts"].items():
            lines.append(f"- `{key}`: {value}")
    else:
        lines.append("- none")
    lines.extend(["", "## Row Results", "", "| Entry | Form | Ready | Warnings | Blockers |", "| --- | --- | ---: | ---: | ---: |"])
    for row in report["rows"]:
        lines.append(
            "| {entry} | {form} | {ready} | {warnings} | {blockers} |".format(
                entry=row["release_entry_id"],
                form=row["form"],
                ready="yes" if row["admission_ready"] else "no",
                warnings=len(row["warnings"]),
                blockers=len(row["blockers"]),
            )
        )
    lines.extend(["", "## Claim Boundary", ""])
    for item in report["claim_boundary"]:
        lines.append(f"- {item}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def admit_task_manifest(path: Path, admission_report: str) -> None:
    payload = read_json(path)
    entry_id = str(payload.get("release_entry_id") or payload.get("legacy_entry_id") or "")
    payload["benchmark"] = "vabench-release-v1"
    payload["release_entry_id"] = entry_id
    payload["level"] = payload.get("level") or infer_level(entry_id)
    payload["track"] = payload.get("track", "core")
    counts = payload.setdefault("counts", {})
    counts["benchmark_score"] = True
    counts["l0_conformance"] = False
    counts["model_capability"] = True
    cert = payload.setdefault("certification", {})
    cert["paper_score_status"] = "admitted_to_score_denominator"
    cert["score_admission_evidence"] = admission_report
    notes = payload.setdefault("notes", [])
    if isinstance(notes, list):
        notes = [note for note in notes if "outside paper score" not in str(note)]
        admission_note = "Admitted to the paper score denominator after v1.1 score-admission audit."
        if admission_note not in notes:
            notes.append(admission_note)
        payload["notes"] = notes
    write_json(path, payload)


def admit_entry_manifest(path: Path, admission_report: str) -> None:
    payload = read_json(path)
    entry_id = str(payload.get("release_entry_id") or payload.get("legacy_entry_id") or "")
    payload["benchmark"] = "vabench-release-v1"
    payload["release_entry_id"] = entry_id
    payload["level"] = payload.get("level") or infer_level(entry_id)
    payload["track"] = payload.get("track", "core")
    payload["source_base_id"] = payload.get("source_base_id") or payload.get("id") or entry_id
    payload["source_tasks"] = [
        {
            "form": str(task.get("form", "")),
            "source_path": f"vabench300_task_specific:{entry_id}",
            "prompt": True,
            "meta": True,
            "checks": True,
            "gold": True,
            "asset_complete": True,
        }
        for task in payload.get("release_tasks", [])
        if isinstance(task, dict)
    ]
    counts = payload.setdefault("counts", {})
    counts["benchmark_score"] = True
    counts["l0_conformance"] = False
    counts["model_capability"] = False
    cert = payload.setdefault("certification", {})
    cert["paper_score_status"] = "admitted_to_score_denominator"
    cert["score_admission_evidence"] = admission_report
    payload["package_status"] = "v1.1_fresh_spectre_certified_score_admitted"
    payload["release_blockers"] = [
        blocker
        for blocker in payload.get("release_blockers", [])
        if blocker != "score_denominator_admission_pending_after_certification"
    ]
    write_json(path, payload)


def apply_admission(report: dict[str, Any]) -> None:
    if report.get("verdict") != "admit_all":
        raise SystemExit("refusing to apply score admission because audit verdict is not admit_all")
    manifest = read_json(MANIFEST_JSON)
    admitted_task_ids = {str(row["task_id"]) for row in report["rows"]}
    admission_report = rel(REPORT_JSON)
    entry_paths: set[Path] = set()

    for row in manifest.get("tasks", []):
        if not isinstance(row, dict) or str(row.get("task_id")) not in admitted_task_ids:
            continue
        row["counted_in_score"] = True
        row["content_denominator_included"] = True
        row["content_exclusion_reasons"] = []
        row["exclusion_reasons"] = []
        row["paper_score_status"] = "admitted_to_score_denominator"
        row["score_admission_evidence"] = admission_report
        task_manifest = root_path(str(row["release_task_manifest"]))
        admit_task_manifest(task_manifest, admission_report)
        entry_paths.add(task_entry_manifest_path(task_manifest))

    for entry_path in sorted(entry_paths):
        admit_entry_manifest(entry_path, admission_report)

    summary = manifest.setdefault("summary", {})
    summary["paper_score_ready_task_count"] = 300
    summary["paper_score_disabled_v11_task_count"] = 0
    summary["score_denominator_pending_v11_task_count"] = 0
    summary["score_denominator_admitted_v11_task_count"] = EXPECTED_V11_ROWS
    manifest["status"] = "management_surface_with_v11_score_admitted"
    manifest["v11_score_admission_evidence"] = admission_report
    claim_boundary = manifest.setdefault("claim_boundary", [])
    if isinstance(claim_boundary, list):
        claim_boundary = [
            item
            for item in claim_boundary
            if "271 inherited v1 rows remain the only current paper-score-ready rows" not in str(item)
            and "Do not count v1.1 rows" not in str(item)
        ]
        admission_boundary = (
            "All 29 fresh-certified v1.1 rows are admitted to the paper score denominator; "
            "support-suite exclusions still apply."
        )
        if admission_boundary not in claim_boundary:
            claim_boundary.append(admission_boundary)
        manifest["claim_boundary"] = claim_boundary
    write_json(MANIFEST_JSON, manifest)
    write_expansion_readme(manifest)


def write_expansion_readme(manifest: dict[str, Any]) -> None:
    summary = manifest.get("summary", {}) if isinstance(manifest.get("summary"), dict) else {}
    lines = [
        "# vaBench 300 Expansion Manifest",
        "",
        f"- tasks: {summary.get('task_count', 300)}",
        f"- existing certified v1 tasks: {summary.get('existing_certified_v1_task_count', 271)}",
        f"- task-specific v1.1 tasks: {summary.get('task_specific_v11_task_count', EXPECTED_V11_ROWS)}",
        f"- paper-score-ready tasks: {summary.get('paper_score_ready_task_count', 300)}",
        f"- simulator-certified benchmark tasks: {summary.get('certified_task_count', 300)}",
        f"- fresh Spectre-certified v1.1 tasks: {summary.get('fresh_spectre_v11_pass_count', EXPECTED_V11_ROWS)}",
        f"- score-denominator-admitted v1.1 tasks: {summary.get('score_denominator_admitted_v11_task_count', EXPECTED_V11_ROWS)}",
        f"- score-denominator-pending v1.1 tasks: {summary.get('score_denominator_pending_v11_task_count', 0)}",
        f"- negatives per task: {summary.get('required_negative_per_task', 5)}",
        f"- total partial-pass negatives: {summary.get('partial_pass_negative_count', 1500)}",
        f"- static shallow-shape verified negatives after audit: {summary.get('negative_static_shallow_shape_verified_count', 1500)}",
        "- simulator shallow-lane verified negatives: recorded by `v11_task_specific_quality_evidence.json`",
        "- full-checker fail verified negatives: recorded by `v11_task_specific_quality_evidence.json`",
        "",
        "Certification boundary: the 29 v1.1 rows now have task-specific prompts, gold implementations, checker IDs, near-miss negatives, local EVAS quality evidence, fresh EVAS/Spectre PASS evidence, and explicit score-denominator admission evidence.",
        "",
        "## Purpose",
        "",
        "This directory is the primary vaBench 300 management surface. It indexes 271 inherited certified v1 form-level rows plus 29 task-specific v1.1 rows. Use 300 as the asset-management and simulator-certification surface. The current scored model-evaluation denominator contains 265 core rows after support-suite exclusions.",
        "",
        "`benchmark-vabench-release-v1/reports/vabench_300_v11_fresh_spectre_rerun.json` records the compact fresh Spectre rerun import for the 29 v1.1 rows. Raw simulator outputs are intentionally not versioned.",
        "",
        "Every task has a partial-pass negative manifest with five near-miss candidates. For v1.1 rows, the negatives are generated from task-specific variants intended to compile and run while failing the registered full checker.",
        "",
        "## Files",
        "",
        "- `VABENCH_300_MANIFEST.json`: the 300-task index.",
        "- `v11_task_specific_quality_evidence.json`: EVAS gold/negative quality evidence for v1.1 rows.",
        "- `benchmark-vabench-release-v1/reports/vabench_300_v11_fresh_spectre_rerun.json`: compact fresh Spectre rerun evidence for v1.1 rows.",
        "- `benchmark-vabench-release-v1/reports/vabench_300_v11_score_admission.json`: score-denominator admission audit for the 29 v1.1 rows.",
        "- `negative_audit.json`: asset/hash/count audit for all negative manifests.",
        "- `existing-negatives/`: five negative candidates for each existing certified v1 task.",
        "- `proposed-tasks/`: the 29 v1.1 task assets, including prompt, checks, gold, release task manifests, and negatives.",
        "",
        "## Schemas",
        "",
        "- `../../schemas/vabench-300-expansion-manifest.schema.json`",
        "- `../../schemas/vabench-partial-pass-negatives.schema.json`",
        "",
        "## Commands",
        "",
        "Regenerate the pre-import expansion package:",
        "",
        "```bash",
        "python3 runners/build_vabench_300_expansion.py",
        "```",
        "",
        "Reattach fresh v1.1 Spectre evidence after a rerun:",
        "",
        "```bash",
        "python3 runners/import_vabench_300_v11_spectre_rerun.py --summary /path/to/summary.json",
        "```",
        "",
        "Audit and admit v1.1 rows to the score denominator:",
        "",
        "```bash",
        "python3 runners/audit_vabench_300_v11_score_admission.py --apply",
        "```",
        "",
        "Audit negative manifests:",
        "",
        "```bash",
        "python3 runners/audit_vabench_300_expansion.py",
        "```",
        "",
        "Run the focused tests:",
        "",
        "```bash",
        "PYTHONPATH=runners python3 -m pytest tests/test_vabench_300_expansion.py -q",
        "```",
    ]
    README_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit and optionally admit vaBench 300 v1.1 rows to the score denominator.")
    parser.add_argument("--apply", action="store_true", help="Apply admission flags after a passing audit.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = build_report()
    write_json(REPORT_JSON, report)
    write_markdown(report)
    if args.apply:
        apply_admission(report)
        report = build_report()
        write_json(REPORT_JSON, report)
        write_markdown(report)
    print(
        "wrote v1.1 score admission audit: status={status}; verdict={verdict}; ready={ready}/{total}".format(
            status=report["status"],
            verdict=report["verdict"],
            ready=report["summary"]["admission_ready_rows"],
            total=report["summary"]["audited_v11_rows"],
        )
    )


if __name__ == "__main__":
    main()
