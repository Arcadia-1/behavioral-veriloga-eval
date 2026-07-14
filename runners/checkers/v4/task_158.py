"""Task-specific checker for canonical v4 DUT 158."""
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

def _v3_logic_at(rows: list[dict[str, float]], signal: str, time_s: float, threshold: float = 0.45) -> int | None:
    value = sample_signal_at(rows, signal, time_s)
    if value is None:
        return None
    return 1 if value > threshold else 0

def check_v3_ref_flash_8level_decoder(rows: list[dict[str, float]]) -> tuple[bool, str]:
    tap_names = [f"dt{idx}" for idx in range(8)]
    required = {"time", "vin", "clks", "dout", "vres", *tap_names}
    missing = _v3_missing_columns(rows, required)
    if missing:
        return False, missing

    edge_samples = _v3_edge_sample_times(rows, "clks", threshold=0.45)
    if len(edge_samples) < 3:
        return False, f"too_few_clks_edges={len(edge_samples)}"
    max_dout_error = 0.0
    max_res_error = 0.0
    checked = 0
    for edge_t, sample_t in edge_samples:
        tap_bits = [_v3_logic_at(rows, name, edge_t, threshold=0.45) for name in tap_names]
        vin = sample_signal_at(rows, "vin", edge_t)
        observed_dout = sample_signal_at(rows, "dout", sample_t)
        observed_vres = sample_signal_at(rows, "vres", sample_t)
        if vin is None or observed_dout is None or observed_vres is None or any(bit is None for bit in tap_bits):
            return False, f"missing_ref_flash_sample={edge_t * 1e9:.3f}ns"
        count = float(sum(tap_bits))
        expected_dout = count / 8.0
        expected_vres = vin - (count - 4.0) / 8.0
        max_dout_error = max(max_dout_error, abs(observed_dout - expected_dout))
        max_res_error = max(max_res_error, abs(observed_vres - expected_vres))
        checked += 1
    ok = max_dout_error <= 0.035 and max_res_error <= 0.035
    return ok, f"checked={checked} max_dout_error={max_dout_error:.5f} max_res_error={max_res_error:.5f}"

CHECKER_ID = "v4_158_ref_flash_8level_decoder"
CHECKER: Checker = check_v3_ref_flash_8level_decoder
