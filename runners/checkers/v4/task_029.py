"""Task-specific checker for canonical v4 DUT 029."""
from __future__ import annotations

from ..api import Checker
def check_cmp_hysteresis(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "out_p", "out_n"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/out_p/out_n"

    threshold = 0.45
    times_ns = [r["time"] * 1e9 for r in rows]
    out_p = [r["out_p"] for r in rows]
    out_n = [r["out_n"] for r in rows]

    threshold_crossings: list[float] = []
    if {"vinp", "vinn"}.issubset(rows[0]):
        diffs = [row["vinp"] - row["vinn"] for row in rows]
        for idx in range(1, len(rows)):
            previous = diffs[idx - 1]
            current = diffs[idx]
            target = None
            if previous < 0.005 <= current:
                target = 0.005
            elif previous > -0.005 >= current:
                target = -0.005
            if target is None or current == previous:
                continue
            fraction = (target - previous) / (current - previous)
            crossing_time = rows[idx - 1]["time"] + fraction * (
                rows[idx]["time"] - rows[idx - 1]["time"]
            )
            threshold_crossings.append(crossing_time)

    if max(out_p) - min(out_p) < threshold or max(out_n) - min(out_n) < threshold:
        return False, (
            "outputs_do_not_toggle "
            f"observed=out_p_span:{max(out_p) - min(out_p):.3f},out_n_span:{max(out_n) - min(out_n):.3f} "
            "expected=>0.45 window=full_trace"
        )

    rail_checks = 0
    guarded_transition_samples = 0
    rail_errors: list[str] = []
    if {"vdd", "vss"}.issubset(rows[0]):
        for row in rows[:: max(1, len(rows) // 160)]:
            if row["time"] < 0.5e-9:
                continue
            if any(abs(row["time"] - crossing) <= 0.5e-9 for crossing in threshold_crossings):
                guarded_transition_samples += 1
                continue
            vdd = row["vdd"]
            vss = row["vss"]
            mid = 0.5 * (vdd + vss)
            outp_hi = row["out_p"] > mid
            outn_hi = row["out_n"] > mid
            if outp_hi == outn_hi:
                rail_errors.append(
                    f"observed=out_p:{row['out_p']:.3f},out_n:{row['out_n']:.3f} "
                    f"expected=complementary_rails:{vss:.3f}/{vdd:.3f} window={row['time'] * 1e9:.3f}ns"
                )
            elif outp_hi and (abs(row["out_p"] - vdd) > 0.10 or abs(row["out_n"] - vss) > 0.10):
                rail_errors.append(
                    f"observed=out_p:{row['out_p']:.3f},out_n:{row['out_n']:.3f} "
                    f"expected=out_p:{vdd:.3f},out_n:{vss:.3f} window={row['time'] * 1e9:.3f}ns"
                )
            elif outn_hi and (abs(row["out_n"] - vdd) > 0.10 or abs(row["out_p"] - vss) > 0.10):
                rail_errors.append(
                    f"observed=out_p:{row['out_p']:.3f},out_n:{row['out_n']:.3f} "
                    f"expected=out_p:{vss:.3f},out_n:{vdd:.3f} window={row['time'] * 1e9:.3f}ns"
                )
            rail_checks += 1
        if rail_checks < 12:
            return False, f"insufficient_rail_checks observed={rail_checks} expected>=12 window=full_trace"
        if rail_errors:
            return False, "rail_or_complement_error " + " ".join(rail_errors[:3])

    pre = [out_p[idx] for idx, t in enumerate(times_ns) if t < 20.0]
    mid = [out_p[idx] for idx, t in enumerate(times_ns) if 35.0 < t < 60.0]
    post = [out_p[idx] for idx, t in enumerate(times_ns) if t > 75.0]
    if not pre or not mid or not post:
        return False, "insufficient_hysteresis_windows"

    pre_low_frac = sum(1 for v in pre if v < threshold) / len(pre)
    mid_high_frac = sum(1 for v in mid if v > threshold) / len(mid)
    post_low_frac = sum(1 for v in post if v < threshold) / len(post)
    if pre_low_frac < 0.95 or mid_high_frac < 0.95 or post_low_frac < 0.95:
        return False, (
            f"window_fracs observed=pre:{pre_low_frac:.3f},mid:{mid_high_frac:.3f},post:{post_low_frac:.3f} "
            "expected=>=0.95 window=pre/mid/post"
        )

    rise_t = None
    fall_t = None
    for idx in range(1, len(out_p)):
        if rise_t is None and out_p[idx - 1] < threshold <= out_p[idx]:
            rise_t = times_ns[idx]
        if fall_t is None and out_p[idx - 1] > threshold >= out_p[idx]:
            fall_t = times_ns[idx]

    if rise_t is None or fall_t is None:
        return False, "missing_trip_crossings"
    if not (29.0 <= rise_t <= 31.5):
        return False, f"rise_t_out_of_range observed={rise_t:.3f}ns expected=29.0..31.5ns window=positive_crossing"
    if not (68.5 <= fall_t <= 71.5):
        return False, f"fall_t_out_of_range observed={fall_t:.3f}ns expected=68.5..71.5ns window=negative_crossing"
    return True, (
        f"rise_t={rise_t:.3f}ns fall_t={fall_t:.3f}ns rail_checks={rail_checks} "
        f"guarded_transition_samples={guarded_transition_samples}"
    )

CHECKER_ID = "v4_029_hysteresis_comparator"
CHECKER: Checker = check_cmp_hysteresis
