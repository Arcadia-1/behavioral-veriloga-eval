"""Event-relative checker for the successive-approximation calibration FSM."""

from __future__ import annotations

from ..api import Checker, Row
from .stimulus_relative import diagnostic, pass_note


VTH = 0.45
TARGET = 0.45
STEP_INIT = 0.18
VMIN = 0.05
VMAX = 0.85
SETTLE_S = 0.2e-9
PROPERTY_IDS = (
    "P_RESET_SEARCH_STATE",
    "P_SIGNED_TRIAL_UPDATE",
    "P_SUCCESSIVE_STEP_HALVING",
    "P_FOUR_STEP_DONE",
    "P_TRIM_CLAMP",
)


def _rising_edge_indexes(rows: list[Row], signal: str) -> list[int]:
    return [
        index
        for index in range(1, len(rows))
        if float(rows[index - 1][signal]) <= VTH < float(rows[index][signal])
    ]


def _sample_after_event(rows: list[Row], edge_index: int, next_edge_index: int | None) -> Row:
    edge_time = float(rows[edge_index]["time"])
    if next_edge_index is None:
        deadline = float(rows[-1]["time"])
    else:
        deadline = float(rows[next_edge_index]["time"])
    target_time = edge_time + min(SETTLE_S, max(0.0, deadline - edge_time) * 0.4)
    sample = rows[edge_index]
    for row in rows[edge_index:]:
        if float(row["time"]) >= deadline and next_edge_index is not None:
            break
        sample = row
        if float(row["time"]) >= target_time:
            break
    return sample


def check_successive_approximation_calibration_search_fsm(
    rows: list[Row],
) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vin", "out", "metric"}
    missing = sorted(required - (set(rows[0]) if rows else set()))
    if missing:
        return False, diagnostic(
            "P_SIGNED_TRIAL_UPDATE",
            "invalid_trace",
            expected="signals:" + ",".join(sorted(required)),
            observed="missing:" + ",".join(missing),
            event="full_trace",
        )

    reset_observed = any(
        float(row["rst"]) > VTH
        and abs(float(row["out"]) - TARGET) <= 0.08
        and float(row["metric"]) < 0.15
        for row in rows
    )
    clamp_errors = sum(
        not (VMIN - 0.03 <= float(row["out"]) <= VMAX + 0.03) for row in rows
    )

    edges = _rising_edge_indexes(rows, "clk")
    expected_out = TARGET
    step = STEP_INIT
    cycle = 0
    update_checks = 0
    update_errors = 0
    metric_errors = 0
    positive_updates = 0
    negative_updates = 0
    post_done_holds = 0

    for position, edge_index in enumerate(edges):
        edge = rows[edge_index]
        next_edge_index = edges[position + 1] if position + 1 < len(edges) else None
        sample = _sample_after_event(rows, edge_index, next_edge_index)
        if float(edge["rst"]) > VTH:
            expected_out = TARGET
            step = STEP_INIT
            cycle = 0
            continue
        if float(sample["rst"]) > VTH:
            continue

        if cycle < 4:
            vin = float(edge["vin"])
            if vin > TARGET:
                expected_out += step
                positive_updates += 1
            elif vin < TARGET:
                expected_out -= step
                negative_updates += 1
            expected_out = min(VMAX, max(VMIN, expected_out))
            step *= 0.5
            cycle += 1
            update_checks += 1
        else:
            post_done_holds += 1

        if abs(float(sample["out"]) - expected_out) > 0.045:
            update_errors += 1
        expected_metric_high = cycle >= 4
        if (float(sample["metric"]) > VTH) != expected_metric_high:
            metric_errors += 1

    coverage_ok = (
        reset_observed
        and update_checks >= 4
        and positive_updates > 0
        and negative_updates > 0
        and post_done_holds > 0
    )
    ok = coverage_ok and update_errors == 0 and metric_errors == 0 and clamp_errors == 0
    note = (
        f"reset={reset_observed} updates={update_checks} positive={positive_updates} "
        f"negative={negative_updates} post_done_holds={post_done_holds} "
        f"update_errors={update_errors} metric_errors={metric_errors} "
        f"clamp_errors={clamp_errors}"
    )
    if not coverage_ok:
        return False, diagnostic(
            "P_SIGNED_TRIAL_UPDATE",
            "insufficient_excitation",
            expected="reset,4_updates,positive,negative,post_done_hold",
            observed=note.replace(" ", ","),
            event="clk.rising",
        )
    if clamp_errors:
        return False, diagnostic(
            "P_TRIM_CLAMP",
            "behavior_mismatch",
            expected="out_within_clamp",
            observed=f"clamp_errors={clamp_errors}",
            event="full_trace",
        )
    if update_errors:
        return False, diagnostic(
            "P_SIGNED_TRIAL_UPDATE",
            "behavior_mismatch",
            expected="out_tracks_successive_signed_updates",
            observed=f"update_errors={update_errors}",
            event="clk.rising",
        )
    if metric_errors:
        return False, diagnostic(
            "P_FOUR_STEP_DONE",
            "behavior_mismatch",
            expected="metric_high_after_four_updates",
            observed=f"metric_errors={metric_errors}",
            event="clk.rising",
        )
    return ok, pass_note(PROPERTY_IDS, note)


CHECKER_ID = "v4_044_successive_approximation_calibration_search_fsm"
CHECKER: Checker = check_successive_approximation_calibration_search_fsm
