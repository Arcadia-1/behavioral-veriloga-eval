# Slew Rate Limiter

Implement `slew_rate_limiter.va` in Verilog-A.

## Public Interface

Declare module `slew_rate_limiter(vin, vout)` with scalar electrical
voltage-domain ports.

## Public Parameter Contract

- `step`: maximum internal output change per update, default `0.015`.
- `tr`: output transition smoothing time, default `200p`.

## Functional Contract

- Initialize the internal output state at `0 V`.
- Update the state on a `1 ns` timer.
- On each update, move the internal state toward `V(vin)` by no more than
  `step`.
- Limit both rising and falling changes; if `V(vin)` is within one `step` of
  the internal state, the state may settle directly to `V(vin)`.
- Drive `vout` from the internal state with a smoothed voltage contribution.
- The response should eventually reach both high and low input levels while
  remaining visibly slower than an instantaneous copy of `vin`.

The visible testbench is a public verification scenario for wiring and saved
observables. Do not hard-code its transient stop time, waveform breakpoints, or
sample windows into the DUT.

## Modeling Constraints

Return only `slew_rate_limiter.va`. Do not emit a Spectre testbench, checker
logic, private test hooks, or simulator-private side channels. Use voltage
contributions only; do not use current contributions, `ddt()`, or `idt()`.
