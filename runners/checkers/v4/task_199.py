"""Task-specific checker for canonical v4 DUT 199."""
from __future__ import annotations

from ..api import Checker
def _stable_bits_tuple(row: dict[str, float], bit_names: list[str]) -> tuple[int, ...] | None:
    bits = [_stable_voltage_bit(row, signal) for signal in bit_names]
    if any(bit is None for bit in bits):
        return None
    return tuple(int(bit) for bit in bits if bit is not None)

def check_v3_l2_7b_dac_ready(rows: list[dict[str, float]]) -> tuple[bool, str]:
    bit_names = [f"din{i}" for i in range(1, 8)]
    required = {"time", "rdy", "aout", *bit_names}
    if not rows or not required.issubset(rows[0]):
        return False, "missing l2 7b dac ready signals"
    vth = 0.45
    vdd = 0.9
    weights_by_bit = [0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0]
    total_weight = sum(weights_by_bit) + 1.0
    armed = False
    expected = 0.0
    prev_rdy = rows[0].get("rdy", 0.0)
    settle_until = 0.0
    checked = 0
    edge_count = 0
    max_err = 0.0
    for row in rows:
        t = row.get("time")
        rdy = row.get("rdy")
        if t is None or rdy is None:
            continue
        if prev_rdy is not None and prev_rdy <= vth and rdy > vth:
            edge_count += 1
            if not armed:
                armed = True
                expected = 0.0
            else:
                bits = _stable_bits_tuple(row, bit_names)
                if bits is not None:
                    switched = sum(float(bit) * weight for bit, weight in zip(bits, weights_by_bit))
                    expected = (switched / total_weight) * 2.0 * vdd - vdd
            settle_until = t + 0.08e-9
        prev_rdy = rdy
        if t < settle_until:
            continue
        err = abs(row["aout"] - expected)
        max_err = max(max_err, err)
        checked += 1
    if checked < 20 or edge_count < 3:
        return False, f"insufficient_ready_dac_rows={checked} edges={edge_count}"
    return max_err <= 0.03, f"checked={checked} ready_edges={edge_count} max_ready_dac_error={max_err:.5f}"

def _stable_voltage_bit(row: dict[str, float], signal: str) -> int | None:
    value = row.get(signal)
    if value is None:
        return None
    if value <= 0.15:
        return 0
    if value >= 0.75:
        return 1
    return None

CHECKER_ID = "v4_199_l2_7b_dac_ready"
CHECKER: Checker = check_v3_l2_7b_dac_ready
