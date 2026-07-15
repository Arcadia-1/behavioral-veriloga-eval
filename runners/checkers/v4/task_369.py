"""Task-specific checker for canonical v4 DUT 369."""
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

def check_v4_369_offset_cancellation_servo(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {
        "time", "vinp", "vinn", "clk", "rst", "cal_en", "corrected_out",
        "trim_4", "trim_3", "trim_2", "trim_1", "trim_0", "error_metric", "done",
    }
    missing = _missing(rows, required)
    if missing:
        return _missing_result("v4_369_offset_cancellation_servo", missing)
    clear = PropertyResult("P_RESET_DISABLE_CLEAR")
    search = PropertyResult("P_TRIM_SEARCH_DIRECTION")
    corrected = PropertyResult("P_CORRECTED_RESIDUAL")
    metric = PropertyResult("P_ERROR_METRIC")
    done = PropertyResult("P_DONE_QUALIFICATION")
    samples = _clock_samples(rows, "clk")
    previous_code: int | None = None
    previous_sampled_diff: float | None = None
    in_tol_streak = 0
    active_codes: set[int] = set()
    for row in samples:
        t = _value(row, "time")
        raw_code = _code(row, ["trim_0", "trim_1", "trim_2", "trim_3", "trim_4"])
        signed_code = raw_code if raw_code < 16 else -(raw_code - 15)
        if _high(row, "rst"):
            observed = max(
                abs(_value(row, name))
                for name in ("corrected_out", "trim_4", "trim_3", "trim_2", "trim_1", "trim_0", "error_metric", "done")
            )
            if observed > 0.08:
                clear.mismatch(t, expected="reset_clears_outputs", observed=f"max_abs={observed:.6g}", gap=observed)
            previous_code = 0
            previous_sampled_diff = 0.0
            in_tol_streak = 0
            continue
        differential = _value(row, "vinp") - _value(row, "vinn")
        expected_corrected = differential - signed_code * 0.002
        observed_corrected = _value(row, "corrected_out")
        if abs(observed_corrected - expected_corrected) > 0.012:
            corrected.mismatch(t, expected=f"corrected_out={expected_corrected:.6g}", observed=f"corrected_out={observed_corrected:.6g}", gap=observed_corrected-expected_corrected)
        observed_metric = _value(row, "error_metric")
        if _high(row, "cal_en"):
            active_codes.add(signed_code)
            # Sampler and integrator are clocked together.  The integrator
            # consumes the sample retained from the preceding enabled edge.
            expected_metric = (
                previous_sampled_diff - signed_code * 0.002
                if previous_sampled_diff is not None
                else observed_metric
            )
            if abs(observed_metric - expected_metric) > 0.016:
                metric.mismatch(t, expected=f"error_metric={expected_metric:.6g}", observed=f"error_metric={observed_metric:.6g}", gap=observed_metric-expected_metric)
            if previous_code is not None and previous_sampled_diff is not None:
                delta = signed_code - previous_code
                prior_residual = previous_sampled_diff - previous_code * 0.002
                if prior_residual > 0.005 and delta < 0:
                    search.mismatch(t, expected="signed_trim_non_decreasing_for_positive_error", observed=f"delta={delta}", gap=delta)
                if prior_residual < -0.005 and delta > 0:
                    search.mismatch(t, expected="signed_trim_non_increasing_for_negative_error", observed=f"delta={delta}", gap=delta)
                if abs(delta) > 1:
                    search.mismatch(t, expected="one_code_step_per_clock", observed=f"delta={delta}", gap=abs(delta)-1)
            in_tol_streak = in_tol_streak + 1 if abs(observed_metric) <= 0.0055 else 0
            expected_done = in_tol_streak >= 4
            observed_done = _high(row, "done")
            if observed_done and not expected_done:
                done.mismatch(t, expected=f"done=0,streak={in_tol_streak}", observed="done=1", gap=1)
            previous_sampled_diff = differential
        previous_code = signed_code
    if len(active_codes) < 2:
        search.mismatch(0.0, expected="at_least_two_active_trim_codes", observed=f"codes={sorted(active_codes)}", gap=2-len(active_codes))
    return _finish([clear, search, corrected, metric, done], allowance={"P_ERROR_METRIC": 2, "P_DONE_QUALIFICATION": 1})

CHECKER_ID = "v4_369_offset_cancellation_servo"
CHECKER: Checker = check_v4_369_offset_cancellation_servo
