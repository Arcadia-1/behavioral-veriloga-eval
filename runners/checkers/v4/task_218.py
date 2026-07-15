"""Task-specific checker for canonical v4 DUT 218."""
from __future__ import annotations

from ..api import Checker
def rising_edges(values: list[float], times: list[float], threshold: float = 0.45) -> list[float]:
    edges: list[float] = []
    for i in range(1, len(values)):
        if values[i - 1] < threshold <= values[i]:
            edges.append(times[i])
    return edges

def _threshold_crossings(
    values: list[float],
    times: list[float],
    *,
    threshold: float = 0.0,
    direction: str,
) -> list[float]:
    edges: list[float] = []
    for idx in range(1, len(values)):
        v0 = values[idx - 1]
        v1 = values[idx]
        if direction == "rising":
            hit = v0 <= threshold < v1
        elif direction == "falling":
            hit = v0 >= threshold > v1
        else:
            raise ValueError(f"unsupported direction={direction!r}")
        if not hit:
            continue
        t0 = times[idx - 1]
        t1 = times[idx]
        if v1 == v0:
            edges.append(t1)
        else:
            alpha = (threshold - v0) / (v1 - v0)
            edges.append(t0 + alpha * (t1 - t0))
    return edges

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

def _max_signal_value(
    rows: list[dict[str, float]],
    signals: list[str],
    *,
    default: float,
) -> float:
    values: list[float] = []
    for row in rows:
        for signal in signals:
            value = row.get(signal)
            if value is not None:
                values.append(value)
    return max(values) if values else default

def _event_probe_time(
    rows: list[dict[str, float]],
    event_time_s: float,
    *,
    delay_s: float = 0.18e-9,
) -> float | None:
    if not rows:
        return None
    last_time = rows[-1].get("time")
    if last_time is None:
        return None
    probe_time = event_time_s + delay_s
    if probe_time <= last_time:
        return probe_time
    fallback = last_time - 0.02e-9
    return fallback if fallback > event_time_s else None

def check_v3_clocked_comparator_dual_output(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "clk", "vinn", "vinp", "outn", "outp"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing clocked comparator dual output signals"
    vdd = _max_signal_value(rows, ["clk", "outp", "outn"], default=1.0)
    vth = 0.5 * vdd
    times = [row["time"] for row in rows]
    clk_values = [row["clk"] for row in rows]
    rising_edges = _threshold_crossings(clk_values, times, threshold=vth, direction="rising")
    falling_edges = _threshold_crossings(clk_values, times, threshold=vth, direction="falling")
    if len(rising_edges) < 2 or len(falling_edges) < 1:
        return False, f"insufficient_clock_edges rise={len(rising_edges)} fall={len(falling_edges)}"

    failures: list[str] = []
    decision_checks = 0
    reset_checks = 0
    saw_positive = False
    saw_negative = False
    saw_equal = False

    for edge_t in rising_edges:
        probe_t = _event_probe_time(rows, edge_t, delay_s=0.22e-9)
        if probe_t is None:
            continue
        vinp = sample_signal_at(rows, "vinp", edge_t)
        vinn = sample_signal_at(rows, "vinn", edge_t)
        outp = sample_signal_at(rows, "outp", probe_t)
        outn = sample_signal_at(rows, "outn", probe_t)
        if vinp is None or vinn is None or outp is None or outn is None:
            continue
        if vinp > vinn + 1e-6:
            exp_p, exp_n = vdd, 0.0
            saw_positive = True
        elif vinn > vinp + 1e-6:
            exp_p, exp_n = 0.0, vdd
            saw_negative = True
        else:
            exp_p, exp_n = 0.0, 0.0
            saw_equal = True
        decision_checks += 1
        if abs(outp - exp_p) > 0.08 or abs(outn - exp_n) > 0.08:
            failures.append(
                f"decision@{probe_t * 1e9:.3f}ns outp/outn={outp:.3f}/{outn:.3f} "
                f"expected={exp_p:.3f}/{exp_n:.3f}"
            )

    for edge_t in falling_edges:
        probe_t = _event_probe_time(rows, edge_t, delay_s=0.22e-9)
        if probe_t is None:
            continue
        outp = sample_signal_at(rows, "outp", probe_t)
        outn = sample_signal_at(rows, "outn", probe_t)
        if outp is None or outn is None:
            continue
        reset_checks += 1
        if abs(outp) > 0.08 or abs(outn) > 0.08:
            failures.append(f"reset@{probe_t * 1e9:.3f}ns outp/outn={outp:.3f}/{outn:.3f}")

    if decision_checks < 2 or reset_checks < 1:
        return False, f"insufficient_checks decisions={decision_checks} resets={reset_checks}"
    if not (saw_positive and saw_negative):
        return False, f"missing_polarity_coverage positive={saw_positive} negative={saw_negative} equal={saw_equal}"
    if failures:
        return False, " ".join(failures[:5])
    return True, (
        f"decisions={decision_checks} resets={reset_checks} "
        f"positive={saw_positive} negative={saw_negative} equal={saw_equal}"
    )

CHECKER_ID = "v4_218_clocked_comparator_dual_output"
CHECKER: Checker = check_v3_clocked_comparator_dual_output
