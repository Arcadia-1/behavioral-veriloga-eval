from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "benchmark-vabench-release-v1" / "reports" / "finish_readiness.json"


def test_finish_readiness_allows_finish_after_imported_full_rerun() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    checks = {item["id"]: item for item in report["checks"]}

    assert report["status"] == "ready_to_finish"
    assert report["ready_to_run_fresh_dual"] is False
    assert report["ready_to_import_fresh_dual"] is True
    assert report["ready_to_finish_release"] is True
    assert report["run_scope"]["primary_queue_rows"] == 0
    assert report["run_scope"]["ready_primary_queue_rows"] == 0
    assert report["run_scope"]["staged_bundle_count"] == 0
    assert report["run_scope"]["expected_primary_summary_tasks_total"] == 0

    assert checks["P1_local_release_package_ready"]["status"] == "pass"
    assert checks["P2_primary_rerun_queue_ready"]["status"] == "pass"
    assert checks["P3_staging_ready"]["status"] == "pass"
    assert checks["P4_bridge_ready"]["status"] == "pass"
    assert checks["P5_current_summary_acceptable"]["status"] == "pass"
    assert checks["P6_import_gate_clear"]["status"] == "pass"
    assert checks["P7_full_dual_certification_clear"]["status"] == "pass"


def test_finish_readiness_records_fresh_summary_acceptance_criteria_and_commands() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    criteria = report["fresh_summary_acceptance_criteria"]
    assert "summary.status == complete" in criteria
    assert any("matches the imported full-rerun summary" in item for item in criteria)
    assert "summary.expected_miss_count == 0" in criteria
    assert "A stale, blocked, dry-run, or partial summary must not be imported." in report["claim_boundary"]

    commands = report["next_commands"]
    assert commands["finish_after_bridge"] == "python3 runners/finish_vabench_release_after_bridge.py"
    assert commands["direct_primary_rerun"].startswith("./scripts/run_with_bridge.sh")
    assert commands["dry_run_finish_plan"].endswith("--dry-run --no-refresh-reports")


def test_finish_readiness_points_to_authoritative_evidence_sources() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    sources = report["evidence_sources"]

    assert sources["dual_rerun_queue"].endswith("dual_rerun_queue.json")
    assert sources["dual_rerun_staging"].endswith("dual_rerun_staging_manifest.json")
    assert sources["bridge_profile_diagnostics"].endswith("bridge_profile_diagnostics.json")
    assert sources["dual_rerun_import"].endswith("dual_rerun_import.json")
