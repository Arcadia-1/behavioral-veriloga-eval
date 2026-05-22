#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

from vabench_policy import (
    CONTENT_DENOMINATOR_EXCLUDED_ENTRIES,
    content_denominator_exclusion_reasons,
    is_content_denominator_entry,
)


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
MANIFEST = PACKAGE_ROOT / "MANIFEST.json"
REPORT_JSON = PACKAGE_ROOT / "reports" / "content_contract_audit.json"
REPORT_MD = PACKAGE_ROOT / "reports" / "content_contract_audit.md"

EXPECTED_CATEGORIES = {
    "Data Converters",
    "Comparators and Decision Circuits",
    "PLL / Clock / Event Timing",
    "Calibration, DEM, and Control",
    "Digital and Event-Driven Logic",
    "Measurement and Testbench Instrumentation",
    "Stimulus and Sources",
    "Analog Behavioral Signal Conditioning",
    "Sample, Hold, and Analog Memory",
}

GENERIC_CHECKS = {
    "behavioral_module_present",
    "companion_testbench_available",
    "voltage_domain_outputs",
}
AUXILIARY_COMPANION_CHECK = "auxiliary_companion_not_counted_as_strong_claim"

HIGH_RISK_ENTRIES: dict[str, str] = {}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def strip_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    text = re.sub(r"//.*", "", text)
    return text


def normalize_veriloga(text: str) -> str:
    text = strip_comments(text)
    text = re.sub(r"\bmodule\s+[A-Za-z_][A-Za-z0-9_]*", "module MODULE", text)
    text = re.sub(r"\bendmodule\b", "endmodule", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_modules(text: str) -> list[str]:
    return re.findall(r"\bmodule\s+([A-Za-z_][A-Za-z0-9_]*)", text)


def extract_sim_checks(checks_text: str) -> list[str]:
    checks: list[str] = []
    in_sim = False
    for line in checks_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("sim_correct:"):
            in_sim = True
            continue
        if in_sim and stripped == "checks:":
            continue
        if in_sim and stripped and re.match(r"^[A-Za-z_][A-Za-z0-9_-]*:", stripped):
            break
        if in_sim and stripped.startswith("-"):
            checks.append(stripped.lstrip("- ").strip().strip('"').strip("'"))
    return checks


def code_excerpt(path: Path, max_lines: int = 80) -> dict[str, object]:
    lines = read_text(path).splitlines()
    end = min(len(lines), max_lines)
    numbered = [f"{idx + 1:4d}: {line}" for idx, line in enumerate(lines[:end])]
    return {
        "path": rel(path),
        "start_line": 1,
        "end_line": end,
        "text": "\n".join(numbered),
    }


def task_paths(task: dict[str, object]) -> dict[str, object]:
    gold = [ROOT / str(item) for item in task.get("gold", [])]
    return {
        "prompt": ROOT / str(task.get("prompt", "")),
        "checks": ROOT / str(task.get("checks", "")),
        "gold": gold,
        "gold_va": [path for path in gold if path.suffix == ".va"],
        "gold_scs": [path for path in gold if path.suffix == ".scs"],
    }


def primary_task(entry: dict[str, object], form: str = "e2e") -> dict[str, object] | None:
    for task in entry.get("release_tasks", []):
        if isinstance(task, dict) and task.get("form") == form:
            return task
    tasks = entry.get("release_tasks", [])
    if tasks and isinstance(tasks[0], dict):
        return tasks[0]
    return None


def build_entry_source_signature(entry: dict[str, object]) -> dict[str, object] | None:
    task = primary_task(entry, "e2e")
    if not task:
        return None
    paths = task_paths(task)
    gold_va = paths["gold_va"]
    if not gold_va:
        return None
    combined = "\n".join(normalize_veriloga(read_text(path)) for path in gold_va)
    modules: list[str] = []
    excerpts = []
    for path in gold_va:
        text = read_text(path)
        modules.extend(extract_modules(text))
        excerpts.append(code_excerpt(path, max_lines=70))
    return {
        "entry_id": entry["release_entry_id"],
        "level": entry["level"],
        "category": entry["category"],
        "base_function": entry["base_function"],
        "form": task["form"],
        "gold_va": [rel(path) for path in gold_va],
        "modules": modules,
        "hash": hashlib.sha256(combined.encode("utf-8")).hexdigest(),
        "normalized_source_len": len(combined),
        "excerpts": excerpts,
    }


def audit_counts(manifest: dict[str, object]) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    entries = manifest["entries"]
    content_entries = [entry for entry in entries if is_content_denominator_entry(str(entry["release_entry_id"]))]
    categories = Counter(entry["category"] for entry in content_entries)
    levels = Counter(entry["level"] for entry in content_entries)
    excluded_levels = Counter(
        entry["level"] for entry in entries if not is_content_denominator_entry(str(entry["release_entry_id"]))
    )
    expected_content_entries = 75 - len(CONTENT_DENOMINATOR_EXCLUDED_ENTRIES)
    expected_levels = {"L1": 60 - excluded_levels.get("L1", 0), "L2": 15 - excluded_levels.get("L2", 0)}

    if len(entries) != 75:
        findings.append(blocker("package_entry_count_drift", f"manifest has {len(entries)} entries, expected 75 clean package assets"))
    if len(content_entries) != expected_content_entries:
        findings.append(
            blocker(
                "content_denominator_count_drift",
                f"content denominator has {len(content_entries)} entries, expected {expected_content_entries} after policy exclusions",
            )
        )
    if levels != expected_levels:
        findings.append(
            blocker(
                "content_level_count_drift",
                f"content denominator level counts are {dict(levels)}, expected {expected_levels}",
            )
        )
    extra = set(categories) - EXPECTED_CATEGORIES
    missing = EXPECTED_CATEGORIES - set(categories)
    if extra or missing:
        findings.append(blocker("category_set_drift", f"extra={sorted(extra)} missing={sorted(missing)}"))

    for category in sorted(EXPECTED_CATEGORIES):
        cat_entries = [entry for entry in content_entries if entry["category"] == category]
        if not any(entry["level"] == "L1" for entry in cat_entries):
            findings.append(blocker("category_missing_l1", f"{category} has no L1 entry"))
        if not any(entry["level"] == "L2" for entry in cat_entries):
            findings.append(review("category_missing_l2", f"{category} has no L2 entry"))

    if any(entry.get("counted_in_score") for entry in entries):
        findings.append(blocker("score_enabled_during_content_audit", "at least one entry is counted in score"))
    return findings


def blocker(kind: str, message: str, **extra: object) -> dict[str, object]:
    return {"severity": "BLOCKER", "kind": kind, "message": message, **extra}


def review(kind: str, message: str, **extra: object) -> dict[str, object]:
    return {"severity": "REVIEW_REQUIRED", "kind": kind, "message": message, **extra}


def info(kind: str, message: str, **extra: object) -> dict[str, object]:
    return {"severity": "INFO", "kind": kind, "message": message, **extra}


def audit_duplicate_l2(entries: list[dict[str, object]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    signatures = [sig for entry in entries if (sig := build_entry_source_signature(entry))]
    by_hash: dict[str, list[dict[str, object]]] = defaultdict(list)
    for sig in signatures:
        if sig["level"] == "L2":
            by_hash[str(sig["hash"])].append(sig)

    findings: list[dict[str, object]] = []
    duplicate_groups: list[dict[str, object]] = []
    for group in by_hash.values():
        if len(group) < 2:
            continue
        included = [item for item in group if is_content_denominator_entry(str(item["entry_id"]))]
        keep = included[0] if included else group[0]
        remove = [item for item in group if item["entry_id"] != keep["entry_id"]]
        duplicate_groups.append(
            {
                "keep_candidate": keep["entry_id"],
                "remove_or_rewrite_candidates": [item["entry_id"] for item in remove],
                "content_denominator_keep_candidates": [item["entry_id"] for item in included],
                "reason": "L2 e2e gold Verilog-A normalizes to identical source except module names/comments.",
                "entries": group,
            }
        )
        findings.append(
            blocker(
                "duplicate_l2_gold_kernel",
                "duplicate L2 e2e gold kernel detected in the clean release; remove or rewrite duplicate entries before claiming distinct functions",
                keep_candidate=keep["entry_id"],
                remove_or_rewrite_candidates=[item["entry_id"] for item in remove],
                content_denominator_keep_candidates=[item["entry_id"] for item in included],
                code_excerpts=[item["excerpts"][0] for item in group if item["excerpts"]],
            )
        )
    return findings, duplicate_groups


def audit_task_contracts(entries: list[dict[str, object]]) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []
    for entry in entries:
        entry_id = str(entry["release_entry_id"])
        if not is_content_denominator_entry(entry_id):
            findings.append(
                info(
                    "content_denominator_excluded_entry",
                    "entry remains in the package as traceable material but is excluded from strong content claims",
                    entry_id=entry_id,
                    base_function=entry["base_function"],
                    reasons=content_denominator_exclusion_reasons(entry_id),
                )
            )
            continue
        if entry_id in HIGH_RISK_ENTRIES:
            task = primary_task(entry, "dut") or primary_task(entry, "e2e")
            excerpts = []
            sim_checks: list[str] = []
            if task:
                paths = task_paths(task)
                if paths["gold_va"]:
                    excerpts = [code_excerpt(path, max_lines=70) for path in paths["gold_va"][:2]]
                checks_path = paths["checks"]
                if checks_path.exists():
                    sim_checks = extract_sim_checks(read_text(checks_path))
            findings.append(
                review(
                    "high_risk_entry_manual_review",
                    HIGH_RISK_ENTRIES[entry_id],
                    entry_id=entry_id,
                    category=entry["category"],
                    base_function=entry["base_function"],
                    sim_checks=sim_checks,
                    code_excerpts=excerpts,
                )
            )

        for task in entry.get("release_tasks", []):
            if not isinstance(task, dict):
                continue
            paths = task_paths(task)
            checks_path = paths["checks"]
            prompt_path = paths["prompt"]
            sim_checks = extract_sim_checks(read_text(checks_path)) if checks_path.exists() else []
            generic = [item for item in sim_checks if item in GENERIC_CHECKS]
            auxiliary_companion = AUXILIARY_COMPANION_CHECK in sim_checks
            if auxiliary_companion and sim_checks and set(sim_checks).issubset(GENERIC_CHECKS | {AUXILIARY_COMPANION_CHECK}):
                findings.append(
                    info(
                        "auxiliary_companion_checker",
                        "DUT companion is explicitly outside the strong function-level benchmark claim until a real behavior checker is added",
                        entry_id=entry_id,
                        form=task.get("form"),
                        checks=sim_checks,
                        checks_path=rel(checks_path),
                        code_excerpts=[code_excerpt(path, max_lines=50) for path in paths["gold_va"][:1]],
                    )
                )
            elif sim_checks and set(sim_checks).issubset(GENERIC_CHECKS):
                findings.append(
                    review(
                        "shallow_generic_checker",
                        "sim_correct only checks generic companion/module presence rather than circuit behavior",
                        entry_id=entry_id,
                        form=task.get("form"),
                        checks=sim_checks,
                        checks_path=rel(checks_path),
                        code_excerpts=[code_excerpt(path, max_lines=50) for path in paths["gold_va"][:1]],
                    )
                )
            elif len(generic) >= 2:
                findings.append(
                    review(
                        "checker_contains_generic_guardrails",
                        "sim_correct contains multiple generic checks; confirm function-level checks also exist",
                        entry_id=entry_id,
                        form=task.get("form"),
                        checks=sim_checks,
                        checks_path=rel(checks_path),
                    )
                )

            if prompt_path.exists():
                prompt = read_text(prompt_path).lower()
                base_function = str(entry["base_function"]).lower()
                if "binary-weighted voltage dac" in base_function and "thermometer_dac" in prompt:
                    findings.append(
                        review(
                            "historical_name_in_public_prompt",
                            "binary DAC public prompt still contains historical thermometer_dac naming",
                            entry_id=entry_id,
                            form=task.get("form"),
                            prompt_path=rel(prompt_path),
                        )
                    )
    return findings


def summarize_l2(entries: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for entry in entries:
        if entry["level"] != "L2":
            continue
        task = primary_task(entry, "e2e")
        if not task:
            continue
        paths = task_paths(task)
        checks = extract_sim_checks(read_text(paths["checks"])) if paths["checks"].exists() else []
        modules: list[str] = []
        for path in paths["gold_va"]:
            modules.extend(extract_modules(read_text(path)))
        rows.append(
            {
                "entry_id": entry["release_entry_id"],
                "content_denominator_included": is_content_denominator_entry(str(entry["release_entry_id"])),
                "content_exclusion_reasons": content_denominator_exclusion_reasons(str(entry["release_entry_id"])),
                "category": entry["category"],
                "base_function": entry["base_function"],
                "gold_va_modules": modules,
                "sim_checks": checks,
                "gold_va": [rel(path) for path in paths["gold_va"]],
                "checks_path": rel(paths["checks"]),
                "prompt_path": rel(paths["prompt"]),
            }
        )
    return rows


def build_report() -> dict[str, object]:
    manifest = read_json(MANIFEST)
    entries = manifest["entries"]
    content_entries = [entry for entry in entries if is_content_denominator_entry(str(entry["release_entry_id"]))]
    content_forms = [form for form in manifest["forms"] if is_content_denominator_entry(str(form["release_entry_id"]))]
    entry_payloads = [
        read_json(ROOT / str(entry["release_entry_manifest"]))
        for entry in entries
        if (ROOT / str(entry["release_entry_manifest"])).exists()
    ]

    findings: list[dict[str, object]] = []
    findings.extend(audit_counts(manifest))
    duplicate_findings, duplicate_groups = audit_duplicate_l2(entry_payloads)
    findings.extend(duplicate_findings)
    findings.extend(audit_task_contracts(entry_payloads))

    severity_counts = Counter(finding["severity"] for finding in findings)
    status = "fail" if severity_counts["BLOCKER"] else "review_required" if severity_counts["REVIEW_REQUIRED"] else "pass"

    return {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "status": status,
        "entry_count": len(entries),
        "form_count": len(manifest["forms"]),
        "content_denominator_entry_count": len(content_entries),
        "content_denominator_form_count": len(content_forms),
        "content_excluded_entry_count": len(entries) - len(content_entries),
        "content_excluded_entries": {
            entry_id: reasons for entry_id, reasons in sorted(CONTENT_DENOMINATOR_EXCLUDED_ENTRIES.items())
        },
        "severity_counts": dict(sorted(severity_counts.items())),
        "duplicate_groups": duplicate_groups,
        "l2_review_table": summarize_l2(entry_payloads),
        "findings": findings,
        "recommended_policy": [
            "Do not retain exact duplicate L2 kernels in the clean release package; rewrite them before re-admission.",
            "Keep score disabled; allow only unweighted pass-rate reporting after content review.",
            "For shallow companion checkers, either add function-level behavior checks or mark the companion as auxiliary outside the strong benchmark claim.",
            "Treat REVIEW_REQUIRED findings as human semantic review queue, not simulator failures.",
        ],
    }


def finding_table(findings: list[dict[str, object]]) -> list[str]:
    lines = ["| Severity | Kind | Entry | Form | Message |", "| --- | --- | --- | --- | --- |"]
    if not findings:
        lines.append("| none | none | none | none | none |")
        return lines
    for item in findings:
        lines.append(
            "| {severity} | `{kind}` | `{entry}` | `{form}` | {message} |".format(
                severity=item["severity"],
                kind=item["kind"],
                entry=item.get("entry_id", item.get("keep_candidate", "-")),
                form=item.get("form", "-"),
                message=str(item["message"]).replace("|", "\\|"),
            )
        )
    return lines


def write_markdown(report: dict[str, object]) -> None:
    lines = [
        "# vaBench Content Contract Audit",
        "",
        f"Date: {report['date']}",
        "",
        "This report audits benchmark content semantics before model baselines or",
        "paper-facing benchmark claims. EVAS/Spectre certification proves simulator",
        "agreement, but this report asks whether the public task, checker, and gold",
        "source describe the same circuit function.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| status | `{report['status']}` |",
        f"| release entries | {report['entry_count']} |",
        f"| release forms | {report['form_count']} |",
        f"| content denominator entries | {report['content_denominator_entry_count']} |",
        f"| content denominator forms | {report['content_denominator_form_count']} |",
        f"| content-excluded entries | {report['content_excluded_entry_count']} |",
    ]
    for severity, count in dict(report["severity_counts"]).items():
        lines.append(f"| {severity} findings | {count} |")

    lines.extend(["", "## Findings", ""])
    lines.extend(finding_table(report["findings"]))

    lines.extend(
        [
            "",
            "## Duplicate L2 Kernel Groups",
            "",
            "| Keep candidate | Remove or rewrite candidates | Reason |",
            "| --- | --- | --- |",
        ]
    )
    if report["duplicate_groups"]:
        for group in report["duplicate_groups"]:
            lines.append(
                f"| `{group['keep_candidate']}` | `{', '.join(group['remove_or_rewrite_candidates'])}` | {group['reason']} |"
            )
    else:
        lines.append("| none | none | none |")

    lines.extend(
        [
            "",
            "## L2 Review Table",
            "",
            "| Entry | Content denominator | Category | Function | Gold modules | sim_correct checks |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in report["l2_review_table"]:
        lines.append(
            "| `{entry}` | `{included}` | {category} | {function} | `{modules}` | {checks} |".format(
                entry=row["entry_id"],
                included=row["content_denominator_included"],
                category=row["category"],
                function=row["base_function"],
                modules=", ".join(row["gold_va_modules"]) or "-",
                checks="<br>".join(row["sim_checks"]) or "-",
            )
        )

    lines.extend(["", "## Code Excerpts for Manual Judgment", ""])
    excerpt_count = 0
    for finding in report["findings"]:
        for excerpt in finding.get("code_excerpts", [])[:2]:
            excerpt_count += 1
            lines.extend(
                [
                    f"### {finding['kind']} / {finding.get('entry_id', finding.get('keep_candidate', 'duplicate'))}",
                    "",
                    f"`{excerpt['path']}:{excerpt['start_line']}`",
                    "",
                    "```verilog",
                    excerpt["text"],
                    "```",
                    "",
                ]
            )
    if excerpt_count == 0:
        lines.append("No excerpts were needed.")

    lines.extend(
        [
            "## Recommended Policy",
            "",
        ]
    )
    for item in report["recommended_policy"]:
        lines.append(f"- {item}")
    lines.append("")
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    report = build_report()
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report)
    print(
        "content audit status={status} entries={entries} forms={forms} blockers={blockers} review={review}".format(
            status=report["status"],
            entries=report["entry_count"],
            forms=report["form_count"],
            blockers=report["severity_counts"].get("BLOCKER", 0),
            review=report["severity_counts"].get("REVIEW_REQUIRED", 0),
        )
    )


if __name__ == "__main__":
    main()
