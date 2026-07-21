"""Task-specific checker for canonical v4 DUT 202."""
from __future__ import annotations

from ..api import Checker


def sample_signal_at(rows: list[dict[str, float]], signal: str, time_s: float) -> float | None:
    if not rows or "time" not in rows[0] or signal not in rows[0]:
        return None
    first_time = rows[0]["time"]
    last_time = rows[-1].get("time")
    if last_time is None or time_s < first_time or time_s > last_time:
        return None
    if time_s == first_time:
        return rows[0].get(signal)
    for idx in range(1, len(rows)):
        prev = rows[idx - 1]
        cur = rows[idx]
        t0 = prev.get("time")
        t1 = cur.get("time")
        if t0 is None or t1 is None:
            continue
        if t0 <= time_s <= t1:
            v0 = prev.get(signal)
            v1 = cur.get(signal)
            if v0 is None or v1 is None:
                return None
            if t1 == t0:
                return v1
            alpha = (time_s - t0) / (t1 - t0)
            return v0 + alpha * (v1 - v0)
    return None

WINDOWS_NS: dict[str, tuple[tuple[float, float], ...]] = {
    "rst": ((0.5, 0.8),),
    "s": ((1.5, 2.5),),
    "sar": ((3.0, 5.4),),
    "clk_sar": ((3.0, 3.25), (3.6, 3.85), (4.2, 4.45)),
    "res": ((6.0, 6.6),),
    "intg": ((8.0, 8.7),),
    "zoom": ((9.2, 10.8),),
    "clk_zoom": ((9.2, 9.45), (9.8, 10.05)),
    "rst_zoom": ((11.0, 11.5),),
}


def _threshold_edges(rows: list[dict[str, float]], signal: str) -> list[float]:
    edges: list[float] = []
    for previous, current in zip(rows, rows[1:]):
        v0 = previous[signal]
        v1 = current[signal]
        rising = v0 < 0.55 <= v1
        falling = v0 > 0.55 >= v1
        if not rising and not falling:
            continue
        t0 = previous["time"]
        t1 = current["time"]
        if v1 == v0:
            edges.append(t1)
        else:
            edges.append(t0 + (0.55 - v0) * (t1 - t0) / (v1 - v0))
    return edges


def _inside_window(time_ns: float, windows: tuple[tuple[float, float], ...]) -> bool:
    phase_ns = time_ns % 32.0
    return any(start <= phase_ns <= stop for start, stop in windows)


def _away_from_edges(time_ns: float, windows: tuple[tuple[float, float], ...]) -> bool:
    phase_ns = time_ns % 32.0
    return all(abs(phase_ns - edge) >= 0.06 for window in windows for edge in window)

def check_v3_adc_zoom_timing_sequencer(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "rst", "s", "sar", "res", "intg", "clk_sar", "zoom", "clk_zoom", "rst_zoom"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing adc zoom timing sequencer signals"
    if rows[-1]["time"] < 44.0e-9:
        return False, f"trace_too_short_for_second_frame={rows[-1]['time'] * 1e9:.3f}ns"

    checked = 0
    max_level_error = 0.0
    for signal, windows in WINDOWS_NS.items():
        for frame in (0.0, 32.0):
            expected_edges = [frame + edge for window in windows for edge in window]
            actual_edges = [edge * 1e9 for edge in _threshold_edges(rows, signal)]
            frame_edges = [edge for edge in actual_edges if frame <= edge < frame + 16.0]
            if len(frame_edges) != len(expected_edges):
                return False, (
                    f"{signal}_edge_count_frame={int(frame / 32)} "
                    f"observed={len(frame_edges)} expected={len(expected_edges)}"
                )
            for observed, expected in zip(frame_edges, expected_edges):
                if abs(observed - expected) > 0.055:
                    return False, (
                        f"{signal}_edge_time={observed:.4f}ns expected={expected:.4f}ns"
                    )

        for step in range(0, 441):
            time_ns = step * 0.1
            if not _away_from_edges(time_ns, windows):
                continue
            observed = sample_signal_at(rows, signal, time_ns * 1e-9)
            if observed is None:
                return False, f"missing_{signal}_sample_at={time_ns:.3f}ns"
            expected = 1.1 if _inside_window(time_ns, windows) else 0.0
            error = abs(observed - expected)
            max_level_error = max(max_level_error, error)
            checked += 1
            if error > 0.09:
                return False, (
                    f"{signal}@{time_ns:.3f}ns={observed:.4f} "
                    f"expected={expected:.4f}"
                )
    return True, f"frames=2 samples={checked} max_level_error={max_level_error:.4f}"

CHECKER_ID = "v4_202_adc_zoom_timing_sequencer"
CHECKER: Checker = check_v3_adc_zoom_timing_sequencer
