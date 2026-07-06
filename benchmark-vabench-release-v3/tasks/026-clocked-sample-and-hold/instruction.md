# Clocked Sample And Hold

## Task Contract

Implement the requested Verilog-A artifact for `Clocked Sample And Hold`.
- Form: `dut`
- Level: `L1`
- Category: `sampling_analog_memory`
- Target artifact(s): `sample_hold.va`

Implement `sample_hold.va` in Verilog-A.

## Public Verilog-A Interface

Declare module `sample_hold(VDD, VSS, IN, CLK, OUT)` with scalar electrical
voltage-domain ports.

- `VDD`, `VSS`: local supply rails.
- `IN`: analog input voltage to be sampled.
- `CLK`: voltage-coded sampling clock.
- `OUT`: held analog output voltage.

## Public Parameter Contract

- `vth`: clock threshold, default `0.45`.
- `tedge`: output transition smoothing time, default `100p`.

## Required Behavior

- Sample `IN` on each rising `CLK` crossing of `vth`.
- Hold the sampled voltage on `OUT` between rising clock crossings.
- Do not continuously track `IN` while the clock is between sample events.
- Drive `OUT` with smooth voltage-domain `transition(...)` behavior.

## Modeling Constraints

Return only `sample_hold.va`. Do not emit a Spectre testbench, validation logic,
validation-only hooks, or simulator-specific side channels. Use voltage
contributions only; do not use current contributions, `ddt()`, or `idt()`.

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one complete source artifact named `sample_hold.va`. Do not include explanatory prose outside the source artifact contents.
