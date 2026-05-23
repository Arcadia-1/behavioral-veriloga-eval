from __future__ import annotations

import csv
import json
from pathlib import Path

from runners.vabench_release_paths import release_entry_path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "VABENCH_RELEASE_SEED_MANIFEST.csv"
PACKAGE_TASKS = ROOT / "benchmark-vabench-release-v1" / "tasks"


def rows() -> list[dict[str, str]]:
    return list(csv.DictReader(MANIFEST.open(encoding="utf-8")))


def test_seed_manifest_links_all_current_l1_seed_entries() -> None:
    manifest = rows()

    assert len(manifest) == 26
    assert {row["certification_status"] for row in manifest} == {"not_certified"}
    assert "background_calibration_accumulator" not in {row["base_id"] for row in manifest}
    assert "offset_calibration_fsm" not in {row["base_id"] for row in manifest}


def test_seed_release_entries_are_score_enabled_after_certification() -> None:
    for row in rows():
        payload = json.loads(release_entry_path(PACKAGE_TASKS, row["entry_id"]).read_text(encoding="utf-8"))

        assert payload["counts"] == {
            "benchmark_score": True,
            "model_capability": False,
            "l0_conformance": False,
        }
        assert payload["certification"]["static"] == "pass"
        assert payload["certification"]["evas"] in {"pass", "pending"}
        assert payload["certification"]["spectre"] in {"pass", "pending"}
        if payload["certification"]["evas"] == "pending" or payload["certification"]["spectre"] == "pending":
            assert "evas_certification" in payload["release_blockers"]
            assert "spectre_certification" in payload["release_blockers"]
        assert payload["source_tasks"]
        assert all(source["prompt"] and source["meta"] and source["checks"] and source["gold"] for source in payload["source_tasks"])
        assert payload["release_tasks"]
        for release_task in payload["release_tasks"]:
            assert release_task["asset_materialized"] is True
            assert (ROOT / release_task["prompt"]).exists()
            assert (ROOT / release_task["meta"]).exists()
            assert (ROOT / release_task["checks"]).exists()
            assert release_task["gold"]
            assert all((ROOT / gold).exists() for gold in release_task["gold"])
