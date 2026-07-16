"""Stimulus-relative checker for canonical v4 DUT 011."""

from __future__ import annotations

from statistics import median

from ..api import Checker, Row
from .trace_utils import median_step, property_diagnostics, sample_signal, threshold_crossings


def check_v4_pfd_updn_logic(rows: list[Row]) -> tuple[bool, str]:
    required = {"time", "vdd", "vss", "ref", "div", "up", "dn"}
    missing = sorted(required - (set(rows[0]) if rows else set()))
    if missing:
        return False, "missing_columns=" + ",".join(missing)

    vdd = median(row["vdd"] for row in rows[len(rows) // 10 :])
    vss = median(row["vss"] for row in rows[len(rows) // 10 :])
    span = vdd - vss
    threshold = vss + 0.5 * span
    events: list[tuple[float, str]] = []
    for signal in ("ref", "div"):
        events.extend((time_s, signal + "+") for time_s in threshold_crossings(rows, signal, threshold=threshold, direction=1))
        events.extend((time_s, signal + "-") for time_s in threshold_crossings(rows, signal, threshold=threshold, direction=-1))
    events.sort()

    dt = max(median_step(rows), 1e-12)
    up_state = dn_state = 0
    ref_sets = div_sets = ref_clears = div_clears = 0
    ref_errors = div_errors = clear_errors = rail_errors = overlap_errors = 0
    checked = 0
    for index, (event_time, event) in enumerate(events):
        if event == "ref+":
            if dn_state:
                ref_clears += 1
                up_state = dn_state = 0
            else:
                ref_sets += 1
                up_state = 1
        elif event == "div+":
            if up_state:
                div_clears += 1
                up_state = dn_state = 0
            else:
                div_sets += 1
                dn_state = 1

        next_time = events[index + 1][0] if index + 1 < len(events) else rows[-1]["time"]
        gap = max(0.0, next_time - event_time)
        settle = min(max(4.0 * dt, 40e-12), 0.35 * gap) if gap > 0 else 0.0
        if settle <= 0.0:
            continue
        up = sample_signal(rows, "up", event_time + settle)
        dn = sample_signal(rows, "dn", event_time + settle)
        if up is None or dn is None:
            continue
        checked += 1
        expected_up = vdd if up_state else vss
        expected_dn = vdd if dn_state else vss
        up_bad = abs(up - expected_up) > 0.08 * max(span, 1e-9)
        dn_bad = abs(dn - expected_dn) > 0.08 * max(span, 1e-9)
        rail_errors += up_bad + dn_bad
        if event.startswith("ref"):
            ref_errors += up_bad or dn_bad
        else:
            div_errors += up_bad or dn_bad
        if event.endswith("+") and not up_state and not dn_state:
            clear_errors += up_bad or dn_bad
        overlap_errors += up > threshold and dn > threshold

    coverage_missing = (
        int(ref_sets < 2)
        + int(div_sets < 2)
        + int(ref_clears < 2)
        + int(div_clears < 2)
        + int(span < 0.4)
    )
    counts = {
        "P_REF_SETS_UP": ref_errors + int(ref_sets < 2),
        "P_DIV_SETS_DN": div_errors + int(div_sets < 2),
        "P_RESET_RACE_CLEAR": clear_errors + int(ref_clears < 2) + int(div_clears < 2),
        "P_NO_PERSISTENT_OVERLAP": overlap_errors,
        "P_RAIL_REFERENCE": rail_errors + int(span < 0.4),
    }
    ok = checked >= 12 and coverage_missing == 0 and all(count == 0 for count in counts.values())
    coverage = "" if coverage_missing == 0 else f" insufficient_excitation={coverage_missing}"
    return ok, (
        f"checked={checked} ref_sets={ref_sets} div_sets={div_sets} "
        f"ref_clears={ref_clears} div_clears={div_clears} rails={vss:.3f}/{vdd:.3f}{coverage}; "
        f"{property_diagnostics(counts)}"
    )


CHECKER_ID = "v4_011_pfd_up_dn_logic"
CHECKER: Checker = check_v4_pfd_updn_logic
