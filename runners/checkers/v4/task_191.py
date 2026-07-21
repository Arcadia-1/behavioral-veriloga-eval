"""Task-specific checker for canonical v4 DUT 191."""
from __future__ import annotations

from ..api import Checker
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

def check_v3_sar_das_logic_6b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {
        "time",
        "clk_sampling",
        "clk_sar",
        "vcomp",
        "d1",
        "d2",
        "d3",
        "d4",
        "d5",
        "d6",
        "db1",
        "db2",
        "db3",
        "db4",
        "db5",
        "db6",
        "co",
        "cob",
    }
    if not rows or not required.issubset(rows[0]):
        return False, "missing sar das logic signals"
    vdd = _max_signal_value(rows, ["clk_sampling", "clk_sar", "vcomp"], default=1.1)
    vcm = 0.5 * vdd
    events: list[tuple[float, str]] = []
    events.extend((t, "sampling_rise") for t in _edge_times_for_signal(rows, "clk_sampling", threshold=vcm, direction="rising"))
    events.extend((t, "sampling_fall") for t in _edge_times_for_signal(rows, "clk_sampling", threshold=vcm, direction="falling"))
    events.extend((t, "sar_rise") for t in _edge_times_for_signal(rows, "clk_sar", threshold=vcm, direction="rising"))
    events.extend((t, "sar_fall") for t in _edge_times_for_signal(rows, "clk_sar", threshold=vcm, direction="falling"))
    events.sort(key=lambda item: item[0])

    if sum(1 for _, kind in events if kind == "sampling_rise") < 1:
        return False, "missing_sampling_rising_reset"
    if sum(1 for _, kind in events if kind == "sampling_fall") < 1:
        return False, "missing_sampling_falling_preset"
    sar_rises = sum(1 for _, kind in events if kind == "sar_rise")
    if sar_rises < 6:
        return False, f"insufficient_sar_rising_edges={sar_rises}"

    bit = 7
    b = {idx: 0 for idx in range(1, 7)}
    bb = {idx: 0 for idx in range(1, 7)}
    cout = 0
    coutb = 0
    checked = 0
    for event_time, kind in events:
        prior = {f"d{idx}": b[idx] for idx in range(1, 7)}
        prior.update({f"db{idx}": bb[idx] for idx in range(1, 7)})
        prior.update({"co": cout, "cob": coutb})
        if kind == "sampling_rise":
            bit = 7
            b = {idx: 0 for idx in range(1, 7)}
            bb = {idx: 0 for idx in range(1, 7)}
            cout = 0
            coutb = 0
        elif kind == "sampling_fall":
            b = {idx: 1 for idx in range(1, 7)}
            bb = {idx: 1 for idx in range(1, 7)}
            cout = 0
            coutb = 0
        elif kind == "sar_rise":
            vcomp = sample_signal_at(rows, "vcomp", event_time + 0.02e-9)
            if vcomp is None:
                vcomp = sample_signal_at(rows, "vcomp", event_time)
            if vcomp is None:
                return False, f"missing_vcomp_at_sar_edge={event_time * 1e9:g}ns"
            if vcomp > vcm:
                cout = 1
                coutb = 0
                if bit == 7:
                    b[6] = 1
                elif bit == 6:
                    bb[5] = 0
                elif bit == 5:
                    bb[4] = 0
                elif bit == 4:
                    bb[3] = 0
                elif bit == 3:
                    bb[2] = 0
                elif bit == 2:
                    bb[1] = 0
            else:
                cout = 0
                coutb = 1
                if bit == 7:
                    bb[6] = 1
                elif bit == 6:
                    b[5] = 0
                elif bit == 5:
                    b[4] = 0
                elif bit == 4:
                    b[3] = 0
                elif bit == 3:
                    b[2] = 0
                elif bit == 2:
                    b[1] = 0
            bit -= 1
        elif kind == "sar_fall":
            cout = 0
            coutb = 0

        delay_probe = _event_probe_time(rows, event_time, delay_s=0.025e-9)
        if delay_probe is not None:
            ok, detail = _assert_logic_levels(rows, prior, delay_probe, vhi=vdd, tol=0.13)
            if not ok:
                return False, f"{kind}_output_delay_{detail}"
            checked += 1

        probe_time = _event_probe_time(rows, event_time, delay_s=0.17e-9)
        if probe_time is None:
            continue
        expected = {f"d{idx}": b[idx] for idx in range(1, 7)}
        expected.update({f"db{idx}": bb[idx] for idx in range(1, 7)})
        expected.update({"co": cout, "cob": coutb})
        ok, detail = _assert_logic_levels(rows, expected, probe_time, vhi=vdd, tol=0.13)
        if not ok:
            return False, f"{kind}_{detail}"
        checked += 1
    if checked < 8:
        return False, f"insufficient_sar_logic_checks={checked}"
    return True, f"checked={checked} sar_rises={sar_rises} final_bit={bit}"

CHECKER_ID = "v4_191_sar_das_logic_6b"
CHECKER: Checker = check_v3_sar_das_logic_6b
