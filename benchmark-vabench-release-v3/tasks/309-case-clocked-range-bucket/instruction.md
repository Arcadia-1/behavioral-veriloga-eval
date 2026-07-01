# Case Clocked Range Bucket

Implement one behavioral Verilog-A DUT file named `case_clocked_range_bucket.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

```verilog
module case_clocked_range_bucket (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Use a Verilog-A `case` statement to select a range bucket from sampled `vin`, with `mode` adding a small output offset.

On each rising crossing of `clk` through `vth = 0.45` V, compute:

- bucket/state `0` when `vin < 0.30`
- bucket/state `1` when `0.30 <= vin < 0.60`
- bucket/state `2` otherwise
- `mode_hi = 1` when `mode > 0.45`, otherwise `0`

Use `case (state_q)` to update:

- state `0`: `out = 0.10 + 0.10 * mode_hi`, `metric = 0.10`
- state `1`: `out = 0.45 + 0.10 * mode_hi`, `metric = 0.45`
- default/state `2`: `out = 0.80 + 0.05 * mode_hi`, `metric = 0.80`

A high `rst` resets state and outputs to zero. Drive outputs with `transition(..., 0, tr, tr)` using `tr = 200p`. Do not use `I(...)`, `ddt(...)`, or `idt(...)`.

## Output

Return exactly one source artifact named `case_clocked_range_bucket.va`. Do not generate a Spectre testbench for this task.
