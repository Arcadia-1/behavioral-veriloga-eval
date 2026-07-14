"""Task-specific checker for canonical v4 DUT 362."""
from __future__ import annotations

from checkers.api import Checker
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

def _control_clear_samples(
    rows: list[dict[str, float]], *, enable: str | None, settle: float
) -> list[dict[str, float]]:
    times = [float(rows[0]["time"]) + settle]
    times.extend(t + settle for t in _rising_times(rows, "rst"))
    if enable is not None:
        times.extend(t + settle for t in _falling_times(rows, enable))
    end = float(rows[-1]["time"])
    return [_sample_at(rows, min(t, end)) for t in times if t <= end]

def check_v4_362_frequency_word_dco_divider_monitor(rows: list[dict[str, float]]) -> tuple[bool, str]:
    pids = ["P_RESET_DISABLE_STOP", "P_FREQUENCY_WORD_MAPPING", "P_DIVIDER_MONITOR", "P_RESTART_MONOTONICITY"]
    required = {"time", "enable", "rst", "dco_clk", "div_clk", "freq_metric"} | {f"fcw_{i}" for i in range(6)}
    missing = _missing(rows, required, pids)
    if missing:
        return missing
    clear_samples = _control_clear_samples(rows, enable="enable", settle=0.8e-9)
    clear_bad = clear_gap = clear_time = 0
    for row in clear_samples:
        gap = max(abs(float(row["dco_clk"])), abs(float(row["div_clk"])), abs(float(row["freq_metric"])))
        if gap > 0.08:
            clear_bad += 1
            clear_gap, clear_time = max(clear_gap, gap), float(row["time"])

    metric_bad = 0
    metric_checks = 0
    metric_gap = metric_time = 0.0
    code_edges = sorted(
        edge
        for bit in range(6)
        for edge in (_rising_times(rows, f"fcw_{bit}") + _falling_times(rows, f"fcw_{bit}"))
    )
    control_edges = sorted(code_edges + _rising_times(rows, "enable") + _falling_times(rows, "enable") + _rising_times(rows, "rst") + _falling_times(rows, "rst"))
    for row in rows[:: max(1, len(rows) // 500)]:
        if not _active(row, enable="enable"):
            continue
        if any(abs(float(row["time"]) - edge) < 0.6e-9 for edge in control_edges):
            continue
        code = _code(row, [f"fcw_{i}" for i in range(6)])
        target = min(250e6, 80e6 + 2e6 * code)
        expected = 0.9 * (target - 80e6) / 170e6
        gap = abs(float(row["freq_metric"]) - expected)
        metric_checks += 1
        if gap > 0.045:
            metric_bad += 1
            if gap > metric_gap:
                metric_gap, metric_time = gap, float(row["time"])

    dco_rises = _rising_times(rows, "dco_clk")
    divider_control_edges = sorted(
        _falling_times(rows, "enable") + _rising_times(rows, "rst")
    )
    divider_interval_breaks = sorted(
        _rising_times(rows, "enable")
        + _falling_times(rows, "enable")
        + _rising_times(rows, "rst")
        + _falling_times(rows, "rst")
    )
    div_edges = sorted(
        edge
        for edge in (_rising_times(rows, "div_clk") + _falling_times(rows, "div_clk"))
        if not any(abs(edge - control_edge) < 0.6e-9 for control_edge in divider_control_edges)
    )
    divider_bad = 0
    divider_checks = 0
    divider_gap = divider_time = 0.0
    for a, b in zip(div_edges, div_edges[1:]):
        if any(a < control_edge < b for control_edge in divider_interval_breaks):
            continue
        mid = _sample_at(rows, 0.5 * (a + b))
        if not _active(mid, enable="enable"):
            continue
        count = sum(a < edge <= b for edge in dco_rises)
        divider_checks += 1
        gap = abs(count - 4)
        if gap != 0:
            divider_bad += 1
            if gap > divider_gap:
                divider_gap, divider_time = float(gap), b

    restart_bad = 0
    restart_checks = 0
    restart_gap = restart_time = 0.0
    enable_rises = _rising_times(rows, "enable")
    rates: list[tuple[int, float]] = []
    for start in enable_rises:
        row = _sample_at(rows, start + 1e-12)
        if _high(row, "rst"):
            continue
        code = _code(row, [f"fcw_{i}" for i in range(6)])
        target = min(250e6, 80e6 + 2e6 * code)
        first = _first_after(dco_rises, start)
        if first is not None:
            restart_checks += 1
            gap = abs((first - start) - 0.5 / target)
            if gap > 0.55e-9:
                restart_bad += 1
                restart_gap, restart_time = gap, start
    # Stable-code period checks also enforce monotonic frequency behavior.
    for a, b in zip(dco_rises, dco_rises[1:]):
        row = _sample_at(rows, 0.5 * (a + b))
        if not _active(row, enable="enable"):
            continue
        code = _code(row, [f"fcw_{i}" for i in range(6)])
        rates.append((code, 1.0 / (b - a)))
    by_code: dict[int, list[float]] = {}
    for code, freq in rates:
        by_code.setdefault(code, []).append(freq)
    medians = [(code, sorted(vals)[len(vals) // 2]) for code, vals in sorted(by_code.items()) if len(vals) >= 2]
    for (c0, f0), (c1, f1) in zip(medians, medians[1:]):
        restart_checks += 1
        if c1 > c0 and f1 + 0.02 * f0 < f0:
            restart_bad += 1
            restart_gap = max(restart_gap, f0 - f1)
    return _finish([
        PropertyDiagnostic("P_RESET_DISABLE_STOP", int(clear_bad), "clocks=metric=0", f"max_clear_gap={clear_gap:.3g}", float(clear_time), float(clear_gap), len(clear_samples)),
        PropertyDiagnostic("P_FREQUENCY_WORD_MAPPING", metric_bad, "metric_normalizes_80_to_250MHz", f"sampled={metric_checks}", metric_time, metric_gap, metric_checks, allowed_mismatches=max(2, metric_checks // 20)),
        PropertyDiagnostic("P_DIVIDER_MONITOR", divider_bad, "four_dco_rises_per_div_toggle", f"intervals={divider_checks}", divider_time, divider_gap, divider_checks),
        PropertyDiagnostic("P_RESTART_MONOTONICITY", restart_bad, "half_period_restart_and_nondecreasing_rate", f"codes={[code for code, _ in medians]}", restart_time, restart_gap, restart_checks),
    ])

CHECKER_ID = "v4_362_frequency_word_dco_divider_monitor"
CHECKER: Checker = check_v4_362_frequency_word_dco_divider_monitor
