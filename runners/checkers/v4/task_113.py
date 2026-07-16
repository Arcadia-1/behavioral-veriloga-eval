"""Task-specific checker for canonical v4 DUT 113."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import crossings, diagnostic, max_signal_value, pass_note, probe_time, require_signals, sample


PROPERTY_IDS = (
    "P_THRESHOLD_DECODE",
    "P_WEIGHT_ORDER",
    "P_BIPOLAR_ENDPOINTS",
    "P_MONOTONIC_CODE_WEIGHT",
    "P_CONTINUOUS_DECODE",
)


def check_v3_sar_weighted_sum(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "d10", "d9", "d8", "d7", "d6", "d5", "d4", "d3", "d2", "d1", "d0", "vout"}
    missing = require_signals(rows, required, "P_THRESHOLD_DECODE")
    if missing:
        return False, missing

    bit_signals = ["d10", "d9", "d8", "d7", "d6", "d5", "d4", "d3", "d2", "d1", "d0"]
    weights = [448, 256, 128, 80, 48, 32, 16, 8, 4, 2, 1]
    vth = 0.5 * max_signal_value(rows, bit_signals, default=0.9)
    change_times: list[float] = []
    for signal in bit_signals:
        change_times.extend(crossings(rows, signal, threshold=vth, direction="rising"))
        change_times.extend(crossings(rows, signal, threshold=vth, direction="falling"))
    change_times = sorted(set(round(t, 15) for t in change_times))
    candidates = [rows[0]["time"]]
    for index, change in enumerate(change_times):
        next_change = change_times[index + 1] if index + 1 < len(change_times) else None
        probe = probe_time(rows, change, next_change, fraction=0.25)
        if probe is not None:
            candidates.append(probe)

    checked = 0
    distinct_codes: set[int] = set()
    max_err = 0.0
    for index, t in enumerate(candidates):
        code_weight = 0
        code_bits = 0
        for idx, signal in enumerate(bit_signals):
            value = sample(rows, signal, t)
            if value is None:
                break
            if value > vth:
                code_weight += weights[idx]
                code_bits |= 1 << (len(bit_signals) - 1 - idx)
        else:
            observed = sample(rows, "vout", t)
            if observed is None:
                continue
            expected = code_weight / 512.0 - 1.0
            err = abs(observed - expected)
            max_err = max(max_err, err)
            distinct_codes.add(code_bits)
            checked += 1
            if err > 0.025:
                return False, diagnostic(
                    "P_WEIGHT_ORDER",
                    "weighted_sum_mismatch",
                    expected=f"code=0x{code_bits:03x},vout={expected:.4f}",
                    observed=f"vout={observed:.4f},err={err:.4f}",
                    event=f"code_state[{index}]",
                )
    if checked < 4:
        return False, diagnostic(
            "P_CONTINUOUS_DECODE",
            "insufficient_checks",
            expected="checked>=4",
            observed=f"checked={checked}",
            event="code_state_set",
        )
    if len(distinct_codes) < 4:
        return False, diagnostic(
            "P_BIPOLAR_ENDPOINTS",
            "insufficient_code_coverage",
            expected="distinct_codes>=4",
            observed=f"distinct_codes={len(distinct_codes)}",
            event="code_state_set",
        )
    detail = f"checked={checked} distinct_codes={len(distinct_codes)} max_err={max_err:.5f}"
    return True, pass_note(PROPERTY_IDS, detail)

CHECKER_ID = "v4_113_sar_weighted_sum"
CHECKER: Checker = check_v3_sar_weighted_sum
