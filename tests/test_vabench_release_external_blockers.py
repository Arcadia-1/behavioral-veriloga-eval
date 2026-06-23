from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "benchmark-vabench-release-v1" / "reports" / "external_blockers.json"


def test_external_blockers_is_claim_boundary_not_certification() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    assert report["status"] in {"blocked", "pending", "clear"}
    assert any("not EVAS/Spectre certification evidence" in item for item in report["claim_boundary"])
    assert any("blocked or dry-run simulator summary" in item for item in report["claim_boundary"])
    assert report["completion_status"] == "in_progress"


def test_external_blockers_explain_current_bridge_and_rerun_chain() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    blockers = {item["id"]: item for item in report["blockers"]}

    assert report["bridge_status"] in {"ready", "blocked"}
    assert report["latest_rerun_summary_status"] == "complete"
    assert report["latest_import_status"] == "imported"
    assert report["queue_count"] == 0
    assert report["ready_staging_bundle_count"] == 0
    assert "B1_bridge_ssh_or_tunnel_reachability" not in blockers
    assert "B2_fresh_dual_rerun_not_complete" not in blockers
    assert "B3_fresh_result_import_not_complete" not in blockers
    assert blockers["B4_downstream_paper_claims_disabled"]["status"] == "pending"


def test_external_blockers_include_recovery_commands_and_stop_conditions() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    for item in report["blockers"]:
        assert item["recovery_commands"]
        assert item["stop_condition"]
        assert item["claim_impact"]

    commands = [
        command
        for item in report["blockers"]
        for command in item["recovery_commands"]
    ]
    assert "python3 runners/report_vabench_release_speed_debug.py" in commands
    assert "python3 runners/report_vabench_release_baseline_artifact.py" in commands
    assert "python3 runners/finish_vabench_release_after_bridge.py" not in commands
