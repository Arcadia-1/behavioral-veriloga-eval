"""Task-specific checker for canonical v4 DUT 006."""
from __future__ import annotations

from ..api import Checker
def sample_signal_at(rows: list[dict[str, float]], signal: str, time_s: float) -> float | None:
    if not rows or "time" not in rows[0] or signal not in rows[0]:
        return None
    first_time = rows[0]["time"]
    last_time = rows[-1].get("time")
    if last_time is None or time_s < first_time or time_s > last_time:
        return None
    if time_s == first_time:
        return rows[0].get(signal)
    for idx in range(1, len(rows)):
        prev = rows[idx - 1]
        cur = rows[idx]
        t0 = prev.get("time")
        t1 = cur.get("time")
        if t0 is None or t1 is None:
            continue
        if t0 <= time_s <= t1:
            v0 = prev.get(signal)
            v1 = cur.get(signal)
            if v0 is None or v1 is None:
                return None
            if t1 == t0:
                return v1
            alpha = (time_s - t0) / (t1 - t0)
            return v0 + alpha * (v1 - v0)
    return None

def check_v3_element_shuffler(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst_n", "out0", "out1", "out2", "out3"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/clk/rst_n/out0/out1/out2/out3"

    signals = ["out0", "out1", "out2", "out3"]
    sample_times_ns = [20.0, 40.0, 60.0, 80.0, 100.0, 120.0, 160.0, 180.0, 200.0, 220.0]
    expected = [2, 0, 3, 1, 2, 0, 2, 0, 3, 1]
    observed: list[int | None] = []
    failures: list[str] = []
    reset_low_probe_ns = 138.0
    reset_low_value = sample_signal_at(rows, "rst_n", reset_low_probe_ns * 1e-9)
    if reset_low_value is None:
        failures.append(f"missing_rst_n_probe_at={reset_low_probe_ns:g}ns")
    elif reset_low_value > 0.45:
        failures.append(f"rst_n_not_low_at={reset_low_probe_ns:g}ns")

    for sample_t_ns, expected_idx in zip(sample_times_ns, expected):
        rst_value = sample_signal_at(rows, "rst_n", sample_t_ns * 1e-9)
        if rst_value is None:
            failures.append(f"missing_rst_n_at={sample_t_ns:g}ns")
        elif rst_value <= 0.45:
            failures.append(f"rst_n_not_released_at={sample_t_ns:g}ns")
        values = [sample_signal_at(rows, signal, sample_t_ns * 1e-9) for signal in signals]
        if any(value is None for value in values):
            failures.append(f"missing_sample_at={sample_t_ns:g}ns")
            observed.append(None)
            continue
        active = [idx for idx, value in enumerate(values) if value is not None and value > 0.45]
        observed.append(active[0] if len(active) == 1 else None)
        if active != [expected_idx]:
            failures.append(f"{sample_t_ns:g}ns_active={active}_expected={expected_idx}")

    observed_text = ",".join("-" if item is None else str(item) for item in observed)
    expected_text = ",".join(str(item) for item in expected)
    if failures:
        return False, f"active_sequence={observed_text} expected={expected_text} failures={' '.join(failures)}"
    return True, f"active_sequence={observed_text} expected={expected_text} reset_low_at={reset_low_probe_ns:g}ns"

def check_v4_element_shuffler(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "rst_n", "out0", "out1", "out2", "out3"}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0])) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing)

    clock_rises: list[float] = []
    reset_falls: list[float] = []
    for previous, current in zip(rows, rows[1:]):
        if previous["clk"] < 0.45 <= current["clk"]:
            clock_rises.append(current["time"])
        if previous["rst_n"] > 0.45 >= current["rst_n"]:
            reset_falls.append(current["time"])

    output_for_state = (1, 2, 0, 3)
    state = 0
    active_clock_count = 0
    reset_sample_count = 0
    failures: list[str] = []
    observations: list[str] = []
    events = [(time_s, "reset") for time_s in reset_falls]
    events.extend((time_s, "clock") for time_s in clock_rises)
    for event_time, kind in sorted(events):
        if kind == "reset":
            state = 0
            reset_sample_count += 1
        else:
            rst_n = sample_signal_at(rows, "rst_n", event_time)
            if rst_n is None:
                failures.append(f"clock@{event_time * 1e9:.3f}ns_rst=missing")
                continue
            if rst_n <= 0.45:
                continue
            state = (state + 1) % 4
            active_clock_count += 1

        expected_index = output_for_state[state]
        values = [sample_signal_at(rows, f"out{index}", event_time + 2.0e-9) for index in range(4)]
        if any(value is None for value in values):
            failures.append(f"{kind}@{event_time * 1e9:.3f}ns=missing")
            continue
        assert all(value is not None for value in values)
        active = [index for index, value in enumerate(values) if value > 0.45]
        observations.append(str(active[0]) if len(active) == 1 else "-")
        for index, value in enumerate(values):
            if index == expected_index and value < 0.81:
                failures.append(
                    f"{kind}@{event_time * 1e9:.3f}ns_out{index}_high={value:.3f}<0.810"
                )
            elif index != expected_index and value > 0.09:
                failures.append(
                    f"{kind}@{event_time * 1e9:.3f}ns_out{index}_low={value:.3f}>0.090"
                )

    coverage_ok = active_clock_count >= 8 and reset_sample_count >= 1
    return coverage_ok and not failures, (
        f"active_clocks={active_clock_count} reset_samples={reset_sample_count} "
        f"active_sequence={','.join(observations)} failures={len(failures)}"
        + (" failure_detail=" + ";".join(failures[:6]) if failures else "")
    )

CHECKER_ID = "v4_006_element_shuffler"
CHECKER: Checker = check_v4_element_shuffler
