"""Task-specific checker for canonical v4 DUT 353."""
from __future__ import annotations

from ..api import Checker
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

def check_v4_ffe_transmitter_3tap(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "data", "clk", "rst", "pre_1", "pre_0", "post_1", "post_0", "vout", "main_dbg", "pre_dbg", "post_dbg"}
    missing = _v4_missing_columns(rows, required)
    if missing:
        return False, missing
    sym0 = 0
    sym1 = 0
    sym2 = 0
    errors = 0
    checked = 0
    pre_codes: set[int] = set()
    post_codes: set[int] = set()
    out_values: list[float] = []
    for edge_t in _rising_times(rows, "clk"):
        edge_row = min(rows, key=lambda row: abs(row["time"] - edge_t))
        if edge_row["rst"] > 0.45:
            sym0 = sym1 = sym2 = 0
            expected_main = expected_pre = expected_post = expected_out = 0.45
        else:
            sym2 = sym1
            sym1 = sym0
            sym0 = 1 if edge_row["data"] > 0.45 else -1
            pre_code = _v4_code(edge_row, ["pre_0", "pre_1"])
            post_code = _v4_code(edge_row, ["post_0", "post_1"])
            pre_codes.add(pre_code)
            post_codes.add(post_code)
            expected_main = 0.45 + 0.18 * sym0
            expected_pre = 0.45 + 0.04 * pre_code * sym1
            expected_post = 0.45 - 0.04 * post_code * sym2
            expected_out = _v4_clip(0.45 + 0.18 * sym0 + 0.04 * pre_code * sym1 - 0.04 * post_code * sym2)
            out_values.append(expected_out)
        sample = _sample_after(rows, edge_t, 0.8e-9)
        if not _v4_close(sample["main_dbg"], expected_main, 0.07):
            errors += 1
        if not _v4_close(sample["pre_dbg"], expected_pre, 0.07):
            errors += 1
        if not _v4_close(sample["post_dbg"], expected_post, 0.07):
            errors += 1
        if not _v4_close(sample["vout"], expected_out, 0.08):
            errors += 1
        checked += 1
    out_span = max(out_values, default=0.45) - min(out_values, default=0.45)
    ok = errors == 0 and checked >= 10 and len(pre_codes) >= 3 and len(post_codes) >= 3 and out_span > 0.25
    return ok, (
        f"v4_ffe checked={checked} pre_codes={sorted(pre_codes)} post_codes={sorted(post_codes)} "
        f"out_span={out_span:.3f} errors={errors}"
    )

CHECKER_ID = "v4_353_ffe_transmitter_3tap"
CHECKER: Checker = check_v4_ffe_transmitter_3tap
