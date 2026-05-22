from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "benchmark-vabench-release-v1"
REPORT = PACKAGE / "reports" / "dual_certification.json"


def test_dual_evidence_import_certifies_materialized_release_forms() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    assert report["status"] == "pass"
    assert report["simulator_rerun"] is True
    assert report["dual_certified_release_task_count"] == 259
    assert report["dual_failed_release_task_count"] == 0
    assert report["dual_pending_release_task_count"] == 0
    assert report["dual_pass_materialized_entry_count"] == 75
    assert report["dual_pending_materialized_entry_count"] == 0
    assert report["dual_failed_materialized_entry_count"] == 0
    assert report["fully_certified_entry_count"] == 75
    assert report["evas_pass_spectre_fail_count"] == 0
    assert report["issue_count"] == 0
    assert report["source_equivalence_blocked_release_task_count"] == 0
    assert report["source_equivalence_failure_count"] == 0


def test_dual_evidence_records_historical_source_and_hash_equivalence() -> None:
    evidence_paths = sorted((PACKAGE / "evidence" / "dual").glob("*/*/evidence.json"))

    assert len(evidence_paths) == 259
    certified_count = 0
    pending_count = 0
    fresh_rerun_count = 0
    historical_count = 0
    for path in evidence_paths:
        evidence = json.loads(path.read_text(encoding="utf-8"))
        assert evidence["static"] == "pass"
        if evidence["verdict"] != "certified":
            pending_count += 1
            assert evidence["evas"] == "pending"
            assert evidence["spectre"] == "pending"
            assert evidence["pending_blockers"]
            continue
        assert evidence["evas"] == "pass"
        assert evidence["spectre"] == "pass"
        assert evidence["failures"] == []
        assert evidence["pending_blockers"] == []
        if evidence["historical_evidence"]["simulator_rerun"] is True:
            assert evidence["historical_evidence"]["source"] == "fresh release dual rerun"
            assert evidence["release_rerun"]["summary"].startswith("results/vabench-release-v1-")
            fresh_rerun_count += 1
        else:
            assert evidence["historical_evidence"]["evas_result"].startswith(
                "results/vabench-main-v1-main120-gold-evas-2026-05-08/"
            )
            assert evidence["historical_evidence"]["spectre_result"].startswith(
                "results/vabench-main-v1-main120-gold-spectre-jin-2026-05-08/"
            )
            historical_count += 1
        certified_count += 1
    assert certified_count == 259
    assert pending_count == 0
    assert fresh_rerun_count == 161
    assert historical_count == 98


def test_incomplete_seed_entries_remain_blocked_by_missing_forms() -> None:
    entries = {
        path.parent.name: json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((PACKAGE / "tasks").glob("*/release_entry.json"))
    }

    assert entries["vbr1_l1_vco_phase_integrator"]["missing_forms"] == []
    assert entries["vbr1_l1_clock_divider"]["missing_forms"] == []
    certified = [
        entry
        for entry in entries.values()
        if entry["certification"]["static"] == "pass"
        and entry["certification"]["evas"] == "pass"
        and entry["certification"]["spectre"] == "pass"
        and entry["missing_forms"] == []
        and entry["release_blockers"] == []
    ]
    assert len(certified) == 75
    selected_entries = [entry for entry in entries.values() if str(entry["package_status"]).startswith("selected_")]
    assert len(selected_entries) == 47
    assert all(entry["certification"]["evas"] == "pass" for entry in selected_entries)
    assert all(entry["certification"]["spectre"] == "pass" for entry in selected_entries)
