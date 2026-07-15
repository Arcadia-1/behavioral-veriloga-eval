"""Task-specific checker for canonical v4 DUT 018."""
from __future__ import annotations

from ..api import Checker
def check_vbm1_thermometer_dac_15seg(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "empty"
    seg_names = [f"seg{i}" for i in range(15)]
    required = {"time", "aout", *seg_names}
    if not required.issubset(rows[0]):
        return False, f"missing time/aout/seg0..seg14; keys={list(rows[0].keys())[:10]}"

    checkpoints = [
        (15e-9, 0),
        (45e-9, 1),
        (75e-9, 2),
        (105e-9, 7),
        (135e-9, 14),
        (165e-9, 15),
    ]
    levels: list[tuple[int, float]] = []
    errors: list[float] = []
    notes: list[str] = []
    for target_t, expected_count in checkpoints:
        row = min(rows, key=lambda r: abs(r["time"] - target_t))
        observed_count = sum(1 for name in seg_names if row[name] > 0.45)
        expected_v = 0.9 * expected_count / 15.0
        error = abs(row["aout"] - expected_v)
        levels.append((expected_count, row["aout"]))
        errors.append(error)
        notes.append(f"{expected_count}:{row['aout']:.3f}/{observed_count}")

    monotonic = all(levels[i][1] <= levels[i + 1][1] + 1e-6 for i in range(len(levels) - 1))
    counts_match = all(
        sum(1 for name in seg_names if min(rows, key=lambda r, t=t: abs(r["time"] - t))[name] > 0.45) == count
        for t, count in checkpoints
    )
    max_err = max(errors)
    full_scale_ok = abs(levels[-1][1] - 0.9) <= 0.02
    ok = counts_match and monotonic and max_err <= 0.02 and full_scale_ok
    return ok, (
        f"levels={' '.join(notes)} max_err={max_err:.3f} "
        f"monotonic={monotonic} counts_match={counts_match} "
        f"full_scale_ok={full_scale_ok}"
    )

CHECKER_ID = "v4_018_unit_element_thermometer_dac"
CHECKER: Checker = check_vbm1_thermometer_dac_15seg
