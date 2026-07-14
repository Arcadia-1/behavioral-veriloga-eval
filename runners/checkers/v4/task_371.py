"""Task-specific checker for canonical v4 DUT 371."""
from __future__ import annotations

from checkers.api import Checker
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

def _clip(value: float, lo: float = VSS, hi: float = VDD) -> float:
    return min(max(value, lo), hi)

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

def _code(row: dict[str, float], names_lsb_first: list[str]) -> int:
    return sum((1 << index) for index, name in enumerate(names_lsb_first) if _high(row, name))

def check_v4_371_bandgap_startup_trim_system(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {
        "time", "vdd_sense", "clk", "rst", "trim_req", "temp_proxy", "vref",
        "trim_3", "trim_2", "trim_1", "trim_0", "ready", "error_metric",
    }
    missing = _missing(rows, required)
    if missing:
        return _missing_result("v4_371_bandgap_startup_trim_system", missing)
    clear = PropertyResult("P_RESET_BROWNOUT_CLEAR")
    startup = PropertyResult("P_POR_STARTUP")
    core = PropertyResult("P_CORE_REFERENCE")
    search = PropertyResult("P_TRIM_SEARCH")
    ready = PropertyResult("P_READY_QUALIFICATION")
    samples = _clock_samples(rows, "clk")
    por_count = 0
    previous_code: int | None = None
    previous_error: float | None = None
    ready_streak = 0
    codes: set[int] = set()
    previous_supply_active = False
    for row in samples:
        t = _value(row, "time")
        reset = _high(row, "rst")
        supply_ok = _value(row, "vdd_sense") >= 0.72
        code = _code(row, ["trim_0", "trim_1", "trim_2", "trim_3"])
        if reset or not supply_ok:
            por_count = 0
            ready_streak = 0
            observed = max(abs(_value(row, name)) for name in ("vref", "trim_3", "trim_2", "trim_1", "trim_0", "ready", "error_metric"))
            # startup_en is a clocked helper output; the trim controller sees
            # its previous value on the first brownout edge.
            if (not previous_supply_active) and observed > 0.08:
                clear.mismatch(t, expected="brownout_reset_outputs_low", observed=f"max_abs={observed:.6g}", gap=observed)
            previous_code = 0
            previous_error = 0.0
            previous_supply_active = False
            continue
        por_count = min(2, por_count + 1)
        started = por_count >= 2
        observed_vref = _value(row, "vref")
        if not started:
            if observed_vref > 0.08:
                startup.mismatch(t, expected=f"vref_low_before_two_edges,count={por_count}", observed=f"vref={observed_vref:.6g}", gap=observed_vref)
            previous_code = code
            previous_error = _value(row, "error_metric")
            continue
        base = _clip(0.588 + 0.040 * (_value(row, "temp_proxy") - 0.6))
        expected_vref = _clip(base + code * 0.002)
        if abs(observed_vref - expected_vref) > 0.015:
            core.mismatch(t, expected=f"vref={expected_vref:.6g}", observed=f"vref={observed_vref:.6g}", gap=observed_vref-expected_vref)
        observed_error = _value(row, "error_metric")
        expected_error = 0.6 - expected_vref
        if abs(observed_error - expected_error) > 0.015:
            core.mismatch(t, expected=f"error_metric={expected_error:.6g}", observed=f"error_metric={observed_error:.6g}", gap=observed_error-expected_error)
        if _high(row, "trim_req"):
            codes.add(code)
            if previous_code is not None and previous_error is not None:
                delta = code - previous_code
                if previous_error > 0.005 and delta < 0:
                    search.mismatch(t, expected="trim_non_decreasing_for_positive_error", observed=f"delta={delta}", gap=delta)
                if previous_error < -0.005 and delta > 0:
                    search.mismatch(t, expected="trim_non_increasing_for_negative_error", observed=f"delta={delta}", gap=delta)
                if abs(delta) > 1:
                    search.mismatch(t, expected="one_trim_step_per_clock", observed=f"delta={delta}", gap=abs(delta)-1)
            ready_streak = ready_streak + 1 if abs(observed_error) <= 0.0055 else 0
            observed_ready = _high(row, "ready")
            if observed_ready and ready_streak < 3:
                ready.mismatch(t, expected=f"ready=0,streak={ready_streak}", observed="ready=1", gap=1)
            if observed_ready and abs(observed_error) > 0.006:
                ready.mismatch(t, expected="ready_only_within_tolerance", observed=f"error={observed_error:.6g}", gap=abs(observed_error)-0.005)
        previous_code = code
        previous_error = observed_error
        previous_supply_active = True
    if len(codes) < 2:
        search.mismatch(0.0, expected="at_least_two_trim_codes", observed=f"codes={sorted(codes)}", gap=2-len(codes))
    return _finish([clear, startup, core, search, ready], allowance={"P_CORE_REFERENCE": 2, "P_READY_QUALIFICATION": 1})

CHECKER_ID = "v4_371_bandgap_startup_trim_system"
CHECKER: Checker = check_v4_371_bandgap_startup_trim_system
