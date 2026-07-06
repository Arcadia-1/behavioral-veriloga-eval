# Clocked DAC 4b Binary

## Task Contract

Implement the requested Verilog-A artifact for `Clocked DAC 4b Binary`.
- Form: `dut`
- Level: `L1`
- Category: `data_converter`
- Target artifact(s): `clocked_dac_4b_binary.va`

The module must be named `clocked_dac_4b_binary` and use this port order:

`D1, D2, D3, D4, CLK, VOUT`

On each rising crossing of `CLK`, latch `D1` as the MSB and `D4` as the LSB.
Drive a mid-rise bipolar output `(code + 0.5) * lsb - 0.9`, where
`lsb = 1.8 / 16`.

## Public Verilog-A Interface

The file `clocked_dac_4b_binary.va` must define `module clocked_dac_4b_binary(D1, D2, D3, D4, CLK, VOUT);`. All ports are electrical. `D1` is the MSB, `D4` is the LSB, `CLK` is the update clock, and `VOUT` is the held analog output.

## Public Parameter Contract

The public parameters declared by `clocked_dac_4b_binary.va` are part of the contract and may be overridden by validation harnesses:

- `parameter real vth = 0.45;`
- `parameter real lsb = 1.8 / 16.0;`

## Required Behavior

On each rising crossing of `CLK` through `vth`, latch the voltage-coded input word with `D1` as the MSB and `D4` as the LSB. Decode high bits as inputs above `vth`, form the unsigned 4-bit code, and drive a held bipolar midrise DAC level `VOUT = (code + 0.5) * lsb - 0.9`. Hold the reconstructed output between clock updates and smooth the output contribution.

## Modeling Constraints

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one complete source artifact named `clocked_dac_4b_binary.va`. Do not include explanatory prose outside the source artifact contents.
