"""Task-specific checker for canonical v4 DUT 308."""
from __future__ import annotations

from ..api import Checker
from ..common.v4_topup import (
    _v4_topup_clip01,
    _v4_topup_logic_high,
    _v4_topup_near,
    _v4_topup_span,
)
from ..common.relative_events import active_start, first_rising_after, latest_assertion, sample_after_event

def check_v4_308_correlated_double_sampler_offset_cancel(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1006 empty_trace"
    reset_clear = any(
        _v4_topup_logic_high(row, "rst")
        and _v4_topup_near(row["vout"], 0.45, 0.08)
        and row["offset_dbg"] < 0.15
        and row["valid"] < 0.15
        for row in rows
    )
    late_reset = latest_assertion(rows, "rst")
    late_reset_clear = any(
        late_reset is not None and row["time"] >= late_reset
        and _v4_topup_logic_high(row, "rst")
        and _v4_topup_near(row["vout"], 0.45, 0.08)
        and row["offset_dbg"] < 0.15
        and row["valid"] < 0.15
        for row in rows
    )
    first_signal_sample = first_rising_after(rows, "sample_signal")
    premature_valid = sum(
        1 for row in rows
        if first_signal_sample is not None
        and row["time"] < first_signal_sample
        and row["valid"] > 0.45
    )
    activation = active_start(rows, reset="rst")
    checked = vout_errors = offset_errors = 0
    polarity_pos = polarity_neg = False
    previous = rows[0]
    for row in rows[1:]:
        clk_rise = (not _v4_topup_logic_high(previous, "clk")) and _v4_topup_logic_high(row, "clk")
        previous = row
        if (
            not clk_rise
            or row["time"] < activation
            or _v4_topup_logic_high(row, "rst")
            or not _v4_topup_logic_high(row, "sample_signal")
        ):
            continue
        sample = sample_after_event(rows, float(row["time"]), clock_signal="clk")
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
    diagnostics = {
        "P_ON_RESET_CLEAR_RESET_SAMPLE_SIGNAL": int(not reset_clear or not late_reset_clear),
        "P_ON_A_RISING_CLK_EDGE_WITH": int(checked < 2 or vout_errors),
        "P_ON_A_LATER_RISING_CLK_EDGE": int(offset_errors),
        "P_DRIVE_VOUT_AS_VCM_PLUS_THE": int(vout_errors),
        "P_EXPOSE_THE_RESET_SAMPLE_ON_OFFSET": int(_v4_topup_span(rows, "offset_dbg") <= 0.12),
        "P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE": 0,
    }
    return ok, (
        f"v4_308 checked={checked} reset_clear={reset_clear} late_reset_clear={late_reset_clear} premature_valid={premature_valid} "
        f"polarity_pos={polarity_pos} polarity_neg={polarity_neg} vout_errors={vout_errors} "
        f"offset_errors={offset_errors} offset_span={_v4_topup_span(rows, 'offset_dbg'):.3f} "
        f"vout_span={_v4_topup_span(rows, 'vout'):.3f}; "
        + "; ".join(f"{key} mismatch_count={value}" for key, value in diagnostics.items())
    )

CHECKER_ID = "v4_308_correlated_double_sampler_offset_cancel"
CHECKER: Checker = check_v4_308_correlated_double_sampler_offset_cancel
