#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
TASKS_ROOT = PACKAGE_ROOT / "tasks"
EVIDENCE_ROOT = PACKAGE_ROOT / "evidence"
REPORTS_ROOT = PACKAGE_ROOT / "reports"
REPORT_JSON = REPORTS_ROOT / "schema_validation.json"
REPORT_MD = REPORTS_ROOT / "schema_validation.md"
PACKAGE_MANIFEST = PACKAGE_ROOT / "MANIFEST.json"
EXPANSION_ROOT = PACKAGE_ROOT / "vabench-300-expansion"
SCHEMAS = {
    "release_entry": ROOT / "schemas" / "vabench-release-entry.schema.json",
    "package_manifest": ROOT / "schemas" / "vabench-package-manifest.schema.json",
    "evaluator_contract": ROOT / "schemas" / "vabench-evaluator-contract.schema.json",
    "speed_debug_artifact": ROOT / "schemas" / "vabench-speed-debug-artifact.schema.json",
    "baseline_artifact": ROOT / "schemas" / "vabench-baseline-artifact.schema.json",
    "paper_artifacts": ROOT / "schemas" / "vabench-paper-artifacts.schema.json",
    "claim_gate": ROOT / "schemas" / "vabench-claim-gate.schema.json",
    "score_denominator": ROOT / "schemas" / "vabench-score-denominator.schema.json",
    "dual_rerun_queue": ROOT / "schemas" / "vabench-dual-rerun-queue.schema.json",
    "dual_rerun_staging": ROOT / "schemas" / "vabench-dual-rerun-staging.schema.json",
    "dual_rerun_import": ROOT / "schemas" / "vabench-dual-rerun-import.schema.json",
    "bridge_diagnostics": ROOT / "schemas" / "vabench-bridge-diagnostics.schema.json",
    "external_blockers": ROOT / "schemas" / "vabench-external-blockers.schema.json",
    "finish_readiness": ROOT / "schemas" / "vabench-finish-readiness.schema.json",
    "completion_audit": ROOT / "schemas" / "vabench-completion-audit.schema.json",
    "finish_after_bridge_attempt": ROOT / "schemas" / "vabench-finish-after-bridge-attempt.schema.json",
    "conformance_manifest": ROOT / "schemas" / "vabench-conformance-manifest.schema.json",
    "artifact_index": ROOT / "schemas" / "vabench-artifact-index.schema.json",
    "checksum_manifest": ROOT / "schemas" / "vabench-checksum-manifest.schema.json",
    "paper_tables": ROOT / "schemas" / "vabench-paper-tables.schema.json",
    "release_task_manifest_sync": ROOT / "schemas" / "vabench-release-task-manifest-sync.schema.json",
    "release_status": ROOT / "schemas" / "vabench-release-status.schema.json",
    "asset_integrity": ROOT / "schemas" / "vabench-asset-integrity.schema.json",
    "static_certification": ROOT / "schemas" / "vabench-static-certification.schema.json",
    "dual_certification": ROOT / "schemas" / "vabench-dual-certification.schema.json",
    "certification_matrix": ROOT / "schemas" / "vabench-certification-matrix.schema.json",
    "remaining_work": ROOT / "schemas" / "vabench-remaining-work.schema.json",
    "release_task": ROOT / "schemas" / "vabench-release-task.schema.json",
    "evidence": ROOT / "schemas" / "vabench-evidence.schema.json",
    "result": ROOT / "schemas" / "vabench-release-result.schema.json",
    "vabench_300_expansion_manifest": ROOT / "schemas" / "vabench-300-expansion-manifest.schema.json",
    "partial_pass_negatives": ROOT / "schemas" / "vabench-partial-pass-negatives.schema.json",
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def expected_release_entry_count(default: int) -> int:
    if not PACKAGE_MANIFEST.exists():
        return default
    manifest = read_json(PACKAGE_MANIFEST)
    summary = manifest.get("summary", {})
    if not isinstance(summary, dict):
        return default
    try:
        return int(summary.get("entry_count", default))
    except (TypeError, ValueError):
        return default


def validate_files(schema_id: str, paths: list[Path]) -> dict[str, object]:
    schema = read_json(SCHEMAS[schema_id])
    validator = jsonschema.Draft202012Validator(schema)
    failures: list[dict[str, str]] = []
    for path in paths:
        payload = read_json(path)
        errors = sorted(validator.iter_errors(payload), key=lambda err: list(err.path))
        for err in errors:
            failures.append(
                {
                    "path": rel(path),
                    "schema": schema_id,
                    "json_path": ".".join(str(part) for part in err.path),
                    "message": err.message,
                }
            )
    return {
        "schema": schema_id,
        "schema_path": rel(SCHEMAS[schema_id]),
        "file_count": len(paths),
        "failure_count": len(failures),
        "failures": failures,
    }


def build_report() -> dict[str, object]:
    groups = {
        "package_manifest": [PACKAGE_ROOT / "MANIFEST.json"] if (PACKAGE_ROOT / "MANIFEST.json").exists() else [],
        "evaluator_contract": [PACKAGE_ROOT / "EVALUATOR.json"] if (PACKAGE_ROOT / "EVALUATOR.json").exists() else [],
        "speed_debug_artifact": [REPORTS_ROOT / "speed_debug_artifact.json"] if (REPORTS_ROOT / "speed_debug_artifact.json").exists() else [],
        "baseline_artifact": [REPORTS_ROOT / "baseline_artifact.json"] if (REPORTS_ROOT / "baseline_artifact.json").exists() else [],
        "paper_artifacts": [REPORTS_ROOT / "paper_artifacts.json"] if (REPORTS_ROOT / "paper_artifacts.json").exists() else [],
        "claim_gate": [REPORTS_ROOT / "claim_gate.json"] if (REPORTS_ROOT / "claim_gate.json").exists() else [],
        "score_denominator": [REPORTS_ROOT / "score_denominator_manifest.json"] if (REPORTS_ROOT / "score_denominator_manifest.json").exists() else [],
        "dual_rerun_queue": [REPORTS_ROOT / "dual_rerun_queue.json"] if (REPORTS_ROOT / "dual_rerun_queue.json").exists() else [],
        "dual_rerun_staging": [REPORTS_ROOT / "dual_rerun_staging_manifest.json"] if (REPORTS_ROOT / "dual_rerun_staging_manifest.json").exists() else [],
        "dual_rerun_import": [REPORTS_ROOT / "dual_rerun_import.json"] if (REPORTS_ROOT / "dual_rerun_import.json").exists() else [],
        "bridge_diagnostics": [REPORTS_ROOT / "bridge_profile_diagnostics.json"] if (REPORTS_ROOT / "bridge_profile_diagnostics.json").exists() else [],
        "external_blockers": [REPORTS_ROOT / "external_blockers.json"] if (REPORTS_ROOT / "external_blockers.json").exists() else [],
        "finish_readiness": [REPORTS_ROOT / "finish_readiness.json"] if (REPORTS_ROOT / "finish_readiness.json").exists() else [],
        "completion_audit": [REPORTS_ROOT / "completion_audit.json"] if (REPORTS_ROOT / "completion_audit.json").exists() else [],
        "finish_after_bridge_attempt": [REPORTS_ROOT / "finish_after_bridge_attempt.json"] if (REPORTS_ROOT / "finish_after_bridge_attempt.json").exists() else [],
        "conformance_manifest": [REPORTS_ROOT / "conformance_manifest.json"] if (REPORTS_ROOT / "conformance_manifest.json").exists() else [],
        "artifact_index": [REPORTS_ROOT / "artifact_index.json"] if (REPORTS_ROOT / "artifact_index.json").exists() else [],
        "checksum_manifest": [REPORTS_ROOT / "checksum_manifest.json"] if (REPORTS_ROOT / "checksum_manifest.json").exists() else [],
        "paper_tables": [REPORTS_ROOT / "paper_tables.json"] if (REPORTS_ROOT / "paper_tables.json").exists() else [],
        "release_task_manifest_sync": [REPORTS_ROOT / "release_task_manifest_sync.json"] if (REPORTS_ROOT / "release_task_manifest_sync.json").exists() else [],
        "release_status": [REPORTS_ROOT / "release_status.json"] if (REPORTS_ROOT / "release_status.json").exists() else [],
        "asset_integrity": [REPORTS_ROOT / "asset_integrity.json"] if (REPORTS_ROOT / "asset_integrity.json").exists() else [],
        "static_certification": [REPORTS_ROOT / "static_certification.json"] if (REPORTS_ROOT / "static_certification.json").exists() else [],
        "dual_certification": [REPORTS_ROOT / "dual_certification.json"] if (REPORTS_ROOT / "dual_certification.json").exists() else [],
        "certification_matrix": [REPORTS_ROOT / "certification_matrix.json"] if (REPORTS_ROOT / "certification_matrix.json").exists() else [],
        "remaining_work": [REPORTS_ROOT / "remaining_work.json"] if (REPORTS_ROOT / "remaining_work.json").exists() else [],
        "release_entry": sorted(TASKS_ROOT.glob("*/vbr1_*/release_entry.json")),
        "release_task": sorted(TASKS_ROOT.glob("*/vbr1_*/forms/*/release_task.json")),
        "evidence": sorted(EVIDENCE_ROOT.glob("*/*/*/evidence.json")),
        "result": sorted(EVIDENCE_ROOT.glob("*/*/*/*result.json")),
        "vabench_300_expansion_manifest": (
            [EXPANSION_ROOT / "VABENCH_300_MANIFEST.json"]
            if (EXPANSION_ROOT / "VABENCH_300_MANIFEST.json").exists()
            else []
        ),
        "partial_pass_negatives": sorted(EXPANSION_ROOT.glob("**/manifest.json")),
    }
    validations = [validate_files(schema_id, paths) for schema_id, paths in groups.items()]
    issue_count = sum(int(item["failure_count"]) for item in validations)
    release_task_count = sum(
        len(read_json(path).get("release_tasks", []))
        for path in groups["release_entry"]
    )
    expected_counts = {
        "package_manifest": 1,
        "evaluator_contract": 1,
        "speed_debug_artifact": 1,
        "baseline_artifact": 1,
        "paper_artifacts": 1,
        "claim_gate": 1,
        "score_denominator": 1,
        "dual_rerun_queue": 1,
        "dual_rerun_staging": 1,
        "dual_rerun_import": 1,
        "bridge_diagnostics": 1,
        "external_blockers": 1,
        "finish_readiness": 1,
        "completion_audit": 1,
        "conformance_manifest": 1,
        "artifact_index": 1,
        "checksum_manifest": 1,
        "paper_tables": 1,
        "release_task_manifest_sync": 1,
        "release_status": 1,
        "asset_integrity": 1,
        "static_certification": 1,
        "dual_certification": 1,
        "certification_matrix": 1,
        "remaining_work": 1,
        "release_entry": expected_release_entry_count(len(groups["release_entry"])),
        "release_task": release_task_count,
        "evidence": release_task_count * 2,
        "result": release_task_count * 3,
        "vabench_300_expansion_manifest": 1 if (EXPANSION_ROOT / "VABENCH_300_MANIFEST.json").exists() else 0,
        "partial_pass_negatives": 300 if (EXPANSION_ROOT / "VABENCH_300_MANIFEST.json").exists() else 0,
    }
    count_issues = [
        {
            "schema": schema_id,
            "expected": expected,
            "actual": len(groups[schema_id]),
        }
        for schema_id, expected in expected_counts.items()
        if len(groups[schema_id]) != expected
    ]
    return {
        "date": date.today().isoformat(),
        "release": "vabench-release-v1",
        "status": "pass" if issue_count == 0 and not count_issues else "fail",
        "validated_file_count": sum(len(paths) for paths in groups.values()),
        "issue_count": issue_count,
        "count_issue_count": len(count_issues),
        "count_issues": count_issues,
        "validations": validations,
        "notes": [
            "This report validates release entry, release task, evidence, and result JSON against release schemas.",
            "Schema validity does not imply EVAS/Spectre certification; claim gates remain in paper_artifacts.json and completion_audit.json.",
        ],
    }


def write_markdown(report: dict[str, object]) -> None:
    lines = [
        "# vaBench Release Schema Validation",
        "",
        f"Date: {report['date']}",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| status | `{report['status']}` |",
        f"| validated files | {report['validated_file_count']} |",
        f"| schema issues | {report['issue_count']} |",
        f"| count issues | {report['count_issue_count']} |",
        "",
        "## Groups",
        "",
        "| Schema | Files | Failures |",
        "| --- | ---: | ---: |",
    ]
    for item in report["validations"]:
        lines.append(f"| `{item['schema']}` | {item['file_count']} | {item['failure_count']} |")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    report = build_report()
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    write_markdown(report)
    print(
        "validated release schemas: status={status}; files={files}; issues={issues}".format(
            status=report["status"],
            files=report["validated_file_count"],
            issues=report["issue_count"],
        )
    )


if __name__ == "__main__":
    main()
