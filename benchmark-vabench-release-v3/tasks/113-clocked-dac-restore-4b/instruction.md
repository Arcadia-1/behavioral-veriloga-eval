# Clocked DAC Restore 4b

## Task Contract

Implement the requested Verilog-A artifact for `Clocked DAC Restore 4b`.
- Form: `dut`
- Level: `L1`
- Category: `data_converter`
- Target artifact(s): `clocked_dac_restore_4b.va`

Implement a clocked 4-bit mid-rise bipolar DAC reconstruction block.

## Public Verilog-A Interface

Declare module `clocked_dac_restore_4b` with positional ports `D3, D2, D1,
D0, CLK, VOUT`. All ports are electrical. `D3` is the most significant bit and
`D0` is the least significant bit.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vth = 0.45 V`: decision threshold for `CLK` and input bits.
- `lsb = 1.8 / 16 V`: DAC least-significant-bit step.
- `tr = 20 ps`: output transition smoothing time.

## Required Behavior

On each rising `CLK` edge, latch the 4-bit input code. Drive `VOUT` as a
mid-rise bipolar DAC level: the selected level is centered around zero, uses a
half-LSB offset inside each code bin, and spans the nominal `-0.9 V` to `+0.9 V`
range across the 16 codes.

Hold the reconstructed output between clock edges.

## Modeling Constraints

Return only `clocked_dac_restore_4b.va`. Use deterministic voltage-domain
Verilog-A and smooth output transitions. Do not modify or emit the support
testbench, add validation logic, hard-code specific waveform sample points, add
simulator-specific side channels, use current contributions, `ddt()`, or
`idt()`.

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one complete source artifact named `clocked_dac_restore_4b.va`. Do not include explanatory prose outside the source artifact contents.
