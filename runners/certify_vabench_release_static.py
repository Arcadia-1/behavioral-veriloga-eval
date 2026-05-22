#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
TASKS_ROOT = PACKAGE_ROOT / "tasks"
EVIDENCE_ROOT = PACKAGE_ROOT / "evidence" / "static"
REPORT_JSON = PACKAGE_ROOT / "reports" / "static_certification.json"
REPORT_MD = PACKAGE_ROOT / "reports" / "static_certification.md"


@dataclass(frozen=True)
class SyntaxGuardrails:
    must_include: list[str]
    must_not_include: list[str]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_entries() -> list[tuple[Path, dict[str, object]]]:
    entries: list[tuple[Path, dict[str, object]]] = []
    for path in sorted(TASKS_ROOT.glob("*/release_entry.json")):
        entries.append((path, json.loads(path.read_text(encoding="utf-8"))))
    return entries


def parse_yaml_scalar(value: str) -> str:
    value = value.strip()
    if value in {"[]", ""}:
        return ""
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


def parse_syntax_guardrails(path: Path) -> SyntaxGuardrails:
    must_include: list[str] = []
    must_not_include: list[str] = []
    in_syntax = False
    target: list[str] | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        stripped = raw.strip()
        if stripped == "syntax:":
            in_syntax = True
            target = None
            continue
        if in_syntax and raw and not raw.startswith(" "):
            break
        if not in_syntax:
            continue
        if stripped.startswith("must_include:"):
            target = must_include
            suffix = parse_yaml_scalar(stripped.split(":", 1)[1])
            if suffix:
                target.append(suffix)
            continue
        if stripped.startswith("must_not_include:"):
            target = must_not_include
            suffix = parse_yaml_scalar(stripped.split(":", 1)[1])
            if suffix:
                target.append(suffix)
            continue
        if stripped.startswith("-") and target is not None:
            value = parse_yaml_scalar(stripped[1:])
            if value:
                target.append(value)
    return SyntaxGuardrails(must_include=must_include, must_not_include=must_not_include)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def text_has_token(text: str, token: str) -> bool:
    if token == "tran":
        return re.search(r"\btran\b", text) is not None
    if token == "save":
        return re.search(r"\bsave\b", text) is not None
    return token in text


def task_gold_text(task: dict[str, object]) -> str:
    chunks: list[str] = []
    for gold in task.get("gold", []):
        path = ROOT / str(gold)
        if path.exists() and path.is_file():
            chunks.append(read_text(path))
    return "\n".join(chunks)


def task_va_text(task: dict[str, object]) -> str:
    chunks: list[str] = []
    for gold in task.get("gold", []):
        path = ROOT / str(gold)
        if path.suffix == ".va" and path.exists() and path.is_file():
            chunks.append(read_text(path))
    return "\n".join(chunks)


def certify_task(entry: dict[str, object], task: dict[str, object]) -> dict[str, object]:
    entry_id = str(entry["release_entry_id"])
    form = str(task["form"])
    task_id = f"{entry_id}:{form}"
    checks_path = ROOT / str(task["checks"])
    guardrails = parse_syntax_guardrails(checks_path)
    gold_text = task_gold_text(task)
    va_text = task_va_text(task)

    failures: list[str] = []
    for token in guardrails.must_include:
        if not text_has_token(gold_text, token):
            failures.append(f"must_include token missing from gold assets: {token}")
    for token in guardrails.must_not_include:
        if text_has_token(va_text, token):
            failures.append(f"must_not_include token present in Verilog-A gold assets: {token}")

    status = "pass" if not failures else "fail"
    evidence_dir = EVIDENCE_ROOT / entry_id / form
    evidence_dir.mkdir(parents=True, exist_ok=True)
    evidence_path = evidence_dir / "evidence.json"
    result_path = evidence_dir / "result.json"

    evidence = {
        "release_entry_id": entry_id,
        "task_id": task_id,
        "task_form": form,
        "taxonomy": {
            "level": entry["level"],
            "category": entry["category"],
            "base_function": entry["base_function"],
        },
        "static": status,
        "evas": "pending",
        "spectre": "pending",
        "verdict": "not_certified" if status == "pass" else "quarantined",
        "artifacts": [str(task["prompt"]), str(task["meta"]), str(task["checks"]), *task.get("gold", [])],
        "checks": {
            "must_include": guardrails.must_include,
            "must_not_include": guardrails.must_not_include,
            "failures": failures,
        },
        "notes": "Static release certification only; EVAS and Spectre remain pending.",
    }
    result = {
        "task_id": task_id,
        "release_entry_id": entry_id,
        "backend": "static",
        "status": "PASS" if status == "pass" else "FAIL_STATIC",
        "scores": {
            "must_include_total": len(guardrails.must_include),
            "must_not_include_total": len(guardrails.must_not_include),
            "failure_count": len(failures),
        },
        "artifacts": [rel(evidence_path), rel(result_path)],
        "notes": failures,
    }
    evidence_path.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    task["static_status"] = status
    task["static_evidence"] = rel(evidence_path)
    task["static_result"] = rel(result_path)

    return {
        "entry_id": entry_id,
        "form": form,
        "task_id": task_id,
        "status": status,
        "failure_count": len(failures),
        "failures": failures,
        "evidence": rel(evidence_path),
        "result": rel(result_path),
    }


def update_entry(path: Path, entry: dict[str, object], task_reports: list[dict[str, object]]) -> None:
    statuses = [report["status"] for report in task_reports]
    static_status = "pass" if statuses and all(status == "pass" for status in statuses) else "fail"
    certification = entry.setdefault("certification", {})
    if isinstance(certification, dict):
        certification["static"] = static_status
    blockers = entry.get("release_blockers", [])
    if isinstance(blockers, list) and static_status == "pass":
        entry["release_blockers"] = [blocker for blocker in blockers if blocker != "static_validation"]
    path.write_text(json.dumps(entry, indent=2) + "\n", encoding="utf-8")


def build_report() -> dict[str, object]:
    task_reports: list[dict[str, object]] = []
    entry_reports: list[dict[str, object]] = []
    for path, entry in read_entries():
        per_entry: list[dict[str, object]] = []
        for task in entry.get("release_tasks", []):
            if isinstance(task, dict):
                per_entry.append(certify_task(entry, task))
        update_entry(path, entry, per_entry)
        task_reports.extend(per_entry)
        entry_reports.append(
            {
                "entry_id": entry["release_entry_id"],
                "release_task_count": len(per_entry),
                "static": "pass" if per_entry and all(report["status"] == "pass" for report in per_entry) else "fail",
                "missing_forms": entry.get("missing_forms", []),
                "evas": entry.get("certification", {}).get("evas", "pending"),
                "spectre": entry.get("certification", {}).get("spectre", "pending"),
                "certification_status": "not_certified",
            }
        )

    issue_count = sum(int(report["failure_count"]) for report in task_reports)
    return {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "status": "pass" if issue_count == 0 else "fail",
        "static_certified_release_task_count": sum(1 for report in task_reports if report["status"] == "pass"),
        "static_failed_release_task_count": sum(1 for report in task_reports if report["status"] == "fail"),
        "static_certified_entry_count": sum(1 for report in entry_reports if report["static"] == "pass"),
        "entry_count": len(entry_reports),
        "issue_count": issue_count,
        "task_reports": task_reports,
        "entry_reports": entry_reports,
        "notes": [
            "Static certification checks copied release gold assets against syntax guardrails from checks.yaml.",
            "Static pass does not imply EVAS or Spectre certification.",
            "Rows remain unscored until static, EVAS, and Spectre are all pass.",
        ],
    }


def write_markdown(report: dict[str, object]) -> None:
    failures = [task for task in report["task_reports"] if task["status"] != "pass"]
    lines = [
        "# vaBench Release Static Certification",
        "",
        f"Date: {report['date']}",
        "",
        "This report records static release certification for materialized",
        "release forms. It checks public syntax guardrails against copied gold",
        "assets and writes per-form evidence/result JSON files. It is not an",
        "EVAS or Spectre simulation report.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| status | `{report['status']}` |",
        f"| static-certified release forms | {report['static_certified_release_task_count']} |",
        f"| static-failed release forms | {report['static_failed_release_task_count']} |",
        f"| static-certified entries | {report['static_certified_entry_count']} |",
        f"| entries with materialized assets | {report['entry_count']} |",
        f"| blocking issues | {report['issue_count']} |",
        "",
        "## Failures",
        "",
        "| Entry | Form | Failures |",
        "| --- | --- | --- |",
    ]
    if failures:
        for task in failures:
            lines.append(f"| `{task['entry_id']}` | `{task['form']}` | {'; '.join(task['failures'])} |")
    else:
        lines.append("| none | none | none |")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    report = build_report()
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report)
    print(
        "static-certified {forms} release forms across {entries} entries; {issues} issues".format(
            forms=report["static_certified_release_task_count"],
            entries=report["static_certified_entry_count"],
            issues=report["issue_count"],
        )
    )
    if report["issue_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
