"""Task-specific checker for canonical v4 DUT 388."""
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
        if row["time"] < settle_s:
            continue
        prior = _sample_after(rows, row["time"], -settle_s)
        if prior["time"] >= row["time"]:
            continue
        if all(abs(row[name] - prior[name]) <= tol for name in watched):
            samples.append(row)
    return samples

def check_v4_source_follower_buffer_macro(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "vbias", "enable", "rst", "vout", "headroom_metric", "valid"}
    missing = _v4_missing_columns(rows, required)
    if missing:
        return False, missing
    errors = 0
    checked = 0
    clamp_seen = False
    disabled_seen = False
    for row in _v4_settled_sparse_samples(rows, {"vin", "vbias", "enable", "rst"}):
        if row["time"] < 3e-9 or 0.1 < row["enable"] < 0.8 or 0.1 < row["rst"] < 0.8:
            continue
        if row["rst"] > 0.45 or row["enable"] <= 0.45 or row["vbias"] <= 0.10:
            expected_out = 0.0
            expected_metric = 0.0
            expected_valid = 0.0
            disabled_seen = disabled_seen or row["enable"] <= 0.45
        else:
            max_out = row["vbias"] - 0.10
            raw = row["vin"] - 0.12
            expected_out = _v4_clip(raw, 0.0, max_out)
            clamp_seen = clamp_seen or expected_out < raw - 0.04
            expected_metric = _v4_clip(row["vbias"] - expected_out)
            expected_valid = 0.9
        if not _v4_close(row["vout"], expected_out, 0.08):
            errors += 1
        if not _v4_close(row["headroom_metric"], expected_metric, 0.08):
            errors += 1
        if not _v4_close(row["valid"], expected_valid, 0.08):
            errors += 1
        checked += 1
    ok = errors == 0 and checked >= 20 and clamp_seen and disabled_seen
    return ok, f"v4_source_follower checked={checked} clamp_seen={clamp_seen} disabled={disabled_seen} errors={errors}"

CHECKER_ID = "v4_388_source_follower_buffer_macro"
CHECKER: Checker = check_v4_source_follower_buffer_macro
