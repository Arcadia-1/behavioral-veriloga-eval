"""Task-specific checker for canonical v4 DUT 011."""
from __future__ import annotations

from checkers.api import Checker
def rising_edges(values: list[float], times: list[float], threshold: float = 0.45) -> list[float]:
    edges: list[float] = []
    for i in range(1, len(values)):
        if values[i - 1] < threshold <= values[i]:
            edges.append(times[i])
    return edges

def weighted_logic_high_fraction(rows: list[dict[str, float]], signal: str, threshold: float) -> float:
    if len(rows) < 2:
        return 0.0
    total_dt = rows[-1]["time"] - rows[0]["time"]
    if total_dt <= 0.0:
        return 0.0

    high_dt = 0.0
    for idx in range(1, len(rows)):
        dt = rows[idx]["time"] - rows[idx - 1]["time"]
        if dt <= 0.0:
            continue
        v_mid = 0.5 * (rows[idx - 1][signal] + rows[idx][signal])
        if v_mid > threshold:
            high_dt += dt
    return high_dt / total_dt

def time_window(rows: list[dict[str, float]], t_start: float, t_end: float) -> list[dict[str, float]]:
    return [r for r in rows if t_start <= r["time"] <= t_end]

def check_pfd_reset_race(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows or not {"ref", "div", "up", "dn"}.issubset(rows[0]):
        return False, "missing ref/div/up/dn"

    vth = max(r["ref"] for r in rows) * 0.5
    first = time_window(rows, 20e-9, 120e-9)
    second = time_window(rows, 160e-9, 260e-9)
    if len(first) < 4 or len(second) < 4:
        return False, "insufficient_window_samples"

    up_first = weighted_logic_high_fraction(first, "up", vth)
    dn_first = weighted_logic_high_fraction(first, "dn", vth)
    up_second = weighted_logic_high_fraction(second, "up", vth)
    dn_second = weighted_logic_high_fraction(second, "dn", vth)

    first_times = [r["time"] for r in first]
    second_times = [r["time"] for r in second]
    up_pulses_first = len(rising_edges([r["up"] for r in first], first_times, threshold=vth))
    dn_pulses_second = len(rising_edges([r["dn"] for r in second], second_times, threshold=vth))

    overlap_dt = 0.0
    total_dt = 0.0
    for idx in range(1, len(rows)):
        dt = rows[idx]["time"] - rows[idx - 1]["time"]
        if dt <= 0.0:
            continue
        total_dt += dt
        up_mid = 0.5 * (rows[idx - 1]["up"] + rows[idx]["up"])
        dn_mid = 0.5 * (rows[idx - 1]["dn"] + rows[idx]["dn"])
        if up_mid > vth and dn_mid > vth:
            overlap_dt += dt
    overlap_frac = overlap_dt / max(total_dt, 1e-18)

    ok = (
        0.001 <= up_first <= 0.08
        and dn_first <= 0.01
        and 0.001 <= dn_second <= 0.08
        and up_second <= 0.01
        and up_pulses_first >= 4
        and dn_pulses_second >= 4
        and overlap_frac <= 0.01
    )
    return ok, (
        f"up_first={up_first:.4f} dn_first={dn_first:.4f} "
        f"up_second={up_second:.4f} dn_second={dn_second:.4f} "
        f"up_pulses_first={up_pulses_first} dn_pulses_second={dn_pulses_second} "
        f"overlap_frac={overlap_frac:.4f}"
    )

def check_v4_pfd_updn_logic(rows: list[dict[str, float]]) -> tuple[bool, str]:
    """Add the v4 public local-rail contract to the legacy PFD pulse check."""
    pulse_ok, pulse_note = check_pfd_reset_race(rows)
    required = {"vdd", "vss", "up", "dn"}
    if not rows or not required.issubset(rows[0]):
        return False, f"{pulse_note} missing local rail observables"

    # Rails are DC in this task.  Exclude the initial pre-source row: before
    # DC sources settle it is legitimate for a contribution output to be 0 V
    # even when the exercised local VSS is nonzero.
    stable_rows = [row for row in rows if row["time"] >= 10e-9]
    if not stable_rows:
        return False, f"{pulse_note} no stable local-rail samples"
    vdd = max(row["vdd"] for row in stable_rows)
    vss = max(row["vss"] for row in stable_rows)
    rail_span = vdd - vss
    up_hi, up_lo = max(row["up"] for row in stable_rows), min(row["up"] for row in stable_rows)
    dn_hi, dn_lo = max(row["dn"] for row in stable_rows), min(row["dn"] for row in stable_rows)
    tolerance = 0.04
    rail_ok = (
        rail_span >= 0.4
        and abs(up_hi - vdd) <= tolerance
        and abs(up_lo - vss) <= tolerance
        and abs(dn_hi - vdd) <= tolerance
        and abs(dn_lo - vss) <= tolerance
    )
    rail_note = (
        f"rail_reference vdd={vdd:.4f} vss={vss:.4f} "
        f"up_hi_lo={up_hi:.4f}/{up_lo:.4f} dn_hi_lo={dn_hi:.4f}/{dn_lo:.4f} "
        f"rail_ok={rail_ok}"
    )
    return pulse_ok and rail_ok, f"{pulse_note} {rail_note}"

CHECKER_ID = "v4_011_pfd_up_dn_logic"
CHECKER: Checker = check_v4_pfd_updn_logic
