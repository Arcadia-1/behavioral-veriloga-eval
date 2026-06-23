from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "benchmark-vabench-release-v1"
QUEUE = ROOT / "docs" / "VABENCH_MANUAL_REVIEW_QUEUE.csv"


def test_manual_review_queue_covers_every_clean_release_entry_once() -> None:
    manifest = json.loads((PACKAGE / "MANIFEST.json").read_text(encoding="utf-8"))
    expected_ids = {entry["release_entry_id"] for entry in manifest["entries"]}
    rows = list(csv.DictReader(QUEUE.open(encoding="utf-8")))

    assert len(rows) == 86
    assert {row["entry_id"] for row in rows} == expected_ids
    assert all(row["risk"] in {"P0", "P1", "P2", "P3"} for row in rows)
    assert all(row["human_review_question"] for row in rows)
    assert all(row["next_action_preference"] for row in rows)


def test_manual_review_queue_surfaces_current_review_items() -> None:
    rows = {row["entry_id"]: row for row in csv.DictReader(QUEUE.open(encoding="utf-8"))}

    assert "simple_binary_voltage_dac_4b" in rows["vbr1_l1_binary_weighted_voltage_dac"]["prompt_preview"]
    assert "thermometer" not in rows["vbr1_l1_binary_weighted_voltage_dac"]["prompt_preview"].lower()
    assert rows["vbr1_l2_pipeline_adc_chain"]["risk"] == "P1"
    assert rows["vbr1_l1_pipeline_adc_stage"]["risk"] in {"P2", "P3"}
    assert "vbr1_l1_clocked_comparator" not in rows
