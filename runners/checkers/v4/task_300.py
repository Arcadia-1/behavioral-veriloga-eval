"""Task-specific checker for canonical v4 DUT 300."""
from __future__ import annotations

from ..api import Checker
import math

def _v3_integrated_mod_phase_values(
    rows: list[dict[str, float]],
    *,
    freq_fn,
    modulus: float,
) -> list[float]:
    phase = 0.0
    phases = [phase]
    for prev, row in zip(rows, rows[1:]):
        dt = max(0.0, row["time"] - prev["time"])
        if prev.get("rst", 0.0) <= 0.45 and row.get("rst", 0.0) <= 0.45:
            f0 = freq_fn(prev)
            f1 = freq_fn(row)
            phase = (phase + 0.5 * (f0 + f1) * dt) % modulus
        phases.append(phase)
    return phases

def check_v3_503_differential_vco_clip_idtmod(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vinp", "vinm", "outp", "outm", "metric"}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing)

    fnom = 20.0e6
    dfdv = 160.0e6
    fmin = 5.0e6
    fmax = 80.0e6
    vcm = 0.45
    vac = 0.4

    def _clip(x: float) -> float:
        return fmin if x < fmin else (fmax if x > fmax else x)

    phases = _v3_integrated_mod_phase_values(
        rows,
        freq_fn=lambda row: _clip(fnom + dfdv * (row["vinp"] - row["vinm"])),
        modulus=1.0,
    )
    two_pi = 2.0 * math.pi
    stride = max(1, len(rows) // 160)
    checked = 0
    max_err = 0.0
    outp_span_lo: float | None = None
    outp_span_hi: float | None = None
    saw_upper_clamp_case = any(fnom + dfdv * (row["vinp"] - row["vinm"]) > fmax for row in rows)
    for index in range(0, len(rows), stride):
        if rows[index]["time"] < 8.0e-9:
            continue
        phase = phases[index]
        outp_expected = vcm + vac * math.sin(two_pi * phase)
        outm_expected = vcm - vac * math.sin(two_pi * phase)
        metric_expected = 0.9 * phase
        outp_err = abs(rows[index]["outp"] - outp_expected)
        outm_err = abs(rows[index]["outm"] - outm_expected)
        max_err = max(max_err, outp_err, outm_err)
        checked += 1
        outp_span_lo = outp_expected if outp_span_lo is None else min(outp_span_lo, outp_expected)
        outp_span_hi = outp_expected if outp_span_hi is None else max(outp_span_hi, outp_expected)
        if outp_err > 0.08:
            return False, (
                f"outp@{rows[index]['time'] * 1e9:g}ns={rows[index]['outp']:.4f} "
                f"expected={outp_expected:.4f} tol=0.0800"
            )
        if outm_err > 0.08:
            return False, (
                f"outm@{rows[index]['time'] * 1e9:g}ns={rows[index]['outm']:.4f} "
                f"expected={outm_expected:.4f} tol=0.0800"
            )
        if 0.05 < phase < 0.95:
            metric_err = abs(rows[index]["metric"] - metric_expected)
            max_err = max(max_err, metric_err)
            if metric_err > 0.06:
                return False, (
                    f"metric@{rows[index]['time'] * 1e9:g}ns={rows[index]['metric']:.4f} "
                    f"expected={metric_expected:.4f} tol=0.0600"
                )
    if checked < 20:
        return False, f"insufficient_samples={checked}"
    outp_span = (outp_span_hi - outp_span_lo) if (outp_span_lo is not None) else 0.0
    if outp_span < 0.5 * vac:
        return False, f"insufficient_outp_dynamic_range={outp_span:.4f}"
    clamp_note = " upper_clamp_exercised" if saw_upper_clamp_case else ""
    return True, f"samples={checked} outp_span={outp_span:.4f} max_err={max_err:.4f}{clamp_note}"

CHECKER_ID = "v4_300_differential_vco_clip_idtmod"
CHECKER: Checker = check_v3_503_differential_vco_clip_idtmod
