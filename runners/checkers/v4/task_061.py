"""Task-specific checker for canonical v4 DUT 061."""
from __future__ import annotations

from ..api import Checker
def _logic_bits_to_int(row: dict[str, float], prefix: str, width: int, vth: float = 0.45) -> int:
    return sum((1 << bit) for bit in range(width) if row[f"{prefix}{bit}"] > vth)

def _rising_times(rows: list[dict[str, float]], col: str, vth: float = 0.45) -> list[float]:
    times: list[float] = []
    last = rows[0][col] > vth
    for row in rows[1:]:
        cur = row[col] > vth
        if not last and cur:
            times.append(row["time"])
        last = cur
    return times

def _falling_times(rows: list[dict[str, float]], col: str, vth: float = 0.45) -> list[float]:
    times: list[float] = []
    last = rows[0][col] > vth
    for row in rows[1:]:
        cur = row[col] > vth
        if last and not cur:
            times.append(row["time"])
        last = cur
    return times

def _sample_after(rows: list[dict[str, float]], t: float, delay: float = 5e-9) -> dict[str, float]:
    target = t + delay
    return min(rows, key=lambda row: abs(row["time"] - target))

def check_event_counter_windowed_16b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "gate", "event", "done", *{f"count{i}" for i in range(16)}}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing[:12])
    gate_rises = _rising_times(rows, "gate")
    gate_falls = _falling_times(rows, "gate")
    event_rises = _rising_times(rows, "event")
    errors = 0
    checked: list[int] = []
    outside_events_checked = 0
    reset_checks = 0
    hold_checks = 0
    failures: list[str] = []
    for start_t, stop_t in zip(gate_rises, gate_falls):
        next_event = next((event_t for event_t in event_rises if event_t > start_t), stop_t)
        open_delay = min(0.10e-9, max(0.04e-9, 0.40 * (next_event - start_t)))
        open_row = _sample_after(rows, start_t, open_delay)
        open_count = _logic_bits_to_int(open_row, "count", 16)
        if open_row["done"] > 0.45 or open_count != 0:
            failures.append(
                f"window_open observed=count:{open_count},done:{open_row['done']:.3f} "
                f"expected=count:0,done:0 window={start_t * 1e9:.3f}ns"
            )
        else:
            reset_checks += 1
        expected = sum(1 for t in event_rises if start_t < t < stop_t)
        row = _sample_after(rows, stop_t, 0.20e-9)
        actual = _logic_bits_to_int(row, "count", 16)
        if row["done"] <= 0.45 or actual != expected:
            errors += 1
            failures.append(
                f"window_close observed=count:{actual},done:{row['done']:.3f} "
                f"expected=count:{expected},done:>0.45 window={start_t * 1e9:.3f}-{stop_t * 1e9:.3f}ns"
            )
        checked.append(expected)
        next_start = next((rise for rise in gate_rises if rise > stop_t), rows[-1]["time"] + 1e-9)
        for event_t in event_rises:
            if not (stop_t < event_t < next_start):
                continue
            probe_t = min(rows[-1]["time"], event_t + 0.05e-9)
            if probe_t <= event_t:
                continue
            hold_row = _sample_after(rows, event_t, 0.05e-9)
            held = _logic_bits_to_int(hold_row, "count", 16)
            outside_events_checked += 1
            hold_checks += 1
            if held != expected or hold_row["done"] <= 0.45:
                errors += 1
                failures.append(
                    f"out_of_window_event observed=count:{held},done:{hold_row['done']:.3f} "
                    f"expected=count:{expected},done:>0.45 window={event_t * 1e9:.3f}ns"
                )
                break
    if failures:
        return False, " ".join(failures[:5])
    ok = (
        errors == 0
        and len(checked) >= 2
        and max(checked, default=0) > 0
        and outside_events_checked >= 1
        and reset_checks >= 1
        and hold_checks >= 1
    )
    return ok, (
        f"checked={checked} errors={errors} reset_checks={reset_checks} "
        f"outside_events_checked={outside_events_checked} hold_checks={hold_checks}"
    )

CHECKER_ID = "v4_061_event_counter_windowed_16b"
CHECKER: Checker = check_event_counter_windowed_16b
