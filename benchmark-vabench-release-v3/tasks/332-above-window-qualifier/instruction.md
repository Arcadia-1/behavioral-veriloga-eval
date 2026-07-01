# Above Window Qualifier

Implement one behavioral Verilog-A DUT file named `above_window_qualifier.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

```verilog
module above_window_qualifier (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Use `above()` and `last_crossing()` to qualify whether two rising threshold crossings arrive inside a timing window.

This is a pure voltage-domain behavioral task. Do not use current-domain `I(...)` branch contributions.

Use voltage-coded logic with `vth = 0.45` V and high outputs near `0.9` V.

Implement:

- `@(above(V(vin) - vth))` sets a latch and drives `out` high
- continuously evaluate `lc_q = last_crossing(V(vin) - vth, +1, 0.0, 1e-12)`
- `@(cross(V(vin) - vth, +1, 0.0, 1e-12))` records `lc_q`
- when two consecutive rising crossings are separated by at least `120 ns` and at most `260 ns`, drive `metric = 0.9`
- otherwise drive `metric = 0.0`
- `@(cross(V(rst) - vth, +1))` clears the latch, metric, and stored crossing time
- drive `out = 0.9` when the latch is set, otherwise `0.0`

The hidden testbench drives three rising threshold crossings: the second is inside the qualification window and the third is too late after reset. The evaluator checks latch behavior and the bounded timing-window metric.

## Output

Return exactly one source artifact named `above_window_qualifier.va`. Do not generate a Spectre testbench for this task.
