from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
SOURCE = (
    ROOT
    / "benchmark-vabench-release-v4"
    / "provenance"
    / "dut-base-v3-exact-five-hash-bound-v2"
)

from runners.checkers.v4.task_397 import check_v4_baseband_offset_gain_trim_macro


def _family(prefix: str) -> Path:
    matches = list(SOURCE.glob(f"{prefix}-*"))
    assert len(matches) == 1
    return matches[0]


def test_task392_decks_do_not_alias_d0_d2_or_d1_d3_sources() -> None:
    for deck in (
        _family("392") / "evaluator" / "score_tb.scs",
        _family("392") / "public" / "task" / "feedback_tb.scs",
    ):
        text = deck.read_text(encoding="utf-8")
        assert "Vd0 (d0 0) vsource type=pwl wave=[0 0 92n 0]" not in text
        assert "Vd2 (d2 0) vsource type=pwl wave=[0 0 92n 0]" not in text
        assert "Vd1 (d1 0) vsource type=pwl wave=[0 0.9 92n 0.9]" not in text
        assert "Vd3 (d3 0) vsource type=pwl wave=[0 0.9 92n 0.9]" not in text
        assert "28.2n 0.9" in text
        assert "68.2n 0.9" in text


def test_task393_second_align_is_mid_frame_not_natural_wrap() -> None:
    for deck in (
        _family("393") / "evaluator" / "score_tb.scs",
        _family("393") / "public" / "task" / "feedback_tb.scs",
    ):
        text = deck.read_text(encoding="utf-8")
        align_line = next(line for line in text.splitlines() if line.startswith("Valign_pulse"))
        assert "48n 0 48.2n 0.9" not in align_line
        assert "35n 0 35.2n 0.9 36n 0.9 36.2n 0" in align_line


def _clip(value: float, lo: float = 0.0, hi: float = 0.9) -> float:
    return max(lo, min(hi, value))


def _code_bits(code: int, prefix: str) -> dict[str, float]:
    return {f"{prefix}_{bit}": 0.9 if code & (1 << bit) else 0.0 for bit in range(3)}


def _expected(vin: float, gain_code: int, offset_code: int) -> tuple[float, float]:
    raw = 0.45 + (0.7 + 0.1 * gain_code) * (vin - 0.45) + 0.025 * (offset_code - 3)
    out = _clip(raw)
    return out, abs(out - 0.45)


def _row(
    time: float,
    *,
    clk: float,
    rst: float,
    enable: float,
    vin: float,
    gain_code: int,
    offset_code: int,
    vout: float,
    residual_metric: float,
    valid: bool,
) -> dict[str, float]:
    return {
        "time": time,
        "clk": clk,
        "rst": rst,
        "enable": enable,
        "vin": vin,
        **_code_bits(gain_code, "gain"),
        **_code_bits(offset_code, "offset"),
        "vout": vout,
        "residual_metric": residual_metric,
        "valid": 0.9 if valid else 0.0,
    }


def _registered_trim_trace(*, async_before_edge: bool) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    previous_out = 0.45
    previous_metric = 0.0
    previous_valid = False
    rows.append(
        _row(
            0.0,
            clk=0.0,
            rst=0.9,
            enable=0.0,
            vin=0.45,
            gain_code=0,
            offset_code=0,
            vout=previous_out,
            residual_metric=previous_metric,
            valid=previous_valid,
        )
    )
    stimuli = [
        (0.30, 0, 0, False),
        (0.62, 1, 2, True),
        (0.22, 4, 7, True),
        (0.84, 7, 7, True),
        (0.18, 2, 0, True),
        (0.76, 5, 3, True),
        (0.51, 3, 5, True),
        (0.88, 6, 6, True),
        (0.12, 1, 1, True),
        (0.68, 7, 0, True),
        (0.42, 0, 4, True),
        (0.81, 4, 2, True),
    ]
    for index, (vin, gain_code, offset_code, enabled) in enumerate(stimuli):
        edge = 2e-9 + index * 5e-9
        rst = 0.9 if index == 0 else 0.0
        enable = 0.9 if enabled else 0.0
        if rst > 0.45 or enable <= 0.45:
            expected_out, expected_metric, expected_valid = 0.45, 0.0, False
        else:
            expected_out, expected_metric = _expected(vin, gain_code, offset_code)
            expected_valid = True
        before_out = expected_out if async_before_edge else previous_out
        before_metric = expected_metric if async_before_edge else previous_metric
        before_valid = expected_valid if async_before_edge else previous_valid
        rows.append(
            _row(
                edge - 0.4e-9,
                clk=0.0,
                rst=rst,
                enable=enable,
                vin=vin,
                gain_code=gain_code,
                offset_code=offset_code,
                vout=before_out,
                residual_metric=before_metric,
                valid=before_valid,
            )
        )
        rows.append(
            _row(
                edge,
                clk=0.9,
                rst=rst,
                enable=enable,
                vin=vin,
                gain_code=gain_code,
                offset_code=offset_code,
                vout=before_out,
                residual_metric=before_metric,
                valid=before_valid,
            )
        )
        rows.append(
            _row(
                edge + 0.8e-9,
                clk=0.9,
                rst=rst,
                enable=enable,
                vin=vin,
                gain_code=gain_code,
                offset_code=offset_code,
                vout=expected_out,
                residual_metric=expected_metric,
                valid=expected_valid,
            )
        )
        rows.append(
            _row(
                edge + 1.0e-9,
                clk=0.0,
                rst=rst,
                enable=enable,
                vin=vin,
                gain_code=gain_code,
                offset_code=offset_code,
                vout=expected_out,
                residual_metric=expected_metric,
                valid=expected_valid,
            )
        )
        previous_out = expected_out
        previous_metric = expected_metric
        previous_valid = expected_valid
    return rows


def test_task397_accepts_registered_trim_updates_after_clock_edges() -> None:
    ok, note = check_v4_baseband_offset_gain_trim_macro(
        _registered_trim_trace(async_before_edge=False)
    )
    assert ok, note
    assert "hold_errors=0" in note


def test_task397_rejects_asynchronous_pre_edge_trim_updates() -> None:
    ok, note = check_v4_baseband_offset_gain_trim_macro(
        _registered_trim_trace(async_before_edge=True)
    )
    assert not ok
    assert "hold_errors=" in note
    assert "hold_errors=0" not in note
