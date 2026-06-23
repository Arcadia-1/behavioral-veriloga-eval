#!/usr/bin/env python3
from __future__ import annotations

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
CONFORMANCE_JSON = REPORTS_ROOT / "conformance_manifest.json"
ENABLEMENT_JSON = REPORTS_ROOT / "score_denominator_enablement.json"
ENABLEMENT_MD = REPORTS_ROOT / "score_denominator_enablement.md"
REPORT_JSON = REPORTS_ROOT / "score_denominator_manifest.json"
REPORT_MD = REPORTS_ROOT / "score_denominator_manifest.md"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


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
                    "track": entry.get("track", "core"),
                    "difficulty": entry.get("difficulty", "D2"),
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
                "track": entry.get("track", "core"),
                "difficulty": entry.get("difficulty", "D2"),
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
    track_entry_counts = dict(sorted(Counter(row["track"] for row in entry_rows).items()))
    track_form_counts = dict(sorted(Counter(row["track"] for row in form_rows).items()))
    difficulty_entry_counts = dict(sorted(Counter(row["difficulty"] for row in entry_rows).items()))
    difficulty_form_counts = dict(sorted(Counter(row["difficulty"] for row in form_rows).items()))
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
            "certified_entry_count": certified_entries,
            "certified_form_count": certified_forms,
            "benchmark_score_enabled_entry_count": enabled_entries,
            "benchmark_score_enabled_form_count": enabled_forms,
            "scored_entry_count": scored_entries,
            "scored_form_count": scored_forms,
            "core_scored_entry_count": sum(1 for row in entry_rows if row["track"] == "core" and row["counted_in_score"]),
            "core_scored_form_count": sum(1 for row in form_rows if row["track"] == "core" and row["counted_in_score"]),
            "support_scored_entry_count": sum(
                1 for row in entry_rows if row["track"] == "support" and row["counted_in_score"]
            ),
            "support_scored_form_count": sum(
                1 for row in form_rows if row["track"] == "support" and row["counted_in_score"]
            ),
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
                " Measurement/stimulus support-suite rows remain package assets but are reported outside "
                "the core circuit score."
            ),
            "score_claim_allowed": bool(scored_entries or scored_forms) and l0_count == 0,
        },
        "entry_rows": entry_rows,
        "form_rows": form_rows,
        "evidence_sources": {
            "release_tasks_root": rel(TASKS_ROOT),
            "release_surface_reader": "runners/vabench_release_surface.py",
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
        f"| score-enabled entries | {summary['benchmark_score_enabled_entry_count']} |",
        f"| score-enabled forms | {summary['benchmark_score_enabled_form_count']} |",
        f"| scored entries | {summary['scored_entry_count']} |",
        f"| scored forms | {summary['scored_form_count']} |",
        f"| core scored entries | {summary['core_scored_entry_count']} |",
        f"| core scored forms | {summary['core_scored_form_count']} |",
        f"| support scored entries | {summary['support_scored_entry_count']} |",
        f"| support scored forms | {summary['support_scored_form_count']} |",
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


def write_deferred_enablement_snapshot(report: dict[str, Any]) -> None:
    if report["status"] == "score_enabled":
        return
    summary = report["summary"]
    entry_rows = report["entry_rows"]
    form_rows = report["form_rows"]
    snapshot = {
        "date": report["date"],
        "release": report["release"],
        "status": "blocked",
        "summary": {
            "release_entry_count": summary["planned_entry_count"],
            "release_form_count": summary["release_form_count"],
            "enabled_entry_count": 0,
            "enabled_form_count": 0,
            "disabled_entry_count": summary["planned_entry_count"],
            "disabled_form_count": summary["release_form_count"],
            "content_excluded_entry_count": summary["content_excluded_entry_count"],
            "content_excluded_form_count": summary["content_excluded_form_count"],
            "benchmark_score_flagged_entry_count": summary["benchmark_score_enabled_entry_count"],
            "benchmark_score_flagged_form_count": summary["benchmark_score_enabled_form_count"],
            "scored_entry_count": summary["scored_entry_count"],
            "scored_form_count": summary["scored_form_count"],
            "dual_certification_ready": False,
            "dual_blockers": [f"score_denominator_manifest.status={report['status']}"],
            "disabled_reason_counts": dict(summary["entry_exclusion_reason_counts"]),
        },
        "policy": {
            "source_of_truth_after_refresh": rel(REPORT_JSON),
            "enabled_rule": (
                "benchmark_score flags may mark the intended release denominator, but score enablement "
                "is blocked until every counted row has static/EVAS/Spectre certification."
            ),
            "excluded_rule": "Content-excluded duplicates remain package assets but do not enter scored benchmark denominators.",
            "l0_rule": "L0 conformance remains outside the L1/L2 benchmark denominator.",
        },
        "entry_rows": [
            {
                "release_entry_id": row["release_entry_id"],
                "manifest": row["manifest"],
                "certified": row["certified"],
                "content_denominator_included": row["content_denominator_included"],
                "benchmark_score_flagged": row["benchmark_score_enabled"],
                "score_enabled": row["counted_in_score"],
                "disabled_reasons": row["exclusion_reasons"],
                "form_count": len(row["required_forms"]),
            }
            for row in entry_rows
        ],
        "form_rows": [
            {
                "release_entry_id": row["release_entry_id"],
                "form": row["form"],
                "manifest": row["manifest"],
                "certified": row["certified"],
                "content_denominator_included": row["content_denominator_included"],
                "benchmark_score_flagged": row["benchmark_score_enabled"],
                "score_enabled": row["counted_in_score"],
            }
            for row in form_rows
        ],
        "evidence_sources": {
            "score_denominator_manifest": rel(REPORT_JSON),
            "release_tasks_root": rel(TASKS_ROOT),
        },
        "notes": [
            "This is a current blocked snapshot, not a successful score-enablement write step.",
            "score_denominator_manifest.json remains the source of truth for counted_in_score rows.",
        ],
    }
    ENABLEMENT_JSON.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# vaBench Release Score Denominator Enablement",
        "",
        f"Date: {snapshot['date']}",
        "",
        "This is a blocked snapshot for the current release package. It replaces older",
        "enablement records so current reports do not point at removed entries.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| status | `{snapshot['status']}` |",
        f"| release entries | {snapshot['summary']['release_entry_count']} |",
        f"| release forms | {snapshot['summary']['release_form_count']} |",
        f"| score-enabled entries | {snapshot['summary']['enabled_entry_count']} |",
        f"| score-enabled forms | {snapshot['summary']['enabled_form_count']} |",
        f"| benchmark-score-flagged entries | {snapshot['summary']['benchmark_score_flagged_entry_count']} |",
        f"| benchmark-score-flagged forms | {snapshot['summary']['benchmark_score_flagged_form_count']} |",
        f"| scored entries | {snapshot['summary']['scored_entry_count']} |",
        f"| scored forms | {snapshot['summary']['scored_form_count']} |",
        f"| dual certification ready | `{snapshot['summary']['dual_certification_ready']}` |",
        "",
        "## Blocking Rule",
        "",
        snapshot["policy"]["enabled_rule"],
    ]
    ENABLEMENT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    report = build_report()
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report)
    write_deferred_enablement_snapshot(report)
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
