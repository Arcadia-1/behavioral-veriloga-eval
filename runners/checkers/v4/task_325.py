"""Task-specific checker for canonical v4 DUT 325."""
from __future__ import annotations

from ..api import Checker
VDD = 0.9
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

def check_v4_325_fine_coarse_tdc_encoder(rows: list[dict[str, float]]) -> tuple[bool, str]:
    req = {
        "time", "start", "stop", "ref_clk", "rst", "enable",
        "coarse_0", "coarse_1", "coarse_2", "coarse_3", "fine_metric", "valid",
    }
    miss = _missing(rows, req)
    if miss:
        return False, f"v4_325 missing_signals={','.join(miss)}"
    prev_start = float(rows[0]["start"])
    prev_stop = float(rows[0]["stop"])
    prev_ref = float(rows[0]["ref_clk"])
    armed = awaiting_result = False
    ref_edges = 0
    last_ref_time = previous_ref_time = 0.0
    expected_coarse = 0
    expected_fine = 0.0
    checked = latch_errors = fine_errors = clear_errors = valid_errors = 0
    reset_clear = disabled_clear = False
    ever_enabled = False
    coarse_seen: set[int] = set()
    fine_max = 0.0
    valid_edges = 0
    for row in rows:
        t = float(row["time"])
        start = float(row["start"])
        stop = float(row["stop"])
        ref = float(row["ref_clk"])
        rst = _high(row, "rst")
        enabled = _high(row, "enable") and not rst
        coarse = _code(row, ["coarse_0", "coarse_1", "coarse_2", "coarse_3"])
        fine = float(row["fine_metric"])
        valid = _high(row, "valid")
        if not enabled:
            clear = coarse == 0 and abs(fine) < 0.08 and not valid
            if rst and clear:
                reset_clear = True
            if ever_enabled and (not _high(row, "enable")) and clear:
                disabled_clear = True
            if (rst or (ever_enabled and not _high(row, "enable") and disabled_clear)) and not clear:
                clear_errors += 1
            armed = False
            awaiting_result = False
            ref_edges = 0
            prev_start, prev_stop, prev_ref = start, stop, ref
            continue
        ever_enabled = True
        if _rising(prev_start, start):
            armed = True
            awaiting_result = False
            ref_edges = 0
            last_ref_time = previous_ref_time = 0.0
        if armed and _rising(prev_ref, ref):
            ref_edges += 1
            previous_ref_time = last_ref_time
            last_ref_time = t
        if armed and _rising(prev_stop, stop):
            expected_coarse = min(ref_edges, 15)
            if previous_ref_time > 0.0 and last_ref_time > previous_ref_time:
                expected_fine = VDD * min(1.0, max(0.0, (t - last_ref_time) / (last_ref_time - previous_ref_time)))
            else:
                expected_fine = 0.0
            awaiting_result = True
            armed = False
        if armed and not _high(row, "start") and valid:
            valid_errors += 1
        if awaiting_result and float(row["valid"]) > 0.8:
            awaiting_result = False
            checked += 1
            coarse_seen.add(coarse)
            fine_max = max(fine_max, fine)
            if coarse != expected_coarse:
                latch_errors += 1
            if abs(fine - expected_fine) > 0.12:
                fine_errors += 1
            valid_edges += 1
        prev_start, prev_stop, prev_ref = start, stop, ref
    ok = (
        checked >= 3
        and reset_clear
        and disabled_clear
        and valid_edges >= 3
        and len(coarse_seen) >= 2
        and fine_max > 0.05
        and latch_errors <= 1
        and fine_errors <= 1
        and valid_errors <= 1
    )
    clear_mismatches = int(not reset_clear) + int(not disabled_clear)
    return ok, (
        f"v4_325 checked={checked} ref_edges_last={ref_edges} coarse={sorted(coarse_seen)} "
        f"fine_max={fine_max:.3f} valid_edges={valid_edges} reset_clear={reset_clear} "
        f"disabled_clear={disabled_clear} latch_errors={latch_errors} "
        f"fine_errors={fine_errors} valid_errors={valid_errors} clear_errors={clear_errors}; "
        f"P_ON_RESET_OR_WHEN_DISABLED_CLEAR mismatch_count={clear_mismatches}; "
        f"P_A_RISING_START_EDGE_ARMS_A mismatch_count={int(checked < 3)}; "
        f"P_COUNT_RISING_REF_CLK_EDGES_UNTIL mismatch_count={latch_errors}; "
        f"P_LATCH_THE_COARSE_COUNT_INTO_COARSE mismatch_count={latch_errors + fine_errors}; "
        f"P_ASSERT_VALID_ONLY_AFTER_THE_STOP mismatch_count={valid_errors}"
    )

CHECKER_ID = "v4_325_fine_coarse_tdc_encoder"
CHECKER: Checker = check_v4_325_fine_coarse_tdc_encoder
