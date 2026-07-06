# First Order Lowpass

## Task Contract

Implement the requested Verilog-A artifact for `First Order Lowpass`.
- Form: `dut`
- Level: `L1`
- Category: `baseband_signal_conditioning`
- Target artifact(s): `first_order_lowpass.va`

Implement `first_order_lowpass.va` in Verilog-A.

## Public Verilog-A Interface

Declare module `first_order_lowpass(vin, vout)` with scalar electrical
voltage-domain ports.

## Public Parameter Contract

- `alpha`: low-pass update coefficient, default `0.025`.
- `tr`: output transition smoothing time, default `200p`.

## Required Behavior

- Initialize the internal output state at `0 V`.
- Update the state on a `500 ps` timer as
  `y = y + alpha * (V(vin) - y)`.
- Drive `vout` from the internal state with a smoothed voltage contribution.
- The step response should be monotone, bounded by the input level, and visibly
  slower than an instantaneous copy of `vin`.

## Modeling Constraints

Return only `first_order_lowpass.va`. Do not emit a Spectre testbench, validation harness
logic, validation-only hooks, or simulator-specific side channels. Use voltage
contributions only; do not use current contributions, `ddt()`, or `idt()`.

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one complete source artifact named `first_order_lowpass.va`. Do not include explanatory prose outside the source artifact contents.
