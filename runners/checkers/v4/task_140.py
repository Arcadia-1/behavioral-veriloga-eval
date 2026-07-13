"""Task-specific checker for canonical v4 DUT 140."""
from __future__ import annotations

from checkers.api import Checker
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

def _v3_logic_stable_rows(
    rows: list[dict[str, float]],
    inputs: list[str],
    *,
    threshold: float = 0.45,
    settle_after_edge_s: float = 0.4e-9,
):
    edges: list[float] = []
    for signal in inputs:
        edges.extend(_v3_edge_times(rows, signal, threshold=threshold, direction=1))
        edges.extend(_v3_edge_times(rows, signal, threshold=threshold, direction=-1))
    for row in rows:
        if any(abs(row[signal] - threshold) <= 0.12 for signal in inputs):
            continue
        t = row["time"]
        if any(edge <= t <= edge + settle_after_edge_s for edge in edges):
            continue
        yield row

def check_v3_rs_latch_voltage(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin_s", "vin_r", "vout_q", "vout_qbar"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/vin_s/vin_r/vout_q/vout_qbar"
    q = 0
    checked = 0
    max_err = 0.0
    modes: set[str] = set()
    amplitude_mismatches = 0
    set_reset_mismatches = 0
    hold_mismatches = 0
    complement_mismatches = 0
    stable_rows = list(_v3_logic_stable_rows(rows, ["vin_s", "vin_r"]))
    stride = max(1, len(stable_rows) // 260)
    for row in stable_rows[::stride]:
        s = 1 if row["vin_s"] > 0.45 else 0
        r = 1 if row["vin_r"] > 0.45 else 0
        mode = ""
        if s and not r:
            q = 1
            mode = "set"
        elif r and not s:
            q = 0
            mode = "reset"
        elif not s and not r:
            mode = "hold_high" if q else "hold_low"
        else:
            continue
        modes.add(mode)
        q_target = 0.9 if q else 0.0
        qbar_target = 0.0 if q else 0.9
        q_error = abs(row["vout_q"] - q_target)
        qbar_error = abs(row["vout_qbar"] - qbar_target)
        sample_error = max(q_error, qbar_error)
        max_err = max(max_err, sample_error)
        amplitude_mismatches += sample_error > 0.08
        if mode in {"set", "reset"}:
            set_reset_mismatches += sample_error > 0.08
        else:
            hold_mismatches += sample_error > 0.08
        complement_mismatches += abs(row["vout_q"] + row["vout_qbar"] - 0.9) > 0.08
        checked += 1
    if checked < 20:
        return False, f"too_few_rs_latch_samples={checked}"
    required_modes = {"set", "reset", "hold_high", "hold_low"}
    if not required_modes.issubset(modes):
        return False, f"insufficient_rs_latch_modes={sorted(modes)}"
    counts = {
        "P_LOGIC_THRESHOLDS_OUTPUT_AMPLITUDE": amplitude_mismatches,
        "P_SET_RESET_PRIORITY": set_reset_mismatches,
        "P_HOLD_STATE": hold_mismatches,
        "P_QBAR_COMPLEMENT": complement_mismatches,
    }
    ok = all(count == 0 for count in counts.values())
    return ok, (
        f"checked={checked} max_error={max_err:.5f} modes={sorted(modes)}; "
        + "; ".join(
            f"{property_id} mismatch_count={count}"
            for property_id, count in counts.items()
        )
    )

CHECKER_ID = "v4_140_rs_latch_voltage"
CHECKER: Checker = check_v3_rs_latch_voltage
