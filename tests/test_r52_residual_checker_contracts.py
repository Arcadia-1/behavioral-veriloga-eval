from __future__ import annotations

import csv
from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
RUNNERS = ROOT / "runners"
if str(RUNNERS) not in sys.path:
    sys.path.insert(0, str(RUNNERS))

from checkers.common.relative_events import rising_edges, sample_step
from checkers.v4.registry import load_checker
from checkers.v4.task_140 import check_v3_rs_latch_voltage
from checkers.v4.task_211 import check_v3_sum5_signed_sar_weight
from checkers.v4.task_212 import check_v3_lt_readout_sar4
from checkers.v4.task_307 import check_v4_307_switched_capacitor_integrator_phase_pair
from checkers.v4.task_312 import check_v4_312_interleaved_adc_skew_monitor


EVAS_FULL400 = (
    ROOT.parents[1]
    / "_experiment_runs"
    / "r51-complete-refresh-20260723"
    / "work-stimulus-full400"
)
R51_SPECTRE_812 = (
    ROOT.parents[1]
    / "_experiment_runs"
    / "r51-spectre-recert-20260722"
    / "work"
    / "v4-812"
    / "v4-812"
)

NS = 1e-9
VTH = 0.45


ARCHIVED_EVAS_CASES = {
    "v4_140_rs_latch_voltage": EVAS_FULL400 / "v4-640/affine",
    "v4_211_sum5_signed_sar_weight": EVAS_FULL400 / "v4-711/affine",
    "v4_212_lt_readout_sar4": EVAS_FULL400 / "v4-712/affine",
    "v4_307_switched_capacitor_integrator_phase_pair": EVAS_FULL400 / "v4-807/affine",
}


def _load_rows(csv_path: Path) -> list[dict[str, float]]:
    if not csv_path.is_file():
        pytest.skip(f"archived trace is not available: {csv_path}")
    with csv_path.open(newline="", encoding="utf-8") as handle:
        return [{name: float(value) for name, value in row.items()} for row in csv.DictReader(handle)]


@pytest.mark.parametrize("checker_id,cases_dir", ARCHIVED_EVAS_CASES.items())
def test_residual_cluster_archived_evas_references_pass_and_mutations_fail(
    checker_id: str,
    cases_dir: Path,
) -> None:
    checker = load_checker(checker_id)
    assert checker is not None
    reference_ok, reference_note = checker(_load_rows(cases_dir / "correct/output/tran.csv"))

    assert reference_ok, reference_note

    mutation_dirs = sorted(path for path in cases_dir.iterdir() if path.name.startswith("neg_"))
    assert mutation_dirs
    for mutation_dir in mutation_dirs:
        mutation_ok, mutation_note = checker(_load_rows(mutation_dir / "output/tran.csv"))
        assert not mutation_ok, f"{checker_id} accepted {mutation_dir.name}: {mutation_note}"


def test_task812_r51_classic_reference_passes_and_mutations_fail() -> None:
    reference_ok, reference_note = check_v4_312_interleaved_adc_skew_monitor(
        _load_rows(R51_SPECTRE_812 / "correct/tran_spectre.csv")
    )
    assert reference_ok, reference_note

    mutation_dirs = sorted(path for path in R51_SPECTRE_812.iterdir() if path.name.startswith("neg_"))
    assert mutation_dirs
    for mutation_dir in mutation_dirs:
        mutation_ok, mutation_note = check_v4_312_interleaved_adc_skew_monitor(
            _load_rows(mutation_dir / "tran_spectre.csv")
        )
        assert not mutation_ok, f"v4_312 accepted {mutation_dir.name}: {mutation_note}"


def _transition(old: float, new: float, start_ns: float, time_ns: float, settle_ns: float) -> float:
    if time_ns <= start_ns:
        return old
    fraction = (time_ns - start_ns) / settle_ns
    if fraction >= 1.0:
        return new
    return old + (new - old) * max(0.0, fraction)


def _slow_rs_latch_rows(*, wrong_hold: bool = False) -> list[dict[str, float]]:
    phases = [
        (0, 0),
        (1, 0),
        (0, 0),
        (0, 1),
        (0, 0),
        (1, 0),
        (0, 0),
        (0, 1),
    ]
    rows: list[dict[str, float]] = []
    previous_inputs = phases[0]
    q_state = 0
    previous_q = 0.0
    previous_qbar = 0.9
    for phase_index, inputs in enumerate(phases):
        start_ns = phase_index * 5.0
        s, r = inputs
        if s and not r:
            q_state = 1
        elif r and not s:
            q_state = 0
        target_q = 0.9 if q_state else 0.0
        target_qbar = 0.0 if q_state else 0.9
        if wrong_hold and phase_index >= 2 and s == 0 and r == 0:
            target_q = 0.45
            target_qbar = 0.45
        for sample_index in range(20):
            time_ns = start_ns + sample_index * 0.25
            rows.append(
                {
                    "time": time_ns * NS,
                    "vin_s": _transition(
                        0.9 if previous_inputs[0] else 0.0,
                        0.9 if s else 0.0,
                        start_ns,
                        time_ns,
                        0.20,
                    ),
                    "vin_r": _transition(
                        0.9 if previous_inputs[1] else 0.0,
                        0.9 if r else 0.0,
                        start_ns,
                        time_ns,
                        0.20,
                    ),
                    "vout_q": _transition(previous_q, target_q, start_ns, time_ns, 0.90),
                    "vout_qbar": _transition(previous_qbar, target_qbar, start_ns, time_ns, 0.90),
                }
            )
        previous_inputs = inputs
        previous_q = target_q
        previous_qbar = target_qbar
    return rows


def _slow_sum5_rows(*, wrong_output: bool = False) -> list[dict[str, float]]:
    weights = {5: 0.5, 4: 0.25, 3: 0.125, 2: 0.0625, 1: 0.03125}
    states = [
        (0, 0, 0, 0, 0),
        (1, 0, 0, 0, 0),
        (1, 1, 0, 0, 0),
        (1, 1, 1, 0, 0),
        (1, 1, 1, 1, 0),
        (1, 1, 1, 1, 1),
        (0, 1, 0, 1, 0),
        (1, 0, 1, 0, 1),
    ]

    def expected(bits: tuple[int, int, int, int, int]) -> float:
        signed_sum = sum(weights[bit] if bits[bit - 1] else -weights[bit] for bit in range(1, 6))
        return 1.1 * (2.0 * signed_sum - 1.0)

    rows: list[dict[str, float]] = []
    previous_bits = states[0]
    previous_out = expected(previous_bits)
    for state_index, bits in enumerate(states):
        start_ns = state_index * 5.0
        target = expected(bits)
        if wrong_output and state_index >= 2:
            target *= 0.5
        for sample_index in range(20):
            time_ns = start_ns + sample_index * 0.25
            row = {"time": time_ns * NS}
            for bit_index, bit in enumerate(bits, start=1):
                old_level = 1.1 if previous_bits[bit_index - 1] else 0.0
                new_level = 1.1 if bit else 0.0
                row[f"d{bit_index}"] = _transition(old_level, new_level, start_ns, time_ns, 0.20)
            row["out"] = _transition(previous_out, target, start_ns, time_ns, 0.90)
            rows.append(row)
        previous_bits = bits
        previous_out = target
    return rows


def _slow_sar4_rows(*, wrong_output: bool = False) -> list[dict[str, float]]:
    codes = [0, 1, 3, 7, 15, 2, 12, 5]
    rows: list[dict[str, float]] = []
    previous_code = codes[0]
    previous_out = previous_code * 1.8 / 16.0
    for state_index, code in enumerate(codes):
        start_ns = state_index * 5.0
        target = code * 1.8 / 16.0
        if wrong_output and state_index >= 2:
            target *= 0.5
        for sample_index in range(20):
            time_ns = start_ns + sample_index * 0.25
            row = {"time": time_ns * NS, "gnd": 0.0}
            for bit in range(4):
                old_level = 1.8 if previous_code & (1 << bit) else 0.0
                new_level = 1.8 if code & (1 << bit) else 0.0
                row[f"d{bit}"] = _transition(old_level, new_level, start_ns, time_ns, 0.20)
            row["vout"] = _transition(previous_out, target, start_ns, time_ns, 0.90)
            rows.append(row)
        previous_code = code
        previous_out = target
    return rows


def test_slow_pwl_settle_samples_are_ignored_without_weakening_sum5_mutation_detection() -> None:
    ok, note = check_v3_sum5_signed_sar_weight(_slow_sum5_rows())
    assert ok, note

    mutation_ok, mutation_note = check_v3_sum5_signed_sar_weight(_slow_sum5_rows(wrong_output=True))
    assert not mutation_ok, mutation_note


def test_slow_pwl_settle_samples_are_ignored_without_weakening_rs_latch_detection() -> None:
    ok, note = check_v3_rs_latch_voltage(_slow_rs_latch_rows())
    assert ok, note

    mutation_ok, mutation_note = check_v3_rs_latch_voltage(_slow_rs_latch_rows(wrong_hold=True))
    assert not mutation_ok, mutation_note


def test_slow_pwl_settle_samples_are_ignored_without_weakening_sar4_mutation_detection() -> None:
    ok, note = check_v3_lt_readout_sar4(_slow_sar4_rows())
    assert ok, note

    mutation_ok, mutation_note = check_v3_lt_readout_sar4(_slow_sar4_rows(wrong_output=True))
    assert not mutation_ok, mutation_note


def _sparse_initial_window_rows() -> list[dict[str, float]]:
    rows = _load_rows(EVAS_FULL400 / "v4-807/affine/correct/output/tran.csv")
    first_phase_event = min(rising_edges(rows, "phi1") + rising_edges(rows, "phi2"))
    pre = [row for row in rows if row["time"] < first_phase_event]
    post = [row for row in rows if row["time"] >= first_phase_event]
    sparse_pre = [pre[0], pre[len(pre) // 2], pre[-1]]
    assert len(sparse_pre) < 8
    assert sample_step(sparse_pre + post) == pytest.approx(sample_step(rows))
    return sparse_pre + post


def test_task807_initial_coverage_uses_semantic_time_not_raw_row_count() -> None:
    ok, note = check_v4_307_switched_capacitor_integrator_phase_pair(
        _sparse_initial_window_rows()
    )

    assert ok, note
    assert "initial_errors=0" in note


def _pwl(time_ns: float, points: list[tuple[float, float]]) -> float:
    if time_ns <= points[0][0]:
        return points[0][1]
    for (left_t, left_v), (right_t, right_v) in zip(points, points[1:]):
        if time_ns <= right_t:
            return _transition(left_v, right_v, left_t, time_ns, right_t - left_t)
    return points[-1][1]


def _clock_from_edges(time_ns: float, edges_ns: list[float]) -> float:
    for edge_ns in edges_ns:
        rise_start = edge_ns - 0.03
        rise_end = edge_ns + 0.03
        fall_start = edge_ns + 0.62
        fall_end = edge_ns + 0.68
        if rise_start <= time_ns <= rise_end:
            return _transition(0.0, 0.9, rise_start, time_ns, rise_end - rise_start)
        if rise_end < time_ns < fall_start:
            return 0.9
        if fall_start <= time_ns <= fall_end:
            return _transition(0.9, 0.0, fall_start, time_ns, fall_end - fall_start)
    return 0.0


def _coincident_enable_clock_rows() -> list[dict[str, float]]:
    clk_a_edges = [4.0, 8.0, 13.0, 18.0, 22.0, 26.0, 30.0, 38.0, 42.0, 46.0, 52.0, 56.0]
    clk_b_edges = [5.0, 9.0, 15.0, 19.0, 23.0, 27.0, 31.0, 43.0, 47.0, 53.0, 57.0]
    clock_events = sorted([(time_ns, "a") for time_ns in clk_a_edges] + [(time_ns, "b") for time_ns in clk_b_edges])
    vin_a_points = [(0.0, 0.70), (24.0, 0.70), (24.1, 0.47), (40.0, 0.47), (40.1, 0.72), (60.0, 0.72)]
    vin_b_points = [(0.0, 0.40), (24.0, 0.40), (24.1, 0.44), (40.0, 0.44), (40.1, 0.39), (60.0, 0.39)]
    enable_points = [
        (0.0, 0.0),
        (3.94, 0.0),
        (3.98, 0.9),
        (38.0, 0.9),
        (38.04, 0.0),
        (40.0, 0.0),
        (40.04, 0.9),
        (60.0, 0.9),
    ]
    rst_points = [(0.0, 0.9), (1.0, 0.9), (1.04, 0.0), (34.0, 0.0), (34.04, 0.9), (36.0, 0.9), (36.04, 0.0), (60.0, 0.0)]
    control_edges = [34.02, 38.02]

    sa_start = sb_start = sa_target = sb_target = 0.45
    sa_start_ns = sb_start_ns = 0.0
    ready_start = ready_target = 0.0
    ready_start_ns = 0.0
    ready_a = ready_b = False
    consecutive = 0
    current_metric = (0.0, 0.0, 0.0)
    metric_targets: list[tuple[float, tuple[float, float, float], tuple[float, float, float]]] = []
    event_index = 0

    def set_ready_target(target_ns: float) -> None:
        nonlocal ready_start, ready_target, ready_start_ns
        next_target = 0.9 if ready_a and ready_b else 0.0
        if next_target != ready_target:
            ready_start = _transition(ready_start, ready_target, ready_start_ns, target_ns, 0.20)
            ready_target = next_target
            ready_start_ns = target_ns

    for tick_index in range(int(60.0 / 0.5) + 1):
        tick_ns = tick_index * 0.5
        while event_index < len(clock_events) and clock_events[event_index][0] <= tick_ns + 1e-12:
            event_ns, channel = clock_events[event_index]
            control_edge_at_clock = any(abs(event_ns - control_edge_ns) <= 0.08 for control_edge_ns in control_edges)
            if _pwl(event_ns, rst_points) > VTH or _pwl(event_ns, enable_points) <= VTH or control_edge_at_clock:
                sa_start = _transition(sa_start, sa_target, sa_start_ns, event_ns, 0.20)
                sb_start = _transition(sb_start, sb_target, sb_start_ns, event_ns, 0.20)
                sa_target = sb_target = 0.45
                sa_start_ns = sb_start_ns = event_ns
                ready_a = ready_b = False
                consecutive = 0
            elif channel == "a":
                sa_start = _transition(sa_start, sa_target, sa_start_ns, event_ns, 0.20)
                sa_target = _pwl(event_ns, vin_a_points)
                sa_start_ns = event_ns
                ready_a = True
            else:
                sb_start = _transition(sb_start, sb_target, sb_start_ns, event_ns, 0.20)
                sb_target = _pwl(event_ns, vin_b_points)
                sb_start_ns = event_ns
                ready_b = True
            set_ready_target(event_ns)
            event_index += 1

        ready_at_tick = _transition(ready_start, ready_target, ready_start_ns, tick_ns, 0.20)
        if _pwl(tick_ns, rst_points) > VTH or _pwl(tick_ns, enable_points) <= VTH or ready_at_tick <= VTH:
            consecutive = 0
            next_metric = (0.0, 0.0, 0.0)
        else:
            sa = _transition(sa_start, sa_target, sa_start_ns, tick_ns, 0.20)
            sb = _transition(sb_start, sb_target, sb_start_ns, tick_ns, 0.20)
            skew = abs(sa - sb)
            magnitude = 0.5 * (abs(sa - 0.45) + abs(sb - 0.45))
            consecutive = consecutive + 1 if skew > 0.04 else 0
            next_metric = (skew, magnitude, 0.9 if consecutive >= 2 else 0.0)
        metric_targets.append((tick_ns, current_metric, next_metric))
        current_metric = next_metric

    def output(time_ns: float, output_index: int) -> float:
        tick_index = min(int((time_ns + 1e-12) / 0.5), len(metric_targets) - 1)
        tick_ns, old_metric, new_metric = metric_targets[tick_index]
        return _transition(old_metric[output_index], new_metric[output_index], tick_ns, time_ns, 0.20)

    times_ns = {round(index * 0.02, 12) for index in range(int(60.0 / 0.02) + 1)}
    for edge_ns in clk_a_edges + clk_b_edges:
        times_ns.update((edge_ns - 0.03, edge_ns, edge_ns + 0.03, edge_ns + 0.62, edge_ns + 0.68))
    times_ns.update(point[0] for point in enable_points + rst_points + vin_a_points + vin_b_points)

    return [
        {
            "time": time_ns * NS,
            "vin_a": _pwl(time_ns, vin_a_points),
            "vin_b": _pwl(time_ns, vin_b_points),
            "clk_a": _clock_from_edges(time_ns, clk_a_edges),
            "clk_b": _clock_from_edges(time_ns, clk_b_edges),
            "rst": _pwl(time_ns, rst_points),
            "enable": _pwl(time_ns, enable_points),
            "skew_metric": output(time_ns, 0),
            "magnitude_metric": output(time_ns, 1),
            "alarm": output(time_ns, 2),
        }
        for time_ns in sorted(time_ns for time_ns in times_ns if 0.0 <= time_ns <= 60.0)
    ]


def test_task812_control_threshold_transition_at_clock_blocks_capture() -> None:
    ok, note = check_v4_312_interleaved_adc_skew_monitor(_coincident_enable_clock_rows())

    assert ok, note
    assert "skew_errors=0" in note
    assert "alarm_errors=0" in note
