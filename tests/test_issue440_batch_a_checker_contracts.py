from __future__ import annotations

import csv
import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

from checkers.v4.task_068 import CHECKER as check_068
from checkers.v4.task_070 import CHECKER as check_070
from checkers.v4.task_077 import CHECKER as check_077
from checkers.v4.task_084 import CHECKER as check_084
from checkers.v4.task_089 import CHECKER as check_089
from checkers.v4.task_089 import STREAMING_CHECKER as stream_089
from checkers.v4.task_093 import CHECKER as check_093
from checkers.v4.task_093 import STREAMING_CHECKER as stream_093


RELEASE = ROOT / "benchmark-vabench-release-v4/provenance/dut-base-v3-exact-five-hash-bound-v2"


def _assert_passes(checker, rows: list[dict[str, float]]) -> None:
    passed, detail = checker(rows)
    assert passed, detail


def _assert_fails(checker, rows: list[dict[str, float]]) -> None:
    passed, detail = checker(rows)
    assert not passed, detail


def _write_csv(path: Path, rows: list[dict[str, float]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _clock_rows(
    *,
    vss: float = 0.0,
    low: float = 0.0,
    high: float = 0.9,
    width_ns: float = 10.0,
    clk270_high: float | None = None,
) -> list[dict[str, float]]:
    rows = []
    for index in range(1301):
        time_ns = index * 0.1
        row = {"time": time_ns * 1e-9, "vss": vss}
        for name, phase_ns in (
            ("clk0", 2.0),
            ("clk90", 7.0),
            ("clk180", 12.0),
            ("clk270", 17.0),
        ):
            active = time_ns >= phase_ns and (time_ns - phase_ns) % 20.0 < width_ns
            phase_high = clk270_high if name == "clk270" and clk270_high is not None else high
            row[name] = vss + (phase_high if active else low)
        rows.append(row)
    return rows


def test_068_checks_all_cycles_duty_and_common_parameterized_rails() -> None:
    _assert_passes(check_068, _clock_rows())
    _assert_passes(check_068, _clock_rows(high=1.1))
    _assert_passes(check_068, _clock_rows(vss=0.2, high=0.9))
    _assert_fails(check_068, _clock_rows(high=0.5, width_ns=1.0))
    _assert_fails(check_068, _clock_rows(clk270_high=0.45))
    _assert_fails(check_068, _clock_rows(vss=0.2, low=0.2, high=1.1))

    family = RELEASE / "068-multiphase-clock-generator-4ph"
    feedback_lines = [
        line
        for line in (family / "public/task/feedback_tb.scs").read_text().splitlines()
        if line and not line.startswith("simulatorOptions options")
    ]
    score_lines = [
        line for line in (family / "evaluator/score_tb.scs").read_text().splitlines() if line
    ]
    assert feedback_lines == score_lines
    assert "Vvss (vss 0) vsource dc=0.2" in score_lines
    assert "save vss clk0 clk90 clk180 clk270" in score_lines


def _jitter_clock_rows(
    *, include_disabled_window: bool, jitter_while_disabled: bool = False
) -> list[dict[str, float]]:
    seed = 91
    disabled_indices = set(range(9, 14)) if include_disabled_window else set()
    transition_times = [5.0e-9]
    for edge_index in range(1, 25):
        if edge_index in disabled_indices and not jitter_while_disabled:
            half_period_ns = 10.0
        else:
            half_period_ns = 10.0 + (((seed + 3 * edge_index) % 5) - 2) * 0.8
        transition_times.append(transition_times[-1] + half_period_ns * 1e-9)

    rows = []
    clock_high = False
    rows.append(
        {
            "time": 0.0,
            "jitter_en": 0.9,
            "clk_out": 0.0,
            **{f"seed{bit}": 0.9 if seed & (1 << bit) else 0.0 for bit in range(8)},
        }
    )
    for edge_index, time_s in enumerate(transition_times, start=1):
        clock_high = not clock_high
        rows.append(
            {
                "time": time_s,
                "jitter_en": 0.0 if edge_index in disabled_indices else 0.9,
                "clk_out": 0.9 if clock_high else 0.0,
                **{f"seed{bit}": 0.9 if seed & (1 << bit) else 0.0 for bit in range(8)},
            }
        )
    rows.append({**rows[-1], "time": rows[-1]["time"] + 5.0e-9})
    return rows


def test_070_requires_enabled_and_disabled_jitter_en_coverage() -> None:
    _assert_passes(check_070, _jitter_clock_rows(include_disabled_window=True))
    _assert_fails(check_070, _jitter_clock_rows(include_disabled_window=False))
    _assert_fails(
        check_070,
        _jitter_clock_rows(
            include_disabled_window=True,
            jitter_while_disabled=True,
        ),
    )


_SEQ_077 = (-1.0, -0.5, 0.0, 0.5, 1.0, 0.5, 0.0, -0.5)


def _sequence_rows(*, sigma: float, dt_ns: float, shortcut: bool) -> list[dict[str, float]]:
    step_ns = dt_ns / 10.0
    rows = []
    for index in range(181):
        time_ns = index * step_ns
        if shortcut:
            delta = sigma * math.sin(2.0 * math.pi * time_ns / (8.0 * dt_ns))
        else:
            sequence_index = int((time_ns + 1e-10) / dt_ns) % len(_SEQ_077)
            delta = sigma * _SEQ_077[sequence_index]
        rows.append({"time": time_ns * 1e-9, "vin_i": 0.2, "vout_o": 0.2 + delta})
    return rows


def test_077_checks_sequence_and_hold_without_hardcoding_sigma_or_dt() -> None:
    _assert_passes(check_077, _sequence_rows(sigma=0.10, dt_ns=0.5, shortcut=False))
    _assert_passes(check_077, _sequence_rows(sigma=0.037, dt_ns=0.8, shortcut=False))
    _assert_fails(check_077, _sequence_rows(sigma=0.10, dt_ns=0.5, shortcut=True))


_DATA_EDGES_NS = (20.0, 30.0, 40.0, 50.0, 60.0, 70.0)


def _data_logic(time_ns: float) -> bool:
    return bool(sum(time_ns >= edge for edge in _DATA_EDGES_NS) % 2)


def _retimed_logic(time_ns: float) -> bool:
    clock_edges = (5.0, 25.0, 45.0, 65.0, 85.0)
    prior = [edge for edge in clock_edges if edge <= time_ns]
    return _data_logic(prior[-1]) if prior else False


def _bbpd_rows(*, vss: float, vdd: float, retimed_shortcut: bool) -> list[dict[str, float]]:
    rows = []
    for index in range(1001):
        time_ns = index * 0.1
        clk_high = time_ns >= 5.0 and (time_ns - 5.0) % 20.0 < 10.0
        up_high = any(edge <= time_ns < edge + 1.0 for edge in (20.0, 40.0, 60.0))
        dn_high = any(edge <= time_ns < edge + 1.0 for edge in (30.0, 50.0, 70.0))
        rows.append(
            {
                "time": time_ns * 1e-9,
                "vdd": vdd,
                "vss": vss,
                "clk": vdd if clk_high else vss,
                "data": vdd if _data_logic(time_ns) else vss,
                "up": vdd if up_high else vss,
                "dn": vdd if dn_high else vss,
                "retimed_data": vss
                if retimed_shortcut
                else (vdd if _retimed_logic(time_ns) else vss),
            }
        )
    return rows


def test_084_checks_retimed_data_against_observed_supply_rails() -> None:
    _assert_passes(check_084, _bbpd_rows(vss=0.0, vdd=0.9, retimed_shortcut=False))
    _assert_passes(check_084, _bbpd_rows(vss=0.2, vdd=1.1, retimed_shortcut=False))
    _assert_fails(check_084, _bbpd_rows(vss=0.0, vdd=0.9, retimed_shortcut=True))


def _interval_rows(
    *,
    vss: float,
    vdd: float,
    self_scaled: bool,
    single_shot: bool = False,
    recapture_extra_b: bool = False,
    ignore_vss_span: bool = False,
    reuse_first_result: bool = False,
) -> list[dict[str, float]]:
    rows = []
    span = vdd - vss
    for index in range(2601):
        time_ns = index * 0.01
        cycle0 = time_ns >= 1.20 if single_shot else 1.20 <= time_ns < 2.00
        cycle1 = not single_shot and time_ns >= 2.12
        output_high = vss + span * (0.3 if self_scaled else 1.0)
        if recapture_extra_b and 1.55 <= time_ns < 2.00:
            normalized_delay = 0.45 / 0.2
        elif cycle1:
            normalized_delay = 1.0 if reuse_first_result else 0.12 / 0.2
        else:
            normalized_delay = 0.20 / 0.2
        delay_level = (
            normalized_delay
            if ignore_vss_span
            else vss + span * normalized_delay
        )
        if single_shot:
            a_high = time_ns >= 1.0
            b_high = time_ns >= 1.2
        else:
            a_high = 1.0 <= time_ns < 1.9 or time_ns >= 2.0
            b_high = (
                1.2 <= time_ns < 1.45
                or 1.55 <= time_ns < 1.9
                or time_ns >= 2.12
            )
        rows.append(
            {
                "time": time_ns * 1e-9,
                "vdd": vdd,
                "vss": vss,
                "a": vdd if a_high else vss,
                "b": vdd if b_high else vss,
                "seen_out": output_high if (cycle0 or cycle1) else vss,
                "delay_out": delay_level if (cycle0 or cycle1) else vss,
            }
        )
    return rows


def _assert_089_rejected_by_row_and_streaming(
    tmp_path: Path,
    name: str,
    rows: list[dict[str, float]],
) -> None:
    passed, detail = check_089(rows)
    assert not passed, f"{name}: {detail}"
    csv_path = tmp_path / f"{name}.csv"
    _write_csv(csv_path, rows)
    score, notes = stream_089(csv_path)
    assert score == 0.0, f"{name}: {notes}"


def test_089_accepts_two_supply_normalized_measurement_cycles(
    tmp_path: Path,
) -> None:
    rows = _interval_rows(vss=0.2, vdd=1.1, self_scaled=False)
    _assert_passes(check_089, rows)
    csv_path = tmp_path / "valid_089.csv"
    _write_csv(csv_path, rows)
    assert stream_089(csv_path)[0] == 1.0


def test_089_rejects_seen_out_below_supply_rail_in_row_and_streaming(
    tmp_path: Path,
) -> None:
    _assert_089_rejected_by_row_and_streaming(
        tmp_path,
        "seen_out_below_supply_rail_089",
        _interval_rows(vss=0.0, vdd=1.0, self_scaled=True),
    )


def test_089_rejects_single_shot_trace_in_row_and_streaming(tmp_path: Path) -> None:
    _assert_089_rejected_by_row_and_streaming(
        tmp_path,
        "single_shot_089",
        _interval_rows(
            vss=0.0,
            vdd=1.0,
            self_scaled=False,
            single_shot=True,
        ),
    )


def test_089_rejects_extra_b_recapture_in_row_and_streaming(tmp_path: Path) -> None:
    _assert_089_rejected_by_row_and_streaming(
        tmp_path,
        "extra_b_recapture_089",
        _interval_rows(
            vss=0.0,
            vdd=1.0,
            self_scaled=False,
            recapture_extra_b=True,
        ),
    )


def test_089_rejects_ignored_vss_span_normalization_in_row_and_streaming(
    tmp_path: Path,
) -> None:
    _assert_089_rejected_by_row_and_streaming(
        tmp_path,
        "ignores_vss_span_089",
        _interval_rows(
            vss=0.2,
            vdd=1.1,
            self_scaled=False,
            ignore_vss_span=True,
        ),
    )


def test_089_rejects_reused_first_cycle_result_in_row_and_streaming(
    tmp_path: Path,
) -> None:
    _assert_089_rejected_by_row_and_streaming(
        tmp_path,
        "reuses_first_result_089",
        _interval_rows(
            vss=0.2,
            vdd=1.1,
            self_scaled=False,
            reuse_first_result=True,
        ),
    )


def _gain_rows(*, vss: float, vdd: float, self_scaled: bool) -> list[dict[str, float]]:
    rows = []
    span = vdd - vss
    common = vss + 0.5 * span
    for index in range(121):
        time_ns = index * 2.0
        x = 0.03 * math.sin(2.0 * math.pi * time_ns / 20.0)
        active = time_ns >= 30.0
        rows.append(
            {
                "time": time_ns * 1e-9,
                "vdd": vdd,
                "vss": vss,
                "vinp": common + x,
                "vinn": common,
                "voutp": common + 6.0 * x,
                "voutn": common,
                "gain_out": (vss + span * (1.0 / 3.0 if self_scaled else 0.6)) if active else vss,
                "valid": (vss + span * (5.0 / 9.0 if self_scaled else 1.0)) if active else vss,
            }
        )
    return rows


def test_093_uses_supply_for_row_and_streaming_normalization(tmp_path: Path) -> None:
    valid = _gain_rows(vss=0.2, vdd=1.1, self_scaled=False)
    adversarial = _gain_rows(vss=0.0, vdd=0.9, self_scaled=True)
    _assert_passes(check_093, valid)
    passed, detail = check_093(adversarial)
    assert not passed
    assert "property_id=P_NORMALIZED_GAIN_OUTPUT" in detail
    valid_csv = tmp_path / "valid_093.csv"
    adversarial_csv = tmp_path / "adversarial_093.csv"
    _write_csv(valid_csv, valid)
    _write_csv(adversarial_csv, adversarial)
    assert stream_093(valid_csv)[0] == 1.0
    assert stream_093(adversarial_csv)[0] == 0.0
