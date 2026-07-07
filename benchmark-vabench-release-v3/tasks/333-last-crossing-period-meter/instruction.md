# Last Crossing Period Meter

## Task Contract

Implement one behavioral Verilog-A DUT file named `last_crossing_period_meter.va`.

This task focuses on period measurement using Cadence `last_crossing()`. The DUT is a reusable voltage-domain behavioral helper and must be implemented in Verilog-A.

Build a rising-edge period meter that stores the previous and current threshold crossing times reported by `last_crossing()`.

## Public Verilog-A Interface

```verilog
module last_crossing_period_meter (
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
- Use `last_crossing(V(vin) - vth, +1)` to obtain the latest rising crossing time.
- Scale measured periods by `400 ns` for the `out` voltage.

## Required Behavior

- On the first rising crossing, initialize the previous-crossing state and keep both outputs low.
- On the second and later rising crossings, compute `period_q = last_t - prev_t`.
- Drive `out = vhi * period_q / 400 ns`, clipped to `0.0 ... vhi`.
- Drive `metric = vhi` once a valid period has been measured, otherwise `0.0`.
- On a rising reset crossing, clear the period state and both outputs.
- Smooth `out` and `metric` with `transition(..., 0.0, tr, tr)`.

## Modeling Constraints

- Keep the model pure voltage-domain behavioral Verilog-A.
- Do not instantiate transistor-level devices.
- Do not use current-domain `I(...)` branch contributions.
- Use voltage-coded logic; treat voltages above `vth` as logic high where a threshold is specified.

The visible testbench is a public wiring and smoke scenario. Do not hard-code
its transient stop time, waveform breakpoints, or sample windows into the DUT.
The evaluator checks measured-period voltage and reset clearing behavior across
private timing windows.

## Output Contract

Return exactly one source artifact named `last_crossing_period_meter.va`. Do not generate a Spectre testbench for this task.
