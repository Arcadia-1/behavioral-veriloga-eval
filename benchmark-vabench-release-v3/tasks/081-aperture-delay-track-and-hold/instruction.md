# Aperture Delay Track And Hold

Implement `sample_hold_aperture_ref.va` in Verilog-A.

## Public Interface

Declare module `sample_hold_aperture_ref(VDD, VSS, clk, vin, vout)` with
scalar electrical voltage-domain ports. `clk` is a voltage-coded control input.

## Public Parameter Contract

- `vth`: clock threshold, default `0.45`.
- `taperture`: aperture delay after a rising clock edge, default `200p`.
- `tedge`: output transition smoothing time, default `50p`.

## Functional Contract

- Initialize the held value from the initial value of `vin`.
- On each rising `clk` transition, arm a sample for `$abstime + taperture`.
- At the delayed aperture instant, capture the current value of `vin`.
- Hold the captured value on `vout` until the next delayed sample.
- Drive `vout` with smooth voltage-domain transitions.

## Modeling Constraints

Return only `sample_hold_aperture_ref.va`. Do not emit a Spectre testbench,
checker logic, private test hooks, or simulator-private side channels. Use
voltage contributions only; do not use current contributions, `ddt()`, or
`idt()`.
