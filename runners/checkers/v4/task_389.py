"""Task-specific checker for canonical v4 DUT 389."""
from __future__ import annotations

from ..api import Checker
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

def _v4_clip(value: float, lo: float = 0.0, hi: float = 0.9) -> float:
    return max(lo, min(hi, value))

def _v4_close(actual: float, expected: float, tol: float = 0.07) -> bool:
    return abs(actual - expected) <= tol

def _v4_sparse_samples(rows: list[dict[str, float]], count: int = 450) -> list[dict[str, float]]:
    if not rows:
        return []
    step = max(1, len(rows) // count)
    return rows[::step]

def _v4_settled_sparse_samples(
    rows: list[dict[str, float]],
    watched: set[str],
    *,
    settle_s: float = 0.5e-9,
    count: int = 450,
    tol: float = 0.02,
) -> list[dict[str, float]]:
    samples: list[dict[str, float]] = []
    for row in _v4_sparse_samples(rows, count=count):
        prior = _sample_after(rows, row["time"], -settle_s)
        if prior["time"] >= row["time"]:
            continue
        if all(abs(row[name] - prior[name]) <= tol for name in watched):
            samples.append(row)
    return samples

def check_v4_cascode_gain_cell_headroom(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "vbias", "vdd_sense", "enable", "rst", "vout", "gain_metric", "headroom_ok"}
    missing = _v4_missing_columns(rows, required)
    if missing:
        return False, f"P_TRACE_CONTRACT mismatch_count=1 expected=required_signals observed={missing}"
    vout_errors = metric_errors = flag_errors = clear_errors = 0
    checked = 0
    clamp_seen = False
    disabled_seen = False
    ok_low_seen = False
    for row in _v4_settled_sparse_samples(rows, {"vin", "vbias", "vdd_sense", "enable", "rst"}):
        if 0.1 < row["enable"] < 0.8 or 0.1 < row["rst"] < 0.8:
            continue
        rail_limit = min(row["vdd_sense"], row["vbias"]) - 0.16
        inactive = row["rst"] > 0.45 or row["enable"] <= 0.45
        if inactive:
            expected_out = 0.45
            expected_metric = 0.0
            expected_ok = 0.0
            disabled_seen = disabled_seen or row["enable"] <= 0.45
        else:
            raw = 0.45 - 1.8 * (row["vin"] - 0.45)
            expected_out = _v4_clip(raw, 0.0, rail_limit)
            clamp_seen = clamp_seen or expected_out < raw - 0.04 or expected_out > raw + 0.04
            expected_metric = abs(expected_out - 0.45)
            expected_ok = 0.9 if rail_limit > 0.50 else 0.0
            ok_low_seen = ok_low_seen or expected_ok <= 0.45
        if not _v4_close(row["vout"], expected_out, 0.09):
            if inactive:
                clear_errors += 1
            else:
                vout_errors += 1
        if not _v4_close(row["gain_metric"], expected_metric, 0.08):
            if inactive:
                clear_errors += 1
            else:
                metric_errors += 1
        if (row["headroom_ok"] > 0.45) != (expected_ok > 0.45):
            if inactive:
                clear_errors += 1
            else:
                flag_errors += 1
        checked += 1
    coverage_errors = int(not clamp_seen) + int(not disabled_seen) + int(not ok_low_seen)
    ok = (
        checked >= 20
        and clear_errors == 0
        and vout_errors == 0
        and metric_errors == 0
        and flag_errors == 0
        and coverage_errors == 0
    )
    notes = [
        f"P_RESET_DISABLE_CLEAR mismatch_count={clear_errors} expected=vout=0.45,metrics=0,headroom_ok=0_when_inactive observed=checked={checked}",
        f"P_CASCODE_TRANSFER mismatch_count={vout_errors} expected=rail_clamped_gain_transfer observed=checked={checked}",
        f"P_GAIN_METRIC mismatch_count={metric_errors} expected=abs(vout-0.45) observed=checked={checked}",
        f"P_HEADROOM_QUALIFICATION mismatch_count={flag_errors} expected=headroom_ok=rail_margin_condition observed=checked={checked}",
        f"P_EXERCISE_COVERAGE mismatch_count={coverage_errors} expected=clamp_disable_and_low_margin_regions observed=clamp={clamp_seen},disabled={disabled_seen},low={ok_low_seen}",
    ]
    return ok, "; ".join(notes)

CHECKER_ID = "v4_389_cascode_gain_cell_headroom"
CHECKER: Checker = check_v4_cascode_gain_cell_headroom
