"""Task-specific checker for canonical v4 DUT 338."""
from __future__ import annotations

from checkers.api import Checker
def _v4_topup_clip01(value: float, low: float = 0.0, high: float = 0.9) -> float:
    return max(low, min(high, value))

def _v4_topup_logic_high(row: dict[str, float], name: str, threshold: float = 0.45) -> bool:
    return float(row.get(name, 0.0)) > threshold

def check_v4_1036_lna_blocker_compression_detector(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1036 empty_trace"
    checked = vout_errors = metric_errors = flag_errors = clear_errors = 0
    reset_clear = disabled_clear = compressed_seen = uncompressed_seen = False
    for row in rows[::6]:
        t = float(row["time"])
        rst = _v4_topup_logic_high(row, "rst")
        enabled = _v4_topup_logic_high(row, "enable") and not rst
        if not enabled:
            clear = abs(row["vout"] - 0.45) < 0.08 and row["compression_metric"] < 0.10 and row["compressed"] < 0.10
            reset_clear = reset_clear or (rst and t < 5e-9 and clear)
            disabled_clear = disabled_clear or (t > 82e-9 and clear)
            if ((rst and t < 5e-9) or t > 82e-9) and not clear:
                clear_errors += 1
            continue
        excess = max(0.0, float(row["blocker"]) - 0.6)
        gain = 6.0 / (1.0 + excess / 0.25)
        expected_vout = _v4_topup_clip01(0.45 + gain * (float(row["vin"]) - 0.45))
        expected_metric = 0.9 * (6.0 - gain) / 6.0
        expected_flag = expected_metric > 0.1
        checked += 1
        compressed_seen = compressed_seen or expected_flag
        uncompressed_seen = uncompressed_seen or not expected_flag
        if abs(float(row["vout"]) - expected_vout) > 0.12:
            vout_errors += 1
        if abs(float(row["compression_metric"]) - expected_metric) > 0.10:
            metric_errors += 1
        if _v4_topup_logic_high(row, "compressed") != expected_flag:
            flag_errors += 1
    ok = checked >= 15 and reset_clear and disabled_clear and compressed_seen and uncompressed_seen and vout_errors <= 4 and metric_errors <= 4 and flag_errors <= 3 and clear_errors <= 3
    return ok, f"v4_1036 checked={checked} reset_clear={reset_clear} disabled_clear={disabled_clear} compressed_seen={compressed_seen} uncompressed_seen={uncompressed_seen} vout_errors={vout_errors} metric_errors={metric_errors} flag_errors={flag_errors} clear_errors={clear_errors}"

CHECKER_ID = "v4_338_lna_blocker_compression_detector"
CHECKER: Checker = check_v4_1036_lna_blocker_compression_detector
