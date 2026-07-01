# Function Code Normalizer

Implement one behavioral Verilog-A DUT file named `function_code_normalizer.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

```verilog
module function_code_normalizer (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Use a Verilog-A user-defined function named `normalize4` or an equivalently clear function to quantize the sampled input into a 4-bit normalized code.

On each rising crossing of `clk` through `vth = 0.45` V, sample `V(vin)` and update:

- Clamp the sampled value to the input range `[0.0, 0.9]`
- Compute `code = floor(16 * vin / 0.9)`, then clamp `code` to `[0, 15]`
- `out = code / 15.0 * 0.9`
- `metric = out / 0.9`

Drive both outputs with `transition(..., 0, tr, tr)` using `tr = 200p`. The model must remain pure voltage-domain behavioral Verilog-A: no `I(...)`, `ddt(...)`, or `idt(...)`.

## Output

Return exactly one source artifact named `function_code_normalizer.va`. Do not generate a Spectre testbench for this task.
