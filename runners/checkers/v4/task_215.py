"""Task-specific checker for canonical v4 DUT 215."""
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

def _v3_formula_check(
    rows: list[dict[str, float]],
    *,
    required: set[str],
    output: str,
    expected_fn,
    tol: float,
    min_checked: int,
    max_rows: int = 240,
    stable_fn=None,
) -> tuple[bool, str]:
    if not rows or not required.issubset(rows[0]):
        return False, "missing " + "/".join(sorted(required))
    stride = max(1, len(rows) // max_rows)
    checked = 0
    max_err = 0.0
    for row in rows[::stride]:
        if stable_fn is not None and not stable_fn(row):
            continue
        expected = expected_fn(row)
        if expected is None:
            continue
        observed = row.get(output)
        if observed is None:
            return False, f"missing_{output}_sample"
        max_err = max(max_err, abs(observed - expected))
        checked += 1
    if checked < min_checked:
        return False, f"too_few_formula_samples={checked}"
    return max_err <= tol, f"checked={checked} max_error={max_err:.5f}"

def _v3_away_from_edges(row_time: float, edge_times: list[float], margin_s: float = 80e-12) -> bool:
    return all(abs(row_time - edge_time) > margin_s for edge_time in edge_times)

def _v3_stable_formula_check(
    rows: list[dict[str, float]],
    *,
    required: set[str],
    output: str,
    logic_signals: list[str],
    threshold: float,
    expected_fn,
    tol: float,
    min_checked: int,
    margin_s: float = 80e-12,
) -> tuple[bool, str]:
    if not rows or not required.issubset(rows[0]):
        return False, "missing " + "/".join(sorted(required))
    edge_times: list[float] = []
    for signal in logic_signals:
        edge_times.extend(
            _signal_threshold_edges(
                rows,
                signal,
                threshold=threshold,
                directions=("rising", "falling"),
            )
        )

    def stable(row: dict[str, float]) -> bool:
        row_time = row.get("time")
        if row_time is None or row_time < 50e-12:
            return False
        if not _v3_away_from_edges(row_time, edge_times, margin_s=margin_s):
            return False
        return all(abs(row[signal] - threshold) > 0.05 for signal in logic_signals)

    return _v3_formula_check(
        rows,
        required=required,
        output=output,
        expected_fn=expected_fn,
        tol=tol,
        min_checked=min_checked,
        stable_fn=stable,
    )

def check_v3_lt_read_sar7b_weighted(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vout", "gnd", *{f"d{i}" for i in range(8)}}
    if not rows or not required.issubset(rows[0]):
        return False, "missing lt read sar7b weighted signals"
    vth = 0.45
    weights = {7: 1.0, 6: 0.5, 5: 0.25, 4: 0.125, 3: 0.0625, 2: 0.03125, 1: 0.015625, 0: 0.0078125}

    def expected(row: dict[str, float]) -> float:
        total = sum(weight if row[f"d{bit}"] > vth else 0.0 for bit, weight in weights.items())
        return -0.9 + 0.9 * total

    return _v3_stable_formula_check(
        rows,
        required=required,
        output="vout",
        logic_signals=[f"d{i}" for i in range(8)],
        threshold=vth,
        expected_fn=expected,
        tol=0.035,
        min_checked=20,
    )

CHECKER_ID = "v4_215_lt_read_sar7b_weighted"
CHECKER: Checker = check_v3_lt_read_sar7b_weighted
