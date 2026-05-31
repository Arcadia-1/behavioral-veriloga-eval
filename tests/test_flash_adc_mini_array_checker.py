from __future__ import annotations

from runners.simulate_evas import check_release_flash_adc_mini_array


def _flash_rows(*, corrupt_cmp: bool = False, direct_encoder_only: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for code in range(8):
        edge_t = (5.0 + 10.0 * code) * 1e-9
        vin = (code + 0.5) * 0.9 / 8.0
        cmp_bits = [1 if idx < code else 0 for idx in range(7)]
        if corrupt_cmp and code == 5:
            cmp_bits[6] = 1
        if direct_encoder_only:
            cmp_bits = [0] * 7

        dout0 = 0.9 if code & 1 else 0.0
        dout1 = 0.9 if code & 2 else 0.0
        dout2 = 0.9 if code & 4 else 0.0

        base = {
            "vin": vin,
            "dout0": dout0,
            "dout1": dout1,
            "dout2": dout2,
        }
        for idx, bit in enumerate(cmp_bits):
            base[f"cmp{idx}"] = 0.9 if bit else 0.0

        rows.append({"time": edge_t - 0.1e-9, "clk": 0.0, **base})
        rows.append({"time": edge_t, "clk": 0.9, **base})
        rows.append({"time": edge_t + 0.6e-9, "clk": 0.9, **base})
        rows.append({"time": edge_t + 4.0e-9, "clk": 0.0, **base})
    return sorted(rows, key=lambda row: row["time"])


def test_flash_mini_array_checker_accepts_comparator_ladder_and_encoder() -> None:
    ok, note = check_release_flash_adc_mini_array(_flash_rows())

    assert ok, note
    assert "observed_codes=0,1,2,3,4,5,6,7" in note
    assert "comparator_mismatches=0" in note


def test_flash_mini_array_checker_rejects_direct_encoder_without_comparators() -> None:
    ok, note = check_release_flash_adc_mini_array(_flash_rows(direct_encoder_only=True))

    assert not ok
    assert "comparator_mismatches=" in note


def test_flash_mini_array_checker_rejects_non_thermometer_comparator_vector() -> None:
    ok, note = check_release_flash_adc_mini_array(_flash_rows(corrupt_cmp=True))

    assert not ok
    assert "thermometer_errors=1" in note
