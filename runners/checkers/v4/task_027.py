"""Stimulus-relative checker for canonical v4 DUT 027."""
from __future__ import annotations

import math

from ..api import Checker
from .stimulus_relative import (
    bit_code,
    event_settle_delay,
    finish,
    missing_trace,
    rising_indices,
    row_at_or_after,
)


PROPERTY_IDS = [
    "P_V2B_ROUND_AND_CLAMP",
    "P_ACTIVE_LOW_RESET_POINTER",
    "P_ROTATING_POINTER_UPDATE",
    "P_POINTER_ONE_HOT",
    "P_DWA_SELECTED_MASK",
    "P_SYSTEM_CODE_BINDING",
]
CODE_BITS = ["code_0", "code_1", "code_2", "code_3"]
PTR_BITS = [f"ptr_{index}" for index in range(16)]
CELL_BITS = [f"cell_en_{index}" for index in range(16)]


def _active_indices(row: dict[str, float], signals: list[str]) -> set[int]:
    return {index for index, signal in enumerate(signals) if row[signal] > 0.45}


def check_dwa_dem_encoder(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk_i", "rst_ni", "vin_node", *CODE_BITS, *PTR_BITS, *CELL_BITS}
    results, error = missing_trace(CHECKER_ID, rows, required, PROPERTY_IDS)
    if error is not None:
        return error
    by_id = {result.property_id: result for result in results}

    edges = rising_indices(rows, "clk_i")
    edge_times = [float(rows[index]["time"]) for index in edges]
    settle = event_settle_delay(edge_times)
    pointer = 0
    previous_helper_code = 0
    reset_edges = 0
    post_reset_edges = 0
    wrap_events = 0
    helper_codes: set[int] = set()
    zero_mask_checks = 0

    for index in edges:
        edge = rows[index]
        event_time = float(edge["time"])
        sample = row_at_or_after(rows, event_time + settle)
        expected_helper_code = min(15, max(0, math.floor(edge["vin_node"] + 0.5)))
        observed_helper_code = bit_code(sample, CODE_BITS)
        helper_codes.add(expected_helper_code)
        by_id["P_V2B_ROUND_AND_CLAMP"].condition(
            observed_helper_code == expected_helper_code,
            expected=f"helper_code={expected_helper_code}",
            observed=f"helper_code={observed_helper_code}",
            time_s=sample["time"],
            gap=abs(observed_helper_code - expected_helper_code),
        )

        if edge["rst_ni"] < 0.45:
            pointer = 0
            effective_code = 0
            reset_edges += 1
            property_id = "P_ACTIVE_LOW_RESET_POINTER"
        else:
            previous_pointer = pointer
            effective_code = previous_helper_code
            pointer = (pointer + effective_code) % 16
            post_reset_edges += 1
            if pointer < previous_pointer:
                wrap_events += 1
            property_id = "P_ROTATING_POINTER_UPDATE"

        observed_pointer_bits = _active_indices(sample, PTR_BITS)
        expected_pointer_bits = {pointer}
        by_id[property_id].condition(
            observed_pointer_bits == expected_pointer_bits,
            expected=f"pointer={pointer}",
            observed=f"pointer_bits={sorted(observed_pointer_bits)}",
            time_s=sample["time"],
            gap=len(observed_pointer_bits ^ expected_pointer_bits),
        )
        by_id["P_POINTER_ONE_HOT"].condition(
            observed_pointer_bits == expected_pointer_bits,
            expected="exactly_one_hot_pointer",
            observed=f"pointer_bits={sorted(observed_pointer_bits)}",
            time_s=sample["time"],
            gap=abs(len(observed_pointer_bits) - 1),
        )

        expected_cells = {(pointer - offset) % 16 for offset in range(effective_code + 1)}
        observed_cells = _active_indices(sample, CELL_BITS)
        if effective_code == 0:
            zero_mask_checks += 1
        by_id["P_DWA_SELECTED_MASK"].condition(
            observed_cells == expected_cells,
            expected=f"cells={sorted(expected_cells)}",
            observed=f"cells={sorted(observed_cells)}",
            time_s=sample["time"],
            gap=len(observed_cells ^ expected_cells),
        )
        by_id["P_SYSTEM_CODE_BINDING"].condition(
            observed_helper_code == expected_helper_code
            and observed_pointer_bits == expected_pointer_bits
            and observed_cells == expected_cells,
            expected=(
                f"helper={expected_helper_code},effective={effective_code},pointer={pointer}"
            ),
            observed=(
                f"helper={observed_helper_code},pointer_bits={sorted(observed_pointer_bits)},"
                f"cell_count={len(observed_cells)}"
            ),
            time_s=sample["time"],
            gap=(
                abs(observed_helper_code - expected_helper_code)
                + len(observed_pointer_bits ^ expected_pointer_bits)
                + len(observed_cells ^ expected_cells)
            ),
        )
        previous_helper_code = expected_helper_code

    by_id["P_V2B_ROUND_AND_CLAMP"].condition(
        len(helper_codes) >= 5,
        expected="at_least_5_distinct_helper_codes",
        observed=f"codes={sorted(helper_codes)}",
        time_s=edge_times[-1] if edge_times else 0.0,
        gap=max(0, 5 - len(helper_codes)),
    )
    by_id["P_ACTIVE_LOW_RESET_POINTER"].condition(
        reset_edges >= 1,
        expected="sampled_active_low_reset",
        observed=f"reset_edges={reset_edges}",
        time_s=edge_times[-1] if edge_times else 0.0,
        gap=max(0, 1 - reset_edges),
    )
    by_id["P_ROTATING_POINTER_UPDATE"].condition(
        post_reset_edges >= 5 and wrap_events >= 1,
        expected="at_least_5_updates_and_1_wrap",
        observed=f"updates={post_reset_edges},wraps={wrap_events}",
        time_s=edge_times[-1] if edge_times else 0.0,
        gap=max(0, 5 - post_reset_edges) + max(0, 1 - wrap_events),
    )
    by_id["P_DWA_SELECTED_MASK"].condition(
        zero_mask_checks >= 1,
        expected="code_zero_boundary_cell_exercised",
        observed=f"zero_mask_checks={zero_mask_checks}",
        time_s=edge_times[-1] if edge_times else 0.0,
        gap=max(0, 1 - zero_mask_checks),
    )
    return finish(
        CHECKER_ID,
        results,
        coverage=(
            f"rising_edges={len(edges)} reset_edges={reset_edges} "
            f"post_reset_edges={post_reset_edges} helper_codes={len(helper_codes)} "
            f"wraps={wrap_events}"
        ),
    )


CHECKER_ID = "v4_027_dwa_dem_encoder"
CHECKER: Checker = check_dwa_dem_encoder
