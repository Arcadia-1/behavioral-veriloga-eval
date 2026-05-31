from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "benchmark-vabench-release-v1" / "reports" / "artifact_index.json"


def test_artifact_index_lists_core_release_surfaces() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    artifacts = {item["id"]: item for item in report["artifacts"]}

    assert report["status"] == "in_progress"
    assert report["missing_artifact_count"] == 0
    for key in [
        "release_tracker",
        "release_package_readme",
        "release_package_manifest",
        "release_evaluator_contract",
        "release_schemas",
        "release_task_manifest_sync",
        "schema_validation",
        "asset_integrity",
        "static_certification",
        "dual_certification",
        "certification_matrix",
        "l0_conformance_manifest",
        "dual_rerun_staging",
        "bridge_profile_diagnostics",
        "external_blockers",
        "finish_readiness",
        "speed_debug_artifact",
        "baseline_artifact",
        "score_denominator_enablement",
        "score_denominator_manifest",
        "paper_artifacts",
        "claim_gate",
        "paper_tables",
        "completion_audit",
        "checksum_manifest",
    ]:
        assert artifacts[key]["exists"] is True


def test_artifact_index_separates_certification_evidence_from_diagnostics() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    artifacts = {item["id"]: item for item in report["artifacts"]}

    assert artifacts["static_certification"]["certification_evidence"] is True
    assert artifacts["dual_certification"]["certification_evidence"] is True
    assert artifacts["certification_matrix"]["certification_evidence"] is False
    assert artifacts["bridge_profile_diagnostics"]["certification_evidence"] is False
    assert artifacts["external_blockers"]["certification_evidence"] is False
    assert artifacts["finish_readiness"]["certification_evidence"] is False
    assert artifacts["release_package_manifest"]["certification_evidence"] is False
    assert artifacts["release_evaluator_contract"]["certification_evidence"] is False
    assert artifacts["dual_rerun_staging"]["certification_evidence"] is False
    assert artifacts["finish_after_bridge_attempt"]["certification_evidence"] is False
    assert artifacts["score_denominator_enablement"]["certification_evidence"] is False
    assert artifacts["score_denominator_manifest"]["certification_evidence"] is False
    assert artifacts["claim_gate"]["certification_evidence"] is False
    assert artifacts["paper_tables"]["certification_evidence"] is False


def test_artifact_index_records_reproducible_finish_commands() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    commands = {item["id"]: item["command"] for item in report["commands"]}

    assert "python3 runners/run_vabench_release_longrun.py" == commands["refresh_release_package"]
    assert commands["finish_after_bridge"] == "python3 runners/finish_vabench_release_after_bridge.py"
    assert commands["external_blockers"] == "python3 runners/report_vabench_release_external_blockers.py"
    assert commands["finish_readiness"] == "python3 runners/report_vabench_release_finish_readiness.py"
    assert commands["certification_matrix"] == "python3 runners/report_vabench_release_certification_matrix.py"
    assert commands["claim_gate"] == "python3 runners/report_vabench_release_claim_gate.py"
    assert commands["package_manifest"] == "python3 runners/report_vabench_release_package_manifest.py"
    assert commands["evaluator_contract"] == "python3 runners/report_vabench_release_evaluator_contract.py"
    assert commands["score_denominator_enablement"] == "python3 runners/enable_vabench_release_score_denominator.py"
    assert commands["paper_tables"] == "python3 runners/report_vabench_release_paper_tables.py"
    assert commands["primary_dual_rerun"].startswith("./scripts/run_with_bridge.sh")
