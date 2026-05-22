#!/usr/bin/env python3
from __future__ import annotations

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
CONFORMANCE_JSON = REPORTS_ROOT / "conformance_manifest.json"
ENABLEMENT_JSON = REPORTS_ROOT / "score_denominator_enablement.json"
REPORT_JSON = REPORTS_ROOT / "score_denominator_manifest.json"
REPORT_MD = REPORTS_ROOT / "score_denominator_manifest.md"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def read_release_entries() -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for path in sorted(TASKS_ROOT.glob("CT*/vbr1_*/release_entry.json")):
        payload = read_json(path)
        if payload:
            payload["_manifest_path"] = rel(path)
            entries.append(payload)
    return entries


def task_manifest_path(entry: dict[str, Any], task: dict[str, Any]) -> Path:
    release_path = task.get("release_path", "")
    return ROOT / str(release_path) / "release_task.json"


def task_status(task: dict[str, Any], task_manifest: dict[str, Any]) -> tuple[str, str, str]:
    cert = task_manifest.get("certification", {})
    if not isinstance(cert, dict):
        cert = {}
    static = str(cert.get("static", task.get("static_status", "pending")))
    evas = str(cert.get("evas", task.get("evas_status", "pending")))
    spectre = str(cert.get("spectre", task.get("spectre_status", "pending")))
    return static, evas, spectre


def entry_required_forms(entry: dict[str, Any]) -> list[str]:
    forms = [str(task.get("form", "")) for task in entry.get("release_tasks", []) if task.get("form")]
    missing = [str(item) for item in entry.get("missing_forms", [])]
    return sorted(set(forms + missing))


def entry_certified(entry: dict[str, Any], form_rows: list[dict[str, Any]]) -> bool:
    if entry.get("missing_forms") or entry.get("release_blockers"):
        return False
    expected_forms = set(entry_required_forms(entry))
    certified_forms = {
        str(row["form"])
        for row in form_rows
        if row["release_entry_id"] == entry["release_entry_id"] and row["certified"]
    }
    return bool(expected_forms) and expected_forms.issubset(certified_forms)


def form_exclusion_reasons(
    release_entry_id: str,
    task_manifest: dict[str, Any],
    static: str,
    evas: str,
    spectre: str,
) -> list[str]:
    reasons = []
    reasons.extend(
        f"content_denominator_excluded:{reason}"
        for reason in content_denominator_exclusion_reasons(release_entry_id)
    )
    counts = task_manifest.get("counts", {})
    if not isinstance(counts, dict) or not bool(counts.get("benchmark_score", False)):
        reasons.append("benchmark_score_disabled")
    if static != "pass":
        reasons.append(f"task_static:{static}")
    if evas != "pass":
        reasons.append(f"task_evas:{evas}")
    if spectre != "pass":
        reasons.append(f"task_spectre:{spectre}")
    return reasons


def entry_exclusion_reasons(entry: dict[str, Any], certified: bool) -> list[str]:
    reasons = []
    reasons.extend(
        f"content_denominator_excluded:{reason}"
        for reason in content_denominator_exclusion_reasons(str(entry["release_entry_id"]))
    )
    counts = entry.get("counts", {})
    if not isinstance(counts, dict) or not bool(counts.get("benchmark_score", False)):
        reasons.append("benchmark_score_disabled")
    if entry.get("missing_forms"):
        reasons.append("entry_missing_required_forms")
    for blocker in entry.get("release_blockers", []):
        reasons.append(f"entry_blocker:{blocker}")
    if not certified:
        reasons.append("entry_not_fully_certified")
    return reasons


def build_form_rows(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for entry in entries:
        for task in entry.get("release_tasks", []):
            manifest_path = task_manifest_path(entry, task)
            task_manifest = read_json(manifest_path)
            counts = task_manifest.get("counts", {})
            if not isinstance(counts, dict):
                counts = {}
            static, evas, spectre = task_status(task, task_manifest)
            certified = static == "pass" and evas == "pass" and spectre == "pass"
            benchmark_score_enabled = bool(counts.get("benchmark_score", False))
            content_denominator_included = is_content_denominator_entry(str(entry["release_entry_id"]))
            counted = content_denominator_included and benchmark_score_enabled and certified
            reasons = form_exclusion_reasons(str(entry["release_entry_id"]), task_manifest, static, evas, spectre)
            rows.append(
                {
                    "release_entry_id": entry["release_entry_id"],
                    "task_id": task_manifest.get("id", f"{entry['release_entry_id']}:{task.get('form', '')}"),
                    "form": task.get("form", ""),
                    "level": entry.get("level", ""),
                    "category": entry.get("category", ""),
                    "base_function": entry.get("base_function", ""),
                    "score_surface": entry.get("score_surface", ""),
                    "manifest": rel(manifest_path),
                    "static": static,
                    "evas": evas,
                    "spectre": spectre,
                    "certified": certified,
                    "benchmark_score_enabled": benchmark_score_enabled,
                    "content_denominator_included": content_denominator_included,
                    "counted_in_score": counted,
                    "exclusion_reasons": [] if counted else reasons,
                }
            )
    return rows


def build_entry_rows(entries: list[dict[str, Any]], form_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for entry in entries:
        counts = entry.get("counts", {})
        if not isinstance(counts, dict):
            counts = {}
        certified = entry_certified(entry, form_rows)
        benchmark_score_enabled = bool(counts.get("benchmark_score", False))
        content_denominator_included = is_content_denominator_entry(str(entry["release_entry_id"]))
        counted = content_denominator_included and benchmark_score_enabled and certified
        rows.append(
            {
                "release_entry_id": entry["release_entry_id"],
                "level": entry.get("level", ""),
                "category": entry.get("category", ""),
                "base_function": entry.get("base_function", ""),
                "score_surface": entry.get("score_surface", ""),
                "required_forms": entry_required_forms(entry),
                "missing_forms": entry.get("missing_forms", []),
                "release_blockers": entry.get("release_blockers", []),
                "manifest": entry.get("_manifest_path", ""),
                "certified": certified,
                "benchmark_score_enabled": benchmark_score_enabled,
                "content_denominator_included": content_denominator_included,
                "counted_in_score": counted,
                "exclusion_reasons": [] if counted else entry_exclusion_reasons(entry, certified),
            }
        )
    return rows


def reason_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for row in rows:
        counts.update(str(item) for item in row.get("exclusion_reasons", []))
    return dict(sorted(counts.items()))


def build_report() -> dict[str, Any]:
    entries = read_release_entries()
    form_rows = build_form_rows(entries)
    entry_rows = build_entry_rows(entries, form_rows)
    conformance = read_json(CONFORMANCE_JSON)
    scored_entries = sum(1 for row in entry_rows if row["counted_in_score"])
    scored_forms = sum(1 for row in form_rows if row["counted_in_score"])
    enabled_entries = sum(1 for row in entry_rows if row["benchmark_score_enabled"])
    enabled_forms = sum(1 for row in form_rows if row["benchmark_score_enabled"])
    certified_entries = sum(1 for row in entry_rows if row["certified"])
    certified_forms = sum(1 for row in form_rows if row["certified"])
    content_denominator_entries = [row for row in entry_rows if row["content_denominator_included"]]
    content_denominator_forms = [row for row in form_rows if row["content_denominator_included"]]
    l0_count = int(conformance.get("benchmark_coverage_count", 0) or 0)
    fully_certified = certified_entries == len(entry_rows) and certified_forms == len(form_rows)
    status = (
        "score_enabled"
        if scored_entries or scored_forms
        else "disabled_until_score_enablement"
        if fully_certified
        else "disabled_until_full_certification"
    )
    return {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "status": status,
        "summary": {
            "planned_entry_count": len(entry_rows),
            "release_form_count": len(form_rows),
            "content_denominator_entry_count": len(content_denominator_entries),
            "content_excluded_entry_count": len(entry_rows) - len(content_denominator_entries),
            "content_denominator_form_count": len(content_denominator_forms),
            "content_excluded_form_count": len(form_rows) - len(content_denominator_forms),
            "certified_entry_count": certified_entries,
            "certified_form_count": certified_forms,
            "benchmark_score_enabled_entry_count": enabled_entries,
            "benchmark_score_enabled_form_count": enabled_forms,
            "scored_entry_count": scored_entries,
            "scored_form_count": scored_forms,
            "l0_conformance_counted_in_denominator": l0_count,
            "entry_exclusion_reason_counts": reason_counts(entry_rows),
            "form_exclusion_reason_counts": reason_counts(form_rows),
        },
        "claim_rule": {
            "source_of_truth": rel(REPORT_JSON),
            "denominator_policy": (
                "Only rows with benchmark_score_enabled=true and static/evas/spectre pass may enter "
                "the benchmark score denominator. Content-excluded duplicates and L0 conformance "
                "remain excluded."
            ),
            "score_claim_allowed": bool(scored_entries or scored_forms) and l0_count == 0,
        },
        "entry_rows": entry_rows,
        "form_rows": form_rows,
        "evidence_sources": {
            "release_tasks_root": rel(TASKS_ROOT),
            "conformance_manifest": rel(CONFORMANCE_JSON),
            "score_denominator_enablement": rel(ENABLEMENT_JSON),
        },
    }


def write_markdown(report: dict[str, Any]) -> None:
    summary = report["summary"]
    lines = [
        "# vaBench Release Score Denominator Manifest",
        "",
        f"Date: {report['date']}",
        "",
        "This manifest is the source of truth for what is allowed to enter the",
        "benchmark score denominator. Counted rows must be in the frozen content",
        "denominator, score-enabled, and certified by static, EVAS, and Spectre checks.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| status | `{report['status']}` |",
        f"| planned entries | {summary['planned_entry_count']} |",
        f"| release forms | {summary['release_form_count']} |",
        f"| content denominator entries | {summary['content_denominator_entry_count']} |",
        f"| content-excluded entries | {summary['content_excluded_entry_count']} |",
        f"| content denominator forms | {summary['content_denominator_form_count']} |",
        f"| content-excluded forms | {summary['content_excluded_form_count']} |",
        f"| certified entries | {summary['certified_entry_count']} |",
        f"| certified forms | {summary['certified_form_count']} |",
        f"| score-enabled entries | {summary['benchmark_score_enabled_entry_count']} |",
        f"| score-enabled forms | {summary['benchmark_score_enabled_form_count']} |",
        f"| scored entries | {summary['scored_entry_count']} |",
        f"| scored forms | {summary['scored_form_count']} |",
        f"| L0 conformance counted | {summary['l0_conformance_counted_in_denominator']} |",
        "",
        "## Entry Exclusion Reasons",
        "",
    ]
    for key, value in summary["entry_exclusion_reason_counts"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Form Exclusion Reasons", ""])
    for key, value in summary["form_exclusion_reason_counts"].items():
        lines.append(f"- `{key}`: {value}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    report = build_report()
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report)
    summary = report["summary"]
    print(
        "wrote score denominator manifest: status={status}; scored_entries={entries}; scored_forms={forms}".format(
            status=report["status"],
            entries=summary["scored_entry_count"],
            forms=summary["scored_form_count"],
        )
    )


if __name__ == "__main__":
    main()
