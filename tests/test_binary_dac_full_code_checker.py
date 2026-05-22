from __future__ import annotations

from runners.simulate_evas import check_simple_binary_dac_4b


def _binary_dac_rows(*, denominator: float = 15.0, corrupt_code_at: int | None = None) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for code in range(16):
        time_s = (5.0 + 10.0 * code) * 1e-9
        observed_code = code
        if corrupt_code_at is not None and code == corrupt_code_at:
            observed_code ^= 1
        aout = 0.9 * code / denominator
        rows.append(
            {
                "time": time_s,
                "code_0": 0.9 if observed_code & 1 else 0.0,
                "code_1": 0.9 if observed_code & 2 else 0.0,
                "code_2": 0.9 if observed_code & 4 else 0.0,
                "code_3": 0.9 if observed_code & 8 else 0.0,
                "aout": aout,
            }
        )
    return rows


def test_binary_dac_checker_accepts_all_16_ideal_codes() -> None:
    ok, note = check_simple_binary_dac_4b(_binary_dac_rows())

    assert ok, note
    assert "observed_codes=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15" in note
    assert "code_mismatches=0" in note


def test_binary_dac_checker_rejects_denominator_16_endpoint_bug() -> None:
    ok, note = check_simple_binary_dac_4b(_binary_dac_rows(denominator=16.0))

    assert not ok
    assert "full_scale_ok=False" in note


def test_binary_dac_checker_rejects_code_stimulus_mismatch() -> None:
    ok, note = check_simple_binary_dac_4b(_binary_dac_rows(corrupt_code_at=9))

    assert not ok
    assert "code_mismatches=1" in note
