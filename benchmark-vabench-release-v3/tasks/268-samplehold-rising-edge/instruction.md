# Source Samplehold Rising Edge

Implement `samplehold_rising_edge.va` in Verilog-A.

## Public Interface

Declare module `samplehold_rising_edge(control, vin, vout)` with scalar
electrical voltage-domain ports.

- `control`: voltage-coded sampling control.
- `vin`: analog input voltage to be sampled.
- `vout`: held output voltage.

## Public Parameter Contract

- `thresh`: rising-edge control threshold, default `2.5`.
- `tdel`: output transition delay, default `20p`.
- `tr`: output transition rise/fall smoothing time, default `20p`.

## Functional Contract

- Sample `vin` on each rising `control` crossing of `thresh`.
- Hold the sampled voltage on `vout` until the next rising control crossing.
- Do not continuously track `vin` between sample events.
- Drive `vout` with smooth voltage-domain `transition(...)` behavior.

## Modeling Constraints

Return only `samplehold_rising_edge.va`. Do not emit a Spectre testbench,
checker logic, private test hooks, or simulator-private side channels. Use
voltage contributions only; do not use current contributions, `ddt()`, or
`idt()`.
