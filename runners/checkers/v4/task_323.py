"""Task-specific checker for canonical v4 DUT 323."""
from __future__ import annotations

from checkers.api import Checker
def _v4_topup_logic_high(row: dict[str, float], name: str, threshold: float = 0.45) -> bool:
    return float(row.get(name, 0.0)) > threshold

def _v4_code_from_bits(row: dict[str, float], bits: list[str]) -> int:
    return sum((1 << idx) for idx, bit in enumerate(bits) if _v4_topup_logic_high(row, bit))

def _v4_rising(prev_v: float, now_v: float, vth: float = 0.45) -> bool:
    return now_v > vth and prev_v <= vth

def check_v4_1021_programmable_clock_skew_aligner(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1021 empty_trace"
    prev_clk_in = float(rows[0].get("clk_in", 0.0))
    prev_clk_out = float(rows[0].get("clk_out", 0.0))
    expected_metric = 0.0
    checked = metric_errors = timing_errors = valid_errors = clear_errors = 0
    input_edges = output_edges = 0
    reset_clear = disabled_clear = valid_seen = False
    codes_seen: set[int] = set()
    pending_edges: list[tuple[float, int]] = []
    for row in rows:
        t = float(row["time"])
        clk_in = float(row["clk_in"])
        clk_out = float(row["clk_out"])
        rst = _v4_topup_logic_high(row, "rst")
        enabled = _v4_topup_logic_high(row, "enable") and not rst
        if not enabled:
            pending_edges.clear()
            clear = abs(float(row["clk_out"])) < 0.08 and abs(float(row["delay_metric"])) < 0.08 and not _v4_topup_logic_high(row, "valid")
            if rst and t < 5e-9 and clear:
                reset_clear = True
            if t > 82e-9 and not _v4_topup_logic_high(row, "enable") and clear:
                disabled_clear = True
            if ((rst and t < 5e-9) or t > 82e-9) and not clear:
                clear_errors += 1
            prev_clk_in = clk_in
            prev_clk_out = clk_out
            continue
        code = _v4_code_from_bits(row, ["skew_0", "skew_1", "skew_2"])
        if _v4_rising(prev_clk_in, clk_in):
            input_edges += 1
            codes_seen.add(code)
            expected_metric = 0.1 * code
            pending_edges.append((t, code))
        if _v4_rising(prev_clk_out, clk_out):
            output_edges += 1
            valid_seen = True
            if pending_edges:
                input_time, edge_code = pending_edges.pop(0)
                expected_delay = 0.2e-9 * edge_code
                if abs((t - input_time) - expected_delay) > 0.36e-9:
                    timing_errors += 1
            else:
                timing_errors += 1
        prev_clk_in = clk_in
        prev_clk_out = clk_out
        if t < 8e-9:
            continue
        checked += 1
        if abs(float(row["delay_metric"]) - expected_metric) > 0.06:
            metric_errors += 1
        if output_edges > 0 and not _v4_topup_logic_high(row, "valid"):
            valid_errors += 1
    metric_budget = max(6, checked // 20)
    valid_budget = 4
    clear_budget = 4
    ok = (
        checked >= 40
        and len(codes_seen) >= 4
        and input_edges >= 5
        and output_edges >= max(3, input_edges - 2)
        and reset_clear
        and disabled_clear
        and valid_seen
        and timing_errors == 0
        and metric_errors <= metric_budget
        and valid_errors <= valid_budget
        and clear_errors <= clear_budget
    )
    return ok, (
        f"v4_1021 checked={checked} codes={sorted(codes_seen)} input_edges={input_edges} "
        f"output_edges={output_edges} reset_clear={reset_clear} disabled_clear={disabled_clear} "
        f"valid_seen={valid_seen} timing_errors={timing_errors} metric_errors={metric_errors} "
        f"valid_errors={valid_errors} clear_errors={clear_errors}; "
        f"P_ON_RESET_OR_WHEN_DISABLED_DRIVE mismatch_count={max(0, clear_errors - clear_budget) + int(not reset_clear) + int(not disabled_clear)}; "
        f"P_DECODE_SKEW_2_SKEW_0_AS mismatch_count={timing_errors + max(0, metric_errors - metric_budget)}; "
        f"P_FOR_EACH_ACCEPTED_INPUT_CLOCK_EDGE mismatch_count={timing_errors + max(0, input_edges - output_edges - 1)}; "
        f"P_EXPOSE_THE_ACTIVE_DELAY_CODE_AS mismatch_count={max(0, metric_errors - metric_budget)}; "
        f"P_ASSERT_VALID_AFTER_THE_FIRST_DELAYED mismatch_count={max(0, valid_errors - valid_budget) + int(not valid_seen)}"
    )

CHECKER_ID = "v4_323_programmable_clock_skew_aligner"
CHECKER: Checker = check_v4_1021_programmable_clock_skew_aligner
