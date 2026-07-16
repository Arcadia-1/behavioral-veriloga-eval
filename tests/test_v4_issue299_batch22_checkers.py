from __future__ import annotations

import pytest

from runners.checkers.v4.task_211 import CHECKER as CHECKER_211
from runners.checkers.v4.task_212 import CHECKER as CHECKER_212
from runners.checkers.v4.task_215 import CHECKER as CHECKER_215
from runners.checkers.v4.task_219 import CHECKER as CHECKER_219


@pytest.mark.parametrize(
    ("checker", "row"),
    [
        (CHECKER_211, {"out": -2.165625, **{f"d{i}": 0.0 for i in range(1, 6)}}),
        (CHECKER_212, {"vout": 0.0, "gnd": 0.0, **{f"d{i}": 0.0 for i in range(4)}}),
        (CHECKER_215, {"vout": -0.9, "gnd": 0.0, **{f"d{i}": 0.0 for i in range(8)}}),
        (
            CHECKER_219,
            {"vdd": 0.0, "gnd": 0.0, "b1": 0.0, "b0": 0.0, "t0": 0.0, "t1": 0.0, "t2": 0.0},
        ),
    ],
)
def test_zeroed_stimulus_is_rejected_as_insufficient_excitation(checker, row) -> None:
    rows = [{"time": index * 10e-12, **row} for index in range(300)]

    ok, note = checker(rows)

    assert not ok
    assert note == "insufficient_logic_excitation=1"
