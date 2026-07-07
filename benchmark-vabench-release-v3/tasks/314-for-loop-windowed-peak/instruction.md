# For Loop Windowed Peak

## Task Contract

Implement one behavioral Verilog-A DUT file named `for_loop_windowed_peak.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Public Verilog-A Interface

```verilog
module for_loop_windowed_peak (
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

Use a Verilog-A `for` loop over a four-sample history array to compute a windowed peak and trough.

The model keeps `samples[0:3]`, initialized to zero. On a rising crossing of `clk` through `vth = 0.45` V:

- if `rst` is high, clear all samples and drive both outputs to zero
- otherwise shift the history toward older indexes and store the new `V(vin)` in `samples[0]`
- initialize `peak_v` and `min_v` from `samples[0]`
- use a `for` loop over the remaining entries to find the maximum and minimum sample in the four-entry window
- drive `out = peak_v`
- drive `metric = min_v`

A rising `rst` event must also clear the sample history immediately. Drive outputs with `transition(..., 0, tr, tr)` using `tr = 200p`. Do not use `I(...)`, `ddt(...)`, or `idt(...)`.

## Modeling Constraints

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

Keep the implementation behavioral and public-interface compatible. Do not add Spectre testbench code, simulator-private hooks, or extra output artifacts.

## Output Contract

Return exactly one source artifact named `for_loop_windowed_peak.va`. Do not generate a Spectre testbench for this task.
