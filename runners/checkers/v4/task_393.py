"""Task-specific checker for canonical v4 DUT 393."""
from __future__ import annotations

from bisect import bisect_left

from ..api import Checker
from .diagnostics import with_property_diagnostics


def _v4_topup_logic_high(row: dict[str, float], name: str, threshold: float = 0.45) -> bool:
    return float(row.get(name, 0.0)) > threshold

def _v4_rising(prev_v: float, now_v: float, vth: float = 0.45) -> bool:
    return now_v > vth and prev_v <= vth

def check_v4_952_deserializer_demux_alignment_macro(rows: list[dict[str, float]]) -> tuple[bool, str]:
    if not rows:
        return False, "v4_952 empty_trace"
    prev_clk = float(rows[0].get("clk", 0.0))
    prev_align = float(rows[0].get("align_pulse", 0.0))
    slot = 0
    updated = 0
    outs = [0.0, 0.0, 0.0, 0.0]
    checked = out_errors = metric_errors = valid_errors = clear_errors = 0
    reset_clear = disabled_clear = align_seen = valid_seen = one_seen = zero_seen = False
    ever_enabled = False
    disable_time: float | None = None
    times = [float(row["time"]) for row in rows]
    for row in rows:
        t = float(row["time"])
        rst = _v4_topup_logic_high(row, "rst")
        enabled = _v4_topup_logic_high(row, "enable") and not rst
        if not enabled:
            slot = 0; updated = 0; outs = [0.0, 0.0, 0.0, 0.0]
            clear = all(row[f"out{i}"] < 0.10 for i in range(4)) and row["phase_metric"] < 0.10 and row["word_valid"] < 0.10
            reset_clear = reset_clear or (rst and clear)
            disabled = ever_enabled and not _v4_topup_logic_high(row, "enable")
            if disabled and disable_time is None:
                disable_time = t
            disabled_ready = (
                disabled
                and disable_time is not None
                and t >= disable_time + 0.7e-9
            )
            disabled_clear = disabled_clear or (disabled_ready and clear)
            if (rst or disabled_ready) and not clear:
                clear_errors += 1
            prev_clk = float(row["clk"]); prev_align = float(row["align_pulse"])
            continue
        ever_enabled = True
        disable_time = None
        if _v4_rising(prev_align, float(row["align_pulse"])):
            slot = 0; updated = 0; align_seen = True
        if _v4_rising(prev_clk, float(row["clk"])):
            bit_v = 0.9 if _v4_topup_logic_high(row, "serial_in") else 0.0
            outs[slot] = bit_v
            expected_metric = 0.9 * slot / 3.0
            slot = (slot + 1) % 4
            updated = min(4, updated + 1)
            expected_valid = updated >= 4
            valid_seen = valid_seen or expected_valid
            one_seen = one_seen or bit_v > 0.45
            zero_seen = zero_seen or bit_v < 0.45
            sample_index = min(len(rows) - 1, bisect_left(times, t + 0.7e-9))
            sample = rows[sample_index]
            if (
                not _v4_topup_logic_high(sample, "rst")
                and _v4_topup_logic_high(sample, "enable")
            ):
                checked += 1
                for idx, expected in enumerate(outs):
                    if abs(float(sample[f"out{idx}"]) - expected) > 0.10:
                        out_errors += 1
                        break
                if abs(float(sample["phase_metric"]) - expected_metric) > 0.12:
                    metric_errors += 1
                if _v4_topup_logic_high(sample, "word_valid") != expected_valid:
                    valid_errors += 1
        prev_clk = float(row["clk"]); prev_align = float(row["align_pulse"])
    ok = checked >= 6 and reset_clear and disabled_clear and align_seen and valid_seen and one_seen and zero_seen and out_errors <= 2 and metric_errors <= 2 and valid_errors <= 1 and clear_errors <= 12
    return ok, f"v4_952 checked={checked} reset_clear={reset_clear} disabled_clear={disabled_clear} align_seen={align_seen} valid_seen={valid_seen} one_seen={one_seen} zero_seen={zero_seen} out_errors={out_errors} metric_errors={metric_errors} valid_errors={valid_errors} clear_errors={clear_errors}"

CHECKER_ID = "v4_393_deserializer_demux_alignment_macro"
CHECKER: Checker = with_property_diagnostics(
    check_v4_952_deserializer_demux_alignment_macro,
    {
        "P_ON_RESET_OR_WHEN_DISABLED_CLEAR": (
            "clear_errors",
            "!reset_clear",
            "!disabled_clear",
        ),
        "P_A_RISING_ALIGN_PULSE_RESETS_THE": "!align_seen",
        "P_ON_EACH_RISING_CLK_EDGE_WHILE": ("out_errors", "metric_errors"),
        "P_ASSERT_WORD_VALID_AFTER_ALL_FOUR": ("valid_errors", "!valid_seen"),
        "P_PHASE_METRIC_MUST_EXPOSE_THE_ACTIVE": "metric_errors",
    },
)
