"""Task-specific checker for canonical v4 DUT 078."""
from __future__ import annotations

from checkers.api import Checker
def check_prbs7(rows: list[dict[str, float]]) -> tuple[bool, str]:
    """PRBS-7: require the exposed state bus to follow the public tap relation."""
    if not rows:
        return False, "empty"
    required = {"clk", "rst_n", "en", "serial_out"} | {f"state_{idx}" for idx in range(7)}
    missing = required - set(rows[0])
    if missing:
        return False, f"missing_columns={','.join(sorted(missing))}"

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
    for edge_t in _rising_times(rows, "clk"):
        row = _sample_after(rows, edge_t, 0.15e-9)
        code = state_code(row)
        serial = logic(row, "serial_out")
        if code is None or serial is None:
            continue
        if serial != ((code >> 6) & 1):
            return False, (
                f"serial_state_mismatch observed=serial:{serial},state6:{(code >> 6) & 1} "
                f"expected=serial_out==state_6 window={edge_t * 1e9:.3f}ns"
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
                        f"enable_hold observed=state:{code} expected=state:{prev_code} "
                        f"window={edge_t * 1e9:.3f}ns"
                    )
            prev_code = code
            continue
        prev_code = code
    if reset_codes:
        reset_unique = sorted(set(reset_codes))
        if len(reset_unique) != 1 or reset_unique[0] == 0:
            gate_failures.append(
                f"reset_seed observed=states:{reset_unique} expected=single_nonzero_seed window=rst_n_low"
            )
    if gate_failures:
        return False, " ".join(gate_failures[:5])

    post = [row for row in rows if row["time"] > 2e-9 and row["rst_n"] > 0.7 and row["en"] > 0.7]
    if len(post) < 20:
        return False, "too_few_post_init_samples"

    stable_codes: list[int] = []
    serial_bits: list[int] = []
    for row in post:
        code = state_code(row)
        serial = logic(row, "serial_out")
        if code is None or serial is None:
            continue
        if serial != ((code >> 6) & 1):
            return False, f"serial_state_mismatch code={code}"
        if not stable_codes or stable_codes[-1] != code:
            stable_codes.append(code)
            serial_bits.append(serial)

    if len(stable_codes) < 10:
        return False, f"unique_state_steps={len(stable_codes)}"
    if 0 in stable_codes:
        return False, "entered_zero_state"

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
        f"shift_mismatches={shift_mismatches} feedback_mismatches={feedback_mismatches}"
    )
    if reset_checks or hold_checks:
        note += f" reset_checks={reset_checks} hold_checks={hold_checks}"
    return ok, note

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

CHECKER_ID = "v4_078_lfsr_prbs_generator"
CHECKER: Checker = check_prbs7
