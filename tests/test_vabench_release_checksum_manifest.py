from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "benchmark-vabench-release-v1" / "reports" / "checksum_manifest.json"


def test_checksum_manifest_hashes_release_artifact_surface_without_self_reference() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    files = {row["path"]: row for row in report["files"]}

    assert report["status"] == "pass"
    assert report["algorithm"] == "sha256"
    assert report["file_count"] > 2500
    assert "benchmark-vabench-release-v1/reports/checksum_manifest.json" not in files
    assert "benchmark-vabench-release-v1/reports/checksum_manifest.md" not in files
    assert "docs/VABENCH_RELEASE_TRACKER.csv" in files
    assert "schemas/vabench-release-result.schema.json" in files
    assert "schemas/vabench-package-manifest.schema.json" in files
    assert "schemas/vabench-evaluator-contract.schema.json" in files
    assert "schemas/vabench-speed-debug-artifact.schema.json" in files
    assert "schemas/vabench-baseline-artifact.schema.json" in files
    assert "schemas/vabench-paper-artifacts.schema.json" in files
    assert "schemas/vabench-claim-gate.schema.json" in files
    assert "schemas/vabench-score-denominator.schema.json" in files
    assert "schemas/vabench-dual-rerun-queue.schema.json" in files
    assert "schemas/vabench-dual-rerun-staging.schema.json" in files
    assert "schemas/vabench-dual-rerun-import.schema.json" in files
    assert "schemas/vabench-bridge-diagnostics.schema.json" in files
    assert "schemas/vabench-external-blockers.schema.json" in files
    assert "schemas/vabench-finish-readiness.schema.json" in files
    assert "schemas/vabench-completion-audit.schema.json" in files
    assert "schemas/vabench-finish-after-bridge-attempt.schema.json" in files
    assert "schemas/vabench-conformance-manifest.schema.json" in files
    assert "schemas/vabench-artifact-index.schema.json" in files
    assert "schemas/vabench-checksum-manifest.schema.json" in files
    assert "schemas/vabench-paper-tables.schema.json" in files
    assert "schemas/vabench-release-task-manifest-sync.schema.json" in files
    assert "schemas/vabench-release-status.schema.json" in files
    assert "schemas/vabench-asset-integrity.schema.json" in files
    assert "schemas/vabench-static-certification.schema.json" in files
    assert "schemas/vabench-dual-certification.schema.json" in files
    assert "schemas/vabench-certification-matrix.schema.json" in files
    assert "schemas/vabench-remaining-work.schema.json" in files
    assert "benchmark-vabench-release-v1/README.md" in files
    assert "benchmark-vabench-release-v1/EVALUATOR.json" in files
    assert "benchmark-vabench-release-v1/EVALUATOR.md" in files
    assert "benchmark-vabench-release-v1/MANIFEST.json" in files
    assert "benchmark-vabench-release-v1/MANIFEST.csv" in files
    assert "benchmark-vabench-release-v1/MANIFEST.md" in files
    assert "benchmark-vabench-release-v1/reports/artifact_index.json" in files


def test_checksum_manifest_categorizes_tasks_evidence_reports_and_schemas() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    counts = report["category_counts"]

    assert counts["release_tasks"] > 0
    assert counts["release_evidence"] > 0
    assert counts["release_reports"] > 0
    assert counts["schemas"] >= 30
    assert counts["release_docs"] >= 3
