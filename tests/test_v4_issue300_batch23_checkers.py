from __future__ import annotations

from runners.checkers.v4.task_222 import CHECKER as CHECKER_222
from runners.checkers.v4.task_224 import CHECKER as CHECKER_224


def test_trim_ctrl_rejects_constant_zero_stimulus() -> None:
    rows = [
        {
            "time": index * 10e-12,
            "ain": 0.0,
            **{f"dout{bit}": 0.0 for bit in range(5)},
        }
        for index in range(300)
    ]

    ok, note = CHECKER_222(rows)

    assert not ok
    assert note.startswith("insufficient_excitation trim_ctrl_5bit")


def test_coarse_quantizer_rejects_constant_zero_stimulus() -> None:
    rows = [
        {
            "time": index * 10e-12,
            "vin": 0.0,
            "d0": 0.0,
            "d1": 0.0,
            "d2": 1.0,
            "vres": 0.0,
        }
        for index in range(300)
    ]

    ok, note = CHECKER_224(rows)

    assert not ok
    assert note.startswith("insufficient_excitation coarse_qtz_3bit_residue")
