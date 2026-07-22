from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

from checkers.v4.task_343 import check_v4_343_pipeline_adc_two_stage
from checkers.v4.task_353 import check_v4_ffe_transmitter_3tap


VDD = 0.9
VCM = 0.45


def _code_bits(code: int) -> dict[str, float]:
    return {f"code_{bit}": VDD if code & (1 << bit) else 0.0 for bit in range(4)}


def _pipeline_code(vin: float) -> int:
    return min(15, int(16.0 * max(0.0, min(VDD, vin)) / VDD))


def _pipeline_residue(vin: float) -> float:
    clipped = max(0.0, min(VDD, vin))
    coarse = min(3, int(4.0 * clipped / VDD))
    return max(0.0, min(VDD, 4.0 * (clipped - VDD * coarse / 4.0)))


def _pipeline_rows(*, delayed_by_three_edges: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    samples = {1: 0.10, 4: 0.50, 6: 1.02, 7: 0.70}
    reset_edges = {0, 3}
    outputs: dict[int, int] = {}
    for edge, vin in samples.items():
        outputs[edge + (3 if delayed_by_three_edges else 2)] = _pipeline_code(vin)

    residue = 0.0
    for edge in range(10):
        t = (1.0 + edge) * 1e-9
        rst = VDD if edge in reset_edges else 0.0
        vin = samples.get(edge, 0.25)
        valid_i = VDD if edge in samples and not rst else 0.0
        code = 0
        valid_o = 0.0
        if rst:
            residue = 0.0
        elif valid_i:
            residue = _pipeline_residue(vin)
        if not rst and edge in outputs:
            code = outputs[edge]
            valid_o = VDD
        base = {
            "vin": vin,
            "rst": rst,
            "valid_i": valid_i,
            "residue_dbg": residue,
            "valid_o": valid_o,
            **_code_bits(code),
        }
        rows.append({"time": t - 0.1e-9, "clk": 0.0, **base})
        rows.append({"time": t, "clk": VDD, **base})
        rows.append({"time": t + 0.7e-9, "clk": VDD, **base})
    return rows


def _ffe_expected(data_high: bool, pre_code: int, post_code: int, history: tuple[int, int, int]) -> tuple[int, int, int, float, float, float, float]:
    sym0, sym1, _sym2 = history
    next_sym2 = sym1
    next_sym1 = sym0
    next_sym0 = 1 if data_high else -1
    main = VCM + 0.18 * next_sym0
    pre = VCM + 0.04 * pre_code * next_sym1
    post = VCM - 0.04 * post_code * next_sym2
    out = max(0.0, min(VDD, VCM + 0.18 * next_sym0 + 0.04 * pre_code * next_sym1 - 0.04 * post_code * next_sym2))
    return next_sym0, next_sym1, next_sym2, main, pre, post, out


def _legacy_353_checker_accepts(rows: list[dict[str, float]]) -> bool:
    sym0 = sym1 = sym2 = 0
    checked = 0
    pre_codes: set[int] = set()
    post_codes: set[int] = set()
    out_values: list[float] = []
    last_clk_high = rows[0]["clk"] > 0.45
    for row in rows:
        clk_high = row["clk"] > 0.45
        if last_clk_high or not clk_high:
            last_clk_high = clk_high
            continue
        last_clk_high = clk_high
        if row["rst"] > 0.45:
            sym0 = sym1 = sym2 = 0
            expected_main = expected_pre = expected_post = expected_out = VCM
        else:
            sym2 = sym1
            sym1 = sym0
            sym0 = 1 if row["data"] > 0.45 else -1
            pre_code = (1 if row["pre_0"] > 0.45 else 0) + (2 if row["pre_1"] > 0.45 else 0)
            post_code = (1 if row["post_0"] > 0.45 else 0) + (2 if row["post_1"] > 0.45 else 0)
            pre_codes.add(pre_code)
            post_codes.add(post_code)
            expected_main = VCM + 0.18 * sym0
            expected_pre = VCM + 0.04 * pre_code * sym1
            expected_post = VCM - 0.04 * post_code * sym2
            expected_out = max(0.0, min(VDD, VCM + 0.18 * sym0 + 0.04 * pre_code * sym1 - 0.04 * post_code * sym2))
            out_values.append(expected_out)
        checks = (
            (row["main_dbg"], expected_main, 0.07),
            (row["pre_dbg"], expected_pre, 0.07),
            (row["post_dbg"], expected_post, 0.07),
            (row["vout"], expected_out, 0.08),
        )
        if any(abs(observed - expected) > tolerance for observed, expected, tolerance in checks):
            return False
        checked += 1
    out_span = max(out_values, default=VCM) - min(out_values, default=VCM)
    return checked >= 10 and len(pre_codes) >= 3 and len(post_codes) >= 3 and out_span > 0.25


def _ffe_rows(*, midrun_reset: bool = True, clear_midrun_history: bool = True) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    pattern = [
        (True, 0, 1, True),
        (False, 1, 1, False),
        (True, 3, 0, False),
        (False, 2, 3, midrun_reset),
        (True, 3, 3, False),
        (False, 1, 0, False),
        (True, 0, 2, False),
        (False, 2, 1, False),
        (True, 3, 2, False),
        (True, 0, 0, False),
    ]
    history = (0, 0, 0)
    for edge, (data_high, pre_code, post_code, rst) in enumerate(pattern):
        t = (1.0 + edge) * 1e-9
        if rst:
            if edge == 0 or clear_midrun_history:
                history = (0, 0, 0)
            main = pre = post = out = VCM
        else:
            sym0, sym1, sym2, main, pre, post, out = _ffe_expected(data_high, pre_code, post_code, history)
            history = (sym0, sym1, sym2)
        base = {
            "data": VDD if data_high else 0.0,
            "rst": VDD if rst else 0.0,
            "pre_0": VDD if pre_code & 1 else 0.0,
            "pre_1": VDD if pre_code & 2 else 0.0,
            "post_0": VDD if post_code & 1 else 0.0,
            "post_1": VDD if post_code & 2 else 0.0,
            "main_dbg": main,
            "pre_dbg": pre,
            "post_dbg": post,
            "vout": out,
        }
        rows.append({"time": t - 0.1e-9, "clk": 0.0, **base})
        rows.append({"time": t, "clk": VDD, **base})
        rows.append({"time": t + 0.8e-9, "clk": VDD, **base})
    return rows


def test_343_requires_exact_next_edge_latency_and_midrun_reset_recovery() -> None:
    passed, detail = check_v4_343_pipeline_adc_two_stage(_pipeline_rows())
    assert passed, detail

    passed, detail = check_v4_343_pipeline_adc_two_stage(_pipeline_rows(delayed_by_three_edges=True))
    assert not passed
    assert "P_PIPE_VALID_LATENCY" in detail or "P_PIPE_EXACT_LATENCY" in detail


def test_353_requires_midrun_reset_history_clear() -> None:
    passed, detail = check_v4_ffe_transmitter_3tap(_ffe_rows())
    assert passed, detail

    assert _legacy_353_checker_accepts(_ffe_rows(midrun_reset=False, clear_midrun_history=False))

    passed, detail = check_v4_ffe_transmitter_3tap(_ffe_rows(midrun_reset=True, clear_midrun_history=False))
    assert not passed
    assert "P_RESET_HISTORY_CLEAR" in detail or "P_PRE_TAP" in detail or "P_POST_TAP" in detail
