"""Task-specific checker for canonical v4 DUT 163."""
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

def _v3_logic_at(rows: list[dict[str, float]], signal: str, time_s: float, threshold: float = 0.45) -> int | None:
    value = sample_signal_at(rows, signal, time_s)
    if value is None:
        return None
    return 1 if value > threshold else 0

def check_v3_cyclic_decoder_10b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "dp", "dn", "ready", "clks", "dout"}
    missing = _v3_missing_columns(rows, required)
    if missing:
        return False, missing

    clk_edges = _v3_edge_sample_times(rows, "clks", threshold=0.55)
    ready_edges = [edge_t for edge_t, _ in _v3_edge_sample_times(rows, "ready", threshold=0.55, delay_s=0.0)]
    events = [(edge_t, "clk") for edge_t, _ in clk_edges] + [(edge_t, "ready") for edge_t in ready_edges]
    events.sort()

    nbit = 10
    counter = nbit - 1
    total = 0.0
    expected_samples: list[tuple[float, float]] = []
    half_weight_seen = False
    for event_t, event_kind in events:
        if event_kind == "ready":
            dp = _v3_logic_at(rows, "dp", event_t, threshold=0.55)
            dn = _v3_logic_at(rows, "dn", event_t, threshold=0.55)
            if dp is None or dn is None:
                return False, f"missing_cyclic_decision_at={event_t * 1e9:.3f}ns"
            if counter >= 0:
                if dp:
                    total += 2.0 ** counter
                elif dn:
                    total += 0.5 * (2.0 ** counter)
                    half_weight_seen = True
            counter -= 1
            continue
        sample_t = event_t + 1.8e-9
        if sample_t <= rows[-1]["time"]:
            expected_samples.append((sample_t, total / (2.0 ** nbit - 1.0) - 0.5))
        counter = nbit - 1
        total = 0.0

    if len(expected_samples) < 2:
        return False, f"too_few_cyclic_publication_samples={len(expected_samples)}"
    max_error = 0.0
    for sample_t, expected in expected_samples:
        observed = sample_signal_at(rows, "dout", sample_t)
        if observed is None:
            return False, f"missing_cyclic_dout_sample={sample_t * 1e9:.3f}ns"
        max_error = max(max_error, abs(observed - expected))
    ok = max_error <= 0.025 and half_weight_seen
    return ok, f"published={len(expected_samples)} half_weight_seen={half_weight_seen} max_error={max_error:.5f}"

CHECKER_ID = "v4_163_cyclic_decoder_10b"
CHECKER: Checker = check_v3_cyclic_decoder_10b
