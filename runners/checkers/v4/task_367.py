"""Task-specific checker for canonical v4 DUT 367."""
from __future__ import annotations

from checkers.api import Checker
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

def _active(row: dict[str, float], *, enable: str | None = None, reset: str = "rst") -> bool:
    return not _high(row, reset) and (enable is None or _high(row, enable))

def _control_clear_samples(
    rows: list[dict[str, float]], *, enable: str | None, settle: float
) -> list[dict[str, float]]:
    times = [float(rows[0]["time"]) + settle]
    times.extend(t + settle for t in _rising_times(rows, "rst"))
    if enable is not None:
        times.extend(t + settle for t in _falling_times(rows, enable))
    end = float(rows[-1]["time"])
    return [_sample_at(rows, min(t, end)) for t in times if t <= end]

def check_v4_367_baseband_agc_filter_chain(rows: list[dict[str, float]]) -> tuple[bool, str]:
    pids = ["P_RESET_DISABLE_CLEAR", "P_LEVEL_GAIN_CONTROL", "P_VGA_FILTER_RESPONSE", "P_CLIP_AND_SETTLE"]
    required = {"time", "vin", "target", "clk", "rst", "enable", "vout", "level_metric", "clip_flag", "settled"} | {f"gain_{i}" for i in range(4)}
    missing = _missing(rows, required, pids)
    if missing:
        return missing
    clear_samples = _control_clear_samples(rows, enable="enable", settle=0.8e-9)
    clear_bad = 0
    clear_gap = clear_time = 0.0
    for row in clear_samples:
        code = _code(row, [f"gain_{i}" for i in range(4)])
        gap = max(abs(code - 4) / 15.0, abs(float(row["vout"]) - VCM), abs(float(row["level_metric"])), abs(float(row["clip_flag"])), abs(float(row["settled"])))
        if gap > 0.08:
            clear_bad += 1
            if gap > clear_gap:
                clear_gap, clear_time = gap, float(row["time"])

    level_bad = filter_bad = status_bad = 0
    level_checks = filter_checks = status_checks = 0
    level_gap = level_time = filter_gap = filter_time = status_gap = status_time = 0.0
    clock_edges = _rising_times(rows, "clk")
    prev_code = 4
    prev_level = 0.0
    prev_vout = VCM
    settle_streak = 0
    clip_seen = settled_seen = False
    for t in clock_edges:
        after = _sample_at(rows, t + 0.65e-9)
        if not _active(after, enable="enable"):
            prev_code, prev_level, prev_vout, settle_streak = 4, 0.0, VCM, 0
            continue
        code = _code(after, [f"gain_{i}" for i in range(4)])
        level_expected = abs(float(after["vin"]) - VCM)
        gap_level = abs(float(after["level_metric"]) - level_expected)
        level_checks += 1
        if gap_level > 0.025:
            level_bad += 1
            if gap_level > level_gap:
                level_gap, level_time = gap_level, t
        err = float(after["target"]) - prev_level
        expected_step = 1 if err > 0.02 and prev_code < 15 else -1 if err < -0.02 and prev_code > 0 else 0
        gap_code = abs((code - prev_code) - expected_step)
        if gap_code > 0:
            level_bad += 1
            level_gap, level_time = max(level_gap, float(gap_code)), t

        gain = 0.5 + 0.1 * code
        vga = VCM + gain * (float(after["vin"]) - VCM)
        raw = prev_vout + 0.25 * (vga - prev_vout)
        expected_vout = min(VDD, max(VSS, raw))
        gap_out = abs(float(after["vout"]) - expected_vout)
        filter_checks += 1
        if gap_out > 0.055:
            filter_bad += 1
            if gap_out > filter_gap:
                filter_gap, filter_time = gap_out, t

        expected_clip = raw < VSS or raw > VDD
        observed_clip = _high(after, "clip_flag")
        clip_seen = clip_seen or observed_clip
        settle_streak = settle_streak + 1 if abs(prev_level - float(after["target"])) <= 0.02 else 0
        expected_settled = settle_streak >= 3
        observed_settled = _high(after, "settled")
        settled_seen = settled_seen or observed_settled
        status_checks += 1
        if observed_clip != expected_clip or observed_settled != expected_settled:
            status_bad += 1
            status_gap, status_time = 1.0, t
        prev_code, prev_level, prev_vout = code, float(after["level_metric"]), float(after["vout"])
    if not clip_seen:
        status_bad += 1
        status_checks += 1
        status_gap = max(status_gap, 1.0)
    if not settled_seen:
        status_bad += 1
        status_checks += 1
        status_gap = max(status_gap, 1.0)
    return _finish([
        PropertyDiagnostic("P_RESET_DISABLE_CLEAR", clear_bad, "gain=4,vout=vcm,metrics_flags=0", f"max_clear_gap={clear_gap:.3g}", clear_time, clear_gap, len(clear_samples)),
        PropertyDiagnostic("P_LEVEL_GAIN_CONTROL", level_bad, "level=abs(vin-vcm),gain_moves_to_target", f"clock_checks={level_checks}", level_time, level_gap, level_checks, allowed_mismatches=max(2, level_checks // 10)),
        PropertyDiagnostic("P_VGA_FILTER_RESPONSE", filter_bad, "alpha=0.25_toward_unclamped_vga_then_rail_clip", f"samples={filter_checks}", filter_time, filter_gap, filter_checks, allowed_mismatches=max(1, filter_checks // 12)),
        PropertyDiagnostic("P_CLIP_AND_SETTLE", status_bad, "clip_on_raw_excursion,settled_after_three", f"clip_seen={clip_seen} settled_seen={settled_seen}", status_time, status_gap, status_checks, allowed_mismatches=max(1, status_checks // 12)),
    ])

CHECKER_ID = "v4_367_baseband_agc_filter_chain"
CHECKER: Checker = check_v4_367_baseband_agc_filter_chain
