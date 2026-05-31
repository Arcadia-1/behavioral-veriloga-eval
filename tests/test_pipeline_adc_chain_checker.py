from __future__ import annotations

from simulate_evas import check_release_pipeline_adc_chain


def _bits(code: int, width: int) -> list[float]:
    return [0.9 if (code >> bit) & 1 else 0.0 for bit in reversed(range(width))]


def _expected(vin: float) -> tuple[int, int, int, float, float]:
    def stage_code(value: float) -> int:
        if value < 0.9 * 0.25:
            return 0
        if value < 0.9 * 0.50:
            return 1
        if value < 0.9 * 0.75:
            return 2
        return 3

    s1 = stage_code(vin)
    res1 = 0.45 + 4.0 * (vin - (s1 + 0.5) * 0.9 / 4.0)
    res1 = min(0.9, max(0.0, res1))
    s2 = stage_code(res1)
    res2 = 0.45 + 4.0 * (res1 - (s2 + 0.5) * 0.9 / 4.0)
    res2 = min(0.9, max(0.0, res2))
    return s1, s2, 4 * s1 + s2, res1, res2


def _valid_rows() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    lsb = 0.9 / 16.0
    for code in range(16):
        frac = 0.25 if code % 2 == 0 else 0.75
        vin = (code + frac) * lsb
        s1, s2, final, res1, res2 = _expected(vin)
        t0 = code * 10e-9
        rows.append(
            {
                "time": t0,
                "vin": vin,
                "clk": 0.0,
                "res1": res1,
                "res2": res2,
                "s1b1": _bits(s1, 2)[0],
                "s1b0": _bits(s1, 2)[1],
                "s2b1": _bits(s2, 2)[0],
                "s2b0": _bits(s2, 2)[1],
                "dout3": _bits(final, 4)[0],
                "dout2": _bits(final, 4)[1],
                "dout1": _bits(final, 4)[2],
                "dout0": _bits(final, 4)[3],
            }
        )
        rows.append({**rows[-1], "time": t0 + 1.0e-12, "clk": 0.9})
        rows.append({**rows[-1], "time": t0 + 1.0e-9})
        rows.append({**rows[-1], "time": t0 + 4.0e-9, "clk": 0.0})
    return rows


def test_pipeline_adc_chain_checker_accepts_complete_two_stage_flow() -> None:
    ok, note = check_release_pipeline_adc_chain(_valid_rows())
    assert ok, note
    assert "observed_codes=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15" in note


def test_pipeline_adc_chain_checker_rejects_final_code_not_from_stage_concat() -> None:
    rows = _valid_rows()
    for row in rows:
        if 50.5e-9 <= row["time"] <= 51.5e-9:
            row["dout0"] = 0.0 if row["dout0"] > 0.45 else 0.9
            break
    ok, note = check_release_pipeline_adc_chain(rows)
    assert not ok
    assert "final_concat_mismatches=" in note


def test_pipeline_adc_chain_checker_rejects_bad_residue() -> None:
    rows = _valid_rows()
    for row in rows:
        if 80.5e-9 <= row["time"] <= 81.5e-9:
            row["res1"] += 0.2
            break
    ok, note = check_release_pipeline_adc_chain(rows)
    assert not ok
    assert "residue_mismatches=" in note
