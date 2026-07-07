# Case Priority Status Decoder

## Task Contract

Implement one behavioral Verilog-A DUT file named `case_priority_status_decoder.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Public Verilog-A Interface

```verilog
module case_priority_status_decoder (
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

Use a Verilog-A `case` statement to decode a priority status code.

On each rising crossing of `clk` through `vth = 0.45` V, compute `state_q` with this priority order:

- if `vin > 0.75`, state `3`
- else if `mode > 0.60`, state `2`
- else if `vin > 0.35`, state `1`
- else state `0`

Use `case (state_q)` to drive `out` and `metric` to `0.00`, `0.30`, `0.60`, or `0.90` V for states `0`, `1`, `2`, and `3`. A high `rst` resets the state and both outputs to zero. Drive outputs with `transition(..., 0, tr, tr)` using `tr = 200p`. Do not use `I(...)`, `ddt(...)`, or `idt(...)`.

## Modeling Constraints

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

Keep the implementation behavioral and public-interface compatible. Do not add Spectre testbench code, simulator-private hooks, or extra output artifacts.

## Output Contract

Return exactly one source artifact named `case_priority_status_decoder.va`. Do not generate a Spectre testbench for this task.
