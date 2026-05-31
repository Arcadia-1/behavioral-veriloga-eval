from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

import report_deepseek_error_clusters as clusters  # noqa: E402


def test_compile_cluster_local_declaration() -> None:
    row = {
        "primary_attribution": "model_veriloga_subset_failure",
        "evidence": "Parse error: Spectre-incompatible local declaration inside analog/procedural statement",
    }

    assert clusters.classify_cluster(row) == "C01"


def test_compile_cluster_unbounded_event_loop() -> None:
    row = {
        "primary_attribution": "model_veriloga_subset_failure",
        "evidence": "cmp_delay.va:unsupported_unbounded_event_loop",
    }

    assert clusters.classify_cluster(row) == "C07"


def test_behavior_cluster_code_sequence() -> None:
    row = {
        "primary_attribution": "model_behavior_failure",
        "category": "Data Converter Models",
        "evidence": "observed_codes=0,1,2 expected_codes=1,2,3 residue_mismatches=3",
    }

    assert clusters.classify_cluster(row) == "B05"


def test_generation_cluster_incomplete() -> None:
    row = {
        "primary_attribution": "model_incomplete_generation",
        "evidence": "generation_status=no_code_extracted finish_reason=length",
    }

    assert clusters.classify_cluster(row) == "G01"


def test_full_report_clusters_all_failures_once() -> None:
    data = clusters.load_json(clusters.DEFAULT_INPUT)
    report = clusters.build_report(data, clusters.DEFAULT_INPUT)

    assert report["total_rows"] == 236
    assert report["pass_rows"] == 59
    assert report["failed_rows"] == 177
    assert sum(item["count"] for item in report["cluster_summaries"]) == 177
    assert len(report["rows"]) == 177
    assert report["axis_counts"] == {"behavior": 146, "compile": 27, "generation": 4}
