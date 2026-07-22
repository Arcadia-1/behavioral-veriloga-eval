from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

from checkers.v4.task_381 import check_v4_940_fm_vco_modulation_source


def _level(value: float) -> bool:
    return value > 0.45


def _metric(mod_in: float) -> float:
    freq = max(1.0e6, 10.0e6 + 5.0e6 * (mod_in - 0.45))
    return min(0.9, max(0.0, freq / 20.0e6 * 0.9))


def _legacy_weak_accepts(rows: list[dict[str, float]]) -> bool:
    metric_errors = clear_errors = checked = 0
    reset_clear = disabled_clear = low_metric = high_metric = valid_seen = False
    osc_vals: list[float] = []
    marker_vals: list[float] = []
    metric_vals: list[float] = []
    previous_marker_high = _level(rows[0]["phase_marker"])
    marker_rises = 0
    for row in rows[::6]:
        rst = _level(row["rst"])
        enable = _level(row["enable"])
        if not enable or rst:
            clear = row["osc_out"] < 0.12 and row["freq_metric"] < 0.08 and row["phase_marker"] < 0.12 and row["valid"] < 0.10
            reset_clear = reset_clear or (rst and clear)
            disabled_clear = disabled_clear or ((not rst) and (not enable) and clear)
            clear_errors += int(not clear)
            continue
        expected_metric = _metric(row["mod_in"])
        low_metric = low_metric or expected_metric < 0.45
        high_metric = high_metric or expected_metric > 0.45
        osc_vals.append(row["osc_out"])
        marker_vals.append(row["phase_marker"])
        metric_vals.append(row["freq_metric"])
        valid_seen = valid_seen or _level(row["valid"])
        checked += 1
        metric_errors += int(abs(row["freq_metric"] - expected_metric) > 0.10)
    for row in rows:
        rst = _level(row["rst"])
        enable = _level(row["enable"])
        if not enable or rst:
            previous_marker_high = _level(row["phase_marker"])
            continue
        marker_high = _level(row["phase_marker"])
        marker_rise = not previous_marker_high and marker_high
        marker_rises += int(marker_rise)
        previous_marker_high = marker_high
    return (
        checked >= 12
        and reset_clear
        and disabled_clear
        and low_metric
        and high_metric
        and ((max(metric_vals) - min(metric_vals)) if metric_vals else 0.0) >= 0.055
        and max(osc_vals) > 0.65
        and min(osc_vals) < 0.20
        and max(marker_vals) > 0.65
        and min(marker_vals) < 0.20
        and marker_rises > 0
        and valid_seen
        and metric_errors <= 4
        and clear_errors <= 4
    )


def _pre_cadence_period_accepts(rows: list[dict[str, float]]) -> bool:
    edge_times = {"nominal": [], "high": [], "clamp": []}
    previous_marker_high = _level(rows[0]["phase_marker"])
    for row in rows[1:]:
        marker_high = _level(row["phase_marker"])
        marker_rise = not previous_marker_high and marker_high
        previous_marker_high = marker_high
        if not marker_rise or not _level(row["enable"]) or _level(row["rst"]):
            continue
        if abs(row["mod_in"] - 0.45) <= 0.05:
            edge_times["nominal"].append(row["time"])
        elif row["mod_in"] >= 0.70:
            edge_times["high"].append(row["time"])
        elif row["mod_in"] <= -1.0:
            edge_times["clamp"].append(row["time"])
    expected = {"nominal": 100.0e-9, "high": 1.0 / 12.0e6, "clamp": 1.0e-6}
    measured = {
        bucket: sum(b - a for a, b in zip(times, times[1:])) / (len(times) - 1)
        for bucket, times in edge_times.items()
        if len(times) >= 2
    }
    if len(measured) != 3:
        return False
    scales = [measured[bucket] / expected[bucket] for bucket in measured]
    reference_scale = sum(scales) / len(scales)
    return all(abs(scale / reference_scale - 1.0) <= 0.18 for scale in scales)


def _rows(
    *,
    clamp_period_ns: float = 1000.0,
    constant_period_ns: float | None = None,
    extra_marker_event: bool = False,
    immediate_valid: bool = False,
    marker_drift_ns: float = 0.0,
    marker_every_two_cycles: bool = False,
    marker_mode: str = "toggle",
    marker_phase: str = "falling",
    one_shot_valid: bool = False,
) -> list[dict[str, float]]:
    nominal_edges_ns = [125.0, 225.0, 325.0]
    high_edges_ns = [525.0, 605.0, 685.0, 765.0]
    clamp_edges_ns = [855.0 + clamp_period_ns * index for index in range(1, 4)]
    cycle_edges_ns = nominal_edges_ns + high_edges_ns + clamp_edges_ns
    if constant_period_ns is not None:
        nominal_edges_ns = [105.0 + constant_period_ns * index for index in range(7)]
        clamp_edges_ns = [855.0 + constant_period_ns * index for index in range(1, 34)]
        high_edges_ns = []
        cycle_edges_ns = nominal_edges_ns + clamp_edges_ns
    if constant_period_ns is not None:
        nominal_rising_edges_ns = [edge - 0.5 * constant_period_ns for edge in nominal_edges_ns]
        high_rising_edges_ns: list[float] = []
        clamp_rising_edges_ns = [edge - 0.5 * constant_period_ns for edge in clamp_edges_ns]
    else:
        nominal_rising_edges_ns = [edge - 50.0 for edge in nominal_edges_ns]
        high_rising_edges_ns = [edge - 40.0 for edge in high_edges_ns]
        clamp_rising_edges_ns = [edge - 0.5 * clamp_period_ns for edge in clamp_edges_ns]
    rising_edges_ns = nominal_rising_edges_ns + high_rising_edges_ns + clamp_rising_edges_ns
    marker_groups = (
        (nominal_rising_edges_ns, high_rising_edges_ns, clamp_rising_edges_ns)
        if marker_phase == "rising"
        else (nominal_edges_ns, high_edges_ns, clamp_edges_ns)
    )
    marker_edges_ns = [edge for group in marker_groups for edge in group]
    if marker_every_two_cycles:
        marker_edges_ns = [edge for group in marker_groups for edge in group[::2]]
    marker_edges_ns = [
        edge + index * marker_drift_ns for index, edge in enumerate(marker_edges_ns)
    ]
    if extra_marker_event:
        marker_edges_ns += [edge + 20.0 for edge in marker_edges_ns]
    osc_edges_ns = sorted(cycle_edges_ns + rising_edges_ns)
    first_cycle_pre = min(edge for edge in cycle_edges_ns if edge < 805.0)
    first_cycle_post = min(edge for edge in cycle_edges_ns if edge > 830.0)
    rows: list[dict[str, float]] = []
    for step in range(0, 4221, 5):
        time_ns = float(step)
        rst = 0.9 if time_ns <= 3.0 or 805.0 <= time_ns <= 830.0 else 0.0
        enable = 0.9 if 5.0 <= time_ns < 4200.0 else 0.0
        active = enable > 0.45 and rst <= 0.45
        if time_ns < 420.0:
            mod_in = 0.45
        elif time_ns < 840.0:
            mod_in = 0.85
        else:
            mod_in = -2.0
        if not active:
            osc_out = freq_metric = phase_marker = valid = 0.0
        else:
            segment_floor = 0.0 if time_ns < 805.0 else 830.0
            osc_out = 0.9 if sum(segment_floor < edge <= time_ns for edge in osc_edges_ns) % 2 else 0.0
            if marker_mode == "pulse":
                phase_marker = 0.9 if any(edge <= time_ns < edge + 5.0 for edge in marker_edges_ns) else 0.0
            else:
                phase_marker = 0.9 if sum(segment_floor < edge <= time_ns for edge in marker_edges_ns) % 2 else 0.0
            freq_metric = _metric(mod_in)
            first_cycle_done = (time_ns >= first_cycle_pre and time_ns < 805.0) or time_ns >= first_cycle_post
            if one_shot_valid:
                valid = 0.9 if (first_cycle_pre <= time_ns < first_cycle_pre + 10.0 or first_cycle_post <= time_ns < first_cycle_post + 10.0) else 0.0
            else:
                valid = 0.9 if (immediate_valid or first_cycle_done) else 0.0
        rows.append({
            "time": time_ns * 1e-9,
            "mod_in": mod_in,
            "enable": enable,
            "rst": rst,
            "osc_out": osc_out,
            "freq_metric": freq_metric,
            "phase_marker": phase_marker,
            "valid": valid,
        })
    return rows


def _rows_with_solver_dense_sample_and_hold_intervals() -> list[dict[str, float]]:
    rows = [dict(row) for row in _rows()]
    by_time_ns = {round(row["time"] * 1.0e9, 9): row for row in rows}

    # Enable changes just after the 5.0 ns tick.  The reference DUT therefore
    # holds zero until the 5.5 ns tick and its 200 ps output transition settles.
    at_5ns = by_time_ns[5.0]
    at_5ns["enable"] = 0.0
    at_5ns["freq_metric"] = 0.0
    for index in range(1, 36):
        time_ns = 5.0 + 0.02 * index
        row = dict(at_5ns)
        row["time"] = time_ns * 1.0e-9
        row["enable"] = 0.9
        if time_ns <= 5.5:
            row["freq_metric"] = 0.0
        elif time_ns < 5.7:
            row["freq_metric"] = 0.45 * (time_ns - 5.5) / 0.2
        else:
            row["freq_metric"] = 0.45
        rows.append(row)

    # The clamp command likewise changes just after the 840.0 ns tick.  Dense
    # solver rows before 840.7 ns are valid held/transition samples, not 1 row
    # per independent frequency-transfer failure.
    at_840ns = by_time_ns[840.0]
    at_840ns["mod_in"] = 0.85
    at_840ns["freq_metric"] = _metric(0.85)
    for index in range(1, 36):
        time_ns = 840.0 + 0.02 * index
        row = dict(at_840ns)
        row["time"] = time_ns * 1.0e-9
        row["mod_in"] = -2.0
        if time_ns <= 840.5:
            row["freq_metric"] = _metric(0.85)
        elif time_ns < 840.7:
            alpha = (time_ns - 840.5) / 0.2
            row["freq_metric"] = _metric(0.85) + alpha * (_metric(-2.0) - _metric(0.85))
        else:
            row["freq_metric"] = _metric(-2.0)
        rows.append(row)
    return sorted(rows, key=lambda row: row["time"])


def test_task381_gold_like_trace_covers_period_valid_and_clamp() -> None:
    ok, detail = check_v4_940_fm_vco_modulation_source(_rows(marker_mode="toggle"))
    assert ok, detail


def test_task381_accepts_dense_rows_during_sample_and_hold_latency() -> None:
    ok, detail = check_v4_940_fm_vco_modulation_source(
        _rows_with_solver_dense_sample_and_hold_intervals()
    )
    assert ok, detail


def test_task381_period_checks_are_timing_metamorphic() -> None:
    rows = []
    for row in _rows():
        shifted = dict(row)
        shifted["time"] = 1.37 * row["time"] + 2.0e-9
        rows.append(shifted)
    ok, detail = check_v4_940_fm_vco_modulation_source(rows)
    assert ok, detail


def test_task381_accepts_narrow_pulse_phase_marker() -> None:
    ok, detail = check_v4_940_fm_vco_modulation_source(_rows(marker_mode="pulse"))
    assert ok, detail


def test_task381_accepts_rising_edge_pulse_under_timing_metamorph() -> None:
    rows = []
    for row in _rows(marker_mode="pulse", marker_phase="rising"):
        shifted = dict(row)
        shifted["time"] = 1.37 * row["time"] + 2.0e-9
        rows.append(shifted)
    ok, detail = check_v4_940_fm_vco_modulation_source(rows)
    assert ok, detail


def test_task381_rejects_marker_event_only_every_two_cycles() -> None:
    rows = _rows(marker_mode="pulse", marker_every_two_cycles=True)
    assert _pre_cadence_period_accepts(rows)
    ok, detail = check_v4_940_fm_vco_modulation_source(rows)
    assert not ok
    assert "P_PHASE_MARKER_CADENCE" in detail


def test_task381_rejects_multiple_marker_events_per_cycle() -> None:
    ok, detail = check_v4_940_fm_vco_modulation_source(
        _rows(marker_mode="pulse", extra_marker_event=True)
    )
    assert not ok
    assert "P_PHASE_MARKER_ALIGNMENT" in detail


def test_task381_rejects_drifting_marker_phase() -> None:
    ok, detail = check_v4_940_fm_vco_modulation_source(
        _rows(marker_mode="pulse", marker_drift_ns=1.0)
    )
    assert not ok
    assert "P_PHASE_MARKER_ALIGNMENT" in detail


def test_task381_rejects_old_pass_constant_frequency_oscillator() -> None:
    rows = _rows(constant_period_ns=100.0)
    assert _legacy_weak_accepts(rows)
    ok, detail = check_v4_940_fm_vco_modulation_source(rows)
    assert not ok
    assert "P_PERIOD_ORDERING" in detail


def test_task381_rejects_old_pass_immediate_valid() -> None:
    rows = _rows(immediate_valid=True)
    assert _legacy_weak_accepts(rows)
    ok, detail = check_v4_940_fm_vco_modulation_source(rows)
    assert not ok
    assert "P_VALID_AFTER_ENABLE" in detail


def test_task381_rejects_one_shot_valid() -> None:
    ok, detail = check_v4_940_fm_vco_modulation_source(_rows(one_shot_valid=True))
    assert not ok
    assert "P_VALID_AFTER_ENABLE" in detail


def test_task381_rejects_500ns_lower_clamp_period() -> None:
    ok, detail = check_v4_940_fm_vco_modulation_source(_rows(clamp_period_ns=500.0))
    assert not ok
    assert "P_PERIOD_MODEL" in detail
