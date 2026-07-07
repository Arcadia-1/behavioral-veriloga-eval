# Function Clamp Window

## Task Contract

Implement one behavioral Verilog-A DUT file named `function_clamp_window.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Use a Verilog-A analog function named `clamp_window` or an equivalently clear helper function to compute the sampled value.

For Spectre compatibility, declare analog function arguments in Cadence-style Verilog-A form, for example `input x; real x;`, rather than ANSI-style `input real x;`.

## Public Verilog-A Interface

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

## Public Parameter Contract

Use voltage-coded logic with `vth = 0.45` V and high-level scale `vhi = 0.9` V. Drive output transitions with rise/fall time `tr = 200p`. These values may be implemented as compatible Verilog-A parameters or internal constants.

## Required Behavior

On each rising crossing of `clk` through `vth`, sample `V(vin)` and update:

- `out = 0.1` when `vin < 0.1`
- `out = vin` when `0.1 <= vin <= 0.8`
- `out = 0.8` when `vin > 0.8`
- `metric = out / vhi`

## Modeling Constraints

Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices, do not use current-domain `I(...)` branch contributions, and do not use `ddt(...)` or `idt(...)`. Drive both outputs with `transition(..., 0, tr, tr)`.

## Output Contract

Return exactly one source artifact named `function_clamp_window.va`. Do not generate a Spectre testbench for this task.
