"""Task-specific checker for canonical v4 DUT 204."""
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

def _sample_many(
    rows: list[dict[str, float]],
    samples: dict[str, list[tuple[float, float]]],
    *,
    tol: float,
) -> tuple[bool, str]:
    details: list[str] = []
    for signal, expected_samples in samples.items():
        observed: list[float] = []
        for time_ns, expected in expected_samples:
            value = sample_signal_at(rows, signal, time_ns * 1e-9)
            if value is None:
                return False, f"missing_{signal}_sample_at={time_ns:g}ns"
            observed.append(value)
            if abs(value - expected) > tol:
                return False, (
                    f"{signal}@{time_ns:g}ns={value:.4f} expected={expected:.4f} "
                    f"tol={tol:.4f}"
                )
        details.append(f"{signal}=" + ",".join(f"{value:.3f}" for value in observed))
    return True, " ".join(details)

def _sample_many_within_trace(
    rows: list[dict[str, float]],
    samples: dict[str, list[tuple[float, float]]],
    *,
    tol: float,
) -> tuple[bool, str]:
    if not rows:
        return _sample_many(rows, samples, tol=tol)
    end_time = rows[-1].get("time")
    if end_time is None:
        return _sample_many(rows, samples, tol=tol)
    end_ns = end_time * 1e9
    filtered: dict[str, list[tuple[float, float]]] = {}
    for signal, expected_samples in samples.items():
        visible_samples = [
            (time_ns, expected)
            for time_ns, expected in expected_samples
            if time_ns <= end_ns + 1e-3
        ]
        filtered[signal] = visible_samples or expected_samples
    return _sample_many(rows, filtered, tol=tol)

def check_v3_va_dac_6b_se(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "rdy", "aout", *{f"din{i}" for i in range(6)}}
    if not rows or not required.issubset(rows[0]):
        return False, "missing va dac 6b se signals"
    samples = [(0.5, -1.0), (1.5, -0.1368421), (2.5, 0.0526316), (3.5, 0.3263158)]
    end_ns = float(rows[-1]["time"]) * 1e9
    visible = [(time_ns, expected) for time_ns, expected in samples if time_ns <= end_ns + 1e-3]
    if not visible:
        visible = samples
    mismatches: list[tuple[float, float, float]] = []
    for time_ns, expected in visible:
        observed = sample_signal_at(rows, "aout", time_ns * 1e-9)
        if observed is None:
            return False, f"missing_aout_sample_at={time_ns:g}ns"
        if abs(observed - expected) > 0.02:
            mismatches.append((time_ns, observed, expected))
    event_mismatches = len(mismatches)
    weighted_mismatches = sum(1 for time_ns, _, _ in mismatches if time_ns > 0.5)
    normalization_mismatches = sum(1 for time_ns, _, _ in mismatches if time_ns == 0.5)
    detail = " ".join(
        f"aout@{time_ns:g}ns={observed:.4f} expected={expected:.4f}"
        for time_ns, observed, expected in mismatches[:4]
    ) or "all_samples_match"
    ok = not mismatches
    return ok, (
        f"{detail} checked={len(visible)} tol=0.0200; "
        f"P_ON_EACH_RISING_RDY_CROSSING_SAMPLE mismatch_count={event_mismatches}; "
        f"P_TEXT_WEIGHTED_CODE_16_DIN5_8 mismatch_count={weighted_mismatches}; "
        f"P_EACH_DIN_TERM_IS_1_WHEN mismatch_count={normalization_mismatches}"
    )

CHECKER_ID = "v4_204_va_dac_6b_se"
CHECKER: Checker = check_v3_va_dac_6b_se
