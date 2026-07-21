"""Task-specific checker for canonical v4 DUT 059."""
from __future__ import annotations

import math

from ..api import Checker
from .stimulus_relative import diagnostic, pass_note


PROPERTY_IDS = (
    "P_START_ARMS",
    "P_NEXT_STOP_COMPLETES",
    "P_INTERVAL_QUANTIZATION",
    "P_CODE_SATURATION",
    "P_VALID_AND_BIT_ORDER",
)


def _logic_bits_to_int(row: dict[str, float], prefix: str, width: int, vth: float = 0.45) -> int:
    return sum((1 << bit) for bit in range(width) if row[f"{prefix}{bit}"] > vth)

def _rising_times(rows: list[dict[str, float]], col: str, vth: float = 0.45) -> list[float]:
    times: list[float] = []
    last = rows[0][col] > vth
    for row in rows[1:]:
        cur = row[col] > vth
        if not last and cur:
            times.append(row["time"])
        last = cur
    return times

def _sample_after(rows: list[dict[str, float]], t: float, delay: float = 5e-9) -> dict[str, float]:
    target = t + delay
    return min(rows, key=lambda row: abs(row["time"] - target))


def _measurement_pairs(starts: list[float], stops: list[float]) -> list[tuple[float, float]]:
    armed_at: float | None = None
    pairs: list[tuple[float, float]] = []
    events = sorted([(time_s, "start") for time_s in starts] + [(time_s, "stop") for time_s in stops])
    for time_s, kind in events:
        if kind == "start":
            armed_at = time_s
        elif armed_at is not None:
            pairs.append((armed_at, time_s))
            armed_at = None
    return pairs

def check_edge_interval_tdc_8b(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "start", "stop", "valid", *{f"code{i}" for i in range(8)}}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing[:12])
    starts = _rising_times(rows, "start")
    stops = _rising_times(rows, "stop")
    time_scale = float(rows[0].get("_time_scale", 1.0))
    pairs = _measurement_pairs(starts, stops)
    if len(pairs) < 3:
        note = diagnostic(
            "P_NEXT_STOP_COMPLETES",
            "insufficient_excitation",
            expected="completed_measurements>=3",
            observed=f"completed_measurements={len(pairs)}",
            event="start_then_next_stop",
        )
        return False, f"{note} properties_checked={','.join(PROPERTY_IDS)}"

    mismatches: list[tuple[float, int, int, bool]] = []
    checked: list[int] = []
    for start_t, stop_t in pairs:
        expected = max(
            0,
            min(255, math.floor((stop_t - start_t) / (time_scale * 1e-9) + 0.5)),
        )
        row = _sample_after(rows, stop_t, time_scale * 0.20e-9)
        actual = _logic_bits_to_int(row, "code", 8)
        valid = row["valid"] > 0.45
        if not valid or actual != expected:
            mismatches.append((stop_t, expected, actual, valid))
        checked.append(expected)
    if len(set(checked)) < 3:
        note = diagnostic(
            "P_INTERVAL_QUANTIZATION",
            "insufficient_excitation",
            expected="distinct_interval_codes>=3",
            observed=f"distinct_interval_codes={len(set(checked))}",
            event="completed_measurements",
        )
        return False, f"{note} properties_checked={','.join(PROPERTY_IDS)}"
    if mismatches:
        stop_t, expected, actual, valid = mismatches[0]
        property_id = "P_NEXT_STOP_COMPLETES" if not valid else "P_INTERVAL_QUANTIZATION"
        note = diagnostic(
            property_id,
            "behavior_mismatch",
            expected=f"valid=1,code={expected}",
            observed=f"valid={int(valid)},code={actual}",
            event=f"stop.rising@{stop_t:.6e}s",
        )
        return False, f"{note} properties_checked={','.join(PROPERTY_IDS)}"
    note = pass_note(PROPERTY_IDS, f"checked={checked} measurement_pairs={len(pairs)}")
    return True, note

CHECKER_ID = "v4_059_edge_interval_tdc_8b"
CHECKER: Checker = check_edge_interval_tdc_8b
