# Function Deadband Map

Implement one behavioral Verilog-A DUT file named `function_deadband_map.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

```verilog
module function_deadband_map (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Use a Verilog-A user-defined function named `map_value` or an equivalently clear function to implement the deadband transfer curve.

On each rising crossing of `clk` through `vth = 0.45` V, sample `V(vin)` and update:

- `out = 0.0` when `vin < 0.38`
- `out = 0.45` when `0.38 <= vin <= 0.52`
- `out = 0.9` when `vin > 0.52`
- `metric = (out - 0.45) / 0.45`, so the three regions report `-1`, `0`, and `+1`

Drive both outputs with `transition(..., 0, tr, tr)` using `tr = 200p`. The model must remain pure voltage-domain behavioral Verilog-A: no `I(...)`, `ddt(...)`, or `idt(...)`.

## Output

Return exactly one source artifact named `function_deadband_map.va`. Do not generate a Spectre testbench for this task.
