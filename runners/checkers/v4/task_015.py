"""Task-specific checker for canonical v4 DUT 015."""
from __future__ import annotations

from checkers.api import Checker
_RELEASE_SIMPLE_BINARY_DAC_CODES = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
_RELEASE_SIMPLE_BINARY_DAC_SAMPLE_TIMES_NS = (5.0,
 15.0,
 25.0,
 35.0,
 45.0,
 55.0,
 65.0,
 75.0,
 85.0,
 95.0,
 105.0,
 115.0,
 125.0,
 135.0,
 145.0,
 155.0)

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

def check_simple_binary_dac_4b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "aout", "code_0", "code_1", "code_2", "code_3"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/aout/code_0/code_1/code_2/code_3"
    expected = [0.9 * code / 15.0 for code in _RELEASE_SIMPLE_BINARY_DAC_CODES]
    observed: list[float] = []
    observed_codes: list[int] = []
    code_mismatches = 0
    for t_ns, expected_code in zip(_RELEASE_SIMPLE_BINARY_DAC_SAMPLE_TIMES_NS, _RELEASE_SIMPLE_BINARY_DAC_CODES):
        value = sample_signal_at(rows, "aout", t_ns * 1e-9)
        if value is None:
            return False, f"missing_sample_at={t_ns:g}ns"
        observed_code = 0
        for bit_idx in range(4):
            bit_value = sample_signal_at(rows, f"code_{bit_idx}", t_ns * 1e-9)
            if bit_value is None:
                return False, f"missing_code_{bit_idx}_sample_at={t_ns:g}ns"
            if bit_value > 0.45:
                observed_code |= 1 << bit_idx
        if observed_code != expected_code:
            code_mismatches += 1
        observed_codes.append(observed_code)
        observed.append(value)
    max_err = max(abs(got - want) for got, want in zip(observed, expected))
    monotonic = all(b >= a - 1e-3 for a, b in zip(observed, observed[1:]))
    zero_scale_ok = abs(observed[0]) <= 0.02
    full_scale_ok = abs(observed[-1] - 0.90) <= 0.02
    ok = max_err <= 0.02 and monotonic and zero_scale_ok and full_scale_ok and code_mismatches == 0
    obs_text = ",".join(f"{value:.3f}" for value in observed)
    exp_text = ",".join(f"{value:.3f}" for value in expected)
    code_text = ",".join(str(code) for code in observed_codes)
    return ok, (
        f"simple_binary_dac_levels={obs_text} expected={exp_text} "
        f"observed_codes={code_text} code_mismatches={code_mismatches} "
        f"max_err={max_err:.3f} monotonic={monotonic} "
        f"zero_scale_ok={zero_scale_ok} full_scale_ok={full_scale_ok}"
    )

CHECKER_ID = "v4_015_binary_weighted_voltage_dac"
CHECKER: Checker = check_simple_binary_dac_4b
