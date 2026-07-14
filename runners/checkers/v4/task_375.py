"""Task-specific checker for canonical v4 DUT 375."""
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

def _falling_times(rows: list[dict[str, float]], col: str, vth: float = 0.45) -> list[float]:
    times: list[float] = []
    last = rows[0][col] > vth
    for row in rows[1:]:
        cur = row[col] > vth
        if last and not cur:
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

def check_v4_nonoverlap_clock_generator(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk_in", "rst", "enable", "phi1", "phi2", "deadtime_metric", "valid"}
    missing = _v4_missing_columns(rows, required)
    if missing:
        return False, missing
    overlap = sum(
        1
        for row in rows
        if row["rst"] <= 0.45 and row["enable"] > 0.45 and row["phi1"] > 0.45 and row["phi2"] > 0.45
    )
    dead_seen = any(
        row["rst"] <= 0.45
        and row["enable"] > 0.45
        and row["deadtime_metric"] > 0.45
        and row["phi1"] <= 0.45
        and row["phi2"] <= 0.45
        for row in rows
    )
    valid_seen = any(row["time"] > 15e-9 and row["enable"] > 0.45 and row["valid"] > 0.45 for row in rows)
    disable_samples = [
        _sample_after(rows, edge_t, 0.8e-9)
        for edge_t in _falling_times(rows, "enable")
        if edge_t > 1e-9
    ]
    disable_clears = bool(disable_samples) and all(
        row["enable"] <= 0.45
        and row["rst"] <= 0.45
        and row["phi1"] <= 0.45
        and row["phi2"] <= 0.45
        and row["valid"] <= 0.45
        for row in disable_samples
    )
    errors = 0
    checked_rise = 0
    checked_fall = 0
    for edge_t in _rising_times(rows, "clk_in"):
        edge_row = min(rows, key=lambda row: abs(row["time"] - edge_t))
        sample = _sample_after(rows, edge_t, 1.8e-9)
        if edge_row["rst"] <= 0.45 and edge_row["enable"] > 0.45 and sample["enable"] > 0.45:
            checked_rise += 1
            if sample["phi1"] <= 0.45 or sample["phi2"] > 0.45:
                errors += 1
    for edge_t in _falling_times(rows, "clk_in"):
        edge_row = min(rows, key=lambda row: abs(row["time"] - edge_t))
        sample = _sample_after(rows, edge_t, 1.8e-9)
        if edge_row["rst"] <= 0.45 and edge_row["enable"] > 0.45 and sample["enable"] > 0.45:
            checked_fall += 1
            if sample["phi2"] <= 0.45 or sample["phi1"] > 0.45:
                errors += 1
    ok = overlap == 0 and dead_seen and valid_seen and disable_clears and errors == 0 and checked_rise >= 3 and checked_fall >= 3
    return ok, (
        "v4_nonoverlap_clock "
        f"rise={checked_rise} fall={checked_fall} errors={errors} overlap={overlap} "
        f"dead_seen={dead_seen} valid_seen={valid_seen} disable_clears={disable_clears}"
    )

CHECKER_ID = "v4_375_nonoverlap_clock_generator"
CHECKER: Checker = check_v4_nonoverlap_clock_generator
