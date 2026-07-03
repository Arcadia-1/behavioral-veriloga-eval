# Above Threshold Latch

## Task Contract

Implement one behavioral Verilog-A DUT file named `above_threshold_latch.va`.

This task focuses on `above()` threshold detection plus `last_crossing()` timing classification. The DUT is a reusable voltage-domain behavioral helper and must be implemented in Verilog-A.

## Form-Specific Requirements

Build a threshold latch that remains asserted after an input threshold event and uses consecutive rising crossing times to classify close event spacing.

## Public Verilog-A Interface

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

## Public Parameter Contract

- Use `vth = 0.45` V.
- Use high output level `vhi = 0.9` V.
- Use transition edge time `tr = 200p`.
- Use `last_crossing(V(vin) - vth, +1)` to obtain the most recent rising crossing time.
- Treat two consecutive rising crossings less than `250 ns` apart as a close pair.

## Required Behavior

- `@(above(V(vin) - vth))` sets the latch.
- On each rising crossing of `V(vin) - vth`, record the latest crossing time from `last_crossing()`.
- Drive `metric = vhi` when the current and previous rising crossing times are less than `250 ns` apart; otherwise drive `metric = 0.0`.
- On a rising reset crossing, clear the latch, metric, and stored crossing time.
- Drive `out = vhi` when the latch is set, otherwise `0.0`.
- Smooth `out` and `metric` with `transition(..., 0.0, tr, tr)`.

## Modeling Constraints

- Keep the model pure voltage-domain behavioral Verilog-A.
- Do not instantiate transistor-level devices.
- Do not use current-domain `I(...)` branch contributions.
- Use voltage-coded logic; treat voltages above `vth` as logic high where a threshold is specified.

## Output Contract

Return exactly one source artifact named `above_threshold_latch.va`. Do not generate a Spectre testbench for this task.
