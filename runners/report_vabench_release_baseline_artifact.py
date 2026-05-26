#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
REPORTS_ROOT = PACKAGE_ROOT / "reports"
STATUS_REPORT_JSON = REPORTS_ROOT / "release_status.json"
DUAL_REPORT_JSON = REPORTS_ROOT / "dual_certification.json"
SCORE_DENOMINATOR_JSON = REPORTS_ROOT / "score_denominator_manifest.json"
RESULTS_ROOT = ROOT / "results"
REPORT_JSON = REPORTS_ROOT / "baseline_artifact.json"
REPORT_MD = REPORTS_ROOT / "baseline_artifact.md"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def discover_release_baseline_summaries() -> list[str]:
    summaries: list[str] = []
    if not RESULTS_ROOT.exists():
        return summaries
    for path in sorted(RESULTS_ROOT.glob("vabench-release-v1-baseline*/summary.json")):
        summaries.append(rel(path))
    return summaries


def build_report() -> dict[str, object]:
    status = read_json(STATUS_REPORT_JSON)
    dual = read_json(DUAL_REPORT_JSON)
    denominator = read_json(SCORE_DENOMINATOR_JSON)
    denominator_summary = denominator.get("summary", {})
    if not isinstance(denominator_summary, dict):
        denominator_summary = {}
    scored_entries = int(denominator_summary.get("scored_entry_count", 0) or 0)
    scored_forms = int(denominator_summary.get("scored_form_count", 0) or 0)
    certified_entries = int(status.get("fully_certified_entry_count", 0) or 0)
    dual_pending = int(dual.get("dual_pending_release_task_count", 0) or 0)
    dual_failed = int(dual.get("dual_failed_release_task_count", 0) or 0)
    summaries = discover_release_baseline_summaries()
    ready = scored_entries > 0 and scored_forms > 0 and dual_pending == 0 and dual_failed == 0
    if ready:
        execution_plan_status = "ready_for_baseline_runs"
    elif scored_entries > 0 and scored_forms > 0:
        execution_plan_status = "blocked_until_full_certification"
    else:
        execution_plan_status = "blocked_until_scored_release_exists"
    return {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "status": "ready_for_baseline_runs" if ready else "pending_release_baselines",
        "claim_allowed": ready and bool(summaries),
        "scored_release_entries": scored_entries,
        "scored_release_forms": scored_forms,
        "score_denominator_status": denominator.get("status", "missing"),
        "score_denominator": rel(SCORE_DENOMINATOR_JSON),
        "fully_certified_entry_count": certified_entries,
        "dual_pending_release_task_count": dual_pending,
        "dual_failed_release_task_count": dual_failed,
        "baseline_summary_count": len(summaries),
        "baseline_summaries": summaries,
        "execution_plan": {
            "status": execution_plan_status,
            "blocked_by": [
                *(["score denominator is disabled"] if scored_entries == 0 or scored_forms == 0 else []),
                *(["EVAS/Spectre release certification is pending"] if dual_pending else []),
                *(["EVAS/Spectre release certification has failures"] if dual_failed else []),
            ],
            "denominator_preview": {
                "planned_entries": denominator_summary.get("planned_entry_count", 0),
                "release_forms": denominator_summary.get("release_form_count", 0),
                "certified_entries": denominator_summary.get("certified_entry_count", 0),
                "certified_forms": denominator_summary.get("certified_form_count", 0),
                "scored_entries": scored_entries,
                "scored_forms": scored_forms,
            },
            "run_order": [
                "Use score_denominator_manifest.json as the frozen scored-row source.",
                "Run prompt-only model generation on the scored denominator.",
                "Run EVAS-feedback debugging as an engineering baseline, with Spectre as final judge.",
                "Aggregate pass@1, axis rates, and failure taxonomy into a release baseline summary.",
            ],
            "command_templates": [
                "python3 runners/finish_vabench_release_after_bridge.py",
                "python3 runners/report_vabench_release_score_denominator.py",
                "python3 runners/report_vabench_release_baseline_artifact.py",
            ],
            "aggregation_metrics": [
                "pass@1",
                "compile_pass_rate",
                "sim_correct_rate",
                "EVAS_PASS_Spectre_FAIL_count",
                "failure_taxonomy_counts",
            ],
        },
        "baseline_protocol": {
            "minimal_lanes": [
                "prompt_only_generation",
                "evas_feedback_debug_generation",
                "spectre_final_judge_confirmation",
            ],
            "non_goals": [
                "Do not present controller/RAG/SFT orchestration as the core contribution.",
                "Do not tune on the release package or memorize benchmark gold.",
            ],
            "required_result_fields": [
                "model",
                "task_id",
                "release_entry_id",
                "form",
                "candidate_artifacts",
                "evas_status",
                "spectre_status",
                "score",
                "failure_taxonomy",
            ],
            "result_schema_contract": {
                "spectre_is_final_judge": True,
                "evas_is_filter_debug_signal": True,
                "score_denominator_source": rel(SCORE_DENOMINATOR_JSON),
                "unscored_rows_excluded": True,
            },
        },
        "required_to_claim": [
            "Use the enabled score_denominator_manifest.json as the denominator source of truth.",
            "Run baseline model outputs through the release evaluator on scored rows.",
            "Publish pass@1 / axis rates / failure taxonomy with Spectre as the final judge.",
            "Keep baseline methods simple and describe them as stress tests, not as the paper's core method.",
        ],
    }


def write_markdown(report: dict[str, object]) -> None:
    lines = [
        "# vaBench Release Baseline Artifact",
        "",
        f"Date: {report['date']}",
        "",
        "This artifact gates model-baseline claims for the clean vaBench release.",
        "It intentionally keeps baseline workflows simple and secondary to the",
        "benchmark/evaluator contribution.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| status | `{report['status']}` |",
        f"| claim allowed | `{report['claim_allowed']}` |",
        f"| scored release entries | {report['scored_release_entries']} |",
        f"| scored release forms | {report['scored_release_forms']} |",
        f"| score denominator status | `{report['score_denominator_status']}` |",
        f"| fully certified entries | {report['fully_certified_entry_count']} |",
        f"| dual pending forms | {report['dual_pending_release_task_count']} |",
        f"| dual failed forms | {report['dual_failed_release_task_count']} |",
        f"| baseline summaries | {report['baseline_summary_count']} |",
        f"| execution plan | `{report['execution_plan']['status']}` |",
        "",
        "## Minimal Baseline Lanes",
        "",
    ]
    for item in report["baseline_protocol"]["minimal_lanes"]:
        lines.append(f"- `{item}`")
    lines.extend(["", "## Execution Plan", ""])
    for item in report["execution_plan"]["run_order"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Blocked By", ""])
    for item in report["execution_plan"]["blocked_by"]:
        lines.append(f"- {item}")
    if not report["execution_plan"]["blocked_by"]:
        lines.append("- none")
    lines.extend(["", "## Required To Claim", ""])
    for item in report["required_to_claim"]:
        lines.append(f"- {item}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    report = build_report()
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report)
    print(
        "wrote baseline artifact: status={status}; summaries={count}".format(
            status=report["status"],
            count=report["baseline_summary_count"],
        )
    )


if __name__ == "__main__":
    main()
