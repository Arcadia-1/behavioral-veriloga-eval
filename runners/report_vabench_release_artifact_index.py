#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
REPORTS_ROOT = PACKAGE_ROOT / "reports"
REPORT_JSON = REPORTS_ROOT / "artifact_index.json"
REPORT_MD = REPORTS_ROOT / "artifact_index.md"
PLANNED_ENTRY_TARGET = 64


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def exists(path: Path) -> bool:
    return path.exists()


def artifact(
    *,
    artifact_id: str,
    path: Path,
    kind: str,
    purpose: str,
    claim_role: str,
    status: str,
    certification_evidence: bool,
    notes: list[str] | None = None,
) -> dict[str, object]:
    return {
        "id": artifact_id,
        "path": rel(path),
        "exists": exists(path),
        "kind": kind,
        "purpose": purpose,
        "claim_role": claim_role,
        "status": status if exists(path) else "missing",
        "certification_evidence": certification_evidence,
        "notes": notes or [],
    }


def build_report() -> dict[str, object]:
    release_status = read_json(REPORTS_ROOT / "release_status.json")
    schema_validation = read_json(REPORTS_ROOT / "schema_validation.json")
    task_manifest_sync = read_json(REPORTS_ROOT / "release_task_manifest_sync.json")
    asset = read_json(REPORTS_ROOT / "asset_integrity.json")
    static = read_json(REPORTS_ROOT / "static_certification.json")
    dual = read_json(REPORTS_ROOT / "dual_certification.json")
    certification_matrix = read_json(REPORTS_ROOT / "certification_matrix.json")
    queue = read_json(REPORTS_ROOT / "dual_rerun_queue.json")
    staging = read_json(REPORTS_ROOT / "dual_rerun_staging_manifest.json")
    rerun_import = read_json(REPORTS_ROOT / "dual_rerun_import.json")
    bridge = read_json(REPORTS_ROOT / "bridge_profile_diagnostics.json")
    external_blockers = read_json(REPORTS_ROOT / "external_blockers.json")
    finish_readiness = read_json(REPORTS_ROOT / "finish_readiness.json")
    speed = read_json(REPORTS_ROOT / "speed_debug_artifact.json")
    baseline = read_json(REPORTS_ROOT / "baseline_artifact.json")
    score_enablement = read_json(REPORTS_ROOT / "score_denominator_enablement.json")
    score_denominator = read_json(REPORTS_ROOT / "score_denominator_manifest.json")
    paper = read_json(REPORTS_ROOT / "paper_artifacts.json")
    claim_gate = read_json(REPORTS_ROOT / "claim_gate.json")
    paper_tables = read_json(REPORTS_ROOT / "paper_tables.json")
    evaluator_contract = read_json(PACKAGE_ROOT / "EVALUATOR.json")
    completion = read_json(REPORTS_ROOT / "completion_audit.json")
    checksum = read_json(REPORTS_ROOT / "checksum_manifest.json")
    conformance = read_json(REPORTS_ROOT / "conformance_manifest.json")
    queue_count = int(queue.get("queue_count", 0) or 0)

    gates = paper.get("claim_gates", {}) if isinstance(paper.get("claim_gates"), dict) else {}
    artifacts = [
        artifact(
            artifact_id="release_tracker",
            path=ROOT / "docs" / "VABENCH_RELEASE_TRACKER.csv",
            kind="tracker",
            purpose=f"{PLANNED_ENTRY_TARGET}-entry L1/L2 release coverage target.",
            claim_role="coverage_plan",
            status="ready" if release_status.get("planned_entries") == PLANNED_ENTRY_TARGET else "incomplete",
            certification_evidence=False,
        ),
        artifact(
            artifact_id="release_package_root",
            path=PACKAGE_ROOT,
            kind="package",
            purpose="Clean release package root with tasks, conformance, evidence, and reports.",
            claim_role="release_structure",
            status="ready" if release_status.get("source_linked_entry_count") == PLANNED_ENTRY_TARGET else "incomplete",
            certification_evidence=False,
        ),
        artifact(
            artifact_id="release_package_readme",
            path=PACKAGE_ROOT / "README.md",
            kind="runbook",
            purpose="Reader-facing package entrypoint with layout, claim boundaries, and reproducible commands.",
            claim_role="reproducibility",
            status="ready",
            certification_evidence=False,
        ),
        artifact(
            artifact_id="release_package_manifest",
            path=PACKAGE_ROOT / "MANIFEST.json",
            kind="package_manifest",
            purpose="Machine-readable package-level manifest for all release entries, forms, assets, evidence, and score status.",
            claim_role="reproducibility",
            status=str(read_json(PACKAGE_ROOT / "MANIFEST.json").get("status", "missing")),
            certification_evidence=False,
            notes=[
                rel(PACKAGE_ROOT / "MANIFEST.csv"),
                rel(PACKAGE_ROOT / "MANIFEST.md"),
                "This manifest indexes release assets; it is not simulator certification evidence.",
            ],
        ),
        artifact(
            artifact_id="release_evaluator_contract",
            path=PACKAGE_ROOT / "EVALUATOR.json",
            kind="evaluator_contract",
            purpose="Machine-readable evaluator/result contract for task selection, backend roles, score gates, and baseline lanes.",
            claim_role="reproducibility",
            status=str(evaluator_contract.get("status", "missing")),
            certification_evidence=False,
            notes=[
                rel(PACKAGE_ROOT / "EVALUATOR.md"),
                rel(ROOT / "schemas" / "vabench-evaluator-contract.schema.json"),
                "This contract defines evaluator IO and gates; it is not simulator certification evidence.",
            ],
        ),
        artifact(
            artifact_id="release_schemas",
            path=ROOT / "schemas" / "vabench-release-entry.schema.json",
            kind="schema",
            purpose="Machine-readable release entry/task/evidence/result schema family.",
            claim_role="reproducibility",
            status="ready",
            certification_evidence=False,
            notes=[
                rel(ROOT / "schemas" / "vabench-release-task.schema.json"),
                rel(ROOT / "schemas" / "vabench-package-manifest.schema.json"),
                rel(ROOT / "schemas" / "vabench-evaluator-contract.schema.json"),
                rel(ROOT / "schemas" / "vabench-speed-debug-artifact.schema.json"),
                rel(ROOT / "schemas" / "vabench-baseline-artifact.schema.json"),
                rel(ROOT / "schemas" / "vabench-paper-artifacts.schema.json"),
                rel(ROOT / "schemas" / "vabench-claim-gate.schema.json"),
                rel(ROOT / "schemas" / "vabench-score-denominator.schema.json"),
                rel(ROOT / "schemas" / "vabench-dual-rerun-queue.schema.json"),
                rel(ROOT / "schemas" / "vabench-dual-rerun-staging.schema.json"),
                rel(ROOT / "schemas" / "vabench-dual-rerun-import.schema.json"),
                rel(ROOT / "schemas" / "vabench-bridge-diagnostics.schema.json"),
                rel(ROOT / "schemas" / "vabench-external-blockers.schema.json"),
                rel(ROOT / "schemas" / "vabench-finish-readiness.schema.json"),
                rel(ROOT / "schemas" / "vabench-completion-audit.schema.json"),
                rel(ROOT / "schemas" / "vabench-finish-after-bridge-attempt.schema.json"),
                rel(ROOT / "schemas" / "vabench-conformance-manifest.schema.json"),
                rel(ROOT / "schemas" / "vabench-artifact-index.schema.json"),
                rel(ROOT / "schemas" / "vabench-checksum-manifest.schema.json"),
                rel(ROOT / "schemas" / "vabench-paper-tables.schema.json"),
                rel(ROOT / "schemas" / "vabench-release-task-manifest-sync.schema.json"),
                rel(ROOT / "schemas" / "vabench-release-status.schema.json"),
                rel(ROOT / "schemas" / "vabench-asset-integrity.schema.json"),
                rel(ROOT / "schemas" / "vabench-static-certification.schema.json"),
                rel(ROOT / "schemas" / "vabench-dual-certification.schema.json"),
                rel(ROOT / "schemas" / "vabench-certification-matrix.schema.json"),
                rel(ROOT / "schemas" / "vabench-remaining-work.schema.json"),
                rel(ROOT / "schemas" / "vabench-evidence.schema.json"),
                rel(ROOT / "schemas" / "vabench-release-result.schema.json"),
            ],
        ),
        artifact(
            artifact_id="release_task_manifest_sync",
            path=REPORTS_ROOT / "release_task_manifest_sync.json",
            kind="report",
            purpose="Generated per-form release_task.json manifests for every materialized release form.",
            claim_role="reproducibility",
            status=str(task_manifest_sync.get("status", "missing")),
            certification_evidence=False,
        ),
        artifact(
            artifact_id="schema_validation",
            path=REPORTS_ROOT / "schema_validation.json",
            kind="report",
            purpose="Schema validation for release entries, release task manifests, evidence, and results.",
            claim_role="reproducibility",
            status=str(schema_validation.get("status", "missing")),
            certification_evidence=False,
        ),
        artifact(
            artifact_id="asset_integrity",
            path=REPORTS_ROOT / "asset_integrity.json",
            kind="report",
            purpose="Prompt/meta/checks/gold asset integrity audit.",
            claim_role="source_materialization",
            status=str(asset.get("status", "missing")),
            certification_evidence=False,
        ),
        artifact(
            artifact_id="static_certification",
            path=REPORTS_ROOT / "static_certification.json",
            kind="report",
            purpose="Static certification for materialized release forms.",
            claim_role="static_quality",
            status=str(static.get("status", "missing")),
            certification_evidence=True,
        ),
        artifact(
            artifact_id="dual_certification",
            path=REPORTS_ROOT / "dual_certification.json",
            kind="report",
            purpose="Imported EVAS/Spectre certification evidence and pending dual evidence.",
            claim_role="parity",
            status=str(dual.get("status", "missing")),
            certification_evidence=True,
            notes=[
                f"dual_certified_release_task_count={dual.get('dual_certified_release_task_count', 'missing')}",
                f"dual_pending_release_task_count={dual.get('dual_pending_release_task_count', 'missing')}",
                f"evas_pass_spectre_fail_count={dual.get('evas_pass_spectre_fail_count', 'missing')}",
            ],
        ),
        artifact(
            artifact_id="certification_matrix",
            path=REPORTS_ROOT / "certification_matrix.json",
            kind="report",
            purpose="Entry/form-level certification matrix derived from dual evidence and score denominator gates.",
            claim_role="parity_audit",
            status=str(certification_matrix.get("status", "missing")),
            certification_evidence=False,
            notes=[
                "Derived audit view only; dual_certification.json remains the certification evidence source.",
                rel(REPORTS_ROOT / "certification_matrix_entries.csv"),
                rel(REPORTS_ROOT / "certification_matrix_forms.csv"),
            ],
        ),
        artifact(
            artifact_id="l0_conformance_manifest",
            path=REPORTS_ROOT / "conformance_manifest.json",
            kind="report",
            purpose="Non-scored EVAS/Spectre conformance cases kept outside the L1/L2 denominator.",
            claim_role="evaluator_health",
            status="ready" if conformance.get("benchmark_coverage_count") == 0 else "incomplete",
            certification_evidence=False,
        ),
        artifact(
            artifact_id="dual_rerun_queue",
            path=REPORTS_ROOT / "dual_rerun_queue.json",
            kind="execution_queue",
            purpose="Pending primary release rows that still need fresh EVAS/Spectre rerun.",
            claim_role="rerun_plan",
            status=str(queue.get("status", "missing")),
            certification_evidence=False,
        ),
        artifact(
            artifact_id="dual_rerun_staging",
            path=REPORTS_ROOT / "dual_rerun_staging_manifest.json",
            kind="execution_queue",
            purpose="Runnable staged bundles for release dual rerun.",
            claim_role="rerun_plan",
            status=str(staging.get("status", "missing")),
            certification_evidence=False,
            notes=["Staging readiness is not simulator pass evidence."],
        ),
        artifact(
            artifact_id="dual_rerun_import",
            path=REPORTS_ROOT / "dual_rerun_import.json",
            kind="report",
            purpose="Import gate for fresh dual rerun summaries.",
            claim_role="certification_import_gate",
            status=str(rerun_import.get("status", "missing")),
            certification_evidence=False,
            notes=["Blocked, dry-run, or running summaries are not imported as certification evidence."],
        ),
        artifact(
            artifact_id="bridge_profile_diagnostics",
            path=REPORTS_ROOT / "bridge_profile_diagnostics.json",
            kind="diagnostic",
            purpose="External bridge readiness diagnosis for the fresh EVAS/Spectre rerun.",
            claim_role="external_blocker",
            status=str(bridge.get("status", "missing")),
            certification_evidence=False,
            notes=["Bridge readiness is not EVAS/Spectre certification evidence."],
        ),
        artifact(
            artifact_id="external_blockers",
            path=REPORTS_ROOT / "external_blockers.json",
            kind="recovery_report",
            purpose="Conservative blocker and recovery sequence for external bridge, fresh rerun, import, speed, and baseline gates.",
            claim_role="external_blocker",
            status=str(external_blockers.get("status", "missing")),
            certification_evidence=False,
            notes=["This report is a claim-boundary and recovery artifact, not certification evidence."],
        ),
        artifact(
            artifact_id="finish_readiness",
            path=REPORTS_ROOT / "finish_readiness.json",
            kind="readiness_gate",
            purpose="Preflight gate for safely starting, importing, and finishing the fresh EVAS/Spectre release rerun.",
            claim_role="recovery_path",
            status=str(finish_readiness.get("status", "missing")),
            certification_evidence=False,
            notes=["Readiness does not imply simulator certification evidence."],
        ),
        artifact(
            artifact_id="finish_after_bridge_attempt",
            path=REPORTS_ROOT / "finish_after_bridge_attempt.json",
            kind="execution_report",
            purpose="One-command finish attempt report for post-bridge rerun/import/artifact refresh.",
            claim_role="recovery_path",
            status=str(read_json(REPORTS_ROOT / "finish_after_bridge_attempt.json").get("status", "missing")),
            certification_evidence=False,
        ),
        artifact(
            artifact_id="speed_debug_artifact",
            path=REPORTS_ROOT / "speed_debug_artifact.json",
            kind="report",
            purpose="Same-slice EVAS/Spectre timing and debug evidence gate.",
            claim_role="speed_debug",
            status=str(speed.get("status", "missing")),
            certification_evidence=False,
        ),
        artifact(
            artifact_id="baseline_artifact",
            path=REPORTS_ROOT / "baseline_artifact.json",
            kind="report",
            purpose="Model baseline protocol and claim gate.",
            claim_role="baseline",
            status=str(baseline.get("status", "missing")),
            certification_evidence=False,
        ),
        artifact(
            artifact_id="score_denominator_enablement",
            path=REPORTS_ROOT / "score_denominator_enablement.json",
            kind="report",
            purpose="P1 write-step record for frozen benchmark_score flags before denominator manifest rebuild.",
            claim_role="scoring_denominator",
            status=str(score_enablement.get("status", "missing")),
            certification_evidence=False,
            notes=[rel(REPORTS_ROOT / "score_denominator_enablement.md")],
        ),
        artifact(
            artifact_id="score_denominator_manifest",
            path=REPORTS_ROOT / "score_denominator_manifest.json",
            kind="report",
            purpose="Source-of-truth manifest for which release entries/forms may enter score denominators.",
            claim_role="scoring_denominator",
            status=str(score_denominator.get("status", "missing")),
            certification_evidence=False,
            notes=["A task is not scored unless this manifest marks it counted_in_score=true."],
        ),
        artifact(
            artifact_id="paper_artifacts",
            path=REPORTS_ROOT / "paper_artifacts.json",
            kind="report",
            purpose="Paper-facing coverage, parity, speed/debug, baseline, and claim-gate summary.",
            claim_role="paper_claims",
            status=str(paper.get("status", "missing")),
            certification_evidence=False,
        ),
        artifact(
            artifact_id="claim_gate",
            path=REPORTS_ROOT / "claim_gate.json",
            kind="claim_ledger",
            purpose="Paper-facing claim ledger with allowed/blocked wording and required evidence gates.",
            claim_role="paper_claims",
            status=str(claim_gate.get("status", "missing")),
            certification_evidence=False,
            notes=["This ledger prevents imported subset evidence from being phrased as full-release certification."],
        ),
        artifact(
            artifact_id="paper_tables",
            path=REPORTS_ROOT / "paper_tables.json",
            kind="paper_table_export",
            purpose="CSV/Markdown exports for coverage, parity, claim gates, blockers, speed/debug, and baselines.",
            claim_role="paper_claims",
            status=str(paper_tables.get("status", "missing")),
            certification_evidence=False,
            notes=[
                rel(REPORTS_ROOT / "paper_tables" / "coverage.csv"),
                rel(REPORTS_ROOT / "paper_tables" / "parity.csv"),
                rel(REPORTS_ROOT / "paper_tables" / "claim_gate.csv"),
                rel(REPORTS_ROOT / "paper_tables" / "external_blockers.csv"),
                rel(REPORTS_ROOT / "paper_tables" / "speed_baseline.csv"),
            ],
        ),
        artifact(
            artifact_id="completion_audit",
            path=REPORTS_ROOT / "completion_audit.json",
            kind="report",
            purpose="Requirement-by-requirement audit for the active release goal.",
            claim_role="completion_gate",
            status=str(completion.get("status", "missing")),
            certification_evidence=False,
        ),
        artifact(
            artifact_id="checksum_manifest",
            path=REPORTS_ROOT / "checksum_manifest.json",
            kind="report",
            purpose="SHA-256 manifest for release package, release docs, and schema files.",
            claim_role="reproducibility",
            status=str(checksum.get("status", "missing")),
            certification_evidence=False,
            notes=["Checksums support traceability; they are not simulator certification evidence."],
        ),
    ]
    command_index = [
        {
            "id": "refresh_release_package",
            "command": "python3 runners/run_vabench_release_longrun.py",
            "purpose": "Regenerate package, reports, staging, and tests without claiming blocked rerun evidence.",
        },
        {
            "id": "finish_after_bridge",
            "command": "python3 runners/finish_vabench_release_after_bridge.py",
            "purpose": "After bridge recovery, run fresh dual rerun, import complete evidence, and refresh paper gates.",
        },
        {
            "id": "external_blockers",
            "command": "python3 runners/report_vabench_release_external_blockers.py",
            "purpose": "Refresh the claim-boundary blocker report without running simulators.",
        },
        {
            "id": "finish_readiness",
            "command": "python3 runners/report_vabench_release_finish_readiness.py",
            "purpose": "Refresh the preflight gate for starting/importing the fresh EVAS/Spectre release rerun.",
        },
        {
            "id": "certification_matrix",
            "command": "python3 runners/report_vabench_release_certification_matrix.py",
            "purpose": "Refresh the entry/form-level certification audit matrix without running simulators.",
        },
        {
            "id": "claim_gate",
            "command": "python3 runners/report_vabench_release_claim_gate.py",
            "purpose": "Refresh the paper-facing allowed/blocked claim ledger.",
        },
        {
            "id": "package_manifest",
            "command": "python3 runners/report_vabench_release_package_manifest.py",
            "purpose": "Refresh the root package manifest for release entries/forms and score status.",
        },
        {
            "id": "evaluator_contract",
            "command": "python3 runners/report_vabench_release_evaluator_contract.py",
            "purpose": "Refresh the evaluator/result contract and score/baseline gate description.",
        },
        {
            "id": "score_denominator_enablement",
            "command": "python3 runners/enable_vabench_release_score_denominator.py",
            "purpose": "Freeze benchmark_score flags after dual certification before refreshing score_denominator_manifest.json.",
        },
        {
            "id": "paper_tables",
            "command": "python3 runners/report_vabench_release_paper_tables.py",
            "purpose": "Refresh paper-ready CSV and Markdown tables from the current claim-gated reports.",
        },
        {
            "id": "primary_dual_rerun",
            "command": "./scripts/run_with_bridge.sh python3 runners/run_vabench_release_dual_rerun.py --output-root results/vabench-release-v1-dual-rerun --timeout-s 180",
            "purpose": f"Run the {queue_count}-row primary EVAS/Spectre release rerun through the bridge wrapper.",
        },
    ]
    missing = [item["id"] for item in artifacts if not item["exists"]]
    return {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "status": "in_progress" if completion.get("status") != "complete" else "complete",
        "artifact_count": len(artifacts),
        "missing_artifact_count": len(missing),
        "missing_artifacts": missing,
        "claim_gates": gates,
        "artifacts": artifacts,
        "commands": command_index,
        "notes": [
            "This index is a navigation and traceability layer; it does not create new certification evidence.",
            "Only artifacts marked certification_evidence=true can support simulator certification claims.",
            "Paper claims remain governed by claim_gate.json, paper_artifacts.json, and completion_audit.json.",
        ],
    }


def write_markdown(report: dict[str, object]) -> None:
    lines = [
        "# vaBench Release Artifact Index",
        "",
        f"Date: {report['date']}",
        "",
        "This index maps the release package artifacts to their role in the",
        "paper-facing claim surface. It is a navigation layer, not new",
        "certification evidence.",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| status | `{report['status']}` |",
        f"| artifacts | {report['artifact_count']} |",
        f"| missing artifacts | {report['missing_artifact_count']} |",
        "",
        "## Artifacts",
        "",
        "| ID | Status | Claim role | Certification evidence | Path |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in report["artifacts"]:
        lines.append(
            f"| `{item['id']}` | `{item['status']}` | `{item['claim_role']}` | `{item['certification_evidence']}` | `{item['path']}` |"
        )
    lines.extend(["", "## Commands", "", "| ID | Command |", "| --- | --- |"])
    for item in report["commands"]:
        lines.append(f"| `{item['id']}` | `{item['command']}` |")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    report = build_report()
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report)
    print(
        "wrote artifact index: status={status}; artifacts={count}; missing={missing}".format(
            status=report["status"],
            count=report["artifact_count"],
            missing=report["missing_artifact_count"],
        )
    )


if __name__ == "__main__":
    main()
