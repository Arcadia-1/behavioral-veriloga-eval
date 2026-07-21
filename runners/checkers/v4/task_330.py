"""Task-specific checker for canonical v4 DUT 330."""
from __future__ import annotations

from ..api import Checker
from ..common.relative_events import rising_edges, sample_after_event
VCM = 0.45
VTH = 0.45

def _high(row: dict[str, float], name: str, thr: float = VTH) -> bool:
    return float(row.get(name, 0.0)) > thr

def _rising(prev: float, now: float, thr: float = VTH) -> bool:
    return now > thr and prev <= thr

def _missing(rows: list[dict[str, float]], required: set[str]) -> list[str]:
    if not rows:
        return sorted(required)
    return sorted(required - set(rows[0].keys()))

def check_v4_330_ffe_tap_adaptation_monitor(rows: list[dict[str, float]]) -> tuple[bool, str]:
    req = {
        "time", "err_in", "clk", "rst", "enable",
        "tap_pre", "tap_post", "main_out", "adapt_metric", "done",
    }
    miss = _missing(rows, req)
    if miss:
        return False, f"v4_330 missing_signals={','.join(miss)}"

    expected_pre = expected_post = expected_updates = 0
    oracle_checked = oracle_errors = 0
    for edge_time in rising_edges(rows, "clk"):
        edge_index = next(
            (index for index, row in enumerate(rows) if float(row["time"]) >= edge_time),
            None,
        )
        if edge_index is None:
            continue
        stimulus = rows[max(0, edge_index - 1)]
        active = _high(stimulus, "enable") and not _high(stimulus, "rst")
        if not active:
            expected_pre = expected_post = expected_updates = 0
            continue
        if float(stimulus["err_in"]) >= VCM:
            expected_pre = min(3, expected_pre + 1)
            expected_post = max(-3, expected_post - 1)
        else:
            expected_pre = max(-3, expected_pre - 1)
            expected_post = min(3, expected_post + 1)
        expected_updates = min(6, expected_updates + 1)
        post = sample_after_event(
            rows,
            edge_time,
            clock_signal="clk",
            fraction_of_period=0.15,
        )
        if post is None:
            continue
        expected_tap_pre = VCM + 0.08 * expected_pre
        expected_tap_post = VCM + 0.08 * expected_post
        expected_main = max(
            0.0,
            min(
                0.9,
                VCM
                - 0.45 * (expected_tap_pre - VCM)
                - 0.30 * (expected_tap_post - VCM)
                + 0.20 * (float(post["err_in"]) - VCM),
            ),
        )
        expected_adapt = abs(expected_tap_pre - VCM) + abs(expected_tap_post - VCM)
        oracle_checked += 1
        if (
            abs(float(post["tap_pre"]) - expected_tap_pre) > 0.05
            or abs(float(post["tap_post"]) - expected_tap_post) > 0.05
            or abs(float(post["main_out"]) - expected_main) > 0.08
            or abs(float(post["adapt_metric"]) - expected_adapt) > 0.08
            or _high(post, "done") != (expected_updates >= 6)
        ):
            oracle_errors += 1
    prev_clk = float(rows[0]["clk"])
    checked = main_errors = adapt_errors = done_errors = clear_errors = polarity_errors = 0
    reset_clear = disabled_clear = ever_enabled = False
    updates = 0
    adapt_max = 0.0
    done_at = None
    for row in rows:
        t = float(row["time"])
        clk = float(row["clk"])
        rst = _high(row, "rst")
        enabled = _high(row, "enable") and not rst
        if not enabled:
            clear = (
                abs(float(row["tap_pre"]) - VCM) < 0.08
                and abs(float(row["tap_post"]) - VCM) < 0.08
                and abs(float(row["main_out"]) - VCM) < 0.12
                and abs(float(row["adapt_metric"])) < 0.08
                and not _high(row, "done")
            )
            if rst and clear:
                reset_clear = True
            if ever_enabled and (not _high(row, "enable")) and clear:
                disabled_clear = True
            if (rst or (ever_enabled and not _high(row, "enable") and disabled_clear)) and not clear:
                clear_errors += 1
            updates = 0
            prev_clk = clk
            continue
        ever_enabled = True
        if not _rising(prev_clk, clk):
            prev_clk = clk
            continue
        prev_clk = clk
        checked += 1
        updates += 1
        err = float(row["err_in"])
        main = float(row["main_out"])
        expected_main = VCM + 0.65 * (err - VCM)
        if abs(main - expected_main) > 0.15:
            main_errors += 1
        adapt = float(row["adapt_metric"])
        adapt_max = max(adapt_max, adapt)
        pre_offset = float(row["tap_pre"]) - VCM
        post_offset = float(row["tap_post"]) - VCM
        tap_mag = abs(pre_offset) + abs(post_offset)
        if max(abs(pre_offset), abs(post_offset)) > 0.02 and pre_offset * post_offset > 0.0:
            polarity_errors += 1
        if adapt + 0.08 < tap_mag:
            adapt_errors += 1
        done = _high(row, "done")
        if done and updates < 6:
            done_errors += 1
        if done and done_at is None:
            done_at = t
        if (not done) and updates >= 8:
            done_errors += 1
    ok = (
        checked >= 8
        and oracle_checked >= 8
        and oracle_errors == 0
        and reset_clear
        and disabled_clear
        and main_errors <= max(3, checked // 3)
        and adapt_errors <= max(2, checked // 4)
        and polarity_errors == 0
        and done_errors <= 3
        and clear_errors <= 6
    )
    return ok, (
        f"v4_330 checked={checked} updates={updates} done_at={done_at} adapt_max={adapt_max:.3f} "
        f"oracle_checked={oracle_checked} oracle_errors={oracle_errors} main_errors={main_errors} "
        f"adapt_errors={adapt_errors} polarity_errors={polarity_errors} done_errors={done_errors} "
        f"reset_clear={reset_clear} disabled_clear={disabled_clear} clear_errors={clear_errors}; "
        f"P_ON_RESET_OR_WHEN_DISABLED_CLEAR mismatch_count={int(not reset_clear) + int(not disabled_clear)}; "
        f"P_ON_EACH_ENABLED_RISING_CLK_EDGE mismatch_count={max(0, 8 - checked)}; "
        f"P_DRIVE_MAIN_OUT_AS_THE_CURRENT mismatch_count={main_errors}; "
        f"P_EXPOSE_AGGREGATE_TAP_MAGNITUDE_ON_ADAPT mismatch_count={adapt_errors + polarity_errors}; "
        f"P_ASSERT_DONE_AFTER_SIX_ENABLED_ADAPTATION mismatch_count={done_errors}"
    )

CHECKER_ID = "v4_330_ffe_tap_adaptation_monitor"
CHECKER: Checker = check_v4_330_ffe_tap_adaptation_monitor
