"""Task-specific checker for canonical v4 DUT 318."""
from __future__ import annotations

from checkers.api import Checker
from checkers.common.v4_topup import (
    _v4_topup_logic_high,
)

def check_v4_1016_resistor_ladder_monotonic_decoder(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1016 empty_trace"
    def stable_window(t: float) -> bool:
        edge_times = [4.2e-9, 10e-9, 20e-9, 30e-9, 40e-9, 50e-9, 60e-9, 70e-9, 78e-9, 82e-9, 86e-9]
        return all(not (edge <= t <= edge + 2.5e-9) for edge in edge_times)

    checked = code_errors = metric_errors = flag_errors = clear_errors = 0
    codes_seen: set[int] = set()
    disabled_clear = reset_clear = monotonic_sequence = False
    last_code = None
    last_vout = None
    for row in rows:
        t = float(row["time"])
        enabled = _v4_topup_logic_high(row, "enable") and not _v4_topup_logic_high(row, "rst")
        vout = float(row["vout"])
        step_metric = float(row["step_metric"])
        flag = float(row["monotonic_ok"]) > 0.45
        if not enabled:
            clear = abs(vout) < 0.08 and step_metric < 0.08 and not flag
            if t > 80.5e-9 and not _v4_topup_logic_high(row, "enable") and clear:
                disabled_clear = True
            if t < 8e-9 and _v4_topup_logic_high(row, "rst") and clear:
                reset_clear = True
            if (t > 80.5e-9 and not clear) or (t < 8e-9 and _v4_topup_logic_high(row, "rst") and not clear):
                clear_errors += 1
            continue
        if t < 6.8e-9 or not stable_window(t):
            continue
        code = (
            (1 if _v4_topup_logic_high(row, "code_0") else 0)
            + (2 if _v4_topup_logic_high(row, "code_1") else 0)
            + (4 if _v4_topup_logic_high(row, "code_2") else 0)
        )
        expected_vout = 0.9 * code / 7.0
        expected_step = 0.9 / 7.0
        checked += 1
        codes_seen.add(code)
        if abs(vout - expected_vout) > 0.08:
            code_errors += 1
        if abs(step_metric - expected_step) > 0.01:
            metric_errors += 1
        if not flag:
            flag_errors += 1
        if last_code is not None and code > last_code and last_vout is not None and vout + 0.04 >= last_vout:
            monotonic_sequence = True
        last_code = code
        last_vout = vout
    ok = (
        checked >= 35
        and len(codes_seen) >= 8
        and monotonic_sequence
        and disabled_clear
        and reset_clear
        and code_errors <= max(6, checked // 25)
        and metric_errors <= max(6, checked // 25)
        and flag_errors <= max(4, checked // 30)
        and clear_errors <= 3
    )
    return ok, (
        f"v4_1016 checked={checked} codes={sorted(codes_seen)} monotonic_sequence={monotonic_sequence} "
        f"disabled_clear={disabled_clear} reset_clear={reset_clear} code_errors={code_errors} "
        f"metric_errors={metric_errors} flag_errors={flag_errors} clear_errors={clear_errors}"
    )

CHECKER_ID = "v4_1016_resistor_ladder_monotonic_decoder"
CHECKER: Checker = check_v4_1016_resistor_ladder_monotonic_decoder
