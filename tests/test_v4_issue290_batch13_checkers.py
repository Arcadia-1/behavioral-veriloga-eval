from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))


def test_v4_124_rejects_zero_only_tanh_excitation() -> None:
    from checkers.v4.registry import load_checker

    checker = load_checker("v4_124_smooth_comparator_tanh")
    assert checker is not None
    rows = [
        {"time": index * 1e-12, "sigin": 0.0, "sigref": 0.0, "sigout": 0.45}
        for index in range(100)
    ]

    passed, detail = checker(rows)
    assert not passed
    assert "insufficient_tanh_regions" in detail


def test_v4_126_rejects_zero_only_absolute_value_excitation() -> None:
    from checkers.v4.registry import load_checker

    checker = load_checker("v4_126_absolute_value")
    assert checker is not None
    rows = [
        {"time": index * 1e-12, "sigin": 0.0, "sigout": 0.0}
        for index in range(300)
    ]

    passed, detail = checker(rows)
    assert not passed
    assert "insufficient_absolute_value_polarity" in detail


def test_v4_129_rejects_zero_only_polynomial_vcvs_excitation() -> None:
    from checkers.v4.registry import load_checker

    checker = load_checker("v4_129_polynomial_differential_vcvs")
    assert checker is not None
    rows = [
        {"time": index * 1e-12, "inp": 0.0, "inn": 0.0, "outp": 0.5, "outn": 0.5}
        for index in range(100)
    ]

    passed, detail = checker(rows)
    assert not passed
    assert "insufficient_vcvs_polarity" in detail
