# For Loop Weighted Accumulator

Implement one behavioral Verilog-A DUT file named `for_loop_weighted_accumulator.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

```verilog
module for_loop_weighted_accumulator (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Use a Verilog-A `for` loop over array state to implement a four-tap weighted accumulator.

The model keeps `samples[0:3]` and `weights[0:3] = {4.0, 3.0, 2.0, 1.0}`, all initialized in `initial_step`. On a rising crossing of `clk` through `vth = 0.45` V:

- if `rst` is high, clear all samples and drive both outputs to zero
- otherwise shift the history toward older indexes and store the new `V(vin)` in `samples[0]`
- use a `for` loop over all four taps to compute `acc = sum(samples[i] * weights[i])`
- drive `out = acc / 10.0`
- drive `metric = acc`

A rising `rst` event must also clear the sample history immediately. Drive outputs with `transition(..., 0, tr, tr)` using `tr = 200p`. Do not use `I(...)`, `ddt(...)`, or `idt(...)`.

## Output

Return exactly one source artifact named `for_loop_weighted_accumulator.va`. Do not generate a Spectre testbench for this task.
