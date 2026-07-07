# Case Mode Gain Selector

## Task Contract

Implement one behavioral Verilog-A DUT file named `case_mode_gain_selector.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Public Verilog-A Interface

```verilog
module case_mode_gain_selector (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Public Parameter Contract

Use the public parameter names, default values, legal ranges, filenames, and thresholds stated in the required behavior below. Do not add task-private configuration ports or extra configuration parameters.

## Required Behavior

Use a Verilog-A `case` statement to select one of four clocked gain modes.

On each rising crossing of `clk` through `vth = 0.45` V, sample `V(mode)` and convert it to an integer state:

- state `0` when `mode < 0.225`
- state `1` when `0.225 <= mode < 0.45`
- state `2` when `0.45 <= mode < 0.675`
- state `3` otherwise

Then use `case (state_q)` to update:

- state `0`: `out = 0.20 * vin`, `metric = 0.00`
- state `1`: `out = 0.50 * vin`, `metric = 0.30`
- state `2`: `out = 0.75 * vin`, `metric = 0.60`
- default/state `3`: `out = vin`, `metric = 0.90`

When `rst` crosses high or is high during a clock event, reset state and both outputs to zero. Drive outputs with `transition(..., 0, tr, tr)` using `tr = 200p`. Do not use `I(...)`, `ddt(...)`, or `idt(...)`.

## Modeling Constraints

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

Keep the implementation behavioral and public-interface compatible. Do not add Spectre testbench code, simulator-private hooks, or extra output artifacts.

## Output Contract

Return exactly one source artifact named `case_mode_gain_selector.va`. Do not generate a Spectre testbench for this task.
