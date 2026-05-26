from __future__ import annotations

import math
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

import simulate_evas as sim  # noqa: E402


PROMOTED_DUTS = {
    "vbr1_l1_burst_clock_source",
    "vbr1_l1_clocked_adc_quantizer",
    "vbr1_l1_clocked_sample_and_hold",
    "vbr1_l1_sample_and_hold_with_droop_leakage",
    "vbr1_l1_acquisition_limited_sample_and_hold",
    "vbr1_l1_aperture_delay_track_and_hold",
    "vbr1_l1_digital_phase_accumulator_with_modulo_wrap",
    "vbr1_l1_dither_or_noise_like_deterministic_source",
    "vbr1_l1_dwa_dem_encoder",
    "vbr1_l1_first_order_lowpass",
    "vbr1_l1_higher_order_filter",
    "vbr1_l1_hysteresis_comparator",
    "vbr1_l1_propagation_delay_comparator",
    "vbr1_l1_programmable_gain_amplifier",
    "vbr1_l1_ramp_or_step_source",
    "vbr1_l1_resettable_integrator",
    "vbr1_l1_slew_rate_limiter",
    "vbr1_l1_soft_hysteretic_limiter",
    "vbr1_l1_threshold_comparator",
    "vbr1_l1_unit_element_thermometer_dac",
    "vbr1_l1_precision_rectifier_envelope_detector",
    "vbr1_l1_window_comparator_detector",
}


def test_promoted_duts_have_release_behavior_aliases() -> None:
    for entry_id in PROMOTED_DUTS:
        assert sim.has_behavior_check(f"{entry_id}_dut"), entry_id


def _cmp_delay_rows(*, mode: str = "good") -> list[dict[str, float]]:
    phases = [
        (0.0e-9, 4.0e-9, 10e-3),
        (4.0e-9, 8.0e-9, 1e-3),
        (8.0e-9, 12.0e-9, 0.1e-3),
        (12.0e-9, 16.0e-9, 0.01e-3),
    ]
    delays_ns = [0.055, 0.070, 0.085, 0.100]
    if mode == "flat_delay":
        delays_ns = [0.055, 0.055, 0.055, 0.055]

    rows: list[dict[str, float]] = []
    step = 10e-12
    for idx in range(int(16e-9 / step) + 1):
        time = idx * step
        phase_idx = min(int(time // 4.0e-9), 3)
        start_t, _end_t, diff = phases[phase_idx]
        search_start = start_t + 0.1e-9
        delay = delays_ns[phase_idx] * 1e-9
        pulse_start = search_start + delay
        pulse_end = pulse_start + 0.25e-9
        out_high = pulse_start <= time < pulse_end
        if mode == "stuck_high":
            out_high = True
        rows.append(
            {
                "time": time,
                "clk": 0.9 if search_start <= time < search_start + 0.45e-9 else 0.0,
                "vinp": 0.45 + diff / 2,
                "vinn": 0.45 - diff / 2,
                "out_p": 0.9 if out_high else 0.0,
                "out_n": 0.0 if out_high else 0.9,
                "delay_ps": delays_ns[phase_idx] * 1000 if time >= pulse_start else 0.0,
            }
        )
    return rows


def test_cmp_delay_checker_requires_real_delay_growth() -> None:
    assert sim.check_cmp_delay(_cmp_delay_rows())[0]
    assert not sim.check_cmp_delay(_cmp_delay_rows(mode="flat_delay"))[0]
    assert not sim.check_cmp_delay(_cmp_delay_rows(mode="stuck_high"))[0]


def test_cmp_delay_checker_accepts_sparse_spectre_like_samples() -> None:
    dense_rows = _cmp_delay_rows()
    keep_times = {
        0.0,
        16.0e-9,
        *[start + offset for start in (0.0e-9, 4.0e-9, 8.0e-9, 12.0e-9) for offset in (0.0, 0.08e-9, 0.10e-9, 0.18e-9, 0.36e-9, 3.90e-9)],
    }
    sparse_rows = [
        row
        for row in dense_rows
        if any(math.isclose(row["time"], keep, rel_tol=0.0, abs_tol=0.5e-12) for keep in keep_times)
    ]

    assert sim.check_cmp_delay(sparse_rows)[0]


def _first_order_lowpass_rows(*, mode: str = "good") -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    tau = 18.0e-9
    for idx in range(0, 161):
        time = idx * 1.0e-9
        vin = 0.8 if time >= 21.0e-9 else 0.0
        if mode == "no_input_step":
            vin = 0.0
        if mode == "passthrough":
            vout = vin
        elif time < 21.0e-9:
            vout = 0.0
        else:
            vout = 0.8 * (1.0 - math.exp(-(time - 21.0e-9) / tau))
        rows.append({"time": time, "vin": vin, "vout": vout})
    return rows


def test_first_order_lowpass_checker_requires_input_step_and_lag() -> None:
    assert sim.check_vbm1_first_order_lowpass(_first_order_lowpass_rows())[0]
    assert not sim.check_vbm1_first_order_lowpass(_first_order_lowpass_rows(mode="no_input_step"))[0]
    assert not sim.check_vbm1_first_order_lowpass(_first_order_lowpass_rows(mode="passthrough"))[0]


def _resettable_integrator_rows(*, mode: str = "good") -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for idx in range(0, 321):
        time = idx * 1.0e-9
        t_ns = float(idx)
        rst = 0.9 if t_ns <= 25.0 or 221.0 <= t_ns <= 250.0 else 0.0
        vin = 0.002
        if mode == "no_reset_stimulus":
            rst = 0.0
        if rst > 0.45:
            vout = 0.0 if mode != "stale_reset" else 0.34
        elif t_ns < 221.0:
            vout = max(0.0, min(0.85, (t_ns - 26.0) * 0.002))
        else:
            vout = max(0.0, min(0.85, (t_ns - 251.0) * 0.002))
        rows.append({"time": time, "vin": vin, "rst": rst, "vout": vout})
    return rows


def test_resettable_integrator_checker_requires_reset_stimulus_and_restart() -> None:
    assert sim.check_vbm1_resettable_integrator(_resettable_integrator_rows())[0]
    assert not sim.check_vbm1_resettable_integrator(_resettable_integrator_rows(mode="no_reset_stimulus"))[0]
    assert not sim.check_vbm1_resettable_integrator(_resettable_integrator_rows(mode="stale_reset"))[0]


def _slew_rate_limiter_rows(*, mode: str = "good") -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for idx in range(0, 171):
        time = idx * 1.0e-9
        t_ns = float(idx)
        if t_ns < 21.0:
            vin = 0.0
            vout = 0.0
        elif t_ns < 96.0:
            vin = 0.8
            vout = min(0.8, (t_ns - 21.0) * 0.015)
        else:
            vin = 0.1
            vout = max(0.1, 0.8 - (t_ns - 96.0) * 0.015)
        if mode == "no_input_sequence":
            vin = 0.0
        if mode == "passthrough":
            vout = vin
        rows.append({"time": time, "vin": vin, "vout": vout})
    return rows


def test_slew_rate_limiter_checker_requires_input_sequence_and_limited_edges() -> None:
    assert sim.check_vbm1_slew_rate_limiter(_slew_rate_limiter_rows())[0]
    assert not sim.check_vbm1_slew_rate_limiter(_slew_rate_limiter_rows(mode="no_input_sequence"))[0]
    assert not sim.check_vbm1_slew_rate_limiter(_slew_rate_limiter_rows(mode="passthrough"))[0]


def test_noise_source_checker_rejects_flat_passthrough() -> None:
    ok_rows = [
        {"time": idx, "vin_i": 1.0, "vout_o": 1.0 + delta}
        for idx, delta in enumerate([0.08, -0.04, 0.06, -0.07, 0.03, -0.09])
    ]
    bad_rows = [{"time": idx, "vin_i": 1.0, "vout_o": 1.0} for idx in range(6)]

    assert sim.check_noise_gen(ok_rows)[0]
    assert not sim.check_noise_gen(bad_rows)[0]


def _prbs7_rows(*, tap: tuple[int, int] = (6, 5)) -> list[dict[str, float]]:
    state = 127
    rows: list[dict[str, float]] = []
    for step in range(24):
        row = {
            "time": step * 1e-9 + 3e-9,
            "clk": 0.9,
            "rst_n": 0.9,
            "en": 0.9,
            "serial_out": 0.9 if ((state >> 6) & 1) else 0.0,
        }
        for idx in range(7):
            row[f"state_{idx}"] = 0.9 if ((state >> idx) & 1) else 0.0
        rows.append(row)
        feedback = ((state >> tap[0]) & 1) ^ ((state >> tap[1]) & 1)
        state = ((state & 0x3F) << 1) | feedback
    return rows


def test_prbs7_checker_rejects_wrong_feedback_tap() -> None:
    assert sim.check_prbs7(_prbs7_rows())[0]
    assert not sim.check_prbs7(_prbs7_rows(tap=(6, 4)))[0]


def _threshold_comparator_rows(*, inverted: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for idx in range(60):
        time = idx * 0.5e-9
        vinp = 0.7 if idx >= 30 else 0.2
        vinn = 0.2 if idx >= 30 else 0.7
        out_high = vinp > vinn
        if inverted:
            out_high = not out_high
        rows.append({"time": time, "vinp": vinp, "vinn": vinn, "out_p": 0.9 if out_high else 0.0})
    return rows


def test_threshold_comparator_checker_rejects_inverted_polarity() -> None:
    assert sim.check_comparator(_threshold_comparator_rows())[0]
    assert not sim.check_comparator(_threshold_comparator_rows(inverted=True))[0]


def _window_comparator_rows(*, mode: str = "true_window") -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    schmitt_state = False
    previous_vin = 0.0
    for idx in range(91):
        time = idx * 1.0e-9
        vin = 0.9 * (idx / 45.0) if idx <= 45 else 0.9 * ((90 - idx) / 45.0)
        if mode == "true_window":
            high = 0.3 < vin < 0.6
        elif mode == "above_high_stuck":
            high = vin > 0.3
        elif mode == "old_hysteresis":
            if previous_vin < 0.6 <= vin:
                schmitt_state = True
            if previous_vin > 0.3 >= vin:
                schmitt_state = False
            high = schmitt_state
        else:
            raise ValueError(mode)
        rows.append({"time": time, "vin": vin, "out": 0.9 if high else 0.0})
        previous_vin = vin
    return rows


def test_true_window_comparator_checker_rejects_hysteresis_semantics() -> None:
    assert sim.check_true_window_comparator(_window_comparator_rows())[0]
    assert not sim.check_true_window_comparator(_window_comparator_rows(mode="old_hysteresis"))[0]
    assert not sim.check_true_window_comparator(_window_comparator_rows(mode="above_high_stuck"))[0]


def _comparator_measurement_flow_rows(*, mode: str = "good") -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for idx in range(101):
        time = idx * 1.0e-9
        inp = 0.490 + 0.030 * min(time / 80e-9, 1.0)
        inn = 0.500
        tripped = inp >= 0.505
        outp = 0.9 if tripped else 0.0
        valid = 0.9 if tripped else 0.0
        trip_v = 0.505 if tripped else 0.0
        offset_est = 0.005 if tripped else 0.0
        if mode == "early_output":
            outp = 0.9 if inp >= 0.502 else 0.0
        if mode == "early_valid":
            valid = 0.9 if inp >= 0.502 else 0.0
            if valid > 0.45:
                trip_v = 0.505
                offset_est = 0.005
        if mode == "wrong_trip" and tripped:
            trip_v = 0.510
            offset_est = 0.010
        row = {
            "time": time,
            "inp": inp,
            "inn": inn,
            "outp": outp,
            "trip_v": trip_v,
            "offset_est": offset_est,
            "valid": valid,
        }
        if mode == "missing_metric":
            row.pop("trip_v")
        if mode == "shallow_output_only":
            row = {"time": time, "inp": inp, "inn": inn, "outp": outp}
        rows.append(row)
    return rows


def test_comparator_measurement_flow_checker_requires_latched_metrics() -> None:
    assert sim.check_comparator_measurement_flow(_comparator_measurement_flow_rows())[0]
    assert not sim.check_comparator_measurement_flow(_comparator_measurement_flow_rows(mode="missing_metric"))[0]
    assert not sim.check_comparator_measurement_flow(_comparator_measurement_flow_rows(mode="wrong_trip"))[0]
    assert not sim.check_comparator_measurement_flow(_comparator_measurement_flow_rows(mode="shallow_output_only"))[0]
    assert not sim.check_comparator_measurement_flow(_comparator_measurement_flow_rows(mode="early_output"))[0]
    assert not sim.check_comparator_measurement_flow(_comparator_measurement_flow_rows(mode="early_valid"))[0]


def _xor_pd_rows(*, and_gate: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for idx in range(240):
        phase = idx % 40
        ref = phase < 20
        div = 10 <= phase < 30
        out = (ref and div) if and_gate else (ref ^ div)
        rows.append(
            {
                "time": idx * 0.5e-9,
                "ref": 0.9 if ref else 0.0,
                "div": 0.9 if div else 0.0,
                "pd_out": 0.9 if out else 0.0,
            }
        )
    return rows


def test_xor_pd_checker_rejects_non_xor_logic() -> None:
    assert sim.check_xor_pd(_xor_pd_rows())[0]
    assert not sim.check_xor_pd(_xor_pd_rows(and_gate=True))[0]


def _bbpd_rows(*, swapped_outputs: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    data_high = False
    for idx in range(12):
        edge_t = idx * 1.0e-9 + 0.2e-9
        expect_up = idx < 6
        clk = 0.9 if expect_up else 0.0
        retimed_data = 0.0 if expect_up else 0.9
        rows.append(
            {
                "time": edge_t - 0.02e-9,
                "data": 0.9 if data_high else 0.0,
                "clk": clk,
                "retimed_data": retimed_data,
                "up": 0.0,
                "down": 0.0,
            }
        )
        data_high = not data_high
        correct_signal = "up" if expect_up else "down"
        if swapped_outputs:
            observed_signal = "down" if correct_signal == "up" else "up"
        else:
            observed_signal = correct_signal
        pulse = {"up": 0.0, "down": 0.0}
        pulse[observed_signal] = 0.9
        rows.append(
            {
                "time": edge_t,
                "data": 0.9 if data_high else 0.0,
                "clk": clk,
                "retimed_data": retimed_data,
                "up": 0.0,
                "down": 0.0,
            }
        )
        rows.append(
            {
                "time": edge_t + 0.02e-9,
                "data": 0.9 if data_high else 0.0,
                "clk": clk,
                "retimed_data": retimed_data,
                **pulse,
            }
        )
        rows.append(
            {
                "time": edge_t + 0.12e-9,
                "data": 0.9 if data_high else 0.0,
                "clk": clk,
                "retimed_data": retimed_data,
                "up": 0.0,
                "down": 0.0,
            }
        )
    return rows


def test_bbpd_checker_rejects_swapped_up_down_direction() -> None:
    assert sim.check_bbpd(_bbpd_rows())[0]
    assert not sim.check_bbpd(_bbpd_rows(swapped_outputs=True))[0]


def _dwa_rows(*, corrupt_cell_span: bool = False) -> list[dict[str, float]]:
    codes = [3, 7, 2, 5, 1, 8, 4, 6, 6]
    rows: list[dict[str, float]] = []
    ptr = 0
    previous_code: int | None = None
    zero_bus = {f"code_{bit}": 0.0 for bit in range(4)}
    zero_bus.update({f"ptr_{bit}": 0.0 for bit in range(16)})
    zero_bus.update({f"cell_en_{bit}": 0.0 for bit in range(16)})
    for idx, code in enumerate(codes):
        edge_t = idx * 10e-9 + 1e-9
        rows.append({"time": edge_t - 0.1e-9, "clk_i": 0.0, "rst_ni": 0.9, **zero_bus})
        rows.append({"time": edge_t, "clk_i": 0.9, "rst_ni": 0.9, **zero_bus})
        effective_code = code if previous_code is None else previous_code
        ptr = (ptr + effective_code) % 16
        active_cells = {(ptr - offset) % 16 for offset in range(effective_code + 1)}
        if corrupt_cell_span and idx == len(codes) - 1:
            active_cells = set()
        sample = {"time": edge_t + 1.0e-9, "clk_i": 0.9, "rst_ni": 0.9}
        for bit in range(4):
            sample[f"code_{bit}"] = 0.9 if ((code >> bit) & 1) else 0.0
        for bit in range(16):
            sample[f"ptr_{bit}"] = 0.9 if bit == ptr else 0.0
            sample[f"cell_en_{bit}"] = 0.9 if bit in active_cells else 0.0
        rows.append(sample)
        previous_code = code
    return rows


def test_dwa_release_checker_rejects_wrong_cell_span() -> None:
    assert sim.check_dwa_dem_encoder_release(_dwa_rows())[0]
    assert not sim.check_dwa_dem_encoder_release(_dwa_rows(corrupt_cell_span=True))[0]


def _element_shuffler_rows(sequence: list[int]) -> list[dict[str, float]]:
    sample_times_ns = [20.0, 40.0, 60.0, 80.0, 100.0, 120.0]
    rows: list[dict[str, float]] = []
    for time_ns, active in zip(sample_times_ns, sequence):
        row = {"time": time_ns * 1e-9}
        for idx in range(4):
            row[f"out{idx}"] = 0.9 if idx == active else 0.0
        rows.append(row)
    return rows


def test_release_element_shuffler_checker_rejects_plain_rotation() -> None:
    assert sim.check_release_element_shuffler(_element_shuffler_rows([2, 0, 3, 1, 2, 0]))[0]
    assert not sim.check_release_element_shuffler(_element_shuffler_rows([1, 2, 3, 0, 1, 2]))[0]


def _ramp_rows(*, flat_phase: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    period = 8.0
    pulse_w = 1.5
    step = 0.25
    for idx in range(int(34.0 / step) + 1):
        time = idx * step
        phase = 0.0 if flat_phase else time % period
        rows.append(
            {
                "time": time,
                "phase_out": 0.9 * phase / period,
                "guard_out": 0.9 if phase <= pulse_w else 0.0,
            }
        )
    return rows


def test_bound_step_period_guard_checker_rejects_flat_phase() -> None:
    assert sim.check_bound_step_period_guard(_ramp_rows())[0]
    assert not sim.check_bound_step_period_guard(_ramp_rows(flat_phase=True))[0]


def _release_loop_filter_rows(*, metric_stuck_low: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    state = 0.45
    step = 0.20
    integ = 0.0
    cycle = 0
    donev = 0.0
    previous_clk = 0.9

    def vin_at(time_s: float) -> float:
        t_ns = time_s * 1e9
        if t_ns < 8:
            return 0.45 + 0.02 * t_ns / 8
        if t_ns < 14:
            return 0.47 - 0.04 * (t_ns - 8) / 6
        if t_ns < 20:
            return 0.43 + 0.32 * (t_ns - 14) / 6
        if t_ns < 40:
            return 0.75 - 0.57 * (t_ns - 20) / 20
        if t_ns < 58:
            return 0.18 + 0.54 * (t_ns - 40) / 18
        if t_ns < 68:
            return 0.72 - 0.25 * (t_ns - 58) / 10
        if t_ns < 74:
            return 0.47 + 0.31 * (t_ns - 68) / 6
        return 0.78

    for idx in range(161):
        time_s = idx * 0.5e-9
        phase = (time_s * 1e9) % 2.0
        clk = 0.9 if phase < 1.0 else 0.0
        rst = 0.9 if time_s <= 2.0e-9 or 62.1e-9 <= time_s <= 70.0e-9 else 0.0
        vin = vin_at(time_s)
        if previous_clk <= 0.45 < clk:
            errv = vin - 0.45
            if rst > 0.45:
                state = 0.45
                step = 0.20
                integ = 0.0
                cycle = 0
                donev = 0.0
            elif abs(errv) > 0.05:
                state += step if errv > 0 else -step
                integ += errv * 0.04
                step *= 0.5
                cycle += 1
                donev = 0.9 if cycle >= 4 else 0.0
            state = min(max(state, 0.05), 0.85)
        previous_clk = clk
        rows.append(
            {
                "time": time_s,
                "clk": clk,
                "rst": rst,
                "vin": vin,
                "out": state + integ,
                "metric": 0.0 if metric_stuck_low else donev,
            }
        )
    return rows


def test_release_loop_filter_checker_requires_metric_and_pi_semantics() -> None:
    assert sim.check_release_loop_filter(_release_loop_filter_rows())[0]
    ok, note = sim.check_release_loop_filter(_release_loop_filter_rows(metric_stuck_low=True))
    assert not ok
    assert "metric_timing" in note


def _release_charge_pump_rows(*, swapped: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    ctrl = 0.45
    previous_clk = 0.0
    up_edges = {6.0, 8.0, 10.0, 12.0, 14.0, 16.0, 18.0}
    dn_edges = {32.0, 34.0, 36.0, 38.0, 40.0}

    for idx in range(161):
        time_s = idx * 0.5e-9
        t_ns = time_s * 1e9
        clk = 0.9 if (t_ns % 2.0) < 1.0 else 0.0
        rst = 0.9 if time_s <= 2.0e-9 or 62.1e-9 <= time_s <= 66.0e-9 else 0.0
        up = 0.9 if any(abs(t_ns - edge) <= 0.25 for edge in up_edges) else 0.0
        dn = 0.9 if any(abs(t_ns - edge) <= 0.25 for edge in dn_edges) else 0.0
        metric = 0.45
        if previous_clk <= 0.45 < clk:
            if rst > 0.45:
                ctrl = 0.45
                metric = 0.45
            elif up > 0.45 and dn <= 0.45:
                ctrl += -0.06 if swapped else 0.06
                metric = 0.75
            elif dn > 0.45 and up <= 0.45:
                ctrl += 0.06 if swapped else -0.06
                metric = 0.15
            ctrl = min(max(ctrl, 0.05), 0.85)
        previous_clk = clk
        rows.append(
            {
                "time": time_s,
                "clk": clk,
                "rst": rst,
                "up": up,
                "dn": dn,
                "vctrl": ctrl,
                "metric": metric,
            }
        )
    return rows


def test_release_charge_pump_checker_requires_up_dn_pulse_polarity() -> None:
    assert sim.check_release_charge_pump(_release_charge_pump_rows())[0]
    ok, note = sim.check_release_charge_pump(_release_charge_pump_rows(swapped=True))
    assert not ok
    assert "charge_pump_polarity" in note


def _cppll_tracking_rows(*, lock_low: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for idx in range(int(5.0e-6 / 5.0e-9) + 1):
        time_s = idx * 5.0e-9
        ref = 0.9 if idx % 4 < 2 else 0.0
        fb = 0.9 if idx % 4 < 2 else 0.0
        rows.append(
            {
                "time": time_s,
                "ref_clk": ref,
                "fb_clk": fb,
                "lock": 0.0 if lock_low else (0.9 if time_s >= 1.0e-6 else 0.0),
                "vctrl_mon": 0.45,
            }
        )
    return rows


def test_cppll_tracking_checker_requires_late_lock_assertion() -> None:
    assert sim.check_cppll_tracking(_cppll_tracking_rows())[0]
    ok, note = sim.check_cppll_tracking(_cppll_tracking_rows(lock_low=True))
    assert not ok
    assert "late_lock_frac" in note


def _simultaneous_event_rows(*, bad_levels: bool = False, shifted_ref: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    edges = [10e-9, 30e-9, 50e-9, 70e-9]
    levels = [0.18, 0.36, 0.54, 0.72]
    if bad_levels:
        levels = [0.18, 0.32, 0.46, 0.60]
    for edge, level in zip(edges, levels):
        ref_edge = edge + (1.0e-9 if shifted_ref else 0.0)
        rows.append({"time": ref_edge - 0.2e-9, "ref": 0.0, "out": level})
        rows.append({"time": ref_edge, "ref": 0.9, "out": level})
        rows.append({"time": ref_edge + 1.0e-9, "ref": 0.0, "out": level})
        for offset in (2e-9, 5e-9, 8e-9):
            rows.append({"time": edge + offset, "ref": 0.0, "out": level})
    return sorted(rows, key=lambda row: row["time"])


def test_simultaneous_event_order_checker_requires_timed_ref_edges_and_encoded_plateaus() -> None:
    assert sim.check_simultaneous_event_order(_simultaneous_event_rows())[0]
    assert not sim.check_simultaneous_event_order(_simultaneous_event_rows(bad_levels=True))[0]
    assert not sim.check_simultaneous_event_order(_simultaneous_event_rows(shifted_ref=True))[0]


def _conversion_event_controller_rows(*, missing_timeout_readout: bool = False, extra_cmp_done: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for idx in range(171):
        t = idx * 1.0e-9
        rst = 0.9 if t <= 5e-9 else 0.0
        start = 0.9 if (10e-9 <= t <= 12e-9 or 90e-9 <= t <= 92e-9) else 0.0
        cmp_done = 0.9 if 36e-9 <= t <= 39e-9 else 0.0
        if extra_cmp_done and 118e-9 <= t <= 121e-9:
            cmp_done = 0.9
        sample = 0.9 if (10e-9 <= t < 22e-9 or 90e-9 <= t < 102e-9) else 0.0
        compare = 0.9 if (22e-9 <= t < 36e-9 or 102e-9 <= t < 130e-9) else 0.0
        readout = 0.9 if (36e-9 <= t < 52e-9 or 130e-9 <= t < 146e-9) else 0.0
        if missing_timeout_readout and t >= 120e-9:
            readout = 0.0
        done = 0.9 if (52e-9 <= t < 60e-9 or 146e-9 <= t < 154e-9) else 0.0
        if rst > 0.45:
            sample = compare = readout = done = 0.0
        if sample > 0.45:
            state = 0.225
        elif compare > 0.45:
            state = 0.450
        elif readout > 0.45:
            state = 0.675
        elif done > 0.45:
            state = 0.900
        else:
            state = 0.0
        rows.append(
            {
                "time": t,
                "rst": rst,
                "start": start,
                "cmp_done": cmp_done,
                "sample_en": sample,
                "compare_en": compare,
                "readout_en": readout,
                "done": done,
                "state_mon": state,
            }
        )
    return rows


def test_conversion_event_controller_checker_requires_normal_and_timeout_transactions() -> None:
    assert sim.check_conversion_event_controller(_conversion_event_controller_rows())[0]
    assert not sim.check_conversion_event_controller(_conversion_event_controller_rows(missing_timeout_readout=True))[0]
    assert not sim.check_conversion_event_controller(_conversion_event_controller_rows(extra_cmp_done=True))[0]


def _serializer_frame_monitor_rows(*, bad_word_mon: bool = False, frame_error: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    bit_events = []
    for base_t, word in ((16e-9, 0xA5), (86e-9, 0x3C)):
        bits = [(word >> bit) & 1 for bit in range(7, -1, -1)]
        for offset, bit in enumerate(bits):
            bit_events.append((base_t + offset * 5e-9, bit, offset == 0, word, offset == 7))
    for idx in range(281):
        t = idx * 0.5e-9
        phase = (t - 1e-9) % 5e-9
        clk = 0.9 if t >= 1e-9 and phase < 2.5e-9 else 0.0
        load = 0.9 if (2e-9 <= t <= 12e-9 or 72e-9 <= t <= 82e-9) else 0.0
        sout = 0.0
        frame = 0.0
        word_ok = 0.0
        word_mon = 0.0
        for edge_t, bit, is_frame, word, is_last in bit_events:
            if edge_t <= t < edge_t + 5e-9:
                sout = 0.9 if bit else 0.0
                frame = 0.9 if is_frame else 0.0
            if is_last and edge_t <= t < edge_t + 5e-9:
                word_ok = 0.9
                word_mon = 0.9 * word / 255.0
        if t >= 121e-9:
            word_mon = 0.9 * 0x3C / 255.0
        elif t >= 51e-9:
            word_mon = 0.9 * 0xA5 / 255.0
        if bad_word_mon and t >= 51e-9:
            word_mon = 0.05
        rows.append(
            {
                "time": t,
                "clk": clk,
                "load": load,
                "frame": frame,
                "sout": sout,
                "word_ok": word_ok,
                "frame_error": 0.9 if frame_error and 100e-9 <= t <= 102e-9 else 0.0,
                "word_mon": word_mon,
                "din7": 0.9 if t < 70e-9 else 0.0,
                "din6": 0.0,
                "din5": 0.9,
                "din4": 0.0 if t < 70e-9 else 0.9,
                "din3": 0.0 if t < 70e-9 else 0.9,
                "din2": 0.9,
                "din1": 0.0,
                "din0": 0.9 if t < 70e-9 else 0.0,
            }
        )
    return rows


def test_serializer_frame_monitor_checker_requires_word_monitor_and_error_flag() -> None:
    assert sim.check_serializer_frame_monitor_flow(_serializer_frame_monitor_rows())[0]
    assert not sim.check_serializer_frame_monitor_flow(_serializer_frame_monitor_rows(bad_word_mon=True))[0]
    assert not sim.check_serializer_frame_monitor_flow(_serializer_frame_monitor_rows(frame_error=True))[0]


def _final_step_metric_rows(*, bad_levels: bool = False, missing_edge: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    edges = [10e-9, 30e-9, 50e-9, 70e-9]
    levels = [0.225, 0.45, 0.675, 0.9]
    if bad_levels:
        levels = [0.225, 0.35, 0.50, 0.62]
    if missing_edge:
        edges = edges[:-1]
        levels = levels[:-1]
    for edge, level in zip(edges, levels):
        rows.append({"time": edge - 0.2e-9, "ref": 0.0, "metric_out": level})
        rows.append({"time": edge, "ref": 0.9, "metric_out": level})
        rows.append({"time": edge + 1.0e-9, "ref": 0.0, "metric_out": level})
        for offset in (2e-9, 5e-9, 8e-9):
            rows.append({"time": edge + offset, "ref": 0.0, "metric_out": level})
    return sorted(rows, key=lambda row: row["time"])


def test_final_step_metric_checker_requires_exact_edge_count_and_normalized_plateaus() -> None:
    assert sim.check_final_step_file_metric(_final_step_metric_rows())[0]
    assert not sim.check_final_step_file_metric(_final_step_metric_rows(bad_levels=True))[0]
    assert not sim.check_final_step_file_metric(_final_step_metric_rows(missing_edge=True))[0]


def _gain_estimator_rows(*, bad_gain_out: bool = False, missing_valid: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for idx in range(240):
        time = idx * 1e-9
        phase = 2.0 * math.pi * idx / 40.0
        vin_diff = 0.03 * math.sin(phase)
        vout_diff = 0.18 * math.sin(phase)
        valid = 0.9 if time >= 60e-9 and not missing_valid else 0.0
        gain = 2.0 if bad_gain_out else 6.0
        rows.append(
            {
                "time": time,
                "vinp": 0.45 + 0.5 * vin_diff,
                "vinn": 0.45 - 0.5 * vin_diff,
                "voutp": 0.45 + 0.5 * vout_diff,
                "voutn": 0.45 - 0.5 * vout_diff,
                "gain_out": 0.9 * gain / 10.0,
                "valid": valid,
            }
        )
    return rows


def test_gain_estimator_checker_requires_late_valid_and_gain_output() -> None:
    assert sim.check_gain_estimator(_gain_estimator_rows())[0]
    assert not sim.check_gain_estimator(_gain_estimator_rows(bad_gain_out=True))[0]
    assert not sim.check_gain_estimator(_gain_estimator_rows(missing_valid=True))[0]


def test_final_step_metric_side_output_requires_candidate_file(tmp_path: Path) -> None:
    csv_path = tmp_path / "out" / "tran.csv"
    csv_path.parent.mkdir()
    csv_path.write_text("time,ref,metric_out\n", encoding="utf-8")

    missing_ok, missing_note = sim.validate_behavior_side_outputs(
        "final_step_file_metric_smoke",
        tmp_path,
        csv_path,
    )
    assert not missing_ok
    assert missing_note == "candidate_file_missing"

    (tmp_path / "candidate.out").write_text("count=3 metric=0.750", encoding="utf-8")
    bad_ok, bad_note = sim.validate_behavior_side_outputs(
        "final_step_file_metric_smoke",
        tmp_path,
        csv_path,
    )
    assert not bad_ok
    assert "candidate_file_count=3" in bad_note

    (tmp_path / "candidate.out").write_text("count=4 metric=1.000", encoding="utf-8")
    ok, note = sim.validate_behavior_side_outputs(
        "final_step_file_metric_smoke",
        tmp_path,
        csv_path,
    )
    assert ok
    assert "candidate_file_count=4" in note


def _gain_trim_rows(*, cap_upper: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    ctrl = 0.30
    previous_clk = 0.0
    for idx in range(1241):
        time_s = idx * 0.5e-9
        t_ns = time_s * 1e9
        phase = (t_ns - 10.0) % 20.0
        clk = 0.9 if t_ns >= 10.0 and phase < 5.0 else 0.0
        rst = 0.9 if t_ns <= 15.0 else 0.0
        meas = 0.2 if t_ns <= 260.0 else 0.7
        target = 0.45
        if previous_clk <= 0.45 < clk:
            if rst > 0.45:
                ctrl = 0.30
            elif meas < target - 0.02:
                ctrl += 0.05
            elif meas > target + 0.02:
                ctrl -= 0.05
            upper = 0.75 if cap_upper else 0.85
            ctrl = min(max(ctrl, 0.05), upper)
        previous_clk = clk
        rows.append({"time": time_s, "clk": clk, "rst": rst, "meas": meas, "target": target, "gain_ctrl": ctrl})
    return rows


def test_gain_trim_checker_requires_both_clamps() -> None:
    assert sim.check_vbm1_gain_trim_controller(_gain_trim_rows())[0]
    ok, note = sim.check_vbm1_gain_trim_controller(_gain_trim_rows(cap_upper=True))
    assert not ok
    assert "reaches_upper_clamp=False" in note


def _differential_driver_rows(
    *, ignore_enable: bool = False, inverted: bool = False
) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for idx in range(100):
        time = idx * 1e-9
        if idx < 12:
            en = 0.0
            din = 0.0
        elif idx < 35:
            en = 0.9
            din = 0.0
        elif idx < 58:
            en = 0.9
            din = 0.9
        elif idx < 75:
            en = 0.0
            din = 0.9
        else:
            en = 0.9
            din = 0.0
        enabled = en > 0.45 or ignore_enable
        if not enabled:
            diff = 0.0
        else:
            diff = 0.4 if din > 0.45 else -0.4
        if inverted:
            diff = -diff
        rows.append(
            {
                "time": time,
                "din": din,
                "en": en,
                "outp": 0.45 + 0.5 * diff,
                "outn": 0.45 - 0.5 * diff,
            }
        )
    return rows


def test_differential_driver_checker_rejects_enable_and_polarity_bugs() -> None:
    assert sim.check_differential_voltage_output(_differential_driver_rows())[0]
    assert not sim.check_differential_voltage_output(
        _differential_driver_rows(ignore_enable=True)
    )[0]
    assert not sim.check_differential_voltage_output(
        _differential_driver_rows(inverted=True)
    )[0]


def _therm_rows(*, nonmonotonic: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for count in [0, 4, 8, 12, 16]:
        row = {"time": float(count), "vout": float(count)}
        if nonmonotonic and count == 12:
            row["vout"] = 3.0
        for bit in range(16):
            row[f"d{bit}"] = 0.9 if bit < count else 0.0
        rows.append(row)
    return rows


def test_thermometer_dac_checker_rejects_nonmonotonic_output() -> None:
    assert sim.check_dac_therm_16b(_therm_rows())[0]
    assert not sim.check_dac_therm_16b(_therm_rows(nonmonotonic=True))[0]


def _therm15_rows(*, omit_full_scale_segment: bool = False) -> list[dict[str, float]]:
    checkpoints = [
        (15e-9, 0),
        (45e-9, 1),
        (75e-9, 2),
        (105e-9, 7),
        (135e-9, 14),
        (165e-9, 15),
    ]
    rows: list[dict[str, float]] = []
    for time, count in checkpoints:
        effective_count = 14 if omit_full_scale_segment and count == 15 else count
        row = {"time": time, "aout": 0.9 * effective_count / 15.0}
        for bit in range(15):
            row[f"seg{bit}"] = 0.9 if bit < effective_count else 0.0
        rows.append(row)
    return rows


def test_thermometer_dac_15seg_checker_rejects_missing_full_scale_segment() -> None:
    assert sim.check_vbm1_thermometer_dac_15seg(_therm15_rows())[0]
    assert not sim.check_vbm1_thermometer_dac_15seg(
        _therm15_rows(omit_full_scale_segment=True)
    )[0]


def _pfd_small_phase_rows(*, sustained_overlap: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for idx in range(1000):
        phase = idx % 50
        up = 0.9 if phase in {2, 3} else 0.0
        dn = 0.9 if sustained_overlap and 2 <= phase <= 18 else 0.0
        rows.append(
            {
                "time": float(idx),
                "ref": 0.9 if phase < 25 else 0.0,
                "div": 0.9 if 5 <= phase < 30 else 0.0,
                "up": up,
                "dn": dn,
            }
        )
    return rows


def test_pfd_small_phase_checker_rejects_sustained_overlap() -> None:
    assert sim.check_pfd_small_phase_error_response(_pfd_small_phase_rows())[0]
    assert not sim.check_pfd_small_phase_error_response(
        _pfd_small_phase_rows(sustained_overlap=True)
    )[0]


def _retriggerable_stretcher_rows(*, ignore_retrigger: bool = False) -> list[dict[str, float]]:
    times_ns = [
        0.0,
        1.0,
        1.1,
        1.3,
        1.8,
        3.0,
        3.1,
        3.3,
        4.4,
        5.0,
        6.4,
        8.4,
        10.4,
        16.0,
        16.1,
        16.3,
        17.2,
        18.0,
        18.1,
        18.3,
        19.4,
        21.4,
        23.4,
        24.0,
        24.1,
        24.3,
        24.6,
        25.1,
        26.0,
        28.1,
    ]
    trig_pulses = [(1.1, 1.3), (3.1, 3.3), (16.1, 16.3), (18.1, 18.3), (24.1, 24.3)]
    rows: list[dict[str, float]] = []
    for time_ns in times_ns:
        trig = 0.9 if any(lo <= time_ns <= hi for lo, hi in trig_pulses) else 0.0
        rst = 0.9 if 25.1 <= time_ns <= 28.0 else 0.0
        if ignore_retrigger:
            pulse_high = (1.1 <= time_ns <= 5.1) or (16.1 <= time_ns <= 20.1) or (24.1 <= time_ns < 25.1)
        else:
            pulse_high = (1.1 <= time_ns <= 7.1) or (16.1 <= time_ns <= 22.1) or (24.1 <= time_ns < 25.1)
        rows.append(
            {
                "time": time_ns * 1e-9,
                "trig": trig,
                "rst": rst,
                "pulse": 0.9 if pulse_high and rst < 0.45 else 0.0,
            }
        )
    return rows


def test_retriggerable_pulse_stretcher_checker_requires_burst_extension() -> None:
    assert sim.check_release_event_pulse_stretcher(_retriggerable_stretcher_rows())[0]
    assert not sim.check_release_event_pulse_stretcher(
        _retriggerable_stretcher_rows(ignore_retrigger=True)
    )[0]


def _code_capture_row(time_ns: float, *, clk: bool = False, load: bool = False, word: int = 0, over: bool = False) -> dict[str, float]:
    row = {
        "time": time_ns * 1e-9,
        "clk": 0.9 if clk else 0.0,
        "load": 0.9 if load else 0.0,
        "over_lo": 0.0,
        "over_hi": 0.9 if over else 0.0,
        "valid": 0.9 if time_ns >= 21.0 else 0.0,
        "overrange": 0.9 if over else 0.0,
        "code_mon": 0.9 * word / 15.0,
    }
    for bit in range(4):
        row[f"din{bit}"] = 0.9 if (word >> bit) & 1 else 0.0
        row[f"bit{bit}"] = 0.9 if (word >> bit) & 1 else 0.0
    return row


def _adc_code_capture_rows(*, drift_between_loads: bool = False) -> list[dict[str, float]]:
    rows = [
        _code_capture_row(0.0, word=0),
        _code_capture_row(19.9, word=0),
        _code_capture_row(20.0, clk=True, load=True, word=3),
        _code_capture_row(21.0, word=3),
        _code_capture_row(35.0, word=3),
        _code_capture_row(59.9, word=3),
        _code_capture_row(60.0, clk=True, load=True, word=12),
        _code_capture_row(61.0, word=12),
        _code_capture_row(75.0, word=2 if drift_between_loads else 12),
        _code_capture_row(99.9, word=12),
        _code_capture_row(100.0, clk=True, load=True, word=15, over=True),
        _code_capture_row(101.0, word=15, over=True),
    ]
    return rows


def test_adc_code_capture_checker_requires_load_gated_hold_and_overrange() -> None:
    assert sim.check_adc_code_capture_register(_adc_code_capture_rows())[0]
    assert not sim.check_adc_code_capture_register(
        _adc_code_capture_rows(drift_between_loads=True)
    )[0]


def _deser_row(time_ns: float, *, clk: bool = False, frame: bool = False, sin: bool = False, word: int = 0, valid: bool = False) -> dict[str, float]:
    row = {
        "time": time_ns * 1e-9,
        "clk": 0.9 if clk else 0.0,
        "frame": 0.9 if frame else 0.0,
        "sin": 0.9 if sin else 0.0,
        "word_valid": 0.9 if valid else 0.0,
        "word_mon": 0.9 * word / 15.0,
    }
    for bit in range(4):
        row[f"bit{bit}"] = 0.9 if (word >> bit) & 1 else 0.0
    return row


def _serial_deserializer_rows(*, wrong_word: bool = False) -> list[dict[str, float]]:
    first = 0x6 if wrong_word else 0x9
    return [
        _deser_row(0.0),
        _deser_row(19.9),
        _deser_row(20.0, clk=True, frame=True, sin=True),
        _deser_row(30.0, clk=True, sin=False),
        _deser_row(40.0, clk=True, sin=False),
        _deser_row(50.0, clk=True, sin=True, word=first, valid=True),
        _deser_row(51.0, word=first, valid=True),
        _deser_row(60.0, word=first),
        _deser_row(69.9, word=first),
        _deser_row(70.0, clk=True, frame=True, sin=False, word=first),
        _deser_row(80.0, clk=True, sin=True, word=first),
        _deser_row(90.0, clk=True, sin=True, word=first),
        _deser_row(100.0, clk=True, sin=False, word=0x6, valid=True),
        _deser_row(101.0, word=0x6, valid=True),
    ]


def test_serial_readout_deserializer_checker_requires_msb_first_words() -> None:
    assert sim.check_serial_readout_deserializer(_serial_deserializer_rows())[0]
    assert not sim.check_serial_readout_deserializer(_serial_deserializer_rows(wrong_word=True))[0]


def _vin_sampled_droop_hold_rows(*, mode: str = "good") -> list[dict[str, float]]:
    sample_edges_ns = [20.0, 80.0, 145.0]
    reset_start_ns = 120.0
    reset_end_ns = 136.0

    def vin_at(time_ns: float) -> float:
        if time_ns < 55.0:
            return 0.20
        if time_ns < 110.0:
            return 0.72
        if time_ns < 138.0:
            return 0.34
        return 0.34

    rows: list[dict[str, float]] = []
    held = 0.0
    last_sample_idx = -1
    for idx in range(341):
        time_ns = idx * 0.5
        reset_high = reset_start_ns <= time_ns <= reset_end_ns
        sample_high = any(edge <= time_ns <= edge + 2.0 for edge in sample_edges_ns)

        for sample_idx, edge in enumerate(sample_edges_ns):
            if time_ns == edge and not reset_high:
                last_sample_idx = sample_idx
                held = 0.75 if mode == "fixed_internal_level" else vin_at(time_ns)

        if reset_high and mode != "ignore_reset":
            held = 0.0
        elif last_sample_idx >= 0 and mode != "no_droop":
            held *= 0.992

        rows.append(
            {
                "time": time_ns * 1e-9,
                "sample": 0.9 if sample_high else 0.0,
                "rst": 0.9 if reset_high else 0.0,
                "vin": vin_at(time_ns),
                "vout": held,
            }
        )
    return rows


def test_vin_sampled_droop_hold_checker_requires_input_capture_droop_and_reset() -> None:
    assert sim.check_release_vin_sampled_droop_hold(_vin_sampled_droop_hold_rows())[0]
    assert not sim.check_release_vin_sampled_droop_hold(
        _vin_sampled_droop_hold_rows(mode="fixed_internal_level")
    )[0]
    assert not sim.check_release_vin_sampled_droop_hold(
        _vin_sampled_droop_hold_rows(mode="no_droop")
    )[0]
    assert not sim.check_release_vin_sampled_droop_hold(
        _vin_sampled_droop_hold_rows(mode="ignore_reset")
    )[0]


def _acquisition_limited_sample_hold_rows(*, mode: str = "good") -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    held = 0.45
    tracking = False
    for idx in range(181):
        time_ns = idx * 0.5
        rst = time_ns <= 2.0
        sample = 5.0 <= time_ns < 10.0
        vin = 0.25
        if rst:
            held = 0.45
            tracking = False
        elif sample and not tracking:
            tracking = True
            if mode == "instantaneous":
                held = vin
        elif not sample:
            tracking = False

        if sample and mode != "instantaneous" and abs(time_ns - round(time_ns)) < 1e-12:
            held = held + 0.42 * (vin - held)
        if not sample and mode == "hold_drift" and time_ns > 10.0:
            held += 0.003

        rows.append(
            {
                "time": time_ns * 1e-9,
                "sample": 0.9 if sample else 0.0,
                "rst": 0.9 if rst else 0.0,
                "vin": vin,
                "vout": held,
                "metric": 0.9 if sample else 0.0,
            }
        )
    return rows


def test_acquisition_limited_sample_hold_checker_rejects_ideal_jump_and_hold_drift() -> None:
    assert sim.check_acquisition_limited_sample_hold(_acquisition_limited_sample_hold_rows())[0]
    assert not sim.check_acquisition_limited_sample_hold(
        _acquisition_limited_sample_hold_rows(mode="instantaneous")
    )[0]
    assert not sim.check_acquisition_limited_sample_hold(
        _acquisition_limited_sample_hold_rows(mode="hold_drift")
    )[0]


def _converter_front_end_chain_rows(*, mode: str = "good") -> list[dict[str, float]]:
    edges_ns = [5.0 + 20.0 * idx for idx in range(9)]
    aperture_levels = [0.18, 0.72, 0.32, 0.78, 0.40, 0.70, 0.25, 0.65, 0.38]
    pre_levels = [0.18, 0.18, 0.72, 0.32, 0.78, 0.40, 0.70, 0.25, 0.65]
    rows: list[dict[str, float]] = []

    def add(time_ns: float, clk: float, vin: float, vout: float, valid: float, coarse: float) -> None:
        rows.append(
            {
                "time": time_ns * 1e-9,
                "clk": clk,
                "vin": vin,
                "vout": vout,
                "valid": valid,
                "coarse": coarse,
            }
        )

    held = 0.0
    coarse = 0.0
    for idx, edge_ns in enumerate(edges_ns):
        pre = pre_levels[idx]
        aperture = aperture_levels[idx]
        sampled = pre if mode == "sample_edge_not_aperture" else aperture
        coarse = 0.9 if sampled > 0.45 else 0.0
        if mode == "wrong_coarse" and idx in {1, 3}:
            coarse = 0.0 if coarse > 0.45 else 0.9

        add(edge_ns, 0.45, pre, held, 0.0, coarse)
        add(edge_ns + 0.001, 0.9, pre, held, 0.0, coarse)
        add(edge_ns + 0.2, 0.9, aperture, held, 0.0, coarse)
        add(edge_ns + 0.8, 0.9, aperture, sampled, 0.9, coarse)
        add(edge_ns + 1.0, 0.9, aperture, sampled, 0.9, coarse)
        add(edge_ns + 3.5, 0.9, aperture, sampled, 0.9 if mode == "valid_stuck_high" else 0.0, coarse)
        add(edge_ns + 8.0, 0.0, aperture, sampled, 0.0, coarse)

        held = sampled
        if idx + 1 < len(edges_ns):
            next_edge = edges_ns[idx + 1]
            window_points = [edge_ns + offset for offset in (9, 10, 11, 12, 13, 14, 15, 16, 17, 18)]
            for point_idx, time_ns in enumerate(window_points):
                if time_ns >= next_edge - 1.5:
                    continue
                if held > 0.55:
                    droop = 0.0 if mode == "no_hold_droop" else 0.006 * point_idx
                    vout = held - droop
                else:
                    vout = held
                add(time_ns, 0.0, aperture, vout, 0.0, coarse)
            if held > 0.55 and mode != "no_hold_droop":
                held = max(0.0, held - 0.006 * 8)

    return sorted(rows, key=lambda row: row["time"])


def test_converter_front_end_checker_requires_aperture_coarse_valid_and_droop() -> None:
    assert sim.check_release_converter_front_end_chain(_converter_front_end_chain_rows())[0]
    assert not sim.check_release_converter_front_end_chain(
        _converter_front_end_chain_rows(mode="sample_edge_not_aperture")
    )[0]
    assert not sim.check_release_converter_front_end_chain(
        _converter_front_end_chain_rows(mode="wrong_coarse")
    )[0]
    assert not sim.check_release_converter_front_end_chain(
        _converter_front_end_chain_rows(mode="valid_stuck_high")
    )[0]
    assert not sim.check_release_converter_front_end_chain(
        _converter_front_end_chain_rows(mode="no_hold_droop")
    )[0]


def _ct04_common_vin(time_ns: float) -> float:
    if time_ns < 8.0:
        return 0.45
    if time_ns < 12.0:
        return 0.45 + (0.9 - 0.45) * (time_ns - 8.0) / 4.0
    if time_ns < 28.0:
        return 0.9
    if time_ns < 31.0:
        return 0.9 + (0.45 - 0.9) * (time_ns - 28.0) / 3.0
    if time_ns < 37.0:
        return 0.45
    if time_ns < 42.0:
        return 0.45 + (0.1 - 0.45) * (time_ns - 37.0) / 5.0
    if time_ns < 58.0:
        return 0.1
    if time_ns < 61.0:
        return 0.1 + (0.45 - 0.1) * (time_ns - 58.0) / 3.0
    if time_ns < 67.0:
        return 0.45
    if time_ns < 72.0:
        return 0.45 + (0.85 - 0.45) * (time_ns - 67.0) / 5.0
    return 0.85


def _ct04_rows(kind: str, *, mode: str = "good") -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for idx in range(161):
        time_ns = idx * 0.5
        clk = 0.9 if (time_ns % 2.0) < 1.0 else 0.0
        rst = 0.9 if time_ns <= 2.0 else 0.0
        vin = _ct04_common_vin(time_ns)
        out = 0.45
        metric = 0.45

        if kind == "gain":
            target = 1.8 * (vin - 0.45) + 0.45
            clipped = max(0.0, min(0.9, target))
            out = target if mode == "unclamped" else clipped
            metric = 0.0 if mode == "flat_metric" else (0.9 if clipped != target else 0.0)
            if rst > 0.45:
                out = 0.45
                metric = 0.0
        elif kind == "two_pole":
            if 14.0 <= time_ns <= 16.0:
                out, metric = 0.56, 0.62
            elif 24.0 <= time_ns <= 28.0:
                out, metric = 0.76, 0.54
            elif 44.0 <= time_ns <= 52.0:
                out, metric = 0.40, 0.32
            elif 54.0 <= time_ns <= 58.0:
                out, metric = 0.22, 0.36
            if mode == "single_pole":
                if 14.0 <= time_ns <= 16.0:
                    out = 0.78
                metric = 0.45
        elif kind == "soft_limiter":
            if 16.0 <= time_ns <= 24.0:
                out, metric = 0.80, 0.65
            elif 31.0 <= time_ns <= 36.0:
                out, metric = 0.51, 0.65
            elif 46.0 <= time_ns <= 55.0:
                out, metric = 0.12, 0.25
            elif 61.0 <= time_ns <= 66.0:
                out, metric = 0.39, 0.25
            if mode == "memoryless":
                if 31.0 <= time_ns <= 36.0 or 61.0 <= time_ns <= 66.0:
                    out, metric = 0.45, 0.45
        elif kind == "amp_filter":
            if 12.5 <= time_ns <= 15.0:
                out, metric = 0.62, 0.90
            elif 24.0 <= time_ns <= 28.0:
                out, metric = 0.84, 0.90
            elif 33.0 <= time_ns <= 36.0:
                out, metric = 0.70, 0.45
            elif 46.0 <= time_ns <= 53.5:
                out, metric = 0.42, 0.0
            elif 54.0 <= time_ns <= 58.0:
                out, metric = 0.25, 0.0
            if mode == "direct_gain":
                out = metric
        else:
            raise ValueError(kind)

        rows.append({"time": time_ns * 1e-9, "clk": clk, "rst": rst, "vin": vin, "out": out, "metric": metric})
    return rows


def _rectifier_envelope_rows(*, mode: str = "good") -> list[dict[str, float]]:
    knots = [
        (0.0, 0.45),
        (8.0, 0.75),
        (16.0, 0.45),
        (24.0, 0.15),
        (32.0, 0.45),
        (42.0, 0.85),
        (54.0, 0.45),
        (66.0, 0.35),
        (78.0, 0.45),
        (90.0, 0.45),
    ]

    def interp(time_ns: float) -> float:
        for (t0, v0), (t1, v1) in zip(knots, knots[1:]):
            if t0 <= time_ns <= t1:
                frac = (time_ns - t0) / (t1 - t0)
                return v0 + frac * (v1 - v0)
        return knots[-1][1]

    rows: list[dict[str, float]] = []
    env = 0.45
    for idx in range(181):
        time_ns = idx * 0.5
        rst = 0.9 if time_ns <= 2.0 else 0.0
        clk = 0.9 if (time_ns % 2.0) < 1.0 else 0.0
        vin = interp(time_ns)
        rect = min(0.9, 0.45 + abs(vin - 0.45))
        if mode == "half_wave":
            rect = vin if vin > 0.45 else 0.45

        if rst > 0.45:
            env = 0.45
        elif mode == "no_envelope":
            env = rect
        else:
            env = max(rect, max(0.45, env - 0.006))
        metric = 0.9 if env - rect > 0.03 else 0.0
        rows.append(
            {
                "time": time_ns * 1e-9,
                "clk": clk,
                "rst": rst,
                "vin": vin,
                "rect": rect,
                "env": env,
                "metric": metric,
            }
        )
    return rows


def test_precision_rectifier_envelope_checker_requires_full_wave_and_hold() -> None:
    assert sim.check_precision_rectifier_envelope_detector(_rectifier_envelope_rows())[0]
    assert not sim.check_precision_rectifier_envelope_detector(_rectifier_envelope_rows(mode="half_wave"))[0]
    assert not sim.check_precision_rectifier_envelope_detector(_rectifier_envelope_rows(mode="no_envelope"))[0]


def _sar_adc_dac_rows(*, mode: str = "good") -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    vdd = 0.9

    def append_row(time_s: float, clks: float, rst_n: float, vin: float, vin_sh: float, code: int, vout: float) -> None:
        row = {
            "time": time_s,
            "vin": vin,
            "vin_sh": vin_sh,
            "clks": clks,
            "rst_n": rst_n,
            "vout": vout,
        }
        for bit in range(8):
            row[f"dout_{bit}"] = vdd if (code >> bit) & 1 else 0.0
        rows.append(row)

    for cycle in range(502):
        base = cycle * 20.0e-9
        rst_n = vdd if cycle >= 4 else 0.0
        sample_time = base + 1.0e-9
        vin = 0.45 + 0.45 * math.sin(2.0 * math.pi * 100.0e3 * sample_time)
        vin = max(0.0, min(vdd, vin))
        code = max(0, min(255, int(math.floor(vin / vdd * 255.0))))
        vout = code / 255.0 * vdd

        if mode == "vout_tracks_input_but_code_fake":
            code = (cycle * 37) % 256
            vout = vin
        elif mode == "code_offset":
            code = max(0, min(255, code + 40))
            vout = code / 255.0 * vdd
        elif mode != "good":
            raise ValueError(mode)

        append_row(base + 0.2e-9, 0.0, rst_n, vin, vin, code, vout)
        append_row(base + 1.0e-9, vdd, rst_n, vin, vin, code, vout)
        append_row(base + 2.5e-9, vdd, rst_n, vin, vin, code, vout)
        append_row(base + 11.0e-9, 0.0, rst_n, vin, vin, code, vout)

    return rows


def test_sar_adc_dac_checker_requires_code_dac_sample_alignment() -> None:
    assert sim.check_sar_adc_dac_weighted_8b(_sar_adc_dac_rows())[0]
    assert not sim.check_sar_adc_dac_weighted_8b(
        _sar_adc_dac_rows(mode="vout_tracks_input_but_code_fake")
    )[0]
    assert not sim.check_sar_adc_dac_weighted_8b(_sar_adc_dac_rows(mode="code_offset"))[0]


def _converter_static_linearity_rows(*, mode: str = "good") -> list[dict[str, float]]:
    recon_table = {
        0: 0.000,
        1: 0.055,
        2: 0.118,
        3: 0.182,
        4: 0.245,
        5: 0.303,
        6: 0.366,
        7: 0.428,
        8: 0.491,
        9: 0.553,
        10: 0.612,
        11: 0.674,
        12: 0.735,
        13: 0.798,
        14: 0.855,
        15: 0.900,
    }
    rows: list[dict[str, float]] = []
    code_int = 0
    recon = 0.0
    dnl = 0.45
    inl = 0.45
    prev_valid = False
    prev_code = 0
    prev_recon = 0.0
    prev_clk = 0.0
    for idx in range(385):
        time_ns = idx * 0.25
        rst = 0.9 if time_ns <= 2.0 else 0.0
        clk_phase = (time_ns - 1.0) % 4.0
        clk = 0.9 if 0.0 <= clk_phase < 2.0 else 0.0
        vin = min(0.9, max(0.0, 0.9 * max(time_ns - 4.0, 0.0) / 84.0))
        if prev_clk <= 0.45 < clk:
            if rst > 0.45:
                code_int = 0
                recon = 0.0
                dnl = 0.45
                inl = 0.45
                prev_valid = False
                prev_code = 0
                prev_recon = 0.0
            else:
                code_int = max(0, min(15, round((vin / 0.9) * 15.0)))
                recon = 0.06 * code_int if mode == "ideal_converter" else recon_table[code_int]
                inl = max(0.05, min(0.85, 0.45 + 3.0 * (recon - 0.06 * code_int)))
                if prev_valid and code_int > prev_code:
                    ideal_step = 0.06 * (code_int - prev_code)
                    dnl = max(0.05, min(0.85, 0.45 + 4.0 * ((recon - prev_recon) - ideal_step)))
                else:
                    dnl = 0.45
                if mode == "flat_metrics":
                    dnl = 0.45
                    inl = 0.45
                elif mode == "fake_metrics":
                    dnl = 0.30 + 0.015 * code_int
                    inl = 0.60 - 0.008 * code_int
                prev_code = code_int
                prev_recon = recon
                prev_valid = True
        prev_clk = clk
        rows.append(
            {
                "time": time_ns * 1e-9,
                "clk": clk,
                "rst": rst,
                "vin": vin,
                "code": 0.06 * code_int,
                "recon": recon,
                "dnl": dnl,
                "inl": inl,
            }
        )
    return rows


def test_converter_static_linearity_checker_requires_linearity_metrics() -> None:
    assert sim.check_converter_static_linearity_measurement_flow(_converter_static_linearity_rows())[0]
    assert not sim.check_converter_static_linearity_measurement_flow(
        _converter_static_linearity_rows(mode="ideal_converter")
    )[0]
    assert not sim.check_converter_static_linearity_measurement_flow(
        _converter_static_linearity_rows(mode="flat_metrics")
    )[0]
    assert not sim.check_converter_static_linearity_measurement_flow(
        _converter_static_linearity_rows(mode="fake_metrics")
    )[0]


def _programmable_stimulus_sequencer_rows(*, mode: str = "chirp") -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    prbs_state = 7
    burst_level = 0.45
    for idx in range(361):
        time_ns = idx * 0.25
        time_s = time_ns * 1e-9
        rst = 0.9 if time_ns <= 2.0 else 0.0
        clk = 0.9 if (time_ns % 2.0) < 1.0 else 0.0
        mode_v = 0.0 if time_ns < 26.0 else 0.45 if time_ns < 62.0 else 0.9
        gate = 0.9 if 66.0 <= time_ns < 76.0 or 79.5 <= time_ns <= 88.0 else 0.0

        if mode_v < 0.30:
            ramp_frac = min(1.0, max(0.0, (time_s - 3.0e-9) / 23.0e-9))
            out = 0.18 + 0.27 * ramp_frac
            metric = 0.20
        elif mode_v < 0.60:
            sweep_t = min(36.0e-9, max(0.0, time_s - 26.0e-9))
            if mode == "fixed_sine":
                phase = 2.0 * math.pi * 82.0e6 * sweep_t
            else:
                sweep_k = (116.666666e6 - 50.0e6) / 36.0e-9
                phase = 2.0 * math.pi * (50.0e6 * sweep_t + 0.5 * sweep_k * sweep_t * sweep_t)
            out = 0.45 + 0.15 * math.sin(phase)
            metric = 0.50
        elif gate > 0.45:
            if idx % 8 == 0:
                feedback = ((prbs_state >> 2) & 1) ^ ((prbs_state >> 1) & 1)
                prbs_state = ((prbs_state & 3) << 1) | feedback
                burst_level = 0.62 if (prbs_state & 1) else 0.28
            out = burst_level
            metric = 0.80
        else:
            out = 0.45
            metric = 0.65
        if rst > 0.45:
            out = 0.45
            metric = 0.0
        rows.append(
            {
                "time": time_s,
                "clk": clk,
                "rst": rst,
                "mode": mode_v,
                "gate": gate,
                "out": out,
                "metric": metric,
            }
        )
    return rows


def test_programmable_stimulus_checker_requires_chirp_sweep_not_fixed_sine() -> None:
    assert sim.check_programmable_stimulus_sequencer(_programmable_stimulus_sequencer_rows())[0]
    assert not sim.check_programmable_stimulus_sequencer(
        _programmable_stimulus_sequencer_rows(mode="fixed_sine")
    )[0]


def _programmable_gain_amplifier_rows(*, mode: str = "good") -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for idx in range(181):
        time_ns = idx * 0.5
        rst = time_ns <= 2.0
        clk = 0.9 if (time_ns % 8.0) < 4.0 else 0.0
        gain_sel = 0.9 if (20.0 <= time_ns < 48.0 or time_ns >= 72.0) else 0.0
        if time_ns < 8.0:
            vin = 0.45
        elif time_ns < 16.0:
            vin = 0.60
        elif time_ns < 28.0:
            vin = 0.30
        elif time_ns < 38.0:
            vin = 0.72
        elif time_ns < 50.0:
            vin = 0.20
        elif time_ns < 70.0:
            vin = 0.55
        elif time_ns < 83.0:
            vin = 0.85
        else:
            vin = 0.45

        if rst:
            gain = 1.0
        elif mode == "unity_gain":
            gain = 1.0
        elif gain_sel > 0.45:
            gain = 2.4
        else:
            gain = 0.8
        raw = 0.45 + gain * (vin - 0.45)
        if rst:
            out = 0.45
            metric = 0.0
        elif mode == "unbounded":
            out = raw
            metric = 0.0
        else:
            out = max(0.0, min(0.9, raw))
            metric = 0.9 if out != raw else 0.0
        rows.append(
            {
                "time": time_ns * 1e-9,
                "clk": clk,
                "rst": 0.9 if rst else 0.0,
                "gain_sel": gain_sel,
                "vin": vin,
                "out": out,
                "metric": metric,
            }
        )
    return rows


def test_programmable_gain_amplifier_checker_requires_gain_select_and_clamps() -> None:
    assert sim.check_programmable_gain_amplifier(_programmable_gain_amplifier_rows())[0]
    assert not sim.check_programmable_gain_amplifier(
        _programmable_gain_amplifier_rows(mode="unity_gain")
    )[0]
    assert not sim.check_programmable_gain_amplifier(
        _programmable_gain_amplifier_rows(mode="unbounded")
    )[0]


def test_two_pole_filter_checker_requires_lag_and_state_difference_metric() -> None:
    assert sim.check_release_two_pole_filter(_ct04_rows("two_pole"))[0]
    assert not sim.check_release_two_pole_filter(_ct04_rows("two_pole", mode="single_pole"))[0]


def test_soft_hysteretic_limiter_checker_requires_memory_state() -> None:
    assert sim.check_release_soft_hysteretic_limiter(_ct04_rows("soft_limiter"))[0]
    assert not sim.check_release_soft_hysteretic_limiter(
        _ct04_rows("soft_limiter", mode="memoryless")
    )[0]


def test_amplifier_filter_chain_checker_requires_preamp_metric_and_lagged_output() -> None:
    assert sim.check_release_amplifier_filter_chain(_ct04_rows("amp_filter"))[0]
    assert not sim.check_release_amplifier_filter_chain(
        _ct04_rows("amp_filter", mode="direct_gain")
    )[0]
