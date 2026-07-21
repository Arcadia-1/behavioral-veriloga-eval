from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

from checkers.v4.task_202 import CHECKER as CHECKER_202
from checkers.v4.task_207 import CHECKER as CHECKER_207
from checkers.v4.task_213 import CHECKER as CHECKER_213
from checkers.v4.task_219 import CHECKER as CHECKER_219
from checkers.v4.task_244 import CHECKER as CHECKER_244
from checkers.v4.task_248 import CHECKER as CHECKER_248


def _clock(time_ns: float, first_rise_ns: float, period_ns: float = 1.0) -> float:
    if time_ns < first_rise_ns:
        return 0.0
    return 0.9 if (time_ns - first_rise_ns) % period_ns < 0.30 else 0.0


def _rows_202(*, spikes_only: bool = False) -> list[dict[str, float]]:
    windows = {
        "rst": ((0.5, 0.8),),
        "s": ((1.5, 2.5),),
        "sar": ((3.0, 5.4),),
        "clk_sar": ((3.0, 3.25), (3.6, 3.85), (4.2, 4.45)),
        "res": ((6.0, 6.6),),
        "intg": ((8.0, 8.7),),
        "zoom": ((9.2, 10.8),),
        "clk_zoom": ((9.2, 9.45), (9.8, 10.05)),
        "rst_zoom": ((11.0, 11.5),),
    }
    old_probes = {
        "rst": (0.6,),
        "s": (1.8,),
        "sar": (3.4,),
        "clk_sar": (3.1, 3.7, 4.3),
        "res": (6.3,),
        "intg": (8.3,),
        "zoom": (9.6,),
        "clk_zoom": (9.3, 9.9),
        "rst_zoom": (11.2,),
    }
    rows: list[dict[str, float]] = []
    for index in range(4501):
        time_ns = index * 0.01
        phase_ns = time_ns % 32.0
        row = {"time": time_ns * 1e-9}
        for signal, signal_windows in windows.items():
            if spikes_only:
                high = any(abs(phase_ns - probe) <= 0.01 for probe in old_probes[signal])
            else:
                high = any(start <= phase_ns < stop for start, stop in signal_windows)
            row[signal] = 1.1 if high else 0.0
        rows.append(row)
    return rows


def _restore4_rows(*, combinational: bool) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    held_code = 0
    for index in range(401):
        time_ns = index * 0.01
        if time_ns < 1.05:
            bits = (0, 0, 0, 0)
        elif time_ns < 2.05:
            bits = (1, 0, 1, 0)
        elif time_ns < 3.05:
            bits = (0, 1, 0, 1)
        else:
            bits = (1, 1, 1, 1)
        if any(abs(time_ns - edge) < 0.006 for edge in (0.36, 1.36, 2.36, 3.36)):
            held_code = sum(bit << bit_index for bit_index, bit in enumerate(bits))
        code = sum(bit << bit_index for bit_index, bit in enumerate(bits)) if combinational else held_code
        rows.append(
            {
                "time": time_ns * 1e-9,
                "clk": _clock(time_ns, 0.36),
                **{f"d{bit_index}": 0.9 * bit for bit_index, bit in enumerate(bits)},
                "vout": (code + 0.5) * 1.8 / 16.0 - 0.9,
            }
        )
    return rows


def _signed_dac_rows(*, combinational: bool) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    held_total = -15.0
    for index in range(401):
        time_ns = index * 0.01
        if time_ns < 1.05:
            bits = (0, 0, 0, 0)
        elif time_ns < 2.05:
            bits = (0, 1, 0, 1)
        elif time_ns < 3.05:
            bits = (1, 0, 1, 0)
        else:
            bits = (1, 1, 1, 1)
        total = sum((1 if bit else -1) * weight for bit, weight in zip(bits, (1, 2, 4, 8)))
        if any(abs(time_ns - edge) < 0.006 for edge in (0.35, 1.35, 2.35, 3.35)):
            held_total = total
        rows.append(
            {
                "time": time_ns * 1e-9,
                "sh": 1.8 if _clock(time_ns, 0.35) > 0.45 else 0.0,
                **{f"d{bit_index}": 1.8 * bit for bit_index, bit in enumerate(bits)},
                "aout": (total if combinational else held_total) * 1.8 / 16.0,
            }
        )
    return rows


def _bin2ther_rows(*, hardcoded_rails: bool) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for index in range(401):
        time_ns = index * 0.01
        vdd = 0.9 if time_ns < 1.65 else (1.2 if time_ns < 2.75 else 0.7)
        b1 = 0.0 if time_ns < 2.05 else 0.9
        b0 = 0.0 if time_ns < 1.05 else (0.9 if time_ns < 2.05 else (0.0 if time_ns < 3.05 else 0.4))
        if hardcoded_rails:
            high, low, threshold = 0.9, 0.0, 0.45
        else:
            high, low, threshold = vdd, 0.0, 0.5 * vdd
        rows.append(
            {
                "time": time_ns * 1e-9,
                "vdd": vdd,
                "gnd": 0.0,
                "b1": b1,
                "b0": b0,
                "t0": high if b1 > threshold else low,
                "t1": high if b1 > threshold else low,
                "t2": high if b0 > threshold else low,
            }
        )
    return rows


def _adc3_rows(*, combinational: bool) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    held_code = 0
    for index in range(501):
        time_ns = index * 0.01
        vin = 0.02 if time_ns < 1.2 else (0.40 if time_ns < 2.2 else (0.70 if time_ns < 3.2 else 0.99))
        code = max(0, min(7, int(8.0 * vin)))
        if any(abs(time_ns - edge) < 0.006 for edge in (0.5, 1.5, 2.5, 3.5, 4.5)):
            held_code = code
        output_code = code if combinational else held_code
        rows.append(
            {
                "time": time_ns * 1e-9,
                "vin": vin,
                "vclk": _clock(time_ns, 0.5),
                "vd0": 0.9 * (output_code & 1),
                "vd1": 0.9 * ((output_code >> 1) & 1),
                "vd2": 0.9 * ((output_code >> 2) & 1),
            }
        )
    return rows


def _dff_rows(*, combinational: bool) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    held_high = False
    for index in range(401):
        time_ns = index * 0.01
        vin = -0.4 if time_ns < 1.2 else (0.4 if time_ns < 2.2 else -0.3)
        if any(abs(time_ns - edge) < 0.006 for edge in (0.5, 1.5, 2.5, 3.5)):
            held_high = vin > 0.0
        high = vin > 0.0 if combinational else held_high
        q = 1.0 if high else -1.0
        rows.append(
            {
                "time": time_ns * 1e-9,
                "vin_d": vin,
                "vclk": _clock(time_ns, 0.5),
                "vout_q": q,
                "vout_qbar": -q,
            }
        )
    return rows


def test_202_accepts_two_complete_legal_frames() -> None:
    assert CHECKER_202(_rows_202())[0]


def test_202_rejects_sparse_probe_spikes() -> None:
    assert not CHECKER_202(_rows_202(spikes_only=True))[0]


def test_207_accepts_held_restore_output_and_rejects_combinational_tracking() -> None:
    assert CHECKER_207(_restore4_rows(combinational=False))[0]
    assert not CHECKER_207(_restore4_rows(combinational=True))[0]


def test_213_accepts_sampled_dac_and_rejects_combinational_tracking() -> None:
    assert CHECKER_213(_signed_dac_rows(combinational=False))[0]
    assert not CHECKER_213(_signed_dac_rows(combinational=True))[0]


def test_219_accepts_local_rails_and_rejects_hardcoded_default_rails() -> None:
    assert CHECKER_219(_bin2ther_rows(hardcoded_rails=False))[0]
    assert not CHECKER_219(_bin2ther_rows(hardcoded_rails=True))[0]


def test_244_accepts_clocked_adc_and_rejects_combinational_tracking() -> None:
    assert CHECKER_244(_adc3_rows(combinational=False))[0]
    assert not CHECKER_244(_adc3_rows(combinational=True))[0]


def test_248_accepts_dff_hold_and_rejects_combinational_tracking() -> None:
    assert CHECKER_248(_dff_rows(combinational=False))[0]
    assert not CHECKER_248(_dff_rows(combinational=True))[0]
