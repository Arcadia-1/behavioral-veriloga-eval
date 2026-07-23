"""Task-specific checker for canonical v4 DUT 303."""
from __future__ import annotations

from ..api import Checker
from ..common.v4_topup import (
    _v4_topup_clip01,
    _v4_topup_near,
)
from .trace_utils import sample_signal


_TICK = 500e-12
_PROBE_OFFSETS = (300e-12, 450e-12)


def _timer_events(rows: list[dict[str, float]]) -> list[tuple[float, tuple[float, ...]]]:
    start = float(rows[0]["time"])
    stop = float(rows[-1]["time"])
    if stop <= start:
        return []

    # The DUT owns its timer cadence through the Verilog-A ``tick`` parameter.
    # Stimulus affine transforms stretch the deck sources and stop time, but
    # they do not rewrite this parameter, so checker probes must stay on the
    # physical 500 ps timer grid.
    tick = _TICK
    offsets = _PROBE_OFFSETS
    events: list[tuple[float, tuple[float, ...]]] = []
    index = 0
    while True:
        event_time = start + index * tick
        probes = tuple(event_time + offset for offset in offsets)
        if not probes or probes[-1] > stop + tick * 1e-6:
            break
        events.append((event_time, probes))
        index += 1
    return events

def check_v4_303_differential_pair_gm_limiter(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_1001 empty_trace"
    checked = hold_checked = polarity_errors = gain_errors = flag_errors = metric_errors = 0
    inactive_checked = inactive_errors = 0
    pos_seen = neg_seen = compressed_seen = False
    active_seen = disable_seen = False
    gm_gain = 4.0
    diff_limit = 120e-3
    for event_time, probe_times in _timer_events(rows):
        enable = sample_signal(rows, "enable", event_time)
        vinp = sample_signal(rows, "vinp", event_time)
        vinn = sample_signal(rows, "vinn", event_time)
        if enable is None or vinp is None or vinn is None:
            continue
        enabled = enable > 0.45
        disable_seen = disable_seen or (active_seen and not enabled)
        if not enabled:
            inactive_checked += 1
            event_bad = False
            for probe_time in probe_times:
                voutp = sample_signal(rows, "voutp", probe_time)
                voutn = sample_signal(rows, "voutn", probe_time)
                metric = sample_signal(rows, "gm_metric", probe_time)
                flag = sample_signal(rows, "limit_flag", probe_time)
                if None in (voutp, voutn, metric, flag):
                    event_bad = True
                    continue
                hold_checked += 1
                if not (
                    _v4_topup_near(voutp, 0.45, 0.08)
                    and _v4_topup_near(voutn, 0.45, 0.08)
                    and metric < 0.12
                    and flag < 0.12
                ):
                    event_bad = True
            inactive_errors += int(event_bad)
            continue
        active_seen = True
        diff = vinp - vinn
        limited = diff / (1.0 + abs(diff) / diff_limit)
        sep_expected = gm_gain * limited
        voutp_expected = _v4_topup_clip01(0.45 + 0.5 * sep_expected)
        voutn_expected = _v4_topup_clip01(0.45 - 0.5 * sep_expected)
        sep_expected = voutp_expected - voutn_expected
        gm_expected = 0.9 * diff_limit / (diff_limit + abs(diff))
        flag_expected_high = abs(diff) > diff_limit
        checked += 1
        pos_seen = pos_seen or diff > 0.025
        neg_seen = neg_seen or diff < -0.025
        compressed_seen = compressed_seen or flag_expected_high
        polarity_bad = gain_bad = metric_bad = flag_bad = False
        for probe_time in probe_times:
            voutp = sample_signal(rows, "voutp", probe_time)
            voutn = sample_signal(rows, "voutn", probe_time)
            metric = sample_signal(rows, "gm_metric", probe_time)
            flag = sample_signal(rows, "limit_flag", probe_time)
            if None in (voutp, voutn, metric, flag):
                polarity_bad = gain_bad = metric_bad = flag_bad = True
                continue
            hold_checked += 1
            sep_observed = voutp - voutn
            if abs(diff) >= 0.025 and sep_expected * sep_observed <= 0.0:
                polarity_bad = True
            if abs(sep_expected - sep_observed) > 0.13:
                gain_bad = True
            if abs(metric - gm_expected) > 0.18:
                metric_bad = True
            if (flag > 0.45) != flag_expected_high:
                flag_bad = True
        polarity_errors += int(polarity_bad)
        gain_errors += int(gain_bad)
        metric_errors += int(metric_bad)
        flag_errors += int(flag_bad)
    ok = (
        checked >= 20
        and pos_seen
        and neg_seen
        and compressed_seen
        and disable_seen
        and inactive_checked >= 8
        and inactive_errors == 0
        and polarity_errors == 0
        and gain_errors == 0
        and metric_errors == 0
        and flag_errors == 0
    )
    diagnostics = {
        "P_WHEN_DISABLED_DRIVE_BOTH_OUTPUTS_TO": max(
            int(not disable_seen or inactive_checked < 8),
            inactive_errors,
        ),
        "P_WHEN_ENABLED_CONVERT_THE_SAMPLED_DIFFERENTIAL": int(checked < 20) + polarity_errors,
        "P_SCALE_SMALL_SIGNAL_OUTPUT_SEPARATION_BY": gain_errors,
        "P_DRIVE_GM_METRIC_AS_A_VOLTAGE": metric_errors,
        "P_ASSERT_LIMIT_FLAG_ONLY_WHEN_COMPRESSION": flag_errors,
        "P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE": 0,
    }
    return ok, (
        f"v4_303 checked_events={checked} hold_probes={hold_checked} pos={pos_seen} neg={neg_seen} compressed={compressed_seen} "
        f"disable_seen={disable_seen} inactive_checked={inactive_checked} inactive_errors={inactive_errors} "
        f"polarity_errors={polarity_errors} gain_errors={gain_errors} "
        f"metric_errors={metric_errors} flag_errors={flag_errors}; "
        + "; ".join(f"{key} mismatch_count={value}" for key, value in diagnostics.items())
    )

CHECKER_ID = "v4_303_differential_pair_gm_limiter"
CHECKER: Checker = check_v4_303_differential_pair_gm_limiter
