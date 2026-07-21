from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import pytest

from runners.checkers.v4.task_081 import CHECKER, STREAMING_CHECKER


_DT_S = 0.5e-9
_STOP_S = 8.5e-6
_REF_FREQ_HZ = 50.0e6
_REPO_ROOT = Path(__file__).resolve().parents[3]
_TASK_ROOT = (
    _REPO_ROOT
    / "benchmark-vabench-release-v4"
    / "provenance"
    / "dut-base-v3-exact-five-hash-bound-v2"
    / "081-adpll-ratio-hop-timer"
)


def _requested_ratio(time_s: float) -> float:
    if time_s < 2.0e-6:
        return 4.0
    if time_s < 5.2e-6:
        return 6.0
    if time_s < 6.02e-6:
        return 3.49
    if time_s < 6.84e-6:
        return 3.50
    if time_s < 7.66e-6:
        return 2.20
    return 13.20


def _effective_ratio(time_s: float, fault: str | None) -> int:
    if time_s < 2.0e-6:
        return 4
    if time_s < 5.2e-6:
        return 6
    if time_s < 6.02e-6:
        return 3
    if time_s < 6.84e-6:
        return 3 if fault == "round_down_at_half" else 4
    if time_s < 7.66e-6:
        return 2 if fault == "omit_low_saturation" else 3
    return 13 if fault == "omit_high_saturation" else 12


def _logic_level(phase: float) -> float:
    return 0.9 if phase % 1.0 < 0.5 else 0.0


def _rows(*, fault: str | None = None) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    ref_phase = 0.0
    vout_phase = 0.0
    steps = int(_STOP_S / _DT_S) + 1
    for index in range(steps):
        time_s = index * _DT_S
        if index:
            ref_phase += _REF_FREQ_HZ * _DT_S
            vout_phase += _effective_ratio(time_s, fault) * _REF_FREQ_HZ * _DT_S
        lock = 0.0 if 2.0e-6 <= time_s < 3.2e-6 else 0.9
        rows.append(
            {
                "time": time_s,
                "vdd": 0.9,
                "vss": 0.0,
                "ref_clk": _logic_level(ref_phase),
                "ratio_ctrl": _requested_ratio(time_s),
                "fb_clk": _logic_level(ref_phase),
                "vout": _logic_level(vout_phase),
                "vctrl_mon": 0.45,
                "lock": lock,
            }
        )
    return rows


def _write_csv(path: Path, rows: list[dict[str, float]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _stream_result(tmp_path: Path, rows: list[dict[str, float]]) -> tuple[bool, str]:
    csv_path = tmp_path / "task081.csv"
    _write_csv(csv_path, rows)
    score, notes = STREAMING_CHECKER(csv_path)
    return score == 1.0, " ".join(notes)


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _without_backend_options(deck: str) -> str:
    return "\n".join(
        line
        for line in deck.splitlines()
        if line.strip() and not line.startswith("simulatorOptions options ")
    )


def test_legal_half_up_rounding_and_override_saturation_pass_both_checkers(
    tmp_path: Path,
) -> None:
    rows = _rows()
    row_ok, row_note = CHECKER(rows)
    stream_ok, stream_note = _stream_result(tmp_path, rows)
    assert row_ok, row_note
    assert stream_ok, stream_note


def test_task_local_property_inventory_hashes_and_profile_decks_are_synchronized() -> None:
    evaluator = _TASK_ROOT / "evaluator"
    harness_path = evaluator / "harness_spec.json"
    harness = _read_json(harness_path)
    checker = _read_json(evaluator / "checker_profile.json")
    family = _read_json(evaluator / "family_spec.json")
    feedback = _read_json(evaluator / "profiles" / "feedback.json")
    score = _read_json(evaluator / "profiles" / "score.json")

    property_ids = harness["property_ids"]
    assert property_ids == checker["trace_contract"]["property_ids"]
    assert property_ids == [item["id"] for item in family["properties"]]
    assert property_ids == feedback["property_ids"] == score["property_ids"]
    assert "P_RATIO_HALF_STEP_ROUNDING" in property_ids
    assert "P_RATIO_OVERRIDE_SATURATION" in property_ids

    harness_sha256 = hashlib.sha256(harness_path.read_bytes()).hexdigest()
    assert feedback["harness_spec_sha256"] == harness_sha256
    assert score["harness_spec_sha256"] == harness_sha256
    assert harness["source_contract"]["checker_profile_sha256"] == hashlib.sha256(
        (evaluator / "checker_profile.json").read_bytes()
    ).hexdigest()
    assert harness["source_contract"]["family_spec_sha256"] == hashlib.sha256(
        (evaluator / "family_spec.json").read_bytes()
    ).hexdigest()

    feedback_deck = (_TASK_ROOT / "public" / "task" / "feedback_tb.scs").read_text()
    score_deck = (evaluator / "score_tb.scs").read_text()
    assert _without_backend_options(feedback_deck) == _without_backend_options(score_deck)


@pytest.mark.parametrize(
    ("fault", "expected_diagnostic"),
    [
        ("round_down_at_half", "round_half_up_divider_ratio"),
        ("omit_low_saturation", "clamp_low_override_divider_ratio"),
        ("omit_high_saturation", "clamp_high_override_divider_ratio"),
    ],
)
def test_ratio_contract_faults_fail_both_checkers(
    tmp_path: Path,
    fault: str,
    expected_diagnostic: str,
) -> None:
    rows = _rows(fault=fault)
    row_ok, row_note = CHECKER(rows)
    stream_ok, stream_note = _stream_result(tmp_path, rows)
    assert not row_ok
    assert expected_diagnostic in row_note
    assert not stream_ok
    assert expected_diagnostic in stream_note
