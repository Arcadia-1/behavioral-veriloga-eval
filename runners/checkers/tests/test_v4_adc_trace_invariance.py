from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from runners.checkers.v4.task_050 import check_v3_498_dc_aware_adc3bit


def _adc_rows(*, points: int, round_to_nearest: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for index in range(points):
        vin = -0.20 + 1.40 * index / (points - 1)
        clipped = min(1.0, max(0.0, vin))
        scaled = 8.0 * clipped + (0.5 if round_to_nearest else 0.0)
        code = max(0, min(7, int(scaled)))
        rows.append(
            {
                "time": index * 0.2e-9,
                "vin": vin,
                "d2": 0.9 if code & 4 else 0.0,
                "d1": 0.9 if code & 2 else 0.0,
                "d0": 0.9 if code & 1 else 0.0,
            }
        )
    return rows


def test_adc_quantization_is_invariant_to_dc_sweep_density() -> None:
    dense_ok, dense_note = check_v3_498_dc_aware_adc3bit(_adc_rows(points=1401))
    sparse_ok, sparse_note = check_v3_498_dc_aware_adc3bit(_adc_rows(points=69))

    assert dense_ok, dense_note
    assert sparse_ok, sparse_note


def test_adc_round_to_nearest_mutation_remains_rejected_on_sparse_sweep() -> None:
    ok, note = check_v3_498_dc_aware_adc3bit(
        _adc_rows(points=69, round_to_nearest=True)
    )

    assert not ok, note
    assert "property_id=P_3BIT_QUANTIZATION" in note


def test_adc_quantization_samples_settled_plateaus_not_ramp_breakpoints() -> None:
    rows: list[dict[str, float]] = []
    time_s = 0.0
    previous_code = 0
    for code in range(8):
        vin = (code + 0.5) / 8.0
        for _ in range(3):
            rows.append(
                {
                    "time": time_s,
                    "vin": vin,
                    "d2": 0.9 if code & 4 else 0.0,
                    "d1": 0.9 if code & 2 else 0.0,
                    "d0": 0.9 if code & 1 else 0.0,
                }
            )
            time_s += 0.10e-9
        if code == 7:
            continue
        next_vin = (code + 1.5) / 8.0
        for fraction in (0.33, 0.66):
            vin_mid = vin + fraction * (next_vin - vin)
            rows.append(
                {
                    "time": time_s,
                    "vin": vin_mid,
                    # During the declared input transition, the output may
                    # still be the previous settled code.
                    "d2": 0.9 if previous_code & 4 else 0.0,
                    "d1": 0.9 if previous_code & 2 else 0.0,
                    "d0": 0.9 if previous_code & 1 else 0.0,
                }
            )
            time_s += 0.05e-9
        previous_code = code

    ok, note = check_v3_498_dc_aware_adc3bit(rows)

    assert ok, note
