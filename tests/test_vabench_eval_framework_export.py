from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

from export_vabench_eval_framework import (  # noqa: E402
    ALIGNMENT_CSV,
    ALIGNMENT_JSON,
    MODEL_ROSTER_JSON,
    MODEL_ROSTER_TASK_IDS,
    export_eval_framework,
)
from run_vabench_release_minimax_baseline import scored_form_rows  # noqa: E402


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_eval_framework_exports_alignment_and_model_roster() -> None:
    written = export_eval_framework()

    assert written["alignment_json"] == ALIGNMENT_JSON
    assert written["model_roster_json"] == MODEL_ROSTER_JSON

    alignment = read_json(ALIGNMENT_JSON)
    roster = read_json(MODEL_ROSTER_JSON)

    assert alignment["status"] == "pass"
    assert alignment["summary"]["row_count"] == 300
    assert alignment["summary"]["aligned_row_count"] == 300
    assert alignment["summary"]["needs_review_row_count"] == 0
    assert alignment["summary"]["inherited_v1_rows"] == 271
    assert alignment["summary"]["promoted_v1_1_rows"] == 29
    assert alignment["summary"]["provisional_v1_1_rows"] == 0
    assert alignment["summary"]["bit_exact_claim"] == "not_asserted"
    assert alignment["summary"]["waveform_metric_row_count"] == 292
    assert alignment["summary"]["diagnostic_waveform_metric_row_count"] == 300
    assert alignment["summary"]["waveform_metric_recomputed_row_count"] == 8
    assert alignment["summary"]["metric_family_counts"] == {
        "extracted_gain_metric": 4,
        "pll_task_level_lock_frequency_control": 4,
        "waveform_relative_rms_and_absolute_voltage": 292,
    }
    assert all(
        row["alignment_status"] == "spectre_aligned_within_tolerance"
        for row in alignment["rows"]
        if row["provenance"] == "inherited_v1"
    )
    assert all(
        row["alignment_status"] == "spectre_aligned_within_tolerance"
        for row in alignment["rows"]
        if row["provenance"] == "promoted_v1.1"
    )
    assert all(
        row["equality_claim"] == "not bit-exact; equivalent within the stated acceptance gate"
        for row in alignment["rows"]
        if row["provenance"] == "inherited_v1"
    )
    assert all(
        row["equality_claim"] == "not bit-exact; equivalent within the stated acceptance gate"
        for row in alignment["rows"]
        if row["provenance"] == "promoted_v1.1"
    )
    assert all(row["comparison_target"].startswith("gold EVAS") for row in alignment["rows"])
    assert all(row["tolerance_result"] for row in alignment["rows"])
    assert any(row["waveform_metric_source"] == "recomputed_from_spectre_reference_result" for row in alignment["rows"])
    assert any("relative_gate PASS" in row["tolerance_result"] for row in alignment["rows"])
    assert any("small_absolute_gate FAIL" in row["tolerance_result"] for row in alignment["rows"])

    assert roster["status"] == "ready"
    assert roster["summary"]["scored_model_row_count"] == 265
    assert roster["summary"]["gold_aligned_rows"] == 265
    assert len(roster["form_rows"]) == 265
    assert all(row["counted_in_score"] is True for row in roster["form_rows"])
    assert all((ROOT / row["manifest"]).exists() for row in roster["form_rows"])

    assert sum(1 for _ in ALIGNMENT_CSV.open(encoding="utf-8")) == 301
    assert sum(1 for _ in MODEL_ROSTER_TASK_IDS.open(encoding="utf-8")) == 265


def test_model_runner_can_select_vabench300_roster() -> None:
    rows = scored_form_rows(
        denominator_path=MODEL_ROSTER_JSON,
        limit=None,
        entry=None,
        form=None,
        difficulty=None,
        category=None,
    )

    assert len(rows) == 265
    assert {row["provenance"] for row in rows} == {"inherited_v1", "promoted_v1.1"}
    assert all((ROOT / row["manifest"]).exists() for row in rows)
