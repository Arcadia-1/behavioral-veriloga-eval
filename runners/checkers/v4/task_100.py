"""Task-specific checker for canonical v4 DUT 100."""
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

def check_release_converter_front_end_chain(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "clk", "vout", "valid", "coarse"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/vin/clk/vout/valid/coarse"

    times = [r["time"] for r in rows]
    clk_edges = _threshold_crossings([r["clk"] for r in rows], times, threshold=0.45, direction="rising")
    if len(clk_edges) < 6:
        return False, f"too_few_clk_edges={len(clk_edges)}"

    sample_errors: list[float] = []
    coarse_mismatches = 0
    valid_hits = 0
    valid_low_hits = 0
    aperture_sensitive = 0
    for edge_t in clk_edges[:8]:
        vin_edge = sample_signal_at(rows, "vin", edge_t)
        vin_aperture = sample_signal_at(rows, "vin", edge_t + 0.20e-9)
        vout_settled = sample_signal_at(rows, "vout", edge_t + 1.00e-9)
        valid_high = sample_signal_at(rows, "valid", edge_t + 0.80e-9)
        valid_low = sample_signal_at(rows, "valid", edge_t + 3.50e-9)
        coarse = sample_signal_at(rows, "coarse", edge_t + 1.00e-9)
        if None in (vin_edge, vin_aperture, vout_settled, valid_high, valid_low, coarse):
            return False, f"missing_front_end_sample_at={edge_t:.3e}"
        assert vin_edge is not None and vin_aperture is not None and vout_settled is not None
        assert valid_high is not None and valid_low is not None and coarse is not None
        sample_errors.append(abs(vout_settled - vin_aperture))
        expected_coarse_high = vin_aperture > 0.45
        if (coarse > 0.45) != expected_coarse_high:
            coarse_mismatches += 1
        if valid_high > 0.45:
            valid_hits += 1
        if valid_low < 0.45:
            valid_low_hits += 1
        if abs(vin_aperture - vin_edge) > 0.18 and abs(vout_settled - vin_aperture) + 0.08 < abs(vout_settled - vin_edge):
            aperture_sensitive += 1

    max_sample_err = max(sample_errors)
    sample_ok = max_sample_err <= 0.055
    coarse_ok = coarse_mismatches == 0
    valid_ok = valid_hits >= 6 and valid_low_hits >= 6
    aperture_ok = aperture_sensitive >= 2

    droop_windows = 0
    droop_failures = 0
    for start_t, end_t in zip(clk_edges[:7], clk_edges[1:8]):
        t_start = start_t + 2.0e-9
        t_end = end_t - 2.0e-9
        idxs = [idx for idx, row in enumerate(rows) if t_start <= row["time"] <= t_end]
        if len(idxs) < 8:
            continue
        first = rows[idxs[0]]["vout"]
        if first < 0.55:
            continue
        last = rows[idxs[-1]]["vout"]
        droop = first - last
        upward_steps = sum(1 for a, b in zip(idxs[:-1], idxs[1:]) if rows[b]["vout"] - rows[a]["vout"] > 0.004)
        droop_windows += 1
        if not (0.004 <= droop <= 0.16) or upward_steps > max(1, len(idxs) // 8):
            droop_failures += 1

    droop_ok = droop_windows >= 2 and droop_failures == 0
    ok = sample_ok and coarse_ok and valid_ok and aperture_ok and droop_ok
    return ok, (
        f"edges={len(clk_edges)} max_sample_err={max_sample_err:.3f} "
        f"coarse_mismatches={coarse_mismatches} valid_high_hits={valid_hits} "
        f"valid_low_hits={valid_low_hits} aperture_sensitive={aperture_sensitive} "
        f"droop_windows={droop_windows} droop_failures={droop_failures}"
    )

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

CHECKER_ID = "v4_100_sample_hold_droop_front_end"
CHECKER: Checker = check_release_converter_front_end_chain
