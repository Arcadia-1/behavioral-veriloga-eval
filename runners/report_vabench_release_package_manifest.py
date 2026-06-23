#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

from vabench_release_surface import read_release_entries
from vabench_policy import content_denominator_exclusion_reasons, is_content_denominator_entry


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
TASKS_ROOT = PACKAGE_ROOT / "tasks"
REPORTS_ROOT = PACKAGE_ROOT / "reports"
VABENCH300_MANIFEST = PACKAGE_ROOT / "vabench-300-expansion" / "VABENCH_300_MANIFEST.json"
PROPOSED_TASKS_ROOT = PACKAGE_ROOT / "vabench-300-expansion" / "proposed-tasks"
MANIFEST_JSON = PACKAGE_ROOT / "MANIFEST.json"
MANIFEST_CSV = PACKAGE_ROOT / "MANIFEST.csv"
MANIFEST_MD = PACKAGE_ROOT / "MANIFEST.md"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def boolish(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "pass", "enabled"}
    return bool(value)


def level_from_entry_id(release_entry_id: str) -> str:
    lowered = release_entry_id.lower()
    if "_l0_" in lowered:
        return "L0"
    if "_l1_" in lowered:
        return "L1"
    if "_l2_" in lowered:
        return "L2"
    return ""


def score_surface_for(level: str, track: str) -> str:
    if track == "support":
        return "support-suite"
    if level == "L1":
        return "model-capability"
    if level == "L2":
        return "benchmark-e2e"
    return ""


def read_vabench300_tasks() -> list[dict[str, Any]]:
    manifest = read_json(VABENCH300_MANIFEST)
    tasks = manifest.get("tasks", [])
    if not isinstance(tasks, list):
        return []
    return [task for task in tasks if isinstance(task, dict)]


def task_manifest_path(task: dict[str, Any]) -> Path:
    return ROOT / str(task.get("release_path", "")) / "release_task.json"


def score_rows_by_id() -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    score = read_json(REPORTS_ROOT / "score_denominator_manifest.json")
    entries = {
        str(row.get("release_entry_id")): row
        for row in score.get("entry_rows", [])
        if isinstance(row, dict) and row.get("release_entry_id")
    }
    forms = {
        str(row.get("task_id")): row
        for row in score.get("form_rows", [])
        if isinstance(row, dict) and row.get("task_id")
    }
    return entries, forms


def certification_label(static: str, evas: str, spectre: str) -> str:
    if static == "pass" and evas == "pass" and spectre == "pass":
        return "certified"
    if static == "fail" or evas == "fail" or spectre == "fail":
        return "failed"
    return "pending"


def release_entry_manifest_path(release_entry_id: str) -> str:
    candidates = [
        *TASKS_ROOT.glob(f"*/{release_entry_id}/release_entry.json"),
        *PROPOSED_TASKS_ROOT.glob(f"*/{release_entry_id}/release_entry.json"),
    ]
    if candidates:
        return rel(sorted(candidates)[0])
    return ""


def vabench300_form_exclusion_reasons(
    task: dict[str, Any],
    content_denominator_included: bool,
    counted: bool,
    static: str,
    evas: str,
    spectre: str,
) -> list[str]:
    source_reasons = task.get("exclusion_reasons", [])
    if isinstance(source_reasons, list) and source_reasons:
        return [str(item) for item in source_reasons]
    reasons: list[str] = []
    content_reasons = task.get("content_exclusion_reasons", [])
    if isinstance(content_reasons, list):
        reasons.extend(f"content_denominator_excluded:{reason}" for reason in content_reasons)
    elif not content_denominator_included:
        reasons.append("content_denominator_excluded:support_suite_not_core_circuit_score")
    if not counted:
        reasons.append("benchmark_score_disabled")
    if static != "pass":
        reasons.append(f"task_static:{static}")
    if evas != "pass":
        reasons.append(f"task_evas:{evas}")
    if spectre != "pass":
        reasons.append(f"task_spectre:{spectre}")
    return reasons


def build_vabench300_form_rows(tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for task in sorted(
        tasks,
        key=lambda item: (
            str(item.get("legacy_entry_id") or item.get("release_entry_id") or ""),
            str(item.get("form") or ""),
        ),
    ):
        release_entry_id = str(task.get("legacy_entry_id") or task.get("release_entry_id") or "")
        form = str(task.get("form") or "")
        key = (release_entry_id, form)
        if not release_entry_id or not form or key in seen:
            continue
        seen.add(key)
        level = level_from_entry_id(release_entry_id)
        track = str(task.get("track") or "core")
        static = str(task.get("static") or "pending")
        evas = str(task.get("evas") or "pending")
        spectre = str(task.get("spectre") or "pending")
        certification = str(task.get("certification") or certification_label(static, evas, spectre))
        content_denominator_included = boolish(task.get("content_denominator_included"), default=track == "core")
        content_exclusion_reasons = task.get("content_exclusion_reasons", [])
        if not isinstance(content_exclusion_reasons, list):
            content_exclusion_reasons = []
        counted = boolish(
            task.get("counted_in_score"),
            default=content_denominator_included and certification == "certified" and track == "core",
        )
        exclusion_reasons = vabench300_form_exclusion_reasons(
            task,
            content_denominator_included,
            counted,
            static,
            evas,
            spectre,
        )
        rows.append(
            {
                "task_id": str(task.get("legacy_task_id") or f"{release_entry_id}:{form}"),
                "release_entry_id": release_entry_id,
                "form": form,
                "family": str(task.get("family") or ""),
                "level": level,
                "track": track,
                "difficulty": str(task.get("difficulty") or "D2"),
                "category": str(task.get("category") or ""),
                "base_function": str(task.get("base_function") or ""),
                "release_task_manifest": str(task.get("release_task_manifest") or ""),
                "prompt": str(task.get("prompt") or ""),
                "meta": str(task.get("meta") or ""),
                "checks": str(task.get("checks") or ""),
                "gold_count": int(task.get("gold_count") or 0),
                "static": static,
                "evas": evas,
                "spectre": spectre,
                "certification": certification,
                "evidence": str(task.get("evidence") or ""),
                "counted_in_score": counted,
                "exclusion_reasons": [] if counted else exclusion_reasons,
                "content_denominator_included": content_denominator_included,
                "content_exclusion_reasons": [str(item) for item in content_exclusion_reasons],
            }
        )
    return rows


def build_vabench300_entry_rows(form_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_entry: dict[str, list[dict[str, Any]]] = {}
    for row in form_rows:
        by_entry.setdefault(str(row["release_entry_id"]), []).append(row)
    rows: list[dict[str, Any]] = []
    for release_entry_id, forms in sorted(by_entry.items()):
        first = forms[0]
        static_values = {str(row["static"]) for row in forms}
        evas_values = {str(row["evas"]) for row in forms}
        spectre_values = {str(row["spectre"]) for row in forms}
        static = "pass" if static_values == {"pass"} else "fail" if "fail" in static_values else "pending"
        evas = "pass" if evas_values == {"pass"} else "fail" if "fail" in evas_values else "pending"
        spectre = "pass" if spectre_values == {"pass"} else "fail" if "fail" in spectre_values else "pending"
        certification = certification_label(static, evas, spectre)
        counted = any(bool(row["counted_in_score"]) for row in forms)
        content_denominator_included = all(bool(row["content_denominator_included"]) for row in forms)
        exclusion_reasons = sorted(
            {
                str(reason)
                for row in forms
                for reason in row.get("exclusion_reasons", [])
                if not counted
            }
        )
        content_exclusion_reasons = sorted(
            {
                str(reason)
                for row in forms
                for reason in row.get("content_exclusion_reasons", [])
                if not content_denominator_included
            }
        )
        rows.append(
            {
                "release_entry_id": release_entry_id,
                "level": first.get("level", ""),
                "track": first.get("track", "core"),
                "difficulty": first.get("difficulty", "D2"),
                "category": first.get("category", ""),
                "base_function": first.get("base_function", ""),
                "package_status": "v1.1_promoted"
                if any(str(row.get("evidence", "")).endswith("vabench300_p0_p2_closure_20260620.md") for row in forms)
                else "current_l1_l2_release",
                "score_surface": score_surface_for(str(first.get("level", "")), str(first.get("track", "core"))),
                "release_entry_manifest": release_entry_manifest_path(release_entry_id),
                "form_count": len(forms),
                "forms": sorted(str(row["form"]) for row in forms),
                "certification": certification,
                "static": static,
                "evas": evas,
                "spectre": spectre,
                "counted_in_score": counted,
                "exclusion_reasons": [] if counted else exclusion_reasons,
                "content_denominator_included": content_denominator_included,
                "content_exclusion_reasons": content_exclusion_reasons,
                "release_blockers": [],
                "missing_forms": [],
            }
        )
    return rows


def build_report_from_rows(entry_rows: list[dict[str, Any]], form_rows: list[dict[str, Any]]) -> dict[str, Any]:
    release_status = read_json(REPORTS_ROOT / "release_status.json")
    conformance = read_json(REPORTS_ROOT / "conformance_manifest.json")
    completion = read_json(REPORTS_ROOT / "completion_audit.json")
    claim_gate = read_json(REPORTS_ROOT / "claim_gate.json")
    form_status_counts = dict(sorted(Counter(row["certification"] for row in form_rows).items()))
    entry_status_counts = dict(sorted(Counter(row["certification"] for row in entry_rows).items()))
    scored_entries = sum(1 for row in entry_rows if row["counted_in_score"])
    scored_forms = sum(1 for row in form_rows if row["counted_in_score"])
    content_denominator_entries = [row for row in entry_rows if row["content_denominator_included"]]
    content_denominator_forms = [row for row in form_rows if row["content_denominator_included"]]
    track_entry_counts = dict(sorted(Counter(row["track"] for row in entry_rows).items()))
    track_form_counts = dict(sorted(Counter(row["track"] for row in form_rows).items()))
    difficulty_entry_counts = dict(sorted(Counter(row["difficulty"] for row in entry_rows).items()))
    difficulty_form_counts = dict(sorted(Counter(row["difficulty"] for row in form_rows).items()))
    status = "complete" if completion.get("status") == "complete" else "in_progress"
    return {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "status": status,
        "package_root": rel(PACKAGE_ROOT),
        "summary": {
            "planned_entry_count": len(entry_rows),
            "entry_count": len(entry_rows),
            "form_count": len(form_rows),
            "track_entry_counts": track_entry_counts,
            "track_form_counts": track_form_counts,
            "difficulty_entry_counts": difficulty_entry_counts,
            "difficulty_form_counts": difficulty_form_counts,
            "core_entry_count": track_entry_counts.get("core", 0),
            "support_entry_count": track_entry_counts.get("support", 0),
            "core_form_count": track_form_counts.get("core", 0),
            "support_form_count": track_form_counts.get("support", 0),
            "content_denominator_entry_count": len(content_denominator_entries),
            "content_excluded_entry_count": len(entry_rows) - len(content_denominator_entries),
            "content_denominator_form_count": len(content_denominator_forms),
            "content_excluded_form_count": len(form_rows) - len(content_denominator_forms),
            "entry_status_counts": entry_status_counts,
            "form_status_counts": form_status_counts,
            "certified_entry_count": sum(1 for row in entry_rows if row["certification"] == "certified"),
            "certified_form_count": sum(1 for row in form_rows if row["certification"] == "certified"),
            "pending_entry_count": sum(1 for row in entry_rows if row["certification"] == "pending"),
            "pending_form_count": sum(1 for row in form_rows if row["certification"] == "pending"),
            "scored_entry_count": scored_entries,
            "scored_form_count": scored_forms,
            "core_scored_entry_count": sum(
                1 for row in entry_rows if row["track"] == "core" and row["counted_in_score"]
            ),
            "core_scored_form_count": sum(1 for row in form_rows if row["track"] == "core" and row["counted_in_score"]),
            "support_scored_entry_count": sum(
                1 for row in entry_rows if row["track"] == "support" and row["counted_in_score"]
            ),
            "support_scored_form_count": sum(
                1 for row in form_rows if row["track"] == "support" and row["counted_in_score"]
            ),
            "l0_conformance_case_count": int(conformance.get("conformance_case_count", 0) or 0),
            "l0_conformance_counted_in_denominator": int(conformance.get("benchmark_coverage_count", 0) or 0),
        },
        "entries": entry_rows,
        "forms": form_rows,
        "reports": {
            "release_status": rel(REPORTS_ROOT / "release_status.json"),
            "asset_integrity": rel(REPORTS_ROOT / "asset_integrity.json"),
            "static_certification": rel(REPORTS_ROOT / "static_certification.json"),
            "dual_certification": rel(REPORTS_ROOT / "dual_certification.json"),
            "score_denominator": rel(REPORTS_ROOT / "score_denominator_manifest.json"),
            "content_contract_audit": rel(REPORTS_ROOT / "content_contract_audit.json"),
            "claim_gate": rel(REPORTS_ROOT / "claim_gate.json"),
            "finish_readiness": rel(REPORTS_ROOT / "finish_readiness.json"),
            "completion_audit": rel(REPORTS_ROOT / "completion_audit.json"),
            "artifact_index": rel(REPORTS_ROOT / "artifact_index.json"),
        },
        "claim_boundary": [
            "This manifest is an index over package assets and reports; it is not simulator certification evidence.",
            "Rows with counted_in_score=false must not enter benchmark score denominators.",
            "Rows with content_denominator_included=false remain package assets but are excluded from strong benchmark content claims.",
            "Rows with track=support are auxiliary measurement/stimulus assets and must be reported separately from the core circuit score.",
            "Imported subset certification must not be phrased as full release certification.",
            f"claim_gate_status={claim_gate.get('status', 'missing')}",
            f"release_status_planned_entries={release_status.get('planned_entries', 'missing')}",
        ],
    }


def build_report() -> dict[str, Any]:
    vabench300_tasks = read_vabench300_tasks()
    if vabench300_tasks:
        form_rows = build_vabench300_form_rows(vabench300_tasks)
        entry_rows = build_vabench300_entry_rows(form_rows)
        return build_report_from_rows(entry_rows, form_rows)

    release_status = read_json(REPORTS_ROOT / "release_status.json")
    conformance = read_json(REPORTS_ROOT / "conformance_manifest.json")
    completion = read_json(REPORTS_ROOT / "completion_audit.json")
    claim_gate = read_json(REPORTS_ROOT / "claim_gate.json")
    score_entry_rows, score_form_rows = score_rows_by_id()
    entries_src = read_release_entries()
    entry_rows: list[dict[str, Any]] = []
    form_rows: list[dict[str, Any]] = []

    for entry in entries_src:
        release_entry_id = str(entry["release_entry_id"])
        entry_path = ROOT / str(entry.get("_manifest_path", ""))
        content_denominator_included = is_content_denominator_entry(release_entry_id)
        content_exclusion_reasons = content_denominator_exclusion_reasons(release_entry_id)
        forms: list[str] = []
        for task in entry.get("release_tasks", []):
            if not isinstance(task, dict):
                continue
            manifest_path = task_manifest_path(task)
            task_manifest = read_json(manifest_path)
            task_id = str(task_manifest.get("id", f"{release_entry_id}:{task.get('form', '')}"))
            score_form = score_form_rows.get(task_id, {})
            cert = task_manifest.get("certification", {})
            if not isinstance(cert, dict):
                cert = {}
            artifacts = task_manifest.get("artifacts", {})
            if not isinstance(artifacts, dict):
                artifacts = {}
            static = str(cert.get("static", task.get("static_status", "pending")))
            evas = str(cert.get("evas", task.get("evas_status", "pending")))
            spectre = str(cert.get("spectre", task.get("spectre_status", "pending")))
            form = str(task.get("form", ""))
            forms.append(form)
            form_rows.append(
                {
                    "task_id": task_id,
                    "release_entry_id": release_entry_id,
                    "form": form,
                    "family": str(task_manifest.get("family", "")),
                    "level": str(entry.get("level", "")),
                    "track": str(entry.get("track", "core")),
                    "difficulty": str(entry.get("difficulty", "D2")),
                    "category": str(entry.get("category", "")),
                    "base_function": str(entry.get("base_function", "")),
                    "release_task_manifest": rel(manifest_path),
                    "prompt": artifacts.get("prompt", task.get("prompt", "")),
                    "meta": artifacts.get("meta", task.get("meta", "")),
                    "checks": artifacts.get("checks", task.get("checks", "")),
                    "gold_count": len(artifacts.get("gold", task.get("gold", []))),
                    "static": static,
                    "evas": evas,
                    "spectre": spectre,
                    "certification": certification_label(static, evas, spectre),
                    "evidence": cert.get("evidence", task.get("dual_evidence", "")),
                    "counted_in_score": bool(score_form.get("counted_in_score", False)),
                    "exclusion_reasons": score_form.get("exclusion_reasons", []),
                    "content_denominator_included": content_denominator_included,
                    "content_exclusion_reasons": content_exclusion_reasons,
                }
            )

        entry_score = score_entry_rows.get(release_entry_id, {})
        entry_cert = entry.get("certification", {})
        if not isinstance(entry_cert, dict):
            entry_cert = {}
        entry_rows.append(
            {
                "release_entry_id": release_entry_id,
                "level": str(entry.get("level", "")),
                "track": str(entry.get("track", "core")),
                "difficulty": str(entry.get("difficulty", "D2")),
                "category": str(entry.get("category", "")),
                "base_function": str(entry.get("base_function", "")),
                "package_status": str(entry.get("package_status", "")),
                "score_surface": str(entry.get("score_surface", "")),
                "release_entry_manifest": rel(entry_path),
                "form_count": len(forms),
                "forms": sorted(forms),
                "certification": certification_label(
                    str(entry_cert.get("static", "pending")),
                    str(entry_cert.get("evas", "pending")),
                    str(entry_cert.get("spectre", "pending")),
                ),
                "static": str(entry_cert.get("static", "pending")),
                "evas": str(entry_cert.get("evas", "pending")),
                "spectre": str(entry_cert.get("spectre", "pending")),
                "counted_in_score": bool(entry_score.get("counted_in_score", False)),
                "exclusion_reasons": entry_score.get("exclusion_reasons", []),
                "content_denominator_included": content_denominator_included,
                "content_exclusion_reasons": content_exclusion_reasons,
                "release_blockers": entry.get("release_blockers", []),
                "missing_forms": entry.get("missing_forms", []),
            }
        )

    form_status_counts = dict(sorted(Counter(row["certification"] for row in form_rows).items()))
    entry_status_counts = dict(sorted(Counter(row["certification"] for row in entry_rows).items()))
    scored_entries = sum(1 for row in entry_rows if row["counted_in_score"])
    scored_forms = sum(1 for row in form_rows if row["counted_in_score"])
    content_denominator_entries = [row for row in entry_rows if row["content_denominator_included"]]
    content_denominator_forms = [row for row in form_rows if row["content_denominator_included"]]
    track_entry_counts = dict(sorted(Counter(row["track"] for row in entry_rows).items()))
    track_form_counts = dict(sorted(Counter(row["track"] for row in form_rows).items()))
    difficulty_entry_counts = dict(sorted(Counter(row["difficulty"] for row in entry_rows).items()))
    difficulty_form_counts = dict(sorted(Counter(row["difficulty"] for row in form_rows).items()))
    status = "complete" if completion.get("status") == "complete" else "in_progress"
    return {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "status": status,
        "package_root": rel(PACKAGE_ROOT),
        "summary": {
            "planned_entry_count": len(entry_rows),
            "entry_count": len(entry_rows),
            "form_count": len(form_rows),
            "track_entry_counts": track_entry_counts,
            "track_form_counts": track_form_counts,
            "difficulty_entry_counts": difficulty_entry_counts,
            "difficulty_form_counts": difficulty_form_counts,
            "core_entry_count": track_entry_counts.get("core", 0),
            "support_entry_count": track_entry_counts.get("support", 0),
            "core_form_count": track_form_counts.get("core", 0),
            "support_form_count": track_form_counts.get("support", 0),
            "content_denominator_entry_count": len(content_denominator_entries),
            "content_excluded_entry_count": len(entry_rows) - len(content_denominator_entries),
            "content_denominator_form_count": len(content_denominator_forms),
            "content_excluded_form_count": len(form_rows) - len(content_denominator_forms),
            "entry_status_counts": entry_status_counts,
            "form_status_counts": form_status_counts,
            "certified_entry_count": sum(1 for row in entry_rows if row["certification"] == "certified"),
            "certified_form_count": sum(1 for row in form_rows if row["certification"] == "certified"),
            "pending_entry_count": sum(1 for row in entry_rows if row["certification"] == "pending"),
            "pending_form_count": sum(1 for row in form_rows if row["certification"] == "pending"),
            "scored_entry_count": scored_entries,
            "scored_form_count": scored_forms,
            "core_scored_entry_count": sum(
                1 for row in entry_rows if row["track"] == "core" and row["counted_in_score"]
            ),
            "core_scored_form_count": sum(1 for row in form_rows if row["track"] == "core" and row["counted_in_score"]),
            "support_scored_entry_count": sum(
                1 for row in entry_rows if row["track"] == "support" and row["counted_in_score"]
            ),
            "support_scored_form_count": sum(
                1 for row in form_rows if row["track"] == "support" and row["counted_in_score"]
            ),
            "l0_conformance_case_count": int(conformance.get("conformance_case_count", 0) or 0),
            "l0_conformance_counted_in_denominator": int(conformance.get("benchmark_coverage_count", 0) or 0),
        },
        "entries": entry_rows,
        "forms": form_rows,
        "reports": {
            "release_status": rel(REPORTS_ROOT / "release_status.json"),
            "asset_integrity": rel(REPORTS_ROOT / "asset_integrity.json"),
            "static_certification": rel(REPORTS_ROOT / "static_certification.json"),
            "dual_certification": rel(REPORTS_ROOT / "dual_certification.json"),
            "score_denominator": rel(REPORTS_ROOT / "score_denominator_manifest.json"),
            "content_contract_audit": rel(REPORTS_ROOT / "content_contract_audit.json"),
            "claim_gate": rel(REPORTS_ROOT / "claim_gate.json"),
            "finish_readiness": rel(REPORTS_ROOT / "finish_readiness.json"),
            "completion_audit": rel(REPORTS_ROOT / "completion_audit.json"),
            "artifact_index": rel(REPORTS_ROOT / "artifact_index.json"),
        },
        "claim_boundary": [
            "This manifest is an index over package assets and reports; it is not simulator certification evidence.",
            "Rows with counted_in_score=false must not enter benchmark score denominators.",
            "Rows with content_denominator_included=false remain package assets but are excluded from strong benchmark content claims.",
            "Rows with track=support are auxiliary measurement/stimulus assets and must be reported separately from the core circuit score.",
            "Imported subset certification must not be phrased as full release certification.",
            f"claim_gate_status={claim_gate.get('status', 'missing')}",
        ],
    }


def write_csv(report: dict[str, Any]) -> None:
    fields = [
        "task_id",
        "release_entry_id",
        "form",
        "family",
        "level",
        "track",
        "difficulty",
        "category",
        "base_function",
        "certification",
        "static",
        "evas",
        "spectre",
        "counted_in_score",
        "content_denominator_included",
        "release_task_manifest",
        "evidence",
    ]
    with MANIFEST_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in report["forms"]:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_markdown(report: dict[str, Any]) -> None:
    summary = report["summary"]
    lines = [
        "# vaBench Release Package Manifest",
        "",
        f"Date: {report['date']}",
        "",
        "This package-level manifest indexes every release entry and materialized",
        "form. It is a navigation and machine-consumption layer, not simulator",
        "certification evidence.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| status | `{report['status']}` |",
        f"| planned entries | {summary['planned_entry_count']} |",
        f"| entries | {summary['entry_count']} |",
        f"| forms | {summary['form_count']} |",
        f"| core entries | {summary['core_entry_count']} |",
        f"| support entries | {summary['support_entry_count']} |",
        f"| core forms | {summary['core_form_count']} |",
        f"| support forms | {summary['support_form_count']} |",
        f"| content denominator entries | {summary['content_denominator_entry_count']} |",
        f"| content-excluded entries | {summary['content_excluded_entry_count']} |",
        f"| content denominator forms | {summary['content_denominator_form_count']} |",
        f"| content-excluded forms | {summary['content_excluded_form_count']} |",
        f"| certified entries | {summary['certified_entry_count']} |",
        f"| certified forms | {summary['certified_form_count']} |",
        f"| pending entries | {summary['pending_entry_count']} |",
        f"| pending forms | {summary['pending_form_count']} |",
        f"| scored entries | {summary['scored_entry_count']} |",
        f"| scored forms | {summary['scored_form_count']} |",
        f"| core scored entries | {summary['core_scored_entry_count']} |",
        f"| core scored forms | {summary['core_scored_form_count']} |",
        f"| support scored entries | {summary['support_scored_entry_count']} |",
        f"| support scored forms | {summary['support_scored_form_count']} |",
        f"| L0 conformance cases | {summary['l0_conformance_case_count']} |",
        "",
        "## Entry Status Counts",
        "",
        "| Status | Count |",
        "| --- | ---: |",
    ]
    for key, value in summary["entry_status_counts"].items():
        lines.append(f"| `{key}` | {value} |")
    lines.extend(["", "## Form Status Counts", "", "| Status | Count |", "| --- | ---: |"])
    for key, value in summary["form_status_counts"].items():
        lines.append(f"| `{key}` | {value} |")
    lines.extend(["", "## Claim Boundary", ""])
    for item in report["claim_boundary"]:
        lines.append(f"- {item}")
    MANIFEST_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    report = build_report()
    MANIFEST_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_csv(report)
    write_markdown(report)
    print(
        "wrote package manifest: status={status}; entries={entries}; forms={forms}".format(
            status=report["status"],
            entries=report["summary"]["entry_count"],
            forms=report["summary"]["form_count"],
        )
    )


if __name__ == "__main__":
    main()
