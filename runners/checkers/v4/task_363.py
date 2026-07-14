"""Task-specific checker for canonical v4 DUT 363."""
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

def _latest_before(values: list[float], target: float) -> float | None:
    latest = None
    for value in values:
        if value > target:
            break
        latest = value
    return latest

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

def check_v4_363_fractional_n_synthesizer_mini_loop(rows: list[dict[str, float]]) -> tuple[bool, str]:
    pids = ["P_RESET_DISABLE_CLEAR", "P_FRACTIONAL_SELECTION", "P_DCO_DERIVED_DIVIDER", "P_RATIO_WINDOW", "P_FRACTION_MONOTONICITY"]
    required = {"time", "ref_clk", "dco_clk", "rst", "enable", "div_clk", "div_sel", "avg_ratio_metric", "valid"} | {f"frac_{i}" for i in range(4)}
    missing = _missing(rows, required, pids)
    if missing:
        return missing
    clear_samples = _control_clear_samples(rows, enable="enable", settle=0.8e-9)
    clear_bad = 0
    clear_gap = clear_time = 0.0
    for row in clear_samples:
        gap = max(abs(float(row["div_clk"])), abs(float(row["div_sel"])), abs(float(row["avg_ratio_metric"])), abs(float(row["valid"])))
        if gap > 0.08:
            clear_bad += 1
            if gap > clear_gap:
                clear_gap, clear_time = gap, float(row["time"])

    dco_rises = _rising_times(rows, "dco_clk")
    div_edges = sorted(_rising_times(rows, "div_clk") + _falling_times(rows, "div_clk"))
    control_resets = sorted(_rising_times(rows, "rst") + _falling_times(rows, "enable"))
    derive_bad = selection_bad = 0
    derive_checks = selection_checks = 0
    derive_gap = derive_time = selection_gap = selection_time = 0.0
    moduli: list[tuple[float, int, int]] = []
    for a, b in zip(div_edges, div_edges[1:]):
        if any(a < reset_time <= b for reset_time in control_resets):
            continue
        if not _active(_sample_at(rows, a + 0.25e-9), enable="enable"):
            continue
        row = _sample_at(rows, b + 0.25e-9)
        if not _active(row, enable="enable"):
            continue
        count = sum(a < edge <= b for edge in dco_rises)
        expected = 9 if _high(row, "div_sel") else 8
        moduli.append((b, count, expected))
        derive_checks += 1
        gap = abs(count - expected)
        if gap != 0:
            derive_bad += 1
            if gap > derive_gap:
                derive_gap, derive_time = float(gap), b
        selection_checks += 1
        if count not in {8, 9}:
            selection_bad += 1
            selection_gap, selection_time = max(selection_gap, float(min(abs(count - 8), abs(count - 9)))), b

    # A cleanly re-enabled modulo-16 accumulator commanded to code 15 must
    # select n_int, n_int, then n_int+1 on its first three divider decisions.
    # A threshold-at-15 mutation instead produces n_int, n_int+1, n_int.
    selection_probes: list[tuple[float, list[int]]] = []
    for enable_time in _rising_times(rows, "enable"):
        probe_edges = [edge for edge in div_edges if edge >= enable_time][:5]
        if len(probe_edges) < 5:
            continue
        probe_rows = [_sample_at(rows, edge + 0.25e-9) for edge in probe_edges]
        if any(_code(row, [f"frac_{i}" for i in range(4)]) != 15 for row in probe_rows):
            continue
        observed = [1 if _high(row, "div_sel") else 0 for row in probe_rows]
        selection_probes.append((enable_time, observed))
        for edge, actual, expected in zip(probe_edges, observed, [0, 0, 1]):
            selection_checks += 1
            if actual != expected:
                selection_bad += 1
                selection_gap = max(selection_gap, 1.0)
                selection_time = edge

    valid_rises = _rising_times(rows, "valid")
    ratio_bad = 0
    ratio_checks = 0
    ratio_gap = ratio_time = 0.0
    code_metrics: dict[int, list[float]] = {}
    code_changes = sorted(set(_rising_times(rows, "frac_0") + _falling_times(rows, "frac_0") + _rising_times(rows, "frac_1") + _falling_times(rows, "frac_1") + _rising_times(rows, "frac_2") + _falling_times(rows, "frac_2") + _rising_times(rows, "frac_3") + _falling_times(rows, "frac_3")))
    for t in valid_rises:
        row = _sample_at(rows, t + 0.3e-9)
        if not _active(row, enable="enable"):
            continue
        last_change = _latest_before(code_changes, t)
        if last_change is not None and t - last_change < 70e-9:
            continue
        code = _code(row, [f"frac_{i}" for i in range(4)])
        observed = float(row["avg_ratio_metric"])
        expected = 8.0 + code / 16.0
        gap = abs(observed - expected)
        ratio_checks += 1
        code_metrics.setdefault(code, []).append(observed)
        if gap > 0.045:
            ratio_bad += 1
            if gap > ratio_gap:
                ratio_gap, ratio_time = gap, t
    # valid must be a window pulse, not continuously asserted after one update.
    high_fraction = sum(1 for row in rows if _high(row, "valid")) / max(1, len(rows))
    if high_fraction > 0.08:
        ratio_bad += 1
        ratio_checks += 1
        ratio_gap = max(ratio_gap, high_fraction - 0.08)

    mono_bad = 0
    mono_checks = 0
    mono_gap = mono_time = 0.0
    points = [(code, sum(vals) / len(vals)) for code, vals in sorted(code_metrics.items())]
    for (c0, m0), (c1, m1) in zip(points, points[1:]):
        mono_checks += 1
        if c1 > c0 and m1 + 0.02 < m0:
            mono_bad += 1
            mono_gap = max(mono_gap, m0 - m1)
    # Fractional commands must produce both modulus selections when nonzero.
    nonzero_rows = [row for row in rows[:: max(1, len(rows) // 1000)] if _active(row, enable="enable") and _code(row, [f"frac_{i}" for i in range(4)]) > 0]
    if nonzero_rows and not any(_high(row, "div_sel") for row in nonzero_rows):
        selection_bad += 1
        selection_checks += 1
        selection_gap = max(selection_gap, 1.0)
    return _finish([
        PropertyDiagnostic("P_RESET_DISABLE_CLEAR", clear_bad, "all_public_outputs=0", f"max_clear_gap={clear_gap:.3g}", clear_time, clear_gap, len(clear_samples)),
        PropertyDiagnostic("P_FRACTIONAL_SELECTION", selection_bad, "code15_after_clear_selects_8_8_9", f"moduli={sorted(set(count for _, count, _ in moduli))} probes={selection_probes}", selection_time, selection_gap, selection_checks),
        PropertyDiagnostic("P_DCO_DERIVED_DIVIDER", derive_bad, "div_edges_after_8_or_9_dco_rises", f"intervals={derive_checks}", derive_time, derive_gap, derive_checks, allowed_mismatches=max(1, derive_checks // 20)),
        PropertyDiagnostic("P_RATIO_WINDOW", ratio_bad, "metric=8+frac/16_on_window_valid", f"valid_events={len(valid_rises)} high_fraction={high_fraction:.4f}", ratio_time, ratio_gap, ratio_checks),
        PropertyDiagnostic("P_FRACTION_MONOTONICITY", mono_bad, "higher_fraction_nondecreasing_metric", f"points={points}", mono_time, mono_gap, max(1, mono_checks)),
    ])

CHECKER_ID = "v4_363_fractional_n_synthesizer_mini_loop"
CHECKER: Checker = check_v4_363_fractional_n_synthesizer_mini_loop
