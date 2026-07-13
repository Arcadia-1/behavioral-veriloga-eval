"""Task-specific checker for canonical v4 DUT 052."""
from __future__ import annotations

from checkers.api import Checker
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

def check_v3_497_thermometer_bus_encoder(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", *{f"t{i}" for i in range(16)}}
    if not rows or not required.issubset(rows[0]):
        return False, "missing thermometer bus encoder signals"
    sample_times = [1.4e-9, 3.4e-9, 5.4e-9, 7.4e-9, 9.4e-9, 10.8e-9]
    checked = 0
    failures: list[str] = []
    for sample_t in sample_times:
        vin = sample_signal_at(rows, "vin", sample_t)
        if vin is None:
            continue
        clipped = min(1.0, max(0.0, vin))
        code = int(math.floor(16.0 * clipped))
        code = max(0, min(16, code))
        bits = []
        for bit in range(16):
            value = sample_signal_at(rows, f"t{bit}", sample_t)
            if value is None:
                bits.append(-1)
            else:
                bits.append(1 if value > 0.45 else 0)
        if -1 in bits:
            failures.append(f"missing_bus_sample@{sample_t * 1e9:.2f}ns")
            continue
        expected = [1 if bit < code else 0 for bit in range(16)]
        if bits != expected:
            failures.append(
                f"therm@{sample_t * 1e9:.2f}ns code={code} observed={sum(bits)} prefix={''.join(str(x) for x in bits[:8])}"
            )
        if any(bits[i] < bits[i + 1] for i in range(15)):
            failures.append(f"non_prefix_order@{sample_t * 1e9:.2f}ns")
        checked += 1
    if checked < 4:
        return False, f"insufficient_thermometer_samples={checked}"
    if failures:
        return False, " ".join(failures[:5])
    return True, f"thermometer_samples={checked}"

CHECKER_ID = "v4_052_thermometer_bus_encoder"
CHECKER: Checker = check_v3_497_thermometer_bus_encoder
