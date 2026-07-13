"""Task-specific checker for canonical v4 DUT 315."""
from __future__ import annotations

from checkers.api import Checker
from checkers.common.v4_topup import (
    _v4_topup_clip01,
    _v4_topup_logic_high,
)

def check_v4_1013_reference_ladder_buffered_taps(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1013 empty_trace"
    def stable_window(t: float) -> bool:
        edge_times = [12e-9, 28e-9, 40e-9, 44e-9, 50e-9, 66e-9]
        return all(not (edge <= t <= edge + 2.5e-9) for edge in edge_times)

    checked = spacing_errors = flag_errors = clear_errors = 0
    normal_seen = reversed_seen = clamp_seen = disabled_clear = reset_clear = False
    for row in rows:
        t = float(row["time"])
        enabled = _v4_topup_logic_high(row, "enable") and not _v4_topup_logic_high(row, "rst")
        taps = [float(row[f"tap{i}"]) for i in range(4)]
        if not enabled:
            clear = max(abs(v) for v in taps) < 0.08 and float(row["monotonic_ok"]) < 0.12
            if t > 65e-9 and not _v4_topup_logic_high(row, "enable") and clear:
                disabled_clear = True
            if t < 8e-9 and _v4_topup_logic_high(row, "rst") and clear:
                reset_clear = True
            if ((t > 68.5e-9 and not clear) or (t < 8e-9 and _v4_topup_logic_high(row, "rst") and not clear)):
                clear_errors += 1
            continue
        if t < 10e-9 or not stable_window(t):
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
    ok = (
        checked >= 40
        and normal_seen
        and reversed_seen
        and clamp_seen
        and disabled_clear
        and reset_clear
        and spacing_errors <= max(8, checked // 20)
        and flag_errors <= max(6, checked // 25)
        and clear_errors <= 3
    )
    return ok, (
        f"v4_1013 checked={checked} normal={normal_seen} reversed={reversed_seen} clamp={clamp_seen} "
        f"disabled_clear={disabled_clear} reset_clear={reset_clear} spacing_errors={spacing_errors} "
        f"flag_errors={flag_errors} clear_errors={clear_errors}"
    )

CHECKER_ID = "v4_1013_reference_ladder_buffered_taps"
CHECKER: Checker = check_v4_1013_reference_ladder_buffered_taps
