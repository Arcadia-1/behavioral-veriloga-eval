#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

from vabench_policy import content_denominator_exclusion_reasons, is_content_denominator_entry


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
TASKS_ROOT = PACKAGE_ROOT / "tasks"
REPORTS_ROOT = PACKAGE_ROOT / "reports"
MANIFEST_JSON = PACKAGE_ROOT / "MANIFEST.json"
MANIFEST_CSV = PACKAGE_ROOT / "MANIFEST.csv"
MANIFEST_MD = PACKAGE_ROOT / "MANIFEST.md"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


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


def read_entries() -> list[tuple[Path, dict[str, Any]]]:
    rows: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(TASKS_ROOT.glob("CT*/vbr1_*/release_entry.json")):
        rows.append((path, read_json(path)))
    return rows


def certification_label(static: str, evas: str, spectre: str) -> str:
    if static == "pass" and evas == "pass" and spectre == "pass":
        return "certified"
    if static == "fail" or evas == "fail" or spectre == "fail":
        return "failed"
    return "pending"


def build_report() -> dict[str, Any]:
    release_status = read_json(REPORTS_ROOT / "release_status.json")
    conformance = read_json(REPORTS_ROOT / "conformance_manifest.json")
    completion = read_json(REPORTS_ROOT / "completion_audit.json")
    claim_gate = read_json(REPORTS_ROOT / "claim_gate.json")
    score_entry_rows, score_form_rows = score_rows_by_id()
    entries_src = read_entries()
    entry_rows: list[dict[str, Any]] = []
    form_rows: list[dict[str, Any]] = []

    for entry_path, entry in entries_src:
        release_entry_id = str(entry["release_entry_id"])
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
    status = "complete" if completion.get("status") == "complete" else "in_progress"
    return {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "status": status,
        "package_root": rel(PACKAGE_ROOT),
        "summary": {
            "planned_entry_count": int(release_status.get("planned_entries", len(entry_rows)) or 0),
            "entry_count": len(entry_rows),
            "form_count": len(form_rows),
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
