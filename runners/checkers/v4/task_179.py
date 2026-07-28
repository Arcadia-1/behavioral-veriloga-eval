"""Stimulus-relative checker for canonical v4 DUT 179."""

from __future__ import annotations

from ..api import Checker, Row
from .trace_utils import property_diagnostics, sample_signal, threshold_crossings


FULL_RANGE_S = 100e-12
OUTPUT_SETTLE_S = 30e-12
PROPERTY_IDS = (
    "P_SAMPLE_REARMS_MEASUREMENT",
    "P_INPUT_EDGE_PAIR_CAPTURE",
    "P_SIGNED_DELTA_POLARITY",
    "P_FULL_RANGE_SCALE",
)


def _probe_time(event_time: float, next_time: float, settle: float) -> float:
    if next_time == float("inf"):
        return event_time + settle
    return event_time + min(settle, 0.45 * (next_time - event_time))


def check_v3_tdc_ideal_edge_delta(rows: list[Row]) -> tuple[bool, str]:
    required = {"time", "inp", "inn", "samp", "vout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing tdc ideal edge delta signals"

    events = sorted(
        [
            *[(time_s, 0, "samp") for time_s in threshold_crossings(rows, "samp", direction=1)],
            *[(time_s, 1, "inp") for time_s in threshold_crossings(rows, "inp", direction=1)],
            *[(time_s, 1, "inn") for time_s in threshold_crossings(rows, "inn", direction=1)],
        ]
    )
    counts = dict.fromkeys(PROPERTY_IDS, 0)
    # The task contract defines edge deltas and full range in physical seconds.
    # Adaptive simulators may publish different numbers of rows across the same
    # output transition, so an observed transition-row span is not a time-unit
    # conversion and must not rescale either the delta or the settle interval.
    settle = OUTPUT_SETTLE_S
    expected = 0.0
    timep: float | None = None
    timen: float | None = None
    sample_edges = 0
    retained_single_edges = 0
    measured_deltas: list[float] = []
    first_mismatch = ""

    for index, (event_time, _, signal) in enumerate(events):
        next_time = events[index + 1][0] if index + 1 < len(events) else float("inf")
        probe_time = _probe_time(event_time, next_time, settle)
        if probe_time > rows[-1]["time"]:
            continue

        if signal == "samp":
            sample_edges += 1
            timep = None
            timen = None
            property_id = "P_SAMPLE_REARMS_MEASUREMENT"
        else:
            if signal == "inp":
                timep = event_time
            else:
                timen = event_time
            if timep is None or timen is None:
                retained_single_edges += 1
                property_id = "P_SAMPLE_REARMS_MEASUREMENT"
            else:
                expected = (timep - timen) / FULL_RANGE_S
                measured_deltas.append(expected)
                property_id = "P_INPUT_EDGE_PAIR_CAPTURE"

        observed = sample_signal(rows, "vout", probe_time)
        tolerance = max(0.025, 0.01 * abs(expected))
        if observed is None or abs(observed - expected) > tolerance:
            counts[property_id] += 1
            if signal != "samp" and timep is not None and timen is not None:
                counts["P_SIGNED_DELTA_POLARITY"] += 1
                counts["P_FULL_RANGE_SCALE"] += 1
            if not first_mismatch:
                observed_note = "missing" if observed is None else f"{observed:.6g}"
                first_mismatch = (
                    f" first_mismatch_time={probe_time:.12g} expected={expected:.6g} "
                    f"observed={observed_note} property={property_id}"
                )

    positive = sum(delta > 0.2 for delta in measured_deltas)
    negative = sum(delta < -0.2 for delta in measured_deltas)
    counts["P_SAMPLE_REARMS_MEASUREMENT"] += int(sample_edges < 2)
    counts["P_SAMPLE_REARMS_MEASUREMENT"] += int(retained_single_edges < 2)
    counts["P_INPUT_EDGE_PAIR_CAPTURE"] += int(len(measured_deltas) < 2)
    counts["P_SIGNED_DELTA_POLARITY"] += int(not positive or not negative)
    counts["P_FULL_RANGE_SCALE"] += int(
        len({round(abs(delta), 6) for delta in measured_deltas if abs(delta) > 0.2}) < 2
    )
    coverage = (
        f"sample_edges={sample_edges} retained_single_edges={retained_single_edges} "
        f"full_range_s={FULL_RANGE_S:.6g} settle_s={settle:.6g} "
        f"measured_deltas={[round(delta, 6) for delta in measured_deltas]}"
    )
    ok = all(count == 0 for count in counts.values())
    return ok, f"{property_diagnostics(counts)}; {coverage}{first_mismatch}"


CHECKER_ID = "v4_179_tdc_ideal_edge_delta"
CHECKER: Checker = check_v3_tdc_ideal_edge_delta
