# Function Soft Threshold

Implement one behavioral Verilog-A DUT file named `function_soft_threshold.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

```verilog
module function_soft_threshold (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Use a Verilog-A user-defined function named `soft_threshold` or an equivalently clear function to implement a smooth threshold curve.

On each rising crossing of `clk` through `vth = 0.45` V, sample `V(vin)` and update:

- `out = 0.45 + 0.45 * tanh(8.0 * (vin - 0.45))`
- `metric = out`

Drive both outputs with `transition(..., 0, tr, tr)` using `tr = 200p`. The model must remain pure voltage-domain behavioral Verilog-A: no `I(...)`, `ddt(...)`, or `idt(...)`.

## Output

Return exactly one source artifact named `function_soft_threshold.va`. Do not generate a Spectre testbench for this task.
