"""Task-specific checker for canonical v4 DUT 235."""
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

def _signal_threshold_edges(
    rows: list[dict[str, float]],
    signal: str,
    *,
    threshold: float = 0.45,
    directions: tuple[str, ...] = ("rising", "falling"),
) -> list[float]:
    times = [row["time"] for row in rows]
    values = [row[signal] for row in rows]
    edges: list[float] = []
    for direction in directions:
        edges.extend(_threshold_crossings(values, times, threshold=threshold, direction=direction))
    return sorted(edges)

def _v3_away_from_edges(row_time: float, edge_times: list[float], margin_s: float = 80e-12) -> bool:
    return all(abs(row_time - edge_time) > margin_s for edge_time in edge_times)

def _check_v3_pfd_active_low_reset_generic(
    rows: list[dict[str, float]],
    ref_name: str,
    fb_name: str,
    upb_name: str,
    down_name: str,
    *,
    reset_delay: float,
) -> tuple[bool, str]:
    ref_edges = _signal_threshold_edges(rows, ref_name, threshold=0.45, directions=("rising",))
    fb_edges = _signal_threshold_edges(rows, fb_name, threshold=0.45, directions=("rising",))
    events = sorted([(t, "ref") for t in ref_edges] + [(t, "fb") for t in fb_edges])
    if len(ref_edges) < 1 or len(fb_edges) < 1 or len(events) < 3:
        return False, f"too_few_pfd_edges ref={len(ref_edges)} fb={len(fb_edges)}"

    up_state = 0
    down_state = 0
    pending_reset: float | None = None
    reset_times: list[float] = []
    for event_time, kind in events:
        if pending_reset is not None and pending_reset <= event_time:
            up_state = 0
            down_state = 0
            pending_reset = None
        if kind == "ref":
            up_state = 1
        else:
            down_state = 1
        if up_state and down_state:
            pending_reset = event_time + reset_delay
            reset_times.append(pending_reset)

    guard_times = [t for t, _ in events] + reset_times
    transition_guard = min(20e-12, reset_delay / 5.0)
    samples = sorted(
        {
            row["time"]
            for row in rows
            if row["time"] > rows[0]["time"] + 0.05e-9
            and _v3_away_from_edges(row["time"], guard_times, transition_guard)
        }
    )
    if len(samples) < 20:
        return False, f"too_few_pfd_samples={len(samples)}"

    up = 0
    down = 0
    reset_time: float | None = None
    idx = 0
    max_err = 0.0
    checked = 0
    up_asserted = 0
    down_asserted = 0
    reset_seen = 0
    for t in samples:
        while idx < len(events) and events[idx][0] <= t:
            _, kind = events[idx]
            if kind == "ref":
                up = 1
                if down:
                    reset_time = events[idx][0] + reset_delay
            else:
                down = 1
                if up:
                    reset_time = events[idx][0] + reset_delay
            idx += 1
        if reset_time is not None and t >= reset_time:
            up = 0
            down = 0
            reset_time = None
            reset_seen += 1
        got_upb = sample_signal_at(rows, upb_name, t)
        got_down = sample_signal_at(rows, down_name, t)
        if got_upb is None or got_down is None:
            continue
        want_upb = 0.0 if up else 0.9
        want_down = 0.9 if down else 0.0
        max_err = max(max_err, abs(got_upb - want_upb), abs(got_down - want_down))
        checked += 1
        if up:
            up_asserted += 1
        if down:
            down_asserted += 1
    if checked < 20 or up_asserted == 0 or down_asserted == 0 or reset_seen == 0:
        return False, (
            f"insufficient_pfd_state_coverage checked={checked} up={up_asserted} "
            f"down={down_asserted} resets={reset_seen}"
        )
    if max_err > 0.10:
        return False, f"pfd_level_error={max_err:.4f} checked={checked}"
    return True, (
        f"ref_edges={len(ref_edges)} fb_edges={len(fb_edges)} checked={checked} "
        f"up={up_asserted} down={down_asserted} resets={reset_seen} max_err={max_err:.4f}"
    )

def check_v3_pfd_timer_reset(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "a", "b", "ub", "d"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing pfd timer reset signals"
    return _check_v3_pfd_active_low_reset_generic(rows, "a", "b", "ub", "d", reset_delay=100e-12)

CHECKER_ID = "v4_235_pfd_timer_reset"
CHECKER: Checker = check_v3_pfd_timer_reset
