"""Task-specific checker for canonical v4 DUT 223."""
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

def _signal_threshold_edges(
    rows: list[dict[str, float]],
    signal: str,
    *,
    threshold: float = 0.45,
    directions: tuple[str, ...] = ("rising", "falling"),
) -> list[float]:
    times = [row["time"] for row in rows]
    values = [row[signal] for row in rows]
    edges: list[float] = []
    for direction in directions:
        edges.extend(_threshold_crossings(values, times, threshold=threshold, direction=direction))
    return sorted(edges)

def _v3_away_from_edges(row_time: float, edge_times: list[float], margin_s: float = 80e-12) -> bool:
    return all(abs(row_time - edge_time) > margin_s for edge_time in edge_times)

def check_v3_therm8_to_bin4_count(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "b0", "b1", "b2", "b3", *{f"th{i}" for i in range(8)}}
    if not rows or not required.issubset(rows[0]):
        return False, "missing therm8 to bin4 count signals"
    input_signals = [f"th{i}" for i in range(8)]
    threshold = 0.45
    edge_times: list[float] = []
    for signal in input_signals:
        edge_times.extend(_signal_threshold_edges(rows, signal, threshold=threshold, directions=("rising", "falling")))
    checked = 0
    max_err = 0.0
    counts_seen: set[int] = set()
    failures: list[str] = []
    bit_mismatches = 0
    code_mismatches = 0
    arbitrary_pattern_mismatches = 0
    stride = max(1, len(rows) // 120)
    for row in rows[::stride]:
        if row["time"] < 0.05e-9 or not _v3_away_from_edges(row["time"], edge_times, margin_s=90e-12):
            continue
        count = sum(1 for signal in input_signals if row[signal] > threshold)
        counts_seen.add(count)
        checked += 1
        observed_code = sum(
            1 << bit for bit in range(4) if row[f"b{bit}"] > threshold
        )
        row_bit_mismatches = 0
        for bit in range(4):
            signal = f"b{bit}"
            expected = 0.9 if ((count >> bit) & 1) else 0.0
            err = abs(row[signal] - expected)
            max_err = max(max_err, err)
            if err > 0.08:
                failures.append(f"{signal}@{row['time'] * 1e9:.3f}ns={row[signal]:.3f} expected={expected:.3f}")
                row_bit_mismatches += 1
        bit_mismatches += row_bit_mismatches
        code_mismatches += int(observed_code != count)
        high_pattern = [row[signal] > threshold for signal in input_signals]
        is_prefix = high_pattern == sorted(high_pattern, reverse=True)
        if not is_prefix and observed_code != count:
            arbitrary_pattern_mismatches += 1
    coverage_errors = int(checked < 20) + int(len(counts_seen) < 3)
    ok = coverage_errors == 0 and not failures
    detail = " ".join(failures[:6]) or "popcount_outputs_match"
    return ok, (
        f"{detail} checked={checked} counts={sorted(counts_seen)} max_err={max_err:.3f} "
        f"coverage_errors={coverage_errors}; "
        f"P_COUNT_HOW_MANY_OF_TH0_TH7 mismatch_count={code_mismatches}; "
        f"P_ENCODE_THE_COUNT_AS_A_4 mismatch_count={code_mismatches}; "
        f"P_DRIVE_B0_B3_AS_VOLTAGE_CODED mismatch_count={bit_mismatches}; "
        f"P_SUPPORT_ANY_INPUT_PATTERN_BY_COUNTING mismatch_count={arbitrary_pattern_mismatches}"
    )

CHECKER_ID = "v4_223_therm8_to_bin4_count"
CHECKER: Checker = check_v3_therm8_to_bin4_count
