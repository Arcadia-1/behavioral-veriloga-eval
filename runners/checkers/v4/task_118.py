"""Task-specific checker for canonical v4 DUT 118."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import crossings, diagnostic, pass_note, require_signals, sample


PROPERTY_IDS = (
    "P_POSITIVE_UNITY",
    "P_NEGATIVE_UNITY",
    "P_CHANNEL_INDEPENDENCE",
    "P_DIFFERENTIAL_PRESERVATION",
    "P_COMMON_MODE_PRESERVATION",
)


def _signal_threshold_edges(
    rows: list[dict[str, float]],
    signal: str,
    *,
    threshold: float = 0.45,
    directions: tuple[str, ...] = ("rising", "falling"),
) -> list[float]:
    edges: list[float] = []
    for direction in directions:
        edges.extend(crossings(rows, signal, threshold=threshold, direction=direction))
    return sorted(edges)

def _stable_probe_times(
    rows: list[dict[str, float]],
    signals: list[str],
    *,
    threshold: float = 0.45,
    settle_s: float = 0.3e-9,
) -> list[float]:
    if not rows:
        return []
    first_t = rows[0]["time"]
    last_t = rows[-1]["time"]
    cuts = [first_t, last_t]
    for signal in signals:
        cuts.extend(_signal_threshold_edges(rows, signal, threshold=threshold))
    cuts = sorted({t for t in cuts if first_t <= t <= last_t})
    probes: list[float] = []
    for start_t, end_t in zip(cuts, cuts[1:]):
        width = end_t - start_t
        if width <= 2.0 * settle_s:
            continue
        probe_t = 0.5 * (start_t + end_t)
        if start_t + settle_s <= probe_t <= end_t - settle_s:
            probes.append(probe_t)
    return probes

def check_v3_differential_buffer(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vinp", "vinn", "voutp", "voutn"}
    missing = require_signals(rows, required, "P_DIFFERENTIAL_PRESERVATION")
    if missing:
        return False, missing

    probes = _stable_probe_times(rows, ["vinp", "vinn"], threshold=0.45, settle_s=0.5e-9)
    if len(probes) < 2:
        return False, diagnostic(
            "P_CHANNEL_INDEPENDENCE",
            "insufficient_probe_windows",
            expected="probe_windows>=2",
            observed=f"probe_windows={len(probes)}",
            event="input_transition_windows",
        )

    max_err = 0.0
    diff_signs: set[int] = set()
    checked = 0
    for index, time_s in enumerate(probes):
        vinp = sample(rows, "vinp", time_s)
        vinn = sample(rows, "vinn", time_s)
        voutp = sample(rows, "voutp", time_s)
        voutn = sample(rows, "voutn", time_s)
        if vinp is None or vinn is None or voutp is None or voutn is None:
            return False, diagnostic(
                "P_DIFFERENTIAL_PRESERVATION",
                "missing_sample",
                expected="vinp,vinn,voutp,voutn",
                observed="unavailable",
                event=f"stable_window[{index}]",
            )
        err = max(abs(voutp - vinp), abs(voutn - vinn))
        max_err = max(max_err, err)
        if err > 0.025:
            return False, diagnostic(
                "P_DIFFERENTIAL_PRESERVATION",
                "buffer_gain_mismatch",
                expected="voutp=vinp,voutn=vinn",
                observed=f"pair_err={err:.4f}",
                event=f"stable_window[{index}]",
            )
        diff = vinp - vinn
        if abs(diff) > 0.05:
            diff_signs.add(1 if diff > 0.0 else -1)
        checked += 1
    if checked < 2:
        return False, diagnostic(
            "P_CHANNEL_INDEPENDENCE",
            "insufficient_checks",
            expected="checked>=2",
            observed=f"checked={checked}",
            event="stable_window_set",
        )
    if diff_signs != {-1, 1}:
        return False, diagnostic(
            "P_DIFFERENTIAL_PRESERVATION",
            "insufficient_polarity_coverage",
            expected="diff_signs=-1,1",
            observed="diff_signs=" + ",".join(str(value) for value in sorted(diff_signs)),
            event="stable_window_set",
        )
    return True, pass_note(PROPERTY_IDS, f"checked={checked} diff_signs=-1,1 max_pair_error={max_err:.4f}")

CHECKER_ID = "v4_118_differential_buffer"
CHECKER: Checker = check_v3_differential_buffer
