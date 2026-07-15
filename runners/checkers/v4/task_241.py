"""Task-specific checker for canonical v4 DUT 241."""
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

def check_v3_hysteretic_comparator_receiver(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "inp", "inm", "out"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing hysteretic comparator receiver signals"

    times = [row["time"] for row in rows]
    diff = [row["inp"] - row["inm"] for row in rows]
    out = [row["out"] for row in rows]

    vout_high = 0.9
    vout_low = 0.0
    upper_th = 20e-3
    lower_th = -20e-3
    td = 400e-12
    tr = 80e-12
    out_mid = 0.5 * (vout_high + vout_low)

    high_events = _threshold_crossings(diff, times, threshold=upper_th, direction="rising")
    low_events = _threshold_crossings(diff, times, threshold=lower_th, direction="falling")
    if len(high_events) < 2 or len(low_events) < 2:
        return False, f"insufficient_hysteresis_events high={len(high_events)} low={len(low_events)}"

    expected_edges: list[tuple[float, int]] = []
    state = 1 if diff[0] >= upper_th else 0
    for event_time, next_state in sorted([(t, 1) for t in high_events] + [(t, 0) for t in low_events]):
        if next_state == state:
            continue
        expected_edges.append((event_time, next_state))
        state = next_state

    if len(expected_edges) < 4:
        return False, f"insufficient_expected_state_edges={len(expected_edges)}"

    out_rises = _threshold_crossings(out, times, threshold=out_mid, direction="rising")
    out_falls = _threshold_crossings(out, times, threshold=out_mid, direction="falling")
    expected_rises = [t + td + 0.5 * tr for t, next_state in expected_edges if next_state == 1]
    expected_falls = [t + td + 0.5 * tr for t, next_state in expected_edges if next_state == 0]

    edge_tol = 180e-12

    def compare_edges(actual: list[float], expected: list[float], label: str) -> tuple[bool, str, float]:
        if len(actual) < len(expected):
            return False, f"missing_{label}_edges actual={len(actual)} expected={len(expected)}", 0.0
        used: set[int] = set()
        max_err = 0.0
        for want in expected:
            choices = [(abs(got - want), idx, got) for idx, got in enumerate(actual) if idx not in used]
            if not choices:
                return False, f"missing_unmatched_{label}_edge_at={want * 1e9:.3f}ns", max_err
            err, idx, got = min(choices)
            if err > edge_tol:
                return (
                    False,
                    f"{label}_edge_delay_error got={got * 1e9:.3f}ns "
                    f"want={want * 1e9:.3f}ns err={err * 1e12:.1f}ps",
                    max(max_err, err),
                )
            used.add(idx)
            max_err = max(max_err, err)
        return True, "ok", max_err

    ok, msg, rise_err = compare_edges(out_rises, expected_rises, "rising")
    if not ok:
        return False, msg
    ok, msg, fall_err = compare_edges(out_falls, expected_falls, "falling")
    if not ok:
        return False, msg

    expected_centers = expected_rises + expected_falls
    for actual_edge in out_rises + out_falls:
        if min(abs(actual_edge - want) for want in expected_centers) > edge_tol:
            return False, f"unexpected_output_edge_at={actual_edge * 1e9:.3f}ns"

    max_level_err = 0.0
    checked = 0
    high_checked = 0
    low_checked = 0
    for row in rows:
        t = row["time"]
        in_transition = any((edge_t + td - 20e-12) <= t <= (edge_t + td + tr + 80e-12) for edge_t, _ in expected_edges)
        if in_transition:
            continue
        expected_state = 1 if diff[0] >= upper_th else 0
        for edge_t, next_state in expected_edges:
            if t >= edge_t + td + tr + 80e-12:
                expected_state = next_state
        want = vout_high if expected_state else vout_low
        err = abs(row["out"] - want)
        max_level_err = max(max_level_err, err)
        checked += 1
        if expected_state:
            high_checked += 1
        else:
            low_checked += 1

    if checked < 20 or high_checked == 0 or low_checked == 0:
        return False, f"insufficient_settled_samples checked={checked} high={high_checked} low={low_checked}"
    if max_level_err > 0.08:
        return False, f"level_error={max_level_err:.4f} checked={checked}"

    return (
        True,
        f"edges={len(expected_edges)} rise_err_ps={rise_err * 1e12:.1f} "
        f"fall_err_ps={fall_err * 1e12:.1f} level_err={max_level_err:.4f}",
    )

CHECKER_ID = "v4_241_hysteretic_comparator_receiver"
CHECKER: Checker = check_v3_hysteretic_comparator_receiver
