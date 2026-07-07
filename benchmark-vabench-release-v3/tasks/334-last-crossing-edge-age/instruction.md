# Last Crossing Edge Age

## Task Contract

Implement one behavioral Verilog-A DUT file named `last_crossing_edge_age.va`.

This task focuses on edge-age measurement using Cadence `last_crossing()`. The DUT is a reusable voltage-domain behavioral helper and must be implemented in Verilog-A.

Build an age meter that reports elapsed time since the most recent rising threshold crossing.

## Public Verilog-A Interface

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

## Public Parameter Contract

- Use `vth = 0.45` V.
- Use high output level `vhi = 0.9` V.
- Use transition edge time `tr = 200p`.
- Use `last_crossing(V(vin) - vth, +1)` to obtain the latest rising crossing time.
- Use a periodic `timer(0, 50n)` update to refresh the reported age.
- Scale age by `300 ns` for `out`.
- Treat ages up to `150 ns` as short-age events for `metric`.

## Required Behavior

- Use `@(above(V(vin) - vth))` to mark that at least one rising threshold event has occurred.
- Before any rising crossing, drive both outputs to `0.0`.
- On timer updates after a rising crossing, compute `age_q = $abstime - lc_q`.
- Drive `out = vhi * age_q / 300 ns`, clipped to `0.0 ... vhi`.
- Drive `metric = vhi` while `age_q <= 150 ns`, otherwise `0.0`.
- On a rising reset crossing, clear the observed-edge state and both outputs.
- Smooth `out` and `metric` with `transition(..., 0.0, tr, tr)`.

## Modeling Constraints

- Keep the model pure voltage-domain behavioral Verilog-A.
- Do not instantiate transistor-level devices.
- Do not use current-domain `I(...)` branch contributions.
- Use voltage-coded logic; treat voltages above `vth` as logic high where a threshold is specified.

The visible testbench is a public wiring and smoke scenario. Do not hard-code
its transient stop time, waveform breakpoints, or sample windows into the DUT.
The evaluator checks the age ramp, short-age marker, and reset clearing behavior
across private timing windows.

## Output Contract

Return exactly one source artifact named `last_crossing_edge_age.va`. Do not generate a Spectre testbench for this task.
