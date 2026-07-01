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
EXTENSION_SOP_AUDIT_JSON = REPORTS_ROOT / "extension_sop_audit.json"


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


def build_report() -> dict[str, Any]:
    tasks = read_tasks()
    sop_ready_extension_tasks = read_sop_ready_extension_tasks()
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
            "language_extension_notes": "benchmark-vabench-release-v3/LANGUAGE_EXTENSION.md",
            "core_behavior_evidence": "benchmark-vabench-release-v1/reports/benchmark_overview.json",
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
    print(f"wrote {REPORT_JSON.relative_to(ROOT)}")
    print(f"wrote {REPORT_CSV.relative_to(ROOT)}")
    print(f"wrote {REPORT_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
