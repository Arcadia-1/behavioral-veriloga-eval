from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "benchmark-vabench-release-v1" / "reports" / "prompt_contract_manifest.json"


def test_prompt_contract_manifest_records_public_contract_v2() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    assert report["status"] == "pass"
    assert report["prompt_version_id"] == "public-contract-v2"
    assert report["previous_prompt_version"] == "pre-public-contract-v2"
    assert report["prompt_count"] == 249
    assert report["form_counts"] == {
        "bugfix": 49,
        "dut": 54,
        "e2e": 73,
        "tb": 73,
    }
    assert report["sync_script"] == "runners/sync_vabench_release_prompt_contracts.py"
    assert report["claim_policy"]["baseline_comparison"].startswith("pre-public-contract-v2")


def test_prompt_contract_manifest_rows_are_rerun_gated_and_clean() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    for row in report["rows"]:
        assert row["status"] == "pass", row["prompt"]
        assert row["prompt_version_id"] == "public-contract-v2"
        assert row["baseline_compatibility"] == "requires_rerun"
        assert row["missing_sections"] == []
        assert row["forbidden_text_present"] == []
        assert row["missing_target_artifacts"] == []
        assert len(row["prompt_sha256"]) == 64


def test_prompt_contract_manifest_tracks_converter_front_end_artifact_fix() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    row = next(item for item in report["rows"] if item["task_id"] == "vbr1_l2_converter_front_end:e2e")

    assert "tb_sample_hold_droop_ref.scs" in row["target_artifacts"]
    assert "tb_sample_hold_droop.scs" not in row["target_artifacts"]
