# Sample And Hold With Droop Leakage

Implement `leaky_hold.va` in Verilog-A.

## Public Interface

Declare module `leaky_hold(sample, rst, vin, vout)` with scalar electrical
voltage-domain ports.

- `sample`: voltage-coded sample control.
- `rst`: active-high voltage-coded reset.
- `vin`: analog input voltage to be sampled.
- `vout`: held output voltage with leakage.

## Public Parameter Contract

- `vth`: logic threshold, default `0.45`.
- `decay`: held-value multiplier per leakage update, default `0.985`.
- `leak_period`: leakage update interval, default `1n`.
- `tr`: output transition smoothing time, default `500p`.

## Functional Contract

- On each rising `sample` crossing while reset is low, capture the current
  `vin` voltage into the held state.
- While reset is low, apply leakage by periodically multiplying the held state
  by `decay`.
- While reset is high, clear the held state to zero.
- Drive `vout` from the held state with smooth voltage-domain transitions.

## Modeling Constraints

Return only `leaky_hold.va`. Do not emit a Spectre testbench, checker logic,
private test hooks, or simulator-private side channels. Use voltage
contributions only; do not use current contributions, `ddt()`, or `idt()`.
