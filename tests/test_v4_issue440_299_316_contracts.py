from __future__ import annotations

import math

from runners.checkers.v4.task_299 import CHECKER as CHECKER_299
from runners.checkers.v4.task_300 import CHECKER as CHECKER_300


def _integrated_phase_rows_299(*, hardcoded_frequency: float | None = None) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    phase = 0.0
    previous_t = 0.0
    previous_vin = 0.05
    for index in range(401):
        t = index * 4.0e-9
        if t < 0.35e-6:
            vin = 0.05
        elif t < 0.85e-6:
            vin = 0.20
        else:
            vin = 0.55
        if index:
            if hardcoded_frequency is not None:
                freq = hardcoded_frequency
            else:
                freq = 0.5 * (
                    20.0e6 + 40.0e6 * previous_vin
                    + 20.0e6 + 40.0e6 * vin
                )
            phase = (phase + freq * (t - previous_t)) % 1.0
        rows.append(
            {
                "time": t,
                "vin": vin,
                "out": 0.9 * math.sin(2.0 * math.pi * phase),
                "metric": 0.9 * phase,
            }
        )
        previous_t = t
        previous_vin = vin
    return rows


def _integrated_phase_rows_300(*, cover_clamps: bool) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    phase = 0.0
    previous_t = 0.0
    previous_vinp = 0.65 if not cover_clamps else 0.25
    previous_vinm = 0.35 if not cover_clamps else 0.55

    def _freq(vinp: float, vinm: float) -> float:
        raw_freq = 20.0e6 + 160.0e6 * (vinp - vinm)
        return min(80.0e6, max(5.0e6, raw_freq))

    for index in range(401):
        t = index * 4.0e-9
        if not cover_clamps:
            vinp, vinm = 0.65, 0.35
        elif t < 0.45e-6:
            vinp, vinm = 0.25, 0.55
        elif t < 0.95e-6:
            vinp, vinm = 0.65, 0.35
        else:
            vinp, vinm = 0.85, 0.35
        if index:
            freq = 0.5 * (_freq(previous_vinp, previous_vinm) + _freq(vinp, vinm))
            phase = (phase + freq * (t - previous_t)) % 1.0
        rows.append(
            {
                "time": t,
                "vinp": vinp,
                "vinm": vinm,
                "outp": 0.45 + 0.4 * math.sin(2.0 * math.pi * phase),
                "outm": 0.45 - 0.4 * math.sin(2.0 * math.pi * phase),
                "metric": 0.9 * phase,
            }
        )
        previous_t = t
        previous_vinp = vinp
        previous_vinm = vinm
    return rows


def test_299_varied_vin_rejects_hardcoded_28mhz_waveform() -> None:
    ok, note = CHECKER_299(_integrated_phase_rows_299(hardcoded_frequency=28.0e6))
    assert not ok, note


def test_299_varied_vin_accepts_integrated_center_plus_gain_waveform() -> None:
    ok, note = CHECKER_299(_integrated_phase_rows_299())
    assert ok, note


def test_300_requires_lower_and_upper_clamp_coverage() -> None:
    ok, note = CHECKER_300(_integrated_phase_rows_300(cover_clamps=False))
    assert not ok
    assert "insufficient_clamp_coverage" in note


def test_300_accepts_waveform_covering_both_frequency_clamps() -> None:
    ok, note = CHECKER_300(_integrated_phase_rows_300(cover_clamps=True))
    assert ok, note
    assert "lower_clamp_exercised" in note
    assert "upper_clamp_exercised" in note
