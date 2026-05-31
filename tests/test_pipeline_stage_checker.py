from __future__ import annotations

from runners.simulate_evas import check_pipeline_stage


def _expected(vin: float) -> tuple[int, int, float]:
    vin_rel = vin - 0.45
    if vin_rel > 0.9 / 4.0:
        return 1, 0, 0.45 + 2.0 * vin_rel - 0.9 / 2.0
    if vin_rel < -0.9 / 4.0:
        return 0, 0, 0.45 + 2.0 * vin_rel + 0.9 / 2.0
    return 0, 1, 0.45 + 2.0 * vin_rel


def _pipeline_rows(*, wrong_residue: bool = False, wrong_bits: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    cases = [(11e-9, 0.72), (111e-9, 0.45), (211e-9, 0.18)]
    for edge_t, vin in cases:
        d1, d0, vres = _expected(vin)
        if wrong_residue and vin != 0.45:
            vres = 0.45 + 2.0 * (vin - 0.45)
        if wrong_bits and vin == 0.72:
            d1, d0 = 0, 1

        base = {
            "phi1": 0.0,
            "vin": vin,
            "vres": vres,
            "d1": 0.9 if d1 else 0.0,
            "d0": 0.9 if d0 else 0.0,
        }
        rows.append({"time": edge_t - 0.2e-9, "phi2": 0.0, **base})
        rows.append({"time": edge_t, "phi2": 0.9, **base})
        rows.append({"time": edge_t + 1.0e-9, "phi2": 0.9, **base})
        rows.append({"time": edge_t + 5.0e-9, "phi2": 0.0, **base})
    return sorted(rows, key=lambda row: row["time"])


def test_pipeline_stage_checker_accepts_all_three_mdac_regions() -> None:
    ok, note = check_pipeline_stage(_pipeline_rows())

    assert ok, note
    assert "regions=upper:1,middle:1,lower:1" in note
    assert "residue_mismatches=0" in note


def test_pipeline_stage_checker_rejects_missing_subdac_residue_correction() -> None:
    ok, note = check_pipeline_stage(_pipeline_rows(wrong_residue=True))

    assert not ok
    assert "residue_mismatches=2" in note


def test_pipeline_stage_checker_rejects_wrong_subadc_decision_bits() -> None:
    ok, note = check_pipeline_stage(_pipeline_rows(wrong_bits=True))

    assert not ok
    assert "bit_mismatches=1" in note
