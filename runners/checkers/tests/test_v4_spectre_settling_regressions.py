from __future__ import annotations

from collections.abc import Iterable

from runners.checkers.v4.registry import load_checker


VDD = 0.9


def _passes(checker_id: str, rows: list[dict[str, float]]) -> tuple[bool, str]:
    checker = load_checker(checker_id)
    assert checker is not None
    return checker(rows)


def _logic(value: bool) -> float:
    return VDD if value else 0.0


def _ramp_step_rows(
    *,
    transition_guard_sample: bool = True,
    bad_phase: bool = False,
    bad_guard_plateau: bool = False,
) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    period = 1e-9
    fractions = (0.0, 0.10, 0.20, 0.35, 0.45, 0.55, 0.60, 0.61, 0.625, 0.65, 0.70, 0.875, 0.95)
    for cycle in range(7):
        for frac in fractions:
            t = cycle * period + frac * period
            guard = VDD if 0.35 <= frac <= 0.60 else 0.0
            if bad_guard_plateau and 0.35 <= frac <= 0.60:
                guard = 0.83
            if transition_guard_sample and cycle == 3 and frac == 0.61:
                guard = 0.875 * VDD
            if transition_guard_sample and cycle == 3 and frac == 0.625:
                guard = 0.30 * VDD
            rows.append(
                {
                    "time": t,
                    "phase_out": 0.0 if bad_phase and cycle >= 2 else VDD * frac,
                    "guard_out": guard,
                    "VDD": VDD,
                    "VSS": 0.0,
                }
            )
    return rows


def test_079_guard_transition_sample_is_not_scored_as_settled() -> None:
    ok, note = _passes("v4_079_ramp_step_source", _ramp_step_rows())
    assert ok, note


def test_079_stable_off_rail_guard_plateau_still_fails() -> None:
    ok, _note = _passes(
        "v4_079_ramp_step_source",
        _ramp_step_rows(transition_guard_sample=False, bad_guard_plateau=True),
    )
    assert not ok


def _task311_rows(*, wrong_metric_platform: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    held = [0.18, 0.52, 0.78]
    schedule: list[tuple[int, bool, bool, int, int]] = [
        (24, True, False, 0, 0),
        (40, False, True, 0, 0),
        (32, False, False, 0, 0),
        (48, False, False, 1, 6),
        (48, False, False, 2, 6),
        (40, False, False, 3, 0),
        (48, False, False, 0, 6),
        (48, False, False, 1, 6),
        (48, False, False, 2, 6),
    ]
    previous_code = 0
    i = 0
    for count, rst, sample_en, code, old_count in schedule:
        for offset in range(count):
            old_window = old_count > 0 and offset < old_count
            out_code = previous_code if (old_window or code == 3) else code
            if not old_window and code != 3:
                previous_code = code
            valid = 0.0 if rst or code == 3 else VDD
            metric_code = out_code if old_window else code
            metric = 0.0 if rst else min(1.0, 0.45 + 0.15 * metric_code)
            if wrong_metric_platform and i >= 96 and not rst and not sample_en and code != 3:
                metric = 0.05
            rows.append(
                {
                    "time": i * 0.1e-9,
                    "clk": VDD if i % 4 in (2, 3) else 0.0,
                    "rst": _logic(rst),
                    "sample_en": _logic(sample_en),
                    "sel_0": _logic(bool(code & 1)),
                    "sel_1": _logic(bool(code & 2)),
                    "vin0": held[0],
                    "vin1": held[1],
                    "vin2": held[2],
                    "vout": 0.45 if rst else (held[out_code] if out_code < 3 else held[0]),
                    "valid": valid,
                    "channel_metric": metric,
                }
            )
            i += 1
    return rows


def test_311_select_capture_transition_old_output_window_is_allowed() -> None:
    ok, note = _passes("v4_311_muxed_track_hold_array_readout", _task311_rows())
    assert ok, note


def test_311_stable_wrong_metric_platform_still_fails() -> None:
    ok, _note = _passes("v4_311_muxed_track_hold_array_readout", _task311_rows(wrong_metric_platform=True))
    assert not ok


def _task314_expected(vin: float, low: float, high: float, *, enabled: bool, rst: bool, state: bool) -> bool:
    if rst or not enabled:
        return False
    if not state and low + 10e-3 < vin < high - 10e-3:
        return True
    if state and (vin < low - 10e-3 or vin > high + 10e-3):
        return False
    return state


def _task314_rows(*, plateau_error: bool = False, toggle_stuck_high: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    t = 0.0
    low = 0.30
    high = 0.60
    state = False

    def add(vin: float, enabled: bool, rst: bool, count: int, *, old_count: int = 0) -> None:
        nonlocal t, state
        target_state = _task314_expected(vin, low, high, enabled=enabled, rst=rst, state=state)
        old_state = state
        state = target_state
        for idx in range(count):
            use_old = idx < old_count
            observed_state = old_state if use_old else target_state
            row = {
                "time": t,
                "vin": vin,
                "rst": _logic(rst),
                "enable": _logic(enabled),
                "low_trip": low,
                "high_trip": high,
                "inside_flag": _logic(observed_state),
                "state_metric": _logic(observed_state),
                "toggled": VDD if (idx == 0 and target_state != old_state and enabled and not rst) else 0.0,
            }
            if toggle_stuck_high and enabled and not rst and old_state != target_state:
                row["toggled"] = VDD
            if plateau_error and enabled and not rst and idx >= count - 14:
                row["inside_flag"] = _logic(not target_state)
                row["state_metric"] = _logic(not target_state)
            rows.append(row)
            t += 0.1e-9

    add(0.20, True, True, 14)
    add(0.20, False, False, 14)
    add(0.20, True, False, 22)
    add(0.45, True, False, 24, old_count=6)
    add(0.295, True, False, 22)
    add(0.605, True, False, 22)
    add(0.72, True, False, 22, old_count=6)
    add(0.20, True, True, 14)
    add(0.20, False, False, 14)
    return rows


def test_314_control_change_short_old_platform_is_allowed() -> None:
    ok, note = _passes("v4_314_hysteretic_window_comparator", _task314_rows())
    assert ok, note


def test_314_settled_plateau_tail_error_still_fails() -> None:
    ok, _note = _passes("v4_314_hysteretic_window_comparator", _task314_rows(plateau_error=True))
    assert not ok


def test_314_stuck_high_toggle_is_rejected() -> None:
    ok, note = _passes("v4_314_hysteretic_window_comparator", _task314_rows(toggle_stuck_high=True))
    assert not ok
    assert "toggle" in note


def _ladder_taps(hi: float, lo: float) -> tuple[list[float], float]:
    hi_c = max(0.0, min(VDD, max(hi, lo)))
    lo_c = max(0.0, min(VDD, min(hi, lo)))
    span = hi_c - lo_c
    return [lo_c + span * i / 3.0 for i in range(4)], 1.0


def _task315_rows(*, plateau_error: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    t = 0.0
    previous_taps = [0.0, 0.0, 0.0, 0.0]

    def add(hi: float, lo: float, enabled: bool, rst: bool, count: int, *, old_count: int = 0) -> None:
        nonlocal t, previous_taps
        taps, flag = _ladder_taps(hi, lo) if enabled and not rst else ([0.0, 0.0, 0.0, 0.0], 0.0)
        for idx in range(count):
            active_taps = previous_taps if idx < old_count else taps
            row = {
                "time": t,
                "vref_hi": hi,
                "vref_lo": lo,
                "enable": _logic(enabled),
                "rst": _logic(rst),
                "tap0": active_taps[0],
                "tap1": active_taps[1],
                "tap2": active_taps[2],
                "tap3": active_taps[3],
                "monotonic_ok": flag,
            }
            if plateau_error and enabled and not rst and idx >= count - 16:
                row["tap2"] = row["tap1"] - 0.20
                row["monotonic_ok"] = VDD
            rows.append(row)
            t += 0.1e-9
        previous_taps = taps

    add(0.80, 0.10, False, True, 12)
    add(0.80, 0.10, True, False, 20)
    for hi, lo in ((0.15, 0.76), (1.05, -0.04), (0.72, 0.20), (0.22, 0.70), (0.95, -0.05)):
        add(hi, lo, True, False, 16, old_count=5)
    add(0.80, 0.10, False, False, 12)
    add(0.80, 0.10, False, True, 12)
    return rows


def test_315_stimulus_change_short_old_platform_is_allowed() -> None:
    ok, note = _passes("v4_315_reference_ladder_buffered_taps", _task315_rows())
    assert ok, note


def test_315_plateau_tail_spacing_error_still_fails() -> None:
    ok, _note = _passes("v4_315_reference_ladder_buffered_taps", _task315_rows(plateau_error=True))
    assert not ok


def _task318_row(code: int, enabled: bool, rst: bool, *, t: float) -> dict[str, float]:
    clear = not enabled or rst
    return {
        "time": t,
        "enable": _logic(enabled),
        "rst": _logic(rst),
        "code_0": _logic(bool(code & 1)),
        "code_1": _logic(bool(code & 2)),
        "code_2": _logic(bool(code & 4)),
        "vout": 0.0 if clear else VDD * code / 7.0,
        "step_metric": 0.0 if clear else VDD / 7.0,
        "monotonic_ok": 0.0 if clear else VDD,
    }


def _task318_rows(*, plateau_error: bool = False, clear_stuck: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    t = 0.0
    previous = _task318_row(0, False, True, t=t)
    for enabled, rst, codes in (
        (False, True, [0]),
        (True, False, list(range(8))),
        (True, False, list(range(7, -1, -1))),
        (False, False, [0]),
        (False, True, [0]),
    ):
        for code in codes:
            target = _task318_row(code, enabled, rst, t=t)
            for idx in range(12):
                row = dict(target)
                row["time"] = t
                if enabled and not rst and idx < 4:
                    row["vout"] = previous["vout"]
                    row["step_metric"] = previous["step_metric"]
                    row["monotonic_ok"] = previous["monotonic_ok"]
                if plateau_error and enabled and not rst and idx >= 6:
                    row["vout"] = 0.0
                if clear_stuck and not enabled and not rst:
                    row["vout"] = previous["vout"]
                    row["step_metric"] = previous["step_metric"]
                    row["monotonic_ok"] = previous["monotonic_ok"]
                rows.append(row)
                t += 0.1e-9
            previous = target
    return rows


def test_318_code_change_short_old_platform_is_allowed() -> None:
    ok, note = _passes("v4_318_resistor_ladder_monotonic_decoder", _task318_rows())
    assert ok, note


def test_318_plateau_tail_or_clear_stuck_still_fails() -> None:
    for rows in (_task318_rows(plateau_error=True), _task318_rows(clear_stuck=True)):
        ok, _note = _passes("v4_318_resistor_ladder_monotonic_decoder", rows)
        assert not ok


def _gain_bits(code: int) -> dict[str, float]:
    return {"gain_0": _logic(bool(code & 1)), "gain_1": _logic(bool(code & 2)), "gain_2": _logic(bool(code & 4))}


def _task316_rows(
    *,
    disable_stuck_after_settle: bool = False,
    omit_decrement: bool = False,
    omit_late_reset: bool = False,
) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    t = 0.0
    expected_code = 0
    lock_streak = 0
    current_code = 0

    def add_row(clk: float, cal_en: bool, rst: bool, code: int, vout: float, metric: float, locked: bool) -> None:
        nonlocal t
        row = {
            "time": t,
            "clk": clk,
            "rst": _logic(rst),
            "cal_en": _logic(cal_en),
            "vin": 0.55,
            "residue_ref": 0.45,
            "vout": vout,
            "error_metric": metric,
            "locked": _logic(locked),
        }
        row.update(_gain_bits(code))
        rows.append(row)
        t += 0.05e-9

    add_row(0.0, False, True, 0, 0.45, 0.0, False)
    add_row(VDD, False, True, 0, 0.45, 0.0, False)
    add_row(0.0, True, False, 0, 0.45, 0.0, False)
    active_errors = (0.08, 0.06, 0.04, 0.02, 0.005, 0.005, 0.005, 0.005, 0.005)
    if not omit_decrement:
        active_errors = (0.08, 0.06, 0.04, -0.035, 0.02, 0.005, 0.005, 0.005, 0.005, 0.005)
    for signed_err in active_errors:
        edge_vout = max(0.0, min(VDD, 0.45 + (2.0 + 0.25 * expected_code) * (0.55 - 0.45)))
        residue_ref = edge_vout + signed_err
        err = abs(signed_err)
        edge = {
            "time": t,
            "clk": VDD,
            "rst": 0.0,
            "cal_en": VDD,
            "vin": 0.55,
            "residue_ref": residue_ref,
            "vout": edge_vout,
            "error_metric": 0.0,
            "locked": 0.0,
        }
        edge.update(_gain_bits(current_code))
        rows.append(edge)
        t += 0.25e-9
        if signed_err > 0.015:
            expected_code = min(7, expected_code + 1)
        elif signed_err < -0.015:
            expected_code = max(0, expected_code - 1)
        lock_streak = lock_streak + 1 if err <= 0.015 else 0
        current_code = expected_code
        sample_vout = max(0.0, min(VDD, 0.45 + (2.0 + 0.25 * current_code) * (0.55 - 0.45)))
        sample = {
            "time": t,
            "clk": VDD,
            "rst": 0.0,
            "cal_en": VDD,
            "vin": 0.55,
            "residue_ref": residue_ref,
            "vout": sample_vout,
            "error_metric": err,
            "locked": _logic(lock_streak >= 3),
        }
        sample.update(_gain_bits(current_code))
        rows.append(sample)
        t += 0.20e-9
        add_row(0.0, True, False, current_code, sample_vout, err, lock_streak >= 3)

    if not omit_late_reset:
        for _ in range(12):
            add_row(0.0, True, True, 0, 0.45, 0.0, False)

    stale_vout = rows[-1]["vout"]
    stale_metric = rows[-1]["error_metric"]
    stale_locked = rows[-1]["locked"] > 0.45
    for _ in range(7):
        add_row(0.0, False, False, current_code, stale_vout, stale_metric, stale_locked)
    if disable_stuck_after_settle:
        for _ in range(10):
            add_row(0.0, False, False, current_code, stale_vout, stale_metric, stale_locked)
    else:
        for _ in range(4):
            add_row(0.0, False, False, 0, 0.45, 0.0, False)
    return rows


def test_316_disable_transition_under_035ns_is_allowed() -> None:
    ok, note = _passes("v4_316_residue_amplifier_gain_calibration", _task316_rows())
    assert ok, note


def test_316_disable_settled_stuck_output_still_fails() -> None:
    ok, _note = _passes("v4_316_residue_amplifier_gain_calibration", _task316_rows(disable_stuck_after_settle=True))
    assert not ok


def test_316_requires_decrement_and_late_reset_coverage() -> None:
    for rows, expected in (
        (_task316_rows(omit_decrement=True), "decrement_seen=False"),
        (_task316_rows(omit_late_reset=True), "late_reset_clear=False"),
    ):
        ok, note = _passes("v4_316_residue_amplifier_gain_calibration", rows)
        assert not ok
        assert expected in note


def _task384_rows(*, stable_wrong_platform: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    t = 0.0

    def add(vin_values: Iterable[float], enable: bool, rst: bool, vddh: float, *, force_old_low: bool = False) -> None:
        nonlocal t
        for vin in vin_values:
            threshold = 0.45
            expected_out = vddh if enable and not rst and vin > threshold + 1e-6 else 0.0
            if not enable or rst or vddh < 0.2:
                expected_valid = 0.0
            else:
                expected_valid = vddh
            rows.append(
                {
                    "time": t,
                    "vin": vin,
                    "enable": _logic(enable),
                    "rst": _logic(rst),
                    "vddl": VDD,
                    "vddh": vddh,
                    "vout": 0.0 if force_old_low else expected_out,
                    "valid": expected_valid,
                }
            )
            t += 0.05e-9

    add([0.20] * 30, True, True, 0.9)
    add([0.20] * 30, False, False, 0.9)
    add([0.20] * 40, True, False, 0.9)
    add([0.70] * 40, True, False, 0.9)
    add([0.20] * 40, True, False, 0.45)
    add([0.70] * 40, True, False, 0.45)
    moving = [0.443 + 0.00035 * i for i in range(45)]
    add(moving, True, False, 0.9, force_old_low=True)
    if stable_wrong_platform:
        add([0.70] * 45, True, False, 0.9, force_old_low=True)
    else:
        add([0.70] * 45, True, False, 0.9)
    return rows


def test_384_threshold_crossing_with_moving_input_sample_is_skipped() -> None:
    ok, note = _passes("v4_384_level_shifter_enable_rail_tracking", _task384_rows())
    assert ok, note


def test_384_stable_wrong_output_platform_still_fails() -> None:
    ok, _note = _passes("v4_384_level_shifter_enable_rail_tracking", _task384_rows(stable_wrong_platform=True))
    assert not ok


def test_negative_platforms_remain_rejected() -> None:
    cases = (
        ("v4_079_ramp_step_source", _ramp_step_rows(transition_guard_sample=False, bad_phase=True)),
        ("v4_311_muxed_track_hold_array_readout", _task311_rows(wrong_metric_platform=True)),
        ("v4_314_hysteretic_window_comparator", _task314_rows(plateau_error=True)),
        ("v4_315_reference_ladder_buffered_taps", _task315_rows(plateau_error=True)),
        ("v4_318_resistor_ladder_monotonic_decoder", _task318_rows(plateau_error=True)),
        ("v4_316_residue_amplifier_gain_calibration", _task316_rows(disable_stuck_after_settle=True)),
        ("v4_384_level_shifter_enable_rail_tracking", _task384_rows(stable_wrong_platform=True)),
    )
    for checker_id, rows in cases:
        ok, note = _passes(checker_id, rows)
        assert not ok, f"{checker_id} unexpectedly passed: {note}"
