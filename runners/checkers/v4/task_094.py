"""Task-specific checker for canonical v4 DUT 094."""
from __future__ import annotations

from ..api import Checker
def mean_in_window(rows: list[dict[str, float]], key: str, start: float, stop: float) -> float | None:
    values = [r[key] for r in rows if start <= r["time"] <= stop and key in r]
    if not values:
        return None
    return sum(values) / len(values)

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
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, f"missing_columns={','.join(missing)}"

    i_hi = mean_in_window(rows, "out", 12.2e-9, 13.5e-9)
    q_hi = mean_in_window(rows, "metric", 14.2e-9, 15.5e-9)
    i_lo = mean_in_window(rows, "out", 16.2e-9, 17.5e-9)
    q_lo = mean_in_window(rows, "metric", 18.2e-9, 19.5e-9)
    i_cm = mean_in_window(rows, "out", 58.0e-9, 64.0e-9)
    q_cm = mean_in_window(rows, "metric", 58.0e-9, 64.0e-9)
    lo_i_hi = mean_in_window(rows, "lo_i", 12.2e-9, 13.5e-9)
    lo_i_mid_pos = mean_in_window(rows, "lo_i", 14.2e-9, 15.5e-9)
    lo_i_lo = mean_in_window(rows, "lo_i", 16.2e-9, 17.5e-9)
    lo_i_mid_neg = mean_in_window(rows, "lo_i", 18.2e-9, 19.5e-9)
    lo_q_mid_pos = mean_in_window(rows, "lo_q", 12.2e-9, 13.5e-9)
    lo_q_hi = mean_in_window(rows, "lo_q", 14.2e-9, 15.5e-9)
    lo_q_mid_neg = mean_in_window(rows, "lo_q", 16.2e-9, 17.5e-9)
    lo_q_lo = mean_in_window(rows, "lo_q", 18.2e-9, 19.5e-9)
    mix_i_hi = mean_in_window(rows, "mix_i", 12.2e-9, 13.5e-9)
    mix_i_neutral_pos = mean_in_window(rows, "mix_i", 14.2e-9, 15.5e-9)
    mix_i_lo = mean_in_window(rows, "mix_i", 16.2e-9, 17.5e-9)
    mix_i_neutral_neg = mean_in_window(rows, "mix_i", 18.2e-9, 19.5e-9)
    mix_q_neutral_pos = mean_in_window(rows, "mix_q", 12.2e-9, 13.5e-9)
    mix_q_hi = mean_in_window(rows, "mix_q", 14.2e-9, 15.5e-9)
    mix_q_neutral_neg = mean_in_window(rows, "mix_q", 16.2e-9, 17.5e-9)
    mix_q_lo = mean_in_window(rows, "mix_q", 18.2e-9, 19.5e-9)
    phase_0 = mean_in_window(rows, "phase_mon", 12.2e-9, 13.5e-9)
    phase_1 = mean_in_window(rows, "phase_mon", 14.2e-9, 15.5e-9)
    phase_2 = mean_in_window(rows, "phase_mon", 16.2e-9, 17.5e-9)
    phase_3 = mean_in_window(rows, "phase_mon", 18.2e-9, 19.5e-9)
    mix_i_cm = mean_in_window(rows, "mix_i", 58.0e-9, 64.0e-9)
    mix_q_cm = mean_in_window(rows, "mix_q", 58.0e-9, 64.0e-9)
    if None in (
        i_hi,
        q_hi,
        i_lo,
        q_lo,
        i_cm,
        q_cm,
        lo_i_hi,
        lo_i_mid_pos,
        lo_i_lo,
        lo_i_mid_neg,
        lo_q_mid_pos,
        lo_q_hi,
        lo_q_mid_neg,
        lo_q_lo,
        mix_i_hi,
        mix_i_neutral_pos,
        mix_i_lo,
        mix_i_neutral_neg,
        mix_q_neutral_pos,
        mix_q_hi,
        mix_q_neutral_neg,
        mix_q_lo,
        phase_0,
        phase_1,
        phase_2,
        phase_3,
        mix_i_cm,
        mix_q_cm,
    ):
        return False, "iq_missing_sample_windows"
    assert i_hi is not None
    assert q_hi is not None
    assert i_lo is not None
    assert q_lo is not None
    assert i_cm is not None
    assert q_cm is not None
    assert lo_i_hi is not None
    assert lo_i_mid_pos is not None
    assert lo_i_lo is not None
    assert lo_i_mid_neg is not None
    assert lo_q_mid_pos is not None
    assert lo_q_hi is not None
    assert lo_q_mid_neg is not None
    assert lo_q_lo is not None
    assert mix_i_hi is not None
    assert mix_i_neutral_pos is not None
    assert mix_i_lo is not None
    assert mix_i_neutral_neg is not None
    assert mix_q_neutral_pos is not None
    assert mix_q_hi is not None
    assert mix_q_neutral_neg is not None
    assert mix_q_lo is not None
    assert phase_0 is not None
    assert phase_1 is not None
    assert phase_2 is not None
    assert phase_3 is not None
    assert mix_i_cm is not None
    assert mix_q_cm is not None

    if i_hi < 0.70 or q_hi < 0.70:
        return False, f"iq_positive_quadrature_missing i={i_hi:.3f} q={q_hi:.3f}"
    if i_lo > 0.22 or q_lo > 0.22:
        return False, f"iq_negative_quadrature_missing i={i_lo:.3f} q={q_lo:.3f}"
    if abs(i_cm - 0.45) > 0.08 or abs(q_cm - 0.45) > 0.08:
        return False, f"iq_common_mode_hold_wrong i={i_cm:.3f} q={q_cm:.3f}"
    if not (phase_0 < 0.12 and 0.18 <= phase_1 <= 0.42 and 0.48 <= phase_2 <= 0.72 and phase_3 > 0.78):
        return False, (
            "iq_phase_monitor_sequence_wrong "
            f"phase={phase_0:.3f}/{phase_1:.3f}/{phase_2:.3f}/{phase_3:.3f}"
        )
    if not (
        lo_i_hi > 0.74
        and 0.32 <= lo_i_mid_pos <= 0.58
        and lo_i_lo < 0.16
        and 0.32 <= lo_i_mid_neg <= 0.58
        and 0.32 <= lo_q_mid_pos <= 0.58
        and lo_q_hi > 0.74
        and 0.32 <= lo_q_mid_neg <= 0.58
        and lo_q_lo < 0.16
    ):
        return False, (
            "iq_lo_quadrature_sequence_wrong "
            f"lo_i={lo_i_hi:.3f}/{lo_i_mid_pos:.3f}/{lo_i_lo:.3f}/{lo_i_mid_neg:.3f} "
            f"lo_q={lo_q_mid_pos:.3f}/{lo_q_hi:.3f}/{lo_q_mid_neg:.3f}/{lo_q_lo:.3f}"
        )
    if not (
        mix_i_hi > 0.68
        and abs(mix_i_neutral_pos - 0.45) <= 0.08
        and mix_i_lo < 0.24
        and abs(mix_i_neutral_neg - 0.45) <= 0.08
        and abs(mix_q_neutral_pos - 0.45) <= 0.08
        and mix_q_hi > 0.68
        and abs(mix_q_neutral_neg - 0.45) <= 0.08
        and mix_q_lo < 0.24
    ):
        return False, (
            "iq_mixer_outputs_wrong "
            f"mix_i={mix_i_hi:.3f}/{mix_i_neutral_pos:.3f}/{mix_i_lo:.3f}/{mix_i_neutral_neg:.3f} "
            f"mix_q={mix_q_neutral_pos:.3f}/{mix_q_hi:.3f}/{mix_q_neutral_neg:.3f}/{mix_q_lo:.3f}"
        )
    if abs(mix_i_cm - 0.45) > 0.06 or abs(mix_q_cm - 0.45) > 0.06:
        return False, f"iq_mixer_common_mode_wrong i={mix_i_cm:.3f} q={mix_q_cm:.3f}"
    low_tail_rows = [
        row
        for row in rows
        if row["time"] >= 66.0e-9 and row.get("vin", 0.45) < 0.38
    ]
    low_tail_detail = ""
    if len(low_tail_rows) >= 4:
        mix_i_values = [row["mix_i"] for row in low_tail_rows if "mix_i" in row]
        mix_q_values = [row["mix_q"] for row in low_tail_rows if "mix_q" in row]
        out_values = [row["out"] for row in low_tail_rows if "out" in row]
        metric_values = [row["metric"] for row in low_tail_rows if "metric" in row]
        if min(len(mix_i_values), len(mix_q_values), len(out_values), len(metric_values)) < 4:
            return False, "iq_low_tail_missing_outputs"
        mix_span = max(max(mix_i_values) - min(mix_i_values), max(mix_q_values) - min(mix_q_values))
        baseband_span = max(max(out_values) - min(out_values), max(metric_values) - min(metric_values))
        if mix_span < 0.16 or baseband_span < 0.08:
            return False, (
                f"iq_low_tail_not_exercised mix_span={mix_span:.3f} "
                f"baseband_span={baseband_span:.3f}"
            )
        low_tail_detail = f" low_tail_mix_span={mix_span:.3f} low_tail_baseband_span={baseband_span:.3f}"
    return True, (
        "iq_downconversion_chain "
        f"i_hi/q_hi/i_lo/q_lo={i_hi:.3f}/{q_hi:.3f}/{i_lo:.3f}/{q_lo:.3f} "
        f"common_mode={i_cm:.3f}/{q_cm:.3f} "
        f"phase={phase_0:.3f}/{phase_1:.3f}/{phase_2:.3f}/{phase_3:.3f}"
        f"{low_tail_detail}"
    )

CHECKER_ID = "v4_094_iq_downconversion_chain"
CHECKER: Checker = check_iq_downconversion_chain
