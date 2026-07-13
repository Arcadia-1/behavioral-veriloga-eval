"""Task-specific checker for canonical v4 DUT 311."""
from __future__ import annotations

from checkers.api import Checker
from checkers.common.v4_topup import (
    _v4_topup_clip01,
    _v4_topup_logic_high,
    _v4_topup_near,
)

def check_v4_1009_muxed_track_hold_array_readout(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1009 empty_trace"
    held = [0.45, 0.45, 0.45]
    held_valid = [False, False, False]
    expected_out = 0.45
    checked = vout_errors = metric_errors = valid_errors = disabled_update_errors = 0
    reset_clear = disabled_hold_seen = invalid_seen = valid_seen = False
    codes_seen: set[int] = set()
    previous = rows[0]
    last_sample_en = _v4_topup_logic_high(previous, "sample_en")

    def code_at(row: dict[str, float]) -> int:
        return int(_v4_topup_logic_high(row, "sel_0")) + 2 * int(_v4_topup_logic_high(row, "sel_1"))

    for index, row in enumerate(rows[1:], start=1):
        clk_rise = (not _v4_topup_logic_high(previous, "clk")) and _v4_topup_logic_high(row, "clk")
        if clk_rise:
            if _v4_topup_logic_high(row, "rst"):
                held = [0.45, 0.45, 0.45]
                held_valid = [False, False, False]
                expected_out = 0.45
            elif _v4_topup_logic_high(row, "sample_en"):
                held = [float(row["vin0"]), float(row["vin1"]), float(row["vin2"])]
                held_valid = [True, True, True]
            elif any(held_valid):
                disabled_hold_seen = True
        sample_en = _v4_topup_logic_high(row, "sample_en")
        if last_sample_en and not sample_en and any(held_valid):
            disabled_hold_seen = True
        last_sample_en = sample_en

        stable_ref = rows[max(0, index - 8)]
        if any(
            abs(float(row[name]) - float(stable_ref[name])) > 0.25
            for name in ("rst", "sample_en", "sel_0", "sel_1")
        ):
            previous = row
            continue
        code = code_at(row)
        if (
            row["time"] > 7e-9
            and not _v4_topup_logic_high(row, "rst")
            and not sample_en
            and code != 3
            and any(held_valid)
            and abs(float(row["vout"]) - held[code]) > 0.14
        ):
            disabled_update_errors += 1

        previous = row

        if index % 8 != 0 or row["time"] < 7e-9:
            continue
        if _v4_topup_logic_high(row, "rst"):
            if _v4_topup_near(row["vout"], 0.45, 0.08) and row["valid"] < 0.2 and row["channel_metric"] < 0.2:
                reset_clear = True
            continue
        if code == 3:
            invalid_seen = invalid_seen or row["valid"] < 0.25
            if row["valid"] > 0.25:
                valid_errors += 1
            checked += 1
            continue
        codes_seen.add(code)
        expected_out = held[code]
        expected_valid = held_valid[code]
        expected_metric = _v4_topup_clip01(0.45 + 0.15 * code)
        checked += 1
        valid_seen = valid_seen or row["valid"] > 0.45
        if abs(float(row["vout"]) - expected_out) > 0.12:
            vout_errors += 1
        if abs(float(row["channel_metric"]) - expected_metric) > 0.08:
            metric_errors += 1
        if (float(row["valid"]) > 0.45) != expected_valid:
            valid_errors += 1
    ok = (
        checked >= 20
        and reset_clear
        and disabled_hold_seen
        and invalid_seen
        and valid_seen
        and codes_seen >= {0, 1, 2}
        and vout_errors <= max(4, checked // 20)
        and metric_errors <= 1
        and valid_errors <= max(5, checked // 20)
        and disabled_update_errors <= 6
    )
    return ok, (
        f"v4_1009 checked={checked} reset_clear={reset_clear} disabled_hold={disabled_hold_seen} "
        f"invalid_seen={invalid_seen} valid_seen={valid_seen} codes={sorted(codes_seen)} "
        f"vout_errors={vout_errors} metric_errors={metric_errors} valid_errors={valid_errors} "
        f"disabled_update_errors={disabled_update_errors}"
    )

CHECKER_ID = "v4_1009_muxed_track_hold_array_readout"
CHECKER: Checker = check_v4_1009_muxed_track_hold_array_readout
