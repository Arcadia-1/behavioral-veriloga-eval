# Last Crossing Period Meter

Implement one behavioral Verilog-A DUT file named `last_crossing_period_meter.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

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

## Required Behavior

Use `last_crossing()` to measure the period between rising threshold crossings.

This is a pure voltage-domain behavioral task. Do not use current-domain `I(...)` branch contributions.

Use voltage-coded logic with `vth = 0.45` V and high outputs near `0.9` V.

Implement:

- continuously evaluate `lc_q = last_crossing(V(vin) - vth, +1)` using the
  Cadence/Spectre-supported `last_crossing(expr, dir)` form
- `@(cross(V(vin) - vth, +1, 0.0, 1e-12))` records the latest rising crossing time from `lc_q`
- after the first crossing, keep `out = 0.0` and `metric = 0.0`
- after the second and later crossings, compute `period_q = last_t - prev_t`
- drive `out = 0.9 * period_q / 400 ns`, clamped to the range `0.0` to `0.9`
- drive `metric = 0.9` once a valid period has been measured, otherwise `0.0`
- `@(cross(V(rst) - vth, +1))` clears the period state and both outputs

The visible testbench is a public wiring and smoke scenario. Do not hard-code
its transient stop time, waveform breakpoints, or sample windows into the DUT.
The evaluator checks measured-period voltage and reset clearing behavior across
private timing windows.

## Output

Return exactly one source artifact named `last_crossing_period_meter.va`. Do not generate a Spectre testbench for this task.
