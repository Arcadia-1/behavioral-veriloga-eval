# LDO Load-Step Recovery Flow

## Task Contract

- Form: `dut`
- Level: `L2`
- Category: Bias Reference and Power Management
- Target artifact: `ldo_load_step_recovery_flow.va`
- Implement only the requested Verilog-A flow DUT. Do not generate a Spectre testbench, checker logic, or auxiliary test hooks.
- Preserve the public module name, port order, starter parameters, and saved waveform observable names.
- The visible testbench is a public smoke scenario. Use it to understand wiring and observables, but do not hard-code its stop time, maxstep, or exact waveform breakpoints into the DUT behavior.

## Public Verilog-A Interface

```verilog
module ldo_load_step_recovery_flow(clk, rst, vin, out, metric, load_mon, ctrl_mon);
input clk, rst, vin;
output out, metric, load_mon, ctrl_mon;
electrical clk, rst, vin, out, metric, load_mon, ctrl_mon;
```

Starter parameter declarations are part of the public contract:

- `tr = 100p`: output transition rise/fall time.
- `vth = 0.45`: voltage-coded logic threshold.

## Public Behavioral Contract

- `clk` and `rst` are voltage-coded logic signals.
- Treat `vin` as a bounded load-step request for a behavioral LDO recovery flow.
- `load_mon` should track the bounded load request seen by the regulator macro.
- `ctrl_mon` should expose an abstract voltage-domain pass/recovery control response that rises under heavier load or droop and relaxes after recovery.
- `out` is the regulator output after transient load droop and closed-loop recovery.
- A load increase should produce a visible transient droop in `out`, followed by gradual recovery toward the load-dependent regulation target.
- A load reduction should allow `out` to recover upward toward the light-load target.
- Repeated load steps should reset recovery observation and then settle again.
- Drive `metric` high only after the flow has recovered regulation following a load transition.
- Keep the model pure voltage-domain behavioral Verilog-A. Do not use branch-current contributions, transistor-level devices, AC/noise analysis, or KCL/KVL regulation loops.

## Public Observables

Verification scenarios observe these scalar waveforms:

```text
clk rst vin out metric load_mon ctrl_mon
```

Expected behavior categories:

- `load_step_transient_droop_visible`
- `closed_loop_recovery_after_step`
- `metric_marks_recovered_regulation`
- `load_monitor_tracks_step`
- `control_monitor_responds_to_droop`

## Output Contract

Return exactly one source artifact named `ldo_load_step_recovery_flow.va`.
Do not include explanatory prose outside the source artifact contents.
