# First Order Lowpass

Implement `first_order_lowpass.va` in Verilog-A.

## Public Interface

Declare module `first_order_lowpass(vin, vout)` with scalar electrical
voltage-domain ports.

## Public Parameter Contract

- `alpha`: low-pass update coefficient, default `0.025`.
- `tr`: output transition smoothing time, default `200p`.

## Functional Contract

- Initialize the internal output state at `0 V`.
- Update the state on a `500 ps` timer as
  `y = y + alpha * (V(vin) - y)`.
- Drive `vout` from the internal state with a smoothed voltage contribution.
- The step response should be monotone, bounded by the input level, and visibly
  slower than an instantaneous copy of `vin`.

## Modeling Constraints

Return only `first_order_lowpass.va`. Do not emit a Spectre testbench, checker
logic, private test hooks, or simulator-private side channels. Use voltage
contributions only; do not use current contributions, `ddt()`, or `idt()`.
