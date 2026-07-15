"""Task-specific checker for canonical v4 DUT 151."""
from __future__ import annotations

from ..api import Checker
def rising_edges(values: list[float], times: list[float], threshold: float = 0.45) -> list[float]:
    edges: list[float] = []
    for i in range(1, len(values)):
        if values[i - 1] < threshold <= values[i]:
            edges.append(times[i])
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

def _v3_missing_columns(rows: list[dict[str, float]], required: set[str]) -> str | None:
    if not rows:
        return "empty_waveform"
    missing = sorted(required - set(rows[0]))
    if missing:
        return "missing_columns=" + ",".join(missing)
    return None

def _v3_edge_sample_times(
    rows: list[dict[str, float]],
    signal: str,
    *,
    threshold: float = 0.45,
    delay_s: float = 1.8e-9,
) -> list[tuple[float, float]]:
    times = [row["time"] for row in rows]
    edges = rising_edges([row[signal] for row in rows], times, threshold=threshold)
    last_time = times[-1]
    return [(edge_t, edge_t + delay_s) for edge_t in edges if edge_t + delay_s <= last_time]

def check_v3_flash_8level_sum_delay(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vip", "vim", "refp", "refn", "clks", "doutsum", "doutsumdelay"}
    missing = _v3_missing_columns(rows, required)
    if missing:
        return False, missing

    edge_samples = _v3_edge_sample_times(rows, "clks", threshold=0.45)
    if len(edge_samples) < 3:
        return False, f"too_few_clock_edges={len(edge_samples)}"
    previous = 0.0
    max_sum_error = 0.0
    max_delay_error = 0.0
    checked = 0
    for edge_t, sample_t in edge_samples:
        vip = sample_signal_at(rows, "vip", edge_t)
        vim = sample_signal_at(rows, "vim", edge_t)
        refp = sample_signal_at(rows, "refp", edge_t)
        refn = sample_signal_at(rows, "refn", edge_t)
        observed_sum = sample_signal_at(rows, "doutsum", sample_t)
        observed_delay = sample_signal_at(rows, "doutsumdelay", sample_t)
        if None in (vip, vim, refp, refn, observed_sum, observed_delay):
            return False, f"missing_flash8_sample_at={edge_t * 1e9:.3f}ns"
        span = refp - refn
        thresholds = [sign * frac * span * 0.5 for sign in (-1.0, 1.0) for frac in (7.0 / 8.0, 5.0 / 8.0, 3.0 / 8.0, 1.0 / 8.0)]
        thresholds = sorted(thresholds)
        vin = vip - vim
        current = sum(1 for threshold in thresholds if vin > threshold) / 8.0
        max_sum_error = max(max_sum_error, abs(observed_sum - current))
        max_delay_error = max(max_delay_error, abs(observed_delay - previous))
        previous = current
        checked += 1
    ok = max_sum_error <= 0.035 and max_delay_error <= 0.035
    return ok, f"checked={checked} max_sum_error={max_sum_error:.5f} max_delay_error={max_delay_error:.5f}"

CHECKER_ID = "v4_151_flash_8level_sum_delay"
CHECKER: Checker = check_v3_flash_8level_sum_delay
