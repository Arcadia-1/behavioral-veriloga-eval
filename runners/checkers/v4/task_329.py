"""Task-specific checker for canonical v4 DUT 329."""
from __future__ import annotations

from checkers.api import Checker
VCM = 0.45
VTH = 0.45

def _high(row: dict[str, float], name: str, thr: float = VTH) -> bool:
    return float(row.get(name, 0.0)) > thr

def _rising(prev: float, now: float, thr: float = VTH) -> bool:
    return now > thr and prev <= thr

def _code(row: dict[str, float], bits: list[str]) -> int:
    return sum((1 << i) for i, b in enumerate(bits) if _high(row, b))

def _missing(rows: list[dict[str, float]], required: set[str]) -> list[str]:
    if not rows:
        return sorted(required)
    return sorted(required - set(rows[0].keys()))

def check_v4_329_ctle_adaptation_loop(rows: list[dict[str, float]]) -> tuple[bool, str]:
    req = {
        "time", "vin", "edge_metric_in", "clk", "rst", "enable",
        "boost_0", "boost_1", "boost_2", "vout", "adapt_metric", "locked",
    }
    miss = _missing(rows, req)
    if miss:
        return False, f"v4_329 missing_signals={','.join(miss)}"
    prev_clk = float(rows[0]["clk"])
    prev_boost = 0
    checked = adapt_errors = vout_errors = lock_errors = clear_errors = 0
    reset_clear = disabled_clear = ever_enabled = False
    boost_codes: set[int] = set()
    streak = 0
    sample_pending = False
    pending_edge = 0.0
    prev_row = rows[0]
    for row in rows:
        t = float(row["time"])
        clk = float(row["clk"])
        rst = _high(row, "rst")
        enabled = _high(row, "enable") and not rst
        boost = _code(row, ["boost_0", "boost_1", "boost_2"])
        if not enabled:
            clear = (
                boost == 0
                and abs(float(row["vout"]) - VCM) < 0.12
                and abs(float(row["adapt_metric"])) < 0.08
                and not _high(row, "locked")
            )
            if rst and clear:
                reset_clear = True
            if ever_enabled and (not _high(row, "enable")) and clear:
                disabled_clear = True
            if (rst or (ever_enabled and not _high(row, "enable") and disabled_clear)) and not clear:
                clear_errors += 1
            streak = 0
            sample_pending = False
            prev_clk = clk
            prev_boost = 0
            prev_row = row
            continue
        ever_enabled = True
        if _rising(prev_clk, clk):
            sample_pending = t >= 8e-9
            pending_edge = float(row["edge_metric_in"])
        elif sample_pending and prev_clk > VTH and clk <= VTH:
            sample_pending = False
            checked += 1
            boost = _code(prev_row, ["boost_0", "boost_1", "boost_2"])
            boost_codes.add(boost)
            edge = pending_edge
            target = 0.55
            if edge < target - 0.03 and boost < prev_boost:
                adapt_errors += 1
            if edge > target + 0.03 and boost > prev_boost:
                adapt_errors += 1
            vin = float(prev_row["vin"])
            expected = VCM + (vin - VCM) * (1.0 + 0.08 * boost)
            if abs(float(prev_row["vout"]) - expected) > 0.12:
                vout_errors += 1
            if abs(float(prev_row["adapt_metric"]) - abs(edge - target)) > 0.08:
                adapt_errors += 1
            if abs(edge - target) <= 0.03:
                streak += 1
            else:
                streak = 0
            locked = _high(prev_row, "locked")
            if locked and streak < 3:
                lock_errors += 1
            prev_boost = boost
        prev_clk = clk
        prev_row = row
    ok = (
        checked >= 8
        and reset_clear
        and disabled_clear
        and len(boost_codes) >= 2
        and adapt_errors <= max(3, checked // 3)
        and vout_errors <= max(3, checked // 3)
        and lock_errors <= 3
        and clear_errors <= 6
    )
    return ok, (
        f"v4_329 checked={checked} boost_codes={sorted(boost_codes)} "
        f"reset_clear={reset_clear} disabled_clear={disabled_clear} "
        f"adapt_errors={adapt_errors} vout_errors={vout_errors} "
        f"lock_errors={lock_errors} clear_errors={clear_errors}"
    )

CHECKER_ID = "v4_329_ctle_adaptation_loop"
CHECKER: Checker = check_v4_329_ctle_adaptation_loop
