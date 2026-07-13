"""Task-specific checker for canonical v4 DUT 154."""
from __future__ import annotations

from checkers.api import Checker
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

def check_v3_flash_adc_threshold_taps(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "clk", "dout0", "dout1", "dout2", "dout3", "dout4", "dout5", "dout6"}
    missing = _v3_missing_columns(rows, required)
    if missing:
        return False, missing

    edge_samples = _v3_edge_sample_times(rows, "clk", threshold=0.45)
    if len(edge_samples) < 4:
        return False, f"too_few_clk_edges={len(edge_samples)}"
    tap_indices = [1, 5, 10, 15, 20, 25, 30]
    thresholds = [-0.125 + tap * (0.25 / 31.0) for tap in tap_indices]
    max_error = 0.0
    checked = 0
    for edge_t, sample_t in edge_samples:
        vin = sample_signal_at(rows, "vin", edge_t)
        if vin is None:
            return False, f"missing_vin_at_clk={edge_t * 1e9:.3f}ns"
        for idx, threshold in enumerate(thresholds):
            observed = sample_signal_at(rows, f"dout{idx}", sample_t)
            if observed is None:
                return False, f"missing_dout{idx}_sample={sample_t * 1e9:.3f}ns"
            expected = 0.9 if vin > threshold else 0.0
            max_error = max(max_error, abs(observed - expected))
            checked += 1
    return max_error <= 0.09, f"tap_checks={checked} max_error={max_error:.5f}"

CHECKER_ID = "v4_154_flash_adc_threshold_taps"
CHECKER: Checker = check_v3_flash_adc_threshold_taps
