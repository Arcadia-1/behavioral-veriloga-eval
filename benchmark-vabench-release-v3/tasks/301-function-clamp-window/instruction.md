# Function Clamp Window

Implement one behavioral Verilog-A DUT file named `function_clamp_window.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

```verilog
module function_clamp_window (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Use a Verilog-A user-defined function named `clamp_window` or an equivalently clear function to compute the sampled value.

On each rising crossing of `clk` through `vth = 0.45` V, sample `V(vin)` and update:

- `out = 0.1` when `vin < 0.1`
- `out = vin` when `0.1 <= vin <= 0.8`
- `out = 0.8` when `vin > 0.8`
- `metric = out / 0.9`

Drive both outputs with `transition(..., 0, tr, tr)` using `tr = 200p`. The model must remain pure voltage-domain behavioral Verilog-A: no `I(...)`, `ddt(...)`, or `idt(...)`.

## Output

Return exactly one source artifact named `function_clamp_window.va`. Do not generate a Spectre testbench for this task.
