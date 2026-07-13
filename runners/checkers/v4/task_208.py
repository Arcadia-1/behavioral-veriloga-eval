"""Task-specific checker for canonical v4 DUT 208."""
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

def _v3_edge_times(
    rows: list[dict[str, float]],
    signal: str,
    *,
    threshold: float,
    direction: int,
) -> list[float]:
    edges: list[float] = []
    for idx in range(1, len(rows)):
        prev = rows[idx - 1]
        cur = rows[idx]
        v0 = prev.get(signal)
        v1 = cur.get(signal)
        t0 = prev.get("time")
        t1 = cur.get("time")
        if v0 is None or v1 is None or t0 is None or t1 is None:
            continue
        crossed = (v0 < threshold <= v1) if direction > 0 else (v0 > threshold >= v1)
        if not crossed:
            continue
        if v1 == v0:
            edges.append(t1)
        else:
            frac = (threshold - v0) / (v1 - v0)
            edges.append(t0 + frac * (t1 - t0))
    return edges

def check_v3_dac_restore_7bit_clocked(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "vout", *{f"d{i}" for i in range(7)}}
    if not rows or not required.issubset(rows[0]):
        return False, "missing dac restore 7bit clocked signals"
    events: list[tuple[float, str]] = []
    events.extend((edge, "reset") for edge in _v3_edge_times(rows, "rst", threshold=0.45, direction=1))
    events.extend((edge, "clock") for edge in _v3_edge_times(rows, "clk", threshold=0.45, direction=1))
    events.sort(key=lambda item: item[0])
    if not any(kind == "clock" for _, kind in events):
        return False, "missing_dac_restore_clock_edges"
    out_v = 0.0
    max_err = 0.0
    checked = 0
    codes: list[int] = []
    reset_checked = False
    for event_t, kind in events:
        if kind == "reset":
            out_v = 0.0
            reset_checked = True
        else:
            rst = sample_signal_at(rows, "rst", event_t)
            if rst is None:
                return False, f"missing_rst_at={event_t * 1e9:.3f}ns"
            if rst <= 0.45:
                code = 0
                for bit in range(7):
                    value = sample_signal_at(rows, f"d{bit}", event_t)
                    if value is None:
                        return False, f"missing_d{bit}_at={event_t * 1e9:.3f}ns"
                    if value > 0.45:
                        code += 1 << bit
                out_v = (code + 0.5) * 1.8 / 128.0 - 0.9
                codes.append(code)
        sample_t = event_t + 0.20e-9
        if sample_t > rows[-1]["time"]:
            continue
        observed = sample_signal_at(rows, "vout", sample_t)
        if observed is None:
            return False, f"missing_dac_restore_output_at={sample_t * 1e9:.3f}ns"
        max_err = max(max_err, abs(observed - out_v))
        checked += 1
    if checked < 4:
        return False, f"too_few_dac_restore_checks={checked}"
    if reset_checked is False:
        return False, "missing_reset_coverage"
    if len(set(codes)) < 4 or min(codes) > 1 or max(codes) < 120:
        return False, f"insufficient_dac_restore_code_coverage={codes}"
    return max_err <= 0.014, f"checked={checked} codes={codes} max_error={max_err:.5f}"

CHECKER_ID = "v4_208_dac_restore_7bit_clocked"
CHECKER: Checker = check_v3_dac_restore_7bit_clocked
