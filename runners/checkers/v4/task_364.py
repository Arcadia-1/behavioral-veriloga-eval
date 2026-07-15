"""Checker for the enabled I/Q upconversion mixer chain."""

from __future__ import annotations

from ..api import Checker, Row


VCM = 0.45
VDD = 0.9
VSS = 0.0
VTH = 0.45
EDGE_GUARD_S = 0.4e-9


def _high(row: Row, name: str) -> bool:
    return float(row[name]) > VTH


def _crossed(previous: Row, current: Row, signal: str) -> bool:
    before = float(previous[signal])
    after = float(current[signal])
    return (before <= VTH < after) or (before >= VTH > after)


def _crossing_times(rows: list[Row], signal: str) -> list[float]:
    return [
        float(current["time"])
        for previous, current in zip(rows, rows[1:])
        if _crossed(previous, current, signal)
    ]


def _near_any_edge(time_s: float, edges: list[float]) -> bool:
    return any(abs(time_s - edge) < EDGE_GUARD_S for edge in edges)


def check_iq_upconversion_mixer_chain(rows: list[Row]) -> tuple[bool, str]:
    required = {
        "time",
        "i_in",
        "q_in",
        "lo_i",
        "lo_q",
        "rst",
        "enable",
        "rf_out",
        "i_mix_dbg",
        "q_mix_dbg",
        "quad_ok",
    }
    missing = sorted(required - (set(rows[0]) if rows else set()))
    if missing:
        return False, "missing_columns=" + ",".join(missing)

    edge_times: list[float] = []
    for signal in ("lo_i", "lo_q", "rst", "enable"):
        edge_times.extend(_crossing_times(rows, signal))

    stride = max(1, len(rows) // 1000)
    clear_checks = 0
    clear_errors = 0
    mix_checks = 0
    mix_errors = 0
    rf_errors = 0
    for row in rows[::stride]:
        time_s = float(row["time"])
        if _near_any_edge(time_s, edge_times):
            continue
        active = not _high(row, "rst") and _high(row, "enable")
        if not active:
            clear_checks += 1
            gap = max(
                abs(float(row["rf_out"]) - VCM),
                abs(float(row["i_mix_dbg"]) - VCM),
                abs(float(row["q_mix_dbg"]) - VCM),
                abs(float(row["quad_ok"])),
            )
            clear_errors += gap > 0.055
            continue

        lo_i_sign = 1.0 if _high(row, "lo_i") else -1.0
        lo_q_sign = 1.0 if _high(row, "lo_q") else -1.0
        i_expected = VCM + (float(row["i_in"]) - VCM) * lo_i_sign
        q_expected = VCM - (float(row["q_in"]) - VCM) * lo_q_sign
        rf_expected = min(VDD, max(VSS, i_expected + q_expected - VCM))
        mix_checks += 1
        mix_errors += max(
            abs(float(row["i_mix_dbg"]) - i_expected),
            abs(float(row["q_mix_dbg"]) - q_expected),
        ) > 0.035
        rf_errors += abs(float(row["rf_out"]) - rf_expected) > 0.035

    seen_i = False
    seen_q = False
    activity_checks = 0
    activity_errors = 0
    saw_quad_low = False
    saw_quad_high = False
    previous = rows[0]
    for row in rows[1:]:
        active = not _high(row, "rst") and _high(row, "enable")
        if not active:
            seen_i = False
            seen_q = False
            previous = row
            continue
        if _crossed(previous, row, "lo_i"):
            seen_i = True
        if _crossed(previous, row, "lo_q"):
            seen_q = True
        time_s = float(row["time"])
        if not _near_any_edge(time_s, edge_times):
            expected = seen_i and seen_q
            observed = _high(row, "quad_ok")
            saw_quad_low |= not expected
            saw_quad_high |= expected
            activity_checks += 1
            activity_errors += observed != expected
        previous = row

    mix_allowance = max(2, mix_checks // 50)
    activity_allowance = max(3, activity_checks // 100)
    coverage_ok = (
        clear_checks > 0
        and mix_checks >= 10
        and activity_checks >= 10
        and saw_quad_low
        and saw_quad_high
    )
    ok = (
        coverage_ok
        and clear_errors == 0
        and mix_errors <= mix_allowance
        and rf_errors <= mix_allowance
        and activity_errors <= activity_allowance
    )
    return ok, (
        f"clear={clear_checks}/{clear_errors} mix={mix_checks}/{mix_errors} "
        f"rf_errors={rf_errors} activity={activity_checks}/{activity_errors} "
        f"quad_low={saw_quad_low} quad_high={saw_quad_high}"
    )


CHECKER_ID = "v4_364_iq_upconversion_mixer_chain"
CHECKER: Checker = check_iq_upconversion_mixer_chain
