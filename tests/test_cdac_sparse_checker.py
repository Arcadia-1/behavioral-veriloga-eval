from __future__ import annotations

from runners.simulate_evas import (
    _RELEASE_CDAC_CAL_SEQUENCE,
    _RELEASE_CDAC_CODE_SEQUENCE,
    check_release_cdac_feedback_dac,
)


def _cdac_rows(*, low_nibble_only: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for idx, (code, cal) in enumerate(zip(_RELEASE_CDAC_CODE_SEQUENCE, _RELEASE_CDAC_CAL_SEQUENCE)):
        edge_t = 5e-9 + 4e-9 * idx
        sampled_code = code & 0xF if low_nibble_only else code
        diff = 0.6 * (((sampled_code + 32 * cal) / 1023.0) - 0.5)
        vdac_p = 0.45 + 0.5 * diff
        vdac_n = 0.45 - 0.5 * diff
        cal0 = 0.9 if cal & 1 else 0.0
        cal1 = 0.9 if cal & 2 else 0.0

        rows.append(
            {
                "time": edge_t - 0.02e-9,
                "clk": 0.0,
                "cal0": cal0,
                "cal1": cal1,
                "vdac_p": vdac_p,
                "vdac_n": vdac_n,
            }
        )
        rows.append(
            {
                "time": edge_t,
                "clk": 0.9,
                "cal0": cal0,
                "cal1": cal1,
                "vdac_p": vdac_p,
                "vdac_n": vdac_n,
            }
        )
        rows.append(
            {
                "time": edge_t + 0.25e-9,
                "clk": 0.9,
                "cal0": cal0,
                "cal1": cal1,
                "vdac_p": vdac_p,
                "vdac_n": vdac_n,
            }
        )
        rows.append(
            {
                "time": edge_t + 1e-9,
                "clk": 0.0,
                "cal0": cal0,
                "cal1": cal1,
                "vdac_p": vdac_p,
                "vdac_n": vdac_n,
            }
        )
    return sorted(rows, key=lambda row: row["time"])


def test_cdac_sparse_checker_accepts_sparse_10bit_sequence() -> None:
    ok, note = check_release_cdac_feedback_dac(_cdac_rows())

    assert ok, note
    assert "covered_states=16" in note


def test_cdac_sparse_checker_rejects_low_nibble_only_behavior() -> None:
    ok, note = check_release_cdac_feedback_dac(_cdac_rows(low_nibble_only=True))

    assert not ok
    assert "mismatches=" in note
