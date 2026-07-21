from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

from checkers.v4.task_322 import check_v4_1020_glitchless_clock_mux_selector
from checkers.v4.task_323 import check_v4_1021_programmable_clock_skew_aligner
from checkers.v4.task_325 import check_v4_325_fine_coarse_tdc_encoder
from checkers.v4.task_326 import check_v4_1024_fractional_delay_dtc_macro
from checkers.v4.task_331 import check_v4_331_dfe_error_proxy_loop


VDD = 0.9
VCM = 0.45


def _high(row: dict[str, float], name: str, threshold: float = 0.45) -> bool:
    return float(row.get(name, 0.0)) > threshold


def _rising(prev: float, now: float, threshold: float = 0.45) -> bool:
    return now > threshold and prev <= threshold


def _code(row: dict[str, float], bits: list[str]) -> int:
    return sum((1 << idx) for idx, bit in enumerate(bits) if _high(row, bit))


def _level_at_edges(time_ns: float, edges_ns: list[float]) -> float:
    return VDD if sum(edge <= time_ns for edge in edges_ns) % 2 else 0.0


def _pulse_level(time_ns: float, edges_ns: list[float], width_ns: float = 0.5) -> float:
    return VDD if any(edge <= time_ns < edge + width_ns for edge in edges_ns) else 0.0


def _legacy_322_accepts(rows: list[dict[str, float]]) -> bool:
    active = pending = 0
    switched_at = -1.0
    first_edge_seen = False
    checked = out_errors = glitch_errors = valid_errors = clear_errors = 0
    reset_clear = disabled_clear = switch_seen = False
    src_seen: set[int] = set()
    inactive_time: float | None = None
    prev_clk_a = float(rows[0].get("clk_a", 0.0))
    prev_clk_b = float(rows[0].get("clk_b", 0.0))
    last_input_rise = -1.0
    prev_out = float(rows[0].get("clk_out", 0.0))
    switch_windows: list[dict[str, float | bool]] = []
    for row in rows:
        t = float(row["time"])
        rst = _high(row, "rst")
        clk_a = float(row["clk_a"])
        clk_b = float(row["clk_b"])
        enabled = _high(row, "enable") and not rst
        if not enabled:
            if inactive_time is None:
                inactive_time = t
            inactive_ready = t >= inactive_time + 0.7e-9
            active = pending = 0
            first_edge_seen = False
            clear = (
                abs(float(row["clk_out"])) < 0.08
                and abs(float(row["switch_metric"])) < 0.08
                and not _high(row, "valid")
            )
            if rst and inactive_ready and clear:
                reset_clear = True
            if (not rst) and (not _high(row, "enable")) and inactive_ready and clear:
                disabled_clear = True
            if inactive_ready and not clear:
                clear_errors += 1
            prev_out = float(row.get("clk_out", 0.0))
            prev_clk_a = clk_a
            prev_clk_b = clk_b
            continue
        inactive_time = None
        pending = 1 if _high(row, "sel") else 0
        both_low = clk_a <= 0.45 and clk_b <= 0.45
        if pending != active and both_low:
            active = pending
            switched_at = t
            switch_seen = True
            first_edge_seen = False
            switch_windows.append({"start": t + 0.5e-9, "end": t + 4.5e-9, "seen": False})
        expected = float(row["clk_b" if active else "clk_a"])
        src_seen.add(active)
        now_out = float(row["clk_out"])
        if _rising(prev_clk_a, clk_a) or _rising(prev_clk_b, clk_b):
            last_input_rise = t
        if prev_out <= 0.45 and now_out > 0.45:
            if last_input_rise < 0 or t - last_input_rise > 0.5e-9:
                glitch_errors += 1
            first_edge_seen = True
        prev_out = now_out
        prev_clk_a = clk_a
        prev_clk_b = clk_b
        metric_high = _high(row, "switch_metric")
        for window in switch_windows:
            if not bool(window["seen"]) and float(window["start"]) <= t <= float(window["end"]) and metric_high:
                window["seen"] = True
        if not first_edge_seen or (switched_at >= 0 and t < switched_at + 0.7e-9):
            continue
        checked += 1
        if abs(now_out - expected) > 0.14:
            out_errors += 1
        if first_edge_seen and not _high(row, "valid"):
            valid_errors += 1
    return (
        checked >= 80
        and reset_clear
        and disabled_clear
        and switch_seen
        and len(src_seen) >= 2
        and out_errors <= max(12, checked // 5)
        and glitch_errors <= 1
        and sum(not bool(window["seen"]) for window in switch_windows) == 0
        and valid_errors <= max(8, checked // 10)
        and clear_errors <= 4
    )


def _rows_322(*, early_valid: bool = False, stuck_metric: bool = False) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    active = 0
    switch_time_ns: float | None = None
    first_edge_seen = False
    prev_out = 0.0
    for idx in range(0, 430):
        t_ns = idx * 0.1
        rst = VDD if t_ns < 1.0 else 0.0
        enable = VDD if 2.0 <= t_ns < 38.0 else 0.0
        sel = VDD if t_ns >= 15.0 else 0.0
        clk_a = _pulse_level(t_ns, [6.0, 8.0, 10.0, 12.0, 14.0, 20.0, 22.0, 24.0, 26.0, 28.0], 0.7)
        clk_b = _pulse_level(t_ns, [18.0, 21.0, 24.0, 27.0, 30.0, 33.0], 0.7)
        if enable <= 0.45 or rst > 0.45:
            active = 0
            first_edge_seen = False
            switch_time_ns = None
            clk_out = switch_metric = valid = 0.0
        else:
            pending = 1 if sel > 0.45 else 0
            if pending != active and clk_a <= 0.45 and clk_b <= 0.45:
                active = pending
                switch_time_ns = t_ns
                first_edge_seen = False
            clk_out = clk_b if active else clk_a
            if prev_out <= 0.45 and clk_out > 0.45:
                first_edge_seen = True
            if stuck_metric:
                switch_metric = VDD
            else:
                switch_metric = (
                    VDD
                    if switch_time_ns is not None and switch_time_ns + 1.0 <= t_ns <= switch_time_ns + 3.0
                    else 0.0
                )
            valid = VDD if (first_edge_seen or early_valid) else 0.0
        rows.append(
            {
                "time": t_ns * 1e-9,
                "clk_a": clk_a,
                "clk_b": clk_b,
                "sel": sel,
                "rst": rst,
                "enable": enable,
                "clk_out": clk_out,
                "switch_metric": switch_metric,
                "valid": valid,
            }
        )
        prev_out = clk_out
    return rows


def _legacy_323_accepts(rows: list[dict[str, float]]) -> bool:
    prev_clk_in = float(rows[0].get("clk_in", 0.0))
    prev_clk_out = float(rows[0].get("clk_out", 0.0))
    checked = timing_errors = metric_errors = valid_errors = clear_errors = 0
    input_edges = output_edges = 0
    reset_clear = disabled_clear = valid_seen = ever_enabled = False
    codes_seen: set[int] = set()
    pending_edges: list[tuple[float, int]] = []
    expected_metric = 0.0
    for row in rows:
        t = float(row["time"])
        rst = _high(row, "rst")
        enabled = _high(row, "enable") and not rst
        if not enabled:
            pending_edges.clear()
            clear = abs(row["clk_out"]) < 0.08 and abs(row["delay_metric"]) < 0.08 and not _high(row, "valid")
            if rst and clear:
                reset_clear = True
            if ever_enabled and not _high(row, "enable") and clear:
                disabled_clear = True
            if ((rst and reset_clear) or (ever_enabled and not _high(row, "enable") and disabled_clear)) and not clear:
                clear_errors += 1
            prev_clk_in = row["clk_in"]
            prev_clk_out = row["clk_out"]
            continue
        ever_enabled = True
        code = _code(row, ["skew_0", "skew_1", "skew_2"])
        if _rising(prev_clk_in, row["clk_in"]):
            input_edges += 1
            codes_seen.add(code)
            expected_metric = 0.1 * code
            pending_edges.append((t, code))
        if _rising(prev_clk_out, row["clk_out"]):
            output_edges += 1
            valid_seen = True
            if pending_edges:
                input_time, edge_code = pending_edges.pop(0)
                if abs((t - input_time) - 0.2e-9 * edge_code) > 0.36e-9:
                    timing_errors += 1
            else:
                timing_errors += 1
        prev_clk_in = row["clk_in"]
        prev_clk_out = row["clk_out"]
        if input_edges == 0:
            continue
        checked += 1
        if abs(row["delay_metric"] - expected_metric) > 0.06:
            metric_errors += 1
        if output_edges > 0 and not _high(row, "valid"):
            valid_errors += 1
    return (
        checked >= 40
        and len(codes_seen) >= 4
        and input_edges >= 5
        and output_edges >= max(3, input_edges - 2)
        and reset_clear
        and disabled_clear
        and valid_seen
        and timing_errors == 0
        and metric_errors <= max(6, checked // 20)
        and valid_errors <= 4
        and clear_errors <= 4
    )


def _rows_323(*, drop_last: int = 0) -> list[dict[str, float]]:
    input_edges = [5.0, 12.0, 19.0, 26.0, 33.0, 40.0]
    codes = [0, 1, 2, 3, 4, 5]
    output_edges = [edge + code * 0.2 for edge, code in zip(input_edges, codes)]
    if drop_last:
        output_edges = output_edges[:-drop_last]
    rows: list[dict[str, float]] = []
    for idx in range(0, 520):
        t_ns = idx * 0.1
        rst = VDD if t_ns < 1.0 else 0.0
        enable = VDD if 2.0 <= t_ns < 48.0 else 0.0
        edge_index = max(0, sum(edge <= t_ns for edge in input_edges) - 1)
        code = codes[min(edge_index, len(codes) - 1)]
        row = {
            "time": t_ns * 1e-9,
            "clk_in": _pulse_level(t_ns, input_edges),
            "rst": rst,
            "enable": enable,
            "skew_0": VDD if code & 1 else 0.0,
            "skew_1": VDD if code & 2 else 0.0,
            "skew_2": VDD if code & 4 else 0.0,
            "clk_out": _pulse_level(t_ns, output_edges),
            "delay_metric": 0.1 * code if enable > 0.45 and rst <= 0.45 else 0.0,
            "valid": VDD if enable > 0.45 and rst <= 0.45 and sum(edge <= t_ns for edge in output_edges) else 0.0,
        }
        rows.append(row)
    return rows


def _legacy_325_accepts(rows: list[dict[str, float]]) -> bool:
    prev_start = rows[0]["start"]
    prev_stop = rows[0]["stop"]
    prev_ref = rows[0]["ref_clk"]
    armed = awaiting_result = False
    ref_edges = 0
    last_ref_time = previous_ref_time = 0.0
    expected_coarse = 0
    expected_fine = 0.0
    checked = latch_errors = fine_errors = valid_errors = 0
    reset_clear = disabled_clear = ever_enabled = False
    coarse_seen: set[int] = set()
    fine_max = 0.0
    valid_edges = 0
    for row in rows:
        rst = _high(row, "rst")
        enabled = _high(row, "enable") and not rst
        coarse = _code(row, ["coarse_0", "coarse_1", "coarse_2", "coarse_3"])
        valid = _high(row, "valid")
        if not enabled:
            clear = coarse == 0 and abs(row["fine_metric"]) < 0.08 and not valid
            if rst and clear:
                reset_clear = True
            if ever_enabled and not _high(row, "enable") and clear:
                disabled_clear = True
            armed = awaiting_result = False
            ref_edges = 0
            prev_start, prev_stop, prev_ref = row["start"], row["stop"], row["ref_clk"]
            continue
        ever_enabled = True
        if _rising(prev_start, row["start"]):
            armed = True
            awaiting_result = False
            ref_edges = 0
            last_ref_time = previous_ref_time = 0.0
        if armed and _rising(prev_ref, row["ref_clk"]):
            ref_edges += 1
            previous_ref_time = last_ref_time
            last_ref_time = row["time"]
        if armed and _rising(prev_stop, row["stop"]):
            expected_coarse = min(ref_edges, 15)
            expected_fine = (
                VDD * min(1.0, max(0.0, (row["time"] - last_ref_time) / (last_ref_time - previous_ref_time)))
                if previous_ref_time > 0 and last_ref_time > previous_ref_time
                else 0.0
            )
            awaiting_result = True
            armed = False
        if armed and not _high(row, "start") and valid:
            valid_errors += 1
        if awaiting_result and row["valid"] > 0.8:
            awaiting_result = False
            checked += 1
            coarse_seen.add(coarse)
            fine_max = max(fine_max, row["fine_metric"])
            if coarse != expected_coarse:
                latch_errors += 1
            if abs(row["fine_metric"] - expected_fine) > 0.12:
                fine_errors += 1
            valid_edges += 1
        prev_start, prev_stop, prev_ref = row["start"], row["stop"], row["ref_clk"]
    return (
        checked >= 3
        and reset_clear
        and disabled_clear
        and valid_edges >= 3
        and len(coarse_seen) >= 2
        and fine_max > 0.05
        and latch_errors <= 1
        and fine_errors <= 1
        and valid_errors <= 1
    )


def _rows_325(*, valid_while_start_high: bool = False) -> list[dict[str, float]]:
    starts = [5.0, 35.0, 65.0]
    stops = [16.5, 49.0, 82.0]
    ref_edges = [8.0, 11.0, 14.0, 38.0, 41.0, 44.0, 47.0, 68.0, 71.0, 74.0, 77.0, 80.0]
    rows: list[dict[str, float]] = []
    for idx in range(0, 960):
        t_ns = idx * 0.1
        rst = VDD if t_ns < 1.0 else 0.0
        enable = VDD if 2.0 <= t_ns < 92.0 else 0.0
        started = [i for i, s in enumerate(starts) if s <= t_ns]
        stopped = [i for i, stop in enumerate(stops) if stop <= t_ns]
        active_meas = next((i for i, s in enumerate(starts) if s <= t_ns < stops[i]), None)
        start_signal = (
            VDD
            if valid_while_start_high and active_meas is not None
            else _pulse_level(t_ns, starts)
        )
        meas = stopped[-1] if stopped else None
        if active_meas is not None:
            coarse = 0
            fine = 0.0
            valid = VDD if valid_while_start_high and active_meas is not None and enable > 0.45 else 0.0
        elif meas is None:
            coarse = 0
            fine = 0.0
            valid = 0.0
        else:
            counts = [sum(s < edge < stops[i] for edge in ref_edges) for i, s in enumerate(starts)]
            coarse = counts[meas]
            before_stop = [edge for edge in ref_edges if starts[meas] < edge < stops[meas]]
            if len(before_stop) >= 2:
                fine = VDD * min(1.0, max(0.0, (stops[meas] - before_stop[-1]) / (before_stop[-1] - before_stop[-2])))
            else:
                fine = 0.0
            valid = VDD
        if enable <= 0.45 or rst > 0.45:
            coarse = 0
            fine = 0.0
            valid = 0.0
        rows.append(
            {
                "time": t_ns * 1e-9,
                "start": start_signal,
                "stop": _pulse_level(t_ns, stops),
                "ref_clk": _pulse_level(t_ns, ref_edges),
                "rst": rst,
                "enable": enable,
                "coarse_0": VDD if coarse & 1 else 0.0,
                "coarse_1": VDD if coarse & 2 else 0.0,
                "coarse_2": VDD if coarse & 4 else 0.0,
                "coarse_3": VDD if coarse & 8 else 0.0,
                "fine_metric": fine,
                "valid": valid,
            }
        )
    return rows


def _legacy_326_accepts(rows: list[dict[str, float]]) -> bool:
    prev_clk = rows[0]["clk_in"]
    input_edges: list[tuple[float, int]] = []
    checked = metric_errors = valid_errors = 0
    reset_clear = disabled_clear = ever_enabled = False
    codes_seen: set[int] = set()
    expected_metric = 0.0
    update_time = -1.0
    for row in rows:
        rst = _high(row, "rst")
        enabled = _high(row, "enable") and not rst
        if not enabled:
            clear = abs(row["clk_out"]) < 0.08 and abs(row["phase_metric"]) < 0.08 and not _high(row, "valid")
            if rst and clear:
                reset_clear = True
            if ever_enabled and not _high(row, "enable") and clear:
                disabled_clear = True
            prev_clk = row["clk_in"]
            continue
        ever_enabled = True
        if _rising(prev_clk, row["clk_in"]):
            code = _code(row, ["frac_0", "frac_1", "frac_2", "frac_3"])
            input_edges.append((row["time"], code))
            codes_seen.add(code)
            expected_metric = 0.9 * code / 15.0
            update_time = row["time"]
        prev_clk = row["clk_in"]
        if update_time >= 0 and row["time"] >= update_time + 0.7e-9:
            checked += 1
            if abs(row["phase_metric"] - expected_metric) > 0.08:
                metric_errors += 1
            if not _high(row, "valid"):
                valid_errors += 1
    output_edges = [
        row["time"]
        for prev, row in zip(rows, rows[1:])
        if _high(row, "enable") and not _high(row, "rst") and _rising(prev["clk_out"], row["clk_out"])
    ]
    delay_errors = matched = monotonic_pairs = 0
    prev_delay = None
    for edge_t, code in input_edges:
        candidates = [out_t for out_t in output_edges if edge_t + 0.05e-9 <= out_t <= edge_t + 5.5e-9]
        if not candidates:
            delay_errors += 1
            continue
        delay = min(candidates) - edge_t
        matched += 1
        if abs(delay - (code + 1) * 0.2e-9) > 0.55e-9:
            delay_errors += 1
        if prev_delay is not None and code >= 8 and delay > prev_delay:
            monotonic_pairs += 1
        prev_delay = delay
    return (
        checked >= 40
        and len(codes_seen) >= 5
        and matched >= 5
        and monotonic_pairs >= 1
        and reset_clear
        and disabled_clear
        and delay_errors <= 2
        and metric_errors <= max(6, checked // 15)
        and valid_errors <= 4
    )


def _rows_326(*, extra_output: bool = False, drop_last: bool = False) -> list[dict[str, float]]:
    input_edges = [5.0, 12.0, 19.0, 26.0, 33.0, 40.0]
    codes = [0, 4, 8, 12, 14, 15]
    output_edges = [edge + (code + 1) * 0.2 for edge, code in zip(input_edges, codes)]
    if extra_output:
        output_edges.insert(2, output_edges[1] + 0.8)
    if drop_last:
        output_edges = output_edges[:-1]
    rows: list[dict[str, float]] = []
    for idx in range(0, 520):
        t_ns = idx * 0.1
        rst = VDD if t_ns < 1.0 else 0.0
        enable = VDD if 2.0 <= t_ns < 48.0 else 0.0
        edge_index = max(0, sum(edge <= t_ns for edge in input_edges) - 1)
        code = codes[min(edge_index, len(codes) - 1)]
        rows.append(
            {
                "time": t_ns * 1e-9,
                "clk_in": _pulse_level(t_ns, input_edges),
                "rst": rst,
                "enable": enable,
                "frac_0": VDD if code & 1 else 0.0,
                "frac_1": VDD if code & 2 else 0.0,
                "frac_2": VDD if code & 4 else 0.0,
                "frac_3": VDD if code & 8 else 0.0,
                "clk_out": _pulse_level(t_ns, output_edges),
                "phase_metric": 0.9 * code / 15.0 if enable > 0.45 and rst <= 0.45 else 0.0,
                "valid": VDD if enable > 0.45 and rst <= 0.45 and sum(edge <= t_ns for edge in output_edges) else 0.0,
            }
        )
    return rows


def _rows_331(*, first_edge_wrong: bool = False) -> list[dict[str, float]]:
    clk_edges = [5.0, 12.0, 19.0, 26.0, 33.0, 40.0]
    sample_values = [0.75, 0.2, 0.7, 0.25, 0.65, 0.3]
    rows: list[dict[str, float]] = []
    w1 = w0 = 0.0
    h1 = h0 = 0
    edge_results: list[tuple[float, float, float, float, float, float]] = []
    for edge_t, sample in zip(clk_edges, sample_values):
        x = sample - VCM
        r0 = x - w1 * h1 - w0 * h0
        w1 = max(-0.18, min(0.18, w1 + 0.04 * r0 * h1))
        w0 = max(-0.12, min(0.12, w0 + 0.025 * r0 * h0))
        residual = x - w1 * h1 - w0 * h0
        decision = 1 if sample >= VCM else -1
        h0, h1 = h1, decision
        edge_results.append((edge_t + 0.6, w1, w0, residual, abs(residual), sample))
    for idx in range(0, 520):
        t_ns = idx * 0.1
        rst = VDD if t_ns < 1.0 else 0.0
        enable = VDD if 2.0 <= t_ns < 48.0 else 0.0
        edge_index = max(0, sum(edge <= t_ns for edge in clk_edges) - 1)
        sample_in = sample_values[min(edge_index, len(sample_values) - 1)]
        active_result = [item for item in edge_results if item[0] <= t_ns]
        if enable <= 0.45 or rst > 0.45 or not active_result:
            tap1 = tap0 = corrected = VCM
            err = conv = 0.0
        else:
            _obs_t, w1_obs, w0_obs, residual, err_raw, _sample = active_result[-1]
            if first_edge_wrong and len(active_result) == 1:
                tap1 = tap0 = corrected = VCM
                err = 0.0
            else:
                tap1 = VCM + w1_obs
                tap0 = VCM + w0_obs
                corrected = max(0.0, min(VDD, VCM + residual))
                err = min(VDD, err_raw)
            conv = 0.0
        rows.append(
            {
                "time": t_ns * 1e-9,
                "sample_in": sample_in,
                "decision_clk": _pulse_level(t_ns, clk_edges),
                "rst": rst,
                "enable": enable,
                "tap_1": tap1,
                "tap_0": tap0,
                "corrected_out": corrected,
                "error_metric": err,
                "converged": conv,
            }
        )
    return rows


def _legacy_331_accepts(rows: list[dict[str, float]]) -> bool:
    # The old checker is equivalent to the current task331 checker except that
    # it skips comparison on active_edges == 1.  These rows intentionally make
    # only that first edge wrong, so the legacy verdict is the repaired verdict
    # after replacing the first-edge observation with the legal one.
    repaired = _rows_331(first_edge_wrong=False)
    ok, _ = check_v4_331_dfe_error_proxy_loop(repaired)
    return ok


def test_task322_rejects_early_valid_before_first_clean_edge() -> None:
    rows = _rows_322(early_valid=True)
    assert _legacy_322_accepts(rows)
    ok, detail = check_v4_1020_glitchless_clock_mux_selector(rows)
    assert not ok
    assert "P_ASSERT_VALID_AFTER_THE_SELECTED_SOURCE" in detail


def test_task322_rejects_stuck_high_switch_metric() -> None:
    rows = _rows_322(stuck_metric=True)
    assert _legacy_322_accepts(rows)
    ok, detail = check_v4_1020_glitchless_clock_mux_selector(rows)
    assert not ok
    assert "P_EXPOSE_A_SWITCH_EVENT_ON_SWITCH" in detail


def test_task322_accepts_legal_clean_switch() -> None:
    ok, detail = check_v4_1020_glitchless_clock_mux_selector(_rows_322())
    assert ok, detail


def test_task323_rejects_dropped_final_input_edges() -> None:
    rows = _rows_323(drop_last=2)
    assert _legacy_323_accepts(rows)
    ok, detail = check_v4_1021_programmable_clock_skew_aligner(rows)
    assert not ok
    assert "P_FOR_EACH_ACCEPTED_INPUT_CLOCK_EDGE" in detail


def test_task323_accepts_all_delayed_edges() -> None:
    ok, detail = check_v4_1021_programmable_clock_skew_aligner(_rows_323())
    assert ok, detail


def test_task325_rejects_valid_while_measurement_is_still_armed() -> None:
    rows = _rows_325(valid_while_start_high=True)
    assert _legacy_325_accepts(rows)
    ok, detail = check_v4_325_fine_coarse_tdc_encoder(rows)
    assert not ok
    assert "P_ASSERT_VALID_ONLY_AFTER_THE_STOP" in detail


def test_task325_accepts_valid_only_after_stop() -> None:
    ok, detail = check_v4_325_fine_coarse_tdc_encoder(_rows_325())
    assert ok, detail


def test_task326_rejects_extra_output_edges() -> None:
    rows = _rows_326(extra_output=True)
    assert _legacy_326_accepts(rows)
    ok, detail = check_v4_1024_fractional_delay_dtc_macro(rows)
    assert not ok
    assert "P_FOR_EACH_INPUT_EDGE_EMIT_ONE" in detail


def test_task326_rejects_missing_final_output_edge() -> None:
    rows = _rows_326(drop_last=True)
    assert _legacy_326_accepts(rows)
    ok, detail = check_v4_1024_fractional_delay_dtc_macro(rows)
    assert not ok
    assert "P_FOR_EACH_INPUT_EDGE_EMIT_ONE" in detail


def test_task326_accepts_one_to_one_delayed_edges() -> None:
    ok, detail = check_v4_1024_fractional_delay_dtc_macro(_rows_326())
    assert ok, detail


def test_task331_rejects_wrong_first_enabled_decision_edge() -> None:
    rows = _rows_331(first_edge_wrong=True)
    assert _legacy_331_accepts(rows)
    ok, detail = check_v4_331_dfe_error_proxy_loop(rows)
    assert not ok
    assert "decision_errors=" in detail


def test_task331_accepts_first_enabled_decision_edge() -> None:
    ok, detail = check_v4_331_dfe_error_proxy_loop(_rows_331())
    assert ok, detail
