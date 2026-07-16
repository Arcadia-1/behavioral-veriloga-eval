from __future__ import annotations

import csv
import importlib
import os
from pathlib import Path

import pytest


@pytest.mark.parametrize("family_id", range(301, 311))
def test_checker_acceptance_is_invariant_to_uniform_time_transform(family_id: int) -> None:
    """Replay a gold EVAS trace after t' = shift + scale*t.

    The smoke runner keeps raw traces outside the repository.  Set
    ``V4_B31_TRACE_ROOT`` to that run directory to enable this integration
    check; the unit suite remains self-contained when no simulator output is
    available.
    """
    root = os.environ.get("V4_B31_TRACE_ROOT")
    if not root:
        pytest.skip("set V4_B31_TRACE_ROOT to an EVAS smoke work root")
    path = Path(root) / f"v4-{500 + family_id}" / "correct" / "output" / "tran.csv"
    if not path.is_file():
        pytest.skip(f"missing EVAS trace: {path}")
    with path.open(newline="") as handle:
        rows = [{key: float(value) for key, value in row.items()} for row in csv.DictReader(handle)]
    checker = importlib.import_module(f"runners.checkers.v4.task_{family_id:03d}").CHECKER
    original_ok, _ = checker(rows)
    transformed = [dict(row, time=17.0 + 3.25 * row["time"]) for row in rows]
    transformed_ok, note = checker(transformed)
    assert original_ok, "the supplied gold trace must pass before the metamorphic replay"
    assert transformed_ok, note
