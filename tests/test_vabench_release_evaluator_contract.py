from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "benchmark-vabench-release-v1" / "EVALUATOR.json"


def test_evaluator_contract_records_current_selection_and_score_gate() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    selection = contract["task_selection"]
    score_gate = contract["score_gate"]

    assert contract["status"] == "ready"
    assert contract["release"] == "vabench-release-v1"
    assert contract["contract_version"] == "v1"
    assert selection["package_entry_count"] == 79
    assert selection["package_form_count"] == 271
    assert selection["certified_entries"] == 79
    assert selection["certified_forms"] == 271
    assert selection["pending_entries"] == 0
    assert selection["pending_forms"] == 0
    assert selection["scored_entries"] == 66
    assert selection["scored_forms"] == 236
    assert selection["score_enabled"] is True
    assert selection["l0_conformance_excluded"] is True
    assert selection["unscored_rows_excluded"] is True
    assert selection["v11_expansion_task_count"] == 300
    assert selection["v11_expansion_existing_certified_forms"] == 271
    assert selection["v11_expansion_proposed_pending_forms"] == 29
    assert selection["partial_pass_negatives_per_expansion_task"] == 5
    assert selection["partial_pass_negative_count"] == 1500
    assert score_gate["status"] == "score_enabled"
    assert score_gate["score_claim_allowed"] is True
    assert score_gate["ready_to_finish_release"] is True


def test_evaluator_contract_declares_backend_and_result_semantics() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    backends = contract["backend_roles"]
    result = contract["result_contract"]

    assert backends["spectre"]["final_judge"] is True
    assert backends["evas"]["final_judge"] is False
    assert backends["static"]["final_judge"] is False
    assert {"PASS", "FAIL_SIM_CORRECTNESS", "PENDING"} <= set(result["status_values"])
    assert result["spectre_final_judge"] is True
    assert result["evas_pass_spectre_fail_is_hard_mismatch"] is True
    assert "release_entry" in contract["schemas"]
    assert "release_task" in contract["schemas"]
    assert "package_manifest" in contract["schemas"]
    assert "evaluator_contract" in contract["schemas"]
    assert "speed_debug_artifact" in contract["schemas"]
    assert "baseline_artifact" in contract["schemas"]
    assert "paper_artifacts" in contract["schemas"]
    assert "claim_gate" in contract["schemas"]
    assert "score_denominator" in contract["schemas"]
    assert "dual_rerun_queue" in contract["schemas"]
    assert "dual_rerun_staging" in contract["schemas"]
    assert "dual_rerun_import" in contract["schemas"]
    assert "bridge_diagnostics" in contract["schemas"]
    assert "external_blockers" in contract["schemas"]
    assert "finish_readiness" in contract["schemas"]
    assert "completion_audit" in contract["schemas"]
    assert "finish_after_bridge_attempt" in contract["schemas"]
    assert "conformance_manifest" in contract["schemas"]
    assert "artifact_index" in contract["schemas"]
    assert "checksum_manifest" in contract["schemas"]
    assert "paper_tables" in contract["schemas"]
    assert "release_task_manifest_sync" in contract["schemas"]
    assert "release_status" in contract["schemas"]
    assert "asset_integrity" in contract["schemas"]
    assert "static_certification" in contract["schemas"]
    assert "dual_certification" in contract["schemas"]
    assert "certification_matrix" in contract["schemas"]
    assert "remaining_work" in contract["schemas"]
    assert "evidence" in contract["schemas"]
    assert "result" in contract["schemas"]
    assert "vabench_300_expansion_manifest" in contract["schemas"]
    assert "partial_pass_negatives" in contract["schemas"]


def test_evaluator_contract_keeps_baseline_speed_and_claims_blocked() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    baseline = contract["baseline_protocol"]
    speed = contract["speed_debug_protocol"]
    commands = contract["commands"]
    boundary = "\n".join(contract["claim_boundary"])

    assert baseline["status"] == "ready_for_baseline_runs"
    assert baseline["claim_allowed"] is False
    assert speed["status"] == "measured_subset"
    assert speed["claim_allowed"] is False
    assert commands["finish_after_bridge"] == "python3 runners/finish_vabench_release_after_bridge.py"
    assert commands["primary_dual_rerun"].startswith("./scripts/run_with_bridge.sh")
    assert commands["build_300_expansion"] == "python3 runners/build_vabench_300_expansion.py"
    assert commands["audit_300_negatives"] == "python3 runners/audit_vabench_300_expansion.py"
    assert "not simulator certification evidence" in boundary
    assert "Spectre is the final judge" in boundary
    assert "300-task expansion is an asset/negative-candidate surface" in boundary
