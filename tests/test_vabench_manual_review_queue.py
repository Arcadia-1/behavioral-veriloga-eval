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

    assert len(rows) == 75
    assert {row["entry_id"] for row in rows} == expected_ids
    assert all(row["risk"] in {"P0", "P1", "P2", "P3"} for row in rows)
    assert all(row["human_review_question"] for row in rows)
    assert all(row["next_action_preference"] for row in rows)


def test_manual_review_queue_surfaces_known_high_risk_items() -> None:
    rows = {row["entry_id"]: row for row in csv.DictReader(QUEUE.open(encoding="utf-8"))}

    assert rows["vbr1_l1_binary_weighted_voltage_dac"]["risk"] == "P0"
    assert "simple_binary_voltage_dac_4b" in rows["vbr1_l1_binary_weighted_voltage_dac"]["prompt_preview"]
    assert "thermometer" not in rows["vbr1_l1_binary_weighted_voltage_dac"]["prompt_preview"].lower()
    assert rows["vbr1_l1_pfd_small_phase_error_response"]["risk"] == "P2"
    assert rows["vbr1_l1_vco_phase_integrator"]["risk"] == "P2"
    assert rows["vbr1_l1_aperture_delay_track_and_hold"]["risk"] == "P0"
    assert rows["vbr1_l1_one_shot_timer"]["risk"] == "P0"
