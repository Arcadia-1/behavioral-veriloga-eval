# Above Resettable Peak Marker

## Task Contract

Implement one behavioral Verilog-A DUT file named `above_resettable_peak_marker.va`.

This task focuses on `above()`-armed sampled peak tracking. The DUT is a reusable voltage-domain behavioral helper and must be implemented in Verilog-A.

## Form-Specific Requirements

Build a resettable voltage-domain peak marker that arms on an input threshold event and samples the peak on a timer.

## Public Verilog-A Interface

```verilog
module above_resettable_peak_marker (
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
- Use `timer(0, 50n)` for periodic peak sampling after the tracker is armed.

## Required Behavior

- `@(above(V(vin) - vth))` arms the peak tracker.
- While armed, periodically sample `V(vin)` and retain the largest sampled value as `peak_q`.
- Drive `out = vhi` once armed, otherwise `0.0`.
- Drive `metric = peak_q`, clipped to `0.0 ... vhi`.
- On a rising reset crossing, clear the armed state and peak value.
- Smooth `out` and `metric` with `transition(..., 0.0, tr, tr)`.

## Modeling Constraints

- Keep the model pure voltage-domain behavioral Verilog-A.
- Do not instantiate transistor-level devices.
- Do not use current-domain `I(...)` branch contributions.
- Use voltage-coded logic; treat voltages above `vth` as logic high where a threshold is specified.

## Output Contract

Return exactly one source artifact named `above_resettable_peak_marker.va`. Do not generate a Spectre testbench for this task.
