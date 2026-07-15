"""Task-specific checker for canonical v4 DUT 335."""
from __future__ import annotations

from ..api import Checker
def _v4_topup_logic_high(row: dict[str, float], name: str, threshold: float = 0.45) -> bool:
    return float(row.get(name, 0.0)) > threshold

def _v4_edges(rows: list[dict[str, float]], name: str, *, start: float = 0.0, stop: float | None = None, vth: float = 0.45) -> list[float]:
    if not rows:
        return []
    prev = float(rows[0].get(name, 0.0))
    edges: list[float] = []
    for row in rows[1:]:
        t = float(row["time"])
        if t < start or (stop is not None and t > stop):
            prev = float(row.get(name, 0.0))
            continue
        now = float(row.get(name, 0.0))
        if prev <= vth and now > vth:
            edges.append(t)
        prev = now
    return edges

def check_v4_1033_quadrature_oscillator_phase_error_monitor(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1033 empty_trace"
    i_edges = _v4_edges(rows, "clk_i", start=5e-9, stop=82e-9)
    q_edges = _v4_edges(rows, "clk_q", start=5e-9, stop=82e-9)
    expected_by_time: list[tuple[float, float, bool]] = []
    for idx in range(1, len(i_edges)):
        prev_i = i_edges[idx - 1]
        cur_i = i_edges[idx]
        period = cur_i - prev_i
        qs = [q for q in q_edges if prev_i < q < cur_i]
        if not qs or period <= 0:
            continue
        q = qs[0]
        phase = (q - prev_i) / period
        err = abs(phase - 0.25)
        expected_by_time.append((q, min(0.9, 3.6 * err), err <= (60e-3 / 0.9)))
    checked = metric_errors = ok_errors = valid_errors = clear_errors = 0
    reset_clear = disabled_clear = valid_seen = ok_seen = bad_phase_seen = False
    expected_metric = 0.0
    expected_ok = False
    stable_ok = 0
    update_time = -1.0
    exp_idx = 0
    for row in rows:
        t = float(row["time"])
        rst = _v4_topup_logic_high(row, "rst")
        enabled = _v4_topup_logic_high(row, "enable") and not rst
        if not enabled:
            expected_metric = 0.0
            expected_ok = False
            stable_ok = 0
            clear = abs(float(row["phase_error_metric"])) < 0.08 and not _v4_topup_logic_high(row, "quadrature_ok") and not _v4_topup_logic_high(row, "valid")
            if rst and t < 5e-9 and clear:
                reset_clear = True
            if t > 82e-9 and not _v4_topup_logic_high(row, "enable") and clear:
                disabled_clear = True
            if ((rst and t < 5e-9) or t > 82e-9) and not clear:
                clear_errors += 1
            continue
        while exp_idx < len(expected_by_time) and t >= expected_by_time[exp_idx][0]:
            _, expected_metric, raw_ok = expected_by_time[exp_idx]
            stable_ok = stable_ok + 1 if raw_ok else 0
            expected_ok = stable_ok >= 2
            if not raw_ok:
                bad_phase_seen = True
            update_time = expected_by_time[exp_idx][0]
            exp_idx += 1
        if update_time < 0 or t < update_time + 0.7e-9:
            continue
        checked += 1
        if abs(float(row["phase_error_metric"]) - expected_metric) > 0.08:
            metric_errors += 1
        got_ok = _v4_topup_logic_high(row, "quadrature_ok")
        ok_seen = ok_seen or got_ok
        if got_ok != expected_ok:
            ok_errors += 1
        valid = _v4_topup_logic_high(row, "valid")
        valid_seen = valid_seen or valid
        if not valid:
            valid_errors += 1
    metric_budget = max(6, checked // 12)
    ok_budget = max(8, checked // 5)
    valid_budget = max(8, checked // 5)
    clear_budget = 4
    ok = (
        len(i_edges) >= 5
        and len(q_edges) >= 5
        and checked >= 35
        and reset_clear
        and disabled_clear
        and valid_seen
        and ok_seen
        and bad_phase_seen
        and metric_errors <= metric_budget
        and ok_errors <= ok_budget
        and valid_errors <= valid_budget
        and clear_errors <= clear_budget
    )
    return ok, (
        f"v4_1033 checked={checked} i_edges={len(i_edges)} q_edges={len(q_edges)} "
        f"reset_clear={reset_clear} disabled_clear={disabled_clear} valid_seen={valid_seen} "
        f"ok_seen={ok_seen} bad_phase_seen={bad_phase_seen} metric_errors={metric_errors} "
        f"ok_errors={ok_errors} valid_errors={valid_errors} clear_errors={clear_errors}; "
        f"P_ON_RESET_OR_WHEN_DISABLED_CLEAR mismatch_count={max(0, clear_errors - clear_budget) + int(not reset_clear) + int(not disabled_clear)}; "
        f"P_TRACK_RISING_THRESHOLD_CROSSINGS_OF_CLK mismatch_count={int(len(i_edges) < 5) + int(len(q_edges) < 5)}; "
        f"P_ESTIMATE_A_VOLTAGE_DOMAIN_PHASE_ERROR mismatch_count={max(0, metric_errors - metric_budget)}; "
        f"P_ASSERT_QUADRATURE_OK_WHEN_THE_MEASURED mismatch_count={max(0, ok_errors - ok_budget) + int(not ok_seen)}; "
        f"P_ASSERT_VALID_AFTER_BOTH_I_AND mismatch_count={max(0, valid_errors - valid_budget) + int(not valid_seen)}"
    )

CHECKER_ID = "v4_335_quadrature_oscillator_phase_error_monitor"
CHECKER: Checker = check_v4_1033_quadrature_oscillator_phase_error_monitor
