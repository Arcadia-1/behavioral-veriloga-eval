from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

from export_vabench_precision_overview import (  # noqa: E402
    DOCS_PRECISION_JSON,
    PRECISION_JSON,
    PRECISION_MD,
    export_precision_overview,
)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_precision_overview_exports_fourway_and_spectre_anchor() -> None:
    written = export_precision_overview()

    assert written["precision_json"] == PRECISION_JSON
    assert written["precision_md"] == PRECISION_MD
    assert written["docs_precision_json"] == DOCS_PRECISION_JSON

    report = read_json(PRECISION_JSON)
    docs_report = read_json(DOCS_PRECISION_JSON)

    assert report == docs_report
    assert report["status"] == "pass"
    assert report["precision_source"] == "full300_current_summaries"
    assert report["summary"]["bit_exact_claim"] == "not_asserted"
    assert report["summary"]["benchmark_management_rows"] == 300
    assert report["summary"]["fourway_common_rows"] == 300
    assert report["summary"]["precision_evidence_rows"] == 300
    assert report["summary"]["precision_evidence_gap_rows"] == 0
    assert report["summary"]["historical_fourway_common_rows"] == 271
    assert report["summary"]["precision_total_comparisons"] == 900
    assert report["summary"]["precision_pass_comparisons"] == 900
    assert report["summary"]["precision_needs_review_comparisons"] == 0
    assert report["summary"]["precision_blocked_comparisons"] == 0
    assert report["summary"]["all_fourway_candidates_equivalent"] is True
    assert report["summary"]["needs_review_or_blocked_rows"] == 0
    assert report["summary"]["task_metric_comparisons"] == 12
    assert report["summary"]["spectre_self_consistency_pairs"] == 1036
    assert report["summary"]["spectre_self_consistency_pass_pairs"] == 1036

    rows = report["simulator_precision_rows"]
    assert {row["candidate"] for row in rows} == {"evas_python", "evas_rust", "spectre_ax"}
    assert all(row["compared_rows"] == 300 for row in rows)
    assert all(row["equivalent_rows"] == 300 for row in rows)
    assert all(row["claim"] == "equivalent_to_spectre_strict" for row in rows)
    assert all(row["task_metric_rows"] == 4 for row in rows)

    python = next(row for row in rows if row["candidate"] == "evas_python")
    rust = next(row for row in rows if row["candidate"] == "evas_rust")
    ax = next(row for row in rows if row["candidate"] == "spectre_ax")
    assert python["worst_effective_mean_relative_rms_error"] == 0.02166667063680534
    assert python["worst_effective_signal_relative_rms_error"] == 0.14793578426771162
    assert rust["worst_effective_mean_relative_rms_error"] == 0.03441570999201403
    assert rust["worst_effective_signal_relative_rms_error"] == 0.08704924544551784
    assert ax["worst_effective_mean_relative_rms_error"] == 0.019166666666666818
    assert ax["worst_effective_signal_relative_rms_error"] == 0.03833333333333333
    assert rust["max_task_metric_relative_delta"] == 0.017107409990336296

    anchor = report["spectre_self_consistency"]
    assert anchor["mode_a"] == "ax"
    assert anchor["mode_b"] == "classic"
    assert anchor["compared_pairs"] == 1036
    assert anchor["passed_pairs"] == 1036
    assert anchor["needs_review_pairs"] == 0
    assert anchor["row_mean_relative_rms_max"] == 0.08136556776886794
    assert anchor["worst_signal_relative_rms_max"] == 0.12439780220440254

    assert "Do not treat the historical 271-row four-way artifact as the current benchmark denominator." in report["claim_boundary"]["forbidden"]
    assert "Do not claim bit-exact waveform equality." in report["claim_boundary"]["forbidden"]
    assert "relative_waveform" in {gate["name"] for gate in report["gates"]}
    taxonomy = report["pointwise_difference_taxonomy"]
    assert "transition_smoothing" in {row["name"] for row in taxonomy}
    assert "event_time_and_cross" in {row["name"] for row in taxonomy}
    assert "noise_like_or_dithered_stimulus" in {row["name"] for row in taxonomy}
    for item in taxonomy:
        assert item["known_shortcoming"]
        assert item["current_handling"]
        assert item["bug_signal"]
        assert item["feedback_wanted"]
    assert len(report["needs_review_rows"]) == 0
    task_metric_rows = report["task_metric_rows"]
    assert len(task_metric_rows) == 12
    gain_flow_rows = [
        row
        for row in task_metric_rows
        if row["release_entry_id"] == "vbr1_l2_gain_extraction_convergence_measurement_flow"
    ]
    assert len(gain_flow_rows) == 6
    assert any(row["diagnostic_waveform_status"] == "needs_review" for row in gain_flow_rows)
    assert all(row["status"] == "passed" for row in gain_flow_rows)
