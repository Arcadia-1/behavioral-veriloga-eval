#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
TASKS_ROOT = PACKAGE_ROOT / "tasks"
REPORTS_ROOT = PACKAGE_ROOT / "reports"
REPORT_JSON = REPORTS_ROOT / "checker_evidence_workplan.json"
REPORT_MD = REPORTS_ROOT / "checker_evidence_workplan.md"
PROMPT_MANIFEST = REPORTS_ROOT / "prompt_contract_manifest.json"
DUAL_CERTIFICATION = REPORTS_ROOT / "dual_certification.json"
TARGETED_L2_CHECKER_TIGHTENING = REPORTS_ROOT / "targeted_l2_checker_tightening_20260522.json"
SPEED_DEBUG = REPORTS_ROOT / "speed_debug_artifact.json"
SCORE_DENOMINATOR = REPORTS_ROOT / "score_denominator_manifest.json"

GENERIC_CHECKS = {
    "transient_analysis_present",
    "public_observables_saved",
    "dut_or_system_instantiated",
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def release_entries() -> list[dict[str, Any]]:
    return [read_json(path) for path in sorted(TASKS_ROOT.glob("*/vbr1_*/release_entry.json"))]


def parse_sim_checks(path: Path) -> list[str]:
    checks: list[str] = []
    in_sim_correct = False
    in_checks = False
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        stripped = raw.strip()
        if stripped == "sim_correct:":
            in_sim_correct = True
            in_checks = False
            continue
        if in_sim_correct and raw and not raw.startswith(" "):
            break
        if not in_sim_correct:
            continue
        if stripped == "checks:":
            in_checks = True
            continue
        if in_checks:
            if stripped.startswith("- "):
                checks.append(stripped[2:].strip().strip('"'))
                continue
            if stripped:
                in_checks = False
    return checks


def classify_checker_strength(checks: list[str]) -> str:
    if not checks:
        return "missing_behavior_checks"
    specific = [check for check in checks if check not in GENERIC_CHECKS]
    if not specific:
        return "structural_only"
    if len(specific) == 1:
        return "single_behavior_check"
    return "multi_behavior_check"


def l2_e2e_rows(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for entry in entries:
        if entry.get("level") != "L2":
            continue
        for task in entry.get("release_tasks", []):
            if task.get("form") != "e2e":
                continue
            checks_path = ROOT / str(task.get("checks", ""))
            checks = parse_sim_checks(checks_path) if checks_path.exists() else []
            strength = classify_checker_strength(checks)
            rows.append(
                {
                    "release_entry_id": entry.get("release_entry_id", ""),
                    "task_id": f"{entry.get('release_entry_id', '')}:e2e",
                    "category": entry.get("category", ""),
                    "base_function": entry.get("base_function", ""),
                    "checks": checks,
                    "specific_check_count": len([check for check in checks if check not in GENERIC_CHECKS]),
                    "checker_strength": strength,
                    "checks_path": rel(checks_path),
                    "prompt": str(task.get("prompt", "")),
                    "recommended_action": (
                        "manual_l2_composition_audit"
                        if strength in {"missing_behavior_checks", "structural_only", "single_behavior_check"}
                        else "confirm_checker_maps_to_composition_claim"
                    ),
                }
            )
    return rows


def build_work_items(
    prompt_manifest: dict[str, Any],
    dual: dict[str, Any],
    targeted_l2: dict[str, Any],
    speed: dict[str, Any],
    score: dict[str, Any],
    l2_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    weak_l2 = [
        row
        for row in l2_rows
        if row["checker_strength"] in {"missing_behavior_checks", "structural_only", "single_behavior_check"}
    ]
    scored_entries = score.get("summary", {}).get("scored_entry_count", 0) if isinstance(score.get("summary"), dict) else 0
    dual_ok = dual.get("status") == "pass" and int(dual.get("evas_pass_spectre_fail_count", 0) or 0) == 0
    targeted_ok = (
        targeted_l2.get("status") == "pass"
        and int(targeted_l2.get("summary", {}).get("fail_count", 0) or 0) == 0
        and int(targeted_l2.get("summary", {}).get("evas_pass_spectre_fail_count", 0) or 0) == 0
    )
    return [
        {
            "id": "W1_prompt_version_traceability",
            "priority": "P0",
            "status": "done" if prompt_manifest.get("status") == "pass" else "blocked",
            "work": "Treat public-contract-v2 as the prompt source of truth and mark old baselines historical.",
            "evidence": [rel(PROMPT_MANIFEST)],
            "stop_condition": "prompt_contract_manifest status=pass and every row baseline_compatibility=requires_rerun",
        },
        {
            "id": "W2_l2_checker_strength_audit",
            "priority": "P0",
            "status": "needs_manual_review" if weak_l2 else "ready_for_claim_mapping",
            "work": "Audit L2 e2e checkers for composition/measurement-flow strength instead of structural-only pass conditions.",
            "evidence": [rel(REPORT_JSON), *sorted({row["checks_path"] for row in weak_l2})[:10]],
            "row_count": len(l2_rows),
            "weak_or_needs_review_count": len(weak_l2),
            "stop_condition": "Every L2 e2e row has a checker claim mapped to a public composition behavior or is explicitly downgraded.",
        },
        {
            "id": "W3_evas_spectre_parity_evidence",
            "priority": "P0",
            "status": "done" if dual_ok and targeted_ok else "blocked",
            "work": "Keep historical full-release dual certification separate from targeted reruns for checker-tightened rows; preserve zero EVAS PASS / Spectre FAIL.",
            "evidence": [rel(DUAL_CERTIFICATION), rel(TARGETED_L2_CHECKER_TIGHTENING)],
            "targeted_refresh_policy": "No full dual refresh is required for prompt-only changes; checker changes require targeted reruns for affected rows.",
            "stop_condition": "dual_certification status=pass, targeted_l2_checker_tightening status=pass, and EVAS PASS / Spectre FAIL=0 in both evidence sources.",
        },
        {
            "id": "W4_speed_evidence_positioning",
            "priority": "P1",
            "status": "blocked_for_speed_claim" if not bool(speed.get("claim_allowed")) else "claim_allowed",
            "work": "Do not claim aggregate EVAS speedup until the speed artifact allows it; stratify or fix slow EVAS outliers, or narrow the claim.",
            "evidence": [rel(SPEED_DEBUG)],
            "stop_condition": "speed_debug_artifact claim_allowed=true, or paper wording uses a narrower measured-subset/no-speedup-safe statement.",
        },
        {
            "id": "W5_public_contract_v2_baseline_rerun",
            "priority": "P2",
            "status": "pending",
            "work": "Rerun minimal prompt-only baselines on public-contract-v2 after checker-strength decisions are frozen.",
            "evidence": [rel(PROMPT_MANIFEST), rel(SCORE_DENOMINATOR)],
            "scored_entry_count": scored_entries,
            "stop_condition": "Baseline artifact is regenerated against prompt_version_id=public-contract-v2.",
        },
    ]


def build_report() -> dict[str, Any]:
    entries = release_entries()
    l2_rows = l2_e2e_rows(entries)
    strength_counts = Counter(str(row["checker_strength"]) for row in l2_rows)
    prompt_manifest = read_json(PROMPT_MANIFEST)
    dual = read_json(DUAL_CERTIFICATION)
    targeted_l2 = read_json(TARGETED_L2_CHECKER_TIGHTENING)
    speed = read_json(SPEED_DEBUG)
    score = read_json(SCORE_DENOMINATOR)
    work_items = build_work_items(prompt_manifest, dual, targeted_l2, speed, score, l2_rows)
    return {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "status": "in_progress",
        "summary": {
            "prompt_version_id": prompt_manifest.get("prompt_version_id", "missing"),
            "prompt_manifest_status": prompt_manifest.get("status", "missing"),
            "l2_e2e_count": len(l2_rows),
            "l2_checker_strength_counts": dict(sorted(strength_counts.items())),
            "dual_status": dual.get("status", "missing"),
            "dual_certified_release_task_count": dual.get("dual_certified_release_task_count", 0),
            "evas_pass_spectre_fail_count": dual.get("evas_pass_spectre_fail_count", 0),
            "targeted_l2_checker_tightening_status": targeted_l2.get("status", "missing"),
            "targeted_l2_checker_tightening_pass_count": targeted_l2.get("summary", {}).get("pass_count", 0),
            "targeted_l2_checker_tightening_fail_count": targeted_l2.get("summary", {}).get("fail_count", 0),
            "speed_claim_allowed": bool(speed.get("claim_allowed")),
            "score_denominator_status": score.get("status", "missing"),
        },
        "work_items": work_items,
        "l2_e2e_rows": l2_rows,
        "evidence_sources": {
            "prompt_contract_manifest": rel(PROMPT_MANIFEST),
            "dual_certification": rel(DUAL_CERTIFICATION),
            "targeted_l2_checker_tightening": rel(TARGETED_L2_CHECKER_TIGHTENING),
            "speed_debug_artifact": rel(SPEED_DEBUG),
            "score_denominator_manifest": rel(SCORE_DENOMINATOR),
        },
    }


def write_markdown(report: dict[str, Any]) -> None:
    summary = report["summary"]
    lines = [
        "# vaBench Checker and EVAS/Spectre Evidence Workplan",
        "",
        f"Date: {report['date']}",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| prompt version | `{summary['prompt_version_id']}` |",
        f"| prompt manifest status | `{summary['prompt_manifest_status']}` |",
        f"| L2 e2e rows | {summary['l2_e2e_count']} |",
        f"| EVAS PASS / Spectre FAIL | {summary['evas_pass_spectre_fail_count']} |",
        f"| targeted L2 tightening status | `{summary['targeted_l2_checker_tightening_status']}` |",
        f"| targeted L2 tightening pass/fail | {summary['targeted_l2_checker_tightening_pass_count']} / {summary['targeted_l2_checker_tightening_fail_count']} |",
        f"| speed claim allowed | `{summary['speed_claim_allowed']}` |",
        "",
        "## Work Items",
        "",
        "| ID | Priority | Status | Work | Stop Condition |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in report["work_items"]:
        lines.append(
            f"| `{item['id']}` | `{item['priority']}` | `{item['status']}` | {item['work']} | {item['stop_condition']} |"
        )
    lines.extend(
        [
            "",
            "## L2 E2E Checker Strength",
            "",
            "| Entry | Category | Checks | Strength | Action |",
            "| --- | --- | ---: | --- | --- |",
        ]
    )
    for row in report["l2_e2e_rows"]:
        lines.append(
            f"| `{row['release_entry_id']}` | {row['category']} | {len(row['checks'])} | `{row['checker_strength']}` | `{row['recommended_action']}` |"
        )
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    report = build_report()
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report)
    print(
        "wrote checker/evidence workplan: l2_e2e={l2}; speed_claim_allowed={speed}; dual_status={dual}".format(
            l2=report["summary"]["l2_e2e_count"],
            speed=report["summary"]["speed_claim_allowed"],
            dual=report["summary"]["dual_status"],
        )
    )


if __name__ == "__main__":
    main()
