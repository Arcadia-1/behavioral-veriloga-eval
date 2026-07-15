"""Task-specific checker for canonical v4 DUT 050."""
from __future__ import annotations

from ..api import Checker
import math

def sample_signal_at(rows: list[dict[str, float]], signal: str, time_s: float) -> float | None:
    if not rows or "time" not in rows[0] or signal not in rows[0]:
        return None
    first_time = rows[0]["time"]
    last_time = rows[-1].get("time")
    if last_time is None or time_s < first_time or time_s > last_time:
        return None
    if time_s == first_time:
        return rows[0].get(signal)
    for idx in range(1, len(rows)):
        prev = rows[idx - 1]
        cur = rows[idx]
        t0 = prev.get("time")
        t1 = cur.get("time")
        if t0 is None or t1 is None:
            continue
        if t0 <= time_s <= t1:
            v0 = prev.get(signal)
            v1 = cur.get(signal)
            if v0 is None or v1 is None:
                return None
            if t1 == t0:
                return v1
            alpha = (time_s - t0) / (t1 - t0)
            return v0 + alpha * (v1 - v0)
    return None

def check_v3_498_dc_aware_adc3bit(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "d2", "d1", "d0"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing dc-aware adc3bit signals"
    sample_times = [0.6e-9, 1.8e-9, 3.8e-9, 5.8e-9, 7.8e-9, 9.8e-9, 11.8e-9]
    checked = 0
    codes: list[int] = []
    failures: list[str] = []
    for sample_t in sample_times:
        vin = sample_signal_at(rows, "vin", sample_t)
        if vin is None:
            continue
        clipped = min(1.0, max(0.0, vin))
        code = int(math.floor(8.0 * clipped))
        code = max(0, min(7, code))
        expected = {
            "d2": 1 if code >= 4 else 0,
            "d1": 1 if (code % 4) >= 2 else 0,
            "d0": 1 if (code % 2) >= 1 else 0,
        }
        observed: dict[str, int] = {}
        for signal in ("d2", "d1", "d0"):
            value = sample_signal_at(rows, signal, sample_t)
            if value is None:
                failures.append(f"missing_{signal}@{sample_t * 1e9:.2f}ns")
                continue
            observed[signal] = 1 if value > 0.45 else 0
        if observed != expected:
            failures.append(
                f"adc3@{sample_t * 1e9:.2f}ns vin={vin:.3f} code={code} "
                f"obs={observed}"
            )
        codes.append(code)
        checked += 1
    if checked < 6:
        return False, f"insufficient_dc_adc_samples={checked}"
    if min(codes) != 0 or max(codes) != 7 or len(set(codes)) < 5:
        return False, f"insufficient_dc_adc_code_coverage={codes}"
    if failures:
        return False, " ".join(failures[:5])
    return True, f"dc_adc_samples={checked} codes={codes}"

CHECKER_ID = "v4_050_dc_aware_adc3bit"
CHECKER: Checker = check_v3_498_dc_aware_adc3bit
