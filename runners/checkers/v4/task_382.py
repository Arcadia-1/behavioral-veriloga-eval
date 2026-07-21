"""Task-specific checker for canonical v4 DUT 382."""
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

def _v4_close(actual: float, expected: float, tol: float = 0.07) -> bool:
    return abs(actual - expected) <= tol

def _inactive_between(rows: list[dict[str, float]], start: float, stop: float) -> bool:
    return any(
        start < row["time"] <= stop
        and (row["rst"] > 0.45 or row["enable"] <= 0.45)
        for row in rows
    )

def check_v4_programmable_frequency_divider(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk_in", "rst", "enable", "n_3", "n_2", "n_1", "n_0", "clk_div", "ratio_metric", "valid"}
    missing = _v4_missing_columns(rows, required)
    if missing:
        return False, missing
    count = 0
    out_state = 0
    valid = False
    clk_errors = 0
    metric_errors = 0
    valid_errors = 0
    first_error_time: float | None = None
    checked = 0
    toggles = 0
    divisors_seen: set[int] = set()
    inactive_since: float | None = None
    reset_clear = False
    disabled_clear = False
    clear_errors = 0
    for row in rows:
        inactive = row["rst"] > 0.45 or row["enable"] <= 0.45
        if inactive:
            if inactive_since is None:
                inactive_since = row["time"]
            if row["time"] - inactive_since >= 500e-12:
                clear = (
                    row["clk_div"] <= 0.12
                    and abs(row["ratio_metric"]) <= 0.08
                    and row["valid"] <= 0.12
                )
                reset_clear = reset_clear or (row["rst"] > 0.45 and clear)
                disabled_clear = disabled_clear or (
                    row["rst"] <= 0.45 and row["enable"] <= 0.45 and clear
                )
                clear_errors += int(not clear)
        else:
            inactive_since = None
    previous_edge = rows[0]["time"]
    for edge_t in _rising_times(rows, "clk_in"):
        edge_row = min(rows, key=lambda row: abs(row["time"] - edge_t))
        if _inactive_between(rows, previous_edge, edge_t):
            count = 0
            out_state = 0
            valid = False
        if edge_row["rst"] > 0.45 or edge_row["enable"] <= 0.45:
            count = 0
            out_state = 0
            valid = False
            divisor = 1
            metric = 0.0
        else:
            divisor = _v4_code(edge_row, ["n_0", "n_1", "n_2", "n_3"]) + 1
            divisors_seen.add(divisor)
            metric = 0.9 * divisor / 16.0
            if count >= divisor - 1:
                count = 0
                out_state = 1 - out_state
                valid = True
                toggles += 1
            else:
                count += 1
        sample = _sample_after(rows, edge_t, 0.8e-9)
        if _inactive_between(rows, edge_t, sample["time"]):
            count = 0
            out_state = 0
            valid = False
            metric = 0.0
        if (sample["clk_div"] > 0.45) != bool(out_state):
            clk_errors += 1
            first_error_time = first_error_time or edge_t
        if not _v4_close(sample["ratio_metric"], metric, 0.06):
            metric_errors += 1
            first_error_time = first_error_time or edge_t
        if (sample["valid"] > 0.45) != valid:
            valid_errors += 1
            first_error_time = first_error_time or edge_t
        checked += 1
        previous_edge = edge_t
    ok = (
        clk_errors + metric_errors + valid_errors == 0
        and clear_errors == 0
        and reset_clear
        and disabled_clear
        and checked >= 12
        and toggles >= 3
        and len(divisors_seen) >= 3
    )
    return ok, (
        f"v4_programmable_divider checked={checked} toggles={toggles} "
        f"divisors={sorted(divisors_seen)} clk_errors={clk_errors} "
        f"metric_errors={metric_errors} valid_errors={valid_errors} "
        f"first_error_time={first_error_time} reset_clear={reset_clear} "
        f"disabled_clear={disabled_clear} clear_errors={clear_errors}"
    )

CHECKER_ID = "v4_382_programmable_frequency_divider"
CHECKER: Checker = check_v4_programmable_frequency_divider
