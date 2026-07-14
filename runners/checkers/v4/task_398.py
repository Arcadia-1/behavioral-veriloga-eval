"""Event-relative checker for the clocked two-stage op-amp slew model."""

from __future__ import annotations

from ..api import Checker, Row


VDD = 0.9
VSS = 0.0
VCM = 0.45
VTH = 0.45
STAGE1_GAIN = 20.0
STAGE2_GAIN = 5.0
SLEW_STEP = 0.08
SETTLE_TOL = 0.010


def _high(row: Row, signal: str) -> bool:
    return float(row[signal]) > VTH


def _active(row: Row) -> bool:
    return _high(row, "enable") and not _high(row, "rst")


def _clip(value: float) -> float:
    return max(VSS, min(VDD, value))


def _clear(row: Row) -> bool:
    return (
        abs(float(row["vout"]) - VCM) <= 0.08
        and abs(float(row["stage1_metric"]) - VCM) <= 0.08
        and abs(float(row["slew_metric"])) <= 0.05
        and not _high(row, "clamp_flag")
        and not _high(row, "settled")
    )


def _window_sample(rows: list[Row], edge_index: int) -> Row | None:
    """Return the last stable sample before the next clock/control event."""

    edge = rows[edge_index]
    edge_reset = _high(edge, "rst")
    edge_enable = _high(edge, "enable")
    sample_index = edge_index
    for index in range(edge_index + 1, len(rows)):
        row = rows[index]
        control_changed = (
            _high(row, "rst") != edge_reset
            or _high(row, "enable") != edge_enable
        )
        clock_fell = float(row["clk"]) <= VTH
        if control_changed or clock_fell:
            break
        sample_index = index
    return rows[sample_index] if sample_index > edge_index else None


def check_two_stage_opamp_slew_macromodel(rows: list[Row]) -> tuple[bool, str]:
    required = {
        "time",
        "vinp",
        "vinn",
        "clk",
        "rst",
        "enable",
        "load_step",
        "vout",
        "stage1_metric",
        "slew_metric",
        "clamp_flag",
        "settled",
    }
    missing = sorted(required - (set(rows[0]) if rows else set()))
    if missing:
        return False, "missing_columns=" + ",".join(missing)

    previous_clk = float(rows[0]["clk"])
    expected_vout = VCM
    settle_count = 0
    checked = 0
    sample_gaps = 0
    stage1_errors = 0
    vout_errors = 0
    slew_errors = 0
    clamp_errors = 0
    settled_errors = 0
    reset_clear = False
    disabled_clear = False
    ever_active = False
    slew_seen = False
    clamp_seen = False
    settled_seen = False

    inactive_tail: Row | None = None
    inactive_had_reset = False
    inactive_after_active = False

    def close_inactive_run() -> None:
        nonlocal reset_clear, disabled_clear
        if inactive_tail is None:
            return
        clear = _clear(inactive_tail)
        reset_clear |= inactive_had_reset and clear
        disabled_clear |= inactive_after_active and clear

    for index, row in enumerate(rows):
        active = _active(row)
        if not active:
            if inactive_tail is None:
                inactive_had_reset = False
                inactive_after_active = ever_active and not _high(row, "enable")
            inactive_tail = row
            inactive_had_reset |= _high(row, "rst")
            inactive_after_active |= ever_active and not _high(row, "enable")
            expected_vout = VCM
            settle_count = 0
            previous_clk = float(row["clk"])
            continue

        if inactive_tail is not None:
            close_inactive_run()
            inactive_tail = None
            inactive_had_reset = False
            inactive_after_active = False

        ever_active = True
        clk = float(row["clk"])
        rising = previous_clk <= VTH < clk
        previous_clk = clk
        if not rising:
            continue

        sample = _window_sample(rows, index)
        if sample is None:
            sample_gaps += 1
            continue

        stage1 = _clip(VCM + STAGE1_GAIN * (float(row["vinp"]) - float(row["vinn"])))
        raw_target = (
            VCM
            + STAGE2_GAIN * (stage1 - VCM)
            + 0.5 * (float(row["load_step"]) - VCM)
        )
        target = _clip(raw_target)
        clamped = abs(target - raw_target) > 1e-12
        move = max(-SLEW_STEP, min(SLEW_STEP, target - expected_vout))
        expected_vout = _clip(expected_vout + move)
        expected_slew = abs(move)
        settle_count = settle_count + 1 if abs(target - expected_vout) < SETTLE_TOL else 0
        expected_settled = settle_count >= 2

        checked += 1
        slew_seen |= expected_slew > 0.02
        clamp_seen |= clamped
        stage1_errors += abs(float(sample["stage1_metric"]) - stage1) > 0.10
        vout_errors += abs(float(sample["vout"]) - expected_vout) > 0.10
        slew_errors += abs(float(sample["slew_metric"]) - expected_slew) > 0.08
        clamp_errors += _high(sample, "clamp_flag") != clamped
        observed_settled = _high(sample, "settled")
        settled_seen |= expected_settled and observed_settled
        settled_errors += observed_settled != expected_settled

    if inactive_tail is not None:
        close_inactive_run()

    error_allowance = max(1, checked // 8)
    coverage_ok = (
        checked >= 6
        and reset_clear
        and disabled_clear
        and slew_seen
        and clamp_seen
        and settled_seen
        and sample_gaps == 0
    )
    ok = (
        coverage_ok
        and stage1_errors <= error_allowance
        and vout_errors <= error_allowance
        and slew_errors <= error_allowance
        and clamp_errors <= error_allowance
        and settled_errors <= error_allowance
    )
    return ok, (
        f"v4_398 checked={checked} reset_clear={reset_clear} "
        f"disabled_clear={disabled_clear} slew_seen={slew_seen} "
        f"clamp_seen={clamp_seen} settled_seen={settled_seen} "
        f"sample_gaps={sample_gaps} "
        f"stage1_errors={stage1_errors} vout_errors={vout_errors} "
        f"slew_errors={slew_errors} clamp_errors={clamp_errors} "
        f"settled_errors={settled_errors} allowance={error_allowance}"
    )


CHECKER_ID = "v4_398_two_stage_opamp_slew_macromodel"
CHECKER: Checker = check_two_stage_opamp_slew_macromodel
