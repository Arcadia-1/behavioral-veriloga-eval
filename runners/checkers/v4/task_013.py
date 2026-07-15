"""Task-specific checker for canonical v4 DUT 013."""
from __future__ import annotations

from ..api import Checker
def sample_signal(rows: list[dict[str, float]], signal: str, time_s: float) -> float | None:
    if not rows or signal not in rows[0] or "time" not in rows[0]:
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
    return rows[-1].get(signal)

def check_resettable_integrator(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {"time", "vin", "rst", "vout"}
    if not rows or not required.issubset(rows[0]):
        return False, "missing time/vin/rst/vout"

    vin_drive = [sample_signal(rows, "vin", t_ns * 1e-9) for t_ns in (80.0, 200.0, 280.0)]
    rst_levels = [sample_signal(rows, "rst", t_ns * 1e-9) for t_ns in (10.0, 80.0, 230.0, 280.0)]
    if any(value is None for value in vin_drive) or any(value is None for value in rst_levels):
        return False, "missing_vin_or_rst_samples"
    assert all(value is not None for value in vin_drive)
    assert all(value is not None for value in rst_levels)
    input_drive = all(value > 0.001 for value in vin_drive)
    reset_sequence = rst_levels[0] > 0.80 and rst_levels[1] < 0.10 and rst_levels[2] > 0.80 and rst_levels[3] < 0.10

    sample_times_ns = [80.0, 200.0, 230.0, 245.0, 300.0]
    samples: list[float] = []
    for t_ns in sample_times_ns:
        value = sample_signal(rows, "vout", t_ns * 1e-9)
        if value is None:
            return False, f"missing_sample_at={t_ns:g}ns"
        samples.append(value)

    pre_reset_integrated = 0.06 <= samples[0] < samples[1] and samples[1] > 0.30
    reset_clear = samples[2] < 0.05 and samples[3] < 0.05
    post_reset_restarts = 0.06 <= samples[4] <= 0.18
    ok = input_drive and reset_sequence and pre_reset_integrated and reset_clear and post_reset_restarts
    values = ",".join(f"{value:.3f}" for value in samples)
    return ok, (
        f"integrator_samples={values} input_drive={input_drive} "
        f"reset_sequence={reset_sequence} pre_reset_integrated={pre_reset_integrated} "
        f"reset_clear={reset_clear} post_reset_restarts={post_reset_restarts}"
    )

CHECKER_ID = "v4_013_resettable_integrator"
CHECKER: Checker = check_resettable_integrator
