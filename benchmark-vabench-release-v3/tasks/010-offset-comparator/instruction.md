# Offset Comparator

## Task Contract

Implement the requested Verilog-A artifact for `Offset Comparator`.
- Form: `dut`
- Level: `L1`
- Category: `comparator_decision`
- Target artifact(s): `cmp_offset_ref.va`

Implement a clocked voltage-domain comparator with a positive input-referred
offset.

## Public Verilog-A Interface

Declare module `cmp_offset_ref` with positional ports `VDD, VSS, CLK, VINP,
VINN, OUT_P`. All ports are electrical. `VDD` and `VSS` are supply rails, `CLK`
is the sampling clock, `VINP` and `VINN` are the differential analog inputs,
and `OUT_P` is the voltage-coded latched decision output.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vos = 5m V`: positive input-referred offset threshold.
- `tt = 20p`: transition smoothing time for `OUT_P`.

## Required Behavior

- Initialize `OUT_P` low relative to `VSS`.
- On each rising crossing of `CLK` through the voltage-coded logic midpoint,
  latch whether `V(VINP,VSS) - V(VINN,VSS)` is greater than `vos`.
- Drive `OUT_P` high to the `VDD` rail only for latched inputs above the
  positive offset threshold; otherwise drive it low to `VSS`.
- Hold the latched decision between rising clock edges, even if the input
  polarity changes between samples.
- Use smoothed rail-referenced voltage-domain output transitions.

## Modeling Constraints

Return only `cmp_offset_ref.va`. Use voltage contributions only. Do not modify
or emit the support testbench, add validation logic, hard-code waveform sample
points, add simulator-specific side channels, use current contributions,
`ddt()`, or `idt()`. For clocked behavior, update local state in analog event
blocks and place the output voltage contribution outside those event blocks.

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one complete source artifact named `cmp_offset_ref.va`. Do not include explanatory prose outside the source artifact contents.
