"""Task-specific checker for canonical v4 DUT 017."""
from __future__ import annotations

from checkers.api import Checker
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

def check_v4_strongarm_style_latch_comparator(
    rows: list[dict[str, float]],
) -> tuple[bool, str]:
    required = {"time", "clk", "vinp", "vinn", "out_p", "out_n", "lp", "lm", "vdd"}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0] if rows else {}))
        return False, f"missing_strongarm_signals={','.join(missing)}"

    stop_time = rows[-1]["time"]
    feedback_profile = stop_time >= 4.5e-9
    decision_times_ns = [0.60, 1.60, 2.60, 3.60] + ([4.60] if feedback_profile else [])
    expected = ["P", "N", "P", "N"] + (["Z"] if feedback_profile else [])
    reset_times_ns = [0.20, 1.20, 2.20, 3.20] + ([4.20] if feedback_profile else [])
    hold_times_ns = [0.84, 1.84, 2.84, 3.84] if not feedback_profile else [0.82, 1.82, 3.82, 4.82]

    def classify(t_ns: float) -> tuple[str, bool]:
        values = {
            name: sample_signal_at(rows, name, t_ns * 1e-9)
            for name in ("out_p", "out_n", "lp", "lm", "vdd")
        }
        if any(value is None for value in values.values()):
            return "?", False
        high = 0.70 * values["vdd"]
        low = 0.20 * values["vdd"]
        p = values["out_p"] > high and values["out_n"] < low
        n = values["out_n"] > high and values["out_p"] < low
        z = values["out_p"] < low and values["out_n"] < low
        state = "P" if p else "N" if n else "Z" if z else "X"
        monitors_match = (
            abs(values["lp"] - values["out_p"]) <= 0.08
            and abs(values["lm"] - values["out_n"]) <= 0.08
        )
        return state, monitors_match

    decisions = [classify(t_ns) for t_ns in decision_times_ns]
    resets = [classify(t_ns) for t_ns in reset_times_ns]
    holds = [classify(t_ns) for t_ns in hold_times_ns]
    hold_expected = ["P", "N", "N", "Z"] if feedback_profile else expected
    decision_states = [state for state, _ in decisions]
    reset_states = [state for state, _ in resets]
    hold_states = [state for state, _ in holds]

    decision_mismatches = {"P": 0, "N": 0, "Z": 0}
    for (state, monitor_matches), expected_state in zip(decisions, expected):
        if state != expected_state or not monitor_matches:
            decision_mismatches[expected_state] += 1
    reset_mismatches = sum(
        state != "Z" or not monitor_matches for state, monitor_matches in resets
    )
    hold_mismatches = sum(
        state != expected_state or not monitor_matches
        for (state, monitor_matches), expected_state in zip(holds, hold_expected)
    )
    counts = {
        "P_INITIAL_AND_FALLING_RESET": reset_mismatches,
        "P_POSITIVE_DECISION": decision_mismatches["P"],
        "P_NEGATIVE_DECISION": decision_mismatches["N"],
        "P_ZERO_DIFFERENTIAL": decision_mismatches["Z"],
        "P_LATCH_HOLD": hold_mismatches,
    }
    ok = all(count == 0 for count in counts.values())
    return ok, (
        f"decision_states={''.join(decision_states)} expected={''.join(expected)} "
        f"reset_states={''.join(reset_states)} hold_states={''.join(hold_states)}; "
        + "; ".join(
            f"{property_id} mismatch_count={count}"
            for property_id, count in counts.items()
        )
    )

CHECKER_ID = "v4_017_strongarm_style_latch_comparator"
CHECKER: Checker = check_v4_strongarm_style_latch_comparator
