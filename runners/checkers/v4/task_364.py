"""Task-specific checker for canonical v4 DUT 364."""
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

def check_v4_364_iq_upconversion_mixer_chain(rows: list[dict[str, float]]) -> tuple[bool, str]:
    pids = ["P_RESET_DISABLE_CLEAR", "P_IQ_SIGNED_MIXING", "P_RF_SUM_CLAMP", "P_QUADRATURE_ACTIVITY"]
    required = {"time", "i_in", "q_in", "lo_i", "lo_q", "rst", "enable", "rf_out", "i_mix_dbg", "q_mix_dbg", "quad_ok"}
    missing = _missing(rows, required, pids)
    if missing:
        return missing
    clear_samples = _control_clear_samples(rows, enable="enable", settle=0.7e-9)
    clear_bad = 0
    clear_gap = clear_time = 0.0
    for row in clear_samples:
        gap = max(abs(float(row["rf_out"]) - VCM), abs(float(row["i_mix_dbg"]) - VCM), abs(float(row["q_mix_dbg"]) - VCM), abs(float(row["quad_ok"])))
        if gap > 0.055:
            clear_bad += 1
            if gap > clear_gap:
                clear_gap, clear_time = gap, float(row["time"])

    lo_edges = sorted(_rising_times(rows, "lo_i") + _falling_times(rows, "lo_i") + _rising_times(rows, "lo_q") + _falling_times(rows, "lo_q"))
    control_edges = sorted(
        _rising_times(rows, "rst")
        + _falling_times(rows, "rst")
        + _rising_times(rows, "enable")
        + _falling_times(rows, "enable")
    )
    mix_bad = rf_bad = 0
    mix_checks = rf_checks = 0
    mix_gap = mix_time = rf_gap = rf_time = 0.0
    stride = max(1, len(rows) // 800)
    for row in rows[::stride]:
        t = float(row["time"])
        if not _active(row, enable="enable") or any(
            abs(t - edge) < 0.35e-9 for edge in lo_edges + control_edges
        ):
            continue
        si = 1.0 if _high(row, "lo_i") else -1.0
        sq = 1.0 if _high(row, "lo_q") else -1.0
        i_expected = VCM + (float(row["i_in"]) - VCM) * si
        q_expected = VCM - (float(row["q_in"]) - VCM) * sq
        gaps = [abs(float(row["i_mix_dbg"]) - i_expected), abs(float(row["q_mix_dbg"]) - q_expected)]
        mix_checks += 1
        gap = max(gaps)
        if gap > 0.035:
            mix_bad += 1
            if gap > mix_gap:
                mix_gap, mix_time = gap, t
        rf_expected = min(VDD, max(VSS, i_expected + q_expected - VCM))
        gap_rf = abs(float(row["rf_out"]) - rf_expected)
        rf_checks += 1
        if gap_rf > 0.035:
            rf_bad += 1
            if gap_rf > rf_gap:
                rf_gap, rf_time = gap_rf, t

    activity_bad = 0
    activity_checks = 0
    activity_gap = activity_time = 0.0
    seen_i = seen_q = False
    prev_i = float(rows[0]["lo_i"])
    prev_q = float(rows[0]["lo_q"])
    prev_enable = float(rows[0]["enable"])
    for row in rows[1:]:
        enabled = _active(row, enable="enable")
        if _high(row, "rst") or (prev_enable > VTH and float(row["enable"]) <= VTH):
            seen_i = seen_q = False
        if enabled:
            if (prev_i <= VTH < float(row["lo_i"])) or (prev_i >= VTH > float(row["lo_i"])):
                seen_i = True
            if (prev_q <= VTH < float(row["lo_q"])) or (prev_q >= VTH > float(row["lo_q"])):
                seen_q = True
            expected = seen_i and seen_q
            observed = _high(row, "quad_ok")
            # Allow one transition interval after the second qualifying edge.
            if observed != expected and not any(abs(float(row["time"]) - edge) < 0.35e-9 for edge in lo_edges):
                activity_bad += 1
                activity_gap, activity_time = 1.0, float(row["time"])
            activity_checks += 1
        prev_i, prev_q, prev_enable = float(row["lo_i"]), float(row["lo_q"]), float(row["enable"])
    return _finish([
        PropertyDiagnostic("P_RESET_DISABLE_CLEAR", clear_bad, "rf=i_dbg=q_dbg=vcm,quad_ok=0", f"max_clear_gap={clear_gap:.3g}", clear_time, clear_gap, len(clear_samples)),
        PropertyDiagnostic("P_IQ_SIGNED_MIXING", mix_bad, "I=+LOI product,Q=-LOQ product", f"samples={mix_checks}", mix_time, mix_gap, mix_checks, allowed_mismatches=max(2, mix_checks // 50)),
        PropertyDiagnostic("P_RF_SUM_CLAMP", rf_bad, "rf=clip(i_dbg+q_dbg-vcm)", f"samples={rf_checks}", rf_time, rf_gap, rf_checks, allowed_mismatches=max(2, rf_checks // 50)),
        PropertyDiagnostic("P_QUADRATURE_ACTIVITY", activity_bad, "quad_ok_after_both_LO_cross", f"seen_i={seen_i} seen_q={seen_q}", activity_time, activity_gap, activity_checks, allowed_mismatches=max(3, activity_checks // 100)),
    ])

CHECKER_ID = "v4_364_iq_upconversion_mixer_chain"
CHECKER: Checker = check_v4_364_iq_upconversion_mixer_chain
