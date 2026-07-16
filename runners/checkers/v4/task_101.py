"""Task-specific checker for canonical v4 DUT 101."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import structured_result


def sample_signal(rows: list[dict[str, float]], signal: str, time_s: float) -> float | None:
    if not rows or signal not in rows[0] or "time" not in rows[0]:
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
    return rows[-1].get(signal)

def _crossing_times(
    rows: list[dict[str, float]],
    signal: str,
    *,
    threshold: float = 0.45,
    direction: str = "rising",
) -> list[float]:
    if not rows or "time" not in rows[0] or signal not in rows[0]:
        return []
    crossings: list[float] = []
    for idx in range(1, len(rows)):
        prev = rows[idx - 1]
        cur = rows[idx]
        t0 = prev.get("time")
        t1 = cur.get("time")
        v0 = prev.get(signal)
        v1 = cur.get(signal)
        if t0 is None or t1 is None or v0 is None or v1 is None:
            continue
        if direction == "rising":
            hit = v0 <= threshold < v1
        elif direction == "falling":
            hit = v0 >= threshold > v1
        else:
            raise ValueError(f"unsupported direction={direction!r}")
        if not hit:
            continue
        if v1 == v0:
            crossings.append(t1)
        else:
            alpha = (threshold - v0) / (v1 - v0)
            crossings.append(t0 + alpha * (t1 - t0))
    return crossings

def check_settling_time_measurement_tb(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "step", "vout", "done"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/step/vout/done"

    times = [row["time"] for row in rows]
    step_final = rows[-1]["step"]
    step_threshold = max(0.05, 0.5 * step_final)
    step_edges = _crossing_times(rows, "step", threshold=step_threshold, direction="rising")
    done_edges = _crossing_times(rows, "done", threshold=0.45, direction="rising")
    if not step_edges:
        return False, "missing_step_rising_edge"
    if not done_edges:
        return False, "missing_done_rising_edge"

    step_t = step_edges[0]
    done_t = done_edges[0]
    if done_t <= step_t + 50e-9:
        return False, f"done_too_early step={step_t:.3e} done={done_t:.3e}"

    sample_times = [
        step_t + 0.18 * (done_t - step_t),
        step_t + 0.50 * (done_t - step_t),
        done_t - 1.0e-9,
        done_t + 1.5e-9,
        min(times[-1] - 1.0e-9, done_t + 30.0e-9),
    ]
    values: list[float] = []
    done_values: list[float] = []
    for time_s in sample_times:
        vout = sample_signal(rows, "vout", time_s)
        done = sample_signal(rows, "done", time_s)
        if vout is None or done is None:
            return False, f"missing_sample_at={time_s:.3e}"
        values.append(vout)
        done_values.append(done)

    monotone = values[0] < values[1] < values[2] <= values[3] + 0.02 <= values[4] + 0.02
    boundary_ok = done_values[2] < 0.1 and done_values[3] > 0.8 and done_values[4] > 0.8
    late_settled = values[4] > 0.75 and abs(values[4] - step_final) <= max(0.12, 0.18 * max(abs(step_final), 1e-9))
    ok = monotone and boundary_ok and late_settled
    value_text = ",".join(f"{value:.3f}" for value in values)
    done_text = ",".join(f"{value:.3f}" for value in done_values)
    return ok, (
        f"vout_samples={value_text} done_samples={done_text} "
        f"step_t={step_t:.3e} done_t={done_t:.3e} "
        f"monotone={monotone} boundary_ok={boundary_ok} late_settled={late_settled}"
    )

CHECKER_ID = "v4_101_settling_time_measurement"
PROPERTY_IDS = (
    "P_INITIAL_ZERO_STATE",
    "P_FIRST_ORDER_UPDATE",
    "P_RESPONSE_CONVERGENCE",
    "P_DONE_TIME_GATE",
    "P_DONE_SETTLED_GATE",
)
CHECKER: Checker = structured_result(check_settling_time_measurement_tb, PROPERTY_IDS)
