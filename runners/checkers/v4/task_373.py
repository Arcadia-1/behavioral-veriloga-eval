"""Task-specific checker for canonical v4 DUT 373."""
from __future__ import annotations

from ..api import Checker
from dataclasses import dataclass

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

def _logic(value: float, threshold: float = VTH) -> int:
    return int(value > threshold)

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

def check_v4_373_charge_pump_voltage_multiplier_controller(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst", "enable", "target", "vout", "phase_a", "phase_b", "pump_en", "regulation_error", "ready"}
    missing = _missing(rows, required)
    if missing:
        return _missing_result("v4_373_charge_pump_voltage_multiplier_controller", missing)
    clear = PropertyResult("P_RESET_DISABLE_CLEAR")
    phase = PropertyResult("P_NONOVERLAP_PHASES")
    pump = PropertyResult("P_PUMP_REGULATION")
    error = PropertyResult("P_ERROR_REPORTING")
    ready = PropertyResult("P_READY_QUALIFICATION")
    samples = _clock_samples(rows, "clk")
    previous: dict[str, float] | None = None
    last_phase: int | None = None
    ready_streak = 0
    for row in samples:
        t = _value(row, "time")
        reset = _high(row, "rst")
        enabled = _high(row, "enable") and not reset
        va, vb = _logic(_value(row,"phase_a")), _logic(_value(row,"phase_b"))
        if reset:
            observed = max(abs(_value(row,n)) for n in ("vout","pump_en","ready"))
            if observed > 0.09:
                clear.mismatch(t, expected="reset_outputs_low", observed=f"max_abs={observed:.6g}", gap=observed)
            last_phase = None
            ready_streak = 0
            previous = row
            continue
        if not enabled:
            if _high(row,"pump_en") or _high(row,"ready"):
                clear.mismatch(t, expected="disabled_pump_ready_low", observed=f"pump={_logic(_value(row,'pump_en'))},ready={_logic(_value(row,'ready'))}", gap=1)
            last_phase = None
            ready_streak = 0
            previous = row
            continue
        if va + vb != 1:
            phase.mismatch(t, expected="one_hot_phase", observed=f"phase_a={va},phase_b={vb}", gap=abs(1-(va+vb)))
        current_phase = 0 if va else 1
        if last_phase is not None and current_phase == last_phase:
            phase.mismatch(t, expected=f"phase={1-last_phase}", observed=f"phase={current_phase}", gap=1)
        last_phase = current_phase
        vout = _value(row,"vout")
        target = _value(row,"target")
        observed_error = _value(row,"regulation_error")
        expected_error = target-vout
        if abs(observed_error-expected_error) > 0.012:
            error.mismatch(t, expected=f"target-vout={expected_error:.6g}", observed=f"regulation_error={observed_error:.6g}", gap=observed_error-expected_error)
        if vout < -0.02 or vout > 1.82:
            pump.mismatch(t, expected="0<=vout<=1.8", observed=f"vout={vout:.6g}", gap=max(-vout,vout-1.8))
        if previous is not None and _high(previous,"enable") and not _high(previous,"rst"):
            dv = vout-_value(previous,"vout")
            previous_vout = _value(previous,"vout")
            if previous_vout < target - 0.025:
                pre_edge_pump = True
            elif previous_vout > target + 0.025:
                pre_edge_pump = False
            else:
                pre_edge_pump = _high(previous,"pump_en")
            was_pumping = (
                pre_edge_pump
                and (_high(previous,"phase_a") or _high(previous,"phase_b"))
            )
            if was_pumping and not (0.030 <= dv <= 0.052):
                pump.mismatch(t, expected="pump_delta_about_0.04", observed=f"delta={dv:.6g}", gap=dv-0.04)
            if not was_pumping and not (-0.018 <= dv <= 0.012):
                pump.mismatch(t, expected="leak_delta_about_-0.005", observed=f"delta={dv:.6g}", gap=dv+0.005)
        if vout < target-0.055 and not _high(row,"pump_en"):
            error.mismatch(t, expected="pump_en=1_below_target", observed="pump_en=0", gap=(target-vout))
        observed_ready = _high(row,"ready")
        if observed_ready and (ready_streak < 3 or abs(observed_error) > 0.07):
            ready.mismatch(t, expected="qualified_ready_only", observed=f"ready=1,streak={ready_streak},error={observed_error:.6g}", gap=abs(observed_error))
        in_window = abs(observed_error) <= 0.065
        ready_streak = min(3,ready_streak+1) if in_window else 0
        previous = row
    if len(samples) < 8:
        clear.mismatch(0.0, expected="at_least_8_clock_samples", observed=f"samples={len(samples)}", gap=8-len(samples))
    return _finish([clear, phase, pump, error, ready], allowance={"P_PUMP_REGULATION": 3, "P_ERROR_REPORTING": 2})

CHECKER_ID = "v4_373_charge_pump_voltage_multiplier_controller"
CHECKER: Checker = check_v4_373_charge_pump_voltage_multiplier_controller
