"""Task-specific checker for canonical v4 DUT 220."""
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

def _max_signal_value(
    rows: list[dict[str, float]],
    signals: list[str],
    *,
    default: float,
) -> float:
    values: list[float] = []
    for row in rows:
        for signal in signals:
            value = row.get(signal)
            if value is not None:
                values.append(value)
    return max(values) if values else default

def _v3_away_from_edges(row_time: float, edge_times: list[float], margin_s: float = 80e-12) -> bool:
    return all(abs(row_time - edge_time) > margin_s for edge_time in edge_times)

def check_v3_pfd_up_down_state(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "ref", "fb", "up", "down"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing pfd up down state signals"
    vdd = _max_signal_value(rows, ["ref", "fb", "up", "down"], default=1.2)
    if vdd < 0.6:
        vdd = 1.2
    threshold = 0.5 * vdd
    state_update_times: list[float] = []
    for signal in ("ref", "fb"):
        # Only rising crossings update the specified detector state.  Input
        # falling edges do not move the state or start an output transition,
        # so guarding around them can erase a valid short-lived state.
        state_update_times.extend(
            _signal_threshold_edges(rows, signal, threshold=threshold, directions=("rising",))
        )

    state = 0
    checked = 0
    saw_up = False
    saw_down = False
    saw_zero = False
    max_err = 0.0
    failures: list[str] = []
    up_errors = down_errors = zero_errors = 0
    ref_response_errors = fb_response_errors = 0
    prev = rows[0]
    for row in rows[1:]:
        if prev["ref"] <= threshold < row["ref"]:
            state = min(1, state + 1)
        if prev["fb"] <= threshold < row["fb"]:
            state = max(-1, state - 1)
        prev = row
        if row["time"] < 0.05e-9 or not _v3_away_from_edges(
            row["time"], state_update_times, margin_s=90e-12
        ):
            continue
        exp_up = vdd if state == 1 else 0.0
        exp_down = vdd if state == -1 else 0.0
        saw_up = saw_up or state == 1
        saw_down = saw_down or state == -1
        saw_zero = saw_zero or state == 0
        err_up = abs(row["up"] - exp_up)
        err_down = abs(row["down"] - exp_down)
        max_err = max(max_err, err_up, err_down)
        checked += 1
        if err_up > 0.10 or err_down > 0.10:
            failures.append(
                f"t={row['time'] * 1e9:.3f}ns up/down={row['up']:.3f}/{row['down']:.3f} "
                f"expected={exp_up:.3f}/{exp_down:.3f}"
            )
            up_errors += int(err_up > 0.10)
            down_errors += int(err_down > 0.10)
            zero_errors += int(state == 0)
            ref_response_errors += int(state == 1)
            fb_response_errors += int(state == -1)
    coverage_errors = int(checked < 20) + int(not saw_up) + int(not saw_down) + int(not saw_zero)
    total_output_errors = up_errors + down_errors
    ok = coverage_errors == 0 and not failures
    detail = " ".join(failures[:6]) or "state_outputs_match"
    return ok, (
        f"{detail} checked={checked} up={saw_up} down={saw_down} zero={saw_zero} "
        f"up_errors={up_errors} down_errors={down_errors} zero_errors={zero_errors} max_err={max_err:.3f} "
        f"coverage_errors={coverage_errors}; "
        f"P_DETECT_RISING_REF_AND_FB_CROSSINGS mismatch_count={total_output_errors}; "
        f"P_MAINTAIN_AN_INTEGER_DETECTOR_STATE_BOUNDED mismatch_count={zero_errors}; "
        f"P_A_RISING_REF_EDGE_INCREMENTS_THE mismatch_count={ref_response_errors}; "
        f"P_A_RISING_FB_EDGE_DECREMENTS_THE mismatch_count={fb_response_errors}; "
        f"P_DRIVE_UP_HIGH_WHEN_THE_STATE mismatch_count={up_errors}; "
        f"P_DRIVE_DOWN_HIGH_WHEN_THE_STATE mismatch_count={down_errors}"
    )

CHECKER_ID = "v4_220_pfd_up_down_state"
CHECKER: Checker = check_v3_pfd_up_down_state
