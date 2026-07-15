"""Task-specific checker for canonical v4 DUT 134."""
from __future__ import annotations

from ..api import Checker
def _check_affine_transfer_coverage(
    rows: list[dict[str, float]],
    *,
    required: set[str],
    output: str,
    expected_fn: Callable[[dict[str, float]], float],
    drive_fn: Callable[[dict[str, float]], float],
    label: str,
    tolerance: float,
    min_span: float,
) -> tuple[bool, str]:
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0])) if rows else sorted(required)
        return False, f"missing_{label}_columns=" + ",".join(missing)
    checked = 0
    max_err = 0.0
    worst: tuple[float, float, float] | None = None
    first_drive = drive_fn(rows[0])
    drive_min = drive_max = previous_drive = first_drive
    saw_rise = saw_fall = False
    for row in rows:
        if row["time"] < 0.10e-9:
            previous_drive = drive_fn(row)
            continue
        drive = drive_fn(row)
        expected = expected_fn(row)
        error = abs(row[output] - expected)
        if error >= max_err:
            max_err = error
            worst = (row["time"], row[output], expected)
        saw_rise = saw_rise or drive - previous_drive > 1e-5
        saw_fall = saw_fall or drive - previous_drive < -1e-5
        drive_min = min(drive_min, drive)
        drive_max = max(drive_max, drive)
        previous_drive = drive
        checked += 1
    if checked < 20:
        return False, f"insufficient_{label}_samples={checked}"
    if drive_max - drive_min < min_span or not (saw_rise and saw_fall):
        return False, (
            f"insufficient_{label}_coverage range={drive_min:.3f}:{drive_max:.3f} "
            f"rise={saw_rise} fall={saw_fall}"
        )
    if max_err > tolerance:
        assert worst is not None
        time_s, observed, expected = worst
        return False, (
            f"{label}_error@{time_s * 1e9:.3f}ns observed={observed:.4f} "
            f"expected={expected:.4f} max_err={max_err:.4f}"
        )
    return True, (
        f"checked={checked} range={drive_min:.3f}:{drive_max:.3f} "
        f"rise={saw_rise} fall={saw_fall} max_err={max_err:.4f}"
    )

def check_v3_differential_amplifier_core(rows: list[dict[str, float]]) -> tuple[bool, str]:
    return _check_affine_transfer_coverage(
        rows,
        required={"time", "sigin_p", "sigin_n", "sigout"},
        output="sigout",
        expected_fn=lambda row: 2.0 * ((row["sigin_p"] - row["sigin_n"]) - 0.05),
        drive_fn=lambda row: row["sigin_p"] - row["sigin_n"],
        label="differential_amplifier_core",
        tolerance=0.02,
        min_span=0.30,
    )

CHECKER_ID = "v4_134_differential_amplifier_core"
CHECKER: Checker = check_v3_differential_amplifier_core
