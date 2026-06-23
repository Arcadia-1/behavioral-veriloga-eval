from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

import run_vabench_300_dual_rerun as run300  # noqa: E402

EXPANSION = ROOT / "benchmark-vabench-release-v1" / "vabench-300-expansion"
MANIFEST = EXPANSION / "VABENCH_300_MANIFEST.json"
NEGATIVE_AUDIT = EXPANSION / "negative_audit.json"
FRESH_SPECTRE_REPORT = ROOT / "benchmark-vabench-release-v1" / "reports" / "vabench_300_v11_fresh_spectre_rerun.json"
CLOSURE_REPORT = ROOT / "speed-optimization" / "reports" / "vabench300_p0_p2_closure_20260620.md"
MANIFEST_SCHEMA = ROOT / "schemas" / "vabench-300-expansion-manifest.schema.json"
NEGATIVE_SCHEMA = ROOT / "schemas" / "vabench-partial-pass-negatives.schema.json"
EXPECTED_NEGATIVE_KINDS = {
    "boundary_near_miss",
    "timing_window_near_miss",
    "polarity_direction_near_miss",
    "state_reset_near_miss",
    "metric_writeout_near_miss",
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_vabench_300_manifest_materializes_task_and_negative_counts() -> None:
    manifest = read_json(MANIFEST)

    assert manifest["summary"]["task_count"] == 300
    assert manifest["summary"]["existing_certified_v1_task_count"] == 271
    assert manifest["summary"]["proposed_v11_task_count"] == 29
    assert manifest["summary"]["promoted_v11_task_count"] == 29
    assert manifest["summary"]["provisional_v11_task_count"] == 0
    assert manifest["summary"]["certified_task_count"] == 300
    assert manifest["summary"]["pending_certification_task_count"] == 0
    assert manifest["summary"]["paper_score_ready_task_count"] == 300
    assert manifest["summary"]["paper_score_disabled_v11_task_count"] == 0
    assert manifest["summary"]["fresh_spectre_v11_pass_count"] == 29
    assert manifest["summary"]["fresh_spectre_v11_nonpass_count"] == 0
    assert manifest["summary"]["fresh_spectre_v11_parity_pass_count"] == 29
    assert manifest["summary"]["score_denominator_pending_v11_task_count"] == 0
    assert manifest["summary"]["score_denominator_admitted_v11_task_count"] == 29
    assert manifest["summary"]["required_negative_per_task"] == 5
    assert manifest["summary"]["partial_pass_negative_count"] == 1500
    assert manifest["summary"]["negative_static_shallow_shape_verified_count"] == 1500
    assert manifest["summary"]["negative_simulator_shallow_verified_count"] == 145
    assert manifest["summary"]["negative_full_checker_fail_verified_count"] == 145
    assert manifest["summary"]["task_specific_v11_gold_pass_count"] == 29
    assert manifest["summary"]["task_specific_v11_negative_full_checker_fail_count"] == 145
    assert len(manifest["tasks"]) == 300
    assert sum(row["negative_count"] for row in manifest["tasks"]) == 1500
    assert all(row["negative_count"] == 5 for row in manifest["tasks"])


def test_vabench_300_task_ids_are_semantic_and_keep_legacy_aliases() -> None:
    manifest = read_json(MANIFEST)
    task_id_pattern = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*:(dut|tb|bugfix|e2e)$")
    topic_id_pattern = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")

    task_ids = [row["task_id"] for row in manifest["tasks"]]
    assert len(task_ids) == len(set(task_ids)) == 300
    for row in manifest["tasks"]:
        assert task_id_pattern.fullmatch(row["task_id"])
        assert topic_id_pattern.fullmatch(row["topic_id"])
        assert row["task_id"] == f"{row['topic_id']}:{row['form']}"
        assert row["legacy_task_id"].startswith("vbr")
        assert row["legacy_entry_id"].startswith("vbr")
        assert "level" not in row
        assert "release_entry_id" not in row


def test_vabench_300_manifests_match_json_schemas_when_available() -> None:
    jsonschema = pytest.importorskip("jsonschema")
    manifest = read_json(MANIFEST)

    jsonschema.validate(manifest, read_json(MANIFEST_SCHEMA))
    negative_schema = read_json(NEGATIVE_SCHEMA)
    for row in manifest["tasks"]:
        jsonschema.validate(read_json(ROOT / row["negative_manifest"]), negative_schema)


def test_each_vabench_300_negative_manifest_has_five_partial_pass_candidates() -> None:
    manifest = read_json(MANIFEST)
    for row in manifest["tasks"]:
        negative_manifest = ROOT / row["negative_manifest"]
        payload = read_json(negative_manifest)
        assert payload["task_id"] == row["task_id"]
        assert payload["negative_count"] == 5
        assert payload["policy"] == "five_partial_pass_near_miss_negatives_per_task"
        assert {negative["kind"] for negative in payload["negatives"]} == EXPECTED_NEGATIVE_KINDS
        for negative in payload["negatives"]:
            source = ROOT / negative["source"]
            assert source.exists(), negative["source"]
            assert negative["expected"] == "FAIL_FULL_CHECKER"
            assert negative["partial_pass_requirement"]
            assert negative["shallow_passes"]
            assert negative["full_failures"]
            assert negative["kind"] in negative["full_failures"]
            if row["expansion_status"] == "certified_v1.1_promoted":
                assert negative["validation_evidence"] == {
                    "full_checker_lane": "pass",
                    "publication_status": "evas_full_checker_verified_spectre_pending",
                    "simulator_shallow_lane": "pass",
                    "static_shallow_shape": "pass",
                }
            else:
                assert negative["validation_evidence"] == {
                    "full_checker_lane": "pending_external_evas_spectre",
                    "publication_status": "asset_ready_not_simulator_certified",
                    "simulator_shallow_lane": "pending_external_evas_spectre",
                    "static_shallow_shape": "pass",
                }


def test_v11_tasks_are_fresh_spectre_certified_and_score_admitted() -> None:
    manifest = read_json(MANIFEST)
    proposed = [row for row in manifest["tasks"] if row["expansion_status"] == "certified_v1.1_promoted"]
    fresh_report = read_json(FRESH_SPECTRE_REPORT)
    fresh_by_task = {row["task_id"]: row for row in fresh_report["rows"]}

    assert len(proposed) == 29
    assert fresh_report["status"] == "pass"
    assert fresh_report["summary"]["pass_count"] == 29
    assert fresh_report["summary"]["parity_pass_count"] == 29
    for row in proposed:
        assert row["certification"] == "fresh_evas_spectre_certified"
        assert row["static"] == "pass"
        assert row["evas"] == "pass"
        assert row["spectre"] == "pass"
        assert row["counted_in_score"] is True
        assert row["gold_status"] == "promoted_certified"
        assert row["paper_score_status"] == "admitted_to_score_denominator"
        assert row["fresh_spectre_evidence"] == "benchmark-vabench-release-v1/reports/vabench_300_v11_fresh_spectre_rerun.json"
        assert fresh_by_task[row["task_id"]]["raw_status"] == "PASS"
        assert fresh_by_task[row["task_id"]]["spectre_ok"] is True
        assert fresh_by_task[row["task_id"]]["spectre_behavior_score"] == 1.0
        assert fresh_by_task[row["task_id"]]["parity_status"] == "passed"
        release_task = read_json(ROOT / row["release_task_manifest"])
        assert release_task["certification"]["static"] == "pass"
        assert release_task["certification"]["evas"] == "pass"
        assert release_task["certification"]["spectre"] == "pass"
        assert release_task["certification"]["evidence"] == "benchmark-vabench-release-v1/reports/vabench_300_v11_fresh_spectre_rerun.json"
        assert release_task["certification"]["task_specific_quality_evidence"] == "benchmark-vabench-release-v1/vabench-300-expansion/v11_task_specific_quality_evidence.json"
        assert release_task["certification"]["paper_score_status"] == "admitted_to_score_denominator"
        assert release_task["counts"]["benchmark_score"] is True
        assert len(release_task["artifacts"]["gold"]) >= 2
        assert release_task["artifacts"]["negatives"] == row["negative_manifest"]
        assert all((ROOT / path).exists() for path in release_task["artifacts"]["gold"])
        prompt_text = (ROOT / release_task["artifacts"]["prompt"]).read_text(encoding="utf-8")
        assert "vaBench-300 v1.1 Task-Specific Contract" in prompt_text
        assert "task-specific benchmark candidate" in prompt_text


def test_vabench_300_runner_selects_all_certified_rows_by_default() -> None:
    manifest = read_json(MANIFEST)

    default_rows = run300.select_bundles(
        manifest,
        task_ids=None,
        legacy_entries=None,
        topics=None,
        forms=None,
        expansion_statuses=None,
        include_pending=False,
        limit=None,
    )
    certified_v11_rows = run300.select_bundles(
        manifest,
        task_ids=None,
        legacy_entries=None,
        topics=None,
        forms=None,
        expansion_statuses={"certified_v1.1_promoted"},
        include_pending=False,
        limit=None,
    )

    assert len(default_rows) == 300
    assert len(certified_v11_rows) == 29


def test_vabench_300_runner_status_filter_reflects_promoted_v11_rows() -> None:
    manifest = read_json(MANIFEST)

    certified_only = run300.select_bundles(
        manifest,
        task_ids=None,
        legacy_entries=None,
        topics=None,
        forms=None,
        expansion_statuses=None,
        include_pending=False,
        limit=None,
    )
    pending_only = run300.select_bundles(
        manifest,
        task_ids=None,
        legacy_entries=None,
        topics=None,
        forms=None,
        expansion_statuses={"proposed_v1.1_pending_certification"},
        include_pending=False,
        limit=None,
    )
    promoted_only = run300.select_bundles(
        manifest,
        task_ids=None,
        legacy_entries=None,
        topics=None,
        forms=None,
        expansion_statuses={"certified_v1.1_promoted"},
        include_pending=False,
        limit=None,
    )
    all_rows = run300.select_bundles(
        manifest,
        task_ids=None,
        legacy_entries=None,
        topics=None,
        forms=None,
        expansion_statuses=None,
        include_pending=True,
        limit=None,
    )

    assert len(certified_only) == 300
    assert len(pending_only) == 0
    assert len(promoted_only) == 29
    assert {bundle["expansion_status"] for bundle in promoted_only} == {"certified_v1.1_promoted"}
    assert len(all_rows) == 300


def test_negative_audit_proves_static_shallow_near_miss_shape() -> None:
    audit = read_json(NEGATIVE_AUDIT)

    assert audit["status"] == "pass"
    assert audit["task_count"] == 300
    assert audit["negative_count"] == 1500
    assert audit["shallow_static_pass_count"] == 1500
    assert audit["shallow_static_failed_count"] == 0
    assert audit["issue_count"] == 0


def test_full_300_closure_report_is_the_promotion_evidence() -> None:
    manifest = read_json(MANIFEST)
    report = CLOSURE_REPORT.read_text(encoding="utf-8")

    assert manifest["summary"]["certified_task_count"] == 300
    assert manifest["summary"]["provisional_v11_task_count"] == 0
    assert manifest["summary"]["score_denominator_pending_v11_task_count"] == 0
    assert manifest["summary"]["score_denominator_admitted_v11_task_count"] == 29
    assert "fresh full-300 双仿真结果为 300/300 PASS" in report
    assert "0 个 FAIL_PARITY" in report
    assert "0 个 FAIL_EVAS" in report
    assert "0 个 FAIL_INFRA" in report
