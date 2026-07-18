"""Task-specific checker for canonical v4 DUT 361."""
from __future__ import annotations

from ..api import Checker
from dataclasses import dataclass

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

def _first_after(values: list[float], target: float, limit: float | None = None) -> float | None:
    for value in values:
        if value >= target and (limit is None or value <= limit):
            return value
    return None

def _active(row: dict[str, float], *, enable: str | None = None, reset: str = "rst") -> bool:
    return not _high(row, reset) and (enable is None or _high(row, enable))

def _period_scale(edges: list[float], nominal_period: float) -> float:
    periods = [b - a for a, b in zip(edges, edges[1:]) if b > a]
    if not periods:
        return 1.0
    return sorted(periods)[len(periods) // 2] / nominal_period

def _control_clear_samples(
    rows: list[dict[str, float]], *, enable: str | None, settle: float
) -> list[dict[str, float]]:
    times = [float(rows[0]["time"]) + settle]
    times.extend(t + settle for t in _rising_times(rows, "rst"))
    if enable is not None:
        times.extend(t + settle for t in _falling_times(rows, enable))
    end = float(rows[-1]["time"])
    return [_sample_at(rows, min(t, end)) for t in times if t <= end]

def check_v4_361_dll_delay_line_lock(rows: list[dict[str, float]]) -> tuple[bool, str]:
    pids = ["P_RESET_DISABLE_CLEAR", "P_DELAY_LINE_DERIVATION", "P_PHASE_CORRECTION", "P_LOCK_QUALIFICATION"]
    required = {"time", "ref_clk", "in_clk", "rst", "enable", "delayed_clk", "up", "down", "lock"} | {f"delay_{i}" for i in range(5)}
    missing = _missing(rows, required, pids)
    if missing:
        return missing

    in_edges = _rising_times(rows, "in_clk")
    time_scale = _period_scale(in_edges, 10e-9)
    clear_samples = _control_clear_samples(
        rows, enable="enable", settle=0.7e-9 * time_scale
    )
    clear_bad = 0
    clear_gap = clear_time = 0.0
    for row in clear_samples:
        code = _code(row, [f"delay_{i}" for i in range(5)])
        gap = max(abs(code - 16) / 31.0, abs(float(row["delayed_clk"])), abs(float(row["up"])), abs(float(row["down"])), abs(float(row["lock"])))
        if gap > 0.10:
            clear_bad += 1
            if gap > clear_gap:
                clear_gap, clear_time = gap, float(row["time"])

    delayed_edges = _rising_times(rows, "delayed_clk")
    delay_bad = 0
    delay_checks = 0
    delay_gap = delay_time = 0.0
    for t in in_edges:
        row = _sample_at(rows, t)
        if not _active(row, enable="enable"):
            continue
        code = _code(row, [f"delay_{i}" for i in range(5)])
        observed = _first_after(delayed_edges, t, t + 1e-9 * time_scale)
        delay_checks += 1
        if observed is None:
            delay_bad += 1
            delay_gap, delay_time = 1e-9 * time_scale, t
            continue
        actual = observed - t
        low = (code * 5e-12 + 18e-12) * time_scale
        high = (code * 5e-12 + 85e-12) * time_scale
        gap = max(low - actual, actual - high, 0.0)
        if gap > 0:
            delay_bad += 1
            if gap > delay_gap:
                delay_gap, delay_time = gap, t

    ref_edges = _rising_times(rows, "ref_clk")
    phase_bad = 0
    phase_checks = 0
    phase_gap = phase_time = 0.0
    good_streak = 0
    premature_lock = 0
    lock_seen = False
    for ref_t in ref_edges:
        row0 = _sample_at(rows, ref_t)
        if not _active(row0, enable="enable"):
            good_streak = 0
            continue
        delayed_t = min(delayed_edges, key=lambda value: abs(value - ref_t), default=None)
        if delayed_t is None or abs(delayed_t - ref_t) > 2e-9 * time_scale:
            continue
        sample = _sample_at(rows, max(ref_t, delayed_t) + 0.45e-9 * time_scale)
        dt = ref_t - delayed_t
        phase_threshold = 1.25e-12 * time_scale
        expected = "up" if dt > phase_threshold else "down" if dt < -phase_threshold else "none"
        observed = "both" if _high(sample, "up") and _high(sample, "down") else "up" if _high(sample, "up") else "down" if _high(sample, "down") else "none"
        phase_checks += 1
        if observed != expected:
            phase_bad += 1
            phase_gap, phase_time = abs(dt), float(sample["time"])
        if abs(dt) <= 5e-12 * time_scale:
            good_streak += 1
        else:
            good_streak = 0
        if _high(sample, "lock"):
            lock_seen = True
            if good_streak < 4:
                premature_lock += 1
                phase_time = float(sample["time"])
    lock_bad = premature_lock + (0 if lock_seen else 1)
    return _finish([
        PropertyDiagnostic("P_RESET_DISABLE_CLEAR", clear_bad, "code=16 and clocks/status=0", f"max_clear_gap={clear_gap:.3g}", clear_time, clear_gap, len(clear_samples)),
        PropertyDiagnostic("P_DELAY_LINE_DERIVATION", delay_bad, "input-derived delay=code*5ps", f"paired_edges={delay_checks-delay_bad}/{delay_checks}", delay_time, delay_gap, delay_checks, allowed_mismatches=max(1, delay_checks // 12)),
        PropertyDiagnostic("P_PHASE_CORRECTION", phase_bad, "up_if_delayed_early_down_if_late", f"comparisons={phase_checks} mismatches={phase_bad}", phase_time, phase_gap, phase_checks, allowed_mismatches=max(2, phase_checks // 10)),
        PropertyDiagnostic("P_LOCK_QUALIFICATION", lock_bad, "lock_after_four_in_window", f"lock_seen={lock_seen} premature={premature_lock}", phase_time, float(premature_lock), max(1, phase_checks)),
    ])

CHECKER_ID = "v4_361_dll_delay_line_lock"
CHECKER: Checker = check_v4_361_dll_delay_line_lock
