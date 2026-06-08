from __future__ import annotations

import json
import re
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
EXPANSION = ROOT / "benchmark-vabench-release-v1" / "vabench-300-expansion"
MANIFEST = EXPANSION / "VABENCH_300_MANIFEST.json"
NEGATIVE_AUDIT = EXPANSION / "negative_audit.json"
EVAS_GOLD_SUMMARY = EXPANSION / "evas_gold_summary.json"
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
    assert manifest["summary"]["required_negative_per_task"] == 5
    assert manifest["summary"]["partial_pass_negative_count"] == 1500
    assert manifest["summary"]["negative_static_shallow_shape_verified_count"] == 1500
    assert manifest["summary"]["negative_simulator_shallow_verified_count"] == 0
    assert manifest["summary"]["negative_full_checker_fail_verified_count"] == 0
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
            assert negative["validation_evidence"] == {
                "full_checker_lane": "pending_external_evas_spectre",
                "publication_status": "asset_ready_not_simulator_certified",
                "simulator_shallow_lane": "pending_external_evas_spectre",
                "static_shallow_shape": "pass",
            }


def test_proposed_v11_tasks_have_gold_but_remain_pending_certification() -> None:
    manifest = read_json(MANIFEST)
    proposed = [row for row in manifest["tasks"] if row["expansion_status"].startswith("proposed_v1.1")]

    assert len(proposed) == 29
    for row in proposed:
        release_task = read_json(ROOT / row["release_task_manifest"])
        assert release_task["certification"] == {
            "static": "pending",
            "evas": "pending",
            "spectre": "pending",
            "evidence": "",
        }
        assert len(release_task["artifacts"]["gold"]) >= 2
        assert release_task["artifacts"]["negatives"] == row["negative_manifest"]
        assert all((ROOT / path).exists() for path in release_task["artifacts"]["gold"])


def test_negative_audit_proves_static_shallow_near_miss_shape() -> None:
    audit = read_json(NEGATIVE_AUDIT)

    assert audit["status"] == "pass"
    assert audit["task_count"] == 300
    assert audit["negative_count"] == 1500
    assert audit["shallow_static_pass_count"] == 1500
    assert audit["shallow_static_failed_count"] == 0
    assert audit["issue_count"] == 0


def test_evas_gold_summary_records_full_compile_sim_run_without_overclaiming() -> None:
    manifest = read_json(MANIFEST)
    summary = read_json(EVAS_GOLD_SUMMARY)

    assert summary["status"] == "pass"
    assert summary["engine"] == "evas-rust"
    assert summary["engine_label"] == "evas-rust"
    assert summary["task_count"] == 300
    assert summary["compile_sim_pass_count"] == 300
    assert summary["compile_sim_fail_count"] == 0
    assert summary["proposed_task_count"] == 29
    assert summary["proposed_compile_sim_pass_count"] == 29
    assert summary["proposed_behavior_checker_missing_count"] == 0
    assert summary["behavior_checker_missing_count"] == 0
    assert summary["behavior_checker_pass_count"] >= 288
    assert manifest["summary"]["evas_gold_compile_sim_pass_count"] == 300
    assert manifest["summary"]["evas_gold_behavior_checker_missing_count"] == 0
    assert manifest["summary"]["evas_gold_behavior_checker_pass_count"] >= 288
    assert len(summary["results"]) == 300
