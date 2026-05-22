#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
TASKS_ROOT = PACKAGE_ROOT / "tasks"
REPORT_JSON = PACKAGE_ROOT / "reports" / "asset_integrity.json"
REPORT_MD = PACKAGE_ROOT / "reports" / "asset_integrity.md"

FAMILY_BY_FORM = {
    "dut": "spec-to-va",
    "tb": "tb-generation",
    "bugfix": "bugfix",
    "e2e": "end-to-end",
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_entries() -> list[tuple[Path, dict[str, object]]]:
    entries: list[tuple[Path, dict[str, object]]] = []
    for path in sorted(TASKS_ROOT.glob("*/release_entry.json")):
        entries.append((path, json.loads(path.read_text(encoding="utf-8"))))
    return entries


def nonempty(path: Path) -> bool:
    return path.exists() and path.is_file() and path.read_text(encoding="utf-8", errors="ignore").strip() != ""


def audit_release_task(entry_id: str, task: dict[str, object]) -> dict[str, object]:
    issues: list[str] = []
    warnings: list[str] = []
    form = str(task.get("form", ""))
    form_dir = ROOT / str(task.get("release_path", ""))
    prompt = ROOT / str(task.get("prompt", ""))
    meta = ROOT / str(task.get("meta", ""))
    checks = ROOT / str(task.get("checks", ""))
    gold_paths = [ROOT / str(path) for path in task.get("gold", [])]

    if form not in FAMILY_BY_FORM:
        issues.append(f"unknown form {form!r}")
    if not form_dir.is_dir():
        issues.append("release_path is not a directory")
    for label, path in (("prompt", prompt), ("meta", meta), ("checks", checks)):
        if not nonempty(path):
            issues.append(f"{label} missing or empty")
    if not gold_paths:
        issues.append("gold file list is empty")
    for path in gold_paths:
        if not path.exists() or not path.is_file():
            issues.append(f"gold path missing: {rel(path)}")
        elif path.read_text(encoding="utf-8", errors="ignore").strip() == "":
            issues.append(f"gold path empty: {rel(path)}")

    meta_payload = {}
    if meta.exists():
        try:
            meta_payload = json.loads(meta.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            issues.append(f"meta.json is not valid JSON: {exc}")
    if meta_payload:
        expected_family = FAMILY_BY_FORM.get(form)
        if meta_payload.get("family") != expected_family:
            issues.append(f"meta family {meta_payload.get('family')!r} does not match form {form!r}")
        if meta_payload.get("domain") != "voltage":
            issues.append(f"meta domain {meta_payload.get('domain')!r} is not voltage")
        for key in ("id", "task_id", "asset_type", "expected_backend"):
            if key not in meta_payload:
                warnings.append(f"meta missing {key}")
        if meta_payload.get("asset_type") != "vabench_task":
            warnings.append("meta asset_type is not vabench_task")

    if checks.exists():
        checks_text = checks.read_text(encoding="utf-8", errors="ignore")
        if "sim_correct:" not in checks_text:
            issues.append("checks.yaml missing sim_correct")
        if "parity:" not in checks_text:
            issues.append("checks.yaml missing parity")
        if "syntax:" not in checks_text:
            warnings.append("checks.yaml missing syntax guardrail section")

    if prompt.exists():
        prompt_text = prompt.read_text(encoding="utf-8", errors="ignore")
        if "Return exactly" not in prompt_text:
            warnings.append("prompt does not use an explicit 'Return exactly' output contract")
        if form == "bugfix" and "bug" not in prompt_text.lower():
            warnings.append("bugfix prompt does not explicitly mention a bug")

    gold_suffixes = {path.suffix for path in gold_paths}
    if form in {"dut", "bugfix", "e2e"} and ".va" not in gold_suffixes:
        issues.append("gold assets do not include Verilog-A source")
    if form in {"tb", "e2e"} and ".scs" not in gold_suffixes:
        issues.append("gold assets do not include Spectre testbench")
    if form == "bugfix":
        gold_names = {path.name for path in gold_paths}
        if "dut_buggy.va" not in gold_names or "dut_fixed.va" not in gold_names:
            issues.append("bugfix gold must include dut_buggy.va and dut_fixed.va")

    return {
        "entry_id": entry_id,
        "form": form,
        "release_path": rel(form_dir),
        "status": "pass" if not issues else "fail",
        "issues": issues,
        "warnings": warnings,
    }


def build_report() -> dict[str, object]:
    task_reports: list[dict[str, object]] = []
    for _, entry in read_entries():
        entry_id = str(entry["release_entry_id"])
        for task in entry.get("release_tasks", []):
            if isinstance(task, dict):
                task_reports.append(audit_release_task(entry_id, task))

    issue_count = sum(len(task["issues"]) for task in task_reports)
    warning_count = sum(len(task["warnings"]) for task in task_reports)
    form_counts = Counter(str(task["form"]) for task in task_reports)
    status = "pass" if issue_count == 0 else "fail"
    return {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "status": status,
        "audited_release_task_count": len(task_reports),
        "form_counts": dict(sorted(form_counts.items())),
        "issue_count": issue_count,
        "warning_count": warning_count,
        "task_reports": task_reports,
        "notes": [
            "This is an asset integrity audit only.",
            "A pass here does not imply EVAS or Spectre certification.",
            "Warnings identify release wording/checker polish risks that should be reviewed before scoring.",
        ],
    }


def write_markdown(report: dict[str, object]) -> None:
    lines = [
        "# vaBench Release Asset Integrity",
        "",
        f"Date: {report['date']}",
        "",
        "This report checks copied release assets for parseability, file presence,",
        "basic metadata consistency, and obvious prompt/checker guardrails. It is",
        "not a simulator certification report.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| status | `{report['status']}` |",
        f"| audited release forms | {report['audited_release_task_count']} |",
        f"| blocking issues | {report['issue_count']} |",
        f"| review warnings | {report['warning_count']} |",
        "",
        "## Form Counts",
        "",
        "| Form | Count |",
        "| --- | ---: |",
    ]
    for form, count in dict(report["form_counts"]).items():
        lines.append(f"| {form} | {count} |")

    warnings = [task for task in report["task_reports"] if task["warnings"]]
    issues = [task for task in report["task_reports"] if task["issues"]]
    lines.extend(["", "## Blocking Issues", "", "| Entry | Form | Issues |", "| --- | --- | --- |"])
    if issues:
        for task in issues:
            lines.append(f"| `{task['entry_id']}` | `{task['form']}` | {'; '.join(task['issues'])} |")
    else:
        lines.append("| none | none | none |")

    lines.extend(["", "## Review Warnings", "", "| Entry | Form | Warnings |", "| --- | --- | --- |"])
    if warnings:
        for task in warnings:
            lines.append(f"| `{task['entry_id']}` | `{task['form']}` | {'; '.join(task['warnings'])} |")
    else:
        lines.append("| none | none | none |")

    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    report = build_report()
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report)
    print(
        "audited {forms} release forms; {issues} issues; {warnings} warnings".format(
            forms=report["audited_release_task_count"],
            issues=report["issue_count"],
            warnings=report["warning_count"],
        )
    )
    if report["issue_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
