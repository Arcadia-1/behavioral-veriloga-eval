"""Task-specific checker for canonical v4 DUT 180."""
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

def _v4_missing_columns(rows: list[dict[str, float]], required: set[str]) -> str | None:
    if not rows:
        return "missing_columns=" + ",".join(sorted(required)[:16])
    missing = sorted(required - set(rows[0].keys()))
    if missing:
        return "missing_columns=" + ",".join(missing[:16])
    return None

def check_v4_track_hold_with_droop_and_aperture(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "track", "rst", "enable", "vhold", "aperture_metric", "droop_metric", "valid"}
    missing = _v4_missing_columns(rows, required)
    if missing:
        return False, missing
    times = [row["time"] for row in rows]
    track_values = [row["track"] for row in rows]
    falls = _threshold_crossings(track_values, times, threshold=0.45, direction="falling")
    rises = _threshold_crossings(track_values, times, threshold=0.45, direction="rising")

    def evaluate(aperture_gain: float) -> dict[str, object]:
        checked = 0
        errors = 0
        aperture_seen = False
        droop_seen = False
        hold_windows = 0
        for fall in falls:
            rst = sample_signal_at(rows, "rst", min(rows[-1]["time"], fall + 0.05e-9))
            enable = sample_signal_at(rows, "enable", min(rows[-1]["time"], fall + 0.05e-9))
            if rst is None or enable is None or rst > 0.45 or enable <= 0.45:
                continue
            next_rise = min((rise for rise in rises if rise > fall + 0.5e-9), default=rows[-1]["time"])
            if next_rise - fall < 2.0e-9:
                continue
            vin_at_fall = sample_signal_at(rows, "vin", fall + 0.05e-9)
            old_hold = sample_signal_at(rows, "vhold", max(rows[0]["time"], fall - 0.35e-9))
            sample_t = min(rows[-1]["time"], fall + 0.55e-9)
            later_t = min(next_rise - 0.45e-9, fall + 4.2e-9, rows[-1]["time"])
            observed = {
                "vhold": sample_signal_at(rows, "vhold", sample_t),
                "aperture_metric": sample_signal_at(rows, "aperture_metric", sample_t),
                "valid": sample_signal_at(rows, "valid", sample_t),
                "vhold_later": sample_signal_at(rows, "vhold", later_t),
                "droop_metric_later": sample_signal_at(rows, "droop_metric", later_t),
            }
            if vin_at_fall is None or old_hold is None or any(value is None for value in observed.values()):
                continue
            expected_aperture = min(0.9, aperture_gain * abs(vin_at_fall - old_hold))
            if abs(float(observed["vhold"]) - vin_at_fall) > 0.09:
                errors += 1
            if abs(float(observed["aperture_metric"]) - expected_aperture) > 0.05:
                errors += 1
            if float(observed["valid"]) <= 0.45:
                errors += 1
            if later_t > fall + 2.0e-9:
                if float(observed["vhold_later"]) > float(observed["vhold"]) - 0.015:
                    errors += 1
                if float(observed["droop_metric_later"]) <= 0.015:
                    errors += 1
                droop_seen = True
            aperture_seen = aperture_seen or expected_aperture > 0.04
            hold_windows += 1
            checked += 1
        return {
            "aperture_gain": aperture_gain,
            "checked": checked,
            "errors": errors,
            "aperture_seen": aperture_seen,
            "droop_seen": droop_seen,
            "hold_windows": hold_windows,
        }

    candidates = [evaluate(0.6), evaluate(0.55)]
    best = min(candidates, key=lambda item: int(item["errors"]))
    disabled_clears = any(
        row["time"] > 68e-9
        and row["enable"] <= 0.45
        and row["valid"] < 0.20
        and row["vhold"] < 0.20
        and row["droop_metric"] < 0.20
        for row in rows
    )
    ok = (
        int(best["checked"]) >= 3
        and int(best["errors"]) == 0
        and bool(best["aperture_seen"])
        and bool(best["droop_seen"])
        and disabled_clears
    )
    return ok, (
        f"v4_track_hold aperture_gain={float(best['aperture_gain']):.2f} checked={best['checked']} "
        f"errors={best['errors']} aperture={best['aperture_seen']} droop={best['droop_seen']} "
        f"disabled_clears={disabled_clears}"
    )

CHECKER_ID = "v4_180_track_hold_with_droop_and_aperture"
CHECKER: Checker = check_v4_track_hold_with_droop_and_aperture
