from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "benchmark-vabench-release-v1" / "EVALUATOR.json"
V4_REQUIREMENTS = (
    ROOT / "benchmark-vabench-release-v4" / "V4_TRI_FORM_BENCHMARK_REQUIREMENTS.md"
)
V4_SOURCE = (
    ROOT
    / "benchmark-vabench-release-v4"
    / "provenance"
    / "dut-base-v3-exact-five-hash-bound-v2"
)


def test_evaluator_contract_records_current_selection_and_score_gate() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    selection = contract["task_selection"]
    score_gate = contract["score_gate"]

    assert contract["status"] == "ready"
    assert contract["release"] == "vabench-release-v1"
    assert contract["contract_version"] == "v1"
    assert selection["package_entry_count"] == 86
    assert selection["package_form_count"] == 300
    assert selection["certified_entries"] == 86
    assert selection["certified_forms"] == 300
    assert selection["pending_entries"] == 0
    assert selection["pending_forms"] == 0
    assert selection["scored_entries"] == 73
    assert selection["scored_forms"] == 265
    assert selection["score_enabled"] is True
    assert selection["l0_conformance_excluded"] is True
    assert selection["unscored_rows_excluded"] is True
    assert score_gate["status"] == "score_enabled"
    assert score_gate["score_claim_allowed"] is True
    assert score_gate["scored_entries"] == selection["scored_entries"]
    assert score_gate["scored_forms"] == selection["scored_forms"]


def test_evaluator_contract_declares_backend_and_result_semantics() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    backends = contract["backend_roles"]
    result = contract["result_contract"]

    assert backends["spectre"]["final_judge"] is False
    assert backends["evas"]["final_judge"] is True
    assert backends["static"]["final_judge"] is False
    assert {"PASS", "FAIL_SIM_CORRECTNESS", "PENDING"} <= set(result["status_values"])
    assert result["spectre_final_judge"] is False
    assert result["evas_final_judge"] is True
    assert result["evas_pass_spectre_fail_is_hard_mismatch"] is False
    assert "release_entry" in contract["schemas"]
    assert "release_task" in contract["schemas"]
    assert "package_manifest" in contract["schemas"]
    assert "evaluator_contract" in contract["schemas"]
    assert "score_denominator" in contract["schemas"]
    assert "conformance_manifest" in contract["schemas"]
    assert "static_certification" in contract["schemas"]
    assert "dual_certification" in contract["schemas"]
    assert "certification_matrix" in contract["schemas"]
    assert "evidence" in contract["schemas"]
    assert "result" in contract["schemas"]


def test_evaluator_contract_requires_evas_but_not_spectre_for_baselines() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    baseline = contract["baseline_protocol"]
    boundary = "\n".join(contract["claim_boundary"])

    assert baseline["status"] == "ready_for_baseline_runs"
    assert baseline["claim_allowed"] is True
    assert "evas_status" in baseline["required_result_fields"]
    assert "spectre_status" not in baseline["required_result_fields"]
    assert "evas_final_judge_confirmation" in baseline["minimal_lanes"]
    assert "not simulator certification evidence" in boundary
    assert "Pinned strict EVAS is the formal judge" in boundary
    assert "Spectre is optional non-blocking parity evidence" in boundary


def test_v4_normative_surfaces_do_not_require_spectre() -> None:
    requirements = V4_REQUIREMENTS.read_text(encoding="utf-8")
    forbidden_phrases = (
        "final Spectre scoring",
        "Private Spectre score",
        "Spectre is the final scoring backend",
        "targeted Spectre validation",
        "exactly one no-feedback Spectre decision",
    )
    assert not any(phrase in requirements for phrase in forbidden_phrases)

    for path in V4_SOURCE.glob("*/public/task/public_contract.json"):
        contract = json.loads(path.read_text(encoding="utf-8"))
        validation = contract.get("validation_status") or {}
        assert "evas_spectre" not in str(validation.get("next_gate", ""))
        assert validation.get("spectre_score_gold") not in {
            "pending",
            "pending_recertification",
        }
