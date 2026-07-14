"""Task-specific checker for canonical v4 DUT 005."""
from __future__ import annotations

from checkers.api import Checker
def sample_signal_at(rows: list[dict[str, float]], signal: str, time_s: float) -> float | None:
    if not rows or "time" not in rows[0] or signal not in rows[0]:
        return None
    first_time = rows[0]["time"]
    last_time = rows[-1].get("time")
    if last_time is None or time_s < first_time or time_s > last_time:
        return None
    if time_s == first_time:
        return rows[0].get(signal)
    for idx in range(1, len(rows)):
        prev = rows[idx - 1]
        cur = rows[idx]
        t0 = prev.get("time")
        t1 = cur.get("time")
        if t0 is None or t1 is None:
            continue
        if t0 <= time_s <= t1:
            v0 = prev.get(signal)
            v1 = cur.get(signal)
            if v0 is None or v1 is None:
                return None
            if t1 == t0:
                return v1
            alpha = (time_s - t0) / (t1 - t0)
            return v0 + alpha * (v1 - v0)
    return None

def check_v3_debounce_latch(rows: list[dict[str, float]]) -> tuple[bool, str]:
    """V3 debounce latch: reject glitches, reset-arm leakage, and reset-cancel leakage."""
    required = {"time", "out"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/out"
    samples = {
        "reset_arm_rejected_20ns": (20.0, False),
        "short_glitch_low_34ns": (34.0, False),
        "short_glitch_low_40ns": (40.0, False),
        "reset_cancel_low_67ns": (67.0, False),
        "post_cancel_low_72ns": (72.0, False),
        "pre_qualify_low_82ns": (82.0, False),
        "qualified_high_100ns": (100.0, True),
        "qualified_high_130ns": (130.0, True),
    }
    failures: list[str] = []
    notes: list[str] = []
    for label, (time_ns, should_be_high) in samples.items():
        value = sample_signal_at(rows, "out", time_ns * 1e-9)
        if value is None:
            failures.append(f"{label}=missing")
            continue
        is_high = value > 0.45
        notes.append(f"{label}:{value:.3f}")
        if is_high != should_be_high:
            failures.append(f"{label}:{value:.3f}")
    if failures:
        return False, " ".join(failures) + " " + " ".join(notes)
    return True, " ".join(notes)

def _v4_edge_times(
    rows: list[dict[str, float]], signal: str, *, rising: bool, threshold: float = 0.45
) -> list[float]:
    times: list[float] = []
    for previous, current in zip(rows, rows[1:]):
        before = previous[signal]
        after = current[signal]
        if rising and before < threshold <= after:
            times.append(current["time"])
        elif not rising and before > threshold >= after:
            times.append(current["time"])
    return times

def check_v4_debounce_latch(rows: list[dict[str, float]]) -> tuple[bool, str]:
    base_ok, base_note = check_v3_debounce_latch(rows)
    required = {"time", "sig", "rst_n", "out"}
    if not rows or not required.issubset(rows[0]):
        return False, base_note

    sig_rises = _v4_edge_times(rows, "sig", rising=True)
    sig_falls = _v4_edge_times(rows, "sig", rising=False)
    reset_falls = _v4_edge_times(rows, "rst_n", rising=False)
    out_rises = _v4_edge_times(rows, "out", rising=True)
    out_falls = _v4_edge_times(rows, "out", rising=False)
    expected_rises: list[float] = []
    for rise_time in sig_rises:
        reset_at_rise = sample_signal_at(rows, "rst_n", rise_time + 0.05e-9)
        expiry = rise_time + 12.0e-9
        if reset_at_rise is None or reset_at_rise <= 0.45:
            continue
        cancelled = any(rise_time < time_s <= expiry for time_s in sig_falls + reset_falls)
        sig_at_expiry = sample_signal_at(rows, "sig", expiry)
        reset_at_expiry = sample_signal_at(rows, "rst_n", expiry)
        if (
            not cancelled
            and sig_at_expiry is not None
            and reset_at_expiry is not None
            and sig_at_expiry > 0.45
            and reset_at_expiry > 0.45
        ):
            expected_rises.append(expiry)

    unmatched_expected = [
        time_s
        for time_s in expected_rises
        if not any(abs(observed - time_s) <= 1.2e-9 for observed in out_rises)
    ]
    unauthorized_rises = [
        time_s
        for time_s in out_rises
        if not any(abs(time_s - expected) <= 1.2e-9 for expected in expected_rises)
    ]
    legal_fall_events = sig_falls + reset_falls
    unauthorized_falls = [
        time_s
        for time_s in out_falls
        if not any(abs(time_s - event) <= 1.2e-9 for event in legal_fall_events)
    ]
    required_fall_events = [
        time_s
        for time_s in legal_fall_events
        if (sample_signal_at(rows, "out", max(0.0, time_s - 0.3e-9)) or 0.0) > 0.45
    ]
    unmatched_required_falls = [
        time_s
        for time_s in required_fall_events
        if not any(abs(observed - time_s) <= 1.2e-9 for observed in out_falls)
    ]

    rail_failures: list[str] = []
    for label, time_ns, expected_high in (
        ("pre_qualify", 82.0, False),
        ("qualified", 100.0, True),
        ("held_high", 130.0, True),
    ):
        value = sample_signal_at(rows, "out", time_ns * 1e-9)
        if value is None:
            rail_failures.append(f"{label}=missing")
        elif expected_high and value < 0.81:
            rail_failures.append(f"{label}={value:.3f}<0.810")
        elif not expected_high and value > 0.09:
            rail_failures.append(f"{label}={value:.3f}>0.090")

    event_ok = (
        len(expected_rises) >= 1
        and not unmatched_expected
        and not unauthorized_rises
        and not unauthorized_falls
        and not unmatched_required_falls
        and not rail_failures
    )
    return base_ok and event_ok, (
        f"{base_note} expected_rises={len(expected_rises)} observed_rises={len(out_rises)} "
        f"observed_falls={len(out_falls)} unmatched_expected={len(unmatched_expected)} "
        f"unauthorized_rises={len(unauthorized_rises)} unauthorized_falls={len(unauthorized_falls)} "
        f"required_falls={len(required_fall_events)} unmatched_required_falls={len(unmatched_required_falls)} "
        f"rail_failures={len(rail_failures)}"
        + (" unauthorized_rise_ns=" + ",".join(f"{t * 1e9:.3f}" for t in unauthorized_rises[:4]) if unauthorized_rises else "")
        + (" unauthorized_fall_ns=" + ",".join(f"{t * 1e9:.3f}" for t in unauthorized_falls[:4]) if unauthorized_falls else "")
        + (
            " missing_required_fall_ns="
            + ",".join(f"{t * 1e9:.3f}" for t in unmatched_required_falls[:4])
            if unmatched_required_falls
            else ""
        )
        + (" rail_detail=" + ";".join(rail_failures) if rail_failures else "")
    )

CHECKER_ID = "v4_005_debounce_latch"
CHECKER: Checker = check_v4_debounce_latch
