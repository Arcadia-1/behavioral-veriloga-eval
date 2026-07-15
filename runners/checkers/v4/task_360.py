"""Task-specific checker for canonical v4 DUT 360."""
from __future__ import annotations

from ..api import Checker
from dataclasses import dataclass

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

def _latest_before(values: list[float], target: float) -> float | None:
    latest = None
    for value in values:
        if value > target:
            break
        latest = value
    return latest

def _first_after(values: list[float], target: float, limit: float | None = None) -> float | None:
    for value in values:
        if value >= target and (limit is None or value <= limit):
            return value
    return None

def _control_clear_samples(
    rows: list[dict[str, float]], *, enable: str | None, settle: float
) -> list[dict[str, float]]:
    times = [float(rows[0]["time"]) + settle]
    times.extend(t + settle for t in _rising_times(rows, "rst"))
    if enable is not None:
        times.extend(t + settle for t in _falling_times(rows, enable))
    end = float(rows[-1]["time"])
    return [_sample_at(rows, min(t, end)) for t in times if t <= end]

def check_v4_360_digitally_controlled_delay_cell(rows: list[dict[str, float]]) -> tuple[bool, str]:
    pids = ["P_RESET_CLEAR", "P_CODE_CAPTURE_METRIC", "P_EDGE_DELAY_MAPPING", "P_PULSE_INTEGRITY_VALID"]
    required = {"time", "in_clk", "load", "rst", "out_clk", "delay_metric", "valid"} | {f"code_{i}" for i in range(6)}
    missing = _missing(rows, required, pids)
    if missing:
        return missing

    clear_bad = 0
    clear_gap = 0.0
    clear_time = 0.0
    clear_samples = _control_clear_samples(rows, enable=None, settle=0.6e-9)
    for row in clear_samples:
        gap = max(abs(float(row["out_clk"]) - VSS), abs(float(row["delay_metric"]) - VSS), abs(float(row["valid"]) - VSS))
        if gap > 0.08:
            clear_bad += 1
            if gap > clear_gap:
                clear_gap, clear_time = gap, float(row["time"])

    loads = _rising_times(rows, "load")
    metric_bad = 0
    metric_gap = 0.0
    metric_time = 0.0
    loaded: list[tuple[float, int]] = []
    for t in loads:
        row = _sample_at(rows, t + 0.45e-9)
        if _high(row, "rst"):
            continue
        code = _code(row, [f"code_{i}" for i in range(6)])
        loaded.append((t, code))
        expected = VDD * code / 63.0
        gap = abs(float(row["delay_metric"]) - expected)
        if gap > 0.055:
            metric_bad += 1
            if gap > metric_gap:
                metric_gap, metric_time = gap, float(row["time"])

    in_rises = _rising_times(rows, "in_clk")
    in_falls = _falling_times(rows, "in_clk")
    out_rises = _rising_times(rows, "out_clk")
    out_falls = _falling_times(rows, "out_clk")
    reset_rises = _rising_times(rows, "rst")
    delay_bad = 0
    delay_checks = 0
    delay_gap = 0.0
    delay_time = 0.0
    width_bad = 0
    width_checks = 0
    width_gap = 0.0
    width_time = 0.0
    first_output_rise = None
    for t in in_rises:
        load_t = _latest_before([item[0] for item in loaded], t)
        if load_t is None or _high(_sample_at(rows, t), "rst"):
            continue
        last_reset = _latest_before(reset_rises, t)
        if last_reset is not None and last_reset > load_t:
            continue
        code = next(code for lt, code in reversed(loaded) if lt <= t)
        observed = _first_after(out_rises, t, t + 1e-9)
        delay_checks += 1
        if observed is None:
            delay_bad += 1
            delay_gap, delay_time = 1e-9, t
            continue
        first_output_rise = observed if first_output_rise is None else min(first_output_rise, observed)
        expected = 20e-12 + 3e-12 * code
        gap = abs((observed - t) - expected)
        if gap > 65e-12:
            delay_bad += 1
            if gap > delay_gap:
                delay_gap, delay_time = gap, t
        in_fall = _first_after(in_falls, t, t + 8e-9)
        out_fall = _first_after(out_falls, observed, observed + 8e-9)
        if in_fall is not None and out_fall is not None:
            width_checks += 1
            gap_w = abs((out_fall - observed) - (in_fall - t))
            if gap_w > 90e-12:
                width_bad += 1
                if gap_w > width_gap:
                    width_gap, width_time = gap_w, t
    valid_bad = width_bad
    valid_checks = width_checks
    if first_output_rise is not None:
        valid_checks += 1
        row = _sample_at(rows, first_output_rise + 0.4e-9)
        if not _high(row, "valid"):
            valid_bad += 1
            width_time = float(row["time"])
            width_gap = max(width_gap, VTH - float(row["valid"]))

    return _finish([
        PropertyDiagnostic("P_RESET_CLEAR", clear_bad, "out_clk=delay_metric=valid=0", f"max_clear_gap={clear_gap:.3g}", clear_time, clear_gap, len(clear_samples)),
        PropertyDiagnostic("P_CODE_CAPTURE_METRIC", metric_bad, "metric=0.9*code/63", f"loaded_codes={[code for _, code in loaded]}", metric_time, metric_gap, len(loaded)),
        PropertyDiagnostic("P_EDGE_DELAY_MAPPING", delay_bad, "edge_delay=20ps+3ps*code", f"paired_edges={delay_checks-delay_bad}/{delay_checks}", delay_time, delay_gap, delay_checks),
        PropertyDiagnostic("P_PULSE_INTEGRITY_VALID", valid_bad, "equal_edge_delay_and_valid_after_first_rise", f"width_checks={width_checks} valid_seen={first_output_rise is not None}", width_time, width_gap, valid_checks),
    ])

CHECKER_ID = "v4_360_digitally_controlled_delay_cell"
CHECKER: Checker = check_v4_360_digitally_controlled_delay_cell
