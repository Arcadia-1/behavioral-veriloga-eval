#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v3"
REPORTS_ROOT = PACKAGE_ROOT / "reports"
TASKS_JSON = PACKAGE_ROOT / "TASKS.json"
CHECKS_YAML = PACKAGE_ROOT / "CHECKS.yaml"
REPORT_JSON = REPORTS_ROOT / "layered_certification.json"
REPORT_MD = REPORTS_ROOT / "layered_certification.md"
REPORT_CSV = REPORTS_ROOT / "layered_certification_tasks.csv"
STAGED_BLOCKER_JSON = REPORTS_ROOT / "staged_blocker_matrix.json"
STAGED_BLOCKER_MD = REPORTS_ROOT / "staged_blocker_matrix.md"
STAGED_BLOCKER_CSV = REPORTS_ROOT / "staged_blocker_matrix.csv"
EXTENSION_SOP_AUDIT_JSON = REPORTS_ROOT / "extension_sop_audit.json"
VERIFY_LAYERED_JSON = REPORTS_ROOT / "verify_301_494_layered.json"
STAGED_GOLD_PROBE_JSON = REPORTS_ROOT / "staged_promotion_gold_probe.json"


CORE_TIERS = {
    "<none>",
    "formal-candidate",
    "core-formal-candidate",
    "support-formal-candidate",
}

TIER_TO_LAYER = {
    "<none>": (
        "behavioral_event_core",
        "behavior_certified",
        "Inherited original full-300 behavior-certified surface.",
    ),
    "formal-candidate": (
        "behavioral_event_core",
        "behavior_certified",
        "Inherited original full-300 behavior-certified surface.",
    ),
    "core-formal-candidate": (
        "behavioral_event_core",
        "behavior_certified",
        "Inherited original full-300 behavior-certified surface.",
    ),
    "support-formal-candidate": (
        "behavioral_event_support",
        "behavior_certified_support",
        "Inherited original full-300 certified support surface; scoring follows the original denominator policy.",
    ),
    "syntax-extension-candidate": (
        "behavioral_language_extension",
        "compile_supported_candidate",
        "Reference solution compiles with current local EVAS, but behavior checker promotion is still pending.",
    ),
    "ams-mixed-signal-candidate": (
        "ams_mixed_signal_extension",
        "compile_supported_candidate",
        "Verilog-AMS/digital-mixed-signal syntax candidate; not part of the original full-300 behavior claim.",
    ),
    "noise-analysis-candidate": (
        "noise_analysis_extension",
        "compile_supported_candidate",
        "Noise/analysis helper syntax candidate; AC/noise behavior certification is pending.",
    ),
    "cadence-simulator-function-candidate": (
        "cadence_simulator_function_extension",
        "compile_supported_candidate",
        "Cadence simulator helper syntax candidate; behavior certification is pending.",
    ),
    "behavioral-continuous-time-candidate": (
        "behavioral_continuous_time_extension",
        "compile_supported_continuous_time_candidate",
        "Continuous-time operator syntax compiles; dynamic-solver accuracy is not certified.",
    ),
    "kcl-syntax-candidate": (
        "conservative_kcl_syntax_extension",
        "compile_supported_kcl_candidate",
        "KCL/current-contribution syntax compiles; MNA/KCL behavior is not certified.",
    ),
}


def read_tasks() -> dict[str, Any]:
    return json.loads(TASKS_JSON.read_text(encoding="utf-8"))["tasks"]


def read_sop_ready_extension_tasks() -> set[str]:
    if not EXTENSION_SOP_AUDIT_JSON.exists():
        return set()
    try:
        audit = json.loads(EXTENSION_SOP_AUDIT_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return set()
    ready: set[str] = set()
    for row in audit.get("tasks", []):
        if isinstance(row, dict) and row.get("sop_ready") is True:
            task_key = str(row.get("task") or "").strip()
            if task_key:
                ready.add(task_key)
    return ready


def read_sop_audit() -> dict[str, Any]:
    if not EXTENSION_SOP_AUDIT_JSON.exists():
        return {}
    try:
        return json.loads(EXTENSION_SOP_AUDIT_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def read_layered_verification_summary() -> dict[str, Any]:
    if not VERIFY_LAYERED_JSON.exists():
        return {}
    try:
        payload = json.loads(VERIFY_LAYERED_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    summary = payload.get("summary")
    return summary if isinstance(summary, dict) else {}


def read_staged_gold_probe() -> dict[str, Any]:
    if not STAGED_GOLD_PROBE_JSON.exists():
        return {}
    try:
        payload = json.loads(STAGED_GOLD_PROBE_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def read_checks_issue_urls() -> dict[str, list[str]]:
    if not CHECKS_YAML.exists():
        return {}
    issue_pattern = re.compile(r"https://github\.com/Arcadia-1/EVAS/issues/\d+")
    issue_urls: dict[str, list[str]] = {}
    current_key: str | None = None
    current_lines: list[str] = []
    for line in CHECKS_YAML.read_text(encoding="utf-8", errors="ignore").splitlines():
        if line and not line.startswith((" ", "\t")) and line.endswith(": |"):
            if current_key is not None:
                urls = sorted(set(issue_pattern.findall("\n".join(current_lines))))
                if urls:
                    issue_urls[current_key] = urls
            current_key = line.split(":", 1)[0]
            current_lines = []
            continue
        if current_key is not None:
            current_lines.append(line)
    if current_key is not None:
        urls = sorted(set(issue_pattern.findall("\n".join(current_lines))))
        if urls:
            issue_urls[current_key] = urls
    return issue_urls


def task_number(key: str) -> int:
    return int(key.split("-", 1)[0])


def classify_task(
    key: str,
    task: dict[str, Any],
    sop_ready_extension_tasks: set[str],
    checks_issue_urls: dict[str, list[str]],
) -> dict[str, Any]:
    tier = str(task.get("tier") or "<none>")
    if tier not in TIER_TO_LAYER:
        raise ValueError(f"unknown tier for {key}: {tier}")
    semantic_layer, certification_level, claim_boundary = TIER_TO_LAYER[tier]
    number = task_number(key)
    in_original_full_300 = number <= 300
    extension_candidate = number > 300
    sop_ready_extension = extension_candidate and key in sop_ready_extension_tasks
    if sop_ready_extension:
        certification_level = "behavior_certified_extension"
        claim_boundary = (
            "Extension task has SOP-ready behavior evidence: executable visible/hidden tests, "
            "repository behavior checker, and five rejected negative variants. It remains outside "
            "the original full-300 denominator."
        )
    return {
        "task_key": key,
        "task_number": number,
        "task_id": task.get("id", ""),
        "title": task.get("title", ""),
        "form": task.get("form", ""),
        "category": task.get("category", ""),
        "tier": tier,
        "semantic_layer": semantic_layer,
        "certification_level": certification_level,
        "in_original_full_300": in_original_full_300,
        "extension_candidate": extension_candidate,
        "behavior_certified": certification_level.startswith("behavior_certified"),
        "score_claim": (
            "original_full_300_policy"
            if in_original_full_300
            else "extension_behavior_certified_outside_original_300"
            if sop_ready_extension
            else "excluded_until_behavior_promotion"
        ),
        "claim_boundary": claim_boundary,
        "blocking_issue_urls": ";".join(checks_issue_urls.get(key, [])),
        "target": ";".join(task.get("target", [])),
        "syntax_focus": task.get("syntax_focus", ""),
        "certification_scope": task.get("certification_scope", "original_full_300_claim"),
    }


def counter(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    return dict(sorted(Counter(str(row[key]) for row in rows).items()))


def promotion_command_for(blocked_rows: list[dict[str, Any]]) -> str:
    numbers = sorted(int(row["task_number"]) for row in blocked_rows)
    if not numbers:
        return ""
    task_filter = ",".join(f"{number:03d}" for number in numbers)
    return (
        "PYTHONPATH=runners VAEVAS_DEFAULT_EVAS_ENGINE=python "
        "VAEVAS_EVAS_PERSISTENT_WORKER=0 PATH=\"$PWD/.venv-evas/bin:$PATH\" "
        ".venv-evas/bin/python scripts/run_v3_gold_negative_verification.py "
        f"--start {numbers[0]} --end {numbers[-1]} --tasks {task_filter} "
        "--include-staged --timeout 120 --jobs 1 "
        f"--out benchmark-vabench-release-v3/reports/verify_issue_{numbers[0]}_{numbers[-1]}.json"
    )


def promotion_acceptance_for(blocked_rows: list[dict[str, Any]]) -> str:
    task_count = len(blocked_rows)
    negative_count = task_count * 5
    return (
        f"After EVAS support lands, promote the listed {task_count} task(s) by adding sim_correct "
        "behavior contracts/checkers if missing, then require "
        f"{task_count}/{task_count} gold PASS, {negative_count}/{negative_count} negative variants rejected, "
        "and zero expectation_fail in the verification report."
    )


def build_completion_audit(
    summary: dict[str, Any],
    sop_audit: dict[str, Any],
    verification_summary: dict[str, Any],
    blocking_issues: list[dict[str, Any]],
) -> dict[str, Any]:
    sop_summary = sop_audit.get("summary", {}) if isinstance(sop_audit, dict) else {}
    issue_counts = sop_summary.get("issue_counts", {}) if isinstance(sop_summary, dict) else {}
    staged_count = summary["compile_supported_candidate_count"]
    requirements = [
        {
            "requirement": "Scope covers all v3 extension tasks 301-494.",
            "status": "satisfied" if summary["extension_candidate_count"] == 194 else "not_satisfied",
            "evidence": f"layered_certification summary reports extension_candidate_count={summary['extension_candidate_count']}.",
        },
        {
            "requirement": "Each extension task has a clear prompt and required behavior section.",
            "status": "satisfied" if issue_counts.get("missing_required_behavior_section", 0) == 0 else "not_satisfied",
            "evidence": "extension_sop_audit has no missing_required_behavior_section issue.",
        },
        {
            "requirement": "Each extension task has executable visible and hidden test evidence.",
            "status": "satisfied" if sop_summary.get("complete_tests_count") == 194 else "not_satisfied",
            "evidence": f"extension_sop_audit complete_tests_count={sop_summary.get('complete_tests_count')}.",
        },
        {
            "requirement": "Each extension task has five useful negative variants.",
            "status": "satisfied" if not any(str(key).startswith("negative_count_lt5") for key in issue_counts) else "not_satisfied",
            "evidence": "extension_sop_audit reports no negative_count_lt5 issues.",
        },
        {
            "requirement": "Each extension task has repository behavior checker evidence and can be scored fairly.",
            "status": "partial",
            "evidence": (
                f"{summary['behavior_certified_extension_count']} extension tasks are behavior-certified; "
                f"{staged_count} remain excluded_until_behavior_promotion."
            ),
            "gap": (
                "The remaining staged rows are blocked by EVAS support issues or missing "
                "behavior-checker evidence; staged_promotion_gold_probe records the current "
                "per-task blocker."
            ),
        },
        {
            "requirement": "Behavior-certified extension tasks pass gold verification and reject all negative variants.",
            "status": "satisfied" if (
                verification_summary.get("gold_pass") == summary["behavior_certified_extension_count"]
                and verification_summary.get("gold_fail") == 0
                and verification_summary.get("negative_accepted") == 0
                and verification_summary.get("expectation_fail") == 0
            ) else "not_satisfied",
            "evidence": (
                f"verify_301_494_layered: gold_pass={verification_summary.get('gold_pass')}, "
                f"gold_fail={verification_summary.get('gold_fail')}, "
                f"negative_rejected={verification_summary.get('negative_rejected')}, "
                f"negative_accepted={verification_summary.get('negative_accepted')}, "
                f"expectation_fail={verification_summary.get('expectation_fail')}."
            ),
        },
        {
            "requirement": "Every staged task has a concrete EVAS issue and promotion checklist.",
            "status": "satisfied" if (
                sum(issue["task_count"] for issue in blocking_issues) == summary["compile_supported_candidate_count"]
                and all(issue.get("promotion_command") and issue.get("promotion_acceptance") for issue in blocking_issues)
            ) else "not_satisfied",
            "evidence": (
                f"{len(blocking_issues)} blocking issues cover "
                f"{sum(issue['task_count'] for issue in blocking_issues)} staged tasks; "
                "staged_promotion_gold_probe records "
                f"{staged_count}/{staged_count} staged gold cases still failing the current promotion gate."
            ),
        },
    ]
    return {
        "status": "partial_external_blocked",
        "is_complete": False,
        "reason": (
            f"The full 301-494 objective is not complete because {staged_count} extension tasks still lack "
            "behavior checker evidence and are excluded until EVAS support issues are resolved."
        ),
        "requirements": requirements,
    }


def build_report() -> dict[str, Any]:
    tasks = read_tasks()
    sop_audit = read_sop_audit()
    sop_ready_extension_tasks = read_sop_ready_extension_tasks()
    verification_summary = read_layered_verification_summary()
    checks_issue_urls = read_checks_issue_urls()
    rows = [
        classify_task(key, tasks[key], sop_ready_extension_tasks, checks_issue_urls)
        for key in sorted(tasks, key=task_number)
    ]
    extension_rows = [row for row in rows if row["extension_candidate"]]
    behavior_rows = [row for row in rows if row["behavior_certified"]]
    compile_rows = [
        row for row in rows
        if str(row["certification_level"]).startswith("compile_supported")
    ]
    summary = {
        "task_count": len(rows),
        "original_full_300_count": sum(row["in_original_full_300"] for row in rows),
        "extension_candidate_count": len(extension_rows),
        "behavior_certified_count": len(behavior_rows),
        "behavior_certified_extension_count": sum(
            row["extension_candidate"] and row["behavior_certified"] for row in rows
        ),
        "compile_supported_candidate_count": len(compile_rows),
        "unsupported_candidate_count": sum(row["tier"] == "evas-unsupported-candidate" for row in rows),
        "tier_counts": counter(rows, "tier"),
        "semantic_layer_counts": counter(rows, "semantic_layer"),
        "certification_level_counts": counter(rows, "certification_level"),
        "score_claim_counts": counter(rows, "score_claim"),
        "blocking_issue_counts": dict(sorted(Counter(
            issue_url
            for row in rows
            if row["score_claim"] == "excluded_until_behavior_promotion"
            for issue_url in str(row["blocking_issue_urls"]).split(";")
            if issue_url
        ).items())),
    }
    blocking_issues = []
    for issue_url, count in summary["blocking_issue_counts"].items():
        blocked_rows = [
            row for row in rows
            if issue_url in str(row["blocking_issue_urls"]).split(";")
            and row["score_claim"] == "excluded_until_behavior_promotion"
        ]
        blocking_issues.append({
            "issue_url": issue_url,
            "task_count": count,
            "semantic_layers": counter(blocked_rows, "semantic_layer"),
            "promotion_command": promotion_command_for(blocked_rows),
            "promotion_acceptance": promotion_acceptance_for(blocked_rows),
            "tasks": [
                {
                    "task_key": row["task_key"],
                    "task_id": row["task_id"],
                    "title": row["title"],
                    "tier": row["tier"],
                    "semantic_layer": row["semantic_layer"],
                    "target": row["target"],
                }
                for row in blocked_rows
            ],
        })
    return {
        "date": date.today().isoformat(),
        "release": "benchmark-vabench-release-v3",
        "status": "layered_partial",
        "summary": summary,
        "layers": [
            {
                "semantic_layer": layer,
                "task_count": count,
                "certification_levels": counter(
                    [row for row in rows if row["semantic_layer"] == layer],
                    "certification_level",
                ),
            }
            for layer, count in summary["semantic_layer_counts"].items()
        ],
        "blocking_issues": blocking_issues,
        "completion_audit": build_completion_audit(
            summary,
            sop_audit,
            verification_summary,
            blocking_issues,
        ),
        "claim_boundary": [
            "Only tasks 001-300 are part of the original behavior-certified full-300 claim.",
            "Tasks 301-494 are extension candidates; they are excluded from score until promoted with behavior checkers and negative-case scoring.",
            "Compile-supported continuous-time rows do not certify continuous-time numeric accuracy.",
            "Compile-supported KCL rows do not certify MNA/KCL solving behavior.",
            "AMS, noise/analysis, Cadence-helper, and table-model extension rows require layer-specific behavior evidence before paper-facing promotion.",
        ],
        "evidence_sources": {
            "task_manifest": "benchmark-vabench-release-v3/TASKS.json",
            "checker_manifest": "benchmark-vabench-release-v3/CHECKS.yaml",
            "extension_sop_audit": "benchmark-vabench-release-v3/reports/extension_sop_audit.json",
            "behavior_certified_extension_task_evidence": "benchmark-vabench-release-v3/reports/behavior_certified_extension_task_evidence.json",
            "language_extension_notes": "benchmark-vabench-release-v3/LANGUAGE_EXTENSION.md",
            "core_behavior_evidence": "benchmark-vabench-release-v1/reports/benchmark_overview.json",
            "staged_gold_probe": "benchmark-vabench-release-v3/reports/staged_promotion_gold_probe.json",
            "staged_gold_probe_summary": "benchmark-vabench-release-v3/reports/staged_promotion_gold_probe.md",
            "staged_blocker_matrix": "benchmark-vabench-release-v3/reports/staged_blocker_matrix.json",
            "staged_blocker_matrix_summary": "benchmark-vabench-release-v3/reports/staged_blocker_matrix.md",
            "latest_compile_probe": "local evas-rust compile probe for tasks 460-494 solution plus five negative variants per task: 210 files, 0 failures",
        },
        "task_rows": rows,
    }


def write_csv(rows: list[dict[str, Any]]) -> None:
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    fields = [
        "task_key",
        "task_number",
        "task_id",
        "title",
        "tier",
        "semantic_layer",
        "certification_level",
        "behavior_certified",
        "score_claim",
        "claim_boundary",
        "blocking_issue_urls",
        "target",
    ]
    with REPORT_CSV.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def build_staged_blocker_matrix(report: dict[str, Any]) -> dict[str, Any]:
    probe = read_staged_gold_probe()
    probe_rows = {
        str(row.get("task_slug")): row
        for row in probe.get("rows", [])
        if isinstance(row, dict) and row.get("task_slug")
    }
    issue_commands = {
        issue["issue_url"]: {
            "promotion_command": issue.get("promotion_command", ""),
            "promotion_acceptance": issue.get("promotion_acceptance", ""),
        }
        for issue in report["blocking_issues"]
    }
    rows: list[dict[str, Any]] = []
    for task in report["task_rows"]:
        if task["score_claim"] != "excluded_until_behavior_promotion":
            continue
        issue_urls = [
            issue_url
            for issue_url in str(task.get("blocking_issue_urls", "")).split(";")
            if issue_url
        ]
        probe_row = probe_rows.get(task["task_key"], {})
        rows.append({
            "task_key": task["task_key"],
            "task_id": task["task_id"],
            "title": task["title"],
            "tier": task["tier"],
            "semantic_layer": task["semantic_layer"],
            "target": task["target"],
            "issue_urls": issue_urls,
            "probe_status": probe_row.get("status", ""),
            "failure_summary": probe_row.get("failure_summary", ""),
            "promotion_commands": [
                issue_commands.get(issue_url, {}).get("promotion_command", "")
                for issue_url in issue_urls
            ],
            "promotion_acceptance": [
                issue_commands.get(issue_url, {}).get("promotion_acceptance", "")
                for issue_url in issue_urls
            ],
        })
    missing_issue = [row["task_key"] for row in rows if not row["issue_urls"]]
    missing_probe = [row["task_key"] for row in rows if not row["failure_summary"]]
    return {
        "date": report["date"],
        "release": report["release"],
        "summary": {
            "staged_task_count": len(rows),
            "missing_issue_count": len(missing_issue),
            "missing_failure_summary_count": len(missing_probe),
            "issue_count": len({issue_url for row in rows for issue_url in row["issue_urls"]}),
            "semantic_layer_counts": dict(sorted(Counter(row["semantic_layer"] for row in rows).items())),
        },
        "missing_issue_tasks": missing_issue,
        "missing_failure_summary_tasks": missing_probe,
        "tasks": rows,
    }


def write_staged_blocker_csv(matrix: dict[str, Any]) -> None:
    fields = [
        "task_key",
        "task_id",
        "title",
        "tier",
        "semantic_layer",
        "target",
        "issue_urls",
        "probe_status",
        "failure_summary",
    ]
    with STAGED_BLOCKER_CSV.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for row in matrix["tasks"]:
            writer.writerow({
                "task_key": row["task_key"],
                "task_id": row["task_id"],
                "title": row["title"],
                "tier": row["tier"],
                "semantic_layer": row["semantic_layer"],
                "target": row["target"],
                "issue_urls": ";".join(row["issue_urls"]),
                "probe_status": row["probe_status"],
                "failure_summary": row["failure_summary"],
            })


def write_staged_blocker_md(matrix: dict[str, Any]) -> None:
    summary = matrix["summary"]
    lines = [
        "# v3 Staged Blocker Matrix",
        "",
        f"Date: {matrix['date']}",
        "",
        "## Summary",
        "",
        f"- Staged tasks: **{summary['staged_task_count']}**",
        f"- Distinct blocking issues: **{summary['issue_count']}**",
        f"- Missing issue links: **{summary['missing_issue_count']}**",
        f"- Missing failure summaries: **{summary['missing_failure_summary_count']}**",
        "",
        "## Tasks",
        "",
        "| Task | Layer | Issue | Probe status | Failure summary |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in matrix["tasks"]:
        issues = "<br>".join(row["issue_urls"])
        summary_text = str(row["failure_summary"]).replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| `{row['task_key']}` | `{row['semantic_layer']}` | {issues} | "
            f"`{row['probe_status']}` | {summary_text} |"
        )
    lines.append("")
    STAGED_BLOCKER_MD.write_text("\n".join(lines), encoding="utf-8")


def write_staged_blocker_matrix(report: dict[str, Any]) -> None:
    matrix = build_staged_blocker_matrix(report)
    STAGED_BLOCKER_JSON.write_text(json.dumps(matrix, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_staged_blocker_csv(matrix)
    write_staged_blocker_md(matrix)


def write_md(report: dict[str, Any]) -> None:
    summary = report["summary"]
    lines = [
        "# vaBench v3 Layered Certification",
        "",
        f"Date: {report['date']}",
        "",
        "## Headline",
        "",
        f"- Total tasks: **{summary['task_count']}**",
        f"- Original behavior-certified full-300 surface: **{summary['original_full_300_count']}**",
        f"- Extension candidates: **{summary['extension_candidate_count']}**",
        f"- Behavior-certified extension rows: **{summary['behavior_certified_extension_count']}**",
        f"- Compile-supported candidate rows: **{summary['compile_supported_candidate_count']}**",
        f"- Unsupported candidate rows: **{summary['unsupported_candidate_count']}**",
        "",
        "## Semantic Layers",
        "",
        "| Layer | Tasks | Certification levels |",
        "| --- | ---: | --- |",
    ]
    for layer in report["layers"]:
        levels = ", ".join(
            f"{name}: {count}"
            for name, count in layer["certification_levels"].items()
        )
        lines.append(f"| `{layer['semantic_layer']}` | {layer['task_count']} | {levels} |")
    lines.extend([
        "",
        "## Blocking Issues",
        "",
        "| EVAS issue | Blocked tasks | Semantic layers | Promotion acceptance |",
        "| --- | ---: | --- | --- |",
    ])
    for issue in report["blocking_issues"]:
        layers = ", ".join(
            f"{name}: {count}"
            for name, count in issue["semantic_layers"].items()
        )
        lines.append(
            f"| {issue['issue_url']} | {issue['task_count']} | {layers} | "
            f"{issue['promotion_acceptance']} |"
        )
    lines.extend([
        "",
        "## Completion Audit",
        "",
        f"- Status: `{report['completion_audit']['status']}`",
        f"- Complete: `{str(report['completion_audit']['is_complete']).lower()}`",
        f"- Reason: {report['completion_audit']['reason']}",
        "",
        "| Requirement | Status | Evidence | Gap |",
        "| --- | --- | --- | --- |",
    ])
    for item in report["completion_audit"]["requirements"]:
        lines.append(
            f"| {item['requirement']} | `{item['status']}` | {item.get('evidence', '')} | {item.get('gap', '')} |"
        )
    lines.extend([
        "",
        "## Claim Boundary",
        "",
    ])
    lines.extend(f"- {item}" for item in report["claim_boundary"])
    lines.extend([
        "",
        "## Evidence Sources",
        "",
        "| Evidence | Path / note |",
        "| --- | --- |",
    ])
    for key, value in report["evidence_sources"].items():
        lines.append(f"| `{key}` | `{value}` |")
    lines.append("")
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    report = build_report()
    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_csv(report["task_rows"])
    write_md(report)
    write_staged_blocker_matrix(report)
    print(f"wrote {REPORT_JSON.relative_to(ROOT)}")
    print(f"wrote {REPORT_CSV.relative_to(ROOT)}")
    print(f"wrote {REPORT_MD.relative_to(ROOT)}")
    print(f"wrote {STAGED_BLOCKER_JSON.relative_to(ROOT)}")
    print(f"wrote {STAGED_BLOCKER_CSV.relative_to(ROOT)}")
    print(f"wrote {STAGED_BLOCKER_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
