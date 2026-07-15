"""Task-specific checker for canonical v4 DUT 170."""
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

def check_v3_comparator_delay_overdrive_meter(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {
        "time",
        "clk",
        "vinp",
        "vinn",
        "outp",
        "outn",
        "delay_ps",
        "overdrive_mv",
        "polarity",
        "valid",
    }
    if not rows or not required.issubset(rows[0]):
        return False, "missing comparator delay overdrive meter signals"

    vdd = _max_signal_value(rows, ["clk", "outp", "outn", "valid", "polarity"], default=0.9)
    threshold = 0.5 * vdd
    times = [row["time"] for row in rows]
    clk_rises = _threshold_crossings([row["clk"] for row in rows], times, threshold=threshold, direction="rising")
    out_events: list[tuple[float, str]] = []
    out_events += [
        (t, "outp")
        for t in _threshold_crossings([row["outp"] for row in rows], times, threshold=threshold, direction="rising")
    ]
    out_events += [
        (t, "outn")
        for t in _threshold_crossings([row["outn"] for row in rows], times, threshold=threshold, direction="rising")
    ]
    out_events.sort()
    if len(clk_rises) < 4 or len(out_events) < 4:
        return False, f"insufficient_delay_events clk={len(clk_rises)} out={len(out_events)}"

    failures: list[str] = []
    checked = 0
    max_delay_err = 0.0
    max_overdrive_err = 0.0
    saw_outp = False
    saw_outn = False

    for idx, clk_t in enumerate(clk_rises):
        next_clk = clk_rises[idx + 1] if idx + 1 < len(clk_rises) else rows[-1]["time"] + 1e-12
        event = next(((t, name) for t, name in out_events if clk_t + 1e-13 < t < next_clk), None)
        if event is None:
            continue
        event_t, out_name = event
        probe_t = _event_probe_time(rows, event_t, delay_s=0.08e-9)
        if probe_t is None:
            continue
        vinp = sample_signal_at(rows, "vinp", clk_t + 1e-12)
        vinn = sample_signal_at(rows, "vinn", clk_t + 1e-12)
        delay_s = sample_signal_at(rows, "delay_ps", probe_t)
        overdrive_v = sample_signal_at(rows, "overdrive_mv", probe_t)
        polarity = sample_signal_at(rows, "polarity", probe_t)
        valid = sample_signal_at(rows, "valid", probe_t)
        if None in (vinp, vinn, delay_s, overdrive_v, polarity, valid):
            continue
        assert vinp is not None
        assert vinn is not None
        assert delay_s is not None
        assert overdrive_v is not None
        assert polarity is not None
        assert valid is not None

        delay_ps = 1.0e12 * delay_s
        overdrive_mv = 1.0e3 * overdrive_v

        expected_delay_ps = 1.0e12 * (event_t - clk_t)
        expected_overdrive_mv = 1.0e3 * abs(vinp - vinn)
        expected_polarity = vdd if out_name == "outp" else 0.0
        saw_outp = saw_outp or out_name == "outp"
        saw_outn = saw_outn or out_name == "outn"
        delay_err = abs(delay_ps - expected_delay_ps)
        overdrive_err = abs(overdrive_mv - expected_overdrive_mv)
        polarity_err = abs(polarity - expected_polarity)
        max_delay_err = max(max_delay_err, delay_err)
        max_overdrive_err = max(max_overdrive_err, overdrive_err)
        checked += 1
        if delay_err > 4.0:
            failures.append(
                f"delay@{probe_t * 1e9:.3f}ns={delay_ps:.3f} expected={expected_delay_ps:.3f}"
            )
        if overdrive_err > 1.5:
            failures.append(
                f"overdrive@{probe_t * 1e9:.3f}ns={overdrive_mv:.3f} expected={expected_overdrive_mv:.3f}"
            )
        if polarity_err > 0.08 or valid < 0.7 * vdd:
            failures.append(
                f"flags@{probe_t * 1e9:.3f}ns polarity={polarity:.3f}/{expected_polarity:.3f} valid={valid:.3f}"
            )

    if checked < 4:
        return False, f"insufficient_checked_delay_events={checked}"
    if not (saw_outp and saw_outn):
        return False, f"missing_decision_polarity_coverage outp={saw_outp} outn={saw_outn}"
    if failures:
        return False, " ".join(failures[:6])
    return (
        True,
        f"checked={checked} max_delay_err_ps={max_delay_err:.3f} "
        f"max_overdrive_err_mv={max_overdrive_err:.3f}",
    )

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

CHECKER_ID = "v4_170_comparator_delay_overdrive_meter"
CHECKER: Checker = check_v3_comparator_delay_overdrive_meter
