# Above Window Qualifier

## Task Contract

Implement one behavioral Verilog-A DUT file named `above_window_qualifier.va`.

This task focuses on `above()` threshold latching plus bounded `last_crossing()` interval qualification. The DUT is a reusable voltage-domain behavioral helper and must be implemented in Verilog-A.

Build a threshold latch and timing-window qualifier for pairs of rising input threshold crossings.

For Spectre compatibility, call `last_crossing` with the supported crossing-expression and direction arguments, for example `last_crossing(V(vin) - vth, +1)`. Do not use extra tolerance arguments on `last_crossing`.

## Public Verilog-A Interface

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

## Public Parameter Contract

- Use `vth = 0.45` V.
- Use high output level `vhi = 0.9` V.
- Use transition edge time `tr = 200p`.
- Use `last_crossing(V(vin) - vth, +1)` to obtain the most recent rising crossing time.
- The accepted timing window is from `120 ns` through `260 ns` inclusive.

## Required Behavior

- `@(above(V(vin) - vth))` sets a latch.
- On each rising crossing of `V(vin) - vth`, compute the interval from the previous recorded rising crossing.
- Drive `metric = vhi` only when the interval is at least `120 ns` and at most `260 ns`; otherwise drive `metric = 0.0`.
- On a rising reset crossing, clear the latch, metric, and stored crossing time.
- Drive `out = vhi` when the latch is set, otherwise `0.0`.
- Smooth `out` and `metric` with `transition(..., 0.0, tr, tr)`.

## Modeling Constraints

- Keep the model pure voltage-domain behavioral Verilog-A.
- Do not instantiate transistor-level devices.
- Do not use current-domain `I(...)` branch contributions.
- Use voltage-coded logic; treat voltages above `vth` as logic high where a threshold is specified.

## Output Contract

Return exactly one source artifact named `above_window_qualifier.va`. Do not generate a Spectre testbench for this task.
