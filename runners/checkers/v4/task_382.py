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

def check_v4_programmable_frequency_divider(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk_in", "rst", "enable", "n_3", "n_2", "n_1", "n_0", "clk_div", "ratio_metric", "valid"}
    missing = _v4_missing_columns(rows, required)
    if missing:
        return False, missing
    count = 0
    out_state = 0
    valid = False
    errors = 0
    checked = 0
    toggles = 0
    divisors_seen: set[int] = set()
    for edge_t in _rising_times(rows, "clk_in"):
        edge_row = min(rows, key=lambda row: abs(row["time"] - edge_t))
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
        if (sample["clk_div"] > 0.45) != bool(out_state):
            errors += 1
        if not _v4_close(sample["ratio_metric"], metric, 0.06):
            errors += 1
        if (sample["valid"] > 0.45) != valid:
            errors += 1
        checked += 1
    ok = errors == 0 and checked >= 12 and toggles >= 3 and len(divisors_seen) >= 3
    return ok, (
        f"v4_programmable_divider checked={checked} toggles={toggles} "
        f"divisors={sorted(divisors_seen)} errors={errors}"
    )

CHECKER_ID = "v4_382_programmable_frequency_divider"
CHECKER: Checker = check_v4_programmable_frequency_divider
