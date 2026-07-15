"""Task-specific checker for canonical v4 DUT 372."""
from __future__ import annotations

from ..api import Checker
from dataclasses import dataclass

VDD = 0.9
VSS = 0.0
VTH = 0.45

@dataclass
class PropertyResult:
    property_id: str
    mismatch_count: int = 0
    first_time: float | None = None
    expected: str = "contract_satisfied"
    observed: str = "contract_satisfied"
    max_gap: float = 0.0

    def mismatch(
        self,
        time_s: float,
        *,
        expected: object,
        observed: object,
        gap: float = 1.0,
    ) -> None:
        self.mismatch_count += 1
        self.max_gap = max(self.max_gap, abs(float(gap)))
        if self.first_time is None:
            self.first_time = float(time_s)
            self.expected = str(expected)
            self.observed = str(observed)

    def diagnostic(self) -> str:
        sample_time = "none" if self.first_time is None else f"{self.first_time:.12g}"
        return (
            f"{self.property_id} mismatch_count={self.mismatch_count} "
            f"expected={self.expected} observed={self.observed} "
            f"sample_time={sample_time} metric_gap={self.max_gap:.6g}"
        )

def _missing(rows: list[dict[str, float]], required: Iterable[str]) -> list[str]:
    if not rows:
        return sorted(set(required))
    return sorted(set(required) - set(rows[0]))

def _value(row: dict[str, float], name: str) -> float:
    return float(row[name])

def _high(row: dict[str, float], name: str, threshold: float = VTH) -> bool:
    return _value(row, name) > threshold

def _clock_samples(
    rows: list[dict[str, float]], clock: str, *, threshold: float = VTH, settle_s: float = 7e-10
) -> list[dict[str, float]]:
    if len(rows) < 2:
        return []
    rising_times: list[float] = []
    previous = _value(rows[0], clock)
    for row in rows[1:]:
        now = _value(row, clock)
        if previous <= threshold < now:
            rising_times.append(_value(row, "time"))
        previous = now
    samples: list[dict[str, float]] = []
    cursor = 0
    for edge_time in rising_times:
        target = edge_time + settle_s
        while cursor + 1 < len(rows) and _value(rows[cursor], "time") < target:
            cursor += 1
        samples.append(rows[cursor])
    return samples

def _finish(results: list[PropertyResult], *, allowance: dict[str, int] | None = None) -> tuple[bool, str]:
    allowance = allowance or {}
    ok = all(item.mismatch_count <= allowance.get(item.property_id, 0) for item in results)
    return ok, "; ".join(item.diagnostic() for item in results)

def _missing_result(checker_id: str, missing: list[str]) -> tuple[bool, str]:
    return False, (
        f"P_TRACE_CONTRACT mismatch_count={len(missing)} expected=all_required_signals "
        f"observed=missing:{','.join(missing)} sample_time=none metric_gap={len(missing)} "
        f"checker={checker_id}"
    )

def check_v4_372_buck_converter_controller_macro(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vfb", "vref", "clk", "rst", "enable", "pwm", "duty_metric", "soft_ref", "pgood"}
    missing = _missing(rows, required)
    if missing:
        return _missing_result("v4_372_buck_converter_controller_macro", missing)
    clear = PropertyResult("P_RESET_DISABLE_CLEAR")
    soft = PropertyResult("P_SOFT_START_TRACKING")
    duty = PropertyResult("P_DUTY_DIRECTION_BOUNDS")
    pwm = PropertyResult("P_PWM_ENCODING")
    pgood = PropertyResult("P_POWER_GOOD_QUALIFICATION")
    samples = _clock_samples(rows, "clk")
    previous: dict[str, float] | None = None
    carrier_count = 0
    good_count = 0
    for row in samples:
        t = _value(row, "time")
        reset = _high(row, "rst")
        enabled = _high(row, "enable") and not reset
        if not enabled:
            carrier_count = 0
            good_count = 0
            observed = max(abs(_value(row, name)) for name in ("pwm", "duty_metric", "soft_ref", "pgood"))
            if observed > 0.08:
                clear.mismatch(t, expected="all_outputs_low", observed=f"max_abs={observed:.6g}", gap=observed)
            previous = row
            continue

        vref = _value(row, "vref")
        soft_now = _value(row, "soft_ref")
        duty_now = _value(row, "duty_metric")
        if soft_now < -0.02 or soft_now > vref + 0.035:
            soft.mismatch(t, expected=f"0<=soft_ref<={vref:.6g}", observed=f"soft_ref={soft_now:.6g}", gap=max(-soft_now, soft_now-vref))
        if duty_now < 0.035 or duty_now > 0.965:
            duty.mismatch(t, expected="0.05<=duty_metric<=0.95", observed=f"duty_metric={duty_now:.6g}", gap=max(0.05-duty_now,duty_now-0.95))

        if previous is not None and _high(previous, "enable") and not _high(previous, "rst"):
            prev_soft = _value(previous, "soft_ref")
            prev_vref = _value(previous, "vref")
            dsoft = soft_now - prev_soft
            expected_soft_delta = 0.025 if prev_soft < prev_vref - 0.0125 else (-0.025 if prev_soft > prev_vref + 0.0125 else 0.0)
            if abs(dsoft - expected_soft_delta) > 0.018:
                soft.mismatch(t, expected=f"delta={expected_soft_delta:.6g}", observed=f"delta={dsoft:.6g}", gap=dsoft-expected_soft_delta)
            prev_duty = _value(previous, "duty_metric")
            dduty = duty_now - prev_duty
            # vfb may change between clock edges; the continuous comparator is
            # evaluated from the current input and the pre-edge soft state.
            direction = 1 if _value(row, "vfb") < prev_soft else -1
            if direction > 0 and dduty < 0.015 and prev_duty < 0.94:
                duty.mismatch(t, expected="duty_increase", observed=f"delta={dduty:.6g}", gap=0.05-dduty)
            if direction < 0 and dduty > -0.015 and prev_duty > 0.06:
                duty.mismatch(t, expected="duty_decrease", observed=f"delta={dduty:.6g}", gap=dduty+0.05)

        carrier_count = (carrier_count + 1) % 20
        expected_pwm = VDD if (carrier_count + 0.5) < (20.0 * duty_now) else VSS
        observed_pwm = _value(row, "pwm")
        if abs(observed_pwm - expected_pwm) > 0.20:
            pwm.mismatch(t, expected=f"pwm={expected_pwm:.3g}", observed=f"pwm={observed_pwm:.6g}", gap=observed_pwm-expected_pwm)
        if min(abs(observed_pwm-VSS), abs(observed_pwm-VDD)) > 0.15:
            pwm.mismatch(t, expected="rail_valid_pwm", observed=f"pwm={observed_pwm:.6g}", gap=min(abs(observed_pwm),abs(observed_pwm-VDD)))

        in_window = abs(_value(row, "vfb") - vref) <= 0.025 + 1e-6
        good_count = min(3, good_count + 1) if in_window else 0
        expected_good = good_count >= 3
        observed_good = _high(row, "pgood")
        if observed_good != expected_good:
            pgood.mismatch(t, expected=f"pgood={int(expected_good)} streak={good_count}", observed=f"pgood={int(observed_good)}", gap=1)
        previous = row
    if len(samples) < 8:
        clear.mismatch(0.0, expected="at_least_8_clock_samples", observed=f"samples={len(samples)}", gap=8-len(samples))
    return _finish([clear, soft, duty, pwm, pgood], allowance={"P_PWM_ENCODING": 2, "P_POWER_GOOD_QUALIFICATION": 2})

CHECKER_ID = "v4_372_buck_converter_controller_macro"
CHECKER: Checker = check_v4_372_buck_converter_controller_macro
