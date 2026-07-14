"""Task-specific checker for canonical v4 DUT 064."""
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

def check_v4_edge_delay_line_with_deglitch(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "rst", "enable", "vout", "edge_valid", "rejected"}
    missing = _v4_missing_columns(rows, required)
    if missing:
        return False, missing
    reset_rows = [row for row in rows if row["rst"] > 0.45]
    if reset_rows:
        reset_peak = max(max(row["vout"], row["edge_valid"], row["rejected"]) for row in reset_rows)
        if reset_peak > 0.16:
            return False, (
                f"v4_delay_line reset_clear observed=max_output:{reset_peak:.3f} "
                "expected<=0.16 window=rst_high"
            )
    times = [row["time"] for row in rows]
    input_values = [row["vin"] for row in rows]
    output_values = [row["vout"] for row in rows]
    input_edges = sorted(
        _threshold_crossings(input_values, times, threshold=0.45, direction="rising")
        + _threshold_crossings(input_values, times, threshold=0.45, direction="falling")
    )
    output_edges = sorted(
        _threshold_crossings(output_values, times, threshold=0.45, direction="rising")
        + _threshold_crossings(output_values, times, threshold=0.45, direction="falling")
    )
    if len(input_edges) < 5:
        return False, f"v4_delay_line too_few_input_edges observed={len(input_edges)} expected>=5 window=full_trace"
    if len(output_edges) < 2:
        return False, f"v4_delay_line too_few_output_edges observed={len(output_edges)} expected>=2 window=full_trace"

    wide_matches = 0
    early_errors = 0
    delays: list[float] = []
    for in_edge in input_edges:
        if in_edge < 2.0e-9:
            continue
        before = sample_signal_at(rows, "vout", max(rows[0]["time"], in_edge + 0.45e-9))
        if before is None:
            continue
        in_after = sample_signal_at(rows, "vin", min(rows[-1]["time"], in_edge + 0.70e-9))
        if in_after is None:
            continue
        stable_after = sample_signal_at(rows, "vin", min(rows[-1]["time"], in_edge + 1.40e-9))
        if stable_after is None:
            continue
        is_wide = (in_after > 0.45) == (stable_after > 0.45)
        later_edges = [out_edge for out_edge in output_edges if 0.8e-9 <= out_edge - in_edge <= 3.2e-9]
        if is_wide and later_edges:
            wide_matches += 1
            delays.append(later_edges[0] - in_edge)
        if later_edges and abs(before - (0.9 if in_after > 0.45 else 0.0)) < 0.12 and later_edges[0] - in_edge < 0.8e-9:
            early_errors += 1

    rejected_seen = any(row["rejected"] > 0.45 for row in rows)
    valid_seen = any(row["edge_valid"] > 0.45 for row in rows)
    disabled_clears = False
    for row in rows:
        if row["enable"] <= 0.45 and row["time"] > 48.5e-9 and row["vout"] < 0.2:
            disabled_clears = True
            break
    min_delay = min(delays, default=0.0)
    max_delay = max(delays, default=0.0)
    ok = (
        wide_matches >= 2
        and early_errors == 0
        and rejected_seen
        and valid_seen
        and disabled_clears
        and 1.8e-9 <= min_delay <= 3.2e-9
        and max_delay <= 3.4e-9
    )
    if not ok:
        return False, (
            f"v4_delay_line_contract observed=wide_matches:{wide_matches},delay_range:({min_delay:.3e},{max_delay:.3e}),"
            f"rejected:{rejected_seen},valid:{valid_seen},disabled_clears:{disabled_clears},early_errors:{early_errors} "
            "expected=wide_matches>=2,delay=1.8..3.4ns,rejected/valid/disabled_clear,true,no_early "
            "window=full_trace"
        )
    return ok, (
        f"v4_delay_line input_edges={len(input_edges)} output_edges={len(output_edges)} "
        f"wide_matches={wide_matches} delay_range=({min_delay:.3e},{max_delay:.3e}) "
        f"rejected={rejected_seen} valid={valid_seen} disabled_clears={disabled_clears} early_errors={early_errors}"
    )

CHECKER_ID = "v4_064_edge_delay_line_with_deglitch"
CHECKER: Checker = check_v4_edge_delay_line_with_deglitch
