from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "benchmark-vabench-release-v1" / "reports" / "completion_audit.json"


def test_completion_audit_maps_goal_requirements_to_evidence() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    requirements = {item["id"]: item for item in report["requirements"]}

    assert report["status"] == "in_progress"
    assert requirements["R1_schema_package"]["status"] == "proved"
    assert "benchmark-vabench-release-v1/MANIFEST.json" in requirements["R1_schema_package"]["evidence"]
    assert "benchmark-vabench-release-v1/EVALUATOR.json" in requirements["R1_schema_package"]["evidence"]
    assert "schemas/vabench-package-manifest.schema.json" in requirements["R1_schema_package"]["evidence"]
    assert "schemas/vabench-evaluator-contract.schema.json" in requirements["R1_schema_package"]["evidence"]
    assert "schemas/vabench-speed-debug-artifact.schema.json" in requirements["R1_schema_package"]["evidence"]
    assert "schemas/vabench-baseline-artifact.schema.json" in requirements["R1_schema_package"]["evidence"]
    assert "schemas/vabench-paper-artifacts.schema.json" in requirements["R1_schema_package"]["evidence"]
    assert "schemas/vabench-claim-gate.schema.json" in requirements["R1_schema_package"]["evidence"]
    assert "schemas/vabench-score-denominator.schema.json" in requirements["R1_schema_package"]["evidence"]
    assert "schemas/vabench-dual-rerun-queue.schema.json" in requirements["R1_schema_package"]["evidence"]
    assert "schemas/vabench-dual-rerun-staging.schema.json" in requirements["R1_schema_package"]["evidence"]
    assert "schemas/vabench-dual-rerun-import.schema.json" in requirements["R1_schema_package"]["evidence"]
    assert "schemas/vabench-bridge-diagnostics.schema.json" in requirements["R1_schema_package"]["evidence"]
    assert "schemas/vabench-external-blockers.schema.json" in requirements["R1_schema_package"]["evidence"]
    assert "schemas/vabench-finish-readiness.schema.json" in requirements["R1_schema_package"]["evidence"]
    assert "schemas/vabench-completion-audit.schema.json" in requirements["R1_schema_package"]["evidence"]
    assert "schemas/vabench-finish-after-bridge-attempt.schema.json" in requirements["R1_schema_package"]["evidence"]
    assert "schemas/vabench-conformance-manifest.schema.json" in requirements["R1_schema_package"]["evidence"]
    assert "schemas/vabench-artifact-index.schema.json" in requirements["R1_schema_package"]["evidence"]
    assert "schemas/vabench-checksum-manifest.schema.json" in requirements["R1_schema_package"]["evidence"]
    assert "schemas/vabench-paper-tables.schema.json" in requirements["R1_schema_package"]["evidence"]
    assert "schemas/vabench-release-task-manifest-sync.schema.json" in requirements["R1_schema_package"]["evidence"]
    assert "schemas/vabench-release-status.schema.json" in requirements["R1_schema_package"]["evidence"]
    assert "schemas/vabench-asset-integrity.schema.json" in requirements["R1_schema_package"]["evidence"]
    assert "schemas/vabench-static-certification.schema.json" in requirements["R1_schema_package"]["evidence"]
    assert "schemas/vabench-dual-certification.schema.json" in requirements["R1_schema_package"]["evidence"]
    assert "schemas/vabench-certification-matrix.schema.json" in requirements["R1_schema_package"]["evidence"]
    assert "schemas/vabench-remaining-work.schema.json" in requirements["R1_schema_package"]["evidence"]
    assert requirements["R2_tracker_75_entries"]["status"] == "incomplete"
    assert "tracker count or L1/L2 split does not match target" in requirements["R2_tracker_75_entries"]["blockers"]
    assert requirements["R3_source_materialization"]["status"] == "incomplete"
    assert requirements["R4_static_certification"]["status"] == "proved"
    assert requirements["R6_l0_conformance_separate"]["status"] == "proved"
    assert requirements["R8_no_overclaiming"]["status"] == "proved"
    assert "benchmark-vabench-release-v1/reports/claim_gate.json" in requirements["R8_no_overclaiming"]["evidence"]
    assert report["evidence_sources"]["package_manifest"] == "benchmark-vabench-release-v1/MANIFEST.json"
    assert report["evidence_sources"]["evaluator_contract"] == "benchmark-vabench-release-v1/EVALUATOR.json"


def test_completion_audit_keeps_score_speed_and_baseline_claims_pending() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    requirements = {item["id"]: item for item in report["requirements"]}

    assert requirements["R5_dual_certification"]["status"] == "proved"
    assert "benchmark-vabench-release-v1/reports/finish_readiness.json" in requirements["R5_dual_certification"]["evidence"]
    assert requirements["R5_dual_certification"]["blockers"] == []
    assert requirements["R7_paper_artifacts"]["status"] == "incomplete"
    assert "benchmark-vabench-release-v1/reports/paper_tables.json" in requirements["R7_paper_artifacts"]["evidence"]
    assert any(item.startswith("external blocker report active:") for item in report["blocking_conditions"])
    assert "speed/debug timing artifact not claimable" in report["blocking_conditions"]
    assert "release model baseline artifact pending" in report["blocking_conditions"]
