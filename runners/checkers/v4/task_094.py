"""Task-specific checker for canonical v4 DUT 094."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import crossings, diagnostic, event_label, mean_signal, pass_note, require_signals, sample

PROPERTY_IDS = [
    "P_RESET_COMMON_MODE",
    "P_QUADRATURE_SEQUENCE",
    "P_LO_MONITORS",
    "P_MIXER_MONITORS",
    "P_BASEBAND_UPDATES",
    "P_PHASE_MONITOR",
]


def _median_period(edges: list[float]) -> float:
    periods = [right - left for left, right in zip(edges, edges[1:]) if right > left]
    if not periods:
        return 0.0
    periods.sort()
    return periods[len(periods) // 2]


def _phase_code(value: float | None) -> int | None:
    if value is None:
        return None
    code = int(round(value / 0.3))
    if 0 <= code <= 3:
        return code
    return None


def _near_mid(value: float, center: float = 0.45, tolerance: float = 0.08) -> bool:
    return abs(value - center) <= tolerance

def check_iq_downconversion_chain(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {
        "time",
        "clk",
        "rst",
        "vin",
        "out",
        "metric",
        "lo_i",
        "lo_q",
        "mix_i",
        "mix_q",
        "phase_mon",
    }
    missing = require_signals(rows, required, "P_QUADRATURE_SEQUENCE")
    if missing:
        return False, missing

    times = [row["time"] for row in rows]
    clk_edges = crossings(rows, "clk", threshold=0.45, direction="rising")
    period = _median_period(clk_edges)
    if len(clk_edges) < 8 or period <= 0.0:
        return False, diagnostic(
            "P_QUADRATURE_SEQUENCE",
            "insufficient_events",
            expected="at_least_8_clk_edges",
            observed=f"clk_edges:{len(clk_edges)}",
            event="clk_rising",
        )

    reset_falls = crossings(rows, "rst", threshold=0.45, direction="falling")
    reset_release = reset_falls[0] if reset_falls else times[0]
    vin_values = [row["vin"] for row in rows]
    high_threshold = max(0.55, min(0.65, min(vin_values) + 0.55 * (max(vin_values) - min(vin_values))))
    vin_rises = crossings(rows, "vin", threshold=high_threshold, direction="rising")
    if not vin_rises:
        return False, diagnostic(
            "P_BASEBAND_UPDATES",
            "missing_stimulus_event",
            expected="observable_high_vin_step",
            observed=f"vin_range:{min(vin_values):.3f}-{max(vin_values):.3f}",
            event="vin_rising",
        )
    high_start = vin_rises[0]
    high_edges = [
        edge
        for edge in clk_edges
        if edge > reset_release + 0.25 * period
        and sample(rows, "vin", edge + 0.25 * period) is not None
        and float(sample(rows, "vin", edge + 0.25 * period)) >= high_threshold
    ]
    by_phase: dict[int, dict[str, float]] = {}
    for edge in high_edges:
        probe_t = edge + 0.25 * period
        code = _phase_code(sample(rows, "phase_mon", probe_t))
        if code is None or code in by_phase:
            continue
        values = {"event_time": probe_t}
        for signal in ("out", "metric", "lo_i", "lo_q", "mix_i", "mix_q", "phase_mon"):
            value = sample(rows, signal, probe_t)
            if value is None:
                break
            values[signal] = value
        else:
            by_phase[code] = values
        if len(by_phase) == 4:
            break
    if set(by_phase) != {0, 1, 2, 3}:
        return False, diagnostic(
            "P_PHASE_MONITOR",
            "missing_phase_cycle",
            expected="phases:0,1,2,3",
            observed="phases:" + ",".join(str(code) for code in sorted(by_phase)),
            event=event_label("vin_high", 0, high_start),
        )

    phase_0 = by_phase[0]["phase_mon"]
    phase_1 = by_phase[1]["phase_mon"]
    phase_2 = by_phase[2]["phase_mon"]
    phase_3 = by_phase[3]["phase_mon"]
    i_hi = by_phase[0]["out"]
    q_hi = by_phase[1]["metric"]
    i_lo = by_phase[2]["out"]
    q_lo = by_phase[3]["metric"]
    if i_hi < 0.70 or q_hi < 0.70:
        return False, diagnostic(
            "P_BASEBAND_UPDATES",
            "positive_quadrature_missing",
            expected="i_and_q_high_above_0.70",
            observed=f"i:{i_hi:.3f},q:{q_hi:.3f}",
            event=event_label("vin_high", 0, high_start),
        )
    if i_lo > 0.22 or q_lo > 0.22:
        return False, diagnostic(
            "P_BASEBAND_UPDATES",
            "negative_quadrature_missing",
            expected="i_and_q_low_below_0.22",
            observed=f"i:{i_lo:.3f},q:{q_lo:.3f}",
            event=event_label("vin_high", 0, high_start),
        )
    if not (phase_0 < 0.12 and 0.18 <= phase_1 <= 0.42 and 0.48 <= phase_2 <= 0.72 and phase_3 > 0.78):
        return False, diagnostic(
            "P_PHASE_MONITOR",
            "wrong_phase_sequence",
            expected="phase_monitor:0,1,2,3",
            observed=f"phase:{phase_0:.3f}/{phase_1:.3f}/{phase_2:.3f}/{phase_3:.3f}",
            event=event_label("vin_high", 0, high_start),
        )

    lo_i_hi = by_phase[0]["lo_i"]
    lo_i_mid_pos = by_phase[1]["lo_i"]
    lo_i_lo = by_phase[2]["lo_i"]
    lo_i_mid_neg = by_phase[3]["lo_i"]
    lo_q_mid_pos = by_phase[0]["lo_q"]
    lo_q_hi = by_phase[1]["lo_q"]
    lo_q_mid_neg = by_phase[2]["lo_q"]
    lo_q_lo = by_phase[3]["lo_q"]
    if not (
        lo_i_hi > 0.74
        and _near_mid(lo_i_mid_pos)
        and lo_i_lo < 0.16
        and _near_mid(lo_i_mid_neg)
        and _near_mid(lo_q_mid_pos)
        and lo_q_hi > 0.74
        and _near_mid(lo_q_mid_neg)
        and lo_q_lo < 0.16
    ):
        return False, diagnostic(
            "P_LO_MONITORS",
            "wrong_quadrature_sequence",
            expected="lo_i:high,mid,low,mid;lo_q:mid,high,mid,low",
            observed=(
                f"lo_i:{lo_i_hi:.3f}/{lo_i_mid_pos:.3f}/{lo_i_lo:.3f}/{lo_i_mid_neg:.3f};"
                f"lo_q:{lo_q_mid_pos:.3f}/{lo_q_hi:.3f}/{lo_q_mid_neg:.3f}/{lo_q_lo:.3f}"
            ),
            event=event_label("vin_high", 0, high_start),
        )

    mix_i_hi = by_phase[0]["mix_i"]
    mix_i_neutral_pos = by_phase[1]["mix_i"]
    mix_i_lo = by_phase[2]["mix_i"]
    mix_i_neutral_neg = by_phase[3]["mix_i"]
    mix_q_neutral_pos = by_phase[0]["mix_q"]
    mix_q_hi = by_phase[1]["mix_q"]
    mix_q_neutral_neg = by_phase[2]["mix_q"]
    mix_q_lo = by_phase[3]["mix_q"]
    if not (
        mix_i_hi > 0.68
        and _near_mid(mix_i_neutral_pos)
        and mix_i_lo < 0.24
        and _near_mid(mix_i_neutral_neg)
        and _near_mid(mix_q_neutral_pos)
        and mix_q_hi > 0.68
        and _near_mid(mix_q_neutral_neg)
        and mix_q_lo < 0.24
    ):
        return False, diagnostic(
            "P_MIXER_MONITORS",
            "wrong_mixer_outputs",
            expected="mix_i:high,mid,low,mid;mix_q:mid,high,mid,low",
            observed=(
                f"mix_i:{mix_i_hi:.3f}/{mix_i_neutral_pos:.3f}/{mix_i_lo:.3f}/{mix_i_neutral_neg:.3f};"
                f"mix_q:{mix_q_neutral_pos:.3f}/{mix_q_hi:.3f}/{mix_q_neutral_neg:.3f}/{mix_q_lo:.3f}"
            ),
            event=event_label("vin_high", 0, high_start),
        )

    vin_falls = [event for event in crossings(rows, "vin", threshold=high_threshold, direction="falling") if event > high_start]
    if not vin_falls:
        return False, diagnostic(
            "P_RESET_COMMON_MODE",
            "missing_stimulus_event",
            expected="observable_neutral_vin_return",
            observed="vin_falling:none",
            event=event_label("vin_high", 0, high_start),
        )
    neutral_start = vin_falls[0] + 2.0 * period
    neutral_rows = [
        row
        for row in rows
        if row["time"] >= neutral_start and 0.38 <= row["vin"] <= 0.52
    ]
    if len(neutral_rows) < 4:
        return False, diagnostic(
            "P_RESET_COMMON_MODE",
            "missing_neutral_samples",
            expected="at_least_4_neutral_vin_samples",
            observed=f"samples:{len(neutral_rows)}",
            event=event_label("vin_falling", 0, vin_falls[0]),
        )
    i_cm = mean_signal(neutral_rows, "out")
    q_cm = mean_signal(neutral_rows, "metric")
    mix_i_cm = mean_signal(neutral_rows, "mix_i")
    mix_q_cm = mean_signal(neutral_rows, "mix_q")
    assert i_cm is not None and q_cm is not None and mix_i_cm is not None and mix_q_cm is not None
    if abs(i_cm - 0.45) > 0.08 or abs(q_cm - 0.45) > 0.08:
        return False, diagnostic(
            "P_RESET_COMMON_MODE",
            "common_mode_hold_wrong",
            expected="baseband_common_mode_near_0.45",
            observed=f"i:{i_cm:.3f},q:{q_cm:.3f}",
            event=event_label("vin_falling", 0, vin_falls[0]),
        )
    if abs(mix_i_cm - 0.45) > 0.06 or abs(mix_q_cm - 0.45) > 0.06:
        return False, diagnostic(
            "P_MIXER_MONITORS",
            "mixer_common_mode_wrong",
            expected="mixer_common_mode_near_0.45",
            observed=f"i:{mix_i_cm:.3f},q:{mix_q_cm:.3f}",
            event=event_label("vin_falling", 0, vin_falls[0]),
        )

    low_tail_rows = [row for row in rows if row["time"] > vin_falls[0] and row.get("vin", 0.45) < 0.38]
    low_tail_detail = ""
    if len(low_tail_rows) >= 4:
        mix_i_values = [row["mix_i"] for row in low_tail_rows if "mix_i" in row]
        mix_q_values = [row["mix_q"] for row in low_tail_rows if "mix_q" in row]
        out_values = [row["out"] for row in low_tail_rows if "out" in row]
        metric_values = [row["metric"] for row in low_tail_rows if "metric" in row]
        if min(len(mix_i_values), len(mix_q_values), len(out_values), len(metric_values)) < 4:
            return False, diagnostic(
                "P_BASEBAND_UPDATES",
                "low_tail_missing_outputs",
                expected="mix_and_baseband_low_tail_samples",
                observed="incomplete_low_tail_outputs",
                event=event_label("vin_low", 0, low_tail_rows[0]["time"]),
            )
        mix_span = max(max(mix_i_values) - min(mix_i_values), max(mix_q_values) - min(mix_q_values))
        baseband_span = max(max(out_values) - min(out_values), max(metric_values) - min(metric_values))
        if mix_span < 0.16 or baseband_span < 0.08:
            return False, diagnostic(
                "P_BASEBAND_UPDATES",
                "low_tail_not_exercised",
                expected="observable_low_tail_response",
                observed=f"mix_span:{mix_span:.3f},baseband_span:{baseband_span:.3f}",
                event=event_label("vin_low", 0, low_tail_rows[0]["time"]),
            )
        low_tail_detail = f" low_tail_mix_span={mix_span:.3f} low_tail_baseband_span={baseband_span:.3f}"
    return True, pass_note(
        PROPERTY_IDS,
        "iq_downconversion_chain "
        f"i_hi/q_hi/i_lo/q_lo={i_hi:.3f}/{q_hi:.3f}/{i_lo:.3f}/{q_lo:.3f} "
        f"common_mode={i_cm:.3f}/{q_cm:.3f} "
        f"phase={phase_0:.3f}/{phase_1:.3f}/{phase_2:.3f}/{phase_3:.3f}"
        f"{low_tail_detail}",
    )

CHECKER_ID = "v4_094_iq_downconversion_chain"
CHECKER: Checker = check_iq_downconversion_chain
