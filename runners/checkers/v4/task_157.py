"""Task-specific checker for canonical v4 DUT 157."""
from __future__ import annotations

from checkers.api import Checker
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

def _v3_missing_columns(rows: list[dict[str, float]], required: set[str]) -> str | None:
    if not rows:
        return "empty_waveform"
    missing = sorted(required - set(rows[0]))
    if missing:
        return "missing_columns=" + ",".join(missing)
    return None

def _v3_logic_at(rows: list[dict[str, float]], signal: str, time_s: float, threshold: float = 0.45) -> int | None:
    value = sample_signal_at(rows, signal, time_s)
    if value is None:
        return None
    return 1 if value > threshold else 0

def _v3_logic_transition_times(
    rows: list[dict[str, float]],
    signals: list[str],
    *,
    threshold: float = 0.45,
) -> list[float]:
    transition_times: set[float] = set()
    for signal in signals:
        for idx in range(1, len(rows)):
            prev = rows[idx - 1][signal]
            cur = rows[idx][signal]
            if (prev <= threshold < cur) or (prev > threshold >= cur):
                transition_times.add(rows[idx]["time"])
    return sorted(transition_times)

def check_v3_folded_flash_dac_4b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vd4", "vd3", "vd2", "vd1", "vout"}
    missing = _v3_missing_columns(rows, required)
    if missing:
        return False, missing

    bit_names = ["vd4", "vd3", "vd2", "vd1"]
    transition_times = _v3_logic_transition_times(rows, bit_names, threshold=0.45)
    candidate_times = [rows[0]["time"] + 1.0e-9] + [time_s + 1.0e-9 for time_s in transition_times]
    sample_times = [time_s for time_s in candidate_times if rows[0]["time"] <= time_s <= rows[-1]["time"]]
    if len(sample_times) < 3:
        return False, f"too_few_folded_dac_samples={len(sample_times)}"

    max_error = 0.0
    checked = 0
    for sample_t in sample_times:
        bits = [_v3_logic_at(rows, name, sample_t, threshold=0.45) for name in bit_names]
        observed = sample_signal_at(rows, "vout", sample_t)
        if observed is None or any(bit is None for bit in bits):
            return False, f"missing_folded_dac_sample={sample_t * 1e9:.3f}ns"
        msb, b3, b2, b1 = bits
        subcode = 4 * b3 + 2 * b2 + b1
        folded_code = 8 + subcode if msb else 8 - subcode
        expected = folded_code / 16.0
        max_error = max(max_error, abs(observed - expected))
        checked += 1
    return max_error <= 0.025, f"checked={checked} max_error={max_error:.5f}"

CHECKER_ID = "v4_157_folded_flash_dac_4b"
CHECKER: Checker = check_v3_folded_flash_dac_4b
