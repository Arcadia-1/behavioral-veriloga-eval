from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

import report_vabench_model_baseline_quality_audit as audit  # noqa: E402


def make_row(
    task: str,
    *,
    category: str,
    difficulty: str,
    form: str,
    axis: str,
    family: str,
    passed: bool,
) -> dict[str, object]:
    return {
        "task_id": task.replace(":", "_"),
        "release_task_id": task,
        "release_entry_id": task.split(":")[0],
        "category": category,
        "difficulty": difficulty,
        "form": form,
        "triage_axis": axis,
        "root_cause_family": family,
        "dual_pass": passed,
        "evidence": family,
    }


def test_quality_audit_compares_models_and_flags_difficulty_candidates() -> None:
    first = {
        "rows": [
            make_row("d1_basic:dut", category="Comparator", difficulty="D1", form="dut", axis="model_behavior", family="decision_threshold_behavior", passed=False),
            make_row("d2_mid:dut", category="Comparator", difficulty="D2", form="dut", axis="pass", family="strict_dual_pass", passed=True),
            make_row("d3_flow:e2e", category="Converter", difficulty="D3", form="e2e", axis="pass", family="strict_dual_pass", passed=True),
            make_row("hard_ref:e2e", category="Reference", difficulty="D2", form="e2e", axis="model_behavior", family="reference_power_behavior", passed=False),
        ]
    }
    second = {
        "rows": [
            make_row("d1_basic:dut", category="Comparator", difficulty="D1", form="dut", axis="model_behavior", family="decision_threshold_behavior", passed=False),
            make_row("d2_mid:dut", category="Comparator", difficulty="D2", form="dut", axis="pass", family="strict_dual_pass", passed=True),
            make_row("d3_flow:e2e", category="Converter", difficulty="D3", form="e2e", axis="pass", family="strict_dual_pass", passed=True),
            make_row("hard_ref:e2e", category="Reference", difficulty="D2", form="e2e", axis="generation", family="incomplete_generation", passed=False),
        ]
    }

    report = audit.build_report({"first": first, "second": second}, {"first": Path("first.json"), "second": Path("second.json")})

    assert report["pass_overlap"]["both_pass"] == 2
    assert report["pass_overlap"]["both_fail"] == 2
    flagged = {item["model"]: set(item["flags"]) for item in report["difficulty_audit"]}
    assert "D1_not_easier_than_D2" in flagged["first"]
    assert "D3_not_harder_than_D2" in flagged["second"]
    candidates = {item["release_task_id"]: item["reason"] for item in report["difficulty_relabel_candidates"]}
    assert "d1_basic:dut" in candidates
    assert "d3_flow:e2e" in candidates
    reference = next(item for item in report["category_audit"] if item["category"] == "Reference")
    assert reference["risk_label"] == "zero_common_pass"


def test_quality_audit_score_slices_separate_incomplete_rows() -> None:
    report = {
        "rows": [
            make_row("pass:dut", category="A", difficulty="D1", form="dut", axis="pass", family="strict_dual_pass", passed=True),
            make_row("behavior:dut", category="A", difficulty="D1", form="dut", axis="model_behavior", family="other_behavior_failure", passed=False),
            make_row("incomplete:dut", category="A", difficulty="D1", form="dut", axis="generation", family="incomplete_generation", passed=False),
        ]
    }

    summary = audit.model_summary("demo", report)
    slices = {item["slice"]: item for item in summary["score_slices"]}

    assert slices["full_strict"]["total_rows"] == 3
    assert slices["valid_candidate"]["total_rows"] == 2
    assert slices["behavior_ready"]["total_rows"] == 2
    assert slices["behavior_ready"]["strict_dual_pass_rate_pct"] == 50.0
