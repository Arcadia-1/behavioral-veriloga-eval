"""Task-specific checker for canonical v4 DUT 307."""
from __future__ import annotations

from ..api import Checker
from ..common.v4_topup import _v4_topup_clip01, _v4_topup_logic_high, _v4_topup_near
from ..common.relative_events import event_period, rising_edges, sample_after_event, sample_step


def check_v4_307_switched_capacitor_integrator_phase_pair(
    rows: list[dict[str, float]],
) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1005 empty_trace"

    step = sample_step(rows)
    guard = step * 8.0
    first_phase_event = min(rising_edges(rows, "phi1") + rising_edges(rows, "phi2"), default=float("inf"))
    initial_checked = initial_errors = 0
    for row in rows:
        if float(row["time"]) >= first_phase_event - guard:
            break
        initial_checked += 1
        if not (
            _v4_topup_near(row["vout"], 0.45, 0.08)
            and _v4_topup_near(row["phase_metric"], 0.45, 0.08)
            and float(row["valid"]) < 0.15
        ):
            initial_errors += 1

    phi1_edges = rising_edges(rows, "phi1")
    phi2_edges = rising_edges(rows, "phi2")
    events = sorted(
        [(event, 0, "phi1") for event in phi1_edges]
        + [(event, 1, "phi2") for event in phi2_edges]
    )
    phi2_period = event_period(rows, "phi2")
    sampled = 0.45
    have_sample = False
    state = 0.45
    metric = 0.45
    valid = False
    phi1_captures = accepted_pairs = overlap_events = 0
    edge_errors = hold_checked = hold_errors = 0
    positive_steps = negative_steps = False

    for event_time, _, kind in events:
        edge_index = next(
            (index for index, row in enumerate(rows) if float(row["time"]) >= event_time),
            None,
        )
        if edge_index is None:
            continue
        edge_row = rows[edge_index]
        active = _v4_topup_logic_high(edge_row, "enable") and not _v4_topup_logic_high(edge_row, "rst")

        if kind == "phi1":
            if not active:
                sampled = 0.45
                have_sample = False
            elif _v4_topup_logic_high(edge_row, "phi2"):
                have_sample = False
            else:
                sampled = float(edge_row["vin"])
                have_sample = True
                phi1_captures += 1
            continue

        post = sample_after_event(
            rows,
            event_time,
            clock_signal="phi2",
            fraction_of_period=0.05,
        )
        if post is None:
            continue
        overlap = _v4_topup_logic_high(edge_row, "phi1")
        if not active:
            state = 0.45
            metric = 0.45
            valid = False
            have_sample = False
        elif overlap:
            valid = False
            overlap_events += 1
        elif have_sample:
            previous_state = state
            state = _v4_topup_clip01(state + 0.2 * (sampled - 0.45))
            metric = sampled
            valid = True
            accepted_pairs += 1
            positive_steps = positive_steps or state > previous_state + 0.006
            negative_steps = negative_steps or state < previous_state - 0.006
        else:
            valid = False

        if (
            abs(float(post["vout"]) - state) > 0.010
            or abs(float(post["phase_metric"]) - metric) > 0.04
            or (float(post["valid"]) > 0.45) != valid
        ):
            edge_errors += 1

        next_phi2 = next((edge for edge in phi2_edges if edge > event_time), float(rows[-1]["time"]))
        for hold_row in rows:
            hold_time = float(hold_row["time"])
            if hold_time < event_time + max(guard, 0.1 * phi2_period):
                continue
            if hold_time >= next_phi2 - 2.0 * step:
                continue
            if not _v4_topup_logic_high(hold_row, "enable") or _v4_topup_logic_high(hold_row, "rst"):
                continue
            hold_checked += 1
            if (
                abs(float(hold_row["vout"]) - state) > 0.010
                or abs(float(hold_row["phase_metric"]) - metric) > 0.04
                or (float(hold_row["valid"]) > 0.45) != valid
            ):
                hold_errors += 1

    allowed_hold_errors = max(4, hold_checked // 100)
    ok = (
        initial_checked >= 8
        and initial_errors == 0
        and phi1_captures >= 4
        and accepted_pairs >= 3
        and overlap_events >= 1
        and positive_steps
        and negative_steps
        and edge_errors == 0
        and hold_checked >= 20
        and hold_errors <= allowed_hold_errors
    )
    diagnostics = {
        "P_ON_RESET_OR_WHEN_DISABLED_CLEAR": int(initial_checked < 8) + initial_errors,
        "P_ON_A_RISING_PHI1_CROSSING_SAMPLE": int(phi1_captures < 4),
        "P_ON_THE_FOLLOWING_RISING_PHI2_CROSSING": (
            int(accepted_pairs < 3)
            + int(not positive_steps or not negative_steps)
            + edge_errors
        ),
        "P_REJECT_OVERLAPPING_PHI1_AND_PHI2_UPDATES": int(overlap_events < 1),
        "P_EXPOSE_THE_MOST_RECENT_ACCEPTED_PHASE": max(
            0, hold_errors - allowed_hold_errors
        ),
        "P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE": 0,
    }
    return ok, (
        f"v4_307 initial_checked={initial_checked} initial_errors={initial_errors} "
        f"phi1_captures={phi1_captures} accepted_pairs={accepted_pairs} overlap_events={overlap_events} "
        f"positive_steps={positive_steps} negative_steps={negative_steps} edge_errors={edge_errors} "
        f"hold_checked={hold_checked} hold_errors={hold_errors}; "
        + "; ".join(f"{key} mismatch_count={value}" for key, value in diagnostics.items())
    )


CHECKER_ID = "v4_307_switched_capacitor_integrator_phase_pair"
CHECKER: Checker = check_v4_307_switched_capacitor_integrator_phase_pair
