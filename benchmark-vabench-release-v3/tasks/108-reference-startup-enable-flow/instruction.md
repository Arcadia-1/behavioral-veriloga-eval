# Reference Startup Enable Flow

## Task Contract

Implement the requested Verilog-A artifact for `Reference Startup Enable Flow`.
- Form: `dut`
- Level: `L2`
- Category: `bias_reference_power_management`
- Target artifact(s): `reference_startup_enable_flow.va`

- Target artifact: `reference_startup_enable_flow.va`
- Implement only the requested Verilog-A flow DUT. Do not generate a Spectre testbench, validation logic, or auxiliary test hooks.
- Preserve the public module name, port order, starter parameters, and saved waveform observable names.

## Public Verilog-A Interface

```verilog
module reference_startup_enable_flow(clk, rst, vdd_in, en, out, metric, supply_ok, enable_mon, state_mon, startup_mon);
input clk, rst, vdd_in, en;
output out, metric, supply_ok, enable_mon, state_mon, startup_mon;
electrical clk, rst, vdd_in, en, out, metric, supply_ok, enable_mon, state_mon, startup_mon;
```

Starter parameter declarations are part of the public contract:

- `tr = 100p`: output transition rise/fall time.
- `vth = 0.45`: voltage-coded logic threshold.

## Public Parameter Contract

The public parameters declared by the target artifact are part of the contract and may be overridden by validation harnesses. Preserve their names, defaults, ranges, and meanings:

- `parameter real tr = 100p;` in `reference_startup_enable_flow.va`.
- `parameter real vth = 0.45;` in `reference_startup_enable_flow.va`.

## Required Behavior

- `clk`, `rst`, and `en` are voltage-coded logic signals.
- `vdd_in` is the monitored supply waveform for the reference-startup flow.
- `supply_ok` should expose supply-good detection.
- `enable_mon` should expose the enable latch/command state.
- `state_mon` should expose the off, disabled, startup, and valid flow states as bounded voltage-coded monitor levels.
- `startup_mon` should expose bounded startup progress.
- Hold `out` low when reset is active, supply is not good, or enable is low.
- Once supply is good and enable is asserted, start the reference gradually toward a settled value near 0.55 V.
- Drive `metric` high only after the reference has settled to a valid state.
- A supply dip should reset valid status and startup progress; after the supply returns and enable remains asserted, the flow should recover.
- Keep the model pure voltage-domain behavioral Verilog-A. Do not use branch-current contributions, transistor-level devices, AC/noise analysis, or KCL/KVL regulation loops.

## Modeling Constraints

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one source artifact named `reference_startup_enable_flow.va`.
Do not include explanatory prose outside the source artifact contents.
