"""Task-specific checker for canonical v4 DUT 375."""
from __future__ import annotations

from statistics import median

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


def _event_period(rows: list[dict[str, float]], col: str) -> float:
    rising = _rising_times(rows, col)
    periods = [right - left for left, right in zip(rising, rising[1:]) if right > left]
    return float(median(periods)) if periods else 0.0


def _falling_times(rows: list[dict[str, float]], col: str, vth: float = 0.45) -> list[float]:
    times: list[float] = []
    last = rows[0][col] > vth
    for row in rows[1:]:
        cur = row[col] > vth
        if last and not cur:
            times.append(row["time"])
        last = cur
    return times


def _sample_after(rows: list[dict[str, float]], t: float, delay: float) -> dict[str, float]:
    target = t + max(0.0, delay)
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
    period = _event_period(rows, "clk_in")
    rise_delay = 0.22 * period if period > 0.0 else 1.8e-9
    disable_delay = 0.10 * period if period > 0.0 else 0.8e-9
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
    valid_seen = any(row["enable"] > 0.45 and row["valid"] > 0.45 for row in rows)
    inactive_since: float | None = None
    reset_clear = False
    disabled_clear = False
    clear_errors = 0
    valid_latched = False
    valid_errors = 0
    for row in rows:
        inactive = row["rst"] > 0.45 or row["enable"] <= 0.45
        if inactive:
            valid_latched = False
            if inactive_since is None:
                inactive_since = row["time"]
            if row["time"] - inactive_since >= 500e-12:
                clear = all(
                    row[name] <= 0.12
                    for name in ("phi1", "phi2", "deadtime_metric", "valid")
                )
                reset_clear = reset_clear or (row["rst"] > 0.45 and clear)
                disabled_clear = disabled_clear or (
                    row["rst"] <= 0.45 and row["enable"] <= 0.45 and clear
                )
                clear_errors += int(not clear)
            continue
        inactive_since = None
        if row["valid"] > 0.45:
            valid_latched = True
        elif valid_latched:
            valid_errors += 1
    disable_samples = [
        _sample_after(rows, edge_t, disable_delay)
        for edge_t in _falling_times(rows, "enable")
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
        sample = _sample_after(rows, edge_t, rise_delay)
        if edge_row["rst"] <= 0.45 and edge_row["enable"] > 0.45 and sample["enable"] > 0.45:
            checked_rise += 1
            if sample["phi1"] <= 0.45 or sample["phi2"] > 0.45:
                errors += 1
    for edge_t in _falling_times(rows, "clk_in"):
        edge_row = min(rows, key=lambda row: abs(row["time"] - edge_t))
        sample = _sample_after(rows, edge_t, rise_delay)
        if edge_row["rst"] <= 0.45 and edge_row["enable"] > 0.45 and sample["enable"] > 0.45:
            checked_fall += 1
            if sample["phi2"] <= 0.45 or sample["phi1"] > 0.45:
                errors += 1
    ok = (
        overlap == 0
        and dead_seen
        and valid_seen
        and reset_clear
        and disabled_clear
        and disable_clears
        and clear_errors == 0
        and valid_errors == 0
        and errors == 0
        and checked_rise >= 3
        and checked_fall >= 3
    )
    return ok, (
        "v4_nonoverlap_clock "
        f"rise={checked_rise} fall={checked_fall} errors={errors} overlap={overlap} "
        f"dead_seen={dead_seen} valid_seen={valid_seen} reset_clear={reset_clear} "
        f"disabled_clear={disabled_clear} disable_clears={disable_clears} "
        f"clear_errors={clear_errors} valid_errors={valid_errors}"
    )

CHECKER_ID = "v4_375_nonoverlap_clock_generator"
CHECKER: Checker = check_v4_nonoverlap_clock_generator
