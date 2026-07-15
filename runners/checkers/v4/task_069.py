"""Task-specific checker for canonical v4 DUT 069."""
from __future__ import annotations

from ..api import Checker
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

def check_configurable_pulse_train(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "start", "pulse", "done", *{f"period{i}" for i in range(4)}, *{f"width{i}" for i in range(4)}, *{f"count{i}" for i in range(4)}}
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0].keys())) if rows else sorted(required)
        return False, "missing_columns=" + ",".join(missing[:12])
    times = [row["time"] for row in rows]
    edge_pairs = [
        (rows[min(range(len(times)), key=lambda idx: abs(times[idx] - t))], _sample_after(rows, t, 1e-9))
        for t in _rising_times(rows, "clk")
    ]
    running = False
    period = width = total = 0
    tick = emitted = 0
    errors = 0
    done_seen = False
    expected_total = 0
    expected_total_all = 0
    zero_code_command = False
    failures: list[str] = []
    pre_start_quiet = False
    for edge_row, out_row in edge_pairs:
        if edge_row["start"] > 0.45 and not running:
            raw_period = _logic_bits_to_int(edge_row, "period", 4)
            raw_width = _logic_bits_to_int(edge_row, "width", 4)
            raw_total = _logic_bits_to_int(edge_row, "count", 4)
            zero_code_command = raw_period == 0 and raw_width == 0 and raw_total == 0
            period = max(1, raw_period)
            width = max(1, raw_width)
            total = max(1, raw_total)
            expected_total = total
            expected_total_all += total
            running = True
            tick = 0
            emitted = 0
        elif not running and expected_total == 0:
            pre_start_quiet = pre_start_quiet or (out_row["pulse"] <= 0.45 and out_row["done"] <= 0.45)
        expected_pulse = running and emitted < total and (tick % period) < width
        if (out_row["pulse"] > 0.45) != expected_pulse:
            errors += 1
            if zero_code_command:
                failures.append(
                    f"zero_code_minimum observed=pulse:{out_row['pulse']:.3f} expected=0.9 "
                    f"window={edge_row['time'] * 1e9:.3f}ns"
                )
            else:
                failures.append(
                    f"pulse_state observed={out_row['pulse']:.3f} expected={0.9 if expected_pulse else 0.0:.1f} "
                    f"window={edge_row['time'] * 1e9:.3f}ns period={period} width={width} count={total}"
                )
        if running:
            if tick % period == period - 1:
                emitted += 1
            tick += 1
            if emitted >= total and (tick % period) == 0:
                running = False
        expected_done = not running and emitted >= total and total > 0
        done_seen = done_seen or expected_done
        if (out_row["done"] > 0.45) != expected_done:
            errors += 1
            failures.append(
                f"done_state observed={out_row['done']:.3f} expected={0.9 if expected_done else 0.0:.1f} "
                f"window={edge_row['time'] * 1e9:.3f}ns period={period} width={width} count={total}"
            )
    pulse_count = len(_rising_times(rows, "pulse"))
    if expected_total_all and pulse_count != expected_total_all:
        errors += 1
        failures.insert(
            0,
            f"pulse_count observed={pulse_count} expected={expected_total_all} window=full_trace"
        )
    if failures:
        return False, " ".join(failures[:5])
    return errors == 0 and done_seen and pre_start_quiet, (
        f"errors={errors} done_seen={done_seen} pre_start_quiet={pre_start_quiet} "
        f"pulse_count={pulse_count} expected_total={expected_total_all}"
    )

CHECKER_ID = "v4_069_configurable_pulse_train_generator"
CHECKER: Checker = check_configurable_pulse_train
