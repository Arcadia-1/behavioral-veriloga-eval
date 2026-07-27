from __future__ import annotations

import csv
from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

import simulate_evas
from checkers.v4.registry import load_checker
from checkers.v4.task_312 import check_v4_312_interleaved_adc_skew_monitor


EXPERIMENT = (
    ROOT.parents[1]
    / "_experiment_runs"
    / "r52-deepseek-family001-400-threeform-threearm-20260726"
)

ARCHIVED_CASES = {
    "v4_231_decision_router_logic": (
        EXPERIMENT
        / "spectre-audit-pass/cells/v4-731-G2-r00-agentic"
        / "493a4e5b9661ab3cc4185c78bd00a185db9b76db6bbffd22385fe913e99e3590/cases"
    ),
    "v4_254_bias_trim_affine_mapper": (
        EXPERIMENT
        / "spectre-audit-pass/cells/v4-754-G0-r00-oneshot"
        / "09b0f8700f3dbdbff7398519956804a9f960583c2f28ff06526d2984c671516f/cases"
    ),
    "v4_277_calibration_bit_select_flag": (
        EXPERIMENT
        / "spectre-audit-pass/cells/v4-777-G2-r00-agentic"
        / "0f2d2bd2a8042b06d81d5da6620e4ee4b6b4f1b785b553945efeedadc44dde85/cases"
    ),
    "v4_279_explicit_sar_slice_router": (
        EXPERIMENT
        / "spectre-audit-pass/cells/v4-779-G2-r00-noevas"
        / "f1c11fa66fb5897ad68d492b0a1bdbb12a68c2a98865b1c308e854068e970c22/cases"
    ),
    "v4_312_interleaved_adc_skew_monitor": (
        EXPERIMENT
        / "prelaunch-targeted-20260727/classic-spectre-maxstep40-work-retry/cells"
        / "v4-812-G2-r00-agentic"
        / "13ae3adcd7901d1285c854ad9fe5b804ba6c1ede445f0b14f480a32633832d74/cases"
    ),
}


def _load_rows(csv_path: Path) -> list[dict[str, float]]:
    if not csv_path.is_file():
        pytest.skip(f"archived Spectre CSV is not available: {csv_path}")
    with csv_path.open(newline="", encoding="utf-8") as handle:
        return [{name: float(value) for name, value in row.items()} for row in csv.DictReader(handle)]


@pytest.mark.parametrize("checker_id,cases_dir", ARCHIVED_CASES.items())
def test_current35_archived_spectre_reference_passes_and_mutations_fail(
    checker_id: str,
    cases_dir: Path,
) -> None:
    checker = load_checker(checker_id)
    assert checker is not None
    reference_ok, reference_note = checker(_load_rows(cases_dir / "reference/tran_spectre.csv"))

    assert reference_ok, reference_note

    mutation_dirs = sorted(path for path in cases_dir.iterdir() if path.name.startswith("neg_"))
    assert mutation_dirs
    for mutation_dir in mutation_dirs:
        mutation_ok, mutation_note = checker(_load_rows(mutation_dir / "tran_spectre.csv"))
        assert not mutation_ok, f"{checker_id} unexpectedly accepted {mutation_dir.name}: {mutation_note}"


def test_task312_archived_trace_density_controls_low_skew_coverage() -> None:
    rows = _load_rows(
        ARCHIVED_CASES["v4_312_interleaved_adc_skew_monitor"]
        / "reference/tran_spectre.csv"
    )

    dense_ok, dense_note = check_v4_312_interleaved_adc_skew_monitor(rows)
    sparse_rows = rows[::2]
    if sparse_rows[-1]["time"] != rows[-1]["time"]:
        sparse_rows.append(rows[-1])
    sparse_ok, sparse_note = check_v4_312_interleaved_adc_skew_monitor(sparse_rows)

    assert dense_ok, dense_note
    assert "checked=21" in dense_note
    assert "low_skew=True" in dense_note
    assert not sparse_ok
    assert "checked=17" in sparse_note
    assert "low_skew=False" in sparse_note


def test_task312_required_trace_maxstep_contract_rewrites_tran_line(tmp_path: Path) -> None:
    tb = tmp_path / "tb.scs"
    tb.write_text("simulator lang=spectre\ntran tran stop=45n\n", encoding="utf-8")

    maxstep_s = simulate_evas.required_trace_maxstep_for_checker(
        "v4_312_interleaved_adc_skew_monitor"
    )
    changed = simulate_evas.apply_required_trace_maxstep(tb, maxstep_s)

    assert maxstep_s == pytest.approx(40e-12)
    assert changed
    assert "tran tran stop=45n maxstep=40p" in tb.read_text(encoding="utf-8")

