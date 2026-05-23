from __future__ import annotations

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
    "vbr1_l1_differential_output_driver",
    "vbr1_l1_digital_phase_accumulator_with_modulo_wrap",
    "vbr1_l1_dither_or_noise_like_deterministic_source",
    "vbr1_l1_dwa_dem_encoder",
    "vbr1_l1_hysteresis_comparator",
    "vbr1_l1_pfd_small_phase_error_response",
    "vbr1_l1_propagation_delay_comparator",
    "vbr1_l1_ramp_or_step_source",
    "vbr1_l1_serializer_frame_aligner",
    "vbr1_l1_threshold_comparator",
    "vbr1_l1_unit_element_thermometer_dac",
    "vbr1_l1_window_comparator_detector",
    "vbr1_l1_xor_phase_detector",
}


def test_promoted_duts_have_release_behavior_aliases() -> None:
    for entry_id in PROMOTED_DUTS:
        assert sim.has_behavior_check(f"{entry_id}_dut"), entry_id


def test_noise_source_checker_rejects_flat_passthrough() -> None:
    ok_rows = [
        {"time": idx, "vin_i": 1.0, "vout_o": 1.0 + delta}
        for idx, delta in enumerate([0.08, -0.04, 0.06, -0.07, 0.03, -0.09])
    ]
    bad_rows = [{"time": idx, "vin_i": 1.0, "vout_o": 1.0} for idx in range(6)]

    assert sim.check_noise_gen(ok_rows)[0]
    assert not sim.check_noise_gen(bad_rows)[0]


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
