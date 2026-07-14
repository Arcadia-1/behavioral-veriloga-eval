"""Task-specific checker for canonical v4 DUT 057."""
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

def check_config_shift_register_64b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    serial_key = "serial_in" if rows and "serial_in" in rows[0] else "sin"
    required = {"time", "clk", "rst_n", serial_key, *{f"q{i}" for i in range(64)}}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing[:12])
    rising_edges = _rising_times(rows, "clk")
    expected = [0] * 64
    state_failures: list[str] = []
    reset_failures: list[str] = []
    level_failures: list[str] = []
    hold_failures: list[str] = []
    checked_edges = 0
    reset_edges = 0

    for edge_index, edge_t in enumerate(rising_edges):
        rst_n = sample_signal_at(rows, "rst_n", edge_t)
        serial = sample_signal_at(rows, serial_key, edge_t)
        if rst_n is None or serial is None:
            continue
        if rst_n <= 0.45:
            expected = [0] * 64
            reset_edges += 1
        else:
            expected = [1 if serial > 0.45 else 0, *expected[:63]]

        settled = _sample_after(rows, edge_t, 0.25e-9)
        checked_edges += 1
        for bit, expected_bit in enumerate(expected):
            observed = settled[f"q{bit}"]
            if 0.18 < observed < 0.72:
                level_failures.append(
                    f"shift_output_level observed=q{bit}:{observed:.3f} "
                    "expected=low<=0.18_or_high>=0.72 "
                    f"window={edge_t * 1e9:.3f}ns"
                )
            if (observed > 0.45) != bool(expected_bit):
                target = reset_failures if rst_n <= 0.45 else state_failures
                label = "shift_reset" if rst_n <= 0.45 else "shift_state"
                target.append(
                    f"{label} observed=q{bit}:{observed:.3f} expected={expected_bit} "
                    f"window={edge_t * 1e9:.3f}ns edge={edge_index}"
                )

        if edge_index + 1 < len(rising_edges):
            next_edge_t = rising_edges[edge_index + 1]
            hold_start_t = edge_t + 0.35e-9
            hold_end_t = next_edge_t - 0.35e-9
            if hold_end_t > hold_start_t:
                hold_start = min(rows, key=lambda row: abs(row["time"] - hold_start_t))
                hold_end = min(rows, key=lambda row: abs(row["time"] - hold_end_t))
                for bit in range(64):
                    before = hold_start[f"q{bit}"]
                    after = hold_end[f"q{bit}"]
                    if abs(after - before) > 0.18:
                        hold_failures.append(
                            f"shift_hold observed=q{bit}:{before:.3f}->{after:.3f} expected=held "
                            f"window={hold_start_t * 1e9:.3f}-{hold_end_t * 1e9:.3f}ns"
                        )

    failures = reset_failures or level_failures or hold_failures or state_failures
    if failures:
        return False, " ".join(failures[:5])
    if checked_edges < 8:
        return False, f"shift_edges observed={checked_edges} expected>=8 window=full_trace"
    return True, (
        f"shift_contract_pass checked_edges={checked_edges} reset_edges={reset_edges} "
        f"hold_windows={max(0, checked_edges - 1)}"
    )

def _rising_times(rows: list[dict[str, float]], col: str, vth: float = 0.45) -> list[float]:
    times: list[float] = []
    last = rows[0][col] > vth
    for row in rows[1:]:
        cur = row[col] > vth
        if not last and cur:
            times.append(row["time"])
        last = cur
    return times

def _sample_after(rows: list[dict[str, float]], t: float, delay: float = 5e-9) -> dict[str, float]:
    target = t + delay
    return min(rows, key=lambda row: abs(row["time"] - target))

CHECKER_ID = "v4_057_config_shift_register_64b"
CHECKER: Checker = check_config_shift_register_64b
