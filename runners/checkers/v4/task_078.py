"""Task-specific checker for canonical v4 DUT 078."""
from __future__ import annotations

from ..api import Checker
from .stimulus_relative import crossings, diagnostic, pass_note, require_signals


PROPERTY_IDS = (
    "P_RESET_SEED",
    "P_ENABLE_GATING",
    "P_FEEDBACK_POLYNOMIAL",
    "P_SHIFT_SEQUENCE",
    "P_SERIAL_OUTPUT",
    "P_OUTPUT_LEVELS",
)


def check_prbs7(rows: list[dict[str, float]]) -> tuple[bool, str]:
    """PRBS-7: require the exposed state bus to follow the public tap relation."""
    required = {"clk", "rst_n", "en", "serial_out"} | {f"state_{idx}" for idx in range(7)}
    missing = require_signals(rows, required | {"time"}, "P_OUTPUT_LEVELS")
    if missing is not None:
        return False, missing

    def logic(row: dict[str, float], name: str) -> int | None:
        value = row[name]
        if value >= 0.7:
            return 1
        if value <= 0.2:
            return 0
        return None

    def state_code(row: dict[str, float]) -> int | None:
        code = 0
        for idx in range(7):
            bit = logic(row, f"state_{idx}")
            if bit is None:
                return None
            code |= bit << idx
        return code

    reset_codes: list[int] = []
    gate_failures: list[str] = []
    hold_checks = 0
    reset_checks = 0
    prev_code: int | None = None
    clk_edges = crossings(rows, "clk", threshold=0.45, direction="rising")
    if len(clk_edges) < 12:
        return False, diagnostic(
            "P_SHIFT_SEQUENCE",
            "missing_event",
            expected="clk_rises>=12",
            observed=f"clk_rises:{len(clk_edges)}",
            event="full_trace",
        )
    clk_period = _median_interval(clk_edges)
    sample_delay = 0.20 * clk_period
    for edge_index, edge_t in enumerate(clk_edges):
        row = _sample_after(rows, edge_t, sample_delay)
        code = state_code(row)
        serial = logic(row, "serial_out")
        if code is None or serial is None:
            continue
        if serial != ((code >> 6) & 1):
            return False, (
                diagnostic(
                    "P_SERIAL_OUTPUT",
                    "value_mismatch",
                    expected=f"serial_out:{(code >> 6) & 1}",
                    observed=f"serial_out:{serial}",
                    event=f"clk_rise[{edge_index}]",
                )
            )
        if row["rst_n"] <= 0.45:
            reset_codes.append(code)
            reset_checks += 1
            prev_code = code
            continue
        if row["en"] <= 0.45:
            if prev_code is not None:
                hold_checks += 1
                if code != prev_code:
                    gate_failures.append(
                        diagnostic(
                            "P_ENABLE_GATING",
                            "value_mismatch",
                            expected=f"state:{prev_code}",
                            observed=f"state:{code}",
                            event=f"clk_rise[{edge_index}]",
                        )
                    )
            prev_code = code
            continue
        prev_code = code
    if reset_codes:
        reset_unique = sorted(set(reset_codes))
        if len(reset_unique) != 1 or reset_unique[0] == 0:
            gate_failures.append(
                diagnostic(
                    "P_RESET_SEED",
                    "value_mismatch",
                    expected="single_nonzero_seed",
                    observed=f"states:{reset_unique}",
                    event="rst_n_low_clk_rises",
                )
            )
    if gate_failures:
        return False, " ".join(gate_failures[:5])

    reset_release = crossings(rows, "rst_n", threshold=0.45, direction="rising")
    active_start = reset_release[-1] if reset_release else rows[0]["time"]
    post = [row for row in rows if row["time"] >= active_start and row["rst_n"] > 0.7 and row["en"] > 0.7]
    if len(post) < 20:
        return False, diagnostic(
            "P_SHIFT_SEQUENCE",
            "missing_event",
            expected="enabled_post_reset_samples>=20",
            observed=f"enabled_post_reset_samples:{len(post)}",
            event="rst_release_to_trace_end",
        )

    stable_codes: list[int] = []
    serial_bits: list[int] = []
    for row in post:
        code = state_code(row)
        serial = logic(row, "serial_out")
        if code is None or serial is None:
            continue
        if serial != ((code >> 6) & 1):
            return False, diagnostic(
                "P_SERIAL_OUTPUT",
                "value_mismatch",
                expected=f"serial_out:{(code >> 6) & 1}",
                observed=f"serial_out:{serial}",
                event="enabled_sample",
            )
        if not stable_codes or stable_codes[-1] != code:
            stable_codes.append(code)
            serial_bits.append(serial)

    if len(stable_codes) < 10:
        return False, diagnostic(
            "P_SHIFT_SEQUENCE",
            "missing_event",
            expected="unique_state_steps>=10",
            observed=f"unique_state_steps:{len(stable_codes)}",
            event="enabled_samples",
        )
    if 0 in stable_codes:
        return False, diagnostic(
            "P_RESET_SEED",
            "value_mismatch",
            expected="nonzero_prbs_state",
            observed="state:0",
            event="enabled_samples",
        )

    mismatches = 0
    feedback_mismatches = 0
    shift_mismatches = 0
    checked = 0
    for current, observed_next in zip(stable_codes, stable_codes[1:]):
        # Public reference recurrence used by the release gold:
        # new state_0 = old state_6 XOR old state_5; higher bits shift up.
        feedback = ((current >> 6) & 1) ^ ((current >> 5) & 1)
        expected_next = ((current & 0x3F) << 1) | feedback
        checked += 1
        if (observed_next & 1) != feedback:
            feedback_mismatches += 1
        for bit_index in range(1, 7):
            if ((observed_next >> bit_index) & 1) != ((current >> (bit_index - 1)) & 1):
                shift_mismatches += 1
        if observed_next != expected_next:
            mismatches += 1

    serial_transitions = sum(1 for idx in range(len(serial_bits) - 1) if serial_bits[idx] != serial_bits[idx + 1])
    ok = checked >= 8 and mismatches == 0 and serial_transitions >= 3
    note = (
        f"state_steps={len(stable_codes)} checked_transitions={checked} "
        f"mismatches={mismatches} serial_transitions={serial_transitions} "
        f"shift_mismatches={shift_mismatches} feedback_mismatches={feedback_mismatches} "
        f"reset_checks={reset_checks} hold_checks={hold_checks}"
    )
    if not ok:
        return False, diagnostic(
            "P_FEEDBACK_POLYNOMIAL",
            "value_mismatch",
            expected="mismatches:0,serial_transitions>=3,checked>=8",
            observed=(
                f"mismatches:{mismatches},serial_transitions:{serial_transitions},"
                f"checked:{checked}"
            ),
            event="enabled_state_transitions",
        )
    return True, pass_note(PROPERTY_IDS, note)

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


def _median_interval(times: list[float]) -> float:
    intervals = sorted(b - a for a, b in zip(times, times[1:]) if b > a)
    if not intervals:
        return 1e-9
    return intervals[len(intervals) // 2]

CHECKER_ID = "v4_078_lfsr_prbs_generator"
CHECKER: Checker = check_prbs7
