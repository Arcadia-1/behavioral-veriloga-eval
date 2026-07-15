"""Task-specific checker for canonical v4 DUT 291."""
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

def check_v3_490_event_reacquire_lock_detector(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "ref_clk", "fb_clk", "rst", "lock", "phase_metric", "state_mon"}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing)
    times = [row["time"] for row in rows]
    ref_edges = _threshold_crossings([row["ref_clk"] for row in rows], times, threshold=0.45, direction="rising")
    fb_edges = _threshold_crossings([row["fb_clk"] for row in rows], times, threshold=0.45, direction="rising")
    rst_edges = _threshold_crossings([row["rst"] for row in rows], times, threshold=0.45, direction="rising")
    if len(ref_edges) < 6 or len(fb_edges) < 6:
        return False, f"too_few_lock_detector_edges=ref{len(ref_edges)}_fb{len(fb_edges)}"
    min_gap = min((b - a for a, b in zip(sorted(ref_edges + fb_edges), sorted(ref_edges + fb_edges)[1:])), default=1.0e-9)
    output_delay = min(0.30e-9, max(0.12e-9, 0.35 * min_gap))
    events = [(t, "ref") for t in ref_edges] + [(t, "fb") for t in fb_edges] + [(t, "rst") for t in rst_edges]
    events.sort(key=lambda item: (item[0], {"rst": 0, "ref": 1, "fb": 2}[item[1]]))
    last_ref: float | None = None
    good_count = 0
    checked = 0
    max_err = 0.0
    reference_errors = consecutive_errors = reset_errors = observable_errors = 0
    saw_lock = saw_unlock = saw_reset = saw_reacquire = saw_phase_high = saw_phase_low = saw_fail_clear = False
    lock_seen_before_reset = False
    for event_t, kind in events:
        if kind == "ref":
            last_ref = event_t
            continue
        output_t = event_t + output_delay
        if output_t >= times[-1] - 0.05e-9:
            continue
        if kind == "rst":
            good_count = 0
            expected = {"lock": 0.0, "phase_metric": 0.0, "state_mon": 0.0}
            saw_reset = True
        else:
            rst_now = sample_signal_at(rows, "rst", event_t + 1.0e-12)
            if rst_now is not None and rst_now > 0.45:
                good_count = 0
                expected = {"lock": 0.0, "phase_metric": 0.0, "state_mon": 0.0}
                saw_reset = True
            else:
                phase_err = abs(event_t - last_ref) if last_ref is not None else 0.60e-9
                prior_good = good_count
                if last_ref is not None and phase_err <= 0.18e-9:
                    good_count = min(good_count + 1, 3)
                else:
                    good_count = 0
                expected = {
                    "lock": 0.9 if good_count >= 3 else 0.0,
                    "phase_metric": 0.9 * min(1.0, max(0.0, phase_err / 0.60e-9)),
                    "state_mon": 0.9 * min(1.0, max(0.0, good_count / 3.0)),
                }
                saw_phase_high = saw_phase_high or expected["phase_metric"] > 0.55
                saw_phase_low = saw_phase_low or expected["phase_metric"] < 0.25
                saw_fail_clear = saw_fail_clear or (prior_good > 0 and good_count == 0)
        outputs = _v3_values_at(rows, ("lock", "phase_metric", "state_mon"), output_t)
        if outputs is None:
            continue
        errors = {name: abs(outputs[name] - expected[name]) for name in expected}
        max_err = max(max_err, *errors.values())
        lock_error = int(errors["lock"] > 0.10)
        phase_error = int(errors["phase_metric"] > 0.10)
        state_error = int(errors["state_mon"] > 0.10)
        rst_sampled = sample_signal_at(rows, "rst", event_t + 1.0e-12)
        reset_sample = kind == "rst" or (
            kind == "fb" and rst_sampled is not None and rst_sampled > 0.45
        )
        if reset_sample:
            reset_errors += lock_error + phase_error + state_error
        else:
            reference_errors += phase_error
            consecutive_errors += lock_error + state_error
            observable_errors += phase_error + state_error
        saw_lock = saw_lock or expected["lock"] > 0.45
        saw_unlock = saw_unlock or expected["lock"] < 0.45
        if expected["lock"] > 0.45:
            if saw_reset:
                saw_reacquire = True
            else:
                lock_seen_before_reset = True
        saw_reacquire = saw_reacquire or (saw_reset and expected["lock"] > 0.45)
        checked += 1
    if checked < 6:
        return False, f"insufficient_lock_detector_samples={checked}"
    if not (saw_lock and saw_unlock and saw_reset and lock_seen_before_reset and saw_reacquire and saw_phase_high and saw_phase_low and saw_fail_clear):
        return False, "insufficient_lock_detector_coverage"
    ok = max_err <= 0.10
    detail = f"samples={checked} max_err={max_err:.4f}"
    if not ok:
        detail = f"event_reacquire_lock_error={max_err:.4f}"
    return ok, (
        f"{detail}; P_RECORD_REFERENCE_CLOCK_RISING_EDGE_TIME mismatch_count={reference_errors}; "
        f"P_REQUIRE_CONSECUTIVE_IN_WINDOW_FEEDBACK_EDGE mismatch_count={consecutive_errors}; "
        f"P_CLEAR_LOCK_STATE_AND_PROGRESS_WHEN mismatch_count={reset_errors}; "
        f"P_EXPOSE_PHASE_METRIC_AND_STATE_MON mismatch_count={observable_errors}"
    )

CHECKER_ID = "v4_291_event_reacquire_lock_detector"
CHECKER: Checker = check_v3_490_event_reacquire_lock_detector
