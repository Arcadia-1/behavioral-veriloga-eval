# Case Resettable State Decoder

Implement one behavioral Verilog-A DUT file named `case_resettable_state_decoder.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

```verilog
module case_resettable_state_decoder (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Use a Verilog-A `case` statement to decode a resettable clocked state machine.

The model keeps an integer `state_q` initialized to zero. On each rising crossing of `clk` through `vth = 0.45` V:

- if `rst` is high, reset `state_q`, `out`, and `metric` to zero
- otherwise, when `mode > 0.45`, advance `state_q` by one, wrapping from `3` back to `0`
- when `mode <= 0.45`, hold the current state

Use `case (state_q)` to drive both `out` and `metric` to `0.00`, `0.30`, `0.60`, or `0.90` V for states `0`, `1`, `2`, and `3`. A rising `rst` event must also reset the state immediately. Drive outputs with `transition(..., 0, tr, tr)` using `tr = 200p`. Do not use `I(...)`, `ddt(...)`, or `idt(...)`.

## Output

Return exactly one source artifact named `case_resettable_state_decoder.va`. Do not generate a Spectre testbench for this task.
