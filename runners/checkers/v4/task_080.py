"""Task-specific checker for canonical v4 DUT 080."""
from __future__ import annotations

from checkers.api import Checker
import math

def check_multitone(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "empty"
    out_col = next((k for k in rows[0] if k.lower() in {"out", "vout"}), None)
    if out_col is None:
        return False, f"missing out/vout column; keys={list(rows[0].keys())[:10]}"

    times = [r["time"] for r in rows]
    vals = [r[out_col] for r in rows]

    def interp(t: float) -> float | None:
        if not times:
            return None
        if t <= times[0]:
            return vals[0]
        if t >= times[-1]:
            return vals[-1]
        lo = 0
        hi = len(times) - 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if times[mid] <= t:
                lo = mid
            else:
                hi = mid
        t0 = times[lo]
        t1 = times[hi]
        if t1 == t0:
            return vals[lo]
        a = (t - t0) / (t1 - t0)
        return vals[lo] + a * (vals[hi] - vals[lo])

    samples = [
        (0.125e-6, 0.2 * math.sin(2 * math.pi * 1e6 * 0.125e-6) + 0.1 * math.sin(2 * math.pi * 2e6 * 0.125e-6) + 0.05 * math.sin(2 * math.pi * 3e6 * 0.125e-6)),
        (0.275e-6, 0.2 * math.sin(2 * math.pi * 1e6 * 0.275e-6) + 0.1 * math.sin(2 * math.pi * 2e6 * 0.275e-6) + 0.05 * math.sin(2 * math.pi * 3e6 * 0.275e-6)),
        (0.410e-6, 0.2 * math.sin(2 * math.pi * 1e6 * 0.410e-6) + 0.1 * math.sin(2 * math.pi * 2e6 * 0.410e-6) + 0.05 * math.sin(2 * math.pi * 3e6 * 0.410e-6)),
    ]
    errs = []
    for t_check, expected in samples:
        measured = interp(t_check)
        if measured is None:
            errs.append(1.0)
            continue
        errs.append(abs(measured - expected))
    max_err = max(errs)
    ok = max_err < 0.03
    return ok, f"max_err={max_err:.4f}"

CHECKER_ID = "v4_080_sine_periodic_voltage_source"
CHECKER: Checker = check_multitone
