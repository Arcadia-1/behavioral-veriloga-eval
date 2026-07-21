"""Task-specific checker for canonical v4 DUT 186."""
from __future__ import annotations

from ..api import Checker


def sample_signal_at(rows: list[dict[str, float]], signal: str, time_s: float) -> float | None:
    if not rows or "time" not in rows[0] or signal not in rows[0]:
        return None
    first_time = rows[0]["time"]
    last_time = rows[-1].get("time")
    if last_time is None or time_s > last_time:
        return None
    if time_s <= first_time:
        # Affine normalization can move a valid candidate's pre-roll start
        # past a canonical baseline probe. The first row is the stable
        # pre-event state; event and post-event probes still interpolate.
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

def _crossings(
    rows: list[dict[str, float]],
    signals: tuple[str, ...],
    direction: int,
    threshold: float = 0.5,
) -> list[float]:
    events: list[float] = []
    previous = sum(float(rows[0][signal]) for signal in signals)
    previous_time = float(rows[0]["time"])
    for row in rows[1:]:
        now = sum(float(row[signal]) for signal in signals)
        now_time = float(row["time"])
        crossed = previous <= threshold < now if direction > 0 else previous >= threshold > now
        if crossed and now_time > previous_time and now != previous:
            fraction = (threshold - previous) / (now - previous)
            events.append(previous_time + fraction * (now_time - previous_time))
        previous = now
        previous_time = now_time
    return events


def _logic(rows: list[dict[str, float]], signal: str, time_s: float) -> int:
    value = sample_signal_at(rows, signal, time_s)
    return int(value is not None and value > 0.5)


def _mismatches(
    rows: list[dict[str, float]],
    time_s: float,
    expected: dict[str, int],
    *,
    tolerance: float = 0.15,
) -> int:
    count = 0
    for signal, bit in expected.items():
        value = sample_signal_at(rows, signal, time_s)
        if value is None or abs(value - float(bit)) > tolerance:
            count += 1
    return count

def check_v3_sarfend_logic_4b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {
        "time",
        "clks",
        "clkc",
        "dp1",
        "dp2",
        "dp3",
        "dp4",
        "dm1",
        "dm2",
        "dm3",
        "dm4",
        "dout0",
        "dout1",
        "dout2",
        "dout3",
        "dcomp",
        "dcompb",
        "test",
        "dtest0",
        "dtest1",
        "dtest2",
        "dtest3",
    }
    if not rows or not required.issubset(rows[0]):
        return False, "missing sarfend logic outputs"

    clks_rises = _crossings(rows, ("clks",), +1)
    clks_falls = _crossings(rows, ("clks",), -1)
    comparator_rises = _crossings(rows, ("dcomp", "dcompb"), +1)
    comparator_falls = _crossings(rows, ("dcomp", "dcompb"), -1)
    if len(clks_rises) < 3:
        return False, "insufficient_excitation clks_rises<3"

    p = [0, 1, 1, 1]
    m = [0, 1, 1, 1]
    pointer = 0
    captured_dtest = [0, 0, 0, 0]
    reset_errors = decision_errors = dout_errors = clock_errors = 0
    normal_decision_errors = test_decision_errors = 0
    rise_clock_errors = fall_clock_errors = comparator_clock_errors = 0
    normal_decisions = test_decisions = published_words = 0
    completed_conversions = stop_checks = 0
    post_completion_hold_checks = post_completion_hold_errors = 0
    events = (
        [(time_s, "clks_rise") for time_s in clks_rises]
        + [(time_s, "clks_fall") for time_s in clks_falls]
        + [(time_s, "comp_rise") for time_s in comparator_rises]
        + [(time_s, "comp_fall") for time_s in comparator_falls]
    )
    event_priority = {"clks_rise": 0, "clks_fall": 1, "comp_fall": 2, "comp_rise": 3}
    ordered_events = sorted(events, key=lambda item: (item[0], event_priority[item[1]]))
    for event_index, (time_s, event) in enumerate(ordered_events):
        next_time = (
            ordered_events[event_index + 1][0]
            if event_index + 1 < len(ordered_events)
            else float(rows[-1]["time"])
        )
        settle_delay = max(80e-12, min(5e-9, 0.25 * max(0.0, next_time - time_s)))
        probe_time = time_s + settle_delay
        if event == "clks_rise":
            if pointer >= 4:
                completed_conversions += 1
            dout_expected = {
                "dout3": p[0],
                "dout2": p[1],
                "dout1": p[2],
                "dout0": p[3],
            }
            dout_errors += _mismatches(rows, probe_time, dout_expected)
            published_words += 1
            p = [0, 1, 1, 1]
            m = [0, 1, 1, 1]
            pointer = 0
            captured_dtest = [
                _logic(rows, "dtest3", time_s),
                _logic(rows, "dtest2", time_s),
                _logic(rows, "dtest1", time_s),
                _logic(rows, "dtest0", time_s),
            ]
            reset_errors += _mismatches(
                rows,
                probe_time,
                {
                    "dp4": 0,
                    "dm4": 0,
                    "dp3": 1,
                    "dm3": 1,
                    "dp2": 1,
                    "dm2": 1,
                    "dp1": 1,
                    "dm1": 1,
                },
            )
            error_count = _mismatches(rows, probe_time, {"clkc": 0})
            rise_clock_errors += error_count
            clock_errors += error_count
        elif event == "clks_fall":
            error_count = _mismatches(rows, probe_time, {"clkc": 1})
            fall_clock_errors += error_count
            clock_errors += error_count
        elif event == "comp_fall":
            if _logic(rows, "clks", time_s) == 0:
                expected_clkc = 1 if pointer < 4 else 0
                error_count = _mismatches(rows, probe_time, {"clkc": expected_clkc})
                comparator_clock_errors += error_count
                clock_errors += error_count
                if pointer >= 4:
                    stop_checks += 1
                    hold_expected = {
                        "dp4": p[0], "dm4": m[0],
                        "dp3": p[1], "dm3": m[1],
                        "dp2": p[2], "dm2": m[2],
                        "dp1": p[3], "dm1": m[3],
                    }
                    error_count = _mismatches(rows, probe_time, hold_expected)
                    post_completion_hold_errors += error_count
                    post_completion_hold_checks += 1
        elif _logic(rows, "clks", time_s) == 0 and pointer < 4:
            test_mode = _logic(rows, "test", time_s) == 1
            if test_mode:
                decision = captured_dtest[pointer]
                test_decisions += 1
            else:
                decision = int(
                    (sample_signal_at(rows, "dcomp", time_s) or 0.0)
                    > (sample_signal_at(rows, "dcompb", time_s) or 0.0)
                )
                normal_decisions += 1
            p[pointer] = decision
            m[pointer] = 1 - decision
            output_index = 4 - pointer
            error_count = _mismatches(
                rows,
                probe_time,
                {f"dp{output_index}": decision, f"dm{output_index}": 1 - decision},
            )
            decision_errors += error_count
            if test_mode:
                test_decision_errors += error_count
            else:
                normal_decision_errors += error_count
            error_count = _mismatches(rows, probe_time, {"clkc": 0})
            comparator_clock_errors += error_count
            clock_errors += error_count
            pointer += 1
        elif event == "comp_rise" and _logic(rows, "clks", time_s) == 0:
            error_count = _mismatches(rows, probe_time, {"clkc": 0})
            comparator_clock_errors += error_count
            clock_errors += error_count
            stop_checks += 1
            hold_expected = {
                "dp4": p[0], "dm4": m[0],
                "dp3": p[1], "dm3": m[1],
                "dp2": p[2], "dm2": m[2],
                "dp1": p[3], "dm1": m[3],
            }
            error_count = _mismatches(rows, probe_time, hold_expected)
            post_completion_hold_errors += error_count
            post_completion_hold_checks += 1

    sufficient = (
        published_words >= 3
        and completed_conversions >= 2
        and normal_decisions >= 4
        and test_decisions >= 4
        and stop_checks >= 2
        and post_completion_hold_checks >= 2
    )
    ok = sufficient and not (
        reset_errors
        or decision_errors
        or dout_errors
        or clock_errors
        or post_completion_hold_errors
    )
    diagnostics = {
        "P_CONVERSION_RESET_AND_PREVIOUS_WORD": reset_errors,
        "P_SAMPLE_AND_COMPARATOR_DECISIONS": (
            normal_decision_errors + post_completion_hold_errors
        ),
        "P_TEST_OVERRIDE_BEHAVIOR": test_decision_errors,
        "P_DOUT_BIT_MAPPING": dout_errors,
        "P_LOGIC_OUTPUT_LEVELS": clock_errors,
    }
    return ok, (
        f"v4_186 clks_rises={len(clks_rises)} published_words={published_words} "
        f"normal_decisions={normal_decisions} test_decisions={test_decisions} "
        f"completed_conversions={completed_conversions} stop_checks={stop_checks} "
        f"post_completion_hold_checks={post_completion_hold_checks} "
        f"post_completion_hold_errors={post_completion_hold_errors} "
        f"reset_errors={reset_errors} decision_errors={decision_errors} "
        f"dout_errors={dout_errors} clock_errors={clock_errors} "
        f"clock_breakdown={rise_clock_errors}/{fall_clock_errors}/{comparator_clock_errors}; "
        + "; ".join(f"{key} mismatch_count={value}" for key, value in diagnostics.items())
    )

CHECKER_ID = "v4_186_sarfend_logic_4b"
CHECKER: Checker = check_v3_sarfend_logic_4b
