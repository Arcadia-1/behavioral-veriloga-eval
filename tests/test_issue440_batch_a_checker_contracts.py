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
    *,
    include_disabled_window: bool,
    jitter_while_disabled: bool = False,
    input_high: float = 0.9,
    output_high: float = 0.9,
    force_nominal: bool = False,
    fast_edges: bool = False,
) -> list[dict[str, float]]:
    seed = 91
    disabled_indices = set(range(9, 14)) if include_disabled_window else set()
    transition_times = [5.0e-9]
    for edge_index in range(1, 25):
        if force_nominal or (edge_index in disabled_indices and not jitter_while_disabled):
            half_period_ns = 10.0
        else:
            half_period_ns = 10.0 + (((seed + 3 * edge_index) % 5) - 2) * 0.8
        transition_times.append(transition_times[-1] + half_period_ns * 1e-9)

    rows = []
    clock_high = False
    rows.append(
        {
            "time": 0.0,
            "jitter_en": input_high,
            "clk_out": 0.0,
            **{f"seed{bit}": input_high if seed & (1 << bit) else 0.0 for bit in range(8)},
        }
    )
    for edge_index, time_s in enumerate(transition_times, start=1):
        if fast_edges and time_s > 1.0e-12:
            rows.append({**rows[-1], "time": time_s - 1.0e-12})
        clock_high = not clock_high
        rows.append(
            {
                "time": time_s,
                "jitter_en": 0.0 if edge_index in disabled_indices else input_high,
                "clk_out": output_high if clock_high else 0.0,
                **{f"seed{bit}": input_high if seed & (1 << bit) else 0.0 for bit in range(8)},
            }
        )
    rows.append({**rows[-1], "time": rows[-1]["time"] + 5.0e-9})
    return rows


def _suffix_rows(
    rows: list[dict[str, float]],
    label: str,
    refs: dict[str, float] | None = None,
) -> list[dict[str, float]]:
    suffixed: list[dict[str, float]] = []
    for row in rows:
        next_row = {"time": row["time"]}
        next_row.update({f"{name}_{label}": value for name, value in row.items() if name != "time"})
        for name, value in (refs or {}).items():
            next_row[f"{name}_{label}"] = value
        suffixed.append(next_row)
    return suffixed


def _merge_by_time(*traces: list[dict[str, float]]) -> list[dict[str, float]]:
    merged: dict[float, dict[str, float]] = {}
    for trace in traces:
        last: dict[str, float] | None = None
        iterator = iter(trace)
        current = next(iterator, None)
        for time in sorted({row["time"] for trace_rows in traces for row in trace_rows}):
            while current is not None and current["time"] <= time:
                last = current
                current = next(iterator, None)
            if last is None:
                continue
            merged.setdefault(time, {"time": time}).update(
                {name: value for name, value in last.items() if name != "time"}
            )
    return [merged[time] for time in sorted(merged)]


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


def test_070_checks_default_and_override_public_parameters() -> None:
    default = _suffix_rows(
        _jitter_clock_rows(include_disabled_window=True),
        "default",
        {"vdd_ref": 0.9, "vth_ref": 0.45},
    )
    override = _suffix_rows(
        _jitter_clock_rows(
            include_disabled_window=True,
            input_high=0.42,
            output_high=0.7,
        ),
        "override",
        {"vdd_ref": 0.7, "vth_ref": 0.35},
    )
    _assert_passes(check_070, _merge_by_time(default, override))

    hardcoded_vdd = _suffix_rows(
        _jitter_clock_rows(
            include_disabled_window=True,
            input_high=0.42,
            output_high=0.9,
        ),
        "override",
        {"vdd_ref": 0.7, "vth_ref": 0.35},
    )
    _assert_fails(check_070, _merge_by_time(default, hardcoded_vdd))

    hardcoded_vth = _suffix_rows(
        _jitter_clock_rows(
            include_disabled_window=True,
            input_high=0.42,
            output_high=0.7,
            force_nominal=True,
        ),
        "override",
        {"vdd_ref": 0.7, "vth_ref": 0.35},
    )
    _assert_fails(check_070, _merge_by_time(default, hardcoded_vth))

    hardcoded_tr = _suffix_rows(
        _jitter_clock_rows(
            include_disabled_window=True,
            input_high=0.42,
            output_high=0.7,
            fast_edges=True,
        ),
        "override",
        {"vdd_ref": 0.7, "vth_ref": 0.35, "tr_ps_ref": 80.0},
    )
    _assert_fails(check_070, _merge_by_time(default, hardcoded_tr))

    family = RELEASE / "070-jittered-clock-source-deterministic"
    assert (family / "public/task/feedback_tb.scs").read_text() == (
        family / "evaluator/score_tb.scs"
    ).read_text()
    score_deck = (family / "evaluator/score_tb.scs").read_text()
    assert "Xdefault" in score_deck
    assert "Xoverride" in score_deck
    assert "vdd=0.7 vth=0.35 tr=80p" in score_deck


_SEQ_077 = (-1.0, -0.5, 0.0, 0.5, 1.0, 0.5, 0.0, -0.5)


def _sequence_rows(*, override_ignores_parameters: bool, shortcut: bool) -> list[dict[str, float]]:
    step_ns = 0.05
    rows = []
    for index in range(401):
        time_ns = index * step_ns
        default_delta = 0.01 * _SEQ_077[
            int((time_ns + 1e-10) / 0.5) % len(_SEQ_077)
        ]
        override_sigma = 0.01 if override_ignores_parameters else 0.037
        override_dt_ns = 0.5 if override_ignores_parameters else 0.8
        if shortcut:
            override_delta = override_sigma * math.sin(
                2.0 * math.pi * time_ns / (8.0 * override_dt_ns)
            )
        else:
            sequence_index = int((time_ns + 1e-10) / override_dt_ns) % len(_SEQ_077)
            override_delta = override_sigma * _SEQ_077[sequence_index]
        rows.append(
            {
                "time": time_ns * 1e-9,
                "vin_i": 0.2,
                "vout_default": 0.2 + default_delta,
                "vout_override": 0.2 + override_delta,
            }
        )
    return rows


def test_077_checks_default_and_override_parameter_behavior() -> None:
    _assert_passes(check_077, _sequence_rows(override_ignores_parameters=False, shortcut=False))
    _assert_fails(check_077, _sequence_rows(override_ignores_parameters=True, shortcut=False))
    _assert_fails(check_077, _sequence_rows(override_ignores_parameters=False, shortcut=True))


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
    single_shot_output: bool = False,
    recapture_extra_b: bool = False,
    ignore_vss_span: bool = False,
    reuse_first_result: bool = False,
) -> list[dict[str, float]]:
    rows = []
    span = vdd - vss
    for index in range(2601):
        time_ns = index * 0.01
        cycle0 = 1.20 <= time_ns < 2.00
        cycle1 = not single_shot_output and time_ns >= 2.12
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


def _interval_override_parameter_rows(
    *,
    hardcoded_vth: bool = False,
    hardcoded_scale: bool = False,
) -> list[dict[str, float]]:
    rows = []
    capture_pairs = ((10.10, 10.24, 10.13), (20.10, 20.25, 20.13))
    span = 1.0
    scale = 200.0 if hardcoded_scale else 100.0
    for index in range(2601):
        time_ns = index * 0.01

        def level_for(
            true_start: float,
            false_start: float,
            fall: float | None = None,
        ) -> float:
            if false_start <= time_ns < false_start + 0.04:
                return 0.52
            if time_ns >= true_start and (fall is None or time_ns < fall):
                return 0.7
            return 0.0

        a_level = max(
            level_for(10.10, 9.95, 19.86),
            level_for(20.10, 19.95, None),
        )
        b_level = max(
            level_for(10.24, 10.13, 12.10),
            level_for(20.25, 20.13, None),
        )
        active_pair = None
        for a_t, real_b_t, false_b_t in capture_pairs:
            if time_ns < a_t:
                continue
            capture_t = false_b_t if hardcoded_vth else real_b_t
            if time_ns >= capture_t + 0.21:
                active_pair = (a_t, capture_t)
            else:
                active_pair = None
        if active_pair is None:
            delay_level = 0.0
            seen = 0.0
        else:
            a_t, b_t = active_pair
            delay_ps = b_t - a_t
            delay_level = span * (delay_ps * 1000.0) / scale
            seen = 1.0
        rows.append(
            {
                "time": time_ns * 1e-9,
                "vdd": 1.0,
                "vss": 0.0,
                "a": a_level,
                "b": b_level,
                "seen_out": seen,
                "delay_out": delay_level,
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


def test_089_checks_default_and_override_public_parameters(tmp_path: Path) -> None:
    default = _suffix_rows(
        _interval_rows(vss=0.0, vdd=1.0, self_scaled=False),
        "default",
        {"vth_ref": 0.45, "scale_ps_ref": 200.0},
    )
    override = _suffix_rows(
        _interval_override_parameter_rows(),
        "override",
        {"vth_ref": 0.6, "scale_ps_ref": 100.0},
    )
    valid = _merge_by_time(default, override)
    _assert_passes(check_089, valid)
    valid_csv = tmp_path / "valid_grouped_089.csv"
    _write_csv(valid_csv, valid)
    assert stream_089(valid_csv)[0] == 1.0

    hardcoded_vth = _merge_by_time(
        default,
        _suffix_rows(
            _interval_override_parameter_rows(hardcoded_vth=True),
            "override",
            {"vth_ref": 0.6, "scale_ps_ref": 100.0},
        ),
    )
    _assert_089_rejected_by_row_and_streaming(
        tmp_path,
        "hardcoded_vth_override_089",
        hardcoded_vth,
    )

    hardcoded_scale = _merge_by_time(
        default,
        _suffix_rows(
            _interval_override_parameter_rows(hardcoded_scale=True),
            "override",
            {"vth_ref": 0.6, "scale_ps_ref": 100.0},
        ),
    )
    _assert_089_rejected_by_row_and_streaming(
        tmp_path,
        "hardcoded_scale_override_089",
        hardcoded_scale,
    )

    hardcoded_tedge = _merge_by_time(
        default,
        _suffix_rows(
            _interval_override_parameter_rows(),
            "override",
            {"vth_ref": 0.6, "scale_ps_ref": 100.0, "tedge_ps_ref": 80.0},
        ),
    )
    _assert_089_rejected_by_row_and_streaming(
        tmp_path,
        "hardcoded_tedge_override_089",
        hardcoded_tedge,
    )

    family = RELEASE / "089-edge-crossing-interval-timer"
    assert (family / "public/task/feedback_tb.scs").read_text() == (
        family / "evaluator/score_tb.scs"
    ).read_text()
    score_deck = (family / "evaluator/score_tb.scs").read_text()
    assert "Idefault" in score_deck
    assert "Ioverride" in score_deck
    assert "vth=0.6 scale_ps=100.0 tedge=80p" in score_deck


def test_089_rejects_seen_out_below_supply_rail_in_row_and_streaming(
    tmp_path: Path,
) -> None:
    _assert_089_rejected_by_row_and_streaming(
        tmp_path,
        "seen_out_below_supply_rail_089",
        _interval_rows(vss=0.0, vdd=1.0, self_scaled=True),
    )


def test_089_rejects_single_shot_output_for_two_valid_input_cycles(
    tmp_path: Path,
) -> None:
    rows = _interval_rows(
        vss=0.0,
        vdd=1.0,
        self_scaled=False,
        single_shot_output=True,
    )
    passed, detail = check_089(rows)
    assert not passed, detail
    assert "missing_input_edges" not in detail
    assert "seen_out_no_logic_high_samples cycle=1" in detail

    csv_path = tmp_path / "single_shot_output_089.csv"
    _write_csv(csv_path, rows)
    score, notes = stream_089(csv_path)
    assert score == 0.0, notes
    streaming_detail = " ".join(notes)
    assert "missing_input_edges" not in streaming_detail
    assert "seen_out_no_logic_high_samples cycle=1" in streaming_detail


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
