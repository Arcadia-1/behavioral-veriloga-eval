"""Task-specific checker for canonical v4 DUT 054."""
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

def check_v3_056_correlated_double_sampler(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "phi_reset", "phi_signal", "vin", "vout", "valid"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing correlated double sampler signals"
    times = [row["time"] for row in rows]
    reset_edges = _threshold_crossings(
        [row["phi_reset"] for row in rows],
        times,
        threshold=0.45,
        direction="rising",
    )
    signal_edges = _threshold_crossings(
        [row["phi_signal"] for row in rows],
        times,
        threshold=0.45,
        direction="rising",
    )
    if len(reset_edges) < 3 or len(signal_edges) < 3:
        return False, f"insufficient_cds_edges=reset{len(reset_edges)}_signal{len(signal_edges)}"

    def _median(values: list[float]) -> float:
        ordered = sorted(values)
        n = len(ordered)
        mid = n // 2
        if n % 2:
            return ordered[mid]
        return 0.5 * (ordered[mid - 1] + ordered[mid])

    reset_outs: list[float] = []
    reset_valids: list[float] = []
    for reset_t in reset_edges:
        sample_t = reset_t + 0.32e-9
        if sample_t >= times[-1]:
            continue
        out = sample_signal_at(rows, "vout", sample_t)
        valid = sample_signal_at(rows, "valid", sample_t)
        if out is None or valid is None:
            return False, f"missing_reset_observable@{reset_t * 1e9:.2f}ns"
        reset_outs.append(out)
        reset_valids.append(valid)
    if len(reset_outs) < 3:
        return False, f"insufficient_cds_reset_observations={len(reset_outs)}"
    vcm = _median(reset_outs)
    max_reset_out_err = max(abs(value - vcm) for value in reset_outs)
    max_reset_valid = max(reset_valids)
    if max_reset_out_err > 0.045:
        return False, f"reset_output_not_common_mode=max_err{max_reset_out_err:.4f}_samples{reset_outs}"
    if max_reset_valid > 0.18:
        return False, f"valid_not_cleared_on_reset=max{max_reset_valid:.4f}"

    signal_valids: list[float] = []
    for signal_t in signal_edges:
        sample_t = signal_t + 0.32e-9
        if sample_t >= times[-1]:
            continue
        valid = sample_signal_at(rows, "valid", sample_t)
        if valid is None:
            return False, f"missing_signal_valid@{signal_t * 1e9:.2f}ns"
        signal_valids.append(valid)
    if len(signal_valids) < 3:
        return False, f"insufficient_cds_signal_observations={len(signal_valids)}"
    vhi = _median(signal_valids)
    if vhi < 0.65:
        return False, f"valid_not_asserted_after_signal=median{vhi:.4f}_samples{signal_valids}"

    checked = 0
    hold_checked = 0
    max_out_err = 0.0
    max_hold_err = 0.0
    deltas: list[float] = []
    clipped_hi = False
    clipped_lo = False
    for signal_t in signal_edges:
        prior_resets = [reset_t for reset_t in reset_edges if reset_t < signal_t]
        if not prior_resets:
            continue
        reset_t = prior_resets[-1]
        reset_v = sample_signal_at(rows, "vin", reset_t + 1e-12)
        signal_v = sample_signal_at(rows, "vin", signal_t + 1e-12)
        got = sample_signal_at(rows, "vout", signal_t + 0.32e-9)
        valid = sample_signal_at(rows, "valid", signal_t + 0.32e-9)
        if reset_v is None or signal_v is None or got is None or valid is None:
            return False, f"missing_cds_pair_observable@{signal_t * 1e9:.2f}ns"
        delta = signal_v - reset_v
        expected_raw = vcm + delta
        expected = min(vhi, max(0.0, expected_raw))
        clipped_hi = clipped_hi or expected_raw > vhi + 0.02
        clipped_lo = clipped_lo or expected_raw < -0.02
        max_out_err = max(max_out_err, abs(got - expected))
        if valid < 0.65 * vhi:
            return False, f"valid_low_after_signal@{signal_t * 1e9:.2f}ns={valid:.4f}"
        deltas.append(delta)
        checked += 1

        next_resets = [reset_t2 for reset_t2 in reset_edges if reset_t2 > signal_t]
        hold_t = signal_t + 0.85e-9
        if next_resets:
            hold_t = min(hold_t, next_resets[0] - 0.20e-9)
        if hold_t > signal_t + 0.36e-9 and hold_t < times[-1]:
            held = sample_signal_at(rows, "vout", hold_t)
            if held is None:
                return False, f"missing_cds_hold@{hold_t * 1e9:.2f}ns"
            max_hold_err = max(max_hold_err, abs(held - expected))
            hold_checked += 1

    if checked < 3 or hold_checked < 2:
        return False, f"insufficient_cds_pair_checks=pair{checked}_hold{hold_checked}"
    if not any(delta > 0.12 for delta in deltas) or not any(delta < -0.12 for delta in deltas):
        return False, f"insufficient_cds_delta_polarity_coverage={deltas}"
    if not clipped_hi:
        return False, f"missing_cds_high_clip_coverage={deltas}"
    if max_out_err > 0.045:
        return False, f"max_cds_output_err={max_out_err:.4f}_vcm={vcm:.4f}_vhi={vhi:.4f}_deltas={deltas}"
    if max_hold_err > 0.045:
        return False, f"max_cds_hold_err={max_hold_err:.4f}_deltas={deltas}"
    return True, (
        f"pairs={checked} hold={hold_checked} vcm={vcm:.4f} vhi={vhi:.4f} "
        f"deltas={[round(delta, 4) for delta in deltas]} max_err={max_out_err:.4f} "
        f"max_hold_err={max_hold_err:.4f} clipped_lo={clipped_lo}"
    )

CHECKER_ID = "v4_054_correlated_double_sampler"
CHECKER: Checker = check_v3_056_correlated_double_sampler
