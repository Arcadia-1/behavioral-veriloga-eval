"""Task-specific checker for canonical v4 DUT 327."""
from __future__ import annotations

from ..api import Checker
VDD = 0.9
VTH = 0.45

def _high(row: dict[str, float], name: str, thr: float = VTH) -> bool:
    return float(row.get(name, 0.0)) > thr

def _rising(prev: float, now: float, thr: float = VTH) -> bool:
    return now > thr and prev <= thr

def _missing(rows: list[dict[str, float]], required: set[str]) -> list[str]:
    if not rows:
        return sorted(required)
    return sorted(required - set(rows[0].keys()))

def check_v4_327_cdr_eye_monitor(rows: list[dict[str, float]]) -> tuple[bool, str]:
    req = {
        "time", "data_in", "sample_clk", "rst", "enable",
        "early", "late", "eye_metric", "lock_hint", "valid",
    }
    miss = _missing(rows, req)
    if miss:
        return False, f"v4_327 missing_signals={','.join(miss)}"
    prev_clk = float(rows[0]["sample_clk"])
    prev_data = float(rows[0]["data_in"])
    sample_times: list[float] = []
    lock_sample_events: list[tuple[float, int]] = []
    data_edge_times: list[float] = []
    reset_clear = disabled_clear = ever_enabled = False
    clear_errors = mutex_errors = range_errors = 0
    eye_max = 0.0
    enable_epoch = 0
    was_enabled = False
    for row in rows:
        t = float(row["time"])
        clk = float(row["sample_clk"])
        data = float(row["data_in"])
        rst = _high(row, "rst")
        enabled = _high(row, "enable") and not rst
        if not enabled:
            if was_enabled:
                enable_epoch += 1
            was_enabled = False
            clear = (
                not _high(row, "early")
                and not _high(row, "late")
                and not _high(row, "lock_hint")
                and not _high(row, "valid")
                and abs(float(row["eye_metric"])) < 0.08
            )
            if rst and clear:
                reset_clear = True
            if ever_enabled and not _high(row, "enable") and clear:
                disabled_clear = True
            if (rst or (ever_enabled and not _high(row, "enable") and disabled_clear)) and not clear:
                clear_errors += 1
        else:
            was_enabled = True
            ever_enabled = True
            if _rising(prev_clk, clk):
                sample_times.append(t)
            if prev_clk > VTH and clk <= VTH:
                lock_sample_events.append((t, enable_epoch))
            if (data > VTH) != (prev_data > VTH):
                data_edge_times.append(t)
            early = _high(row, "early")
            late = _high(row, "late")
            if early and late:
                mutex_errors += 1
            eye = float(row["eye_metric"])
            eye_max = max(eye_max, eye)
            if eye < -0.05 or eye > VDD + 0.05:
                range_errors += 1
        prev_clk = clk
        prev_data = data

    def flag_seen(name: str, event_t: float) -> bool:
        return any(
            event_t <= float(row["time"]) <= event_t + 1.2e-9
            and _high(row, name)
            for row in rows
        )

    early_events = [
        sample_t
        for sample_t in sample_times
        if any(0.0 <= sample_t - edge_t <= 0.8e-9 for edge_t in data_edge_times)
    ]
    late_events = [
        edge_t
        for edge_t in data_edge_times
        if any(0.0 <= edge_t - sample_t <= 0.8e-9 for sample_t in sample_times)
    ]
    early_misses = sum(not flag_seen("early", t) for t in early_events)
    late_misses = sum(not flag_seen("late", t) for t in late_events)
    valid_misses = sum(not flag_seen("valid", t) for t in sample_times)
    open_streak = 0
    open_streak_reached = False
    lock_seen = False
    early_lock_errors = missing_lock_errors = 0
    previous_epoch: int | None = None
    for sample_t, epoch in lock_sample_events:
        if previous_epoch != epoch:
            open_streak = 0
            previous_epoch = epoch
        sample = next((row for row in rows if float(row["time"]) >= sample_t + 0.7e-9), rows[-1])
        qualifies = float(sample["eye_metric"]) > 0.55
        open_streak = open_streak + 1 if qualifies else 0
        observed_lock = _high(sample, "lock_hint")
        lock_seen = lock_seen or observed_lock
        open_streak_reached = open_streak_reached or open_streak >= 4
        if observed_lock and open_streak < 4:
            early_lock_errors += 1
        if open_streak >= 4 and not observed_lock:
            missing_lock_errors += 1
    lock_errors = early_lock_errors + missing_lock_errors
    checked = len(sample_times)
    ok = (
        checked >= 8
        and reset_clear
        and disabled_clear
        and bool(early_events)
        and bool(late_events)
        and early_misses == 0
        and late_misses == 0
        and valid_misses <= 1
        and mutex_errors == 0
        and range_errors == 0
        and eye_max > 0.55
        and open_streak_reached
        and lock_errors == 0
    )
    clear_mismatches = int(not reset_clear) + int(not disabled_clear)
    timing_mismatches = early_misses + late_misses + mutex_errors
    return ok, (
        f"v4_327 checked={checked} early_events={len(early_events)} late_events={len(late_events)} "
        f"early_misses={early_misses} late_misses={late_misses} lock_seen={lock_seen} "
        f"open_streak_reached={open_streak_reached} eye_max={eye_max:.3f} "
        f"early_lock_errors={early_lock_errors} missing_lock_errors={missing_lock_errors} "
        f"mutex_errors={mutex_errors} range_errors={range_errors} valid_misses={valid_misses} "
        f"reset_clear={reset_clear} disabled_clear={disabled_clear} clear_errors={clear_errors}; "
        f"P_ON_RESET_OR_WHEN_DISABLED_CLEAR mismatch_count={clear_mismatches}; "
        f"P_ON_EACH_SAMPLING_CLOCK_EDGE_COMPARE mismatch_count={valid_misses}; "
        f"P_RAISE_EARLY_OR_LATE_ACCORDING_TO mismatch_count={timing_mismatches}; "
        f"P_DRIVE_EYE_METRIC_FROM_RECENT_TRANSITION mismatch_count={range_errors + int(eye_max <= 0.55)}; "
        f"P_ASSERT_LOCK_HINT_AFTER_FOUR_CONSECUTIVE mismatch_count={lock_errors}"
    )

CHECKER_ID = "v4_327_cdr_eye_monitor"
CHECKER: Checker = check_v4_327_cdr_eye_monitor
