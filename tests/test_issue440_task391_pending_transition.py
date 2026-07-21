from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runners.checkers.v4.task_391 import check_v4_391_lc_vco_behavioral_source


VDD = 0.9
VCM = 0.45
AMP = 0.4


def _ctrl_at(time_s: float) -> float:
    if time_s < 250e-9:
        return -0.1
    if time_s < 600e-9:
        return 0.45
    return 1.0


def _half_period(ctrl: float) -> float:
    clamped = max(0.0, min(VDD, ctrl))
    return 0.5 / (5e6 + 20e6 * clamped / VDD)


def _active_segment(time_s: float) -> tuple[float, float] | None:
    if 10.1e-9 <= time_s < 820.1e-9:
        return (10.1e-9, 820.1e-9)
    if 870.1e-9 <= time_s <= 1050e-9:
        return (870.1e-9, 1050e-9)
    return None


def _edge_schedule(*, retime_pending_edge: bool) -> list[float]:
    edges = [110.1e-9, 210.1e-9]
    next_edge = 250.1e-9 + _half_period(0.45) if retime_pending_edge else 310.1e-9
    while next_edge < 820.1e-9:
        edges.append(next_edge)
        next_edge += _half_period(_ctrl_at(next_edge + 1e-15))

    next_edge = 870.1e-9 + _half_period(1.0)
    while next_edge < 1050e-9:
        edges.append(next_edge)
        next_edge += _half_period(1.0)
    return sorted(edges)


def _state_at(time_s: float, edges: list[float]) -> tuple[float, float, float, float, float]:
    segment = _active_segment(time_s)
    if segment is None:
        return VCM, VCM, 0.0, 0.0, 0.0

    start, end = segment
    half_edges = sum(1 for edge in edges if start < edge <= time_s and edge < end)
    if half_edges == 0:
        return VCM, VCM, max(0.0, min(VDD, _ctrl_at(time_s))), AMP, 0.0

    osc_p_high = half_edges % 2 == 1
    osc_p = VCM + AMP if osc_p_high else VCM - AMP
    osc_n = VCM - AMP if osc_p_high else VCM + AMP
    valid = VDD if half_edges >= 4 else 0.0
    return osc_p, osc_n, max(0.0, min(VDD, _ctrl_at(time_s))), AMP, valid


def _rows(*, retime_pending_edge: bool) -> list[dict[str, float]]:
    edges = _edge_schedule(retime_pending_edge=retime_pending_edge)
    times = {index * 1e-9 for index in range(1051)}
    for event_time in edges + [4.1e-9, 10.1e-9, 250.1e-9, 600.1e-9, 820.1e-9, 870.1e-9]:
        for offset in (-1e-12, 0.0, 1e-12, 0.8e-9):
            sample_time = event_time + offset
            if 0.0 <= sample_time <= 1050e-9:
                times.add(sample_time)

    rows: list[dict[str, float]] = []
    for time_s in sorted(times):
        osc_p, osc_n, freq_metric, amp_metric, valid = _state_at(time_s, edges)
        rows.append(
            {
                "time": time_s,
                "vctrl": _ctrl_at(time_s),
                "enable": VDD if _active_segment(time_s) else 0.0,
                "rst": VDD if time_s < 4.1e-9 else 0.0,
                "osc_p": osc_p,
                "osc_n": osc_n,
                "freq_metric": freq_metric,
                "amp_metric": amp_metric,
                "valid": valid,
            }
        )
    return rows


def test_task391_accepts_pending_transition_preserving_trace() -> None:
    ok, note = check_v4_391_lc_vco_behavioral_source(_rows(retime_pending_edge=False))
    assert ok, note
    assert "P_NO_RETIME_PENDING_TRANSITION:mismatch_count=0" in note


def test_task391_rejects_control_change_retiming_pending_transition() -> None:
    ok, note = check_v4_391_lc_vco_behavioral_source(_rows(retime_pending_edge=True))
    assert not ok
    assert "P_NO_RETIME_PENDING_TRANSITION:mismatch_count=" in note
