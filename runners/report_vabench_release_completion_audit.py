#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
REPORTS_ROOT = PACKAGE_ROOT / "reports"
TRACKER_CSV = ROOT / "docs" / "VABENCH_RELEASE_TRACKER.csv"
SCHEMAS = [
    ROOT / "schemas" / "vabench-release-entry.schema.json",
    ROOT / "schemas" / "vabench-release-task.schema.json",
    ROOT / "schemas" / "vabench-package-manifest.schema.json",
    ROOT / "schemas" / "vabench-evaluator-contract.schema.json",
    ROOT / "schemas" / "vabench-speed-debug-artifact.schema.json",
    ROOT / "schemas" / "vabench-baseline-artifact.schema.json",
    ROOT / "schemas" / "vabench-paper-artifacts.schema.json",
    ROOT / "schemas" / "vabench-claim-gate.schema.json",
    ROOT / "schemas" / "vabench-score-denominator.schema.json",
    ROOT / "schemas" / "vabench-dual-rerun-queue.schema.json",
    ROOT / "schemas" / "vabench-dual-rerun-staging.schema.json",
    ROOT / "schemas" / "vabench-dual-rerun-import.schema.json",
    ROOT / "schemas" / "vabench-bridge-diagnostics.schema.json",
    ROOT / "schemas" / "vabench-external-blockers.schema.json",
    ROOT / "schemas" / "vabench-finish-readiness.schema.json",
    ROOT / "schemas" / "vabench-completion-audit.schema.json",
    ROOT / "schemas" / "vabench-finish-after-bridge-attempt.schema.json",
    ROOT / "schemas" / "vabench-conformance-manifest.schema.json",
    ROOT / "schemas" / "vabench-artifact-index.schema.json",
    ROOT / "schemas" / "vabench-checksum-manifest.schema.json",
    ROOT / "schemas" / "vabench-paper-tables.schema.json",
    ROOT / "schemas" / "vabench-release-task-manifest-sync.schema.json",
    ROOT / "schemas" / "vabench-release-status.schema.json",
    ROOT / "schemas" / "vabench-asset-integrity.schema.json",
    ROOT / "schemas" / "vabench-static-certification.schema.json",
    ROOT / "schemas" / "vabench-dual-certification.schema.json",
    ROOT / "schemas" / "vabench-certification-matrix.schema.json",
    ROOT / "schemas" / "vabench-remaining-work.schema.json",
    ROOT / "schemas" / "vabench-evidence.schema.json",
    ROOT / "schemas" / "vabench-release-result.schema.json",
]
REPORT_JSON = REPORTS_ROOT / "completion_audit.json"
REPORT_MD = REPORTS_ROOT / "completion_audit.md"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def read_tracker() -> list[dict[str, str]]:
    if not TRACKER_CSV.exists():
        return []
    with TRACKER_CSV.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def req(
    *,
    requirement_id: str,
    requirement: str,
    status: str,
    evidence: list[str],
    finding: str,
    blockers: list[str] | None = None,
) -> dict[str, object]:
    return {
        "id": requirement_id,
        "requirement": requirement,
        "status": status,
        "evidence": evidence,
        "finding": finding,
        "blockers": blockers or [],
    }


def build_report() -> dict[str, object]:
    tracker = read_tracker()
    status = read_json(REPORTS_ROOT / "release_status.json")
    asset = read_json(REPORTS_ROOT / "asset_integrity.json")
    static = read_json(REPORTS_ROOT / "static_certification.json")
    dual = read_json(REPORTS_ROOT / "dual_certification.json")
    conformance = read_json(REPORTS_ROOT / "conformance_manifest.json")
    remaining = read_json(REPORTS_ROOT / "remaining_work.json")
    staging = read_json(REPORTS_ROOT / "dual_rerun_staging_manifest.json")
    import_report = read_json(REPORTS_ROOT / "dual_rerun_import.json")
    bridge = read_json(REPORTS_ROOT / "bridge_profile_diagnostics.json")
    external_blockers = read_json(REPORTS_ROOT / "external_blockers.json")
    finish_readiness = read_json(REPORTS_ROOT / "finish_readiness.json")
    speed = read_json(REPORTS_ROOT / "speed_debug_artifact.json")
    baseline = read_json(REPORTS_ROOT / "baseline_artifact.json")
    paper = read_json(REPORTS_ROOT / "paper_artifacts.json")
    claim_gate = read_json(REPORTS_ROOT / "claim_gate.json")
    paper_tables = read_json(REPORTS_ROOT / "paper_tables.json")
    schema_validation = read_json(REPORTS_ROOT / "schema_validation.json")
    package_manifest = read_json(PACKAGE_ROOT / "MANIFEST.json")
    evaluator_contract = read_json(PACKAGE_ROOT / "EVALUATOR.json")
    score_denominator = read_json(REPORTS_ROOT / "score_denominator_manifest.json")
    denominator_summary = score_denominator.get("summary", {})
    if not isinstance(denominator_summary, dict):
        denominator_summary = {}
    dual_rerun_queue = read_json(REPORTS_ROOT / "dual_rerun_queue.json")
    dual_rerun_queue_count = int(dual_rerun_queue.get("queue_count", 0) or 0)

    schema_missing = [rel(path) for path in SCHEMAS if not path.exists()]
    level_counts: dict[str, int] = {}
    for row in tracker:
        level_counts[row.get("level", "")] = level_counts.get(row.get("level", ""), 0) + 1

    paper_gates = paper.get("claim_gates", {}) if isinstance(paper.get("claim_gates"), dict) else {}
    blocking_conditions = list(paper_gates.get("blocking_conditions", []))
    blocked_claim_ids = claim_gate.get("blocked_claim_ids", [])
    if not isinstance(blocked_claim_ids, list):
        blocked_claim_ids = []
    scored_entries = int(status.get("scored_release_entries", 0) or 0)
    scored_forms = int(denominator_summary.get("scored_form_count", 0) or 0)

    requirements = [
        req(
            requirement_id="R1_schema_package",
            requirement="Define the clean release package, task, evaluator, score denominator, rerun/bridge/readiness gate, paper artifact, claim gate, speed/debug, baseline, result, and evidence schemas.",
            status=(
                "proved"
                if PACKAGE_ROOT.exists()
                and not schema_missing
                and package_manifest.get("release") == "vabench-release-v1"
                and evaluator_contract.get("status") == "ready"
                and schema_validation.get("status") == "pass"
                else "incomplete"
            ),
            evidence=[
                rel(PACKAGE_ROOT),
                rel(PACKAGE_ROOT / "MANIFEST.json"),
                rel(PACKAGE_ROOT / "EVALUATOR.json"),
                *[rel(path) for path in SCHEMAS],
                rel(REPORTS_ROOT / "schema_validation.json"),
            ],
            finding=(
                "Release package root, package manifest, evaluator contract, and all current release schemas are present and validate current release JSON surfaces."
                if PACKAGE_ROOT.exists()
                and not schema_missing
                and package_manifest.get("release") == "vabench-release-v1"
                and evaluator_contract.get("status") == "ready"
                and schema_validation.get("status") == "pass"
                else "Release package, manifest, evaluator contract, schema files, or schema validation report are incomplete."
            ),
            blockers=[
                *schema_missing,
                *([] if package_manifest.get("release") == "vabench-release-v1" else ["package manifest is missing or not for vabench-release-v1"]),
                *([] if evaluator_contract.get("status") == "ready" else ["evaluator contract is missing or not ready"]),
                *([] if schema_validation.get("status") == "pass" else ["schema validation is not passing"]),
            ],
        ),
        req(
            requirement_id="R2_tracker_75_entries",
            requirement="Create an execution tracker for the 75 selected L1/L2 functions.",
            status="proved" if len(tracker) == 75 and level_counts == {"L1": 60, "L2": 15} else "incomplete",
            evidence=[rel(TRACKER_CSV), rel(REPORTS_ROOT / "release_status.json")],
            finding=f"Tracker has {len(tracker)} rows with level counts {level_counts}.",
            blockers=[] if len(tracker) == 75 and level_counts == {"L1": 60, "L2": 15} else ["tracker count or L1/L2 split does not match target"],
        ),
        req(
            requirement_id="R3_source_materialization",
            requirement="Materialize each release task with prompt/meta/checks/gold assets.",
            status=(
                "proved"
                if status.get("source_linked_entry_count") == 75
                and status.get("asset_materialized_entry_count") == 75
                and asset.get("status") == "pass"
                else "incomplete"
            ),
            evidence=[rel(REPORTS_ROOT / "asset_integrity.json"), rel(REPORTS_ROOT / "release_status.json")],
            finding=(
                f"source-linked={status.get('source_linked_entry_count')}, "
                f"asset-materialized={status.get('asset_materialized_entry_count')}, "
                f"asset-status={asset.get('status')}"
            ),
            blockers=[] if asset.get("status") == "pass" else list(asset.get("issues", [])),
        ),
        req(
            requirement_id="R4_static_certification",
            requirement="Certify release task source assets with static/integrity checks.",
            status="proved" if static.get("status") == "pass" else "incomplete",
            evidence=[rel(REPORTS_ROOT / "static_certification.json")],
            finding=(
                f"static-status={static.get('status')}, "
                f"static-certified-forms={static.get('static_certified_release_task_count')}"
            ),
            blockers=list(static.get("issues", [])),
        ),
        req(
            requirement_id="R5_dual_certification",
            requirement="Certify release tasks with EVAS/Spectre evidence without importing blocked reruns.",
            status="proved" if dual.get("status") == "pass" else "blocked",
            evidence=[
                rel(REPORTS_ROOT / "dual_certification.json"),
                rel(REPORTS_ROOT / "dual_rerun_staging_manifest.json"),
                rel(REPORTS_ROOT / "dual_rerun_import.json"),
                rel(REPORTS_ROOT / "bridge_profile_diagnostics.json"),
                rel(REPORTS_ROOT / "external_blockers.json"),
                rel(REPORTS_ROOT / "finish_readiness.json"),
            ],
            finding=(
                f"dual-status={dual.get('status')}, dual-certified={dual.get('dual_certified_release_task_count')}, "
                f"dual-pending={dual.get('dual_pending_release_task_count')}, "
                f"EVAS-pass/Spectre-fail={dual.get('evas_pass_spectre_fail_count')}, "
                f"staging={staging.get('status')}, import={import_report.get('status')}, "
                f"bridge={bridge.get('status')}, finish-readiness={finish_readiness.get('status')}"
            ),
            blockers=[]
            if dual.get("status") == "pass"
            else [
                *([] if int(dual.get("dual_pending_release_task_count", 0) or 0) == 0 else ["EVAS/Spectre dual rerun remains pending"]),
                *([] if import_report.get("status") != "blocked" else [f"rerun import blocked: {import_report.get('reason')}"]),
                *([] if bridge.get("status") != "blocked" else [f"bridge blocked: {bridge.get('reason')}"]),
                *(
                    []
                    if external_blockers.get("status") not in {"blocked", "pending"}
                    else [
                        "external blockers active: "
                        f"{external_blockers.get('blocked_count')} blocked, "
                        f"{external_blockers.get('pending_count')} pending"
                    ]
                ),
            ],
        ),
        req(
            requirement_id="R6_l0_conformance_separate",
            requirement="Keep L0 EVAS/Spectre conformance separate from scored L1/L2 benchmark coverage.",
            status=(
                "proved"
                if int(conformance.get("conformance_case_count", 0) or 0) >= 4
                and conformance.get("benchmark_coverage_count") == 0
                else "incomplete"
            ),
            evidence=[rel(REPORTS_ROOT / "conformance_manifest.json")],
            finding=(
                f"conformance-cases={conformance.get('conformance_case_count')}, "
                f"benchmark-coverage-count={conformance.get('benchmark_coverage_count')}"
            ),
            blockers=[] if conformance.get("benchmark_coverage_count") == 0 else ["L0 conformance is leaking into benchmark denominator"],
        ),
        req(
            requirement_id="R7_paper_artifacts",
            requirement="Produce paper-facing coverage, parity, speed/debug, and baseline artifacts.",
            status=(
                "proved"
                if bool(speed.get("claim_allowed")) and bool(baseline.get("claim_allowed"))
                else "incomplete"
            ),
            evidence=[
                rel(REPORTS_ROOT / "paper_artifacts.json"),
                rel(REPORTS_ROOT / "paper_tables.json"),
                rel(REPORTS_ROOT / "external_blockers.json"),
                rel(REPORTS_ROOT / "speed_debug_artifact.json"),
                rel(REPORTS_ROOT / "baseline_artifact.json"),
            ],
            finding=(
                f"paper-status={paper.get('status')}, speed={speed.get('status')}, "
                f"speed-claim={speed.get('claim_allowed')}, baseline={baseline.get('status')}, "
                f"baseline-claim={baseline.get('claim_allowed')}, "
                f"paper-tables={paper_tables.get('status')}"
            ),
            blockers=[
                *([] if speed.get("claim_allowed") else ["speed/debug timing artifact is not claimable"]),
                *([] if baseline.get("claim_allowed") else ["release model baseline artifact is pending"]),
            ],
        ),
        req(
            requirement_id="R8_no_overclaiming",
            requirement="Do not over-claim uncertified tasks, unmeasured speedups, or missing baselines.",
            status=(
                "proved"
                if paper_gates.get("can_claim_scored_benchmark") is True
                and paper_gates.get("can_claim_speedup") is False
                and paper_gates.get("can_claim_model_baseline") is False
                and scored_entries > 0
                and scored_forms > 0
                and claim_gate.get("status") == "in_progress"
                and "C5_score_denominator_enabled" not in blocked_claim_ids
                and "C6_speed_debug_claim" in blocked_claim_ids
                and "C7_model_baseline_claim" in blocked_claim_ids
                else "incomplete"
            ),
            evidence=[
                rel(REPORTS_ROOT / "claim_gate.json"),
                rel(REPORTS_ROOT / "paper_artifacts.json"),
                rel(REPORTS_ROOT / "release_status.json"),
                rel(REPORTS_ROOT / "score_denominator_manifest.json"),
            ],
            finding=(
                f"scored={scored_entries}, "
                f"scored_forms={scored_forms}, "
                f"paper-claim-gates={paper_gates}, "
                f"blocked-claim-ids={blocked_claim_ids}"
            ),
            blockers=[] if blocking_conditions else ["paper claim gates do not list active blockers"],
        ),
    ]

    overall_status = "complete" if all(item["status"] == "proved" for item in requirements) else "in_progress"
    return {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "status": overall_status,
        "proved_count": sum(1 for item in requirements if item["status"] == "proved"),
        "blocked_count": sum(1 for item in requirements if item["status"] == "blocked"),
        "incomplete_count": sum(1 for item in requirements if item["status"] == "incomplete"),
        "requirements": requirements,
        "blocking_conditions": blocking_conditions,
        "next_actions": [
            "Use score_denominator_manifest.json as the recovery checklist for enabling scored release rows.",
            "Complete full-denominator same-slice EVAS/Spectre speed/debug timing from the fresh rerun.",
            "Run simple model baselines only after benchmark_score is enabled for certified release rows.",
        ],
        "notes": [
            "This audit proves the current state requirement-by-requirement; it does not mark the active goal complete.",
            "Blocked or pending simulator attempts are not imported as certification evidence.",
        ],
        "evidence_sources": {
            "tracker": rel(TRACKER_CSV),
            "release_status": rel(REPORTS_ROOT / "release_status.json"),
            "schema_validation": rel(REPORTS_ROOT / "schema_validation.json"),
            "package_manifest": rel(PACKAGE_ROOT / "MANIFEST.json"),
            "evaluator_contract": rel(PACKAGE_ROOT / "EVALUATOR.json"),
            "asset_integrity": rel(REPORTS_ROOT / "asset_integrity.json"),
            "static_certification": rel(REPORTS_ROOT / "static_certification.json"),
            "dual_certification": rel(REPORTS_ROOT / "dual_certification.json"),
            "remaining_work": rel(REPORTS_ROOT / "remaining_work.json"),
            "bridge_profile_diagnostics": rel(REPORTS_ROOT / "bridge_profile_diagnostics.json"),
            "external_blockers": rel(REPORTS_ROOT / "external_blockers.json"),
            "finish_readiness": rel(REPORTS_ROOT / "finish_readiness.json"),
            "claim_gate": rel(REPORTS_ROOT / "claim_gate.json"),
            "paper_tables": rel(REPORTS_ROOT / "paper_tables.json"),
            "paper_artifacts": rel(REPORTS_ROOT / "paper_artifacts.json"),
            "score_denominator_manifest": rel(REPORTS_ROOT / "score_denominator_manifest.json"),
        },
    }


def write_markdown(report: dict[str, object]) -> None:
    lines = [
        "# vaBench Release Completion Audit",
        "",
        f"Date: {report['date']}",
        "",
        "This report maps the active goal to concrete release evidence. It is",
        "intentionally conservative: partial or blocked evidence does not count as",
        "completion.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| status | `{report['status']}` |",
        f"| proved requirements | {report['proved_count']} |",
        f"| blocked requirements | {report['blocked_count']} |",
        f"| incomplete requirements | {report['incomplete_count']} |",
        "",
        "## Requirement Audit",
        "",
        "| ID | Status | Finding |",
        "| --- | --- | --- |",
    ]
    for item in report["requirements"]:
        lines.append(f"| `{item['id']}` | `{item['status']}` | {item['finding']} |")
    lines.extend(["", "## Blocking Conditions", ""])
    for blocker in report["blocking_conditions"]:
        lines.append(f"- {blocker}")
    if not report["blocking_conditions"]:
        lines.append("- none")
    lines.extend(["", "## Next Actions", ""])
    for action in report["next_actions"]:
        lines.append(f"- {action}")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    report = build_report()
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report)
    print(
        "wrote completion audit: status={status}; proved={proved}; blocked={blocked}; incomplete={incomplete}".format(
            status=report["status"],
            proved=report["proved_count"],
            blocked=report["blocked_count"],
            incomplete=report["incomplete_count"],
        )
    )


if __name__ == "__main__":
    main()
