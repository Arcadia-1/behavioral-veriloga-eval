"""Task-specific checker for canonical v4 DUT 365."""
from __future__ import annotations

from ..api import Checker
from dataclasses import dataclass

VCM = 0.45
VDD = 0.9
VSS = 0.0
VTH = 0.45

@dataclass(frozen=True)
class PropertyDiagnostic:
    property_id: str
    mismatch_count: int
    expected: str
    observed: str
    sample_time: float
    metric_gap: float
    checks: int
    allowed_mismatches: int = 0

    @property
    def passed(self) -> bool:
        return self.checks > 0 and self.mismatch_count <= self.allowed_mismatches

    def render(self) -> str:
        return (
            f"{self.property_id} status={'PASS' if self.passed else 'FAIL'} "
            f"mismatch_count={self.mismatch_count} allowed={self.allowed_mismatches} "
            f"checks={self.checks} expected={self.expected} observed={self.observed} "
            f"time={self.sample_time:.12g} gap={self.metric_gap:.6g}"
        )

def _finish(diags: Iterable[PropertyDiagnostic]) -> tuple[bool, str]:
    records = list(diags)
    return all(item.passed for item in records), " | ".join(item.render() for item in records)

def _missing(rows: list[dict[str, float]], required: set[str], property_ids: list[str]) -> tuple[bool, str] | None:
    missing = sorted(required - (set(rows[0]) if rows else set()))
    if not missing:
        return None
    return _finish(
        PropertyDiagnostic(pid, 1, "complete_trace", f"missing={','.join(missing)}", 0.0, float(len(missing)), 1)
        for pid in property_ids
    )

def _high(row: dict[str, float], name: str, threshold: float = VTH) -> bool:
    return float(row[name]) > threshold

def _code(row: dict[str, float], bits_lsb_first: list[str]) -> int:
    return sum((1 << index) for index, name in enumerate(bits_lsb_first) if _high(row, name))

def _signed_sign_magnitude(code: int) -> int:
    return -(code - 7) if code >= 8 else code

def _rising_times(rows: list[dict[str, float]], signal: str, threshold: float = VTH) -> list[float]:
    return _crossing_times(rows, signal, threshold, rising=True)

def _falling_times(rows: list[dict[str, float]], signal: str, threshold: float = VTH) -> list[float]:
    return _crossing_times(rows, signal, threshold, rising=False)

def _crossing_times(
    rows: list[dict[str, float]], signal: str, threshold: float, *, rising: bool
) -> list[float]:
    result: list[float] = []
    for before, after in zip(rows, rows[1:]):
        v0 = float(before[signal])
        v1 = float(after[signal])
        crossed = v0 <= threshold < v1 if rising else v0 >= threshold > v1
        if not crossed:
            continue
        t0 = float(before["time"])
        t1 = float(after["time"])
        fraction = 1.0 if v1 == v0 else (threshold - v0) / (v1 - v0)
        result.append(t0 + fraction * (t1 - t0))
    return result

def _sample_at(rows: list[dict[str, float]], target: float) -> dict[str, float]:
    lo, hi = 0, len(rows) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if float(rows[mid]["time"]) < target:
            lo = mid + 1
        else:
            hi = mid
    return rows[lo]

def _control_clear_samples(
    rows: list[dict[str, float]], *, enable: str | None, settle: float
) -> list[dict[str, float]]:
    times = [float(rows[0]["time"]) + settle]
    times.extend(t + settle for t in _rising_times(rows, "rst"))
    if enable is not None:
        times.extend(t + settle for t in _falling_times(rows, enable))
    end = float(rows[-1]["time"])
    return [_sample_at(rows, min(t, end)) for t in times if t <= end]

def check_v4_365_quadrature_correction_loop(rows: list[dict[str, float]]) -> tuple[bool, str]:
    pids = ["P_RESET_CLEAR", "P_TRIM_DIRECTION", "P_CORRECTION_APPLICATION", "P_LOCK_HOLD"]
    required = {"time", "i_in", "q_in", "clk", "rst", "cal_en", "i_out", "q_out", "error_metric", "locked"} | {f"gain_code_{i}" for i in range(4)} | {f"phase_code_{i}" for i in range(4)}
    missing = _missing(rows, required, pids)
    if missing:
        return missing
    clear_samples = _control_clear_samples(rows, enable=None, settle=0.7e-9)
    clear_bad = 0
    clear_gap = clear_time = 0.0
    for row in clear_samples:
        g = _code(row, [f"gain_code_{i}" for i in range(4)])
        p = _code(row, [f"phase_code_{i}" for i in range(4)])
        gap = max(g / 15.0, p / 15.0, abs(float(row["i_out"]) - VCM), abs(float(row["q_out"]) - VCM), abs(float(row["error_metric"])), abs(float(row["locked"])))
        if gap > 0.07:
            clear_bad += 1
            if gap > clear_gap:
                clear_gap, clear_time = gap, float(row["time"])

    trim_bad = correction_bad = 0
    trim_checks = correction_checks = 0
    trim_gap = trim_time = correction_gap = correction_time = 0.0
    clock_edges = _rising_times(rows, "clk")
    reset_rises = _rising_times(rows, "rst")
    last_gain = last_phase = 0
    last_clock_t: float | None = None
    hold_bad = 0
    hold_checks = 0
    hold_gap = hold_time = 0.0
    good_streak = 0
    for t in clock_edges:
        before = _sample_at(rows, max(0.0, t - 0.3e-9))
        after = _sample_at(rows, t + 0.55e-9)
        if any((last_clock_t is None or last_clock_t < reset_t < t) for reset_t in reset_rises):
            last_gain = last_phase = 0
            good_streak = 0
        if _high(before, "rst") or _high(after, "rst"):
            last_gain = last_phase = 0
            good_streak = 0
            last_clock_t = t
            continue
        gain = _signed_sign_magnitude(_code(after, [f"gain_code_{i}" for i in range(4)]))
        phase = _signed_sign_magnitude(_code(after, [f"phase_code_{i}" for i in range(4)]))
        if _high(after, "cal_en"):
            trim_checks += 1
            i_dev = float(before["i_in"]) - VCM
            q_dev = float(before["q_in"]) - VCM
            gain_error = abs(i_dev) - abs(q_dev) - last_gain * 0.01
            phase_error = i_dev * q_dev - last_phase * 0.01
            expected_gain_step = 1 if gain_error > 0.015 and last_gain < 7 else -1 if gain_error < -0.015 and last_gain > -8 else 0
            expected_phase_step = 1 if phase_error > 0.015 and last_phase < 7 else -1 if phase_error < -0.015 and last_phase > -8 else 0
            observed_gain_step = gain - last_gain
            observed_phase_step = phase - last_phase
            gap = max(abs(observed_gain_step - expected_gain_step), abs(observed_phase_step - expected_phase_step))
            if gap > 0:
                trim_bad += 1
                if gap > trim_gap:
                    trim_gap, trim_time = float(gap), t
            metric_expected = (float(after["i_in"]) - VCM) * (float(after["q_in"]) - VCM) - phase * 0.01
            metric_gap = abs(float(after["error_metric"]) - metric_expected)
            if metric_gap > 0.02:
                trim_bad += 1
                trim_gap, trim_time = max(trim_gap, metric_gap), t
            good_streak = good_streak + 1 if abs(phase_error) <= 0.015 else 0
            if _high(after, "locked") != (good_streak >= 3):
                hold_bad += 1
                hold_gap, hold_time = 1.0, t
            hold_checks += 1
        else:
            hold_checks += 1
            if gain != last_gain or phase != last_phase:
                hold_bad += 1
                hold_gap, hold_time = float(abs(gain-last_gain)+abs(phase-last_phase)), t
        i_dev = float(after["i_in"]) - VCM
        q_dev = float(after["q_in"]) - VCM
        i_expected = min(VDD, max(VSS, VCM + i_dev - 0.5 * gain * 0.01))
        q_expected = min(VDD, max(VSS, VCM + q_dev + 0.5 * gain * 0.01 - phase * 0.01 * i_dev / VCM))
        gap_out = max(abs(float(after["i_out"]) - i_expected), abs(float(after["q_out"]) - q_expected))
        correction_checks += 1
        if gap_out > 0.035:
            correction_bad += 1
            if gap_out > correction_gap:
                correction_gap, correction_time = gap_out, t
        last_gain, last_phase = gain, phase
        last_clock_t = t
    return _finish([
        PropertyDiagnostic("P_RESET_CLEAR", clear_bad, "codes=metric=lock=0,outputs=vcm", f"max_clear_gap={clear_gap:.3g}", clear_time, clear_gap, len(clear_samples)),
        PropertyDiagnostic("P_TRIM_DIRECTION", trim_bad, "signed_trim_steps_reduce_error", f"clock_checks={trim_checks}", trim_time, trim_gap, trim_checks, allowed_mismatches=max(1, trim_checks // 12)),
        PropertyDiagnostic("P_CORRECTION_APPLICATION", correction_bad, "outputs_follow_exposed_signed_codes", f"samples={correction_checks}", correction_time, correction_gap, correction_checks, allowed_mismatches=max(1, correction_checks // 15)),
        PropertyDiagnostic("P_LOCK_HOLD", hold_bad, "lock_after_three_and_codes_hold_when_cal_off", f"checks={hold_checks}", hold_time, hold_gap, hold_checks, allowed_mismatches=max(1, hold_checks // 15)),
    ])

CHECKER_ID = "v4_365_quadrature_correction_loop"
CHECKER: Checker = check_v4_365_quadrature_correction_loop
