"""Stimulus-relative checker for canonical v4 DUT 017."""

from __future__ import annotations

from statistics import median

from ..api import Checker, Row
from .trace_utils import property_diagnostics, sample_signal, threshold_crossings


def check_v4_strongarm_style_latch_comparator(rows: list[Row]) -> tuple[bool, str]:
    required = {"time", "clk", "vinp", "vinn", "out_p", "out_n", "lp", "lm", "vss", "vdd"}
    missing = sorted(required - (set(rows[0]) if rows else set()))
    if missing:
        return False, "missing_columns=" + ",".join(missing)

    vdd = median(row["vdd"] for row in rows)
    vss = median(row["vss"] for row in rows)
    threshold = 0.5 * (vdd + vss)
    rises = threshold_crossings(rows, "clk", threshold=threshold, direction=1)
    falls = threshold_crossings(rows, "clk", threshold=threshold, direction=-1)

    def classify(time_s: float) -> tuple[str, bool]:
        values = {name: sample_signal(rows, name, time_s) for name in ("out_p", "out_n", "lp", "lm")}
        if any(value is None for value in values.values()):
            return "?", False
        high = vss + 0.70 * (vdd - vss)
        low = vss + 0.20 * (vdd - vss)
        p = values["out_p"] > high and values["out_n"] < low
        n = values["out_n"] > high and values["out_p"] < low
        z = values["out_p"] < low and values["out_n"] < low
        state = "P" if p else "N" if n else "Z" if z else "X"
        monitors = abs(values["lp"] - values["out_p"]) <= 0.08 and abs(values["lm"] - values["out_n"]) <= 0.08
        return state, monitors

    decision_errors = {"P": 0, "N": 0, "Z": 0}
    decisions: list[str] = []
    hold_errors = 0
    reset_errors = 0
    for rise in rises:
        fall = next((event for event in falls if event > rise), None)
        if fall is None:
            continue
        vinp = sample_signal(rows, "vinp", rise)
        vinn = sample_signal(rows, "vinn", rise)
        if vinp is None or vinn is None:
            continue
        expected = "P" if vinp - vinn > 5e-4 else "N" if vinn - vinp > 5e-4 else "Z"
        early = classify(rise + 0.28 * (fall - rise))
        late = classify(rise + 0.82 * (fall - rise))
        decisions.append(early[0])
        decision_errors[expected] += int(early[0] != expected or not early[1])
        hold_errors += int(late[0] != expected or not late[1])
        next_rise = next((event for event in rises if event > fall), rows[-1]["time"])
        if next_rise > fall:
            reset_state, monitors = classify(fall + 0.35 * (next_rise - fall))
            reset_errors += int(reset_state != "Z" or not monitors)

    initial_state, initial_monitors = classify(rows[0]["time"])
    reset_errors += int(initial_state != "Z" or not initial_monitors)
    expected_seen = {
        "P": sum(1 for rise in rises if (sample_signal(rows, "vinp", rise) or 0) - (sample_signal(rows, "vinn", rise) or 0) > 5e-4),
        "N": sum(1 for rise in rises if (sample_signal(rows, "vinn", rise) or 0) - (sample_signal(rows, "vinp", rise) or 0) > 5e-4),
        "Z": sum(1 for rise in rises if abs((sample_signal(rows, "vinp", rise) or 0) - (sample_signal(rows, "vinn", rise) or 0)) <= 5e-4),
    }
    coverage_missing = sum(int(expected_seen[state] == 0) for state in ("P", "N", "Z")) + int(len(rises) < 5)
    counts = {
        "P_INITIAL_AND_FALLING_RESET": reset_errors,
        "P_POSITIVE_DECISION": decision_errors["P"] + int(expected_seen["P"] == 0),
        "P_NEGATIVE_DECISION": decision_errors["N"] + int(expected_seen["N"] == 0),
        "P_ZERO_DIFFERENTIAL": decision_errors["Z"] + int(expected_seen["Z"] == 0),
        "P_LATCH_HOLD": hold_errors,
    }
    ok = coverage_missing == 0 and all(count == 0 for count in counts.values())
    coverage = "" if coverage_missing == 0 else f" insufficient_excitation={coverage_missing}"
    return ok, (
        f"clock_rises={len(rises)} decisions={''.join(decisions)} expected_seen={expected_seen}{coverage}; "
        f"{property_diagnostics(counts)}"
    )


CHECKER_ID = "v4_017_strongarm_style_latch_comparator"
CHECKER: Checker = check_v4_strongarm_style_latch_comparator
