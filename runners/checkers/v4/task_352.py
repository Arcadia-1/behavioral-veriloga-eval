"""Task-specific checker for canonical v4 DUT 352."""
from __future__ import annotations

from checkers.api import Checker
def _rising_times(rows: list[dict[str, float]], col: str, vth: float = 0.45) -> list[float]:
    times: list[float] = []
    last = rows[0][col] > vth
    for row in rows[1:]:
        cur = row[col] > vth
        if not last and cur:
            times.append(row["time"])
        last = cur
    return times

def _sample_after(rows: list[dict[str, float]], t: float, delay: float = 5e-9) -> dict[str, float]:
    target = t + delay
    return min(rows, key=lambda row: abs(row["time"] - target))

def _v4_missing_columns(rows: list[dict[str, float]], required: set[str]) -> str | None:
    if not rows:
        return "missing_columns=" + ",".join(sorted(required)[:16])
    missing = sorted(required - set(rows[0].keys()))
    if missing:
        return "missing_columns=" + ",".join(missing[:16])
    return None

def _v4_code(row: dict[str, float], names_lsb_first: list[str], vth: float = 0.45) -> int:
    return sum((1 << bit) for bit, name in enumerate(names_lsb_first) if row[name] > vth)

def _v4_clip(value: float, lo: float = 0.0, hi: float = 0.9) -> float:
    return max(lo, min(hi, value))

def _v4_close(actual: float, expected: float, tol: float = 0.07) -> bool:
    return abs(actual - expected) <= tol

def check_v4_ctle_equalizer_macro(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "clk", "rst", "boost_2", "boost_1", "boost_0", "vout", "edge_metric", "sat_flag"}
    missing = _v4_missing_columns(rows, required)
    if missing:
        return False, missing
    prev_in = 0.45
    errors = 0
    checked = 0
    codes_seen: set[int] = set()
    sat_seen = False
    metric_seen = False
    for edge_t in _rising_times(rows, "clk"):
        edge_row = min(rows, key=lambda row: abs(row["time"] - edge_t))
        if edge_row["rst"] > 0.45:
            prev_in = 0.45
            expected_out = 0.45
            expected_metric = 0.0
            expected_sat = 0.0
        else:
            code = _v4_code(edge_row, ["boost_0", "boost_1", "boost_2"])
            codes_seen.add(code)
            edge = edge_row["vin"] - prev_in
            raw = 0.45 + (edge_row["vin"] - 0.45) + 0.08 * code * edge
            expected_sat = 0.9 if raw > 0.9 or raw < 0.0 else 0.0
            expected_out = _v4_clip(raw)
            expected_metric = min(0.9, abs(0.08 * code * edge))
            sat_seen = sat_seen or expected_sat > 0.45
            metric_seen = metric_seen or expected_metric > 0.03
            prev_in = edge_row["vin"]
        sample = _sample_after(rows, edge_t, 0.8e-9)
        if not _v4_close(sample["vout"], expected_out, 0.08):
            errors += 1
        if not _v4_close(sample["edge_metric"], expected_metric, 0.07):
            errors += 1
        if (sample["sat_flag"] > 0.45) != (expected_sat > 0.45):
            errors += 1
        checked += 1
    ok = errors == 0 and checked >= 8 and len(codes_seen) >= 4 and metric_seen and sat_seen
    return ok, (
        f"v4_ctle checked={checked} codes={sorted(codes_seen)} metric_seen={metric_seen} "
        f"sat_seen={sat_seen} errors={errors}"
    )

CHECKER_ID = "v4_352_ctle_equalizer_macro"
CHECKER: Checker = check_v4_ctle_equalizer_macro
