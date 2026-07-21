"""Task-specific checker for canonical v4 DUT 206."""
from __future__ import annotations

from ..api import Checker
from .diagnostics import with_property_diagnostics


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

def check_v3_sar_comparator_reset_high(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "cmpck", "vinn", "vinp", "dcmpn", "dcmpp"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing sar comparator reset high signals"
    edges: list[tuple[int, str]] = []
    previous = float(rows[0]["cmpck"])
    for index, row in enumerate(rows[1:], start=1):
        current = float(row["cmpck"])
        if previous <= 0.45 < current:
            edges.append((index, "rising"))
        elif previous > 0.45 >= current:
            edges.append((index, "falling"))
        previous = current
    if len(edges) < 3:
        return False, f"insufficient_cmpck_edges={len(edges)}"

    checked = errors = falling = positive = negative = equal = 0
    for edge_number, (index, direction) in enumerate(edges):
        edge = rows[index]
        edge_time = float(edge["time"])
        next_time = (
            float(rows[edges[edge_number + 1][0]]["time"])
            if edge_number + 1 < len(edges)
            else float(rows[-1]["time"])
        )
        if next_time <= edge_time:
            continue
        sample_time = edge_time + 0.2 * (next_time - edge_time)
        dcmpp = sample_signal_at(rows, "dcmpp", sample_time)
        dcmpn = sample_signal_at(rows, "dcmpn", sample_time)
        vinp = sample_signal_at(rows, "vinp", edge_time)
        vinn = sample_signal_at(rows, "vinn", edge_time)
        if None in (dcmpp, dcmpn, vinp, vinn):
            continue
        if direction == "falling":
            expected_p = expected_n = 0.9
            falling += 1
        elif vinp > vinn + 1e-3:
            expected_p, expected_n = 0.9, 0.0
            positive += 1
        elif vinp < vinn - 1e-3:
            expected_p, expected_n = 0.0, 0.9
            negative += 1
        else:
            expected_p = expected_n = 0.0
            equal += 1
        checked += 1
        if abs(dcmpp - expected_p) > 0.08 or abs(dcmpn - expected_n) > 0.08:
            errors += 1
    coverage = falling > 0 and positive > 0 and negative > 0 and equal > 0
    ok = checked >= 3 and coverage and errors == 0
    return ok, (
        f"cmpck_events={checked} errors={errors} coverage={coverage} falling={falling} "
        f"positive={positive} negative={negative} equal={equal}"
    )

CHECKER_ID = "v4_206_sar_comparator_reset_high"
CHECKER: Checker = with_property_diagnostics(
    check_v3_sar_comparator_reset_high,
    {"P_INITIALIZE_BOTH_DECISION_OUTPUTS_HIGH_WHENEVER": ("errors", "!coverage")},
)
