from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "benchmark-vabench-release-v1" / "reports" / "checker_evidence_workplan.json"


def test_checker_evidence_workplan_ties_prompt_version_to_next_work() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    summary = report["summary"]
    work_items = {item["id"]: item for item in report["work_items"]}

    assert summary["prompt_version_id"] == "public-contract-v2"
    assert summary["prompt_manifest_status"] == "pass"
    assert work_items["W1_prompt_version_traceability"]["status"] == "done"
    assert work_items["W5_public_contract_v2_baseline_rerun"]["status"] == "pending"


def test_checker_evidence_workplan_preserves_dual_parity_boundary() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    summary = report["summary"]
    work_items = {item["id"]: item for item in report["work_items"]}

    assert summary["dual_status"] == "pass"
    assert summary["dual_certified_release_task_count"] == 259
    assert summary["evas_pass_spectre_fail_count"] == 0
    assert summary["targeted_l2_checker_tightening_status"] == "pass"
    assert summary["targeted_l2_checker_tightening_pass_count"] == 2
    assert summary["targeted_l2_checker_tightening_fail_count"] == 0
    assert work_items["W3_evas_spectre_parity_evidence"]["status"] == "done"
    assert (
        "benchmark-vabench-release-v1/reports/targeted_l2_checker_tightening_20260522.json"
        in work_items["W3_evas_spectre_parity_evidence"]["evidence"]
    )
    assert work_items["W4_speed_evidence_positioning"]["status"] == "blocked_for_speed_claim"


def test_checker_evidence_workplan_identifies_l2_checker_review_queue() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    summary = report["summary"]
    rows = {row["release_entry_id"]: row for row in report["l2_e2e_rows"]}
    work_items = {item["id"]: item for item in report["work_items"]}

    assert summary["l2_e2e_count"] == 15
    assert summary["l2_checker_strength_counts"] == {
        "multi_behavior_check": 15,
    }
    assert work_items["W2_l2_checker_strength_audit"]["status"] == "ready_for_claim_mapping"
    assert work_items["W2_l2_checker_strength_audit"]["weak_or_needs_review_count"] == 0
    assert rows["vbr1_l2_event_controller"]["checker_strength"] == "multi_behavior_check"
    assert rows["vbr1_l2_measurement_flow"]["checker_strength"] == "multi_behavior_check"
