"""Task-specific checker for canonical v4 DUT 147."""
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

def check_v3_control_word_encoder_7b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows or "time" not in rows[0]:
        return False, "missing encoder waveform"

    available = set(rows[0])
    groups = [
        ("", 85),
        ("_85", 85),
        ("_42", 42),
        ("_0", 0),
        ("_19", 19),
        ("_108", 108),
        ("_127", 127),
    ]
    expected_by_signal: dict[str, list[tuple[float, float]]] = {}
    covered_ctrls: list[int] = []
    for suffix, ctrl in groups:
        signals = [f"d{bit}{suffix}" for bit in range(7)]
        if not set(signals).issubset(available):
            continue
        covered_ctrls.append(ctrl)
        for bit, signal in enumerate(signals):
            expected = 0.9 if ((ctrl >> bit) & 1) else 0.0
            expected_by_signal[signal] = [(5.0, expected), (15.0, expected)]

    if not expected_by_signal:
        return False, "missing encoder output signals"

    ok, detail = _sample_many(rows, expected_by_signal, tol=0.08)
    if not ok:
        return ok, detail
    if len(set(covered_ctrls)) < 2 and set(covered_ctrls) != {85}:
        return False, f"insufficient_control_word_coverage={covered_ctrls}"
    return True, f"{detail} ctrl_values={covered_ctrls}"

CHECKER_ID = "v4_147_control_word_encoder_7b"
CHECKER: Checker = check_v3_control_word_encoder_7b
