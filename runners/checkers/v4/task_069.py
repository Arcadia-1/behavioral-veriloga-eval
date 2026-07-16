"""Task-specific checker for canonical v4 DUT 069."""
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
    "P_IDLE_CAPTURE",
    "P_ZERO_CODE_MINIMUM",
    "P_PULSE_COUNT",
    "P_WIDTH_AND_PERIOD",
    "P_COMPLETION",
    "P_OUTPUT_LEVELS",
)

def check_configurable_pulse_train(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "start", "pulse", "done", *{f"period{i}" for i in range(4)}, *{f"width{i}" for i in range(4)}, *{f"count{i}" for i in range(4)}}
    invalid = require_signals(rows, required, "P_IDLE_CAPTURE")
    if invalid:
        return False, invalid
    clk_rises = crossings(rows, "clk", threshold=0.45, direction="rising")
    edge_pairs = [
        (
            nearest_row(rows, edge_t),
            nearest_row(rows, probe_time(rows, edge_t, clk_rises[index + 1] if index + 1 < len(clk_rises) else None, fraction=0.25) or edge_t),
        )
        for index, edge_t in enumerate(clk_rises)
    ]
    running = False
    period = width = total = 0
    tick = emitted = 0
    errors = 0
    done_seen = False
    expected_total = 0
    expected_total_all = 0
    zero_code_command = False
    failures: list[str] = []
    pre_start_quiet = False
    for edge_index, (edge_row, out_row) in enumerate(edge_pairs, start=1):
        if edge_row is None or out_row is None:
            continue
        if edge_row["start"] > 0.45 and not running:
            raw_period = logic_bits_to_int(edge_row, "period", 4)
            raw_width = logic_bits_to_int(edge_row, "width", 4)
            raw_total = logic_bits_to_int(edge_row, "count", 4)
            zero_code_command = raw_period == 0 and raw_width == 0 and raw_total == 0
            period = max(1, raw_period)
            width = max(1, raw_width)
            total = max(1, raw_total)
            expected_total = total
            expected_total_all += total
            running = True
            tick = 0
            emitted = 0
        elif not running and expected_total == 0:
            pre_start_quiet = pre_start_quiet or (out_row["pulse"] <= 0.45 and out_row["done"] <= 0.45)
        expected_pulse = running and emitted < total and (tick % period) < width
        if (out_row["pulse"] > 0.45) != expected_pulse:
            errors += 1
            if zero_code_command:
                failures.append(
                    diagnostic(
                        "P_ZERO_CODE_MINIMUM",
                        "semantic_mismatch",
                        expected="pulse=high_for_minimum_command",
                        observed=f"pulse={out_row['pulse']:.3f}",
                        event=event_label("clk_rise", edge_index, edge_row["time"]),
                    )
                )
            else:
                failures.append(
                    diagnostic(
                        "P_WIDTH_AND_PERIOD",
                        "semantic_mismatch",
                        expected=f"pulse={0.9 if expected_pulse else 0.0:.1f}",
                        observed=f"pulse={out_row['pulse']:.3f},period={period},width={width},count={total}",
                        event=event_label("clk_rise", edge_index, edge_row["time"]),
                    )
                )
        if running:
            if tick % period == period - 1:
                emitted += 1
            tick += 1
            if emitted >= total and (tick % period) == 0:
                running = False
        expected_done = not running and emitted >= total and total > 0
        done_seen = done_seen or expected_done
        if (out_row["done"] > 0.45) != expected_done:
            errors += 1
            failures.append(
                diagnostic(
                    "P_COMPLETION",
                    "semantic_mismatch",
                    expected=f"done={0.9 if expected_done else 0.0:.1f}",
                    observed=f"done={out_row['done']:.3f},period={period},width={width},count={total}",
                    event=event_label("clk_rise", edge_index, edge_row["time"]),
                )
            )
    pulse_count = len(crossings(rows, "pulse", threshold=0.45, direction="rising"))
    if expected_total_all and pulse_count != expected_total_all:
        errors += 1
        failures.insert(
            0,
            diagnostic(
                "P_PULSE_COUNT",
                "semantic_mismatch",
                expected=f"pulse_count={expected_total_all}",
                observed=f"pulse_count={pulse_count}",
                event="full_trace",
            ),
        )
    if failures:
        return False, " ".join(failures[:5])
    summary = (
        f"errors={errors} done_seen={done_seen} pre_start_quiet={pre_start_quiet} "
        f"pulse_count={pulse_count} expected_total={expected_total_all}"
    )
    ok = errors == 0 and done_seen and pre_start_quiet
    if not ok:
        return False, diagnostic(
            "P_IDLE_CAPTURE",
            "insufficient_coverage",
            expected="quiet_before_start,completion_seen,no_errors",
            observed=summary.replace(" ", "_"),
            event="full_trace",
        )
    return True, pass_note(PROPERTIES, summary)

CHECKER_ID = "v4_069_configurable_pulse_train_generator"
CHECKER: Checker = check_configurable_pulse_train
