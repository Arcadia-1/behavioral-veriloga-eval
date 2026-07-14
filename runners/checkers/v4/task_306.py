"""Task-specific checker for canonical v4 DUT 306."""
from __future__ import annotations

from checkers.api import Checker
from checkers.common.v4_topup import (
    _v4_topup_clip01,
    _v4_topup_logic_high,
    _v4_topup_near,
    _v4_topup_span,
)

def check_v4_306_instrumentation_amplifier_offset_trim(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1004 empty_trace"
    def first_after(target_time: float) -> dict[str, float] | None:
        for candidate in rows:
            if float(candidate["time"]) >= target_time:
                return candidate
        return None

    checked = vout_errors = metric_errors = premature_ready = 0
    ready_seen = reset_clear = late_reset_clear = metric_dynamic = trim_response_seen = False
    trim_adapt = 0.0
    active_corr = 0.0
    update_count = 0
    previous = rows[0]
    for row in rows:
        if _v4_topup_logic_high(row, "rst"):
            if _v4_topup_near(row["vout"], 0.45, 0.08) and row["offset_metric"] < 0.15 and row["ready"] < 0.15:
                reset_clear = True
                late_reset_clear = late_reset_clear or row["time"] > 48e-9
    for row in rows[1:]:
        clk_rise = (not _v4_topup_logic_high(previous, "clk")) and _v4_topup_logic_high(row, "clk")
        previous = row
        if not clk_rise:
            continue
        sample = first_after(float(row["time"]) + 1.0e-9)
        if sample is None:
            continue
        if _v4_topup_logic_high(row, "rst"):
            trim_adapt = 0.0
            active_corr = 0.0
            update_count = 0
            continue
        if row["time"] < 7e-9:
            if sample["ready"] > 0.45:
                premature_ready += 1
            continue
        if not _v4_topup_logic_high(row, "cal_en"):
            continue
        code = (
            int(_v4_topup_logic_high(row, "trim_0"))
            + 2 * int(_v4_topup_logic_high(row, "trim_1"))
            + 4 * int(_v4_topup_logic_high(row, "trim_2"))
        )
        trim_static = (code - 4) * 8.0e-3
        error = float(row["vinp"]) - float(row["vinn"]) - trim_static - trim_adapt
        if error > 4.0e-3:
            trim_adapt += 8.0e-3
        elif error < -4.0e-3:
            trim_adapt -= 8.0e-3
        active_corr = trim_static + trim_adapt
        update_count += 1
        if update_count < 3 and sample["ready"] > 0.45:
            premature_ready += 1
        ready_seen = ready_seen or sample["ready"] > 0.45
        diff = float(sample["vinp"]) - float(sample["vinn"])
        expected = _v4_topup_clip01(0.45 + 8.0 * (diff - active_corr))
        expected_metric = _v4_topup_clip01(0.45 + active_corr)
        checked += 1
        if abs(float(sample["vout"]) - expected) > 0.18:
            vout_errors += 1
        if abs(float(sample["offset_metric"]) - expected_metric) > 0.035:
            metric_errors += 1
        trim_response_seen = trim_response_seen or abs(active_corr) > 0.006
    metric_dynamic = _v4_topup_span(rows, "offset_metric") > 0.03
    ok = (
        checked >= 8
        and reset_clear
        and late_reset_clear
        and ready_seen
        and metric_dynamic
        and trim_response_seen
        and premature_ready == 0
        and vout_errors == 0
        and metric_errors == 0
    )
    return ok, (
        f"v4_306 checked={checked} reset_clear={reset_clear} late_reset_clear={late_reset_clear} ready_seen={ready_seen} "
        f"metric_dynamic={metric_dynamic} trim_response={trim_response_seen} "
        f"premature_ready={premature_ready} vout_errors={vout_errors} metric_errors={metric_errors}"
    )

CHECKER_ID = "v4_306_instrumentation_amplifier_offset_trim"
CHECKER: Checker = check_v4_306_instrumentation_amplifier_offset_trim
