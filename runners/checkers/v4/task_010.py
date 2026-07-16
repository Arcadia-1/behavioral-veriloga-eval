"""Task-specific checker for canonical v4 DUT 010."""
from __future__ import annotations

from ..api import Checker
def rising_edges(values: list[float], times: list[float], threshold: float = 0.45) -> list[float]:
    edges: list[float] = []
    for i in range(1, len(values)):
        if values[i - 1] < threshold <= values[i]:
            edges.append(times[i])
    return edges

def _logic_state(value: float, threshold: float = 0.45) -> str:
    return "H" if value > threshold else "L"

def check_release_offset_comparator(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "vinp", "vinn", "out_p"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/vinp/vinn/out_p"

    times = [r["time"] for r in rows]
    clk_vals = [r["clk"] for r in rows]
    out_vals = [r["out_p"] for r in rows]
    out_span = max(out_vals) - min(out_vals)
    if out_span < 0.60:
        return False, f"output_span_too_small={out_span:.3f}"

    edge_times = rising_edges(clk_vals, times, threshold=0.45)
    if len(edge_times) < 7:
        return False, f"too_few_clock_edges={len(edge_times)}"

    vos = 5e-3
    sample_delay = 0.50e-9
    expected: list[str] = []
    observed: list[str] = []
    diffs_mv: list[float] = []
    mismatches = 0
    for edge_t in edge_times[:7]:
        sample_t = edge_t + sample_delay
        vinp = sample_signal_at(rows, "vinp", edge_t)
        vinn = sample_signal_at(rows, "vinn", edge_t)
        out_p = sample_signal_at(rows, "out_p", sample_t)
        if vinp is None or vinn is None or out_p is None:
            return False, f"missing_sample_near_edge={edge_t * 1e9:.2f}ns"
        diff_v = vinp - vinn
        diffs_mv.append(diff_v * 1e3)
        want = "H" if diff_v > vos else "L"
        got = _logic_state(out_p)
        expected.append(want)
        observed.append(got)
        if got != want:
            mismatches += 1

    sequence = "".join(observed)
    expected_sequence = "".join(expected)
    has_below_offset_positive = any(0.0 <= mv < vos * 1e3 for mv, want in zip(diffs_mv, expected) if want == "L")
    has_above_offset_positive = any(mv > vos * 1e3 for mv, want in zip(diffs_mv, expected) if want == "H")
    has_negative_low = any(mv < -1.0 for mv, want in zip(diffs_mv, expected) if want == "L")
    ok = (
        mismatches == 0
        and sequence == "LLLHHLL"
        and has_below_offset_positive
        and has_above_offset_positive
        and has_negative_low
    )
    diff_text = ",".join(f"{mv:.1f}" for mv in diffs_mv)
    return ok, (
        f"offset_decisions={sequence} expected={expected_sequence} "
        f"diffs_mv=[{diff_text}] mismatches={mismatches} "
        f"below_offset_positive={has_below_offset_positive} "
        f"above_offset_positive={has_above_offset_positive}"
    )

def check_v3_offset_comparator(rows: list[dict[str, float]]) -> tuple[bool, str]:
    base_ok, base_msg = check_release_offset_comparator(rows)
    if not base_ok:
        return False, base_msg

    required = {"time", "vdd", "vss", "out_p"}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing)

    times = [row["time"] for row in rows]
    edge_times = rising_edges([row["clk"] for row in rows], times)
    periods = [right - left for left, right in zip(edge_times, edge_times[1:])]
    if len(edge_times) < 7 or not periods:
        return False, "too_few_clock_edges"
    nominal_period = sorted(periods)[len(periods) // 2]
    sample_delay = 0.125 * nominal_period
    sample_plan: list[tuple[float, str, str]] = []
    previous_expected = "L"
    for index, edge_time in enumerate(edge_times[:7]):
        vinp = sample_signal_at(rows, "vinp", edge_time)
        vinn = sample_signal_at(rows, "vinn", edge_time)
        if vinp is None or vinn is None:
            return False, f"missing_inputs_at_edge={index}"
        expected = "H" if vinp - vinn > 5e-3 else "L"
        sample_plan.append((edge_time + sample_delay, expected, f"edge_{index}"))
        if index > 0:
            sample_plan.append((edge_time - sample_delay, previous_expected, f"hold_before_edge_{index}"))
        previous_expected = expected
    failures: list[str] = []
    observed: list[str] = []
    for time_s, expected, label in sample_plan:
        value = sample_signal_at(rows, "out_p", time_s)
        if value is None:
            failures.append(f"{label}=missing")
            observed.append("?")
            continue
        vdd = sample_signal_at(rows, "vdd", time_s)
        vss = sample_signal_at(rows, "vss", time_s)
        if vdd is None or vss is None or vdd <= vss:
            failures.append(f"{label}:invalid_rails")
            observed.append("?")
            continue
        span = vdd - vss
        state = "H" if value > vss + 0.5 * span else "L"
        observed.append(state)
        if state != expected:
            failures.append(f"{label}:{state}!={expected}@{value:.3f}")
        if expected == "H" and value < vdd - 0.1 * span:
            failures.append(f"{label}:high_not_rail={value:.3f}<min={vdd - 0.1 * span:.3f}")
        if expected == "L" and value > vss + 0.1 * span:
            failures.append(f"{label}:low_not_rail={value:.3f}>max={vss + 0.1 * span:.3f}")

    ok = not failures
    return ok, base_msg + " strict_samples=" + "".join(observed) + (" " + " ".join(failures) if failures else "")

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

CHECKER_ID = "v4_010_offset_comparator"
CHECKER: Checker = check_v3_offset_comparator
