# Last Crossing Edge Age

Implement one behavioral Verilog-A DUT file named `last_crossing_edge_age.va`.

This is a language-semantics extension task based on the Cadence Verilog-A Language Reference. Keep the model pure voltage-domain behavioral Verilog-A: do not instantiate transistor-level devices and do not use current-domain `I(...)` branch contributions.

## Interface

```verilog
module last_crossing_edge_age (
    input  electrical vin,
    input  electrical clk,
    input  electrical mode,
    input  electrical rst,
    output electrical out,
    output electrical metric
);
```

## Required Behavior

Use `last_crossing()` to report the age of the most recent rising threshold crossing.

This is a pure voltage-domain behavioral task. Do not use current-domain `I(...)` branch contributions.

Use voltage-coded logic with `vth = 0.45` V and high outputs near `0.9` V.

Implement:

- continuously evaluate `lc_q = last_crossing(V(vin) - vth, +1)` using the
  Cadence/Spectre-supported `last_crossing(expr, dir)` form
- use `@(above(V(vin) - vth))` to mark that at least one rising threshold event has occurred
- before any rising crossing, drive both outputs to `0.0`
- on `@(timer(0, 50n))`, after a rising crossing, compute `age_q = $abstime - lc_q`
- drive `out = 0.9 * age_q / 300 ns`, clamped to `0.0 ... 0.9`
- drive `metric = 0.9` while `age_q <= 150 ns`, otherwise `0.0`
- `@(cross(V(rst) - vth, +1))` clears the observed-edge state and both outputs

The visible testbench is a public wiring and smoke scenario. Do not hard-code
its transient stop time, waveform breakpoints, or sample windows into the DUT.
The evaluator checks the age ramp, short-age marker, and reset clearing behavior
across private timing windows.

## Output

Return exactly one source artifact named `last_crossing_edge_age.va`. Do not generate a Spectre testbench for this task.
