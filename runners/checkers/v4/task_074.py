"""Task-specific checker for canonical v4 DUT 074."""
from __future__ import annotations

from checkers.api import Checker
def sample_signal(rows: list[dict[str, float]], signal: str, time_s: float) -> float | None:
    if not rows or signal not in rows[0] or "time" not in rows[0]:
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
    return rows[-1].get(signal)

def _crossing_times(
    rows: list[dict[str, float]],
    signal: str,
    *,
    threshold: float = 0.45,
    direction: str = "rising",
) -> list[float]:
    if not rows or "time" not in rows[0] or signal not in rows[0]:
        return []
    crossings: list[float] = []
    for idx in range(1, len(rows)):
        prev = rows[idx - 1]
        cur = rows[idx]
        t0 = prev.get("time")
        t1 = cur.get("time")
        v0 = prev.get(signal)
        v1 = cur.get(signal)
        if t0 is None or t1 is None or v0 is None or v1 is None:
            continue
        if direction == "rising":
            hit = v0 <= threshold < v1
        elif direction == "falling":
            hit = v0 >= threshold > v1
        else:
            raise ValueError(f"unsupported direction={direction!r}")
        if not hit:
            continue
        if v1 == v0:
            crossings.append(t1)
        else:
            alpha = (threshold - v0) / (v1 - v0)
            crossings.append(t0 + alpha * (t1 - t0))
    return crossings

def check_file_metric_writer(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "done"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/vin/done"

    crossings = _crossing_times(rows, "vin")
    if not crossings:
        return False, "no_vin_rising_crossing"

    cross_t = crossings[0]
    before = sample_signal(rows, "done", max(0.0, cross_t - 10e-9))
    after = sample_signal(rows, "done", cross_t + 10e-9)
    final = rows[-1].get("done")
    if before is None or after is None or final is None:
        return False, "missing_done_sample"

    done_low_before = before < 0.1
    done_high_after = after > 0.8 and final > 0.8
    extra_ok = True
    for extra_t in crossings[1:]:
        extra_done = sample_signal(rows, "done", extra_t + 5.0e-9)
        if extra_done is None or extra_done < 0.8:
            extra_ok = False
            break
    ok = done_low_before and done_high_after and extra_ok
    return ok, (
        f"crossings={len(crossings)} first_cross_t={cross_t:.3e} "
        f"done_before={before:.3f} done_after={after:.3f} "
        f"done_final={final:.3f} extra_done_high={extra_ok}"
    )

CHECKER_ID = "v4_074_crossing_metric_writer"
CHECKER: Checker = check_file_metric_writer
