# For Loop Code Popcount

## Task Contract

Implement one behavioral Verilog-A DUT file named `for_loop_code_popcount.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Public Verilog-A Interface

```verilog
module for_loop_code_popcount (
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

Use a Verilog-A `for` loop over a four-entry integer array to compute a voltage-coded popcount.

On a rising crossing of `clk` through `vth = 0.45` V:

- if `rst` is high, clear all bits, clear the count, and drive both outputs to zero
- otherwise derive four bits:
  - `bits[0] = 1` when `vin > 0.20`
  - `bits[1] = 1` when `vin > 0.60`
  - `bits[2] = 1` when `mode > 0.20`
  - `bits[3] = 1` when `mode > 0.60`
- use a `for` loop over `bits[0:3]` to compute `count_q`
- drive `out = 0.9 * count_q / 4.0`
- drive `metric = count_q / 4.0`

A rising `rst` event must also clear the bits immediately. Drive outputs with `transition(..., 0, tr, tr)` using `tr = 200p`. Do not use `I(...)`, `ddt(...)`, or `idt(...)`.

## Modeling Constraints

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

Keep the implementation behavioral and public-interface compatible. Do not add Spectre testbench code, simulator-private hooks, or extra output artifacts.

## Output Contract

Return exactly one source artifact named `for_loop_code_popcount.va`. Do not generate a Spectre testbench for this task.
