from __future__ import annotations

import csv
import math
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))


from checkers.v4.task_082 import check_agc_receiver_leveling_loop  # noqa: E402
from checkers.v4.task_083 import check_release_amplifier_filter_chain  # noqa: E402
from checkers.v4.task_088 import (  # noqa: E402
    _stream_cppll_freq_step_reacquire_csv,
    check_cppll_freq_step_reacquire,
)
from checkers.v4.task_090 import check_v3_dither_adder  # noqa: E402


def test_agc_checker_uses_observed_input_regions_not_absolute_windows() -> None:
    start = 1.25e-6
    rows: list[dict[str, float]] = []
    for idx in range(80):
        time = start + idx * 1.0e-9
        rst = 0.9 if idx < 3 else 0.0
        if idx < 10:
            vin = 0.45
            out = 0.45
            metric = 0.0
            gain = 0.75
            rssi = 0.10
        elif idx < 28:
            vin = 0.535
            out = 0.58
            metric = 0.25
            gain = 0.75
            rssi = 0.22
        elif idx < 48:
            vin = 0.77
            out = 0.82
            metric = 0.35
            gain = 0.52
            rssi = 0.76
        else:
            vin = 0.54
            out = 0.61
            metric = 0.80
            gain = 0.49
            rssi = 0.38
        rows.append(
            {
                "time": time,
                "clk": 0.9 if idx % 2 else 0.0,
                "rst": rst,
                "vin": vin,
                "out": out,
                "metric": metric,
                "gain_mon": gain,
                "rssi_mon": rssi,
            }
        )

    ok, note = check_agc_receiver_leveling_loop(rows)

    assert ok, note
    assert "P_CLOCKED_GAIN_LOOP mismatch_count=0" in note


def test_amplifier_filter_checker_derives_regions_from_vin_segments() -> None:
    start = 2.0e-6
    rows: list[dict[str, float]] = []
    for idx in range(70):
        time = start + idx * 1.0e-9
        rst = 0.9 if idx < 3 else 0.0
        vin = 0.45
        metric = preamp = filt1 = filt2 = out = 0.45
        settle = 0.0
        if 10 <= idx < 36:
            vin = 0.90
            phase = (idx - 10) / 25.0
            metric = preamp = 0.88
            filt1 = 0.76 + 0.08 * min(1.0, phase * 2.0)
            filt2 = out = 0.50 + 0.27 * phase
            settle = 0.20 if phase < 0.35 else 0.82
        elif 38 <= idx < 48:
            vin = 0.45
            metric = preamp = filt1 = filt2 = out = 0.45
            settle = 0.45
        elif 50 <= idx < 68:
            vin = 0.10
            metric = preamp = 0.03
            filt1 = 0.10
            filt2 = out = 0.10
            settle = 0.20
        rows.append(
            {
                "time": time,
                "clk": 0.9 if idx % 2 else 0.0,
                "rst": rst,
                "vin": vin,
                "out": out,
                "metric": metric,
                "preamp_mon": preamp,
                "filt1_mon": filt1,
                "filt2_mon": filt2,
                "settle_metric": settle,
            }
        )

    ok, note = check_release_amplifier_filter_chain(rows)

    assert ok, note
    assert "P_CASCADE_LAG mismatch_count=0" in note


def _clock_value(time_s: float, *, start: float, step_time: float, pre_period: float, post_period: float) -> float:
    if time_s < step_time:
        phase = (time_s - start) % pre_period
        period = pre_period
    else:
        pre_cycles = math.floor((step_time - start) / pre_period)
        aligned_step = start + pre_cycles * pre_period
        phase = (time_s - aligned_step) % post_period
        period = post_period
    return 0.9 if phase < 0.5 * period else 0.0


def _cppll_rows() -> list[dict[str, float]]:
    start = 10.0e-6
    step_time = start + 2.0e-6
    pre_period = 20.4e-9
    post_period = 19.8e-9
    rows: list[dict[str, float]] = []
    for idx in range(15000):
        time = start + idx * 0.2e-9
        lock = 0.9
        if step_time - 0.40e-6 <= time <= step_time + 260e-9:
            lock = 0.0
        rows.append(
            {
                "time": time,
                "ref_clk": _clock_value(time, start=start, step_time=step_time, pre_period=pre_period, post_period=post_period),
                "fb_clk": _clock_value(time, start=start, step_time=step_time, pre_period=pre_period, post_period=post_period),
                "lock": lock,
                "vctrl_mon": 0.45 + 0.04 * math.sin((time - start) / 200e-9),
            }
        )
    return rows


def test_cppll_checker_detects_observed_reference_step_and_streaming_matches(tmp_path: Path) -> None:
    rows = _cppll_rows()

    ok, note = check_cppll_freq_step_reacquire(rows)

    assert ok, note
    csv_path = tmp_path / "tran.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["time", "ref_clk", "fb_clk", "lock", "vctrl_mon"])
        writer.writeheader()
        writer.writerows(rows)

    stream_score, stream_notes = _stream_cppll_freq_step_reacquire_csv(csv_path)

    assert stream_score == 1.0
    assert stream_notes == [note]


def test_dither_checker_uses_observed_dpn_state_segments() -> None:
    start = 4.0e-6
    rows: list[dict[str, float]] = []
    for idx in range(180):
        time = start + idx * 0.5e-9
        dpn = 0.9 if 35 <= idx < 90 or 125 <= idx < 155 else 0.0
        vres_p = 0.56 + 0.02 * math.sin(idx / 15)
        vres_n = 0.34 - 0.02 * math.sin(idx / 15)
        vin_diff = vres_p - vres_n
        dither = 0.024 if dpn > 0.45 else -0.024
        out_diff = vin_diff + dither
        out_cm = 0.5 * (vres_p + vres_n)
        rows.append(
            {
                "time": time,
                "vres_p": vres_p,
                "vres_n": vres_n,
                "dpn": dpn,
                "vout_p": out_cm + 0.5 * out_diff,
                "vout_n": out_cm - 0.5 * out_diff,
            }
        )

    ok, note = check_v3_dither_adder(rows)

    assert ok, note
    assert "P_PARAMETER_OVERRIDE mismatch_count=0" in note
