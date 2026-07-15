"""Task-specific checker for canonical v4 DUT 308."""
from __future__ import annotations

from ..api import Checker
from ..common.v4_topup import (
    _v4_topup_clip01,
    _v4_topup_logic_high,
    _v4_topup_near,
    _v4_topup_span,
)

def check_v4_308_correlated_double_sampler_offset_cancel(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1006 empty_trace"
    def first_after(target_time: float) -> dict[str, float] | None:
        for candidate in rows:
            if float(candidate["time"]) >= target_time:
                return candidate
        return None

    reset_clear = any(
        _v4_topup_logic_high(row, "rst")
        and _v4_topup_near(row["vout"], 0.45, 0.08)
        and row["offset_dbg"] < 0.15
        and row["valid"] < 0.15
        for row in rows
    )
    late_reset_clear = any(
        row["time"] > 50e-9
        and _v4_topup_logic_high(row, "rst")
        and _v4_topup_near(row["vout"], 0.45, 0.08)
        and row["offset_dbg"] < 0.15
        and row["valid"] < 0.15
        for row in rows
    )
    premature_valid = sum(
        1
        for row in rows
        if 3e-9 < row["time"] < 11e-9 and row["valid"] > 0.45
    )
    checked = vout_errors = offset_errors = 0
    polarity_pos = polarity_neg = False
    previous = rows[0]
    for row in rows[1:]:
        clk_rise = (not _v4_topup_logic_high(previous, "clk")) and _v4_topup_logic_high(row, "clk")
        previous = row
        if (
            not clk_rise
            or row["time"] < 12e-9
            or _v4_topup_logic_high(row, "rst")
            or not _v4_topup_logic_high(row, "sample_signal")
        ):
            continue
        sample = first_after(float(row["time"]) + 1.0e-9)
        if sample is None or sample["valid"] <= 0.45:
            continue
        expected = _v4_topup_clip01(0.45 + float(row["vin"]) - float(sample["offset_dbg"]))
        checked += 1
        polarity_pos = polarity_pos or float(row["vin"]) > float(sample["offset_dbg"]) + 0.04
        polarity_neg = polarity_neg or float(row["vin"]) < float(sample["offset_dbg"]) - 0.04
        if abs(float(sample["vout"]) - expected) > 0.13:
            vout_errors += 1
        if not (0.18 <= float(sample["offset_dbg"]) <= 0.78):
            offset_errors += 1
    ok = (
        reset_clear
        and late_reset_clear
        and checked >= 2
        and premature_valid <= 3
        and polarity_pos
        and polarity_neg
        and _v4_topup_span(rows, "offset_dbg") > 0.12
        and _v4_topup_span(rows, "vout") > 0.12
        and vout_errors == 0
        and offset_errors <= max(4, checked // 20)
    )
    return ok, (
        f"v4_308 checked={checked} reset_clear={reset_clear} late_reset_clear={late_reset_clear} premature_valid={premature_valid} "
        f"polarity_pos={polarity_pos} polarity_neg={polarity_neg} vout_errors={vout_errors} "
        f"offset_errors={offset_errors} offset_span={_v4_topup_span(rows, 'offset_dbg'):.3f} "
        f"vout_span={_v4_topup_span(rows, 'vout'):.3f}"
    )

CHECKER_ID = "v4_308_correlated_double_sampler_offset_cancel"
CHECKER: Checker = check_v4_308_correlated_double_sampler_offset_cancel
