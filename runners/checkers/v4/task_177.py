"""Task-specific checker for canonical v4 DUT 177."""
from __future__ import annotations

from ..api import Checker
from .batch18_diagnostics import bind_properties
from .stimulus_relative import normalize_affine_time
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

def check_v3_sync_8b_dffs_v2(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "ck1", "ck9", "do0", "do1", "do2", "do3", "do4", "do5", "do6", "do7", "do8"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing sync 8b dffs outputs"
    rows = normalize_affine_time(rows, [
        ("ck9", 0.45, "rising", 1.025, 0),
        ("ck1", 0.45, "rising", 9.025, 0),
    ])
    if rows is None:
        return False, "missing_phased_clock_stimulus_edges"
    return _sample_many_within_trace(
        rows,
        {
            "do0": [(9.7, 1.0), (19.7, 0.0)],
            "do1": [(9.7, 0.0), (19.7, 1.0)],
            "do2": [(9.7, 1.0), (19.7, 0.0)],
            "do3": [(9.7, 0.0), (19.7, 1.0)],
            "do4": [(9.7, 1.0), (19.7, 0.0)],
            "do5": [(9.7, 0.0), (19.7, 1.0)],
            "do6": [(9.7, 1.0), (19.7, 0.0)],
            "do7": [(9.7, 0.0), (19.7, 1.0)],
            "do8": [(9.7, 1.0), (19.7, 0.0)],
        },
        tol=0.08,
    )

CHECKER_ID = "v4_177_sync_8b_dffs_v2"
CHECKER: Checker = bind_properties(check_v3_sync_8b_dffs_v2, (
    "P_PHASED_CAPTURE_ORDER", "P_INTERMEDIATE_OUTPUT_CAPTURE",
    "P_FINAL_OUTPUT_CAPTURE", "P_FULL_LEVEL_OUTPUTS",
))
