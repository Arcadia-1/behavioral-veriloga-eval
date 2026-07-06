# Offset Gain Amplifier

## Task Contract

Implement the requested Verilog-A artifact for `Offset Gain Amplifier`.
- Form: `dut`
- Level: `L1`
- Category: `mixed_signal`
- Target artifact(s): `offset_gain_amplifier.va`

- Base function: Single-ended offset-correcting gain stage
- Domain: `voltage`
- Output boundary: validation logic is external; do not generate validation harness or testbench, or measurement helper artifacts.

## Public Verilog-A Interface

`offset_gain_amplifier.va` must declare:

```verilog
module offset_gain_amplifier(sigin, sigout);
input sigin;
output sigout;
electrical sigin, sigout;
```

## Public Parameter Contract

This task has no public parameters.

## Required Behavior

Model a single-ended voltage gain stage that subtracts a 0.2 V input offset before applying a fixed voltage gain of 3.0. Drive `sigout` with the amplified offset-corrected signal.

Use a direct voltage-domain contribution. Do not add rail clipping, filtering, current contributions, transistor devices, or testbench-specific constants.

## Modeling Constraints

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one source artifact named `offset_gain_amplifier.va`.
Do not include explanatory prose outside the source artifact contents.
