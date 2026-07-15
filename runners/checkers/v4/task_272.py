"""Task-specific checker for canonical v4 DUT 272."""
from __future__ import annotations

from ..api import Checker
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

def _v3_values_at(
    rows: list[dict[str, float]],
    names: tuple[str, ...],
    time_s: float,
) -> dict[str, float] | None:
    values = {name: sample_signal_at(rows, name, time_s) for name in names}
    if any(value is None for value in values.values()):
        return None
    return {name: float(value) for name, value in values.items() if value is not None}

def check_v3_376_reset_release_sequencer(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "supply_ok", "bias_ok", "stage1", "stage2", "ready", "progress"}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing)
    times = [row["time"] for row in rows]
    clk_edges = _threshold_crossings([row["clk"] for row in rows], times, threshold=0.45, direction="rising")
    if len(clk_edges) < 8:
        return False, f"too_few_reset_release_edges={len(clk_edges)}"
    min_period = min((b - a for a, b in zip(clk_edges, clk_edges[1:])), default=1.0e-9)
    output_delay = min(0.42e-9, 0.42 * min_period)
    stage_q = 0
    checked = 0
    max_err = 0.0
    clear_errors = output_errors = 0
    saw_reset = saw_supply_fault = saw_bias_fault = saw_stage1_only = saw_stage2 = saw_ready = saw_clear = False
    for edge_t in clk_edges:
        output_t = edge_t + output_delay
        if output_t >= times[-1] - 0.05e-9:
            continue
        inputs = _v3_values_at(rows, ("rst", "supply_ok", "bias_ok"), edge_t + 1.0e-12)
        outputs = _v3_values_at(rows, ("stage1", "stage2", "ready", "progress"), output_t)
        if inputs is None or outputs is None:
            continue
        prior_stage = stage_q
        if inputs["rst"] > 0.45 or inputs["supply_ok"] <= 0.45 or inputs["bias_ok"] <= 0.45:
            stage_q = 0
            saw_reset = saw_reset or inputs["rst"] > 0.45
            saw_supply_fault = saw_supply_fault or inputs["supply_ok"] <= 0.45
            saw_bias_fault = saw_bias_fault or inputs["bias_ok"] <= 0.45
            saw_clear = saw_clear or prior_stage > 0
        elif stage_q < 3:
            stage_q += 1
        expected = {
            "stage1": 0.9 if stage_q >= 1 else 0.0,
            "stage2": 0.9 if stage_q >= 2 else 0.0,
            "ready": 0.9 if stage_q >= 3 else 0.0,
            "progress": 0.9 * min(1.0, max(0.0, stage_q / 3.0)),
        }
        errors = {name: abs(outputs[name] - expected[name]) for name in expected}
        max_err = max(max_err, *errors.values())
        sample_errors = sum(error > 0.10 for error in errors.values())
        output_errors += sample_errors
        if inputs["rst"] > 0.45 or inputs["supply_ok"] <= 0.45 or inputs["bias_ok"] <= 0.45:
            clear_errors += sample_errors
        saw_stage1_only = saw_stage1_only or stage_q == 1
        saw_stage2 = saw_stage2 or stage_q == 2
        saw_ready = saw_ready or stage_q >= 3
        checked += 1
    if checked < 8:
        return False, f"insufficient_reset_release_samples={checked}"
    if not (saw_reset and saw_supply_fault and saw_bias_fault and saw_stage1_only and saw_stage2 and saw_ready and saw_clear):
        return False, "insufficient_reset_release_coverage"
    ok = max_err <= 0.10
    detail = f"samples={checked} max_err={max_err:.4f}"
    if not ok:
        detail = f"reset_release_error={max_err:.4f}"
    return ok, (
        f"{detail}; P_INITIALIZE_THE_INTERNAL_STAGE_COUNT_AND mismatch_count={clear_errors}; "
        f"P_AFTER_UPDATING_THE_STAGE_COUNT_DRIVE mismatch_count={output_errors}"
    )

CHECKER_ID = "v4_272_reset_release_sequencer"
CHECKER: Checker = check_v3_376_reset_release_sequencer
