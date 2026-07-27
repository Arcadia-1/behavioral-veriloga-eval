from __future__ import annotations

from runners.checkers.v4.task_315 import check_v4_315_reference_ladder_buffered_taps
from runners.checkers.v4.task_368 import check_v4_927_tia_limiting_receiver_macro
from runners.checkers.v4.task_388 import check_v4_source_follower_buffer_macro


VDD = 0.9


def _logic(value: bool) -> float:
    return VDD if value else 0.0


def _downsample(rows: list[dict[str, float]], step: int) -> list[dict[str, float]]:
    return rows[::step]


def _ladder_taps(hi: float, lo: float) -> tuple[list[float], float]:
    hi_c = max(0.0, min(VDD, max(hi, lo)))
    lo_c = max(0.0, min(VDD, min(hi, lo)))
    span = hi_c - lo_c
    return [lo_c + span * i / 3.0 for i in range(4)], 1.0


def _task315_rows(*, spacing_defect: bool = False) -> list[dict[str, float]]:
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
            if spacing_defect and enabled and not rst and idx >= max(old_count + 3, count // 2):
                row["tap2"] = row["tap1"] - 0.20
                row["monotonic_ok"] = VDD
            rows.append(row)
            t += 0.1e-9
        previous_taps = taps

    add(0.80, 0.10, False, True, 16)
    add(0.80, 0.10, True, False, 20)
    for hi, lo in ((0.15, 0.76), (1.05, -0.04), (0.72, 0.20), (0.22, 0.70), (0.95, -0.05)):
        add(hi, lo, True, False, 16, old_count=5)
    add(0.80, 0.10, False, False, 12)
    add(0.80, 0.10, False, True, 16)
    return rows


def _task368_rows(*, samples_per_window: int, output_defect: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    t = 0.0
    valid_count = 0
    prev_clk = 0.0

    def add_window(vin: float, enabled: bool, rst: bool, duration: float, *, clk_start: float = 0.0, clk_end: float = 0.0) -> None:
        nonlocal t, valid_count, prev_clk
        raw = 4.0 * (vin - 0.45)
        limited = max(-0.35, min(0.35, raw))
        amp = abs(limited)
        for idx in range(samples_per_window):
            frac = idx / max(1, samples_per_window - 1)
            clk = clk_start if frac < 0.50 else clk_end
            rising = clk > 0.45 and prev_clk <= 0.45
            if not enabled or rst:
                valid_count = 0
            elif rising:
                valid_count = valid_count + 1 if amp >= 0.040 else 0
            active = enabled and not rst
            row = {
                "time": t + duration * frac,
                "vin_proxy": vin,
                "rst": _logic(rst),
                "enable": _logic(enabled),
                "clk": clk,
                "vout": 0.45 + limited if active else 0.45,
                "decision": _logic(active and limited >= 0.0),
                "limit_flag": _logic(active and abs(raw) > 0.35),
                "valid": _logic(active and valid_count >= 2),
                "amp_metric": amp if active else 0.0,
            }
            if output_defect and active and t > 5.0e-9:
                row["vout"] = 0.45
                row["limit_flag"] = 0.0
            rows.append(row)
            prev_clk = clk
        t += duration

    add_window(0.45, False, True, 2.0e-9)
    add_window(0.70, True, False, 2.0e-9, clk_start=0.0, clk_end=VDD)
    add_window(0.20, True, False, 2.0e-9, clk_start=VDD, clk_end=0.0)
    add_window(0.70, True, False, 2.0e-9, clk_start=0.0, clk_end=VDD)
    add_window(0.46, True, False, 2.0e-9, clk_start=VDD, clk_end=0.0)
    add_window(0.20, True, False, 2.0e-9, clk_start=0.0, clk_end=VDD)
    add_window(0.45, False, False, 2.0e-9)
    add_window(0.45, False, True, 2.0e-9)
    return rows


def _task388_expected(vin: float, vbias: float, enabled: bool, rst: bool) -> tuple[float, float, float]:
    inactive = rst or not enabled or vbias <= 0.10
    if inactive:
        return 0.0, 0.0, 0.0
    max_out = vbias - 0.10
    raw = vin - 0.12
    vout = max(0.0, min(max_out, raw))
    return vout, max(0.0, min(0.9, vbias - vout)), 0.9


def _task388_rows(*, samples_per_window: int, clear_defect: bool = False, transfer_defect: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    t = 0.0

    def add(vin: float, vbias: float, enabled: bool, rst: bool, duration: float) -> None:
        nonlocal t
        vout, metric, valid = _task388_expected(vin, vbias, enabled, rst)
        for idx in range(samples_per_window):
            frac = idx / max(1, samples_per_window - 1)
            row = {
                "time": t + duration * frac,
                "vin": vin,
                "vbias": vbias,
                "enable": _logic(enabled),
                "rst": _logic(rst),
                "vout": vout,
                "headroom_metric": metric,
                "valid": valid,
            }
            if clear_defect and (rst or not enabled):
                row["vout"] = 0.30
            if transfer_defect and enabled and not rst and vbias > 0.10:
                row["vout"] = 0.0
            rows.append(row)
        t += duration

    add(0.40, 0.70, False, True, 2.0e-9)
    add(0.40, 0.70, False, False, 2.0e-9)
    add(0.45, 0.70, True, False, 2.0e-9)
    add(0.82, 0.58, True, False, 2.0e-9)
    add(0.22, 0.08, True, False, 2.0e-9)
    add(0.40, 0.70, False, False, 2.0e-9)
    return rows


def test_315_result_is_invariant_to_semantic_downsampling() -> None:
    dense_ok, dense_note = check_v4_315_reference_ladder_buffered_taps(_task315_rows())
    sparse_ok, sparse_note = check_v4_315_reference_ladder_buffered_taps(_downsample(_task315_rows(), 2))

    assert dense_ok, dense_note
    assert sparse_ok, sparse_note


def test_315_spacing_defect_still_fails_after_coverage_fix() -> None:
    ok, note = check_v4_315_reference_ladder_buffered_taps(_downsample(_task315_rows(spacing_defect=True), 2))
    assert not ok, note


def test_368_result_is_invariant_to_sample_grid_density() -> None:
    dense_ok, dense_note = check_v4_927_tia_limiting_receiver_macro(_task368_rows(samples_per_window=36))
    sparse_ok, sparse_note = check_v4_927_tia_limiting_receiver_macro(_task368_rows(samples_per_window=8))

    assert dense_ok, dense_note
    assert sparse_ok, sparse_note


def test_368_output_defect_still_fails_after_coverage_fix() -> None:
    ok, note = check_v4_927_tia_limiting_receiver_macro(
        _task368_rows(samples_per_window=8, output_defect=True)
    )
    assert not ok, note


def test_388_result_is_invariant_to_sample_grid_density() -> None:
    dense_ok, dense_note = check_v4_source_follower_buffer_macro(_task388_rows(samples_per_window=24))
    sparse_ok, sparse_note = check_v4_source_follower_buffer_macro(_task388_rows(samples_per_window=4))

    assert dense_ok, dense_note
    assert sparse_ok, sparse_note


def test_388_clear_and_transfer_defects_still_fail_after_coverage_fix() -> None:
    for rows in (
        _task388_rows(samples_per_window=4, clear_defect=True),
        _task388_rows(samples_per_window=4, transfer_defect=True),
    ):
        ok, note = check_v4_source_follower_buffer_macro(rows)
        assert not ok, note
