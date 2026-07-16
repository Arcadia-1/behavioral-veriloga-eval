"""Task-specific checker for canonical v4 DUT 109."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import structured_result


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

def check_v3_comparator_offset_calibration_loop(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "dcmpp", "vinp", "vinn", "offset_est", "valid", "vos_ref"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing comparator offset calibration loop signals"

    vdd = _max_signal_value(rows, ["clk", "dcmpp", "valid"], default=0.9)
    final_t = rows[-1]["time"]
    final_vinp = sample_signal_at(rows, "vinp", final_t)
    final_vinn = sample_signal_at(rows, "vinn", final_t)
    final_est = sample_signal_at(rows, "offset_est", final_t)
    final_valid = sample_signal_at(rows, "valid", final_t)
    ref_offset = sample_signal_at(rows, "vos_ref", final_t)
    if None in (final_vinp, final_vinn, final_est, final_valid, ref_offset):
        return False, "missing_final_calibration_samples"

    assert final_vinp is not None
    assert final_vinn is not None
    assert final_est is not None
    assert final_valid is not None
    assert ref_offset is not None

    final_diff = final_vinp - final_vinn
    final_common = 0.5 * (final_vinp + final_vinn)
    mid_supply = 0.5 * vdd
    diff_err = abs(final_diff - final_est)
    ref_err = abs(final_est - ref_offset)
    cm_err = abs(final_common - mid_supply)
    valid_ok = final_valid > 0.7 * vdd

    times = [row["time"] for row in rows]
    clk_falls = _threshold_crossings(
        [row["clk"] for row in rows],
        times,
        threshold=0.5 * vdd,
        direction="falling",
    )
    valid_edges = _threshold_crossings(
        [row["valid"] for row in rows],
        times,
        threshold=0.5 * vdd,
        direction="rising",
    )
    if len(clk_falls) < 7:
        return False, f"insufficient_calibration_updates={len(clk_falls)}"
    if not valid_edges:
        return False, "valid_never_asserted"

    ok = valid_ok and diff_err <= 0.0025 and ref_err <= 0.0025 and cm_err <= 0.0025
    return (
        ok,
        f"offset_est={final_est:.5f} ref={ref_offset:.5f} diff={final_diff:.5f} "
        f"diff_err={diff_err:.5f} ref_err={ref_err:.5f} cm_err={cm_err:.5f} "
        f"valid={final_valid:.3f} updates={len(clk_falls)} valid_edges={len(valid_edges)}",
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

CHECKER_ID = "v4_109_comparator_offset_calibration_loop"
PROPERTY_IDS = (
    "P_ZERO_INITIAL_ESTIMATE",
    "P_FALLING_EDGE_UPDATE",
    "P_DECISION_DIRECTION",
    "P_SUCCESSIVE_STEP_HALVING",
    "P_SYMMETRIC_DIFFERENTIAL_STIMULUS",
    "P_VALID_COMPLETION",
)
CHECKER: Checker = structured_result(check_v3_comparator_offset_calibration_loop, PROPERTY_IDS)
