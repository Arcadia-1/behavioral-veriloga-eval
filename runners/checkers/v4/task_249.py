"""Task-specific checker for canonical v4 DUT 249."""
from __future__ import annotations

from checkers.api import Checker
import math

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

def _external_reset_pfd_state_changes(
    rows: list[dict[str, float]],
    *,
    reset_delay: float,
    threshold: float = 0.45,
) -> tuple[list[tuple[float, int, int, str]], list[float], int]:
    ref_edges = _signal_threshold_edges(rows, "ref", threshold=threshold, directions=("rising",))
    fb_edges = _signal_threshold_edges(rows, "fb", threshold=threshold, directions=("rising",))
    rstb_falls = _signal_threshold_edges(rows, "rstb", threshold=threshold, directions=("falling",))
    events = sorted(
        [(t, "ref") for t in ref_edges]
        + [(t, "fb") for t in fb_edges]
        + [(t, "rstb_fall") for t in rstb_falls]
    )
    up = 0
    down = 0
    timer_time: float | None = None
    timer_times: list[float] = []
    state_changes: list[tuple[float, int, int, str]] = [(rows[0]["time"], up, down, "initial")]
    external_reset_clears = 0
    idx = 0
    while idx < len(events) or timer_time is not None:
        event_time = events[idx][0] if idx < len(events) else math.inf
        next_timer = timer_time if timer_time is not None else math.inf
        if next_timer <= event_time:
            up = 0
            down = 0
            state_changes.append((next_timer, up, down, "timer_reset"))
            timer_times.append(next_timer)
            timer_time = None
            continue
        t, kind = events[idx]
        idx += 1
        rstb_value = sample_signal_at(rows, "rstb", t)
        rstb_high = rstb_value is not None and rstb_value > threshold
        if kind == "rstb_fall":
            if up or down:
                external_reset_clears += 1
            up = 0
            down = 0
            timer_time = None
            state_changes.append((t, up, down, "external_reset"))
            continue
        if not rstb_high:
            state_changes.append((t, up, down, f"{kind}_ignored_reset_low"))
            continue
        if kind == "ref":
            up = 1
            if down:
                timer_time = t + reset_delay
        elif kind == "fb":
            down = 1
            if up:
                timer_time = t + reset_delay
        state_changes.append((t, up, down, kind))
    return state_changes, sorted(timer_times), external_reset_clears

def check_v3_pfd_active_low_reset(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "ref", "fb", "rstb", "up", "down"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing pfd active-low reset signals"
    ref_edges = _signal_threshold_edges(rows, "ref", threshold=0.45, directions=("rising",))
    fb_edges = _signal_threshold_edges(rows, "fb", threshold=0.45, directions=("rising",))
    rstb_edges = _signal_threshold_edges(rows, "rstb", threshold=0.45, directions=("rising", "falling"))
    if len(ref_edges) < 2 or len(fb_edges) < 2 or len(rstb_edges) < 2:
        return False, f"too_few_pfd_reset_edges ref={len(ref_edges)} fb={len(fb_edges)} rstb={len(rstb_edges)}"
    state_changes, timer_times, external_reset_clears = _external_reset_pfd_state_changes(
        rows,
        reset_delay=80e-12,
    )
    guard_times = sorted(ref_edges + fb_edges + rstb_edges + timer_times)
    if not timer_times:
        return False, "no_delayed_timer_reset_seen"
    max_err = 0.0
    checked = 0
    up_rows = down_rows = both_rows = reset_low_rows = idle_rows = 0
    change_idx = 0
    up_state = 0
    down_state = 0
    for row in rows:
        t = row["time"]
        while change_idx + 1 < len(state_changes) and state_changes[change_idx + 1][0] <= t:
            change_idx += 1
            _, up_state, down_state, _ = state_changes[change_idx]
        if t < rows[0]["time"] + 0.05e-9:
            continue
        if not _v3_away_from_edges(t, guard_times, 35e-12):
            continue
        rstb_high = row["rstb"] > 0.45
        expected_up = 0.9 if (rstb_high and up_state) else 0.0
        expected_down = 0.9 if (rstb_high and down_state) else 0.0
        max_err = max(max_err, abs(row["up"] - expected_up), abs(row["down"] - expected_down))
        checked += 1
        if not rstb_high:
            reset_low_rows += 1
        elif up_state and down_state:
            both_rows += 1
        elif up_state:
            up_rows += 1
        elif down_state:
            down_rows += 1
        else:
            idle_rows += 1
    if (
        checked < 30
        or up_rows == 0
        or down_rows == 0
        or both_rows == 0
        or reset_low_rows == 0
        or idle_rows == 0
        or external_reset_clears == 0
    ):
        return False, (
            f"insufficient_pfd_external_reset_coverage checked={checked} up={up_rows} "
            f"down={down_rows} both={both_rows} reset_low={reset_low_rows} idle={idle_rows} "
            f"external_reset_clears={external_reset_clears}"
        )
    if max_err > 0.12:
        return False, f"pfd_external_reset_level_error={max_err:.4f} checked={checked}"
    return True, (
        f"ref_edges={len(ref_edges)} fb_edges={len(fb_edges)} timer_resets={len(timer_times)} "
        f"external_reset_clears={external_reset_clears} checked={checked} max_err={max_err:.4f}"
    )

CHECKER_ID = "v4_249_pfd_active_low_reset"
CHECKER: Checker = check_v3_pfd_active_low_reset
