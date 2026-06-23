#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
REPORTS_ROOT = PACKAGE_ROOT / "reports"
CONTRACT_JSON = PACKAGE_ROOT / "EVALUATOR.json"
CONTRACT_MD = PACKAGE_ROOT / "EVALUATOR.md"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def as_int(value: object) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def build_report() -> dict[str, Any]:
    manifest = read_json(PACKAGE_ROOT / "MANIFEST.json")
    score = read_json(REPORTS_ROOT / "score_denominator_manifest.json")
    speed = read_json(REPORTS_ROOT / "speed_debug_artifact.json")
    baseline = read_json(REPORTS_ROOT / "baseline_artifact.json")
    finish = read_json(REPORTS_ROOT / "finish_readiness.json")
    claim_gate = read_json(REPORTS_ROOT / "claim_gate.json")
    conformance = read_json(REPORTS_ROOT / "conformance_manifest.json")
    score_summary = score.get("summary", {})
    if not isinstance(score_summary, dict):
        score_summary = {}
    manifest_summary = manifest.get("summary", {})
    if not isinstance(manifest_summary, dict):
        manifest_summary = {}

    scored_entries = as_int(score_summary.get("scored_entry_count"))
    scored_forms = as_int(score_summary.get("scored_form_count"))
    score_enabled = scored_entries > 0 and scored_forms > 0
    ready_for_baseline = baseline.get("status") == "ready_for_baseline_runs"
    l0_excluded = as_int(conformance.get("benchmark_coverage_count")) == 0
    status = "ready" if (PACKAGE_ROOT / "MANIFEST.json").exists() and score.get("status") else "in_progress"
    return {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "status": status,
        "contract_version": "v1",
        "inputs": {
            "package_manifest": rel(PACKAGE_ROOT / "MANIFEST.json"),
            "score_denominator": rel(REPORTS_ROOT / "score_denominator_manifest.json"),
            "claim_gate": rel(REPORTS_ROOT / "claim_gate.json"),
            "finish_readiness": rel(REPORTS_ROOT / "finish_readiness.json"),
            "l0_conformance_manifest": rel(REPORTS_ROOT / "conformance_manifest.json"),
        },
        "schemas": {
            "release_entry": rel(ROOT / "schemas" / "vabench-release-entry.schema.json"),
            "release_task": rel(ROOT / "schemas" / "vabench-release-task.schema.json"),
            "package_manifest": rel(ROOT / "schemas" / "vabench-package-manifest.schema.json"),
            "evaluator_contract": rel(ROOT / "schemas" / "vabench-evaluator-contract.schema.json"),
            "speed_debug_artifact": rel(ROOT / "schemas" / "vabench-speed-debug-artifact.schema.json"),
            "baseline_artifact": rel(ROOT / "schemas" / "vabench-baseline-artifact.schema.json"),
            "paper_artifacts": rel(ROOT / "schemas" / "vabench-paper-artifacts.schema.json"),
            "claim_gate": rel(ROOT / "schemas" / "vabench-claim-gate.schema.json"),
            "score_denominator": rel(ROOT / "schemas" / "vabench-score-denominator.schema.json"),
            "dual_rerun_queue": rel(ROOT / "schemas" / "vabench-dual-rerun-queue.schema.json"),
            "dual_rerun_staging": rel(ROOT / "schemas" / "vabench-dual-rerun-staging.schema.json"),
            "dual_rerun_import": rel(ROOT / "schemas" / "vabench-dual-rerun-import.schema.json"),
            "bridge_diagnostics": rel(ROOT / "schemas" / "vabench-bridge-diagnostics.schema.json"),
            "external_blockers": rel(ROOT / "schemas" / "vabench-external-blockers.schema.json"),
            "finish_readiness": rel(ROOT / "schemas" / "vabench-finish-readiness.schema.json"),
            "completion_audit": rel(ROOT / "schemas" / "vabench-completion-audit.schema.json"),
            "finish_after_bridge_attempt": rel(ROOT / "schemas" / "vabench-finish-after-bridge-attempt.schema.json"),
            "conformance_manifest": rel(ROOT / "schemas" / "vabench-conformance-manifest.schema.json"),
            "artifact_index": rel(ROOT / "schemas" / "vabench-artifact-index.schema.json"),
            "checksum_manifest": rel(ROOT / "schemas" / "vabench-checksum-manifest.schema.json"),
            "paper_tables": rel(ROOT / "schemas" / "vabench-paper-tables.schema.json"),
            "release_task_manifest_sync": rel(ROOT / "schemas" / "vabench-release-task-manifest-sync.schema.json"),
            "release_status": rel(ROOT / "schemas" / "vabench-release-status.schema.json"),
            "asset_integrity": rel(ROOT / "schemas" / "vabench-asset-integrity.schema.json"),
            "static_certification": rel(ROOT / "schemas" / "vabench-static-certification.schema.json"),
            "dual_certification": rel(ROOT / "schemas" / "vabench-dual-certification.schema.json"),
            "certification_matrix": rel(ROOT / "schemas" / "vabench-certification-matrix.schema.json"),
            "remaining_work": rel(ROOT / "schemas" / "vabench-remaining-work.schema.json"),
            "evidence": rel(ROOT / "schemas" / "vabench-evidence.schema.json"),
            "result": rel(ROOT / "schemas" / "vabench-release-result.schema.json"),
        },
        "task_selection": {
            "source_of_truth": rel(REPORTS_ROOT / "score_denominator_manifest.json"),
            "package_entry_count": as_int(manifest_summary.get("entry_count")),
            "package_form_count": as_int(manifest_summary.get("form_count")),
            "certified_entries": as_int(manifest_summary.get("certified_entry_count")),
            "certified_forms": as_int(manifest_summary.get("certified_form_count")),
            "pending_entries": as_int(manifest_summary.get("pending_entry_count")),
            "pending_forms": as_int(manifest_summary.get("pending_form_count")),
            "scored_entries": scored_entries,
            "scored_forms": scored_forms,
            "score_enabled": score_enabled,
            "l0_conformance_excluded": l0_excluded,
            "unscored_rows_excluded": True,
            "selection_rule": "Only rows marked counted_in_score=true by score_denominator_manifest.json may enter benchmark scores.",
        },
        "backend_roles": {
            "static": {
                "role": "source/package integrity gate",
                "certification_scope": "asset and static contract only",
                "final_judge": False,
            },
            "evas": {
                "role": "fast behavioral Verilog-A filter and debug evaluator",
                "certification_scope": "fast signal for release tasks, never final alone",
                "final_judge": False,
            },
            "spectre": {
                "role": "final simulator reference for release certification and scoring",
                "certification_scope": "behavioral correctness and final pass/fail axis",
                "final_judge": True,
            },
        },
        "result_contract": {
            "schema": rel(ROOT / "schemas" / "vabench-release-result.schema.json"),
            "required_fields": ["task_id", "release_entry_id", "backend", "status", "scores", "artifacts"],
            "status_values": [
                "PASS",
                "FAIL_STATIC",
                "FAIL_DUT_COMPILE",
                "FAIL_TB_COMPILE",
                "FAIL_SIM_CORRECTNESS",
                "FAIL_INFRA",
                "PENDING",
            ],
            "evidence_schema": rel(ROOT / "schemas" / "vabench-evidence.schema.json"),
            "evidence_verdict_values": ["not_certified", "certified", "quarantined"],
            "spectre_final_judge": True,
            "evas_pass_spectre_fail_is_hard_mismatch": True,
        },
        "score_gate": {
            "status": score.get("status", "missing"),
            "score_claim_allowed": bool(score.get("claim_rule", {}).get("score_claim_allowed", False))
            if isinstance(score.get("claim_rule"), dict)
            else False,
            "scored_entries": scored_entries,
            "scored_forms": scored_forms,
            "blocking_reason": (
                "score denominator is disabled until benchmark_score is explicitly enabled"
                if score.get("status") == "disabled_until_score_enablement"
                else "score denominator is disabled until full EVAS/Spectre certification"
            )
            if not score_enabled
            else "",
            "finish_readiness_status": finish.get("status", "missing"),
            "ready_to_finish_release": finish.get("ready_to_finish_release", False),
        },
        "baseline_protocol": {
            "status": baseline.get("status", "missing"),
            "ready_for_baseline_runs": ready_for_baseline,
            "claim_allowed": baseline.get("claim_allowed", False),
            "claim_status": baseline.get("claim_status", "missing"),
            "final_judge_baseline_count": as_int(baseline.get("final_judge_baseline_count")),
            "minimal_lanes": baseline.get("baseline_protocol", {}).get("minimal_lanes", [])
            if isinstance(baseline.get("baseline_protocol"), dict)
            else [],
            "required_result_fields": baseline.get("baseline_protocol", {}).get("required_result_fields", [])
            if isinstance(baseline.get("baseline_protocol"), dict)
            else [],
            "non_goals": baseline.get("baseline_protocol", {}).get("non_goals", [])
            if isinstance(baseline.get("baseline_protocol"), dict)
            else [],
            "unscored_rows_excluded": True,
        },
        "speed_debug_protocol": {
            "status": speed.get("status", "missing"),
            "claim_allowed": speed.get("claim_allowed", False),
            "required_timing_fields": speed.get("measurement_plan", {}).get("required_timing_fields", [])
            if isinstance(speed.get("measurement_plan"), dict)
            else [],
            "timed_rows": speed.get("measurement_scope", {}).get("timed_rows", 0)
            if isinstance(speed.get("measurement_scope"), dict)
            else 0,
        },
        "commands": {
            "refresh_package": "python3 runners/run_vabench_release_longrun.py",
            "finish_after_bridge": "python3 runners/finish_vabench_release_after_bridge.py",
            "primary_dual_rerun": "./scripts/run_with_bridge.sh python3 runners/run_vabench_release_dual_rerun.py --output-root results/vabench-release-v1-dual-rerun --timeout-s 180",
            "enable_score_denominator": "python3 runners/enable_vabench_release_score_denominator.py",
            "refresh_score_denominator": "python3 runners/report_vabench_release_score_denominator.py",
            "refresh_baseline_gate": "python3 runners/report_vabench_release_baseline_artifact.py",
        },
        "claim_boundary": [
            "This contract defines evaluator IO and score gates; it is not simulator certification evidence.",
            "Spectre is the final judge for release scoring.",
            "EVAS is a fast filter/debug evaluator and cannot certify a task by itself.",
            "L0 conformance cases are evaluator health checks and never scored benchmark rows.",
            "Baseline and speed/debug claims are independent dedicated-artifact gates.",
            f"claim_gate_status={claim_gate.get('status', 'missing')}",
        ],
    }


def write_markdown(report: dict[str, Any]) -> None:
    selection = report["task_selection"]
    score_gate = report["score_gate"]
    baseline = report["baseline_protocol"]
    speed = report["speed_debug_protocol"]
    lines = [
        "# vaBench Release Evaluator Contract",
        "",
        f"Date: {report['date']}",
        "",
        "This contract describes how the release package is consumed by evaluators",
        "and paper-facing baselines. It does not create certification evidence.",
        "",
        "## Task Selection",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| package entries | {selection['package_entry_count']} |",
        f"| package forms | {selection['package_form_count']} |",
        f"| certified entries | {selection['certified_entries']} |",
        f"| certified forms | {selection['certified_forms']} |",
        f"| scored entries | {selection['scored_entries']} |",
        f"| scored forms | {selection['scored_forms']} |",
        f"| L0 conformance excluded | `{selection['l0_conformance_excluded']}` |",
        "",
        "## Backend Roles",
        "",
        "| Backend | Role | Final judge |",
        "| --- | --- | --- |",
    ]
    for backend, payload in report["backend_roles"].items():
        lines.append(f"| `{backend}` | {payload['role']} | `{payload['final_judge']}` |")
    lines.extend(
        [
            "",
            "## Gates",
            "",
            f"- Score gate: `{score_gate['status']}`; scored entries/forms = {score_gate['scored_entries']}/{score_gate['scored_forms']}",
            f"- Finish readiness: `{score_gate['finish_readiness_status']}`",
            f"- Baseline gate: `{baseline['status']}`; claim allowed = `{baseline['claim_allowed']}`",
            f"- Speed/debug gate: `{speed['status']}`; claim allowed = `{speed['claim_allowed']}`",
            "",
            "## Commands",
            "",
            "| Command | Value |",
            "| --- | --- |",
        ]
    )
    for key, value in report["commands"].items():
        lines.append(f"| `{key}` | `{value}` |")
    lines.extend(["", "## Claim Boundary", ""])
    for item in report["claim_boundary"]:
        lines.append(f"- {item}")
    CONTRACT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    report = build_report()
    CONTRACT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report)
    print(
        "wrote evaluator contract: status={status}; scored_forms={forms}; baseline={baseline}".format(
            status=report["status"],
            forms=report["task_selection"]["scored_forms"],
            baseline=report["baseline_protocol"]["status"],
        )
    )


if __name__ == "__main__":
    main()
