"""Task-specific checker for canonical v4 DUT 370."""
from __future__ import annotations

from bisect import bisect_right

from ..api import Checker


def _v4_topup_clip01(value: float, low: float = 0.0, high: float = 0.9) -> float:
    return max(low, min(high, value))


def _v4_topup_logic_high(row: dict[str, float], name: str, threshold: float = 0.45) -> bool:
    return float(row.get(name, 0.0)) > threshold


def _v4_code_from_bits(row: dict[str, float], bits: list[str]) -> int:
    return sum((1 << idx) for idx, bit in enumerate(bits) if _v4_topup_logic_high(row, bit))


def _v4_rising(prev_v: float, now_v: float, vth: float = 0.45) -> bool:
    return now_v > vth and prev_v <= vth


def _v4_interpolate(rows: list[dict[str, float]], times: list[float], signal: str, target_time: float) -> float | None:
    if not rows or target_time < times[0] or target_time > times[-1]:
        return None
    right = bisect_right(times, target_time)
    if right == 0:
        return float(rows[0][signal])
    left = right - 1
    if right == len(rows) or times[left] == target_time:
        return float(rows[left][signal])
    t0 = times[left]
    t1 = times[right]
    if t1 == t0:
        return float(rows[right][signal])
    alpha = (target_time - t0) / (t1 - t0)
    return float(rows[left][signal]) + alpha * (float(rows[right][signal]) - float(rows[left][signal]))


def _v4_sample_at(rows: list[dict[str, float]], times: list[float], target_time: float) -> dict[str, float] | None:
    if target_time < times[0] or target_time > times[-1]:
        return None
    sample = {"time": target_time}
    for key in rows[0]:
        if key == "time":
            continue
        value = _v4_interpolate(rows, times, key, target_time)
        if value is None:
            return None
        sample[key] = value
    return sample


def check_v4_929_opamp_feedback_settling_monitor(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_929 empty_trace"
    times = [float(row["time"]) for row in rows]
    prev_clk = float(rows[0].get("clk", 0.0))
    vout = 0.45
    settle_count = 0
    checked = vout_errors = err_errors = settled_errors = clear_errors = 0
    reset_clear = disabled_clear = settled_seen = move_seen = False
    inactive_time: float | None = None
    for row in rows:
        t = float(row["time"])
        rst = _v4_topup_logic_high(row, "rst")
        enabled = _v4_topup_logic_high(row, "enable") and not rst
        if not enabled:
            if inactive_time is None:
                inactive_time = t
            inactive_ready = t >= inactive_time + 0.7e-9
            vout = 0.45; settle_count = 0
            clear = abs(row["vout"] - 0.45) < 0.08 and abs(row["error_metric"] - 0.45) < 0.08 and row["settled"] < 0.10
            reset_clear = reset_clear or (rst and inactive_ready and clear)
            disabled = not rst and not _v4_topup_logic_high(row, "enable")
            disabled_clear = disabled_clear or (disabled and inactive_ready and clear)
            if inactive_ready and not clear:
                clear_errors += 1
            prev_clk = float(row["clk"])
            continue
        inactive_time = None
        now_clk = float(row["clk"])
        if _v4_rising(prev_clk, now_clk):
            code = _v4_code_from_bits(row, ["gain_0", "gain_1", "gain_2"])
            target = _v4_topup_clip01(0.45 + (1.0 + 0.5 * code) * (float(row["vin"]) - 0.45))
            old = vout
            vout = _v4_topup_clip01(vout + 0.3 * (target - vout))
            err = target - vout
            settle_count = settle_count + 1 if abs(err) < 0.040 else 0
            # Anchor the settle window to the first recorded active edge.  The
            # clock is a discrete event signal; linearly interpolating its
            # threshold crossing makes the probe time depend on trace density.
            sample = _v4_sample_at(rows, times, t + 0.7e-9)
            if sample is not None:
                checked += 1
                move_seen = move_seen or abs(vout - old) > 0.01
                expected_settled = settle_count >= 3
                settled_seen = settled_seen or expected_settled
                if abs(float(sample["vout"]) - vout) > 0.10:
                    vout_errors += 1
                if abs(float(sample["error_metric"]) - (err + 0.45)) > 0.12:
                    err_errors += 1
                if _v4_topup_logic_high(sample, "settled") != expected_settled:
                    settled_errors += 1
        prev_clk = now_clk
    # `settled` changes on the same logical update as a thresholded clock
    # event.  EVAS and Spectre can expose that update on adjacent trace rows;
    # budget by logical edge count, not by raw trace density.
    settled_error_budget = max(1, checked // 15)
    ok = checked >= 6 and reset_clear and disabled_clear and move_seen and settled_seen and vout_errors <= 1 and err_errors <= 1 and settled_errors <= settled_error_budget and clear_errors <= 12
    diagnostics = [
        f"P_ON_RESET_OR_WHEN_ENABLE_IS mismatch_count={clear_errors + int(not reset_clear) + int(not disabled_clear)} expected=vout=vcm,metric=settled=0 observed=reset_clear={reset_clear},disabled_clear={disabled_clear},clear_errors={clear_errors}",
        f"P_DECODE_GAIN_2_GAIN_0_INTO mismatch_count={vout_errors + int(checked < 6)} expected=target_from_binary_gain_code observed=checked={checked},vout_errors={vout_errors}",
        f"P_UPDATE_VOUT_ONCE_PER_RISING_CLK mismatch_count={vout_errors + int(not move_seen)} expected=alpha_step_toward_target observed=vout_errors={vout_errors},move_seen={move_seen}",
        f"P_CLAMP_VOUT_TO_THE_RANGE_VSS mismatch_count={vout_errors} expected=vss<=vout<=vdd observed=vout_errors={vout_errors}",
        f"P_ERROR_METRIC_MUST_EXPOSE_THE_SIGNED mismatch_count={err_errors} expected=error_metric=vcm+target-vout observed=err_errors={err_errors}",
        f"P_ASSERT_SETTLED_AFTER_THREE_CONSECUTIVE_UPDATES mismatch_count={max(0, settled_errors - settled_error_budget) + int(not settled_seen)} expected=settled_after_three observed=settled_errors={settled_errors},budget={settled_error_budget},settled_seen={settled_seen}",
    ]
    return ok, "; ".join(diagnostics)

CHECKER_ID = "v4_370_opamp_feedback_settling_monitor"
CHECKER: Checker = check_v4_929_opamp_feedback_settling_monitor
