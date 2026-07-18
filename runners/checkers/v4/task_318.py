"""Task-specific checker for canonical v4 DUT 318."""
from __future__ import annotations

from ..api import Checker
from ..common.v4_topup import (
    _v4_topup_logic_high,
)

def check_v4_318_resistor_ladder_monotonic_decoder(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1016 empty_trace"

    def settled(index: int) -> bool:
        """Score stable code/output plateaus, independent of event timestamps."""
        if index < 2:
            return False
        names = (
            "enable", "rst", "code_0", "code_1", "code_2",
            "vout", "step_metric", "monotonic_ok",
        )
        for current in range(index - 1, index + 1):
            previous = rows[current - 1]
            row = rows[current]
            if any(abs(float(row[name]) - float(previous[name])) > 1e-4 for name in names):
                return False
        return True

    checked = code_errors = metric_errors = flag_errors = clear_errors = 0
    codes_seen: set[int] = set()
    disabled_clear = reset_clear = monotonic_sequence = False
    last_code = None
    last_vout = None
    saw_active = False
    for index, row in enumerate(rows):
        t = float(row["time"])
        enabled = _v4_topup_logic_high(row, "enable") and not _v4_topup_logic_high(row, "rst")
        vout = float(row["vout"])
        step_metric = float(row["step_metric"])
        flag = float(row["monotonic_ok"]) > 0.45
        if not enabled:
            clear = abs(vout) < 0.08 and step_metric < 0.08 and not flag
            stable = settled(index)
            if saw_active and not _v4_topup_logic_high(row, "enable") and not _v4_topup_logic_high(row, "rst") and stable and clear:
                disabled_clear = True
            if _v4_topup_logic_high(row, "rst") and stable and clear:
                reset_clear = True
            if stable and ((saw_active and not _v4_topup_logic_high(row, "enable") and not _v4_topup_logic_high(row, "rst")) or _v4_topup_logic_high(row, "rst")) and not clear:
                clear_errors += 1
            continue
        saw_active = True
        if not settled(index):
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
    code_error_limit = max(50, checked // 8)
    metric_error_limit = max(6, checked // 25)
    flag_error_limit = max(6, checked // 30)
    clear_error_limit = max(7, checked // 50)
    ok = (
        checked >= 35
        and len(codes_seen) >= 8
        and monotonic_sequence
        and disabled_clear
        and reset_clear
        and code_errors <= code_error_limit
        and metric_errors <= metric_error_limit
        and flag_errors <= flag_error_limit
        and clear_errors <= clear_error_limit
    )
    return ok, (
        f"v4_318 checked={checked} codes={sorted(codes_seen)} monotonic_sequence={monotonic_sequence} "
        f"disabled_clear={disabled_clear} reset_clear={reset_clear} code_errors={code_errors} "
        f"metric_errors={metric_errors} flag_errors={flag_errors} clear_errors={clear_errors} "
        f"code_error_limit={code_error_limit} metric_error_limit={metric_error_limit} "
        f"flag_error_limit={flag_error_limit} clear_error_limit={clear_error_limit}"
    )

CHECKER_ID = "v4_318_resistor_ladder_monotonic_decoder"
CHECKER: Checker = check_v4_318_resistor_ladder_monotonic_decoder
