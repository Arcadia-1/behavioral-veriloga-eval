"""Task-specific checker for canonical v4 DUT 192."""
from __future__ import annotations

from checkers.api import Checker
def _threshold_crossings(
    values: list[float],
    times: list[float],
    *,
    threshold: float = 0.0,
    direction: str,
) -> list[float]:
    edges: list[float] = []
    for idx in range(1, len(values)):
        v0 = values[idx - 1]
        v1 = values[idx]
        if direction == "rising":
            hit = v0 <= threshold < v1
        elif direction == "falling":
            hit = v0 >= threshold > v1
        else:
            raise ValueError(f"unsupported direction={direction!r}")
        if not hit:
            continue
        t0 = times[idx - 1]
        t1 = times[idx]
        if v1 == v0:
            edges.append(t1)
        else:
            alpha = (threshold - v0) / (v1 - v0)
            edges.append(t0 + alpha * (t1 - t0))
    return edges

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

def _max_signal_value(
    rows: list[dict[str, float]],
    signals: list[str],
    *,
    default: float,
) -> float:
    values: list[float] = []
    for row in rows:
        for signal in signals:
            value = row.get(signal)
            if value is not None:
                values.append(value)
    return max(values) if values else default

def _edge_times_for_signal(
    rows: list[dict[str, float]],
    signal: str,
    *,
    threshold: float,
    direction: str,
) -> list[float]:
    times = [row["time"] for row in rows if "time" in row and signal in row]
    values = [row[signal] for row in rows if "time" in row and signal in row]
    if len(times) < 2:
        return []
    return _threshold_crossings(values, times, threshold=threshold, direction=direction)

def _event_probe_time(
    rows: list[dict[str, float]],
    event_time_s: float,
    *,
    delay_s: float = 0.18e-9,
) -> float | None:
    if not rows:
        return None
    last_time = rows[-1].get("time")
    if last_time is None:
        return None
    probe_time = event_time_s + delay_s
    if probe_time <= last_time:
        return probe_time
    fallback = last_time - 0.02e-9
    return fallback if fallback > event_time_s else None

def _assert_sample_close(
    rows: list[dict[str, float]],
    signal: str,
    time_s: float,
    expected: float,
    *,
    tol: float,
) -> tuple[bool, str]:
    value = sample_signal_at(rows, signal, time_s)
    if value is None:
        return False, f"missing_{signal}_sample_at={time_s * 1e9:g}ns"
    if abs(value - expected) > tol:
        return False, f"{signal}@{time_s * 1e9:g}ns={value:.4f} expected={expected:.4f} tol={tol:.4f}"
    return True, f"{signal}@{time_s * 1e9:g}ns={value:.4f}"

def _assert_logic_levels(
    rows: list[dict[str, float]],
    expected_bits: dict[str, int],
    time_s: float,
    *,
    vhi: float,
    vlo: float = 0.0,
    tol: float = 0.12,
) -> tuple[bool, str]:
    checked = 0
    for signal, bit in expected_bits.items():
        expected = vhi if bit else vlo
        ok, detail = _assert_sample_close(rows, signal, time_s, expected, tol=tol)
        if not ok:
            return False, detail
        checked += 1
    return True, f"checked_logic_levels={checked}@{time_s * 1e9:g}ns"

def check_v3_sar_logic_4b_self_timed(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clkc", "rst", "dcmpp", "dcmpn", "cmpck", "dout1", "dout2", "dout3", "dout4", "dbotp1", "dbotp2", "dbotp3", "dbotn1", "dbotn2", "dbotn3"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing sar logic 4b self timed signals"
    vhi = _max_signal_value(rows, ["clkc", "rst", "dcmpp", "dcmpn"], default=1.0)
    threshold = 0.5 * vhi
    reset_rises = _edge_times_for_signal(rows, "rst", threshold=threshold, direction="rising")
    clkc_rises = _edge_times_for_signal(rows, "clkc", threshold=threshold, direction="rising")
    comp_events: list[tuple[float, str]] = []
    for signal in ("dcmpp", "dcmpn"):
        comp_events.extend((t, "rise") for t in _edge_times_for_signal(rows, signal, threshold=threshold, direction="rising"))
        comp_events.extend((t, "fall") for t in _edge_times_for_signal(rows, signal, threshold=threshold, direction="falling"))
    comp_events.sort(key=lambda item: item[0])
    comp_rises = [t for t, kind in comp_events if kind == "rise"]
    if not clkc_rises:
        return False, "missing_clkc_start_edge"
    if len(comp_rises) < 4:
        return False, f"insufficient_comparator_pulses={len(comp_rises)}"

    step = 4
    d = {idx: 0 for idx in range(1, 5)}
    bp = {idx: 1 for idx in range(1, 4)}
    bn = {idx: 1 for idx in range(1, 4)}
    checked = 0

    if reset_rises:
        reset_probe = _event_probe_time(rows, reset_rises[0], delay_s=0.22e-9)
        if reset_probe is not None:
            expected_reset = {"cmpck": 0, "dout1": 0, "dout2": 0, "dout3": 0, "dout4": 0}
            expected_reset.update({f"dbotp{idx}": 1 for idx in range(1, 4)})
            expected_reset.update({f"dbotn{idx}": 1 for idx in range(1, 4)})
            ok, detail = _assert_logic_levels(rows, expected_reset, reset_probe, vhi=vhi, tol=0.12)
            if not ok:
                return False, f"reset_{detail}"
            checked += 1

    start_probe = _event_probe_time(rows, clkc_rises[0], delay_s=0.24e-9)
    if start_probe is not None:
        ok, detail = _assert_logic_levels(rows, {"cmpck": 1}, start_probe, vhi=vhi, tol=0.12)
        if not ok:
            return False, f"clkc_start_{detail}"
        checked += 1

    for event_time, kind in comp_events:
        if kind == "rise":
            dcmpp_value = sample_signal_at(rows, "dcmpp", event_time + 0.02e-9)
            dcmpn_value = sample_signal_at(rows, "dcmpn", event_time + 0.02e-9)
            if dcmpp_value is None or dcmpn_value is None:
                return False, f"missing_comparator_value_at={event_time * 1e9:g}ns"
            positive = dcmpp_value > dcmpn_value
            if 1 <= step <= 4:
                d[step] = 1 if positive else 0
            if step > 1:
                ctrl_idx = step - 1
                if positive:
                    bp[ctrl_idx] = 0
                else:
                    bn[ctrl_idx] = 0
            logic_probe = _event_probe_time(rows, event_time, delay_s=0.14e-9)
            if logic_probe is not None:
                expected = {f"dout{idx}": d[idx] for idx in range(1, 5)}
                expected.update({f"dbotp{idx}": bp[idx] for idx in range(1, 4)})
                expected.update({f"dbotn{idx}": bn[idx] for idx in range(1, 4)})
                ok, detail = _assert_logic_levels(rows, expected, logic_probe, vhi=vhi, tol=0.12)
                if not ok:
                    return False, f"decision_step{step}_{detail}"
                checked += 1
            cmpck_low_probe = _event_probe_time(rows, event_time, delay_s=0.24e-9)
            if cmpck_low_probe is not None:
                ok, detail = _assert_logic_levels(rows, {"cmpck": 0}, cmpck_low_probe, vhi=vhi, tol=0.12)
                if not ok:
                    return False, f"cmpck_close_step{step}_{detail}"
                checked += 1
        else:
            if step > 1:
                step -= 1
                cmpck_high_probe = _event_probe_time(rows, event_time, delay_s=0.24e-9)
                if cmpck_high_probe is not None:
                    ok, detail = _assert_logic_levels(rows, {"cmpck": 1}, cmpck_high_probe, vhi=vhi, tol=0.12)
                    if not ok:
                        return False, f"cmpck_reopen_step{step}_{detail}"
                    checked += 1
    if checked < 8:
        return False, f"insufficient_self_timed_sar_checks={checked}"
    return True, f"checked={checked} comparator_pulses={len(comp_rises)} final_step={step}"

CHECKER_ID = "v4_192_sar_logic_4b_self_timed"
CHECKER: Checker = check_v3_sar_logic_4b_self_timed
