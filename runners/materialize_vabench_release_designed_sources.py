#!/usr/bin/env python3
from __future__ import annotations

import csv
import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = ROOT / "benchmark-vabench-release-v1"
TASKS_ROOT = PACKAGE_ROOT / "tasks"
TRACKER_CSV = ROOT / "docs" / "VABENCH_RELEASE_TRACKER.csv"
SELECTED_MANIFEST_CSV = ROOT / "docs" / "VABENCH_RELEASE_SELECTED_MANIFEST.csv"
SELECTED_MANIFEST_MD = ROOT / "docs" / "VABENCH_RELEASE_SELECTED_MANIFEST.md"

FORM_TO_FAMILY = {
    "dut": "spec-to-va",
    "tb": "tb-generation",
    "bugfix": "bugfix",
    "e2e": "end-to-end",
}


@dataclass(frozen=True)
class DesignedSpec:
    entry_id: str
    module: str
    summary: str
    behavior_checks: tuple[str, ...]
    profile: str
    bug: str


DESIGNED_SPECS: dict[str, DesignedSpec] = {
    "vbr1_l1_dac_mismatch_unit_weighting_model": DesignedSpec(
        "vbr1_l1_dac_mismatch_unit_weighting_model",
        "dac_mismatch_unit_weighting_model",
        "Model a 4-bit voltage DAC using explicit nonideal unit weights and a bounded output range.",
        ("weighted_code_response", "explicit_mismatch_terms", "bounded_reconstruction_voltage"),
        "weighted_dac",
        "The buggy implementation uses ideal binary weights and therefore hides the intended mismatch.",
    ),
    "vbr1_l1_charge_pump_abstraction": DesignedSpec(
        "vbr1_l1_charge_pump_abstraction",
        "charge_pump_abstraction",
        "Represent UP/DN pulse effects as a voltage-domain control-node update without current contributions.",
        ("up_pulse_increases_control", "down_pulse_decreases_control", "control_voltage_clamped"),
        "charge_pump",
        "The buggy implementation swaps UP and DN polarity.",
    ),
    "vbr1_l1_loop_filter_abstraction": DesignedSpec(
        "vbr1_l1_loop_filter_abstraction",
        "loop_filter_abstraction",
        "Approximate the continuous-time proportional/integral loop-filter trend with EVAS-supported sampled voltage-domain state updates on clock edges.",
        (
            "proportional_step_decays",
            "integral_residual_accumulates",
            "metric_asserts_after_valid_updates",
            "reset_clears_integrator",
            "filtered_output_bounded",
        ),
        "loop_filter",
        "The buggy implementation omits reset clearing of the integrator state.",
    ),
    "vbr1_l1_calibration_deadband_controller": DesignedSpec(
        "vbr1_l1_calibration_deadband_controller",
        "calibration_deadband_controller",
        "Update a bounded trim code only when the signed error is outside a deadband.",
        ("trim_holds_inside_deadband", "trim_moves_for_large_error", "trim_clamped_to_range"),
        "deadband_cal",
        "The buggy implementation updates the trim inside the deadband.",
    ),
    "vbr1_l1_successive_approximation_calibration_search_fsm": DesignedSpec(
        "vbr1_l1_successive_approximation_calibration_search_fsm",
        "successive_approximation_calibration_search_fsm",
        "Run a clocked successive-approximation trim search with halving step size and completion flag.",
        ("step_size_halves", "trim_direction_follows_error", "done_after_search_window"),
        "sar_cal_fsm",
        "The buggy implementation keeps a constant step size instead of halving it.",
    ),
    "vbr1_l2_complete_calibration_loop": DesignedSpec(
        "vbr1_l2_complete_calibration_loop",
        "complete_calibration_loop",
        "Close a simple calibration loop from error stimulus through controller and actuator output.",
        ("error_drives_trim", "actuator_moves_opposite_error", "loop_converges_toward_target"),
        "cal_loop",
        "The buggy implementation drives the actuator in the same direction as the error.",
    ),
    "vbr1_l1_event_pulse_stretcher": DesignedSpec(
        "vbr1_l1_event_pulse_stretcher",
        "event_pulse_stretcher",
        "Convert trigger crossings into a retriggerable one-shot pulse: every trigger while active refreshes the falling deadline.",
        (
            "trigger_creates_pulse",
            "retrigger_refreshes_pulse_deadline",
            "pulse_stays_high_through_burst",
            "reset_forces_low",
        ),
        "pulse_stretcher",
        "The buggy implementation ignores triggers while a pulse is already active, so burst triggers do not extend the pulse.",
    ),
    "vbr1_l2_adc_dac_source_sweep_flow": DesignedSpec(
        "vbr1_l2_adc_dac_source_sweep_flow",
        "adc_dac_source_sweep_flow",
        "Sweep an analog input through a small quantizer and DAC reconstruction path.",
        ("code_monotonic_with_input", "reconstruction_follows_code", "saturation_at_rails"),
        "adc_dac_sweep",
        "The buggy implementation omits output saturation at the top code.",
    ),
    "vbr1_l1_soft_hysteretic_limiter": DesignedSpec(
        "vbr1_l1_soft_hysteretic_limiter",
        "soft_hysteretic_limiter",
        "Limit a voltage signal with smooth compression and stateful hysteresis around thresholds.",
        ("smooth_limiting", "hysteresis_state_memory", "bounded_output"),
        "soft_limiter",
        "The buggy implementation collapses the hysteresis thresholds into a single threshold.",
    ),
    "vbr1_l1_voltage_gain_amplifier": DesignedSpec(
        "vbr1_l1_voltage_gain_amplifier",
        "voltage_gain_amplifier",
        "Apply a voltage-domain gain with output common-mode offset and rail clamps.",
        ("gain_applied", "common_mode_offset", "output_clamped"),
        "gain_amp",
        "The buggy implementation omits the rail clamp.",
    ),
    "vbr1_l1_higher_order_filter": DesignedSpec(
        "vbr1_l1_higher_order_filter",
        "higher_order_filter",
        "Approximate a second-order low-pass response with two sampled internal filter states.",
        ("two_filter_states", "step_response_is_smoothed", "reset_clears_states"),
        "two_pole_filter",
        "The buggy implementation updates only one pole state.",
    ),
    "vbr1_l2_amplifier_filter_chain": DesignedSpec(
        "vbr1_l2_amplifier_filter_chain",
        "amplifier_filter_chain",
        "Combine a gain block and low-pass filter and expose the filtered response metric.",
        ("amplified_input", "filtered_output_lags_input", "metric_tracks_settling"),
        "amp_filter_chain",
        "The buggy implementation measures the unfiltered amplifier output.",
    ),
}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def slugify(value: str) -> str:
    value = value.lower().replace("/", " ")
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def required_forms(row: dict[str, str]) -> list[str]:
    forms = row["required_task_forms"].replace("e2e-form", "e2e").split(";")
    return [form.strip() for form in forms if form.strip() in FORM_TO_FAMILY]


def va_source(module: str, profile: str, *, buggy: bool = False) -> str:
    variant = "buggy" if buggy else "fixed"
    if profile == "weighted_dac":
        weights = ("1.00, 2.00, 4.00, 8.00" if buggy else "1.00, 2.02, 3.96, 8.08")
        w0, w1, w2, w3 = (("1.00", "2.00", "4.00", "8.00") if buggy else ("1.00", "2.02", "3.96", "8.08"))
        total = "15.00" if buggy else "15.06"
        return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(b0, b1, b2, b3, out);
input b0, b1, b2, b3;
output out;
electrical b0, b1, b2, b3, out;
parameter real vhi = 0.9;
parameter real vlo = 0.0;
parameter real tr = 100p;
real y;
analog begin
    y = (((V(b0) > 0.45) ? {w0} : 0.00)
       + ((V(b1) > 0.45) ? {w1} : 0.00)
       + ((V(b2) > 0.45) ? {w2} : 0.00)
       + ((V(b3) > 0.45) ? {w3} : 0.00)) / {total};
    // {variant}: intended unit weights are [{weights}].
    V(out) <+ transition(vlo + (vhi - vlo) * y, 0, tr, tr);
end
endmodule
"""
    if profile == "charge_pump":
        up_update = "state = state - step;" if buggy else "state = state + step;"
        down_update = "state = state + step;" if buggy else "state = state - step;"
        return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
parameter real tr = 100p;
parameter real deadband = 0.05;
real state, step, errv, metricv;
analog begin
    @(initial_step) begin
        state = 0.45;
        step = 0.08;
        metricv = 0.45;
    end
    @(cross(V(clk) - 0.45, +1)) begin
        errv = V(vin) - 0.45;
        if (V(rst) > 0.45) begin
            state = 0.45;
            metricv = 0.45;
        end else if (errv > deadband) begin
            {up_update}
            metricv = 0.75;
        end else if (errv < -deadband) begin
            {down_update}
            metricv = 0.15;
        end else begin
            metricv = 0.45;
        end
        if (state > 0.85) state = 0.85;
        if (state < 0.05) state = 0.05;
    end
    V(out) <+ transition(state, 0, tr, tr);
    V(metric) <+ transition(metricv, 0, tr, tr);
end
endmodule
"""
    if profile in {"charge_pump", "loop_filter", "deadband_cal", "sar_cal_fsm", "cal_loop", "gain_cal_loop"}:
        update = "state = state - step;" if (buggy and profile in {"charge_pump", "cal_loop", "gain_cal_loop"}) else "state = state + step;"
        deadband_condition = "(errv > deadband || errv < -deadband)"
        if buggy and profile == "deadband_cal":
            deadband_condition = "(errv < deadband && errv > -deadband)"
        halve = "step = step * 0.5;" if not (buggy and profile == "sar_cal_fsm") else "step = step;"
        reset_line = "integ = 0.0;" if not (buggy and profile == "loop_filter") else "integ = integ;"
        done_line = "donev = (cycle >= 4) ? 0.9 : 0.0;" if not (buggy and profile == "sar_loop") else "donev = 0.0;"
        return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
parameter real tr = 100p;
parameter real deadband = 0.05;
real state, step, integ, errv, donev;
integer cycle;
analog begin
    @(initial_step) begin
        state = 0.45;
        step = 0.20;
        integ = 0.0;
        cycle = 0;
        donev = 0.0;
    end
    @(cross(V(clk) - 0.45, +1)) begin
        errv = V(vin) - 0.45;
        if (V(rst) > 0.45) begin
            state = 0.45;
            step = 0.20;
            {reset_line}
            cycle = 0;
            donev = 0.0;
        end else if {deadband_condition} begin
            if (errv > 0.0) begin
                {update}
            end else begin
                state = state - step;
            end
            integ = integ + errv * 0.04;
            {halve}
            cycle = cycle + 1;
            {done_line}
        end
        if (state > 0.85) state = 0.85;
        if (state < 0.05) state = 0.05;
    end
    V(out) <+ transition(state + integ, 0, tr, tr);
    V(metric) <+ transition(donev, 0, tr, tr);
end
endmodule
"""
    if profile == "pulse_stretcher":
        hold_line = "remaining = width;" if not buggy else "if (remaining <= 0.0) remaining = width;"
        metric_expr = "s1 - s2 + 0.45"
        if buggy and profile == "amp_filter_chain":
            metric_expr = "s1"
        return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(trig, rst, pulse);
input trig, rst;
output pulse;
electrical trig, rst, pulse;
parameter real tr = 50p;
parameter real width = 4n;
real level, remaining;
analog begin
    @(initial_step) begin
        level = 0.0;
        remaining = 0.0;
    end
    @(cross(V(trig) - 0.45, +1)) begin
        level = 0.9;
        {hold_line}
    end
    @(timer(0, 0.5n)) begin
        if (V(rst) > 0.45) begin
            level = 0.0;
            remaining = 0.0;
        end else if (remaining > 0.0) begin
            remaining = remaining - 0.5n;
            if (remaining <= 0.0) level = 0.0;
        end
    end
    V(pulse) <+ transition(level, 0, tr, tr);
end
endmodule
"""
    if profile in {"gain_amp", "soft_limiter", "two_pole_filter", "conditioning_chain", "amp_filter_chain"}:
        clamp = "" if (buggy and profile == "gain_amp") else "if (y > 0.9) y = 0.9; if (y < 0.0) y = 0.0;"
        pole2 = "s2 = s2 + alpha * (s1 - s2);" if not (buggy and profile in {"two_pole_filter", "conditioning_chain", "soft_limiter"}) else "s2 = s1;"
        alpha = "0.45" if profile == "gain_amp" else "0.18"
        metric_expr = "s1 - s2 + 0.45"
        if buggy and profile == "amp_filter_chain":
            metric_expr = "s1"
        if buggy and profile == "soft_limiter":
            hys_update = "hys = 0.0;"
        else:
            hys_update = "if (V(vin) > 0.62) hys = 0.04;\n            if (V(vin) < 0.38) hys = -0.04;"
        return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
parameter real tr = 100p;
parameter real gain = 1.8;
parameter real alpha = {alpha};
real s1, s2, y, hys;
analog begin
    @(initial_step) begin
        s1 = 0.0;
        s2 = 0.0;
        hys = 0.0;
    end
    @(cross(V(clk) - 0.45, +1)) begin
        if (V(rst) > 0.45) begin
            s1 = 0.0;
            s2 = 0.0;
            hys = 0.0;
        end else begin
            y = gain * (V(vin) - 0.45) + 0.45;
            {hys_update}
            s1 = s1 + alpha * (y + hys - s1);
            {pole2}
            y = s2;
            {clamp}
        end
    end
    V(out) <+ transition(y, 0, tr, tr);
    V(metric) <+ transition({metric_expr}, 0, tr, tr);
end
endmodule
"""
    return f"""`include "constants.vams"
`include "disciplines.vams"

module {module}(clk, rst, vin, aux, out, metric);
input clk, rst, vin, aux;
output out, metric;
electrical clk, rst, vin, aux, out, metric;
parameter real tr = 100p;
real sample, code, recon, metricv;
integer q;
analog begin
    @(initial_step) begin
        sample = 0.0;
        code = 0.0;
        recon = 0.0;
        metricv = 0.0;
    end
    @(cross(V(clk) - 0.45, +1)) begin
        if (V(rst) > 0.45) begin
            sample = 0.0;
            code = 0.0;
            recon = 0.0;
            metricv = 0.0;
        end else begin
            sample = V(vin);
            q = 0;
            if (sample > 0.9) q = 15;
            else if (sample > 0.0) q = sample / 0.9 * 15.0 + 0.5;
            code = q / 15.0;
            recon = 0.9 * code;
            metricv = (sample > 0.25 && sample < 0.65) ? 0.9 : 0.0;
        end
    end
    V(out) <+ transition(recon, 0, tr, tr);
    V(metric) <+ transition(metricv, 0, tr, tr);
end
endmodule
"""


def tb_source(module: str, form: str) -> str:
    calibration_modules = {
        "calibration_deadband_controller",
        "charge_pump_abstraction",
        "loop_filter_abstraction",
        "successive_approximation_calibration_search_fsm",
        "complete_calibration_loop",
    }
    filter_modules = {
        "soft_hysteretic_limiter",
        "voltage_gain_amplifier",
        "higher_order_filter",
        "amplifier_filter_chain",
    }
    if module == "dac_mismatch_unit_weighting_model":
        instance = f"XDUT (b0 b1 b2 b3 out) {module}"
        sources = """Vb0 (b0 0) vsource type=pwl wave=[0 0 5n 0 5.1n 0.9 10n 0.9 10.1n 0 20n 0 20.1n 0.9 40n 0.9]
Vb1 (b1 0) vsource type=pwl wave=[0 0 12n 0 12.1n 0.9 40n 0.9]
Vb2 (b2 0) vsource type=pwl wave=[0 0 20n 0 20.1n 0.9 40n 0.9]
Vb3 (b3 0) vsource type=pwl wave=[0 0 30n 0 30.1n 0.9 40n 0.9]"""
        saves = "save b0 b1 b2 b3 out"
    elif "pulse_stretcher" in module:
        instance = f"XDUT (trig rst pulse) {module}"
        sources = """Vtrig (trig 0) vsource type=pwl wave=[0 0 1n 0 1.1n 0.9 1.3n 0 3n 0 3.1n 0.9 3.3n 0 16n 0 16.1n 0.9 16.3n 0 18n 0 18.1n 0.9 18.3n 0 24n 0 24.1n 0.9 24.3n 0 50n 0]
Vrst  (rst  0) vsource type=pwl wave=[0 0 25n 0 25.1n 0.9 28n 0.9 28.1n 0]"""
        saves = "save trig rst pulse"
    elif module in {
        "adc_dac_source_sweep_flow",
    }:
        instance = f"XDUT (clk rst vin aux out metric) {module}"
        sources = """Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 period=2n width=1n rise=50p fall=50p
Vrst (rst 0) vsource type=pwl wave=[0 0.9 2n 0.9 2.1n 0 80n 0]
Vvin (vin 0) vsource type=pwl wave=[0 0.05 10n 0.1 30n 0.7 60n 0.35 80n 0.85]
Vaux (aux 0) vsource dc=0.45"""
        saves = "save clk rst vin out metric"
    elif module in calibration_modules:
        instance = f"XDUT (clk rst vin out metric) {module}"
        sources = """Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 period=2n width=1n rise=50p fall=50p
Vrst (rst 0) vsource type=pwl wave=[0 0.9 2n 0.9 2.1n 0 62n 0 62.1n 0.9 66n 0.9 66.1n 0 80n 0]
Vvin (vin 0) vsource type=pwl wave=[0 0.45 8n 0.47 14n 0.43 20n 0.75 40n 0.18 58n 0.72 68n 0.47 74n 0.78 80n 0.78]"""
        saves = "save clk rst vin out metric"
    elif module in filter_modules:
        instance = f"XDUT (clk rst vin out metric) {module}"
        sources = """Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 period=2n width=1n rise=50p fall=50p
Vrst (rst 0) vsource type=pwl wave=[0 0.9 2n 0.9 2.1n 0 80n 0]
Vvin (vin 0) vsource type=pwl wave=[0 0.45 8n 0.45 12n 0.9 28n 0.9 31n 0.45 37n 0.45 42n 0.1 58n 0.1 61n 0.45 67n 0.45 72n 0.85 80n 0.85]"""
        saves = "save clk rst vin out metric"
    else:
        instance = f"XDUT (clk rst vin out metric) {module}"
        sources = """Vclk (clk 0) vsource type=pulse val0=0 val1=0.9 period=2n width=1n rise=50p fall=50p
Vrst (rst 0) vsource type=pwl wave=[0 0.9 2n 0.9 2.1n 0 80n 0]
Vvin (vin 0) vsource type=pwl wave=[0 0.2 10n 0.25 25n 0.75 55n 0.35 80n 0.65]"""
        saves = "save clk rst vin out metric"
    include = f'ahdl_include "{module}.va"'
    if form == "bugfix":
        include = 'ahdl_include "dut_fixed.va"'
    return f"""simulator lang=spectre
global 0

{include}

{sources}

{instance}

tran tran stop=80n maxstep=0.5n
{saves}
"""


def port_contract(spec: DesignedSpec) -> dict[str, str]:
    if spec.profile == "weighted_dac":
        return {
            "module": f"module {spec.module}(b0, b1, b2, b3, out);",
            "directions": "input b0, b1, b2, b3;\noutput out;",
            "disciplines": "electrical b0, b1, b2, b3, out",
            "signals": "b0..b3 are voltage-coded logic bits, low=0 V and high=0.9 V with threshold 0.45 V. out is a bounded voltage reconstruction in [0, 0.9] V.",
            "saved": "b0 b1 b2 b3 out",
        }
    if spec.profile == "pulse_stretcher":
        return {
            "module": f"module {spec.module}(trig, rst, pulse);",
            "directions": "input trig, rst;\noutput pulse;",
            "disciplines": "electrical trig, rst, pulse",
            "signals": "trig and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. pulse is a voltage-coded output pulse. Each rising trig edge refreshes the pulse deadline to trigger_time + 4 ns; rst high forces pulse low.",
            "saved": "trig rst pulse",
        }
    if spec.profile == "loop_filter":
        return {
            "module": f"module {spec.module}(clk, rst, vin, out, metric);",
            "directions": "input clk, rst, vin;\noutput out, metric;",
            "disciplines": "electrical clk, rst, vin, out, metric",
            "signals": "clk and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. vin is a signed loop-error stimulus around 0.45 V. out is a bounded loop-control voltage. metric is a voltage-coded update/convergence observable.",
            "saved": "clk rst vin out metric",
        }
    if spec.profile in {"charge_pump", "deadband_cal", "sar_cal_fsm", "cal_loop", "gain_cal_loop"}:
        return {
            "module": f"module {spec.module}(clk, rst, vin, out, metric);",
            "directions": "input clk, rst, vin;\noutput out, metric;",
            "disciplines": "electrical clk, rst, vin, out, metric",
            "signals": "clk and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. vin is a signed error stimulus around 0.45 V. out is a bounded trim/control voltage. metric is a voltage-coded status or completion observable.",
            "saved": "clk rst vin out metric",
        }
    if spec.profile in {"gain_amp", "soft_limiter", "two_pole_filter", "conditioning_chain", "amp_filter_chain"}:
        return {
            "module": f"module {spec.module}(clk, rst, vin, out, metric);",
            "directions": "input clk, rst, vin;\noutput out, metric;",
            "disciplines": "electrical clk, rst, vin, out, metric",
            "signals": "clk and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. vin is an analog voltage stimulus. out is the bounded conditioned voltage. metric exposes the filter/settling internal response.",
            "saved": "clk rst vin out metric",
        }
    return {
        "module": f"module {spec.module}(clk, rst, vin, aux, out, metric);",
        "directions": "input clk, rst, vin, aux;\noutput out, metric;",
        "disciplines": "electrical clk, rst, vin, aux, out, metric",
        "signals": "clk and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. vin is the analog stimulus. aux is a reserved analog control input. out is the reconstructed output voltage. metric is a voltage-coded public observable.",
        "saved": "clk rst vin out metric",
    }


def prompt_text(row: dict[str, str], spec: DesignedSpec, form: str) -> str:
    family = FORM_TO_FAMILY[form]
    if form == "tb":
        artifact = "the Spectre testbench file"
        task_line = "Write a Spectre transient testbench for the described behavioral Verilog-A module."
    elif form == "bugfix":
        artifact = "the repaired Verilog-A artifact"
        task_line = f"Repair the supplied buggy Verilog-A implementation. Bug to fix: {spec.bug}"
    elif form == "e2e":
        artifact = "the Verilog-A module and Spectre testbench artifacts"
        task_line = "Write both the Verilog-A behavioral module and a Spectre transient testbench."
    else:
        artifact = "the Verilog-A DUT artifact"
        task_line = "Write the Verilog-A behavioral module only."
    checks = "\n".join(f"- {item}" for item in spec.behavior_checks)
    ports = port_contract(spec)
    abstraction_note = ""
    if spec.profile == "loop_filter":
        abstraction_note = (
            "\nThis is a sampled/event-driven behavioral abstraction of the loop-filter "
            "control trend. It must not require current-domain charge storage, true "
            "continuous-time RC integration, or KCL/KVL solving.\n"
        )
    return f"""# {row['base_function']} ({family})

{task_line}

Behavioral intent:

{spec.summary}

Module name: `{spec.module}`.
Domain: pure voltage-domain behavioral Verilog-A.
Do not use current contributions, transistor-level devices, AC/noise analysis,
or KCL/KVL solving assumptions.
{abstraction_note}

Public port contract:

```verilog
{ports['module']}
{ports['directions']}
{ports['disciplines']}
```

Signal contract:

{ports['signals']}

Saved waveform columns:

```text
{ports['saved']}
```

Public behavior checks:

{checks}

Public transient contract:

```spectre
tran tran stop=80n maxstep=0.5n
```

## Output Contract

Return exactly {artifact}. Do not include explanatory prose outside the source
file contents. Preserve the module names, ports, saved waveform columns, and
transient simulation contract specified above.
"""


def meta_payload(row: dict[str, str], spec: DesignedSpec, form: str) -> dict[str, object]:
    task_id = f"{row['entry_id']}_{form}"
    family = FORM_TO_FAMILY[form]
    artifacts = {
        "dut": [f"{spec.module}.va"],
        "tb": [f"tb_{spec.module}.scs"],
        "bugfix": ["dut_fixed.va"],
        "e2e": [f"{spec.module}.va", f"tb_{spec.module}.scs"],
    }[form]
    inputs = ["prompt.md"]
    payload: dict[str, object] = {
        "id": task_id,
        "task_id": task_id,
        "asset_type": "vabench_task",
        "benchmark": "vabench-release-v1",
        "release_entry_id": row["entry_id"],
        "family": family,
        "category": row["category"],
        "domain": "voltage",
        "difficulty": "medium" if row["level"] == "L1" else "hard",
        "expected_backend": "evas",
        "inputs": inputs,
        "artifacts": artifacts,
        "scoring": ["dut_compile", "tb_compile", "sim_correct"],
        "behavior_checks": list(spec.behavior_checks),
        "designed_source": True,
    }
    if form == "bugfix":
        payload["inputs"] = ["prompt.md", "gold/dut_buggy.va"]
        payload["public_inputs"] = ["prompt.md", "gold/dut_buggy.va"]
        payload["submission_artifacts"] = ["dut_fixed.va"]
        payload["private_reference_artifacts"] = ["gold/dut_fixed.va"]
    return payload


def checks_text(spec: DesignedSpec, form: str) -> str:
    if form == "tb":
        must_include = ['"tran"', '"save"']
    else:
        must_include = ['"transition("']
        if spec.profile in {"pulse_stretcher"}:
            must_include.append('"@(timer("')
        elif spec.profile != "weighted_dac":
            must_include.append('"@(cross("')
    checks = "\n".join(f"    - {token}" for token in must_include)
    behavior = "\n".join(f"    - \"{item}\"" for item in spec.behavior_checks)
    return f"""syntax:
  must_include:
{checks}
  must_not_include:
    - "I("
    - "ddt("
dut_compile:
  backend: "evas"
tb_compile:
  backend: "evas"
sim_correct:
  checks:
{behavior}
parity:
  reference: "spectre"
  status: "pending_until_evas_spectre_rerun"
  notes:
    - "Designed release source; no imported historical EVAS/Spectre dual evidence yet."
"""


def write_form_assets(entry_dir: Path, row: dict[str, str], spec: DesignedSpec, form: str) -> dict[str, object]:
    form_dir = entry_dir / "forms" / form
    gold_dir = form_dir / "gold"
    gold_dir.mkdir(parents=True, exist_ok=True)
    (form_dir / "prompt.md").write_text(prompt_text(row, spec, form), encoding="utf-8")
    (form_dir / "meta.json").write_text(json.dumps(meta_payload(row, spec, form), indent=2) + "\n", encoding="utf-8")
    (form_dir / "checks.yaml").write_text(checks_text(spec, form), encoding="utf-8")
    gold_files: list[Path] = []
    if form in {"dut", "e2e"}:
        path = gold_dir / f"{spec.module}.va"
        path.write_text(va_source(spec.module, spec.profile), encoding="utf-8")
        gold_files.append(path)
    if form in {"tb", "e2e"}:
        path = gold_dir / f"tb_{spec.module}.scs"
        path.write_text(tb_source(spec.module, form), encoding="utf-8")
        gold_files.append(path)
    if form == "bugfix":
        buggy = gold_dir / "dut_buggy.va"
        fixed = gold_dir / "dut_fixed.va"
        buggy.write_text(va_source(spec.module, spec.profile, buggy=True), encoding="utf-8")
        fixed.write_text(va_source(spec.module, spec.profile), encoding="utf-8")
        gold_files.extend([buggy, fixed])
    (form_dir / "SOURCE_TASK.md").write_text(
        "\n".join(
            [
                f"# Designed Release Source: {row['entry_id']} {form}",
                "",
                f"- Source: `designed_release_spec:{row['entry_id']}`",
                f"- Behavior: {spec.summary}",
                "- EVAS/Spectre status: pending rerun",
                "",
                "This form was materialized directly from the release taxonomy",
                "because no existing source task matched the requested function.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return {
        "form": form,
        "release_path": rel(form_dir),
        "prompt": rel(form_dir / "prompt.md"),
        "meta": rel(form_dir / "meta.json"),
        "checks": rel(form_dir / "checks.yaml"),
        "gold": [rel(path) for path in gold_files],
        "public_inputs": ["prompt.md", "gold/dut_buggy.va"] if form == "bugfix" else ["prompt.md"],
        "submission_artifacts": ["dut_fixed.va"] if form == "bugfix" else meta_payload(row, spec, form)["artifacts"],
        "private_reference_artifacts": ["gold/dut_fixed.va"] if form == "bugfix" else [],
        "asset_materialized": True,
        "historical_dual_expected": False,
        "static_status": "pending",
        "evas_status": "pending",
        "spectre_status": "pending",
        "dual_evidence": f"benchmark-vabench-release-v1/evidence/dual/{row['entry_id']}/{form}/evidence.json",
        "fresh_dual_rerun_required": True,
        "source_path": f"designed_release_spec:{row['entry_id']}",
    }


def materialize_entry(row: dict[str, str], spec: DesignedSpec, *, refresh_existing: bool = False) -> bool:
    entry_path = TASKS_ROOT / row["entry_id"] / "release_entry.json"
    if not entry_path.exists():
        return False
    entry = json.loads(entry_path.read_text(encoding="utf-8"))
    if entry.get("release_tasks") and not refresh_existing:
        return False
    entry_dir = entry_path.parent
    forms = required_forms(row)
    release_tasks = [write_form_assets(entry_dir, row, spec, form) for form in forms]
    entry["canonical_kernel"] = spec.module
    entry["source_registry_status"] = "designed_from_release_taxonomy"
    entry["source_evidence_status"] = "designed_source_pending_dual"
    entry["source_tasks"] = [
        {
            "form": form,
            "source_path": f"designed_release_spec:{row['entry_id']}",
            "prompt": True,
            "meta": True,
            "checks": True,
            "gold": True,
            "asset_complete": True,
            "checks_has_sim_correct": True,
            "checks_has_parity": True,
            "checks_normalized_for_release": False,
        }
        for form in forms
    ]
    entry["release_tasks"] = release_tasks
    entry["missing_forms"] = []
    entry["release_blockers"] = ["static_validation", "evas_certification", "spectre_certification"]
    entry_path.write_text(json.dumps(entry, indent=2) + "\n", encoding="utf-8")
    (entry_dir / "README.md").write_text(
        "\n".join(
            [
                f"# {row['base_function']}",
                "",
                f"- Entry: `{row['entry_id']}`",
                f"- Level: `{row['level']}`",
                f"- Category: `{row['category']}`",
                f"- Materialized forms: `{', '.join(forms)}`",
                "- Source: designed from the release taxonomy",
                "- Certification: static pending; EVAS/Spectre pending rerun",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return True


def update_selected_manifest(materialized_ids: set[str]) -> None:
    rows = read_csv(SELECTED_MANIFEST_CSV)
    if not rows:
        return
    tracker = {row["entry_id"]: row for row in read_csv(TRACKER_CSV)}
    for row in rows:
        if row["entry_id"] not in materialized_ids:
            continue
        forms = required_forms(tracker[row["entry_id"]])
        row["forms_materialized"] = "|".join(forms)
        row["missing_forms"] = ""
        row["source_paths"] = f"designed_release_spec:{row['entry_id']}"
        row["invalid_source_paths"] = ""
        row["notes"] = "designed release source generated; dual evidence pending rerun"
    write_csv(SELECTED_MANIFEST_CSV, rows)

    materialized = [row for row in rows if row["forms_materialized"]]
    lines = [
        "# vaBench Release Selected Manifest",
        "",
        "Date: 2026-05-15",
        "",
        "This manifest records selected L1/L2 release entries created by the",
        "long-run materializer. Rows without release-ready source tasks are kept",
        "as explicit pending package entries rather than hidden missing work.",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "| --- | ---: |",
        f"| selected entries | {len(rows)} |",
        f"| entries with copied or designed source assets | {len(materialized)} |",
        f"| entries pending source design | {len(rows) - len(materialized)} |",
        "",
        "## Rows",
        "",
        "| Entry | Forms | Missing forms | Source paths | Notes |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['entry_id']}` | `{row['forms_materialized']}` | `{row['missing_forms']}` | `{row['source_paths']}` | {row['notes']} |"
        )
    SELECTED_MANIFEST_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Materialize designed vaBench release source tasks.")
    parser.add_argument(
        "--refresh-existing",
        action="store_true",
        help="Regenerate existing designed release source assets from current templates.",
    )
    args = parser.parse_args()

    rows = read_csv(TRACKER_CSV)
    materialized: set[str] = set()
    for row in rows:
        spec = DESIGNED_SPECS.get(row["entry_id"])
        if spec and materialize_entry(row, spec, refresh_existing=args.refresh_existing):
            materialized.add(row["entry_id"])
    update_selected_manifest(materialized)
    forms = 0
    tracker = {row["entry_id"]: row for row in rows}
    for entry_id in materialized:
        forms += len(required_forms(tracker[entry_id]))
    print(f"materialized designed release entries: {len(materialized)}; forms: {forms}")


if __name__ == "__main__":
    main()
