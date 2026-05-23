from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "benchmark-vabench-release-v1" / "reports"
REPORT = REPORTS / "paper_tables.json"
TABLES = REPORTS / "paper_tables"


def read_csv(name: str) -> list[dict[str, str]]:
    with (TABLES / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_paper_tables_export_all_expected_tables() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    tables = {item["id"]: item for item in report["tables"]}

    assert report["status"] == "in_progress"
    assert report["table_count"] == 5
    assert set(tables) == {
        "coverage",
        "parity",
        "claim_gate",
        "external_blockers",
        "speed_baseline",
    }
    for table in tables.values():
        assert table["row_count"] > 0
        assert (ROOT / table["csv"]).exists()


def test_coverage_and_parity_tables_keep_scope_boundaries() -> None:
    coverage = {row["metric"]: row for row in read_csv("coverage.csv")}
    parity = {row["metric"]: row for row in read_csv("parity.csv")}

    assert coverage["planned_l1_l2_entries"]["value"] == "72"
    assert coverage["planned_l1_l2_entries"]["claim_status"] == "allowed"
    assert coverage["scored_entries"]["value"] == "72"
    assert coverage["scored_entries"]["claim_status"] == "allowed"
    assert "not a scored denominator" in coverage["planned_l1_l2_entries"]["safe_caption_note"]

    assert parity["dual_certified_release_forms"]["value"] == "245"
    assert parity["dual_certified_release_forms"]["claim_status"] == "allowed"
    assert parity["dual_pending_release_forms"]["value"] == "0"
    assert parity["dual_pending_release_forms"]["claim_status"] == "allowed"
    assert parity["bridge_status"]["value"] == "ready"
    assert "not part of already imported full release certification" in parity["bridge_status"]["safe_caption_note"]
    assert "Full release dual certification evidence" in parity["dual_certified_release_forms"]["safe_caption_note"]


def test_claim_and_speed_baseline_tables_block_unfinished_paper_claims() -> None:
    claims = {row["claim_id"]: row for row in read_csv("claim_gate.csv")}
    speed_baseline = {row["artifact"]: row for row in read_csv("speed_baseline.csv")}

    assert claims["C3_imported_dual_subset_clean"]["status"] == "allowed"
    assert claims["C4_full_release_dual_certified"]["status"] == "allowed"
    assert claims["C9_release_package_complete"]["status"] == "allowed"
    assert claims["C4_full_release_dual_certified"]["blocked_until"] == ""

    assert speed_baseline["speed_debug"]["claim_status"] == "blocked"
    assert speed_baseline["baseline"]["claim_status"] == "blocked"
    assert speed_baseline["score_denominator"]["status"] == "score_enabled"
    assert speed_baseline["score_denominator"]["claim_allowed"] == "True"


def test_paper_table_report_declares_it_is_not_certification_evidence() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    assert any("do not create new certification evidence" in item for item in report["claim_boundary"])
    assert report["source_reports"]["claim_gate"].endswith("claim_gate.json")
    assert report["matrix_summary_snapshot"]["entry_count"] == 72
    assert report["matrix_summary_snapshot"]["pending_form_count"] == 0
