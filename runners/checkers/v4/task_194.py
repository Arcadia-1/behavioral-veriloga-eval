"""Task-specific checker for canonical v4 DUT 194."""
from __future__ import annotations

from ..api import Checker
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

def _check_initial_outputs(
    rows: list[dict[str, float]],
    probe_time: float,
) -> tuple[bool, str]:
    expected = {
        "dout10": 0.0,
        "dout11": 0.0,
        "dout12": 0.0,
        "dout13": 0.9,
        **{f"gainctrl{bit}": 0.9 if (90 >> bit) & 1 else 0.0 for bit in range(7)},
        "ddiff": 0.0,
        "dop": 0.96,
        "dom": 0.32,
        "gctrlcode": 0.90,
    }
    for signal, wanted in expected.items():
        observed = sample_signal_at(rows, signal, probe_time)
        if observed is None:
            return False, f"missing_pipe_adc_initial_output={signal}"
        tolerance = 0.10 if signal.startswith(("dout", "gainctrl")) else 0.04
        if abs(observed - wanted) > tolerance:
            return False, (
                f"initial_{signal}@{probe_time * 1e9:.3f}ns "
                f"observed={observed:.3f} expected={wanted:.3f}"
            )
    return True, "initial_pipe_adc_outputs_valid"

def check_v3_pipe_adc_gain_control_loop(rows: list[dict[str, float]]) -> tuple[bool, str]:
    required = {
        "time",
        "din20",
        "din21",
        "din22",
        "din23",
        "din24",
        "din25",
        "din26",
        "clks",
        "dout10",
        "dout11",
        "dout12",
        "dout13",
        "gainctrl0",
        "gainctrl1",
        "gainctrl2",
        "gainctrl3",
        "gainctrl4",
        "gainctrl5",
        "gainctrl6",
        "ddiff",
        "dop",
        "dom",
        "gctrlcode",
    }
    if not rows or not required.issubset(rows[0]):
        missing = sorted(required - set(rows[0])) if rows else sorted(required)
        return False, "missing_pipe_adc_gain_columns=" + ",".join(missing)
    times = [row["time"] for row in rows]
    edges = _threshold_crossings(
        [row["clks"] for row in rows], times, threshold=0.45, direction="rising"
    )
    if len(edges) < 3:
        return False, f"too_few_pipe_adc_gain_edges={len(edges)}"

    status = 0
    minus_code = 32
    plus_code = 96
    diff_code = 0
    gain_code = 90
    checked = 0
    max_err = 0.0
    failures: list[str] = []
    sampled_codes: set[int] = set()
    saw_minus_phase = saw_plus_phase = saw_gain_update = False

    initial_probe = 0.5 * (times[0] + edges[0])
    initial_ok, initial_detail = _check_initial_outputs(rows, initial_probe)
    if not initial_ok:
        return False, initial_detail
    checked += 1

    for edge_index, edge_t in enumerate(edges):
        code = 0
        for bit_index in range(7):
            value = sample_signal_at(rows, f"din2{bit_index}", edge_t + 1e-12)
            if value is None:
                return False, f"missing_pipe_adc_input_bit={bit_index}@{edge_t * 1e9:.3f}ns"
            if value > 0.45:
                code |= 1 << bit_index
        sampled_codes.add(code)

        previous_gain = gain_code
        if status == 0:
            minus_code = code
            status = 1
            dac_bits = (1, 1, 1, 0)
            saw_minus_phase = True
        else:
            plus_code = code
            diff_code = plus_code - minus_code
            step_code = abs(diff_code - 64)
            if diff_code > 64:
                gain_code = max(0, gain_code - step_code)
            elif diff_code < 64:
                gain_code = min(127, gain_code + step_code)
            status = 0
            dac_bits = (0, 0, 0, 1)
            saw_plus_phase = True
        saw_gain_update = saw_gain_update or gain_code != previous_gain

        expected = {
            **{f"dout1{bit}": 0.9 * dac_bits[bit] for bit in range(4)},
            **{f"gainctrl{bit}": 0.9 if (gain_code >> bit) & 1 else 0.0 for bit in range(7)},
            "ddiff": diff_code / 100.0,
            "dop": plus_code / 100.0,
            "dom": minus_code / 100.0,
            "gctrlcode": gain_code / 100.0,
        }
        probe_times = [edge_t + 0.08e-9]
        if edge_index + 1 < len(edges) and edges[edge_index + 1] - edge_t > 0.25e-9:
            probe_times.append(edges[edge_index + 1] - 0.10e-9)
        for probe_t in probe_times:
            if probe_t >= times[-1]:
                continue
            for signal, wanted in expected.items():
                observed = sample_signal_at(rows, signal, probe_t)
                if observed is None:
                    return False, f"missing_pipe_adc_output={signal}@{probe_t * 1e9:.3f}ns"
                tolerance = 0.10 if signal.startswith(("dout", "gainctrl")) else 0.04
                error = abs(observed - wanted)
                max_err = max(max_err, error)
                if error > tolerance:
                    failures.append(
                        f"{signal}@{probe_t * 1e9:.3f}ns observed={observed:.3f} "
                        f"expected={wanted:.3f} code={code} phase={status}"
                    )
            checked += 1

    if checked < 4 or len(sampled_codes) < 2 or not (saw_minus_phase and saw_plus_phase):
        return False, (
            f"insufficient_pipe_adc_gain_coverage checked={checked} codes={sorted(sampled_codes)} "
            f"minus={saw_minus_phase} plus={saw_plus_phase} gain_update={saw_gain_update}"
        )
    if not saw_gain_update:
        return False, f"missing_pipe_adc_gain_update codes={sorted(sampled_codes)}"
    if failures:
        return False, " ".join(failures[:8])
    return True, (
        f"checked={checked} codes={sorted(sampled_codes)} minus={saw_minus_phase} "
        f"plus={saw_plus_phase} gain_update={saw_gain_update} max_err={max_err:.4f}"
    )

CHECKER_ID = "v4_194_pipe_adc_gain_control_loop"
CHECKER: Checker = check_v3_pipe_adc_gain_control_loop
