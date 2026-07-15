"""Task-specific checker for canonical v4 DUT 393."""
from __future__ import annotations

from ..api import Checker
def _v4_topup_logic_high(row: dict[str, float], name: str, threshold: float = 0.45) -> bool:
    return float(row.get(name, 0.0)) > threshold

def _v4_rising(prev_v: float, now_v: float, vth: float = 0.45) -> bool:
    return now_v > vth and prev_v <= vth

def _v4_batch001_first_after(rows: list[dict[str, float]], target_time: float) -> dict[str, float] | None:
    for row in rows:
        if float(row["time"]) >= target_time:
            return row
    return None

def check_v4_952_deserializer_demux_alignment_macro(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_952 empty_trace"
    prev_clk = float(rows[0].get("clk", 0.0))
    prev_align = float(rows[0].get("align_pulse", 0.0))
    slot = 0
    updated = 0
    outs = [0.0, 0.0, 0.0, 0.0]
    checked = out_errors = metric_errors = valid_errors = clear_errors = 0
    reset_clear = disabled_clear = align_seen = valid_seen = one_seen = zero_seen = False
    for row in rows:
        t = float(row["time"])
        rst = _v4_topup_logic_high(row, "rst")
        enabled = _v4_topup_logic_high(row, "enable") and not rst
        if not enabled:
            slot = 0; updated = 0; outs = [0.0, 0.0, 0.0, 0.0]
            clear = all(row[f"out{i}"] < 0.10 for i in range(4)) and row["phase_metric"] < 0.10 and row["word_valid"] < 0.10
            reset_clear = reset_clear or (rst and t < 5e-9 and clear)
            disabled_clear = disabled_clear or (t > 82e-9 and clear)
            if ((rst and t < 5e-9) or t > 82e-9) and not clear:
                clear_errors += 1
            prev_clk = float(row["clk"]); prev_align = float(row["align_pulse"])
            continue
        if _v4_rising(prev_align, float(row["align_pulse"])):
            slot = 0; updated = 0; align_seen = True
        if _v4_rising(prev_clk, float(row["clk"])):
            bit_v = 0.9 if _v4_topup_logic_high(row, "serial_in") else 0.0
            outs[slot] = bit_v
            expected_metric = 0.9 * slot / 3.0
            slot = (slot + 1) % 4
            updated = min(4, updated + 1)
            expected_valid = updated >= 4
            valid_seen = valid_seen or expected_valid
            one_seen = one_seen or bit_v > 0.45
            zero_seen = zero_seen or bit_v < 0.45
            sample = _v4_batch001_first_after(rows, t + 0.7e-9)
            if sample is not None:
                checked += 1
                for idx, expected in enumerate(outs):
                    if abs(float(sample[f"out{idx}"]) - expected) > 0.10:
                        out_errors += 1
                        break
                if abs(float(sample["phase_metric"]) - expected_metric) > 0.12:
                    metric_errors += 1
                if _v4_topup_logic_high(sample, "word_valid") != expected_valid:
                    valid_errors += 1
        prev_clk = float(row["clk"]); prev_align = float(row["align_pulse"])
    ok = checked >= 6 and reset_clear and disabled_clear and align_seen and valid_seen and one_seen and zero_seen and out_errors <= 2 and metric_errors <= 2 and valid_errors <= 1 and clear_errors <= 12
    return ok, f"v4_952 checked={checked} reset_clear={reset_clear} disabled_clear={disabled_clear} align_seen={align_seen} valid_seen={valid_seen} one_seen={one_seen} zero_seen={zero_seen} out_errors={out_errors} metric_errors={metric_errors} valid_errors={valid_errors} clear_errors={clear_errors}"

CHECKER_ID = "v4_393_deserializer_demux_alignment_macro"
CHECKER: Checker = check_v4_952_deserializer_demux_alignment_macro
