"""Task-specific checker for canonical v4 DUT 326."""
from __future__ import annotations

from ..api import Checker
def _v4_topup_logic_high(row: dict[str, float], name: str, threshold: float = 0.45) -> bool:
    return float(row.get(name, 0.0)) > threshold

def _v4_code_from_bits(row: dict[str, float], bits: list[str]) -> int:
    return sum((1 << idx) for idx, bit in enumerate(bits) if _v4_topup_logic_high(row, bit))

def _v4_rising(prev_v: float, now_v: float, vth: float = 0.45) -> bool:
    return now_v > vth and prev_v <= vth

def _v4_edges(rows: list[dict[str, float]], name: str, *, vth: float = 0.45) -> list[float]:
    if not rows:
        return []
    prev = float(rows[0].get(name, 0.0))
    edges: list[float] = []
    for row in rows[1:]:
        t = float(row["time"])
        enabled = _v4_topup_logic_high(row, "enable") and not _v4_topup_logic_high(row, "rst")
        now = float(row.get(name, 0.0))
        if enabled and prev <= vth and now > vth:
            edges.append(t)
        prev = now
    return edges

def check_v4_1024_fractional_delay_dtc_macro(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1024 empty_trace"
    input_edges: list[tuple[float, int]] = []
    prev_clk = float(rows[0].get("clk_in", 0.0))
    update_time = -1.0
    expected_metric = 0.0
    checked = metric_errors = valid_errors = clear_errors = 0
    reset_clear = disabled_clear = False
    ever_enabled = False
    codes_seen: set[int] = set()
    for row in rows:
        t = float(row["time"])
        clk = float(row["clk_in"])
        rst = _v4_topup_logic_high(row, "rst")
        enabled = _v4_topup_logic_high(row, "enable") and not rst
        if not enabled:
            clear = abs(float(row["clk_out"])) < 0.08 and abs(float(row["phase_metric"])) < 0.08 and not _v4_topup_logic_high(row, "valid")
            disabled = ever_enabled and not _v4_topup_logic_high(row, "enable")
            if rst and clear:
                reset_clear = True
            if disabled and clear:
                disabled_clear = True
            if ((rst and reset_clear) or (disabled and disabled_clear)) and not clear:
                clear_errors += 1
            prev_clk = clk
            continue
        ever_enabled = True
        if _v4_rising(prev_clk, clk):
            code = _v4_code_from_bits(row, ["frac_0", "frac_1", "frac_2", "frac_3"])
            input_edges.append((t, code))
            codes_seen.add(code)
            expected_metric = 0.9 * code / 15.0
            update_time = t
        prev_clk = clk
        if update_time < 0 or t < update_time + 0.7e-9:
            continue
        checked += 1
        if abs(float(row["phase_metric"]) - expected_metric) > 0.08:
            metric_errors += 1
        if not _v4_topup_logic_high(row, "valid"):
            valid_errors += 1
    output_edges = _v4_edges(rows, "clk_out")
    delay_errors = 0
    matched = 0
    prev_delay = None
    monotonic_pairs = 0
    for edge_t, code in input_edges:
        candidates = [out_t for out_t in output_edges if edge_t + 0.05e-9 <= out_t <= edge_t + 5.5e-9]
        if not candidates:
            delay_errors += 1
            continue
        delay = min(candidates) - edge_t
        expected_delay = (code + 1) * 0.2e-9
        matched += 1
        if abs(delay - expected_delay) > 0.55e-9:
            delay_errors += 1
        if prev_delay is not None and code >= 8 and delay > prev_delay:
            monotonic_pairs += 1
        prev_delay = delay
    delay_budget = 2
    metric_budget = max(6, checked // 15)
    valid_budget = 4
    clear_budget = 4
    ok = (
        checked >= 40
        and len(codes_seen) >= 5
        and matched >= 5
        and monotonic_pairs >= 1
        and reset_clear
        and disabled_clear
        and delay_errors <= delay_budget
        and metric_errors <= metric_budget
        and valid_errors <= valid_budget
        and clear_errors <= clear_budget
    )
    return ok, (
        f"v4_1024 checked={checked} codes={sorted(codes_seen)} input_edges={len(input_edges)} "
        f"output_edges={len(output_edges)} matched={matched} monotonic_pairs={monotonic_pairs} "
        f"reset_clear={reset_clear} disabled_clear={disabled_clear} delay_errors={delay_errors} "
        f"metric_errors={metric_errors} valid_errors={valid_errors} clear_errors={clear_errors}; "
        f"P_ON_RESET_OR_WHEN_DISABLED_CLEAR mismatch_count={max(0, clear_errors - clear_budget) + int(not reset_clear) + int(not disabled_clear)}; "
        f"P_DECODE_FRAC_3_FRAC_0_AS mismatch_count={max(0, delay_errors - delay_budget)}; "
        f"P_FOR_EACH_INPUT_EDGE_EMIT_ONE mismatch_count={max(0, delay_errors - delay_budget) + max(0, len(input_edges) - matched)}; "
        f"P_EXPOSE_THE_FRACTIONAL_DELAY_AS_PHASE mismatch_count={max(0, metric_errors - metric_budget)}; "
        f"P_PRESERVE_INPUT_EDGE_ORDER_AND_ASSERT mismatch_count={max(0, valid_errors - valid_budget)}"
    )

CHECKER_ID = "v4_326_fractional_delay_dtc_macro"
CHECKER: Checker = check_v4_1024_fractional_delay_dtc_macro
