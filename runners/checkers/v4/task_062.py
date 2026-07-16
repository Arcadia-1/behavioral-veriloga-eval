"""Task-specific checker for canonical v4 DUT 062."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import (
    crossings,
    diagnostic,
    event_label,
    logic_bits_to_int,
    nearest_row,
    pass_note,
    probe_time,
    require_signals,
)


PROPERTIES = (
    "P_REQUEST_START",
    "P_WAIT_CYCLE_COUNT",
    "P_READY_COMPLETION",
    "P_ZERO_LATENCY",
    "P_RESULT_HOLD_AND_ORDER",
)


def check_ready_valid_latency_counter_12b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "valid_i", "ready_i", "done", *{f"lat{i}" for i in range(12)}}
    invalid = require_signals(rows, required, "P_REQUEST_START")
    if invalid:
        return False, invalid
    clk_rises = crossings(rows, "clk", threshold=0.45, direction="rising")
    rise_rows: list[dict[str, float]] = []
    for index, edge_t in enumerate(clk_rises):
        next_edge = clk_rises[index + 1] if index + 1 < len(clk_rises) else None
        settled_t = probe_time(rows, edge_t, next_edge, fraction=0.25)
        row = nearest_row(rows, settled_t) if settled_t is not None else None
        if row is not None:
            rise_rows.append(row)
    active = False
    count = 0
    errors = 0
    checked: list[int] = []
    failures: list[str] = []
    for edge_index, row in enumerate(rise_rows, start=1):
        valid = row["valid_i"] > 0.45
        ready = row["ready_i"] > 0.45
        if valid and not active:
            active = True
            count = 0
        elif active and not ready:
            count += 1
        if active and ready:
            expected = count
            actual = logic_bits_to_int(row, "lat", 12)
            if row["done"] <= 0.45 or actual != expected:
                errors += 1
                failures.append(
                    diagnostic(
                        "P_READY_COMPLETION",
                        "semantic_mismatch",
                        expected=f"latency={expected},done=high",
                        observed=f"latency={actual},done={row['done']:.3f}",
                        event=event_label("clk_rise", edge_index, row["time"]),
                    )
                )
            checked.append(expected)
            active = False
    if failures:
        return False, " ".join(failures[:5])
    ok = errors == 0 and len(checked) >= 2 and max(checked, default=0) > 0
    summary = f"checked={checked} errors={errors} sampled_clock_edges={len(rise_rows)}"
    if not ok:
        return False, diagnostic(
            "P_WAIT_CYCLE_COUNT",
            "insufficient_coverage",
            expected="two_transactions,nonzero_latency",
            observed=summary.replace(" ", "_"),
            event="full_trace",
        )
    return True, pass_note(PROPERTIES, summary)

CHECKER_ID = "v4_062_latency_counter_ready_valid_12b"
CHECKER: Checker = check_ready_valid_latency_counter_12b
