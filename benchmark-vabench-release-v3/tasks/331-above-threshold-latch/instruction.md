# Above Threshold Latch

Implement one behavioral Verilog-A DUT file named `above_threshold_latch.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

```verilog
module above_threshold_latch (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Use `above()` to set a threshold latch and `last_crossing()` to classify the timing between rising threshold crossings.

This is a pure voltage-domain behavioral task. Do not use current-domain `I(...)` branch contributions.

Use voltage-coded logic with `vth = 0.45` V and high outputs near `0.9` V.

Implement:

- `@(above(V(vin) - vth))` sets a latch and drives `out` high
- continuously evaluate `lc_q = last_crossing(V(vin) - vth, +1, 0.0, 1e-12)`
- `@(cross(V(vin) - vth, +1, 0.0, 1e-12))` records `lc_q`
- when two consecutive rising crossings are less than `250 ns` apart, drive `metric = 0.9`; otherwise drive `metric = 0.0`
- `@(cross(V(rst) - vth, +1))` clears the latch, metric, and stored crossing time
- drive `out = 0.9` when the latch is set, otherwise `0.0`

The hidden testbench drives two close rising threshold crossings, then asserts reset, then drives one more crossing. The evaluator checks that `out` latches high across a falling input, reset clears it, and `metric` only marks the close pre-reset crossing pair.

## Output

Return exactly one source artifact named `above_threshold_latch.va`. Do not generate a Spectre testbench for this task.
