"""Task-specific checker for canonical v4 DUT 144."""
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

def check_v3_clocked_four_input_mux(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "dsel0", "dsel1", "din0", "din1", "din2", "din3", "clks", "dout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing mux input/output signals"
    edges = _v3_edge_times(rows, "clks", threshold=0.45, direction=-1)
    if len(edges) < 4:
        return False, f"too_few_mux_clock_edges={len(edges)}"
    max_err = 0.0
    checked = 0
    selected_codes: set[int] = set()
    for edge in edges:
        dsel0 = sample_signal_at(rows, "dsel0", edge)
        dsel1 = sample_signal_at(rows, "dsel1", edge)
        if dsel0 is None or dsel1 is None:
            return False, f"missing_select_at_edge={edge * 1e9:.3f}ns"
        code = (1 if dsel0 > 0.45 else 0) + (2 if dsel1 > 0.45 else 0)
        selected_codes.add(code)
        expected = sample_signal_at(rows, f"din{code}", edge)
        if expected is None:
            return False, f"missing_din{code}_at_edge={edge * 1e9:.3f}ns"
        sample_t = edge + 1.0e-9
        if sample_t > rows[-1]["time"]:
            continue
        observed = sample_signal_at(rows, "dout", sample_t)
        if observed is None:
            return False, f"missing_dout_sample_at={sample_t * 1e9:.3f}ns"
        max_err = max(max_err, abs(observed - expected))
        checked += 1
    if checked < 4:
        return False, f"too_few_mux_output_checks={checked}"
    if len(selected_codes) < 4:
        return False, f"insufficient_mux_code_coverage={sorted(selected_codes)}"
    return max_err <= 0.035, f"checked={checked} max_error={max_err:.5f} codes={sorted(selected_codes)}"

CHECKER_ID = "v4_144_clocked_four_input_mux"
CHECKER: Checker = check_v3_clocked_four_input_mux
