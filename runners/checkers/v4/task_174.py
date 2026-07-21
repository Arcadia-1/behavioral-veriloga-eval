"""Task-specific checker for canonical v4 DUT 174."""
from __future__ import annotations

from ..api import Checker
from .batch18_diagnostics import bind_properties
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

def check_v3_iterative_isar_dac(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "dcmp", "rst", "clk", "vdac"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing iterative isar dac signals"
    times = [row["time"] for row in rows]
    clk_edges = _threshold_crossings([row["clk"] for row in rows], times, threshold=0.5, direction="rising")
    rst_edges = _threshold_crossings([row["rst"] for row in rows], times, threshold=0.5, direction="rising")
    if len(clk_edges) < 4:
        return False, f"too_few_clk_edges={len(clk_edges)}"
    if not rst_edges:
        return False, "missing_reset_rising_edge"

    failures: list[str] = []
    initial_probe_t = rows[0]["time"] + 0.5 * (rst_edges[0] - rows[0]["time"])
    initial_vdac = sample_signal_at(rows, "vdac", initial_probe_t)
    if initial_vdac is None:
        return False, "missing_initial_vdac_sample"
    if abs(initial_vdac) > 0.02:
        failures.append(f"initial_vdac@{initial_probe_t * 1e9:.3f}ns={initial_vdac:.4f}")

    for rst_t in rst_edges:
        observed = sample_signal_at(rows, "vdac", rst_t + 0.25e-9)
        if observed is None:
            continue
        if abs(observed) > 0.02:
            failures.append(f"reset_vdac@{rst_t * 1e9:.3f}ns={observed:.4f}")

    changes_by_segment: dict[int, list[float]] = {}
    checked_updates = 0
    for clk_t in clk_edges:
        pre = sample_signal_at(rows, "vdac", max(rows[0]["time"], clk_t - 0.08e-9))
        post = sample_signal_at(rows, "vdac", clk_t + 0.25e-9)
        dcmp = sample_signal_at(rows, "dcmp", clk_t + 1e-12)
        if pre is None or post is None or dcmp is None:
            continue
        diff = post - pre
        if abs(diff) < 0.002:
            continue
        expected_sign = -1 if dcmp > 0.5 else 1
        if diff * expected_sign <= 0:
            failures.append(
                f"wrong_update_direction@{clk_t * 1e9:.3f}ns diff={diff:.4f} dcmp={dcmp:.3f}"
            )
        segment = sum(1 for rst_t in rst_edges if rst_t < clk_t)
        changes_by_segment.setdefault(segment, []).append(abs(diff))
        checked_updates += 1

    if checked_updates < 4:
        return False, f"too_few_effective_updates={checked_updates}"

    ratios: list[float] = []
    for segment_changes in changes_by_segment.values():
        for prev, cur in zip(segment_changes, segment_changes[1:]):
            if prev > 0.01 and cur > 0.001:
                ratios.append(cur / prev)
    bad_ratios = [ratio for ratio in ratios if not (0.42 <= ratio <= 0.58)]
    if bad_ratios:
        failures.append("bad_halving_ratios=" + ",".join(f"{ratio:.3f}" for ratio in bad_ratios[:4]))
    if failures:
        return False, " ".join(failures[:5])
    return True, f"updates={checked_updates} ratio_count={len(ratios)}"

CHECKER_ID = "v4_174_iterative_isar_dac"
CHECKER: Checker = bind_properties(check_v3_iterative_isar_dac, (
    "P_RESET_INITIAL_SEARCH_STATE", "P_COMPARATOR_POLARITY_UPDATE",
    "P_RADIX_STEP_REDUCTION", "P_HELD_DAC_OUTPUT",
))
