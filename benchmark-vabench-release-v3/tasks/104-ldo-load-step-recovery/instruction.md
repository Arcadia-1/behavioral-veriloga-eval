# LDO Load-Step Recovery Flow

## Task Contract

Implement the requested Verilog-A artifact for `LDO Load Step Recovery`.
- Form: `dut`
- Level: `L2`
- Category: `bias_reference_power_management`
- Target artifact(s): `ldo_load_step_recovery_flow.va`

- Target artifact: `ldo_load_step_recovery_flow.va`
- Implement only the requested Verilog-A flow DUT. Do not generate a Spectre testbench, validation logic, or auxiliary test hooks.
- Preserve the public module name, port order, starter parameters, and saved waveform observable names.

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

## Public Parameter Contract

The public parameters declared by the target artifact are part of the contract and may be overridden by validation harnesses. Preserve their names, defaults, ranges, and meanings:

- `parameter real tr = 100p;` in `ldo_load_step_recovery_flow.va`.
- `parameter real vth = 0.45;` in `ldo_load_step_recovery_flow.va`.

## Required Behavior

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

## Modeling Constraints

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one source artifact named `ldo_load_step_recovery_flow.va`.
Do not include explanatory prose outside the source artifact contents.
