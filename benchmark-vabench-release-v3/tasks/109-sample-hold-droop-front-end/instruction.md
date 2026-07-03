# Sample Hold Droop Front End

Implement `sample_hold_droop_ref.va` in Verilog-A.

## Public Interface

Declare module `sample_hold_droop_ref(vdd, vss, clk, vin, vout, valid, coarse)`
with scalar electrical voltage-domain ports.

- `vdd`, `vss`: local supply rails.
- `clk`: voltage-coded sampling clock.
- `vin`: analog input voltage.
- `vout`: sampled output voltage with bounded hold droop.
- `valid`: voltage-coded pulse indicating a completed sample.
- `coarse`: voltage-coded coarse decision derived from the held sample.

## Public Parameter Contract

- `vth`: clock and decision threshold, default `0.45`.
- `trf`: output transition smoothing time, default `40p`.
- `tau`: droop time constant, default `90n`.
- `dt`: droop update interval, default `0.5n`.
- `taperture`: sampling aperture delay after a rising clock crossing, default
  `200p`.
- `valid_width`: valid-pulse duration after the aperture sample, default `2n`.

## Functional Contract

Model a compact sampling front end:

- On each rising `clk` crossing, schedule a sample after `taperture`.
- At the aperture sample, capture `vin`, clamp the held value to the local
  `vss`-to-`vdd` range, update `vout`, assert `valid`, and update `coarse`.
- `coarse` is high when the sampled value is above `vth` and low otherwise.
- While the clock is low, apply bounded droop to the held output using `tau`
  and `dt`.
- Deassert `valid` after `valid_width`.

## Modeling Constraints

Return only `sample_hold_droop_ref.va`. Do not emit a Spectre testbench,
checker logic, private test hooks, or simulator-private side channels. Use
voltage contributions only; do not use current contributions, `ddt()`, or
`idt()`.
