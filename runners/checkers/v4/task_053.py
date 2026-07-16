"""Task-specific checker for canonical v4 DUT 053."""
from __future__ import annotations

from ..api import Checker
def check_v3_495_slew_rate_dac4(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "d3", "d2", "d1", "d0", "vout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing slew-rate dac4 signals"
    expected = 0.0
    last_t = rows[0]["time"]
    max_err = 0.0
    max_endpoint_err = 0.0
    checked = 0
    endpoint_checks = 0
    seen_codes: set[int] = set()
    code_transitions = 0
    previous_code: int | None = None
    for row in rows[1:]:
        code = 0
        code += 8 if row["d3"] > 0.45 else 0
        code += 4 if row["d2"] > 0.45 else 0
        code += 2 if row["d1"] > 0.45 else 0
        code += 1 if row["d0"] > 0.45 else 0
        seen_codes.add(code)
        if previous_code is not None and code != previous_code:
            code_transitions += 1
        previous_code = code
        target = code / 15.0
        dt = max(0.0, row["time"] - last_t)
        step = 1e8 * dt
        if expected < target:
            expected = min(target, expected + step)
        elif expected > target:
            expected = max(target, expected - step)
        last_t = row["time"]
        if row["time"] < 0.5e-9:
            continue
        err = abs(row["vout"] - expected)
        max_err = max(max_err, err)
        checked += 1
        if abs(expected - target) < 0.003 and code in {0, 3, 6, 12, 15}:
            endpoint_err = abs(row["vout"] - target)
            max_endpoint_err = max(max_endpoint_err, endpoint_err)
            endpoint_checks += 1
    if checked < 40:
        return False, f"insufficient_slew_samples={checked}"
    if len(seen_codes) < 4 or code_transitions < 3 or not {0, 15}.issubset(seen_codes):
        return False, (
            "insufficient_code_excitation="
            f"codes={sorted(seen_codes)},transitions={code_transitions},"
            "required=code0_code15_four_distinct_three_transitions"
        )
    if endpoint_checks < 8:
        return False, f"insufficient_settled_endpoint_checks={endpoint_checks}"
    if max_err > 0.075:
        return False, f"max_slew_error={max_err:.4f}"
    if max_endpoint_err > 0.020:
        return False, f"max_endpoint_error={max_endpoint_err:.4f}"
    return True, (
        f"slew_samples={checked} settled_checks={endpoint_checks} "
        f"max_err={max_err:.4f} max_endpoint_err={max_endpoint_err:.4f}"
    )

CHECKER_ID = "v4_053_slew_rate_dac4"
CHECKER: Checker = check_v3_495_slew_rate_dac4
