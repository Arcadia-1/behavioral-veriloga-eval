# Resettable Integrator

Implement `resettable_integrator.va` in Verilog-A.

## Public Interface

Declare module `resettable_integrator(vin, rst, vout)` with scalar electrical
voltage-domain ports. `rst` is a voltage-coded control input.

## Public Parameter Contract

- `vth`: reset logic threshold, default `0.45`.
- `gain`: integration gain in inverse seconds, default `1.0e9`.
- `dt`: timer update interval, default `1n`.
- `vmax`: accumulator clamp level, default `0.85`.
- `tr`: output transition smoothing time, default `500p`.

## Functional Contract

- Initialize the internal accumulator to `0 V`.
- Update state only on `@(timer(0, dt))`.
- Treat reset as active high when `V(rst) > vth`; while reset is active, force
  the accumulator and `vout` toward `0 V`.
- When reset is low, add `gain * V(vin) * dt` to the accumulator on each timer
  event.
- Clamp the accumulator to the closed range from `0 V` to `vmax`.
- After reset deasserts, integration must restart from `0 V` using the same
  update rule.
- Drive `vout` from the accumulator with a smoothed voltage contribution.

The visible testbench is a public verification scenario for wiring and saved
observables. Do not hard-code its transient stop time, waveform breakpoints, or
sample windows into the DUT.

## Modeling Constraints

Return only `resettable_integrator.va`. Do not emit a Spectre testbench,
checker logic, private test hooks, or simulator-private side channels. Use
voltage contributions only; do not use current contributions, `ddt()`, or
`idt()`.
