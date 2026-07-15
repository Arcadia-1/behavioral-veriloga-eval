"""Task-specific checker for canonical v4 DUT 111."""
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

def check_v3_hysteresis_trip_characterizer(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "cmp_out", "trip_rise", "trip_fall", "hyst_width", "valid"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing hysteresis trip characterizer signals"

    vdd = _max_signal_value(rows, ["cmp_out", "valid"], default=0.9)
    times = [row["time"] for row in rows]
    cmp_values = [row["cmp_out"] for row in rows]
    rises = _threshold_crossings(cmp_values, times, threshold=0.5 * vdd, direction="rising")
    falls = _threshold_crossings(cmp_values, times, threshold=0.5 * vdd, direction="falling")
    if len(rises) < 2 or len(falls) < 2:
        return False, f"insufficient_trip_events rises={len(rises)} falls={len(falls)}"

    rise_t = rises[-1]
    fall_t = falls[-1]
    expected_rise = sample_signal_at(rows, "vin", rise_t)
    expected_fall = sample_signal_at(rows, "vin", fall_t)
    final_t = rows[-1]["time"]
    trip_rise = sample_signal_at(rows, "trip_rise", final_t)
    trip_fall = sample_signal_at(rows, "trip_fall", final_t)
    hyst_width = sample_signal_at(rows, "hyst_width", final_t)
    valid = sample_signal_at(rows, "valid", final_t)
    if None in (expected_rise, expected_fall, trip_rise, trip_fall, hyst_width, valid):
        return False, "missing_trip_measurement_samples"

    assert expected_rise is not None
    assert expected_fall is not None
    assert trip_rise is not None
    assert trip_fall is not None
    assert hyst_width is not None
    assert valid is not None

    expected_width = expected_rise - expected_fall
    rise_err = abs(trip_rise - expected_rise)
    fall_err = abs(trip_fall - expected_fall)
    width_err = abs(hyst_width - expected_width)
    valid_ok = valid > 0.7 * vdd
    width_ok = expected_width > 0.015
    ok = valid_ok and width_ok and rise_err <= 0.004 and fall_err <= 0.004 and width_err <= 0.004
    return (
        ok,
        f"trip_rise={trip_rise:.5f}/{expected_rise:.5f} trip_fall={trip_fall:.5f}/{expected_fall:.5f} "
        f"width={hyst_width:.5f}/{expected_width:.5f} valid={valid:.3f} "
        f"events={len(rises)}/{len(falls)}",
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

CHECKER_ID = "v4_111_hysteresis_trip_characterizer"
CHECKER: Checker = check_v3_hysteresis_trip_characterizer
