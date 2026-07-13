"""Task-specific checker for canonical v4 DUT 032."""
from __future__ import annotations

from checkers.api import Checker
def _threshold_crossings(
    values: list[float],
    times: list[float],
    *,
    threshold: float = 0.0,
    direction: str,
) -> list[float]:
    edges: list[float] = []
    for idx in range(1, len(values)):
        v0 = values[idx - 1]
        v1 = values[idx]
        if direction == "rising":
            hit = v0 <= threshold < v1
        elif direction == "falling":
            hit = v0 >= threshold > v1
        else:
            raise ValueError(f"unsupported direction={direction!r}")
        if not hit:
            continue
        t0 = times[idx - 1]
        t1 = times[idx]
        if v1 == v0:
            edges.append(t1)
        else:
            alpha = (threshold - v0) / (v1 - v0)
            edges.append(t0 + alpha * (t1 - t0))
    return edges

def sample_signal_at(rows: list[dict[str, float]], signal: str, time_s: float) -> float | None:
    if not rows or "time" not in rows[0] or signal not in rows[0]:
        return None
    first_time = rows[0]["time"]
    last_time = rows[-1].get("time")
    if last_time is None or time_s < first_time or time_s > last_time:
        return None
    if time_s == first_time:
        return rows[0].get(signal)
    for idx in range(1, len(rows)):
        prev = rows[idx - 1]
        cur = rows[idx]
        t0 = prev.get("time")
        t1 = cur.get("time")
        if t0 is None or t1 is None:
            continue
        if t0 <= time_s <= t1:
            v0 = prev.get(signal)
            v1 = cur.get(signal)
            if v0 is None or v1 is None:
                return None
            if t1 == t0:
                return v1
            alpha = (time_s - t0) / (t1 - t0)
            return v0 + alpha * (v1 - v0)
    return None

def mean_in_window(rows: list[dict[str, float]], key: str, start: float, stop: float) -> float | None:
    values = [r[key] for r in rows if start <= r["time"] <= stop and key in r]
    if not values:
        return None
    return sum(values) / len(values)

def _check_clocked_rf_macro_state_contract(
    rows: list[dict[str, float]],
    *,
    label: str,
) -> tuple[bool, str]:
    times = [row["time"] for row in rows]
    clk_rises = _threshold_crossings(
        [row["clk"] for row in rows],
        times,
        threshold=0.45,
        direction="rising",
    )
    failures: list[str] = []
    hold_checks = 0
    max_hold_span = 0.0
    for prev_t, next_t in zip(clk_rises, clk_rises[1:]):
        left_t = prev_t + 0.45e-9
        right_t = next_t - 0.20e-9
        if right_t <= left_t:
            continue
        left_out = sample_signal_at(rows, "out", left_t)
        right_out = sample_signal_at(rows, "out", right_t)
        left_metric = sample_signal_at(rows, "metric", left_t)
        right_metric = sample_signal_at(rows, "metric", right_t)
        if None in (left_out, right_out, left_metric, right_metric):
            continue
        assert left_out is not None and right_out is not None
        assert left_metric is not None and right_metric is not None
        hold_checks += 1
        hold_span = max(abs(right_out - left_out), abs(right_metric - left_metric))
        max_hold_span = max(max_hold_span, hold_span)
        if abs(right_out - left_out) > 0.025 or abs(right_metric - left_metric) > 0.08:
            failures.append(
                f"{label}_clocked_hold observed=out:{left_out:.3f}->{right_out:.3f},"
                f"metric:{left_metric:.3f}->{right_metric:.3f} expected=held "
                f"window={left_t * 1e9:.3f}-{right_t * 1e9:.3f}ns"
            )
            break

    reset_samples: list[float] = []
    if rows[0]["rst"] > 0.45:
        reset_samples.append(min(rows[-1]["time"], rows[0]["time"] + 0.50e-9))
    for edge_t in clk_rises:
        rst_at_edge = sample_signal_at(rows, "rst", edge_t + 1e-15)
        if rst_at_edge is not None and rst_at_edge > 0.45:
            reset_samples.append(min(rows[-1]["time"], edge_t + 0.40e-9))
    reset_checks = 0
    for sample_t in reset_samples:
        out = sample_signal_at(rows, "out", sample_t)
        metric = sample_signal_at(rows, "metric", sample_t)
        if out is None or metric is None:
            continue
        reset_checks += 1
        if abs(out - 0.45) > 0.045 or abs(metric) > 0.08:
            failures.append(
                f"{label}_reset_common_mode observed=out:{out:.3f},metric:{metric:.3f} "
                f"expected=out:0.450,metric:0.000 window={sample_t * 1e9:.3f}ns"
            )
            break

    out_min = min(row["out"] for row in rows)
    out_max = max(row["out"] for row in rows)
    if out_min < 0.025 or out_max > 0.875:
        failures.append(
            f"{label}_output_clamp observed=range:{out_min:.3f}..{out_max:.3f} "
            "expected=0.040..0.860_with_tolerance window=full_trace"
        )
    if len(clk_rises) >= 3 and (hold_checks == 0 or reset_checks == 0):
        failures.append(
            f"{label}_contract_coverage observed=hold:{hold_checks},reset:{reset_checks} "
            "expected=hold>=1,reset>=1 window=full_trace"
        )
    if failures:
        return False, " ".join(failures[:4])
    return True, (
        f"{label}_state_contract hold_checks={hold_checks} reset_checks={reset_checks} "
        f"max_hold_span={max_hold_span:.4f} output_range={out_min:.3f}..{out_max:.3f}"
    )

def check_lna_gain_compression_macro(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst/vin/out/metric"
    state_ok, state_note = _check_clocked_rf_macro_state_contract(rows, label="lna")
    if not state_ok:
        return False, state_note

    small_vin = mean_in_window(rows, "vin", 12.0e-9, 22.0e-9)
    small_out = mean_in_window(rows, "out", 12.0e-9, 22.0e-9)
    comp_high = mean_in_window(rows, "out", 34.0e-9, 44.0e-9)
    comp_low = mean_in_window(rows, "out", 55.0e-9, 63.0e-9)
    comp_metric = mean_in_window(rows, "metric", 34.0e-9, 63.0e-9)
    if None in (small_vin, small_out, comp_high, comp_low, comp_metric):
        return False, "lna_missing_sample_windows"
    assert small_vin is not None
    assert small_out is not None
    assert comp_high is not None
    assert comp_low is not None
    assert comp_metric is not None

    if small_out <= small_vin + 0.045:
        return False, f"lna_small_signal_gain_missing vin={small_vin:.3f} out={small_out:.3f}"
    if not (0.74 <= comp_high <= 0.87):
        return False, f"lna_high_compression_wrong={comp_high:.3f}"
    if not (0.04 <= comp_low <= 0.18):
        return False, f"lna_low_compression_wrong={comp_low:.3f}"
    if comp_metric < 0.55:
        return False, f"lna_compression_metric_low={comp_metric:.3f}"
    return True, (
        "lna_gain_compression_macro "
        f"small={small_vin:.3f}->{small_out:.3f} compressed={comp_low:.3f}/{comp_high:.3f} "
        f"{state_note}"
    )

CHECKER_ID = "v4_032_lna_gain_compression_macro"
CHECKER: Checker = check_lna_gain_compression_macro
