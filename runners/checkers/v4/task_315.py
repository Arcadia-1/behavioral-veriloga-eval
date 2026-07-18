"""Task-specific checker for canonical v4 DUT 315."""
from __future__ import annotations

from ..api import Checker
from ..common.v4_topup import (
    _v4_topup_clip01,
    _v4_topup_logic_high,
)

def check_v4_315_reference_ladder_buffered_taps(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1013 empty_trace"

    def settled(index: int) -> bool:
        """Only score after stimulus and DUT outputs stop moving."""
        if index < 2:
            return False
        names = (
            "vref_hi", "vref_lo", "enable", "rst",
            "tap0", "tap1", "tap2", "tap3", "monotonic_ok",
        )
        for current in range(index - 1, index + 1):
            previous = rows[current - 1]
            row = rows[current]
            if any(abs(float(row[name]) - float(previous[name])) > 1e-4 for name in names):
                return False
        return True

    checked = spacing_errors = flag_errors = clear_errors = 0
    normal_seen = reversed_seen = clamp_seen = disabled_clear = reset_clear = False
    saw_active = False
    for index, row in enumerate(rows):
        t = float(row["time"])
        enabled = _v4_topup_logic_high(row, "enable") and not _v4_topup_logic_high(row, "rst")
        taps = [float(row[f"tap{i}"]) for i in range(4)]
        if not enabled:
            clear = max(abs(v) for v in taps) < 0.08 and float(row["monotonic_ok"]) < 0.12
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
        hi_raw = float(row["vref_hi"])
        lo_raw = float(row["vref_lo"])
        hi_c = _v4_topup_clip01(max(hi_raw, lo_raw))
        lo_c = _v4_topup_clip01(min(hi_raw, lo_raw))
        span = hi_c - lo_c
        expected = [lo_c + span * i / 3.0 for i in range(4)]
        checked += 1
        normal_seen = normal_seen or hi_raw > lo_raw + 0.12
        reversed_seen = reversed_seen or lo_raw > hi_raw + 0.12
        clamp_seen = clamp_seen or hi_raw > 0.92 or lo_raw < -0.02
        if max(abs(taps[i] - expected[i]) for i in range(4)) > 0.08:
            spacing_errors += 1
        monotonic = taps[0] <= taps[1] + 0.02 and taps[1] <= taps[2] + 0.02 and taps[2] <= taps[3] + 0.02
        if (float(row["monotonic_ok"]) > 0.45) != monotonic:
            flag_errors += 1
    spacing_error_limit = max(32, checked // 10)
    flag_error_limit = max(12, checked // 25)
    clear_error_limit = max(14, checked // 25)
    ok = (
        checked >= 40
        and normal_seen
        and reversed_seen
        and clamp_seen
        and disabled_clear
        and reset_clear
        and spacing_errors <= spacing_error_limit
        and flag_errors <= flag_error_limit
        and clear_errors <= clear_error_limit
    )
    return ok, (
        f"v4_315 checked={checked} normal={normal_seen} reversed={reversed_seen} clamp={clamp_seen} "
        f"disabled_clear={disabled_clear} reset_clear={reset_clear} spacing_errors={spacing_errors} "
        f"flag_errors={flag_errors} clear_errors={clear_errors} "
        f"spacing_error_limit={spacing_error_limit} flag_error_limit={flag_error_limit} "
        f"clear_error_limit={clear_error_limit}"
    )

CHECKER_ID = "v4_315_reference_ladder_buffered_taps"
CHECKER: Checker = check_v4_315_reference_ladder_buffered_taps
