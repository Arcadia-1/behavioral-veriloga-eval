"""Task-specific checker for canonical v4 DUT 216."""
from __future__ import annotations

from ..api import Checker
def _threshold_crossings(
    values: list[float],
    times: list[float],
    *,
    threshold: float = 0.0,
    direction: str,
) -> list[float]:
    edges: list[float] = []
    for idx in range(1, len(values)):
        v0 = values[idx - 1]
        v1 = values[idx]
        if direction == "rising":
            hit = v0 <= threshold < v1
        elif direction == "falling":
            hit = v0 >= threshold > v1
        else:
            raise ValueError(f"unsupported direction={direction!r}")
        if not hit:
            continue
        t0 = times[idx - 1]
        t1 = times[idx]
        if v1 == v0:
            edges.append(t1)
        else:
            alpha = (threshold - v0) / (v1 - v0)
            edges.append(t0 + alpha * (t1 - t0))
    return edges

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

def check_v3_sar_13bit_serial_decoder(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "din", "clks", "ready", "dout", "dnum"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing sar 13bit serial decoder signals"
    times = [row["time"] for row in rows]
    threshold = 0.55
    events: list[tuple[float, str]] = []
    events += [(t, "clks") for t in _threshold_crossings([row["clks"] for row in rows], times, threshold=threshold, direction="rising")]
    events += [(t, "ready") for t in _threshold_crossings([row["ready"] for row in rows], times, threshold=threshold, direction="rising")]
    events.sort()
    if not any(kind == "clks" for _, kind in events):
        return False, "missing_clks_publish_edge"
    if sum(1 for _, kind in events if kind == "ready") < 8:
        return False, "too_few_ready_edges"

    counter = 12
    accum = 0.0
    high_count = 0.0
    ready_checks = 0
    publish_checks = 0
    failures: list[str] = []
    for event_t, kind in events:
        if kind == "ready":
            if counter >= 0:
                bit_value = sample_signal_at(rows, "din", event_t + 1e-12)
                if bit_value is not None and bit_value > threshold:
                    accum += 2.0 ** counter
                    high_count += 1.0
                counter -= 1
                observed_count = sample_signal_at(rows, "dnum", event_t + 0.08e-9)
                if observed_count is not None:
                    ready_checks += 1
                    if abs(observed_count - high_count) > 0.15:
                        failures.append(
                            f"dnum@{event_t * 1e9:.3f}ns={observed_count:.3f} expected={high_count:.1f}"
                        )
        else:
            expected = accum / 8191.0 - 0.5
            observed = sample_signal_at(rows, "dout", event_t + 0.08e-9)
            observed_count = sample_signal_at(rows, "dnum", event_t + 0.08e-9)
            if observed is not None:
                publish_checks += 1
                if abs(observed - expected) > 0.035:
                    failures.append(
                        f"dout@{event_t * 1e9:.3f}ns={observed:.4f} expected={expected:.4f}"
                    )
            if observed_count is not None and abs(observed_count) > 0.15:
                failures.append(f"dnum_after_publish@{event_t * 1e9:.3f}ns={observed_count:.3f}")
            counter = 12
            accum = 0.0
            high_count = 0.0

    if ready_checks < 8:
        return False, f"insufficient_ready_checks={ready_checks}"
    if publish_checks < 2:
        return False, f"insufficient_publish_checks={publish_checks}"
    if failures:
        return False, " ".join(failures[:6])
    return True, f"ready_checks={ready_checks} publish_checks={publish_checks}"

CHECKER_ID = "v4_216_sar_13bit_serial_decoder"
CHECKER: Checker = check_v3_sar_13bit_serial_decoder
