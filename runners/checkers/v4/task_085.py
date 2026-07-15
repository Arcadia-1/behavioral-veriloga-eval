"""Task-specific checker for canonical v4 DUT 085."""
from __future__ import annotations

from ..api import Checker
def check_comparator_measurement_flow(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "inp", "inn", "outp", "trip_v", "offset_est", "valid"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/inp/inn/outp/trip_v/offset_est/valid"

    threshold = 0.45
    outp = [r["outp"] for r in rows]
    valid = [r["valid"] for r in rows]
    if max(outp) - min(outp) < 0.3:
        return False, f"outp_range={max(outp) - min(outp):.3f}"
    if max(valid) - min(valid) < 0.3:
        return False, f"valid_range={max(valid) - min(valid):.3f}"

    low_window = [r for r in rows if r["inp"] <= r["inn"] + 0.001]
    high_window = [r for r in rows if r["inp"] >= r["inn"] + 0.009]
    if not low_window or not high_window:
        return False, "insufficient_pre_post_trip_windows"

    low_frac = sum(1 for r in low_window if r["outp"] < threshold) / len(low_window)
    high_frac = sum(1 for r in high_window if r["outp"] > threshold) / len(high_window)
    pre_valid_low_frac = sum(1 for r in low_window if r["valid"] < threshold) / len(low_window)
    if low_frac < 0.9 or high_frac < 0.9 or pre_valid_low_frac < 0.9:
        return False, (
            f"output_or_valid_window_fail low_frac={low_frac:.3f} "
            f"high_frac={high_frac:.3f} pre_valid_low_frac={pre_valid_low_frac:.3f}"
        )

    valid_rows = [r for r in rows if r["valid"] > threshold]
    if not valid_rows:
        return False, "valid_never_asserts"

    first_out_high = next((r for r in rows if r["outp"] > threshold), None)
    if first_out_high is None:
        return False, "outp_never_asserts"
    out_trip_diff = first_out_high["inp"] - first_out_high["inn"]
    if abs(out_trip_diff - 0.005) > 0.0015:
        return False, f"outp_first_trip_diff={out_trip_diff:.4f}"

    first_valid = valid_rows[0]
    valid_trip_diff = first_valid["inp"] - first_valid["inn"]
    if abs(valid_trip_diff - 0.005) > 0.0015:
        return False, f"valid_first_trip_diff={valid_trip_diff:.4f}"
    if first_valid["outp"] <= threshold:
        valid_out_settle_s = 100e-12
        settled_after_valid = any(
            r["time"] >= first_valid["time"]
            and r["time"] <= first_valid["time"] + valid_out_settle_s
            and r["outp"] > threshold
            for r in rows
        )
        if not settled_after_valid:
            return False, f"valid_before_output_trip outp={first_valid['outp']:.3f}"

    final_valid_rows = [r for r in valid_rows if r["time"] >= first_valid["time"] + 2e-9]
    if len(final_valid_rows) < 3:
        final_valid_rows = valid_rows[-min(5, len(valid_rows)) :]

    trip_vals = [r["trip_v"] for r in final_valid_rows]
    offset_vals = [r["offset_est"] for r in final_valid_rows]
    trip_avg = sum(trip_vals) / len(trip_vals)
    offset_avg = sum(offset_vals) / len(offset_vals)
    inn_avg = sum(r["inn"] for r in final_valid_rows) / len(final_valid_rows)
    expected_trip = inn_avg + 0.005
    expected_offset = 0.005
    trip_span = max(trip_vals) - min(trip_vals)
    offset_span = max(offset_vals) - min(offset_vals)

    ok = (
        abs(trip_avg - expected_trip) <= 0.0015
        and abs(offset_avg - expected_offset) <= 0.0015
        and trip_span <= 0.002
        and offset_span <= 0.002
    )
    return ok, (
        f"trip_avg={trip_avg:.4f} expected_trip={expected_trip:.4f} "
        f"offset_avg={offset_avg:.4f} low_frac={low_frac:.3f} "
        f"high_frac={high_frac:.3f} out_trip_diff={out_trip_diff:.4f} "
        f"valid_trip_diff={valid_trip_diff:.4f} trip_span={trip_span:.4f} "
        f"offset_span={offset_span:.4f}"
    )

CHECKER_ID = "v4_085_comparator_offset_search"
CHECKER: Checker = check_comparator_measurement_flow
