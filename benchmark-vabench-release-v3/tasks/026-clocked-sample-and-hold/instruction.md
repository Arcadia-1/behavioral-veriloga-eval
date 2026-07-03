# Clocked Sample And Hold

Implement `sample_hold.va` in Verilog-A.

## Public Interface

Declare module `sample_hold(VDD, VSS, IN, CLK, OUT)` with scalar electrical
voltage-domain ports.

- `VDD`, `VSS`: local supply rails.
- `IN`: analog input voltage to be sampled.
- `CLK`: voltage-coded sampling clock.
- `OUT`: held analog output voltage.

## Public Parameter Contract

- `vth`: clock threshold, default `0.45`.
- `tedge`: output transition smoothing time, default `100p`.

## Functional Contract

- Sample `IN` on each rising `CLK` crossing of `vth`.
- Hold the sampled voltage on `OUT` between rising clock crossings.
- Do not continuously track `IN` while the clock is between sample events.
- Drive `OUT` with smooth voltage-domain `transition(...)` behavior.

## Modeling Constraints

Return only `sample_hold.va`. Do not emit a Spectre testbench, checker logic,
private test hooks, or simulator-private side channels. Use voltage
contributions only; do not use current contributions, `ddt()`, or `idt()`.
