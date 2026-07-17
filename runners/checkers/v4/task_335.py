"""Task-specific checker for canonical v4 DUT 335."""
from __future__ import annotations

from bisect import bisect_left

from ..api import Checker
from .diagnostics import with_diagnostic_contract


def _v4_topup_logic_high(row: dict[str, float], name: str, threshold: float = 0.45) -> bool:
    return float(row.get(name, 0.0)) > threshold

def _v4_edges(rows: list[dict[str, float]], name: str, *, vth: float = 0.45) -> list[float]:
    if not rows:
        return []
    prev = float(rows[0].get(name, 0.0))
    was_active = (
        _v4_topup_logic_high(rows[0], "enable")
        and not _v4_topup_logic_high(rows[0], "rst")
    )
    edges: list[float] = []
    for row in rows[1:]:
        t = float(row["time"])
        active = (
            _v4_topup_logic_high(row, "enable")
            and not _v4_topup_logic_high(row, "rst")
        )
        if not active:
            prev = float(row.get(name, 0.0))
            was_active = False
            continue
        now = float(row.get(name, 0.0))
        if was_active and prev <= vth and now > vth:
            edges.append(t)
        prev = now
        was_active = True
    return edges

def check_v4_1033_quadrature_oscillator_phase_error_monitor(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1033 empty_trace"
    i_edges = _v4_edges(rows, "clk_i")
    q_edges = _v4_edges(rows, "clk_q")
    times = [float(row["time"]) for row in rows]

    def active(row: dict[str, float]) -> bool:
        return _v4_topup_logic_high(row, "enable") and not _v4_topup_logic_high(row, "rst")

    segments: list[tuple[float, float]] = []
    segment_start: float | None = None
    for row in rows:
        t = float(row["time"])
        if active(row) and segment_start is None:
            segment_start = t
        elif not active(row) and segment_start is not None:
            segments.append((segment_start, t))
            segment_start = None
    if segment_start is not None:
        segments.append((segment_start, times[-1]))

    expected_by_segment: list[list[tuple[float, float, bool]]] = []
    for start, stop in segments:
        segment_i = [edge for edge in i_edges if start <= edge < stop]
        segment_q = [edge for edge in q_edges if start <= edge < stop]
        expected: list[tuple[float, float, bool]] = []
        # The DUT learns the I period at the second I edge, so a Q edge in
        # the first interval cannot yet produce a phase measurement.
        for idx in range(2, len(segment_i)):
            prev_i = segment_i[idx - 1]
            cur_i = segment_i[idx]
            period = cur_i - prev_i
            qs = [q for q in segment_q if prev_i < q < cur_i]
            if not qs or period <= 0:
                continue
            q = qs[0]
            phase = (q - prev_i) / period
            err = abs(phase - 0.25)
            metric = min(0.9, 3.6 * err)
            expected.append((q, metric, metric <= 60e-3))
        expected_by_segment.append(expected)

    checked = metric_errors = ok_errors = valid_errors = clear_errors = 0
    reset_clear = disabled_clear = valid_seen = ok_seen = bad_phase_seen = False
    ever_enabled = False
    disable_time: float | None = None
    for row in rows:
        t = float(row["time"])
        rst = _v4_topup_logic_high(row, "rst")
        enabled = active(row)
        if not enabled:
            clear = abs(float(row["phase_error_metric"])) < 0.08 and not _v4_topup_logic_high(row, "quadrature_ok") and not _v4_topup_logic_high(row, "valid")
            if rst and clear:
                reset_clear = True
            disabled = ever_enabled and not _v4_topup_logic_high(row, "enable")
            if disabled and disable_time is None:
                disable_time = t
            disabled_ready = (
                disabled
                and disable_time is not None
                and t >= disable_time + 0.7e-9
            )
            if disabled_ready and clear:
                disabled_clear = True
            if (rst or disabled_ready) and not clear:
                clear_errors += 1
            continue
        ever_enabled = True
        disable_time = None
    for expected_events in expected_by_segment:
        stable_ok = 0
        for update_time, expected_metric, raw_ok in expected_events:
            stable_ok = stable_ok + 1 if raw_ok else 0
            expected_ok = stable_ok >= 2
            bad_phase_seen = bad_phase_seen or not raw_ok
            sample_index = min(len(rows) - 1, bisect_left(times, update_time + 0.7e-9))
            sample = rows[sample_index]
            if not active(sample):
                continue
            checked += 1
            if abs(float(sample["phase_error_metric"]) - expected_metric) > 0.08:
                metric_errors += 1
            got_ok = _v4_topup_logic_high(sample, "quadrature_ok")
            ok_seen = ok_seen or got_ok
            if got_ok != expected_ok:
                ok_errors += 1
            valid = _v4_topup_logic_high(sample, "valid")
            valid_seen = valid_seen or valid
            if not valid:
                valid_errors += 1
    metric_budget = 1
    ok_budget = 1
    valid_budget = 1
    clear_budget = 4
    ok = (
        len(i_edges) >= 5
        and len(q_edges) >= 5
        and checked >= 5
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
CHECKER: Checker = with_diagnostic_contract(check_v4_1033_quadrature_oscillator_phase_error_monitor)
