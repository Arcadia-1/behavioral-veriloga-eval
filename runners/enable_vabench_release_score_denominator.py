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
DUAL_REPORT_JSON = REPORTS_ROOT / "dual_certification.json"
REPORT_JSON = REPORTS_ROOT / "score_denominator_enablement.json"
REPORT_MD = REPORTS_ROOT / "score_denominator_enablement.md"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def as_int(value: object) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def dual_certification_complete(dual: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if dual.get("status") != "pass":
        reasons.append(f"dual_certification.status={dual.get('status', 'missing')}")
    if as_int(dual.get("dual_pending_release_task_count")):
        reasons.append("dual_pending_release_task_count is nonzero")
    if as_int(dual.get("dual_failed_release_task_count")):
        reasons.append("dual_failed_release_task_count is nonzero")
    if as_int(dual.get("evas_pass_spectre_fail_count")):
        reasons.append("evas_pass_spectre_fail_count is nonzero")
    if as_int(dual.get("dual_certified_release_task_count")) == 0:
        reasons.append("dual_certified_release_task_count is zero")
    return not reasons, reasons


def task_manifest_path(task: dict[str, Any]) -> Path:
    return ROOT / str(task.get("release_path", "")) / "release_task.json"


def task_statuses(entry: dict[str, Any], task: dict[str, Any]) -> tuple[str, str, str]:
    task_manifest = read_json(task_manifest_path(task))
    certification = task_manifest.get("certification", {})
    if not isinstance(certification, dict):
        certification = {}
    entry_certification = entry.get("certification", {})
    if not isinstance(entry_certification, dict):
        entry_certification = {}
    static = str(certification.get("static", task.get("static_status", entry_certification.get("static", "pending"))))
    evas = str(certification.get("evas", task.get("evas_status", "pending")))
    spectre = str(certification.get("spectre", task.get("spectre_status", "pending")))
    return static, evas, spectre


def entry_certified(entry: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    certification = entry.get("certification", {})
    if not isinstance(certification, dict):
        certification = {}
    for key in ("static", "evas", "spectre"):
        if certification.get(key) != "pass":
            reasons.append(f"entry_{key}:{certification.get(key, 'missing')}")
    if entry.get("missing_forms"):
        reasons.append("entry_missing_required_forms")
    for blocker in entry.get("release_blockers", []):
        reasons.append(f"entry_blocker:{blocker}")

    tasks = entry.get("release_tasks", [])
    if not isinstance(tasks, list) or not tasks:
        reasons.append("entry_has_no_release_tasks")
        tasks = []
    for task in tasks:
        if not isinstance(task, dict):
            reasons.append("entry_has_malformed_release_task")
            continue
        static, evas, spectre = task_statuses(entry, task)
        form = str(task.get("form", "unknown"))
        if static != "pass":
            reasons.append(f"{form}_static:{static}")
        if evas != "pass":
            reasons.append(f"{form}_evas:{evas}")
        if spectre != "pass":
            reasons.append(f"{form}_spectre:{spectre}")
    return not reasons, reasons


def read_release_entries() -> list[tuple[Path, dict[str, Any]]]:
    rows: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(TASKS_ROOT.glob("*/release_entry.json")):
        rows.append((path, read_json(path)))
    return rows


def set_entry_counts(entry: dict[str, Any], *, benchmark_score: bool) -> None:
    counts = entry.get("counts", {})
    if not isinstance(counts, dict):
        counts = {}
    entry["counts"] = {
        **counts,
        "benchmark_score": benchmark_score,
        "model_capability": False,
        "l0_conformance": False,
    }


def build_and_apply_report() -> dict[str, Any]:
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    dual = read_json(DUAL_REPORT_JSON)
    dual_ready, dual_blockers = dual_certification_complete(dual)
    entries = read_release_entries()
    entry_rows: list[dict[str, Any]] = []
    form_rows: list[dict[str, Any]] = []
    reason_counts: Counter[str] = Counter()

    for path, entry in entries:
        release_entry_id = str(entry.get("release_entry_id", path.parent.name))
        certified, certification_reasons = entry_certified(entry)
        content_included = is_content_denominator_entry(release_entry_id)
        content_reasons = content_denominator_exclusion_reasons(release_entry_id)
        enabled = dual_ready and certified and content_included
        if not enabled:
            reason_counts.update(content_reasons or [])
            reason_counts.update(certification_reasons)
            reason_counts.update(dual_blockers)
        set_entry_counts(entry, benchmark_score=enabled)
        write_json(path, entry)

        tasks = [task for task in entry.get("release_tasks", []) if isinstance(task, dict)]
        entry_rows.append(
            {
                "release_entry_id": release_entry_id,
                "manifest": rel(path),
                "certified": certified,
                "content_denominator_included": content_included,
                "benchmark_score_enabled": enabled,
                "disabled_reasons": []
                if enabled
                else [
                    *[f"content_denominator_excluded:{reason}" for reason in content_reasons],
                    *certification_reasons,
                    *dual_blockers,
                ],
                "form_count": len(tasks),
            }
        )
        for task in tasks:
            form_rows.append(
                {
                    "release_entry_id": release_entry_id,
                    "form": str(task.get("form", "")),
                    "manifest": rel(task_manifest_path(task)),
                    "benchmark_score_enabled": enabled,
                    "content_denominator_included": content_included,
                    "certified": certified,
                }
            )

    enabled_entries = [row for row in entry_rows if row["benchmark_score_enabled"]]
    disabled_entries = [row for row in entry_rows if not row["benchmark_score_enabled"]]
    enabled_forms = [row for row in form_rows if row["benchmark_score_enabled"]]
    disabled_forms = [row for row in form_rows if not row["benchmark_score_enabled"]]
    content_excluded_entries = [row for row in entry_rows if not row["content_denominator_included"]]
    content_excluded_forms = [row for row in form_rows if not row["content_denominator_included"]]
    return {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "status": "enabled" if dual_ready and enabled_entries else "blocked",
        "summary": {
            "release_entry_count": len(entry_rows),
            "release_form_count": len(form_rows),
            "enabled_entry_count": len(enabled_entries),
            "enabled_form_count": len(enabled_forms),
            "disabled_entry_count": len(disabled_entries),
            "disabled_form_count": len(disabled_forms),
            "content_excluded_entry_count": len(content_excluded_entries),
            "content_excluded_form_count": len(content_excluded_forms),
            "dual_certification_ready": dual_ready,
            "dual_blockers": dual_blockers,
            "disabled_reason_counts": dict(sorted(reason_counts.items())),
        },
        "policy": {
            "source_of_truth_after_refresh": rel(REPORTS_ROOT / "score_denominator_manifest.json"),
            "enabled_rule": "benchmark_score=true only for content-denominator entries with full static/EVAS/Spectre certification after dual_certification.status=pass.",
            "excluded_rule": "Content-excluded duplicates remain package assets and certified parity evidence, but do not enter scored benchmark denominators.",
            "l0_rule": "L0 conformance remains outside the L1/L2 benchmark denominator.",
        },
        "entry_rows": entry_rows,
        "form_rows": form_rows,
        "evidence_sources": {
            "dual_certification": rel(DUAL_REPORT_JSON),
            "release_tasks_root": rel(TASKS_ROOT),
            "policy": rel(ROOT / "runners" / "vabench_policy.py"),
        },
    }


def write_markdown(report: dict[str, Any]) -> None:
    summary = report["summary"]
    lines = [
        "# vaBench Release Score Denominator Enablement",
        "",
        f"Date: {report['date']}",
        "",
        "This report records the P1 write step that freezes `counts.benchmark_score`",
        "for the release package before the score denominator manifest is rebuilt.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| status | `{report['status']}` |",
        f"| release entries | {summary['release_entry_count']} |",
        f"| release forms | {summary['release_form_count']} |",
        f"| score-enabled entries | {summary['enabled_entry_count']} |",
        f"| score-enabled forms | {summary['enabled_form_count']} |",
        f"| disabled entries | {summary['disabled_entry_count']} |",
        f"| disabled forms | {summary['disabled_form_count']} |",
        f"| content-excluded entries | {summary['content_excluded_entry_count']} |",
        f"| content-excluded forms | {summary['content_excluded_form_count']} |",
        f"| dual certification ready | `{summary['dual_certification_ready']}` |",
        "",
        "## Policy",
        "",
    ]
    for key, value in report["policy"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Disabled Reasons", ""])
    reason_counts = summary["disabled_reason_counts"]
    if not reason_counts:
        lines.append("- none")
    for key, value in reason_counts.items():
        lines.append(f"- `{key}`: {value}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    report = build_and_apply_report()
    write_json(REPORT_JSON, report)
    write_markdown(report)
    summary = report["summary"]
    print(
        "score denominator enablement: status={status}; enabled_entries={entries}; enabled_forms={forms}".format(
            status=report["status"],
            entries=summary["enabled_entry_count"],
            forms=summary["enabled_form_count"],
        )
    )
    if report["status"] != "enabled":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
