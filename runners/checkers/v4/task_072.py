"""Task-specific checker for canonical v4 DUT 072."""
from __future__ import annotations

from ..api import Checker
def sample_signal(rows: list[dict[str, float]], signal: str, time_s: float) -> float | None:
    if not rows or signal not in rows[0] or "time" not in rows[0]:
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
    return rows[-1].get(signal)

def _crossing_times(
    rows: list[dict[str, float]],
    signal: str,
    *,
    threshold: float = 0.45,
    direction: str = "rising",
) -> list[float]:
    if not rows or "time" not in rows[0] or signal not in rows[0]:
        return []
    crossings: list[float] = []
    for idx in range(1, len(rows)):
        prev = rows[idx - 1]
        cur = rows[idx]
        t0 = prev.get("time")
        t1 = cur.get("time")
        v0 = prev.get(signal)
        v1 = cur.get(signal)
        if t0 is None or t1 is None or v0 is None or v1 is None:
            continue
        if direction == "rising":
            hit = v0 <= threshold < v1
        elif direction == "falling":
            hit = v0 >= threshold > v1
        else:
            raise ValueError(f"unsupported direction={direction!r}")
        if not hit:
            continue
        if v1 == v0:
            crossings.append(t1)
        else:
            alpha = (threshold - v0) / (v1 - v0)
            crossings.append(t0 + alpha * (t1 - t0))
    return crossings

def check_track_hold_aperture(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "vin", "vout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/vin/vout"

    edge_times = _crossing_times(rows, "clk", direction="rising")
    if len(edge_times) < 5:
        return False, f"too_few_clk_edges={len(edge_times)}"

    observations: list[float] = []
    expected: list[float] = []
    mismatches = 0
    for edge_time in edge_times[:7]:
        want = sample_signal(rows, "vin", edge_time + 0.20e-9)
        got = sample_signal(rows, "vout", edge_time + 1.00e-9)
        if want is None or got is None:
            continue
        expected.append(want)
        observations.append(got)
        if abs(got - want) > 0.035:
            mismatches += 1

    if len(observations) < 5:
        return False, f"insufficient_aperture_samples={len(observations)}"
    span = max(observations) - min(observations)
    ok = mismatches == 0 and span > 0.40
    obs_text = ",".join(f"{value:.3f}" for value in observations)
    exp_text = ",".join(f"{value:.3f}" for value in expected)
    return ok, f"aperture_samples={obs_text} expected={exp_text} mismatches={mismatches} span={span:.3f}"

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

def _rising_times(rows: list[dict[str, float]], col: str, vth: float = 0.45) -> list[float]:
    times: list[float] = []
    last = rows[0][col] > vth
    for row in rows[1:]:
        cur = row[col] > vth
        if not last and cur:
            times.append(row["time"])
        last = cur
    return times

def check_v4_aperture_delay_track_and_hold(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "VDD", "VSS", "clk", "vin", "vout"}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing[:12])
    base_ok, base_note = check_vbm1_track_hold_aperture(rows)
    if not base_ok:
        return False, base_note

    edges = _rising_times(rows, "clk")
    if len(edges) < 3:
        return False, f"aperture_delay too_few_clk_edges observed={len(edges)} expected>=3 window=full_trace"
    delayed_checks = 0
    hold_checks = 0
    rail_observation_checks = 0
    max_delayed_err = 0.0
    failures: list[str] = []
    for idx, edge_t in enumerate(edges):
        capture_t = edge_t + 0.20e-9
        settle_t = edge_t + 0.38e-9
        vin_edge = sample_signal_at(rows, "vin", edge_t + 0.01e-9)
        vin_capture = sample_signal_at(rows, "vin", capture_t)
        vout = sample_signal_at(rows, "vout", settle_t)
        if None in (vin_edge, vin_capture, vout):
            continue
        assert vin_edge is not None and vin_capture is not None and vout is not None
        delayed_checks += 1
        delayed_err = abs(vout - vin_capture)
        max_delayed_err = max(max_delayed_err, delayed_err)
        if delayed_err > 0.06:
            failures.append(
                f"delayed_capture observed=vout:{vout:.3f} expected=vin_at_aperture:{vin_capture:.3f} "
                f"window={edge_t * 1e9:.3f}ns"
            )
        if abs(vin_capture - vin_edge) > 0.15 and abs(vout - vin_capture) + 0.04 >= abs(vout - vin_edge):
            rail_observation_checks += 1
        if idx + 1 < len(edges):
            hold_t = min(edges[idx + 1] - 0.15e-9, settle_t + 0.55e-9)
            if hold_t > settle_t:
                held = sample_signal_at(rows, "vout", hold_t)
                if held is not None:
                    hold_checks += 1
                    if abs(held - vout) > 0.04:
                        failures.append(
                            f"hold observed=vout:{held:.3f} expected=held:{vout:.3f} "
                            f"window={settle_t * 1e9:.3f}-{hold_t * 1e9:.3f}ns"
                        )
    vdd_span = max(row["VDD"] for row in rows) - min(row["VDD"] for row in rows)
    vss_span = max(row["VSS"] for row in rows) - min(row["VSS"] for row in rows)
    if max(vdd_span, vss_span) > 0.05:
        out_min = min(row["vout"] for row in rows)
        out_max = max(row["vout"] for row in rows)
        vin_min = min(row["vin"] for row in rows)
        vin_max = max(row["vin"] for row in rows)
        if out_min < vin_min - 0.08 or out_max > vin_max + 0.08:
            failures.append(
                f"rail_observability observed=vout_range:{out_min:.3f}-{out_max:.3f} "
                f"expected=unclamped_vin_range:{vin_min:.3f}-{vin_max:.3f} window=full_trace"
            )
    if delayed_checks < 3 or hold_checks < 2:
        failures.append(
            f"insufficient_aperture_checks observed=delayed:{delayed_checks},hold:{hold_checks} "
            "expected=delayed>=3,hold>=2 window=clk_edges"
        )
    if failures:
        return False, " ".join(failures[:5])
    return True, (
        f"{base_note} delayed_checks={delayed_checks} hold_checks={hold_checks} "
        f"max_delayed_err={max_delayed_err:.4f} rail_sensitive_edges={rail_observation_checks}"
    )

check_vbm1_track_hold_aperture = check_track_hold_aperture

CHECKER_ID = "v4_072_aperture_delay_track_and_hold"
CHECKER: Checker = check_v4_aperture_delay_track_and_hold
