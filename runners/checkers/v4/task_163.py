"""Stimulus-relative checker for canonical v4 DUT 163."""
from __future__ import annotations

from ..api import Checker, Row
from .batch17_stimulus_relative import (
    bind_properties,
    crossings,
    diagnostic,
    event_label,
    logic_at,
    logic_threshold,
    pass_note,
    require_signals,
    sample,
)


PROPERTY_IDS = (
    "P_READY_SERIAL_CAPTURE",
    "P_TERNARY_WEIGHTING",
    "P_NORMALIZED_MIDSCALE_OUTPUT",
    "P_CLOCKED_PUBLICATION_HOLD",
)
SIGNALS = {"time", "dp", "dn", "ready", "clks", "dout"}


def check_v3_cyclic_decoder_10b(rows: list[Row]) -> tuple[bool, str]:
    missing = require_signals(rows, SIGNALS, "P_READY_SERIAL_CAPTURE")
    if missing:
        return False, missing

    ready_threshold = logic_threshold(rows, ("ready",), default_high=1.1)
    clks_threshold = logic_threshold(rows, ("clks",), default_high=1.1)
    decision_threshold = logic_threshold(rows, ("dp", "dn"), default_high=1.1)
    ready_edges = crossings(rows, "ready", threshold=ready_threshold, direction="rising")
    clk_edges = crossings(rows, "clks", threshold=clks_threshold, direction="rising")
    events = [(edge_t, "clk") for edge_t in clk_edges]
    events.extend((edge_t, "ready") for edge_t in ready_edges)
    events.sort()

    if len(clk_edges) < 2 or len(ready_edges) < 4:
        return False, diagnostic(
            "P_READY_SERIAL_CAPTURE",
            "coverage",
            expected="at_least_2_clks_and_4_ready_edges",
            observed=f"clks={len(clk_edges)} ready={len(ready_edges)}",
            event="full_trace",
        )

    nbit = 10
    counter = nbit - 1
    total = 0.0
    expected_samples: list[tuple[float, float, str]] = []
    half_weight_seen = False
    for event_index, (event_t, event_kind) in enumerate(events):
        if event_kind == "ready":
            dp = logic_at(rows, "dp", event_t, threshold=decision_threshold)
            dn = logic_at(rows, "dn", event_t, threshold=decision_threshold)
            if dp is None or dn is None:
                return False, diagnostic(
                    "P_READY_SERIAL_CAPTURE",
                    "invalid_trace",
                    expected="sampled_dp_dn",
                    observed="missing_sample",
                    event=event_label("ready", event_index, event_t),
                )
            if counter >= 0:
                if dp:
                    total += 2.0 ** counter
                elif dn:
                    total += 0.5 * (2.0 ** counter)
                    half_weight_seen = True
            counter -= 1
            continue

        sample_t = event_t + 1.8e-9
        if sample_t <= rows[-1]["time"]:
            expected = total / (2.0 ** nbit - 1.0) - 0.5
            expected_samples.append((sample_t, expected, event_label("clks", event_index, event_t)))
        counter = nbit - 1
        total = 0.0

    if len(expected_samples) < 2:
        return False, diagnostic(
            "P_CLOCKED_PUBLICATION_HOLD",
            "coverage",
            expected="at_least_2_publication_samples",
            observed=f"samples={len(expected_samples)}",
            event="full_trace",
        )

    max_error = 0.0
    for sample_t, expected, label in expected_samples:
        observed = sample(rows, "dout", sample_t)
        if observed is None:
            return False, diagnostic(
                "P_CLOCKED_PUBLICATION_HOLD",
                "invalid_trace",
                expected="dout_sample",
                observed="missing_sample",
                event=label,
            )
        error = abs(observed - expected)
        max_error = max(max_error, error)
        if error > 0.025:
            return False, diagnostic(
                "P_NORMALIZED_MIDSCALE_OUTPUT",
                "value_mismatch",
                expected=f"dout={expected:.5f}",
                observed=f"dout={observed:.5f}",
                event=label,
            )

    if not half_weight_seen:
        return False, diagnostic(
            "P_TERNARY_WEIGHTING",
            "coverage",
            expected="dn_half_weight_decision_seen",
            observed="half_weight_seen=false",
            event="full_trace",
        )
    return True, pass_note(
        PROPERTY_IDS,
        f"published={len(expected_samples)} half_weight_seen={half_weight_seen} max_error={max_error:.5f}",
    )


CHECKER_ID = "v4_163_cyclic_decoder_10b"
CHECKER: Checker = bind_properties(check_v3_cyclic_decoder_10b, PROPERTY_IDS)
