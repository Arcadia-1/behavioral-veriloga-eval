from __future__ import annotations

import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

from score import build_model_results  # noqa: E402
from vabench_policy import should_count_as, validate_or_raise, validation_errors  # noqa: E402


def test_evidence_only_is_excluded_from_model_and_bugfix_counts() -> None:
    meta = {
        "id": "fixed_only_bugfix",
        "family": "bugfix",
        "release_form": "evidence-only",
        "counts": {"model_capability": False, "benchmark_coverage": False, "bugfix_claim": False},
    }

    assert not validation_errors(meta)
    assert not should_count_as(meta, "model_capability")
    assert not should_count_as(meta, "benchmark_coverage")
    assert not should_count_as(meta, "bugfix_claim")


def test_conformance_asset_is_rejected_under_tasks() -> None:
    meta = {
        "id": "timer0_transition_startup",
        "asset_type": "evas_spectre_conformance",
        "family": "conformance",
    }

    with pytest.raises(ValueError, match="conformance assets must live outside"):
        validate_or_raise(meta, ROOT / "tasks" / "conformance" / "timer0_transition_startup")


def test_true_bugfix_requires_buggy_fixed_gold_pair(tmp_path: Path) -> None:
    task_dir = tmp_path / "tasks" / "bugfix" / "voltage" / "demo"
    gold = task_dir / "gold"
    gold.mkdir(parents=True)
    (gold / "dut_fixed.va").write_text("module dut_fixed; endmodule\n", encoding="utf-8")
    meta = {
        "id": "demo",
        "family": "bugfix",
        "release_form": "true-bugfix",
        "provenance_status": "reconstructed_badcase",
        "badcase_origin": "reconstructed",
        "counts": {"model_capability": True, "benchmark_coverage": True, "bugfix_claim": True},
    }

    assert any("buggy/fixed gold source evidence" in error for error in validation_errors(meta, task_dir))

    (gold / "dut_buggy.va").write_text("module dut_buggy; endmodule\n", encoding="utf-8")

    assert not validation_errors(meta, task_dir)


def test_model_results_exclude_non_countable_rows_from_denominator() -> None:
    countable = {
        "task_id": "normal_task",
        "family": "spec-to-va",
        "scores": {"dut_compile": 1.0, "tb_compile": 1.0, "sim_correct": 1.0},
        "required_axes": ["dut_compile", "tb_compile", "sim_correct"],
    }
    evidence_only = {
        "task_id": "fixed_only_bugfix",
        "family": "bugfix",
        "release_form": "evidence-only",
        "counts": {"model_capability": False, "benchmark_coverage": False, "bugfix_claim": False},
        "scores": {"dut_compile": 1.0, "tb_compile": 1.0, "sim_correct": 1.0},
        "required_axes": ["dut_compile", "tb_compile", "sim_correct"],
    }

    summary = build_model_results("demo-model", [countable, evidence_only], temperature=0.0, top_p=1.0)

    assert summary["input_results"] == 2
    assert summary["excluded_from_model_capability"] == 1
    assert summary["total_tasks"] == 1
    assert summary["pass_count"] == 1
