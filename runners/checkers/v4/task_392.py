"""Task-specific checker for canonical v4 DUT 392."""
from __future__ import annotations

from checkers.api import Checker
def _v4_topup_logic_high(row: dict[str, float], name: str, threshold: float = 0.45) -> bool:
    return float(row.get(name, 0.0)) > threshold

def _v4_rising(prev_v: float, now_v: float, vth: float = 0.45) -> bool:
    return now_v > vth and prev_v <= vth

def _v4_batch001_first_after(rows: list[dict[str, float]], target_time: float) -> dict[str, float] | None:
    for row in rows:
        if float(row["time"]) >= target_time:
            return row
    return None

def check_v4_951_serializer_mux_timing_macro(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_951 empty_trace"
    prev_clk = float(rows[0].get("clk", 0.0))
    slot = 0
    frame_count = 0
    checked = serial_errors = slot_errors = valid_errors = clear_errors = 0
    reset_clear = disabled_clear = valid_seen = slot3_seen = one_seen = zero_seen = False
    for row in rows:
        t = float(row["time"])
        rst = _v4_topup_logic_high(row, "rst")
        enabled = _v4_topup_logic_high(row, "enable") and not rst
        if not enabled:
            slot = 0; frame_count = 0
            clear = row["serial_out"] < 0.10 and row["slot_0"] < 0.10 and row["slot_1"] < 0.10 and row["valid"] < 0.10
            reset_clear = reset_clear or (rst and t < 5e-9 and clear)
            disabled_clear = disabled_clear or (t > 82e-9 and clear)
            if ((rst and t < 5e-9) or t > 82e-9) and not clear:
                clear_errors += 1
            prev_clk = float(row["clk"])
            continue
        if _v4_rising(prev_clk, float(row["clk"])):
            selected_name = ["d0", "d1", "d2", "d3"][slot]
            expected_serial = _v4_topup_logic_high(row, selected_name)
            expected_s1 = slot >= 2
            expected_s0 = slot in (1, 3)
            if slot == 3:
                frame_count += 1
            expected_valid = frame_count >= 1
            slot3_seen = slot3_seen or slot == 3
            valid_seen = valid_seen or expected_valid
            one_seen = one_seen or expected_serial
            zero_seen = zero_seen or not expected_serial
            sample = _v4_batch001_first_after(rows, t + 0.7e-9)
            if sample is not None:
                checked += 1
                if _v4_topup_logic_high(sample, "serial_out") != expected_serial:
                    serial_errors += 1
                if _v4_topup_logic_high(sample, "slot_1") != expected_s1 or _v4_topup_logic_high(sample, "slot_0") != expected_s0:
                    slot_errors += 1
                if _v4_topup_logic_high(sample, "valid") != expected_valid:
                    valid_errors += 1
            slot = (slot + 1) % 4
        prev_clk = float(row["clk"])
    ok = checked >= 6 and reset_clear and disabled_clear and slot3_seen and valid_seen and one_seen and zero_seen and serial_errors <= 1 and slot_errors <= 1 and valid_errors <= 1 and clear_errors <= 12
    return ok, f"v4_951 checked={checked} reset_clear={reset_clear} disabled_clear={disabled_clear} slot3_seen={slot3_seen} valid_seen={valid_seen} one_seen={one_seen} zero_seen={zero_seen} serial_errors={serial_errors} slot_errors={slot_errors} valid_errors={valid_errors} clear_errors={clear_errors}"

CHECKER_ID = "v4_392_serializer_mux_timing_macro"
CHECKER: Checker = check_v4_951_serializer_mux_timing_macro
