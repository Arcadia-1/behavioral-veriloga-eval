from __future__ import annotations

import csv
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

from checkers.v4.task_302 import (
    STREAMING_CHECKER as stream_task302_fractional_n_divider_accumulator_flow,
    check_v3_505_fractional_n_divider_accumulator_flow,
)
from checkers.v4.task_322 import check_v4_1020_glitchless_clock_mux_selector
from checkers.v4.task_342 import (
    SETTLE as SAR_SYSTEM_SETTLE,
    check_v4_342_sar_adc_system_4b,
)


VDD = 0.9
VTH = 0.45


def _logic(value: bool) -> float:
    return VDD if value else 0.0


def _clock_high(time_ns: float, edges_ns: list[float], width_ns: float) -> bool:
    return any(edge <= time_ns < edge + width_ns for edge in edges_ns)


def _fracn_rows(
    *,
    shift_ns: float = 0.0,
    counts: list[int] | None = None,
    constant_vctrl: bool = False,
    isolated_vctrl_spike: bool = False,
) -> list[dict[str, float]]:
    dco_edges_ns = [30.0 + 10.0 * index for index in range(120)]
    counts = counts or [16, 15, 15, 16, 15, 15, 15]
    fb_edges_ns = [20.0]
    dco_index = 0
    for count in counts:
        dco_index += count
        fb_edges_ns.append(dco_edges_ns[dco_index - 1])
    ref_edges_ns = [20.0, 180.0, 340.0, 500.0, 660.0, 810.0, 960.0, 1110.0]

    times_ns = set(float(step * 5) for step in range(0, 241))
    for edge in ref_edges_ns + fb_edges_ns + dco_edges_ns:
        times_ns.update({edge - 1.0, edge, edge + 1.0})
    rows: list[dict[str, float]] = []
    for time_ns in sorted(t for t in times_ns if 0.0 <= t <= 1200.0):
        shifted = (time_ns + shift_ns) * 1.0e-9
        if constant_vctrl:
            vctrl = 0.45
        elif time_ns < 660.0:
            vctrl = 0.45
        elif time_ns < 960.0:
            vctrl = 0.55
        else:
            vctrl = 0.48
        if isolated_vctrl_spike and time_ns == 665.0:
            vctrl = 0.90
        lock = (300.0 <= time_ns < 660.0) or time_ns >= 960.0
        rows.append(
            {
                "time": shifted,
                "VDD": VDD,
                "VSS": 0.0,
                "ref_clk": _logic(_clock_high(time_ns, ref_edges_ns, 8.0)),
                "fb_clk": _logic(_clock_high(time_ns, fb_edges_ns, 70.0)),
                "dco_clk": _logic(_clock_high(time_ns, dco_edges_ns, 5.0)),
                "vctrl_mon": vctrl,
                "lock": _logic(lock),
            }
        )
    return rows


def _mux_input(time_ns: float, delay_ns: float) -> bool:
    phase = (time_ns - delay_ns) % 8.0
    return 0.0 <= phase < 2.4


def _mux_rows(
    *,
    scale: float = 1.0,
    shift_ns: float = 0.0,
    no_wait: bool = False,
    missing_valid: bool = False,
) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    active = 0
    valid = False
    switch_end_ns = -1.0
    last_out = False
    for index in range(153):
        base_ns = index * 0.5
        clk_a = _mux_input(base_ns, 1.0)
        clk_b = _mux_input(base_ns, 3.0)
        rst = base_ns < 4.0
        enable = 5.0 <= base_ns < 64.0 or base_ns >= 72.0
        pending = 1 if 20.0 <= base_ns < 36.0 or base_ns >= 52.0 else 0
        if rst or not enable:
            active = 0
            valid = False
            switch_end_ns = -1.0
        elif pending != active and (no_wait or (not clk_a and not clk_b)):
            active = pending
            valid = False
            switch_end_ns = base_ns + 8.0
        out = (clk_b if active else clk_a) if enable and not rst else False
        if enable and not rst and (not last_out and out):
            valid = True
        last_out = out
        rows.append(
            {
                "time": (base_ns * scale + shift_ns) * 1.0e-9,
                "clk_a": _logic(clk_a),
                "clk_b": _logic(clk_b),
                "sel": _logic(bool(pending)),
                "rst": _logic(rst),
                "enable": _logic(enable),
                "clk_out": _logic(out),
                "switch_metric": _logic(enable and not rst and base_ns <= switch_end_ns),
                "valid": 0.0 if missing_valid else _logic(valid and enable and not rst),
            }
        )
    return rows


def _sar342_dense_rows() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []

    def add(
        time_ns: float,
        *,
        vin: float = 0.05,
        clk: float = 0.0,
        rst: float = 0.0,
        start: float = 0.0,
        sample_dbg: float = 0.0,
        dac_dbg: float = 0.0,
        code: int = 0,
        done: bool = False,
    ) -> None:
        rows.append(
            {
                "time": time_ns * 1.0e-9,
                "vin": vin,
                "clk": clk,
                "rst": rst,
                "start": start,
                "code_3": _logic(bool(code & 8)),
                "code_2": _logic(bool(code & 4)),
                "code_1": _logic(bool(code & 2)),
                "code_0": _logic(bool(code & 1)),
                "done": _logic(done),
                "sample_dbg": sample_dbg,
                "dac_dbg": dac_dbg,
            }
        )

    add(0.0, rst=VDD)
    add(1.0, rst=VDD)
    add(3.0)
    conversions = [
        (7.0, [15.0, 25.0, 35.0, 45.0, 55.0], 0.05, [8, 4, 2, 1, 0], 0),
        (77.0, [85.0, 95.0, 105.0, 115.0, 125.0], 0.43, [8, 4, 6, 7, 7], 7),
    ]
    hold_code = 0
    hold_done = False
    hold_dac = 0.0
    for start_ns, edges_ns, sample, trials, final_code in conversions:
        add(
            start_ns - 0.1,
            vin=sample,
            dac_dbg=hold_dac,
            code=hold_code,
            done=hold_done,
        )
        add(start_ns, vin=sample, start=VDD)
        add(start_ns + 0.2, vin=sample)
        previous_dac = 0.0
        for index, (edge_ns, trial_code) in enumerate(zip(edges_ns, trials, strict=True)):
            expected_dac = VDD * trial_code / 16.0
            code = final_code if index == len(edges_ns) - 1 else 0
            add(edge_ns - 0.1, vin=sample, sample_dbg=sample, dac_dbg=previous_dac, code=code)
            add(edge_ns, vin=sample, clk=VDD, sample_dbg=sample, dac_dbg=previous_dac, code=code)
            add(
                edge_ns + 0.65,
                vin=sample,
                clk=VDD,
                sample_dbg=sample,
                dac_dbg=0.5 * (previous_dac + expected_dac),
                code=code,
                done=index == len(edges_ns) - 1,
            )
            add(
                edge_ns + 0.9,
                vin=sample,
                clk=VDD,
                sample_dbg=sample,
                dac_dbg=expected_dac,
                code=code,
                done=index == len(edges_ns) - 1,
            )
            add(
                edge_ns + 1.2,
                vin=sample,
                sample_dbg=sample,
                dac_dbg=expected_dac,
                code=code,
                done=index == len(edges_ns) - 1,
            )
            previous_dac = expected_dac
        add(edges_ns[-1] + 2.0, vin=sample, sample_dbg=sample, dac_dbg=previous_dac, code=final_code, done=True)
        hold_code = final_code
        hold_done = True
        hold_dac = previous_dac
    return sorted(rows, key=lambda row: row["time"])


def test_task302_accepts_shifted_sparse_fractional_tracking_trace() -> None:
    rows = _fracn_rows(shift_ns=77.0)
    ok, note = check_v3_505_fractional_n_divider_accumulator_flow(rows)
    assert ok, note
    assert "P_USE_REF_CLK_AS_THE_REFERENCE mismatch_count=0" in note


def test_task302_rejects_wrong_integer_divider_counts() -> None:
    rows = _fracn_rows(counts=[17, 18, 17, 18, 17, 18])
    ok, note = check_v3_505_fractional_n_divider_accumulator_flow(rows)
    assert not ok
    assert "dco_edges_per_fb_period_out_of_range" in note or "fractional_short_count" in note


def test_task302_rejects_missing_control_correction() -> None:
    rows = _fracn_rows(constant_vctrl=True)
    ok, note = check_v3_505_fractional_n_divider_accumulator_flow(rows)
    assert not ok
    assert "vctrl_span" in note


def test_task302_rejects_missing_control_correction_with_isolated_vctrl_spike() -> None:
    rows = _fracn_rows(constant_vctrl=True, isolated_vctrl_spike=True)
    ok, note = check_v3_505_fractional_n_divider_accumulator_flow(rows)
    assert not ok
    assert "vctrl_span" in note


def test_task302_streaming_checker_matches_row_checker(tmp_path: Path) -> None:
    cases = {
        "passing": _fracn_rows(shift_ns=77.0),
        "wrong_divider": _fracn_rows(counts=[17, 18, 17, 18, 17, 18]),
        "constant_vctrl": _fracn_rows(constant_vctrl=True),
        "constant_vctrl_with_spike": _fracn_rows(
            constant_vctrl=True,
            isolated_vctrl_spike=True,
        ),
    }
    fieldnames = [
        "time",
        "VDD",
        "VSS",
        "ref_clk",
        "fb_clk",
        "dco_clk",
        "vctrl_mon",
        "lock",
    ]
    for name, rows in cases.items():
        csv_path = tmp_path / f"{name}.csv"
        with csv_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        row_ok, row_note = check_v3_505_fractional_n_divider_accumulator_flow(rows)
        stream_score, stream_notes = stream_task302_fractional_n_divider_accumulator_flow(
            csv_path
        )

        assert stream_score == (1.0 if row_ok else 0.0), name
        assert stream_notes == [row_note], name


def test_task322_accepts_scaled_sparse_event_relative_mux_trace() -> None:
    rows = _mux_rows(scale=2.5, shift_ns=31.0)
    ok, note = check_v4_1020_glitchless_clock_mux_selector(rows)
    assert ok, note


def test_task322_rejects_switch_without_both_low_wait() -> None:
    rows = _mux_rows(no_wait=True)
    ok, note = check_v4_1020_glitchless_clock_mux_selector(rows)
    assert not ok
    assert "glitch_errors" in note


def test_task322_rejects_missing_valid_flag() -> None:
    rows = _mux_rows(missing_valid=True)
    ok, note = check_v4_1020_glitchless_clock_mux_selector(rows)
    assert not ok
    assert "valid_errors" in note


def test_task322_short_trace_returns_a_checker_diagnostic() -> None:
    row = {
        "time": 0.0,
        "clk_a": 0.0,
        "clk_b": 0.0,
        "sel": 0.0,
        "rst": VDD,
        "enable": 0.0,
        "clk_out": 0.0,
        "switch_metric": 0.0,
        "valid": 0.0,
    }
    ok, note = check_v4_1020_glitchless_clock_mux_selector([row])
    assert not ok
    assert "insufficient_clock_coverage" in note


def test_task342_samples_after_cascaded_trial_dac_transitions_settle() -> None:
    rows = _sar342_dense_rows()
    assert SAR_SYSTEM_SETTLE >= 9.0e-10
    assert any(
        abs(row["time"] - 15.65e-9) < 1.0e-15 and row["dac_dbg"] != 0.45
        for row in rows
    )

    ok, note = check_v4_342_sar_adc_system_4b(rows)

    assert ok, note
    assert "mismatch_count=0" in note
