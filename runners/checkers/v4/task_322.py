"""Task-specific checker for canonical v4 DUT 322."""
from __future__ import annotations

from ..api import Checker
def _v4_topup_logic_high(row: dict[str, float], name: str, threshold: float = 0.45) -> bool:
    return float(row.get(name, 0.0)) > threshold

def _v4_rising(prev_v: float, now_v: float, vth: float = 0.45) -> bool:
    return now_v > vth and prev_v <= vth

def check_v4_1020_glitchless_clock_mux_selector(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1020 empty_trace"
    active = 0
    pending = 0
    switched_at = -1.0
    first_edge_seen = False
    checked = out_errors = glitch_errors = metric_errors = valid_errors = clear_errors = 0
    reset_clear = disabled_clear = switch_seen = both_sources_seen = False
    ever_enabled = False
    src_seen: set[int] = set()
    prev_clk_a = float(rows[0].get("clk_a", 0.0))
    prev_clk_b = float(rows[0].get("clk_b", 0.0))
    last_input_rise = -1.0
    prev_out = float(rows[0].get("clk_out", 0.0))
    switch_windows: list[dict[str, float | bool]] = []
    for row in rows:
        t = float(row["time"])
        rst = _v4_topup_logic_high(row, "rst")
        clk_a = float(row["clk_a"])
        clk_b = float(row["clk_b"])
        enabled = _v4_topup_logic_high(row, "enable") and not rst
        if not enabled:
            active = 0
            pending = 0
            first_edge_seen = False
            clear = abs(float(row["clk_out"])) < 0.08 and abs(float(row["switch_metric"])) < 0.08 and not _v4_topup_logic_high(row, "valid")
            disabled = ever_enabled and not _v4_topup_logic_high(row, "enable")
            if rst and clear:
                reset_clear = True
            if disabled and clear:
                disabled_clear = True
            if ((rst and reset_clear) or (disabled and disabled_clear)) and not clear:
                clear_errors += 1
            prev_out = float(row.get("clk_out", 0.0))
            prev_clk_a = clk_a
            prev_clk_b = clk_b
            continue
        ever_enabled = True
        pending = 1 if _v4_topup_logic_high(row, "sel") else 0
        both_low = float(row["clk_a"]) <= 0.45 and float(row["clk_b"]) <= 0.45
        if pending != active and both_low:
            active = pending
            switched_at = t
            switch_seen = True
            first_edge_seen = False
            switch_windows.append({"start": t + 0.5e-9, "end": t + 4.5e-9, "seen": False})
        expected = float(row["clk_b" if active else "clk_a"])
        src_seen.add(active)
        now_out = float(row["clk_out"])
        if _v4_rising(prev_clk_a, clk_a) or _v4_rising(prev_clk_b, clk_b):
            last_input_rise = t
        if prev_out <= 0.45 and now_out > 0.45:
            if last_input_rise < 0 or t - last_input_rise > 0.5e-9:
                glitch_errors += 1
            first_edge_seen = True
        prev_out = now_out
        prev_clk_a = clk_a
        prev_clk_b = clk_b
        metric_high = _v4_topup_logic_high(row, "switch_metric")
        for window in switch_windows:
            if bool(window["seen"]):
                continue
            if float(window["start"]) <= t <= float(window["end"]) and metric_high:
                window["seen"] = True
        if not first_edge_seen or (switched_at >= 0 and t < switched_at + 0.7e-9):
            continue
        checked += 1
        if abs(now_out - expected) > 0.14:
            out_errors += 1
        valid_high = _v4_topup_logic_high(row, "valid")
        if first_edge_seen and not valid_high:
            valid_errors += 1
        if not first_edge_seen and valid_high:
            valid_errors += 1
    both_sources_seen = len(src_seen) >= 2
    metric_errors = sum(not bool(window["seen"]) for window in switch_windows)
    out_budget = max(12, checked // 5)
    # Count one missing event once; dense waveform sampling must not dilute it.
    metric_budget = 0
    valid_budget = max(8, checked // 10)
    clear_budget = 4
    ok = (
        checked >= 80
        and reset_clear
        and disabled_clear
        and switch_seen
        and both_sources_seen
        and out_errors <= out_budget
        and glitch_errors == 0
        and metric_errors == 0
        and valid_errors <= valid_budget
        and clear_errors <= clear_budget
    )
    return ok, (
        f"v4_1020 checked={checked} sources={sorted(src_seen)} reset_clear={reset_clear} "
        f"disabled_clear={disabled_clear} switch_seen={switch_seen} out_errors={out_errors} glitch_errors={glitch_errors} "
        f"metric_errors={metric_errors} valid_errors={valid_errors} clear_errors={clear_errors}; "
        f"P_ON_RESET_OR_WHEN_DISABLED_DRIVE mismatch_count={max(0, clear_errors - clear_budget) + int(not reset_clear) + int(not disabled_clear)}; "
        f"P_ROUTE_CLK_A_WHEN_SEL_IS mismatch_count={max(0, out_errors - out_budget) + int(not both_sources_seen)}; "
        f"P_WHEN_SEL_CHANGES_WAIT_UNTIL_BOTH mismatch_count={glitch_errors + int(not switch_seen)}; "
        f"P_EXPOSE_A_SWITCH_EVENT_ON_SWITCH mismatch_count={max(0, metric_errors - metric_budget) + int(not switch_seen)}; "
        f"P_ASSERT_VALID_AFTER_THE_SELECTED_SOURCE mismatch_count={max(0, valid_errors - valid_budget)}"
    )

CHECKER_ID = "v4_322_glitchless_clock_mux_selector"
CHECKER: Checker = check_v4_1020_glitchless_clock_mux_selector
