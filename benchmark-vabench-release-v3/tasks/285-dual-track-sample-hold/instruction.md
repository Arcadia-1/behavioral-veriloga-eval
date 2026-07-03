# Dual Track Sample Hold

Implement `dual_track_sample_hold.va` in Verilog-A.

## Public Interface

Declare module `dual_track_sample_hold(vdd, vss, clk, vin, vout, phase)` with
scalar electrical voltage-domain ports.

- `vdd`, `vss`: local supply rails.
- `clk`: voltage-coded clock/control input.
- `vin`: analog input to be sampled.
- `vout`: held analog output.
- `phase`: voltage-coded monitor that is high while the output stage is in its
  track phase and low while the output stage is holding.

## Public Parameter Contract

- `vth`: clock threshold, default `0.45`.
- `tick`: internal behavioral update interval, default `0.5n`.
- `alpha_in`: first-stage tracking fraction per update, default `0.45`.
- `alpha_out`: output-stage tracking fraction per update, default `0.55`.
- `tedge`: output transition smoothing time, default `50p`.
- `vinit`: initial stored voltage, default `0.0`.

## Functional Contract

Model a dual complementary track/hold sample-and-hold cell:

- During the low clock phase, the input stage tracks `vin` with finite
  acquisition bandwidth while the output stage holds its previous value.
- On the rising clock transition, the input stage stops tracking and retains the
  value acquired during the preceding low phase.
- During the high clock phase, the output stage tracks the retained input-stage
  value with finite output bandwidth.
- On the falling clock transition, the output stage holds its current value
  until the next high clock phase.
- Clamp stored stage values to the local `vss`-to-`vdd` voltage range.
- Drive `vout` and `phase` with smooth voltage-domain transitions.

## Modeling Constraints

Return only `dual_track_sample_hold.va`. Do not emit a Spectre testbench,
checker logic, private test hooks, or simulator-private side channels. Use
voltage contributions only; do not use current contributions, `ddt()`, or
`idt()`.
