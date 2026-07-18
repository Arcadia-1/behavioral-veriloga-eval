"""Task-specific checker for canonical v4 DUT 384."""
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

def check_v4_level_shifter_enable_rail_tracking(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "enable", "rst", "vddl", "vddh", "vout", "valid"}
    missing = _v4_missing_columns(rows, required)
    if missing:
        return False, missing
    errors = 0
    checked = 0
    high_seen = False
    low_seen = False
    disabled_seen = False
    rail_values: list[float] = []
    for row in _v4_settled_sparse_samples(rows, {"vin", "enable", "rst", "vddl", "vddh"}):
        if 0.1 < row["enable"] < 0.8 or 0.1 < row["rst"] < 0.8:
            continue
        if row["rst"] > 0.45 or row["enable"] <= 0.45 or row["vddh"] < 0.2:
            expected_out = 0.0
            expected_valid = 0.0
            disabled_seen = disabled_seen or row["enable"] <= 0.45
        else:
            threshold = 0.5 * row["vddl"] if 0.5 * row["vddl"] >= 0.05 else 0.45
            # Treat samples numerically indistinguishable from the threshold as
            # low; Spectre/EVAS can report a few ulps above an exact PWL value.
            expected_out = row["vddh"] if row["vin"] > threshold + 1e-6 else 0.0
            expected_valid = row["vddh"]
            high_seen = high_seen or expected_out > 0.45
            low_seen = low_seen or expected_out <= 0.45
            rail_values.append(row["vddh"])
        if not _v4_close(row["vout"], expected_out, 0.08):
            errors += 1
        if not _v4_close(row["valid"], expected_valid, 0.08):
            errors += 1
        checked += 1
    rail_tracks = rail_values and (max(rail_values) - min(rail_values) > 0.25)
    error_limit = max(1, checked // 500)
    ok = errors <= error_limit and checked >= 20 and high_seen and low_seen and disabled_seen and rail_tracks
    return ok, (
        f"v4_level_shifter checked={checked} errors={errors} high={high_seen} low={low_seen} "
        f"disabled={disabled_seen} rail_tracks={rail_tracks} "
        f"error_limit={error_limit} "
        f"P_LEVEL_TRANSFER mismatch_count={errors} expected=rail_relative_transfer "
        f"observed=checked_rows={checked} "
        f"P_RESET_ENABLE_CLEAR mismatch_count={int(not disabled_seen)} expected=clear_when_inactive "
        f"observed=disabled_seen={disabled_seen}"
    )

CHECKER_ID = "v4_384_level_shifter_enable_rail_tracking"
CHECKER: Checker = check_v4_level_shifter_enable_rail_tracking
