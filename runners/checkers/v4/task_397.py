"""Task-specific checker for canonical v4 DUT 397."""
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

def check_v4_baseband_offset_gain_trim_macro(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {
        "time",
        "vin",
        "clk",
        "rst",
        "enable",
        "gain_2",
        "gain_1",
        "gain_0",
        "offset_2",
        "offset_1",
        "offset_0",
        "vout",
        "residual_metric",
        "valid",
    }
    missing = _v4_missing_columns(rows, required)
    if missing:
        return False, missing
    valid = False
    errors = 0
    checked = 0
    gain_codes: set[int] = set()
    offset_codes: set[int] = set()
    clipped_seen = False
    disabled_seen = False
    for edge_t in _rising_times(rows, "clk"):
        edge_row = min(rows, key=lambda row: abs(row["time"] - edge_t))
        if edge_row["rst"] > 0.45 or edge_row["enable"] <= 0.45:
            expected_out = 0.45
            expected_metric = 0.0
            valid = False
            disabled_seen = disabled_seen or edge_row["enable"] <= 0.45
        else:
            gain_code = _v4_code(edge_row, ["gain_0", "gain_1", "gain_2"])
            offset_code = _v4_code(edge_row, ["offset_0", "offset_1", "offset_2"])
            gain_codes.add(gain_code)
            offset_codes.add(offset_code)
            raw = 0.45 + (0.7 + 0.1 * gain_code) * (edge_row["vin"] - 0.45) + 0.025 * (offset_code - 3)
            expected_out = _v4_clip(raw)
            clipped_seen = clipped_seen or abs(expected_out - raw) > 0.03
            expected_metric = abs(expected_out - 0.45)
            valid = True
        sample = _sample_after(rows, edge_t, 0.8e-9)
        if not _v4_close(sample["vout"], expected_out, 0.08):
            errors += 1
        if not _v4_close(sample["residual_metric"], expected_metric, 0.07):
            errors += 1
        if (sample["valid"] > 0.45) != valid:
            errors += 1
        checked += 1
    ok = (
        errors == 0
        and checked >= 10
        and len(gain_codes) >= 4
        and len(offset_codes) >= 4
        and disabled_seen
        and clipped_seen
    )
    return ok, (
        f"v4_baseband_trim checked={checked} gain_codes={sorted(gain_codes)} "
        f"offset_codes={sorted(offset_codes)} clipped={clipped_seen} disabled={disabled_seen} errors={errors}"
    )

CHECKER_ID = "v4_397_baseband_offset_gain_trim_macro"
CHECKER: Checker = check_v4_baseband_offset_gain_trim_macro
