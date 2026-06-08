from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

from run_gold_dual_suite import compare_waveforms  # noqa: E402


def write_csv(path: Path, values: list[float]) -> None:
    rows = ["time,vout"]
    rows.extend(f"{idx * 1e-9},{value}" for idx, value in enumerate(values))
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")


def signal_metrics(result: dict, signal: str = "vout") -> dict:
    return result["per_signal"][signal]


def test_digital_one_sample_edge_offset_is_reported_as_alignment_window(tmp_path: Path) -> None:
    reference = [0.0 if idx < 50 else 1.0 for idx in range(101)]
    candidate = [0.0 if idx < 51 else 1.0 for idx in range(101)]
    ref_csv = tmp_path / "ref.csv"
    candidate_csv = tmp_path / "candidate.csv"
    write_csv(ref_csv, reference)
    write_csv(candidate_csv, candidate)

    result = compare_waveforms("generic_task", candidate_csv, ref_csv, sample_n=101)
    metrics = signal_metrics(result)

    assert metrics["kind"] == "digital"
    assert metrics["raw_mismatch_ratio"] > 0.0
    assert metrics["mismatch_ratio"] == 0.0
    assert metrics["sample_alignment_discounted"] is True
    assert result["raw_max_relative_rms_error"] > result["max_relative_rms_error"]


def test_digital_stable_region_mismatch_is_not_discounted(tmp_path: Path) -> None:
    reference = [0.0 if idx < 50 else 1.0 for idx in range(101)]
    candidate = list(reference)
    for idx in range(20, 81):
        candidate[idx] = 1.0 - candidate[idx]
    ref_csv = tmp_path / "ref.csv"
    candidate_csv = tmp_path / "candidate.csv"
    write_csv(ref_csv, reference)
    write_csv(candidate_csv, candidate)

    result = compare_waveforms("generic_task", candidate_csv, ref_csv, sample_n=101)
    metrics = signal_metrics(result)

    assert metrics["kind"] == "digital"
    assert metrics["sample_alignment_discounted"] is False
    assert metrics["mismatch_ratio"] == metrics["raw_mismatch_ratio"]
    assert metrics["mismatch_ratio"] > 0.5


def test_analog_local_activity_sample_error_keeps_raw_metrics_but_uses_stable_region(tmp_path: Path) -> None:
    reference = [idx / 100.0 for idx in range(101)]
    candidate = list(reference)
    candidate[50] = reference[70]
    ref_csv = tmp_path / "ref.csv"
    candidate_csv = tmp_path / "candidate.csv"
    write_csv(ref_csv, reference)
    write_csv(candidate_csv, candidate)

    result = compare_waveforms("generic_task", candidate_csv, ref_csv, sample_n=101)
    metrics = signal_metrics(result)

    assert metrics["kind"] == "analog"
    assert metrics["raw_nrmse"] > 0.0
    assert metrics["nrmse"] == 0.0
    assert metrics["sample_alignment_discounted"] is True
    assert metrics["raw_max_abs_v"] > metrics["max_abs_v"]


def test_analog_persistent_offset_is_not_discounted(tmp_path: Path) -> None:
    reference = [idx / 100.0 for idx in range(101)]
    candidate = [value + 0.05 for value in reference]
    ref_csv = tmp_path / "ref.csv"
    candidate_csv = tmp_path / "candidate.csv"
    write_csv(ref_csv, reference)
    write_csv(candidate_csv, candidate)

    result = compare_waveforms("generic_task", candidate_csv, ref_csv, sample_n=101)
    metrics = signal_metrics(result)

    assert metrics["kind"] == "analog"
    assert metrics["sample_alignment_discounted"] is False
    assert metrics["nrmse"] == metrics["raw_nrmse"]
    assert metrics["max_abs_v"] == metrics["raw_max_abs_v"]


def test_two_level_midrail_residue_is_analog_not_digital(tmp_path: Path) -> None:
    reference = [0.225 if idx < 50 else 0.675 for idx in range(101)]
    candidate = list(reference)
    candidate[50] = 0.450001
    ref_csv = tmp_path / "ref.csv"
    candidate_csv = tmp_path / "candidate.csv"
    write_csv(ref_csv, reference)
    write_csv(candidate_csv, candidate)

    result = compare_waveforms("generic_task", candidate_csv, ref_csv, sample_n=101)
    metrics = signal_metrics(result)

    assert metrics["kind"] == "analog"
    assert "mismatch_ratio" not in metrics
    assert metrics["max_abs_v"] < 1.0
