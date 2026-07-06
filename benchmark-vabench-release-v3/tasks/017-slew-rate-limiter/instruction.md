# Slew Rate Limiter

## Task Contract

Implement the requested Verilog-A artifact for `Slew Rate Limiter`.
- Form: `dut`
- Level: `L1`
- Category: `baseband_signal_conditioning`
- Target artifact(s): `slew_rate_limiter.va`

Implement `slew_rate_limiter.va` in Verilog-A.

## Public Verilog-A Interface

Declare module `slew_rate_limiter(vin, vout)` with scalar electrical
voltage-domain ports.

## Public Parameter Contract

- `step`: maximum internal output change per update, default `0.015`.
- `tr`: output transition smoothing time, default `200p`.

## Required Behavior

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

Return only `slew_rate_limiter.va`. Do not emit a Spectre testbench, validation harness
logic, validation-only hooks, or simulator-specific side channels. Use voltage
contributions only; do not use current contributions, `ddt()`, or `idt()`.

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one complete source artifact named `slew_rate_limiter.va`. Do not include explanatory prose outside the source artifact contents.
