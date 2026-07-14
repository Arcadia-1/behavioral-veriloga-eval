"""Task-specific checker for canonical v4 DUT 030."""
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

def check_ldo_regulator_macro_model(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst/vin/out/metric"

    edge_failures: list[str] = []
    state = 0.60
    edge_checks = 0
    reset_checks = 0
    hold_checks = 0
    max_edge_err = 0.0
    max_metric_err = 0.0
    times = [row["time"] for row in rows]
    clk_rises = _threshold_crossings([row["clk"] for row in rows], times, threshold=0.45, direction="rising")
    for edge_t in clk_rises:
        edge_row = _sample_after(rows, edge_t, 1e-15)
        if edge_row["rst"] > 0.45:
            state = 0.60
            expected_metric = 0.90
            reset_checks += 1
        else:
            load = min(0.9, max(0.0, edge_row["vin"]))
            target = 0.62 - 0.055 * load
            state = min(0.75, max(0.25, state + 0.35 * (target - state)))
            expected_metric = min(0.9, max(0.0, 0.9 - 4.0 * abs(state - target)))
        sample = _sample_after(rows, edge_t, 0.35e-9)
        out_err = abs(sample["out"] - state)
        metric_err = abs(sample["metric"] - expected_metric)
        max_edge_err = max(max_edge_err, out_err)
        max_metric_err = max(max_metric_err, metric_err)
        if out_err > 0.055 or metric_err > 0.09:
            edge_failures.append(
                f"clock_edge observed=out:{sample['out']:.3f},metric:{sample['metric']:.3f} "
                f"expected=out:{state:.3f},metric:{expected_metric:.3f} window={edge_t * 1e9:.3f}ns"
            )
        edge_checks += 1

    for prev_t, next_t in zip(clk_rises, clk_rises[1:]):
        if next_t - prev_t < 0.8e-9:
            continue
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
        assert left_out is not None and right_out is not None and left_metric is not None and right_metric is not None
        hold_checks += 1
        if abs(right_out - left_out) > 0.025 or abs(right_metric - left_metric) > 0.08:
            edge_failures.append(
                f"clocked_hold observed=out:{left_out:.3f}->{right_out:.3f},metric:{left_metric:.3f}->{right_metric:.3f} "
                f"expected=held window={left_t * 1e9:.3f}-{right_t * 1e9:.3f}ns"
            )
            break

    if edge_checks >= 3 and (reset_checks == 0 or hold_checks == 0):
        edge_failures.append(
            f"insufficient_ldo_contract_coverage observed=reset:{reset_checks},hold:{hold_checks} "
            "expected=reset>=1,hold>=1 window=score_trace"
        )
    if edge_failures:
        return False, " ".join(edge_failures[:4])

    light_load = mean_in_window(rows, "out", 10.0e-9, 16.0e-9)
    heavy_load = mean_in_window(rows, "out", 28.0e-9, 40.0e-9)
    recovered = mean_in_window(rows, "out", 55.0e-9, 64.0e-9)
    heavy_metric = mean_in_window(rows, "metric", 28.0e-9, 40.0e-9)
    recovered_metric = mean_in_window(rows, "metric", 55.0e-9, 64.0e-9)
    if None in (light_load, heavy_load, recovered, heavy_metric, recovered_metric):
        return False, "ldo_missing_sample_windows"
    assert light_load is not None
    assert heavy_load is not None
    assert recovered is not None
    assert heavy_metric is not None
    assert recovered_metric is not None

    if not (0.56 <= light_load <= 0.66):
        return False, f"ldo_light_load_regulation_wrong observed={light_load:.3f} expected=0.56..0.66 window=10-16ns"
    if heavy_load >= light_load - 0.015:
        return False, f"ldo_load_step_no_droop observed=light:{light_load:.3f},heavy:{heavy_load:.3f} expected=heavy<light-0.015 window=28-40ns"
    if recovered <= heavy_load + 0.025:
        return False, f"ldo_no_recovery observed=heavy:{heavy_load:.3f},recovered:{recovered:.3f} expected=recovered>heavy+0.025 window=55-64ns"
    if recovered_metric < 0.65 or heavy_metric < 0.45:
        return False, f"ldo_metric_wrong heavy={heavy_metric:.3f} recovered={recovered_metric:.3f}"
    return True, (
        "ldo_regulator_macro_model "
        f"light/heavy/recovered={light_load:.3f}/{heavy_load:.3f}/{recovered:.3f} "
        f"edge_checks={edge_checks} reset_checks={reset_checks} hold_checks={hold_checks} "
        f"max_edge_err={max_edge_err:.4f} max_metric_err={max_metric_err:.4f}"
    )

def _sample_after(rows: list[dict[str, float]], t: float, delay: float = 5e-9) -> dict[str, float]:
    target = t + delay
    return min(rows, key=lambda row: abs(row["time"] - target))

CHECKER_ID = "v4_030_ldo_regulator_macro_model"
CHECKER: Checker = check_ldo_regulator_macro_model
